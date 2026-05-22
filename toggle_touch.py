
# toggle_touch.py
# ---------------
# Prende o apaga el touch en Windows 11.
# Corre esto como admin, si no no va a funcionar.
#
# Cómo se usa:
#     python toggle_touch.py          # alterna el estado
#     python toggle_touch.py on       # fuerza activar
#     python toggle_touch.py off      # fuerza desactivar
#     python toggle_touch.py list     # muestra los dispositivos táctiles

import subprocess
import sys

# VID_222A = ILITEK (la pantalla de 7")
TOUCH_KEYWORDS = ["pantalla táctil", "touch screen", "hid-compliant touch screen", "222a"]


def run_raw(cmd):
    # Ejecuta el comando y devuelve el texto (prueba varios encodings por si acaso)
    result = subprocess.run(cmd, capture_output=True, shell=False)
    for enc in ["cp1252", "utf-8", "cp850", "latin-1"]:
        try:
            return result.stdout.decode(enc)
        except Exception:
            continue
    return result.stdout.decode("utf-8", errors="replace")


def get_touch_devices():
    # Busca dispositivos HID táctiles usando pnputil
    output = run_raw(["pnputil", "/enum-devices", "/class", "HIDClass"])
    devices = []
    current = {}

    for line in output.splitlines():
        line = line.strip()
        # Soporta inglés y español
        if line.startswith("Id. de instancia") or line.startswith("Instance ID"):
            if current:
                devices.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif line.startswith("Descripción del dispositivo") or line.startswith("Device Description"):
            current["desc"] = line.split(":", 1)[1].strip()
        elif line.startswith("Estado") or line.startswith("Device Status"):
            current["status"] = line.split(":", 1)[1].strip()

    if current:
        devices.append(current)

    # Solo los táctiles
    touch = []
    for d in devices:
        desc = d.get("desc", "").lower()
        dev_id = d.get("id", "").lower()
        if any(k in desc for k in TOUCH_KEYWORDS) or any(k in dev_id for k in TOUCH_KEYWORDS):
            touch.append(d)

    return touch


def is_enabled(device):
    # Devuelve True si el touch está prendido
    status = device.get("status", "").lower()
    return "iniciado" in status or "started" in status


def enable_device(device_id):
    result = run_raw(["pnputil", "/enable-device", device_id])
    print(f"  -> {result.strip()}")


def disable_device(device_id):
    result = run_raw(["pnputil", "/disable-device", device_id])
    print(f"  -> {result.strip()}")


def check_admin():
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("ERROR: Esto tiene que correr como admin!")
            print("Dale clic derecho a la terminal y elige 'Ejecutar como administrador'")
            sys.exit(1)
    except Exception:
        pass


def main():
    check_admin()

    action = sys.argv[1].lower() if len(sys.argv) > 1 else "toggle"

    print("Buscando dispositivos táctiles...")
    devices = get_touch_devices()

    if action == "list":
        if not devices:
            print("  No encontré ningún dispositivo táctil HID.")
        for d in devices:
            status = "ACTIVO" if is_enabled(d) else "INACTIVO"
            print(f"  [{status}] {d.get('desc', 'N/A')}")
            print(f"          ID: {d.get('id', 'N/A')}")
        return

    if not devices:
        print("No encontré ningún dispositivo táctil.")
        print("Prueba con: python toggle_touch.py list")
        sys.exit(1)

    for d in devices:
        desc = d.get("desc", d.get("id"))
        enabled = is_enabled(d)
        print(f"\nDispositivo: {desc}")
        print(f"Estado actual: {'ACTIVO' if enabled else 'INACTIVO'}")

        if action == "toggle":
            if enabled:
                print("-> Apagando touch...")
                disable_device(d["id"])
            else:
                print("-> Prendiendo touch...")
                enable_device(d["id"])
        elif action == "on":
            if enabled:
                print("-> Ya está prendido.")
            else:
                print("-> Prendiendo touch...")
                enable_device(d["id"])
        elif action == "off":
            if not enabled:
                print("-> Ya está apagado.")
            else:
                print("-> Apagando touch...")
                disable_device(d["id"])

    print("\nListo!")


if __name__ == "__main__":
    main()