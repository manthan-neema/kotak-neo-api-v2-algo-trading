from broker.Kotak import Kotak
from broker.exchanges.NSE import NSE
from broker.client import Client
login = Client()
client = login.get_client()

nse = NSE(client)
kotak = Kotak(client)

def test_place_buy_order_HDFC_future():
    order_no = nse.place_buy_order("HDFCBANK26MAYFUT", "","550")
    assert order_no != -1, "Order placement failed (buy future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

def test_place_sell_order_HDFC_future():
    order_no = nse.place_sell_order("HDFCBANK26MARFUT", "","550")
    assert order_no != -1, "Order placement failed (sell future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")



# ---------------------------------------------------------
# HDFCBANK26MAR880PE
def test_place_buy_order_HDFC_options():
    order_no = nse.place_buy_order("HDFCBANK26MAR880PE", "","550")
    assert order_no != -1, "Order placement failed (buy option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

def test_place_sell_order_HDFC_options():
    order_no = nse.place_sell_order("HDFCBANK26FEB900PE", "","550")
    assert order_no != -1, "Order placement failed (sell option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")
