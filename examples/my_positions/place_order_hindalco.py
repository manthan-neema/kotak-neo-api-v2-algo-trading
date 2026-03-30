from broker.Kotak import Kotak
from broker.exchanges.NSE import NSE
from broker.client import Client
login = Client()
client = login.get_client()

nse = NSE(client)
kotak = Kotak(client)

def test_place_buy_order_hindalco_future():
    order_no = nse.place_buy_order("HINDALCO26MAYFUT", "","700")
    assert order_no != -1, "Order placement failed (buy future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

def test_place_sell_order_hindalco_future():
    order_no = nse.place_sell_order("HINDALCO26MARFUT", "","700")
    assert order_no != -1, "Order placement failed (sell future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

# ----------------------------------------------------------------------
# Options
# HINDALCO26MAR860PE
def test_place_buy_order_hindalco_options():
    order_no = nse.place_buy_order("HINDALCO26APR850PE", "20","700")
    assert order_no != -1, "Order placement failed (buy option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

# HINDALCO26APR800PE
def test_place_sell_order_hindalco_options():
    order_no = nse.place_sell_order("HINDALCO26APR800PE", "10.0","700")
    assert order_no != -1, "Order placement failed (sell option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")
