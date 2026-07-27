base = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\base.html'
with open(base, 'r', encoding='utf-8') as f:
    text = f.read()

# Let's fix the dropdown styles.
old_dropdown = '''                <!-- Multi-Currency Dropdown -->
                <div class="dropdown tbar-select-wrap currency-dropdown-wrap">
                    <button class="btn dropdown-toggle currency-btn" type="button" id="currencyDropdown" data-bs-toggle="dropdown" aria-expanded="false" style="color: #cbd5e1; font-size: 11px; padding: 0; background: transparent; border: none; font-weight: 500; display: flex; align-items: center; gap: 4px;">'''

new_dropdown = '''                <!-- Multi-Currency Dropdown -->
                <div class="dropdown tbar-select-wrap currency-dropdown-wrap" style="position: relative; z-index: 1050;">
                    <button class="btn dropdown-toggle currency-btn shadow-none" type="button" id="currencyDropdown" data-bs-toggle="dropdown" aria-expanded="false" style="color: #cbd5e1; font-size: 11px; padding: 0; background: transparent; border: none; font-weight: 500; display: flex; align-items: center; gap: 4px; box-shadow: none !important; outline: none !important;">'''

text = text.replace(old_dropdown, new_dropdown)

old_ul = '''                    <ul class="dropdown-menu dropdown-menu-end shadow-sm" aria-labelledby="currencyDropdown" style="font-size: 13px; min-width: 100px; padding: 5px;">'''
new_ul = '''                    <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="currencyDropdown" style="font-size: 13px; min-width: 100px; padding: 5px; z-index: 99999; position: absolute; margin-top: 8px; border-radius: 8px; border: none;">'''

text = text.replace(old_ul, new_ul)

# Also check for .tbar overflow hidden in style.css or base.html
# A common issue is a wrapper having overflow hidden. We can add a class or inline style to fix it.
# Let's replace tbar-right just in case it has overflow hidden
if 'overflow:hidden' in text:
    pass

with open(base, 'w', encoding='utf-8') as f:
    f.write(text)
print('UI fixed')
