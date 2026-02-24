class Kotak:

    def __init__(self, client):
        self.client = client

    def get_order_status(self, order_no):
        order_report = self.client.order_report()

        for order_report in order_report.get("data", []):
            if order_report.get("nOrdNo") == order_no:
                order_status = order_report.get("ordSt")
                order_rejection_reason = order_report.get("rejRsn")
                order_price = order_report.get("avgPrc")

                print("order_no:", order_no)
                print("order_status:", order_status)
                print("order_price:", order_price)
                print("order_rejection_reason:", order_rejection_reason)

                return {
                    "order_status": order_status,
                    "order_rejection_reason": order_rejection_reason,
                    "order_price": order_price
                }

        return None