import re

base_path = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Cart subtotal offcanvas
# <span class="fw-bold" style="font-size: 16px;">{{ store.currency|default:"PKR" }} {{ cart_subtotal|default:"0.00"|floatformat:2 }}</span>
text = re.sub(
    r'<span class="fw-bold" style="font-size: 16px;">\{\{ store\.currency\|default:"PKR" \}\} \{\{ cart_subtotal\|default:"0\.00"\|floatformat:2 \}\}</span>',
    r'<span class="fw-bold" style="font-size: 16px;" data-base-price="{{ cart_subtotal|default:0.00 }}">{{ store.currency|default:"PKR" }} {{ cart_subtotal|default:"0.00"|floatformat:2 }}</span>',
    text
)

# Header cart total
# <span class="sh-cart-total d-none d-lg-inline" id="header-cart-total">{{ store.currency|default:"PKR" }} {{ cart_subtotal|default:"0.00"|floatformat:2 }}</span>
text = re.sub(
    r'<span class="sh-cart-total d-none d-lg-inline" id="header-cart-total">\{\{ store\.currency\|default:"PKR" \}\} \{\{ cart_subtotal\|default:"0\.00"\|floatformat:2 \}\}</span>',
    r'<span class="sh-cart-total d-none d-lg-inline" id="header-cart-total" data-base-price="{{ cart_subtotal|default:0.00 }}">{{ store.currency|default:"PKR" }} {{ cart_subtotal|default:"0.00"|floatformat:2 }}</span>',
    text
)

# Offcanvas cart items
# <span>{{ store.currency|default:"PKR" }} {{ item.total_price|floatformat:2 }}</span>
text = re.sub(
    r'<span>\{\{ store\.currency\|default:"PKR" \}\} \{\{ item\.total_price\|floatformat:2 \}\}</span>',
    r'<span data-base-price="{{ item.total_price }}">{{ store.currency|default:"PKR" }} {{ item.total_price|floatformat:2 }}</span>',
    text
)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('cart patched.')
