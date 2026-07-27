import re

dashboard = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\dashboard.html'
with open(dashboard, 'r', encoding='utf-8') as f:
    text = f.read()

# We want to replace the hardcoded input lines in editProductModal with the dynamic loop
# First, let's remove the old sku and cost price fields
text = re.sub(r'<div class="col-md-3"><label class="form-label">SKU \*</label>.*?</div>\s*', '', text)
text = re.sub(r'<div class="col-md-3"><label class="form-label">Cost Price</label>.*?</div>\s*', '', text)
text = re.sub(r'<div class="col-md-3"><label class="form-label">Selling Price \*</label>.*?</div>\s*', '', text)
text = re.sub(r'<div class="col-md-3"><label class="form-label">Discount Price</label>.*?</div>\s*', '', text)
text = re.sub(r'<div class="col-md-3"><label class="form-label">Model \(Optional\)</label>.*?</div>\s*', '', text)
text = re.sub(r'<div class="col-md-9"><label class="form-label">Variant/Specs \(Optional\)</label>.*?</div>\s*', '', text)

# Now, we insert the new variant block right after the description block in edit modal
desc_block = r'<div class="col-md-12"><label class="form-label">Description</label><textarea name="description" class="form-control" rows="3">{{ product.description }}</textarea></div>'

new_variant_block = '''
                                            <div class="col-12 mt-3">
                                                <h6 class="fw-bold"><i class="fas fa-tags me-2"></i>Product Variants</h6>
                                                <div id="variants-container-{{ product.id }}" class="bg-light p-3 rounded border">
                                                    {% for v in product.variants.all %}
                                                    <div class="variant-row bg-white p-3 rounded border mb-3 position-relative">
                                                        {% if not forloop.first %}
                                                        <button type="button" class="btn btn-sm btn-danger position-absolute" style="top: 10px; right: 10px;" onclick="this.closest('.variant-row').remove();"><i class="fas fa-trash"></i></button>
                                                        {% endif %}
                                                        <input type="hidden" name="variant_id[]" value="{{ v.id }}">
                                                        <div class="row g-2 mb-2">
                                                            <div class="col-md-3"><label class="form-label" style="font-size:12px;">SKU *</label><input type="text" name="sku[]" class="form-control form-control-sm" value="{{ v.sku }}" required></div>
                                                            <div class="col-md-3"><label class="form-label" style="font-size:12px;">Cost Price</label><input type="number" name="cost_price[]" class="form-control form-control-sm" step="0.01" value="{{ v.cost_price|default:0 }}"></div>
                                                            <div class="col-md-3"><label class="form-label" style="font-size:12px;">Selling Price *</label><input type="number" name="selling_price[]" class="form-control form-control-sm" step="0.01" value="{{ v.selling_price|default:0 }}" required></div>
                                                            <div class="col-md-3"><label class="form-label" style="font-size:12px;">Discount Price</label><input type="number" name="discount_price[]" class="form-control form-control-sm" step="0.01" value="{{ v.discount_price|default:'' }}"></div>
                                                        </div>
                                                        <div class="row g-2">
                                                            <div class="col-md-4"><label class="form-label" style="font-size:12px;">Model (Optional)</label><input type="text" name="attr_model[]" class="form-control form-control-sm" value="{{ v.attributes.Model|default:'' }}"></div>
                                                            <div class="col-md-8"><label class="form-label" style="font-size:12px;">Variant/Specs (Optional)</label><input type="text" name="attr_variant[]" class="form-control form-control-sm" value="{{ v.attributes.Variant|default:'' }}" placeholder="e.g. 32GB RAM"></div>
                                                        </div>
                                                    </div>
                                                    {% endfor %}
                                                </div>
                                                <button type="button" class="btn btn-sm btn-outline-primary mt-2" onclick="addVariantRow('{{ product.id }}')"><i class="fas fa-plus"></i> Add Another Variant</button>
                                            </div>
'''

text = text.replace(desc_block, desc_block + "\n" + new_variant_block)

with open(dashboard, 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
