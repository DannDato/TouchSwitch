
# touch_tray.py
# -------------
# Iconito en la bandeja para prender o apagar el touch.
# Corre como admin,

import subprocess
import sys
import threading
from PIL import Image, ImageDraw
import pystray

DEVICE_ID = r"HID\VID_222A&PID_0001\c&2c7688aa&0&0000"


def run_raw(cmd):
    # Ejecuta el comando y devuelve el texto (prueba varios encodings por si acaso)
    result = subprocess.run(cmd, capture_output=True, shell=False)
    for enc in ["cp1252", "utf-8", "cp850", "latin-1"]:
        try:
            return result.stdout.decode(enc)
        except Exception:
            continue
    return result.stdout.decode("utf-8", errors="replace")


def is_touch_enabled():
    # Devuelve True si el touch está prendido
    output = run_raw(["pnputil", "/enum-devices", "/class", "HIDClass"])
    capture_next = False
    for line in output.splitlines():
        line = line.strip()
        if DEVICE_ID in line:
            capture_next = True
        if capture_next and ("Estado" in line or "Device Status" in line):
            status = line.split(":", 1)[1].strip().lower()
            return "iniciado" in status or "started" in status
    return False


def set_touch(enable: bool, retries=3):
    # Prende o apaga el touch, reintenta si falla
    cmd = "/enable-device" if enable else "/disable-device"
    for attempt in range(retries):
        run_raw(["pnputil", cmd, DEVICE_ID])
        import time; time.sleep(1)
        if is_touch_enabled() == enable:
            return True
    return False


def make_icon(enabled: bool):
    # Dibuja un icono simple: verde si está prendido, rojo si está apagado
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    color = (46, 204, 113) if enabled else (231, 76, 60)  # verde / rojo

    # Círculo de fondo
    draw.ellipse([4, 4, 60, 60], fill=color)

    # Dibuja la pantalla y el dedo
    draw.rectangle([20, 14, 44, 42], fill="white", outline="white", width=2)
    draw.ellipse([26, 38, 38, 50], fill="white")

    if not enabled:
        # Dibuja la cruz encima
        draw.line([10, 10, 54, 54], fill="white", width=5)
        draw.line([54, 10, 10, 54], fill="white", width=5)

    return img



class TrayApp:
    def __init__(self):
        self.enabled = is_touch_enabled()
        self.icon = pystray.Icon(
            "touch_toggle",
            make_icon(self.enabled),
            self._tooltip(),
            menu=pystray.Menu(
                pystray.MenuItem(self._label, self.toggle, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Salir", self.quit),
            )
        )

    def _tooltip(self):
        # Tooltip más relajado
        return f"Touch: {'ACTIVO' if self.enabled else 'INACTIVO'} — clic para cambiar"

    def _label(self, item):
        return f"{'Apagar' if self.enabled else 'Prender'} touch"

    def toggle(self, icon=None, item=None):
        def _do():
            target = not self.enabled
            ok = set_touch(target)
            if ok:
                self.enabled = target
            self.icon.icon = make_icon(self.enabled)
            self.icon.title = self._tooltip()
        threading.Thread(target=_do, daemon=True).start()

    def quit(self, icon, item):
        self.icon.stop()

    def run(self):
        self.icon.run()


def check_admin():
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("ERROR: Esto tiene que correr como admin!")
            sys.exit(1)
    except Exception:
        pass


if __name__ == "__main__":
    check_admin()
    app = TrayApp()
    app.run()