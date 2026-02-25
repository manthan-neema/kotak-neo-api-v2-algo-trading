from broker.Kotak import Kotak
from broker.client import Client
from broker.exchanges.MCX import MCX

login = Client()
client = login.get_client()

mcx = MCX(client)
kotak = Kotak(client)

def test_place_buy_order_SILVERMIC_future():
    order_no = mcx.place_buy_order("SILVERMIC30APR26FUT", "","1")
    assert order_no != -1, "Order placement failed (buy future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")

def test_place_sell_order_SILVERMIC_future():
    order_no = mcx.place_sell_order("SILVERMIC30APR26FUT", "","1")
    assert order_no != -1, "Order placement failed (sell future)"

    order_status = kotak.get_order_status(order_no)
    assert (order_status["order_status"] == "complete")