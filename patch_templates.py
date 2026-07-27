import re

pcard = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\includes\product_card.html'
with open(pcard, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '{% if v.discount_price %}<del class="pcard-old">{{ store.currency }} {{ v.discount_price|floatformat:2 }}</del><span class="pcard-current">{{ store.currency }} {{ v.selling_price|floatformat:2 }}</span>',
    '{% if v.discount_price %}<del class="pcard-old" data-base-price="{{ v.discount_price }}">{{ store.currency }} {{ v.discount_price|floatformat:2 }}</del><span class="pcard-current" data-base-price="{{ v.selling_price }}">{{ store.currency }} {{ v.selling_price|floatformat:2 }}</span>'
)
text = text.replace(
    '{% else %}<span class="pcard-current">{{ store.currency }} {{ v.selling_price|floatformat:2 }}</span>{% endif %}',
    '{% else %}<span class="pcard-current" data-base-price="{{ v.selling_price }}">{{ store.currency }} {{ v.selling_price|floatformat:2 }}</span>{% endif %}'
)

with open(pcard, 'w', encoding='utf-8') as f:
    f.write(text)

single = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\single.html'
with open(single, 'r', encoding='utf-8') as f:
    stext = f.read()
    
sold = '''                        <div class="pd-price-row">
                            {% if selected_variant.discount_price %}
                            <span class="pd-price-old">{{ store.currency }} {{ selected_variant.discount_price|floatformat:2 }}</span>
                            <span>{{ store.currency }} {{ selected_variant.selling_price|floatformat:2 }}</span>
                            {% else %}
                            <span>{{ store.currency }} {{ selected_variant.selling_price|floatformat:2 }}</span>
                            {% endif %}
                        </div>'''
snew = '''                        <div class="pd-price-row">
                            {% if selected_variant.discount_price %}
                            <span class="pd-price-old" data-base-price="{{ selected_variant.discount_price }}">{{ store.currency }} {{ selected_variant.discount_price|floatformat:2 }}</span>
                            <span data-base-price="{{ selected_variant.selling_price }}">{{ store.currency }} {{ selected_variant.selling_price|floatformat:2 }}</span>
                            {% else %}
                            <span data-base-price="{{ selected_variant.selling_price }}">{{ store.currency }} {{ selected_variant.selling_price|floatformat:2 }}</span>
                            {% endif %}
                        </div>'''
stext = stext.replace(sold, snew)
with open(single, 'w', encoding='utf-8') as f:
    f.write(stext)
    
print('Templates patched successfully.')
