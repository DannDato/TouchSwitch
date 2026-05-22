import subprocess
result = subprocess.run(['pnputil', '/enum-devices', '/class', 'HIDClass'], capture_output=True)
# Probar diferentes encodings
for enc in ['utf-8', 'cp1252', 'cp850', 'latin-1']:
    try:
        text = result.stdout.decode(enc)
        for line in text.splitlines():
            if any(x in line.lower() for x in ['222', 'táctil', 'tactil', 'touch', 'pantalla']):
                print(f"[{enc}] {repr(line)}")
        break
    except:
        continue