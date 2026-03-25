from broker.Kotak import Kotak
from broker.exchanges.NSE import NSE
from broker.client import Client
login = Client()
client = login.get_client()

nse = NSE(client)
kotak = Kotak(client)

def test_place_buy_order_TCS_future():
    order_no = nse.place_buy_order("TCS26MAYFUT", "","175")
    assert order_no != -1, "Order placement failed (buy future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

def test_place_sell_order_TCS_future():
    order_no = nse.place_sell_order("TCS26MARFUT", "","175")
    assert order_no != -1, "Order placement failed (sell future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

# ----------------------------------------------------------------------
# TCS26MAR860PE
def test_place_buy_order_TCS_options():
    order_no = nse.place_buy_order("TCS26MAR2560PE", "","175")
    assert order_no != -1, "Order placement failed (buy option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

def test_place_sell_order_TCS_options():
    order_no = nse.place_sell_order("TCS26FEB2900PE", "238","175")
    assert order_no != -1, "Order placement failed (sell option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")
