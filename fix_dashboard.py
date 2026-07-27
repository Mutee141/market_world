dashboard = r'c:\Users\user\Desktop\pakages\retailplatform\config\storefront\templates\storefront\dashboard.html'
with open(dashboard, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# find duplicate blocks
new_lines = []
skip = False
for i, line in enumerate(lines):
    if i >= 1726 and i <= 1751:
        continue
    new_lines.append(line)

with open(dashboard, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Duplicate removed!')
