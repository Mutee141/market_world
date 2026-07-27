dashboard = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\dashboard.html'
with open(dashboard, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the broken Featured In section in edit form
bad_block = """
                                                <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:4px;">
                                                    <label style="font-size:13px;"><input type="checkbox" name="sections" value="featured" {% if 'featured' in product.tags %}checked{% endif %}> Featured</label>
                                                    <label style="font-size:13px;"><input type="checkbox" name="sections" value="new_arrival" {% if 'new_arrival' in product.tags %}checked{% endif %}> New Arrival</label>
                                                    <label style="font-size:13px;"><input type="checkbox" name="sections" value="best_seller" {% if 'best_seller' in product.tags %}checked{% endif %}> Best Seller</label>
                                                    <label style="font-size:13px;"><input type="checkbox" name="sections" value="trending" {% if 'trending' in product.tags %}checked{% endif %}> Trending</label>
                                                </div>
                                            </div>"""

good_block = """
                                            <div class="col-md-6">
                                                <label class="form-label">Featured In</label>
                                                <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:4px;">
                                                    <label style="font-size:13px;"><input type="checkbox" name="sections" value="featured" {% if 'featured' in product.tags %}checked{% endif %}> Featured</label>
                                                    <label style="font-size:13px;"><input type="checkbox" name="sections" value="new_arrival" {% if 'new_arrival' in product.tags %}checked{% endif %}> New Arrival</label>
                                                    <label style="font-size:13px;"><input type="checkbox" name="sections" value="best_seller" {% if 'best_seller' in product.tags %}checked{% endif %}> Best Seller</label>
                                                    <label style="font-size:13px;"><input type="checkbox" name="sections" value="trending" {% if 'trending' in product.tags %}checked{% endif %}> Trending</label>
                                                </div>
                                            </div>"""

text = text.replace(bad_block, good_block)

# Fix the JS addVariantRow Discount Price label
js_bad = '<div class="col-md-3"><label class="form-label" style="font-size:12px;">Discount Price</label><input type="number" name="discount_price[]" class="form-control form-control-sm" step="0.01"></div>'
js_good = '<div class="col-md-3"><label class="form-label" style="font-size:12px;">Compare At (Old Price)</label><input type="number" name="discount_price[]" class="form-control form-control-sm" step="0.01"></div>'
text = text.replace(js_bad, js_good)

with open(dashboard, 'w', encoding='utf-8') as f:
    f.write(text)
print('Dashboard UI fixed.')
