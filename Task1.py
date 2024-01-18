def apply_discount_rules(cart, discounts):
    cart_total = sum(item['total'] for item in cart)
    max_discount = 0
    discount_name = ""

    for discount, rule in discounts.items():
        if rule(cart, cart_total):
            current_discount = rule(cart, cart_total)
            if current_discount > max_discount:
                max_discount = current_discount
                discount_name = discount

    return discount_name, max_discount


def flat_10_discount(cart, cart_total):
    return 10 if cart_total > 200 else 0


def bulk_5_discount(cart, cart_total):
    for item in cart:
        if item['quantity'] > 10:
            return item['total'] * 0.05
    return 0


def bulk_10_discount(cart, cart_total):
    total_quantity = sum(item['quantity'] for item in cart)
    return 0.1 * cart_total if total_quantity > 20 else 0


def tiered_50_discount(cart, cart_total):
    total_quantity = sum(item['quantity'] for item in cart)
    for item in cart:
        if item['quantity'] > 15:
            return item['total'] * 0.5
    return 0


def calculate_cost(product, quantity, is_gift_wrapped):
    unit_price = products[product]
    total_price = quantity * unit_price
    gift_wrap_fee = 1 if is_gift_wrapped else 0
    return {
        'product': product,
        'quantity': quantity,
        'total': total_price + gift_wrap_fee,
        'gift_wrap_fee': gift_wrap_fee
    }


products = {'Product A': 20, 'Product B': 40, 'Product C': 50}
discount_rules = {
    'flat_10_discount': flat_10_discount,
    'bulk_5_discount': bulk_5_discount,
    'bulk_10_discount': bulk_10_discount,
    'tiered_50_discount': tiered_50_discount
}

cart = []

for product, price in products.items():
    quantity = int(input(f'Enter the quantity of {product}: '))
    is_gift_wrapped = input(f'Is {product} wrapped as a gift? (yes/no): ').lower() == 'yes'
    cart.append(calculate_cost(product, quantity, is_gift_wrapped))

subtotal = sum(item['total'] for item in cart)

discount_name, discount_amount = apply_discount_rules(cart, discount_rules)
total_discount = discount_amount if discount_name else 0

shipping_fee = sum(item['quantity'] // 10 for item in cart) * 5
total = subtotal - total_discount + shipping_fee

# Output
print("\nProduct Details:")
for item in cart:
    print(f"{item['product']} - Quantity: {item['quantity']} - Total: ${item['total']}")

print("\nSubtotal:", f"${subtotal}")
print("Discount Applied:", f"{discount_name} - ${discount_amount}")
print("Shipping Fee:", f"${shipping_fee}")
print("Total:", f"${total}")
