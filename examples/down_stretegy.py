from broker.client import Client
import time

login = Client()
client= login.get_client()

order_price = int(320000.00)
order_no = 0
order_status = "open"
while(True):

    print("placing sell order at price:", order_price)
    placed_order = client.place_order(exchange_segment="mcx_fo",
                                      product="MIS",
                                      price=str(order_price),
                                      order_type="L",
                                      quantity="1",
                                      validity="DAY",
                                      trading_symbol="SILVERMIC27FEB26FUT",
                                      transaction_type="S",
                                      amo="NO",
                                      disclosed_quantity="0",
                                      market_protection="0",
                                      pf="N"
                                      )

    if placed_order.get("stat") == "Ok":
        order_no = placed_order.get("nOrdNo")
        print(f"✅ Order placed successfully. Order No: {order_no}")
    else:
        print("❌ Order failed:", placed_order.get("nOrdNo"))

    while (order_status != "complete"):
        print("Order Status:", order_status)

        order_report = client.order_report()

        for order_report in order_report.get("data", []):
            if order_report.get("nOrdNo") == order_no:
                print("order report: " + str(order_report))
                order_status = order_report.get("ordSt")
                order_rejection_reason = order_report.get("rejRsn")
                order_status = order_report.get("ordSt")
                order_price = int(float((order_report.get("avgPrc"))))
                break

    print("Order Number:", order_no)
    print("Order Status:", order_status)
    print("Order price:", order_price)
    print("Rejection Reason:", order_rejection_reason)

    order_price -= 300
    order_status = "open"

    print("placing buy order at price:", order_price)
    placed_order = client.place_order(exchange_segment="mcx_fo",
                                      product="MIS",
                                      price=str(order_price),
                                      order_type="L",
                                      quantity="1",
                                      validity="DAY",
                                      trading_symbol="SILVERMIC27FEB26FUT",
                                      transaction_type="B",
                                      amo="NO",
                                      disclosed_quantity="0",
                                      market_protection="0",
                                      pf="N",
                                      trigger_price="0")
    if placed_order.get("stat") == "Ok":
        order_no = placed_order.get("nOrdNo")
        print(f"✅ Order placed successfully. Order No: {order_no}")
    else:
        print("❌ Order failed:", placed_order.get("nOrdNo"))

    while(order_status != "complete"):
        print("Order Status:", order_status)
        order_report = client.order_report()


        for order_report in order_report.get("data", []):
            if order_report.get("nOrdNo") == order_no:
                print("order report: " + str(order_report))
                order_status = order_report.get("ordSt")
                order_rejection_reason = order_report.get("rejRsn")
                order_status = order_report.get("ordSt")
                order_price = int(float((order_report.get("avgPrc"))))
                break

    print("Order Number:", order_no)
    print("Order Status:", order_status)
    print("Order price:", order_price)
    print("Rejection Reason:", order_rejection_reason)

    order_price += 150
    order_status = "open"





