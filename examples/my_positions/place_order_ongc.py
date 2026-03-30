from broker.Kotak import Kotak
from broker.exchanges.NSE import NSE
from broker.client import Client
login = Client()
client = login.get_client()

nse = NSE(client)
kotak = Kotak(client)

def test_place_buy_order_ongc_future():
    order_no = nse.place_buy_order("ONGC26MAYFUT", "","2250")
    assert order_no != -1, "Order placement failed (buy future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

def test_place_sell_order_ongc_future():
    order_no = nse.place_sell_order("ONGC26MARFUT", "","2250")
    assert order_no != -1, "Order placement failed (sell future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")





# ------------------------------------
# Options
def test_place_buy_order_ongc_options():
    order_no = nse.place_buy_order("ONGC26APR270PE", "","2250")
    assert order_no != -1, "Order placement failed (buy option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

# ONGC26APR260PE
# ONGC26MAR268.75PE
def test_place_sell_order_ongc_options():
    order_no = nse.place_sell_order("ONGC26MAR268.75PE", "0.05","2250")
    assert order_no != -1, "Order placement failed (sell option)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")
