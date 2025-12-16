
import os

path = r'c:\Users\Michaeli\Documents\guy\esim-scanner\templates\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the specific malformed tag
new_content = content.replace('{ {', '{{').replace('} }', '}}')
# Also remove spaces around the pipes if any, just in case
new_content = new_content.replace(' | ', '|')

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Fixed {path}")
