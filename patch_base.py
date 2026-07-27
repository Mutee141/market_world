import os

base_path = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the simple select with a custom dropdown
old_select = '''                <div class="tbar-select-wrap">
                    <select class="tbar-select" aria-label="Currency">
                        <option>{{ store.currency|default:"PKR" }}</option>
                    </select>
                </div>'''

new_select = '''                <!-- Multi-Currency Dropdown -->
                <div class="dropdown tbar-select-wrap currency-dropdown-wrap">
                    <button class="btn dropdown-toggle currency-btn" type="button" id="currencyDropdown" data-bs-toggle="dropdown" aria-expanded="false" style="color: #cbd5e1; font-size: 11px; padding: 0; background: transparent; border: none; font-weight: 500; display: flex; align-items: center; gap: 4px;">
                        <img src="https://flagcdn.com/w20/pk.png" width="16" alt="PK" id="active-currency-flag"> 
                        <span id="active-currency-code">PKR</span>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end shadow-sm" aria-labelledby="currencyDropdown" style="font-size: 13px; min-width: 100px; padding: 5px;">
                        <li><a class="dropdown-item currency-item d-flex align-items-center gap-2" href="#" data-currency="PKR" data-flag="pk"><img src="https://flagcdn.com/w20/pk.png" width="18" alt="PK"> PKR</a></li>
                        <li><a class="dropdown-item currency-item d-flex align-items-center gap-2" href="#" data-currency="USD" data-flag="us"><img src="https://flagcdn.com/w20/us.png" width="18" alt="US"> USD</a></li>
                        <li><a class="dropdown-item currency-item d-flex align-items-center gap-2" href="#" data-currency="GBP" data-flag="gb"><img src="https://flagcdn.com/w20/gb.png" width="18" alt="GB"> GBP</a></li>
                        <li><a class="dropdown-item currency-item d-flex align-items-center gap-2" href="#" data-currency="AED" data-flag="ae"><img src="https://flagcdn.com/w20/ae.png" width="18" alt="AE"> AED</a></li>
                    </ul>
                </div>'''

if old_select in text:
    text = text.replace(old_select, new_select)
    
# Inject JS into base.html right before closing body tag
js_logic = '''
<!-- Currency Engine -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const rates = {
        'PKR': 1,
        'USD': 0.0036, // 1 USD = ~277 PKR
        'GBP': 0.0028, // 1 GBP = ~350 PKR
        'AED': 0.0132  // 1 AED = ~75.5 PKR
    };
    
    const symbols = {
        'PKR': 'PKR',
        'USD': '$',
        'GBP': '£',
        'AED': 'AED'
    };

    let currentCurrency = localStorage.getItem('selectedCurrency') || 'PKR';
    
    // Function to format numbers nicely
    function formatMoney(amount, currency) {
        if (currency === 'PKR') {
            return amount.toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ",");
        }
        return amount.toFixed(2).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ",");
    }

    function updatePrices() {
        const rate = rates[currentCurrency];
        const symbol = symbols[currentCurrency];
        
        // Find all elements with data-base-price
        document.querySelectorAll('[data-base-price]').forEach(el => {
            const basePrice = parseFloat(el.getAttribute('data-base-price'));
            if (!isNaN(basePrice)) {
                const converted = basePrice * rate;
                el.innerHTML = symbol + ' ' + formatMoney(converted, currentCurrency);
            }
        });
        
        // Update header cart total explicitly if it doesn't have data attr
        const cartTotalEl = document.getElementById('header-cart-total');
        if(cartTotalEl && cartTotalEl.hasAttribute('data-base-price')) {
            const cartTotal = parseFloat(cartTotalEl.getAttribute('data-base-price'));
            if(!isNaN(cartTotal)) {
                cartTotalEl.innerHTML = symbol + ' ' + formatMoney(cartTotal * rate, currentCurrency);
            }
        }
    }

    function updateActiveDropdownUI() {
        const item = document.querySelector(`.currency-item[data-currency="${currentCurrency}"]`);
        const flagCode = item ? item.getAttribute('data-flag') : 'pk';
        const codeEl = document.getElementById('active-currency-code');
        const flagEl = document.getElementById('active-currency-flag');
        if(codeEl) codeEl.textContent = currentCurrency;
        if(flagEl) flagEl.src = `https://flagcdn.com/w20/${flagCode}.png`;
    }

    // Attach click events
    document.querySelectorAll('.currency-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            currentCurrency = this.getAttribute('data-currency');
            localStorage.setItem('selectedCurrency', currentCurrency);
            updateActiveDropdownUI();
            updatePrices();
        });
    });

    // Initial load
    if(currentCurrency !== 'PKR') {
        updateActiveDropdownUI();
        updatePrices();
    }
});
</script>
'''

if '<!-- Currency Engine -->' not in text:
    text = text.replace('</body>', js_logic + '\n</body>')

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('base.html patched successfully.')
