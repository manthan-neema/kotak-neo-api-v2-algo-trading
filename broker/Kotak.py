from time import sleep


class Kotak:

    def __init__(self, client):
        self.client = client

    def get_order_status(self, order_no):
        sleep(1)
        order_report = self.client.order_report()
        print("order_report:", order_report)

        for order in order_report.get("data", []):
            if (str(order.get("nOrdNo")) == str(order_no)):
                order_status = order.get("ordSt")
                order_rejection_reason = order.get("rejRsn")
                order_price = order.get("avgPrc")

                print("order_no:", order_no)
                print("order_status:", order_status)
                print("order_price:", order_price)
                print("order_rejection_reason:", order_rejection_reason)

                return {
                    "order_status": order_status,
                    "order_rejection_reason": order_rejection_reason,
                    "order_price": order_price
                }
        return -1