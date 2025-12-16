
import os

path = r'c:\Users\Michaeli\Documents\guy\esim-scanner\templates\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# exact target string causing issues
bad_string = "isPopular: { { country.is_popular | tojson } }"
good_string = "isPopular: {{ country.is_popular|tojson }}"

if bad_string in content:
    new_content = content.replace(bad_string, good_string)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("FIXED: Found and replaced the bad string.")
else:
    print("WARNING: Bad string not found. dumping nearby lines:")
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "isPopular" in line:
            print(f"Line {i+1}: {line}")
