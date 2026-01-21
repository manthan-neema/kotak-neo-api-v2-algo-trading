from broker.login import get_authenticated_client
client = get_authenticated_client()

placed_order = client.place_order(exchange_segment="mcx_fo",
                   product="MIS",
                   price="0",
                   order_type="MKT",
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

# sleeping for 5 seconds before placing SL order...
import time
time.sleep(1)

order_report = client.order_report()


for order_report in order_report.get("data", []):
    if order_report.get("nOrdNo") == order_no:
        print("order report: " + str(order_report))
        order_status = order_report.get("ordSt")
        order_rejection_reason = order_report.get("rejRsn")
        order_status = order_report.get("ordSt")
        order_price = order_report.get("avgPrc")
        break

print("Order Number:", order_no)
print("Order Status:", order_status)
print("Order order_price:", order_price)
print("Rejection Reason:", order_rejection_reason)


exit_message = client.logout()
print(exit_message)
