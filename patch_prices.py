import re

dashboard = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\dashboard.html'
with open(dashboard, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Discount Price</label>', 'Compare At (Old Price)</label>')
with open(dashboard, 'w', encoding='utf-8') as f:
    f.write(text)


single = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\single.html'
with open(single, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix price rendering in single.html
old_price_block = """                        <div class="pd-price-row">
                            {% if selected_variant.discount_price %}
                            <span class="pd-price-old">{{ store.currency }} {{ selected_variant.selling_price|floatformat:2 }}</span>
                            <span>{{ store.currency }} {{ selected_variant.discount_price|floatformat:2 }}</span>
                            {% else %}
                            <span>{{ store.currency }} {{ selected_variant.selling_price|floatformat:2 }}</span>
                            {% endif %}
                        </div>"""

new_price_block = """                        <div class="pd-price-row">
                            {% if selected_variant.discount_price %}
                            <span class="pd-price-old">{{ store.currency }} {{ selected_variant.discount_price|floatformat:2 }}</span>
                            <span>{{ store.currency }} {{ selected_variant.selling_price|floatformat:2 }}</span>
                            {% else %}
                            <span>{{ store.currency }} {{ selected_variant.selling_price|floatformat:2 }}</span>
                            {% endif %}
                        </div>"""
text = text.replace(old_price_block, new_price_block)
with open(single, 'w', encoding='utf-8') as f:
    f.write(text)


pcard = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\includes\product_card.html'
with open(pcard, 'r', encoding='utf-8') as f:
    text = f.read()
    
# Fix price rendering in product_card.html
old_card = '{% if v.discount_price %}<del class="pcard-old">{{ store.currency }} {{ v.selling_price|floatformat:2 }}</del><span class="pcard-current">{{ store.currency }} {{ v.discount_price|floatformat:2 }}</span>'
new_card = '{% if v.discount_price %}<del class="pcard-old">{{ store.currency }} {{ v.discount_price|floatformat:2 }}</del><span class="pcard-current">{{ store.currency }} {{ v.selling_price|floatformat:2 }}</span>'
text = text.replace(old_card, new_card)

with open(pcard, 'w', encoding='utf-8') as f:
    f.write(text)

# Also fix views.py to handle duplicate SKUs in variant creation (append index)
views_file = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\views.py'
with open(views_file, 'r', encoding='utf-8') as f:
    vtext = f.read()

vtext = re.sub(
    r"v_sku = skus\[i\]\.strip\(\)",
    r"v_sku = skus[i].strip()\n                    # prevent crash on duplicate sku in same form\n                    if i > 0 and v_sku in skus[:i]: v_sku = f'{v_sku}-{i}'",
    vtext
)

with open(views_file, 'w', encoding='utf-8') as f:
    f.write(vtext)

print("All fixes applied successfully.")
