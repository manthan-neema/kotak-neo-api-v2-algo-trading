"""Fetch positions and compute aggregated position metrics.

Usage: python position.py

This module uses the project's `broker.client.Client` to get an authenticated
NeoAPI client and calls `positions()`. It computes:
 - Total Buy Qty, Total Sell Qty, Carry Fwd Qty, Net Qty (and divides by lotSz for F&O)
 - Total Buy Amount, Total Sell Amount
 - Buy Avg Price, Sell Avg Price, selected Avg Price (per rules in docs)
 - PnL using the formula in docs

Numeric parsing uses Decimal to avoid floating-point rounding issues.
"""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext
from typing import Any, Dict, List

# Use broker client to get an authenticated NeoAPI client
from broker.client import Client

# Set a generous decimal context precision
getcontext().prec = 28


def parse_decimal(value: Any, default: Decimal = Decimal("0")) -> Decimal:
    """Safely parse a numeric-ish value (str/int/float) to Decimal.

    Strips commas and whitespace. Returns `default` on None or parse error.
    """
    if value is None:
        return default
    try:
        # Convert booleans to numbers (False->0 True->1) via int
        if isinstance(value, bool):
            return Decimal(int(value))
        # If it's already a Decimal
        if isinstance(value, Decimal):
            return value
        # Convert ints/floats directly to string then Decimal to avoid
        # Decimal(float) floating inaccuracy
        s = str(value).strip()
        if s == "":
            return default
        s = s.replace(",", "")
        return Decimal(s)
    except (InvalidOperation, ValueError, TypeError):
        return default


def quantize_value(d: Decimal, precision: int) -> Decimal:
    """Round Decimal `d` to `precision` decimal places using HALF_UP."""
    if precision < 0:
        precision = 0
    quant = Decimal(1).scaleb(-precision)  # 10**-precision
    try:
        return d.quantize(quant, rounding=ROUND_HALF_UP)
    except InvalidOperation:
        return d


