"""
# * This is how payments have been configured to work can be easily changed. *

# ? Order Placing
# NOTE: It is my first thought, obviously can be made much better.

# * 1. User will add different products to cart, when ready will click checkout.
# * 2. Order will be added and order items as well, when order.is_complete (all orderitems added)
# * 3. During checkout user will select Payment option: COD or Online.
# * 4. If Online, check Payment Workflow.
# * 5. if COD, set is_paid.

# ? Payment Workflow

# * 1. When the order is successfully placed, create a Stripe Payment Intent against the order
# * 2. Payment Intent can be created using create_payment_intent() view
# * 3. create_payment() view will receive:
#      - order_id
#      - total_amount
# * 4. create_payment() will return 'client_secret' which will be used in stripe.confirmCardPayment() at React Side to deduct the payment.
# * 5. If payment is successful set is_paid
# * 6. If payment is failed set is_paid = false and show user that order is placed but not not paid.
# * 7. User will be able to search for his/her upaid order and pay again.

NOTE: It can be customized futher according to different requirements and is just a basic implementation.

"""
