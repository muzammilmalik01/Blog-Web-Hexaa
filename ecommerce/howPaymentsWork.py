"""
# * This is how payments have been configured to work *

# * 1. When the order is successfully placed, create a Stripe Payment Intent against the order
# * 2. Payment Intent can be created using create_payment_intent() view
# * 3. create_payment() view will receive:
# *     - order_id
# *     - total_amount
# * 4. create_payment() will return 'client_secret' which will be used in stripe.confirmCardPayment() at React Side to deduct the payment.

NOTE: It can be customized futher according to different requirements and is just a basic implementation.

"""