def compute_position_metrics(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Compute required metrics for a single position record.

    Accepts the raw dict returned by the positions API and returns a new dict
    with computed numeric fields (Decimal objects converted to strings).
    """
    # Parse quantities from the response (these may be strings like "10" or "0")
    cfBuyQty = parse_decimal(raw.get("cfBuyQty"))
    flBuyQty = parse_decimal(raw.get("flBuyQty"))
    cfSellQty = parse_decimal(raw.get("cfSellQty"))
    flSellQty = parse_decimal(raw.get("flSellQty"))

    # If lotSz present and > 1, the API expects us to divide these quantities by lotSz
    lotSz = parse_decimal(raw.get("lotSz"), Decimal("1"))
    if lotSz == 0:
        lotSz = Decimal(1)

    # Convert amounts
    buyAmt = parse_decimal(raw.get("buyAmt"))
    cfBuyAmt = parse_decimal(raw.get("cfBuyAmt"))
    sellAmt = parse_decimal(raw.get("sellAmt"))
    cfSellAmt = parse_decimal(raw.get("cfSellAmt"))

    # Price/ratio related
    multiplier = parse_decimal(raw.get("multiplier"), Decimal("1"))
    genNum = parse_decimal(raw.get("genNum"), Decimal("1"))
    genDen = parse_decimal(raw.get("genDen"), Decimal("1"))
    prcNum = parse_decimal(raw.get("prcNum"), Decimal("1"))
    prcDen = parse_decimal(raw.get("prcDen"), Decimal("1"))

    # LTP / last traded price — use 'stkPrc' or fallback to 0
    stkPrc = parse_decimal(raw.get("stkPrc") or raw.get("ltp") or 0)

    # Precision for rounding avg prices
    try:
        precision = int(raw.get("precision") or 2)
    except (TypeError, ValueError):
        precision = 2

    # If lotSz > 1 we divide the raw qty fields by lotSz (as per docs for F&O)
    if lotSz > 1:
        cfBuyQty = cfBuyQty / lotSz
        flBuyQty = flBuyQty / lotSz
        cfSellQty = cfSellQty / lotSz
        flSellQty = flSellQty / lotSz

    # Quantity calculations
    total_buy_qty = cfBuyQty + flBuyQty
    total_sell_qty = cfSellQty + flSellQty
    carry_fwd_qty = cfBuyQty - cfSellQty
    net_qty = total_buy_qty - total_sell_qty

    # Amount calculations
    total_buy_amt = cfBuyAmt + buyAmt
    total_sell_amt = cfSellAmt + sellAmt

    # Denominator factor for converting qty to lots/units (multiplier * genNum/genDen * prcNum/prcDen)
    denom_factor = Decimal(1)
    try:
        denom_factor = multiplier * (genNum / genDen) * (prcNum / prcDen)
    except (InvalidOperation, ZeroDivisionError):
        denom_factor = Decimal(1)

    # Buy and Sell Avg Price safe computation
    def safe_avg_price(total_amt: Decimal, total_qty: Decimal) -> Decimal:
        if total_qty == 0 or denom_factor == 0:
            return Decimal(0)
        try:
            return total_amt / (total_qty * denom_factor)
        except (InvalidOperation, ZeroDivisionError):
            return Decimal(0)

    buy_avg_price = safe_avg_price(total_buy_amt, total_buy_qty)
    sell_avg_price = safe_avg_price(total_sell_amt, total_sell_qty)

    # Final avg price selection per rules
    if total_buy_qty > total_sell_qty:
        avg_price = buy_avg_price
    elif total_buy_qty < total_sell_qty:
        avg_price = sell_avg_price
    else:
        avg_price = Decimal(0)

    # Round prices according to precision
    buy_avg_price_q = quantize_value(buy_avg_price, precision)
    sell_avg_price_q = quantize_value(sell_avg_price, precision)
    avg_price_q = quantize_value(avg_price, precision)

    # PnL calculation: (Total Sell Amt - Total Buy Amt) + (Net qty * LTP * multiplier * (genNum/genDen) * (prcNum/prcDen))
    pnl = (total_sell_amt - total_buy_amt) + (net_qty * stkPrc * denom_factor)
    pnl_q = quantize_value(pnl, precision)

    # Build result dict (convert Decimals to strings to avoid JSON/float surprises)
    res = {
        "symbol": raw.get("sym") or raw.get("trdSym") or raw.get("sym"),
        "raw": raw,
        "cfBuyQty": str(cfBuyQty),
        "flBuyQty": str(flBuyQty),
        "cfSellQty": str(cfSellQty),
        "flSellQty": str(flSellQty),
        "lotSz": str(lotSz),
        "total_buy_qty": str(total_buy_qty),
        "total_sell_qty": str(total_sell_qty),
        "carry_fwd_qty": str(carry_fwd_qty),
        "net_qty": str(net_qty),
        "total_buy_amt": str(total_buy_amt),
        "total_sell_amt": str(total_sell_amt),
        "buy_avg_price": format(buy_avg_price_q, 'f'),
        "sell_avg_price": format(sell_avg_price_q, 'f'),
        "avg_price": format(avg_price_q, 'f'),
        "pnl": format(pnl_q, 'f'),
    }

    return res


def get_positions_and_metrics(client=None) -> List[Dict[str, Any]]:
    """Fetch positions from the API and compute metrics for each position.

    Returns a list of computed position dicts.
    """
    if client is None:
        # Use the broker client singleton to get an authenticated API client
        client = Client().get_client()

    resp = client.positions()
    if not isinstance(resp, dict):
        raise RuntimeError("positions() returned unexpected response type")

    if resp.get("stCode") != 200:
        raise RuntimeError(f"positions() failed: {resp}")

    data = resp.get("data", [])
    results = []
    for rec in data:
        results.append(compute_position_metrics(rec))

    return results


def _print_positions(results: List[Dict[str, Any]]):
    for r in results:
        sym = r.get("symbol")
        print(f"Symbol: {sym}")
        print(f"  Total Buy Qty: {r['total_buy_qty']}")
        print(f"  Total Sell Qty: {r['total_sell_qty']}")
        print(f"  Carry Fwd Qty: {r['carry_fwd_qty']}")
        print(f"  Net Qty: {r['net_qty']}")
        print(f"  Total Buy Amt: {r['total_buy_amt']}")
        print(f"  Total Sell Amt: {r['total_sell_amt']}")
        print(f"  Buy Avg Price: {r['buy_avg_price']}")
        print(f"  Sell Avg Price: {r['sell_avg_price']}")
        print(f"  Selected Avg Price: {r['avg_price']}")
        print(f"  PnL: {r['pnl']}")
        print()


if __name__ == "__main__":
    try:
        res = get_positions_and_metrics()
        _print_positions(res)
    except Exception as e:
        print("Error fetching or computing positions:", e)
