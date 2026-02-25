from broker.exchanges.Exchange import Exchange

class MCX(Exchange):

    def __init__(self, client):
        self.exchange_segment = "mcx_fo"
        super().__init__(client)

    def place_buy_order(self, ticker_symbol, limit_price, quantity):
        print("Placing MCX order")
        super().place_buy_order(ticker_symbol, limit_price, quantity)

    def place_sell_order(self, ticker_symbol, limit_price, quantity):
        print("Placing MCX order")
        return super().place_sell_order(ticker_symbol, limit_price, quantity)
