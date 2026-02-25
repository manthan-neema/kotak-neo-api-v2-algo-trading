from abc import ABC, abstractmethod

class Exchange(ABC):

    def __init__(self, client):
        self.client = client
        self.product="NRML"

    @abstractmethod
    def place_buy_order(self, ticker_symbol, limit_price, quantity):
        if (limit_price):
            placed_order = self.client.place_order(exchange_segment=str(self.exchange_segment),
                                              product=str(self.product),
                                              price=str(limit_price),
                                              order_type="L",
                                              quantity=str(quantity),
                                              validity="DAY",
                                              trading_symbol=str(ticker_symbol),
                                              transaction_type="B",
                                              amo="NO",
                                              disclosed_quantity="0",
                                              market_protection="0",
                                              pf="N"
                                              )
        else:
            placed_order = self.client.place_order(exchange_segment=str(self.exchange_segment),
                                              product=str(self.product),
                                              price="0",
                                              order_type="MKT",
                                              quantity=str(quantity),
                                              validity="DAY",
                                              trading_symbol=str(ticker_symbol),
                                              transaction_type="B",
                                              amo="NO",
                                              disclosed_quantity="0",
                                              market_protection="0",
                                              pf="N",
                                              trigger_price="0")

        return self.__get_order_status(placed_order)

    @abstractmethod
    def place_sell_order(self, ticker_symbol, limit_price, quantity):
        if (limit_price):
            placed_order = self.client.place_order(exchange_segment=str(self.exchange_segment),
                                              product=str(self.product),
                                              price=str(limit_price),
                                              order_type="L",
                                              quantity=str(quantity),
                                              validity="DAY",
                                              trading_symbol=str(ticker_symbol),
                                              transaction_type="S",
                                              amo="NO",
                                              disclosed_quantity="0",
                                              market_protection="0",
                                              pf="N"
                                              )
        else:
            placed_order = self.client.place_order(exchange_segment=str(self.exchange_segment),
                                              product=str(self.product),
                                              price="0",
                                              order_type="MKT",
                                              quantity=str(quantity),
                                              validity="DAY",
                                              trading_symbol=str(ticker_symbol),
                                              transaction_type="S",
                                              amo="NO",
                                              disclosed_quantity="0",
                                              market_protection="0",
                                              pf="N",
                                              trigger_price="0")

        return self.__get_order_status(placed_order)



    def __get_order_status(self, placed_order):
        if placed_order.get("stat") == "Ok":
            order_no = placed_order.get("nOrdNo")
            print(f"✅ Order placed successfully. Order No: {order_no}")
            return order_no
        else:
            print("❌ Order failed:", placed_order)
            return -1
