trigger_price = int(-1)

symbol = "SILVERMIC27FEB26FUT"


from broker.login import get_authenticated_client
client = get_authenticated_client()

if (trigger_price <= 0):
    placed_order = client.place_order(exchange_segment="mcx_fo",
                                      product="MIS",
                                      price="0",
                                      order_type="MKT",
                                      quantity="1",
                                      validity="DAY",
                                      trading_symbol="SILVERMIC27FEB26FUT",
                                      transaction_type="S",
                                      amo="NO",
                                      disclosed_quantity="0",
                                      market_protection="0",
                                      pf="N",
                                      trigger_price="0")
else:
    placed_order = client.place_order(exchange_segment="mcx_fo",
                                      product="MIS",
                                      price=str(trigger_price),
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
    print("❌ Order failed:", str(placed_order))

# sleeping for 5 seconds before placing SL order...
import time
time.sleep(1)

order_report = client.order_report()


for order_report in order_report.get("data", []):
    if order_report.get("nOrdNo") == order_no:
        print("order reprot: " + str(order_report))
        order_status = order_report.get("ordSt")
        order_rejection_reason = order_report.get("rejRsn")
        order_status = order_report.get("ordSt")
        order_price = order_report.get("prc")
        break

print("Order Number:", order_no)
print("Order Status:", order_status)
print("Order price:", order_price)
print("Rejection Reason:", order_rejection_reason)


order_history = client.order_history(order_no)
print("Order History:", str(order_history))
exit_message = client.logout()
print(exit_message)
