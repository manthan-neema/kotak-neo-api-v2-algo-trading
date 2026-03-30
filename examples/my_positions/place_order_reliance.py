from broker.Kotak import Kotak
from broker.exchanges.NSE import NSE
from broker.client import Client
login = Client()
client = login.get_client()

nse = NSE(client)
kotak = Kotak(client)

def test_place_buy_order_RELIANCE_future():
    order_no = nse.place_buy_order("RELIANCE26MAYFUT", "","500")
    assert order_no != -1, "Order placement failed (buy future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

def test_place_sell_order_RELIANCE_future():
    order_no = nse.place_sell_order("RELIANCE26MARFUT", "","500")
    assert order_no != -1, "Order placement failed (sell future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")


# ---------------------------------------------------------
# Options
# RELIANCE26MAR1690CE
def test_place_buy_order_RELIANCE_options():
    order_no = nse.place_buy_order("RELIANCE26MAR1410PE", "","500")
    assert order_no != -1, "Order placement failed (buy option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

# RELIANCE26APR1400PE
def test_place_sell_order_RELIANCE_options():
    order_no = nse.place_sell_order("RELIANCE26MAR1410PE", "","500")
    assert order_no != -1, "Order placement failed (sell option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")
