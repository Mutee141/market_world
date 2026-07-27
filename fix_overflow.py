base = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\base.html'
with open(base, 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure .tbar-wrap or .tbar has no overflow hidden in style attribute if any
text = text.replace('overflow: hidden', 'overflow: visible')

# Let's add inline style to top bar container
text = text.replace('<div class="tbar">', '<div class="tbar" style="overflow: visible !important; position: relative; z-index: 99999;">')
text = text.replace('<div class="top-bar">', '<div class="top-bar" style="overflow: visible !important; position: relative; z-index: 99999;">')
text = text.replace('<header class="header">', '<header class="header" style="overflow: visible !important;">')

with open(base, 'w', encoding='utf-8') as f:
    f.write(text)

print('base html overflow fixed')
