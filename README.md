
# TouchSwitch

Un toque rápido para prender o apagar la pantalla táctil de 7" desde la bandeja del sistema.

---

## ¿Qué hace?

Un iconito vive en tu **bandeja del sistema** (esquina inferior derecha):


| Icono | Estado |
|-------|--------|
| Círculo verde | Touch **ACTIVO** |
| Círculo rojo con cruz | Touch **INACTIVO** |

- **Clic izquierdo** → toggle instantáneo
- **Clic derecho** → menú con opción de salir
- Si el driver tarda en responder, reintenta hasta 3 veces automáticamente

---


## Archivos

```
TouchSwitch/
├── venv/                  # el venv de Python
├── touch_tray.py          # la app de la bandeja
├── toggle_touch.py        # script para usarlo desde la terminal
├── START_TRAY.bat         # el lanzador (pide admin y abre el tray)
└── README.md              # este archivo
```

---


## Requisitos

- Python 3.10+
- Windows 11
- Siempre corre esto como admin (si no, no te deja prender/apagar el touch)

---


## Setup inicial 

```bash
# Crea y activa el venv
python -m venv venv
venv\Scripts\activate

# Instala lo que pide
pip install pystray pillow
```

---


## Uso diario

Dale doble clic a **START_TRAY.bat** — pide permisos de admin y te pone el iconito en la bandeja.

---


## Que arranque solo con Windows

Si quieres que se prenda solo cada vez que prendes la compu:

1. Clic derecho en START_TRAY.bat → **Crear acceso directo**
2. Presiona Win + R y escribe:
   ```
   shell:startup
   ```
3. Mueve el acceso directo ahí

> Ojo: Windows te va a pedir el popup de admin la primera vez. Si no quieres ese popup, mira abajo.


### Quitar el popup de admin al iniciar

1. Abre el Programador de tareas (taskschd.msc)
2. Clic en "Crear tarea" (no la básica)
3. Ponle:
   - General → marca "Ejecutar con los privilegios más altos"
   - Desencadenadores → Nuevo → "Al iniciar sesión"
   - Acciones → Nuevo → pon la ruta completa a START_TRAY.bat
4. Condiciones → quita "Iniciar solo si está conectado a corriente"
5. Listo

Así arranca sin popup y con permisos de admin.

---


## Dispositivo táctil detectado

```
Descripción : Pantalla táctil compatible con HID
ID          : HID\VID_222A&PID_0001\c&2c7688aa&0&0000
Fabricante  : ILITEK
```

---


## Usar desde la terminal (opcional)

Con el venv activado (venv\Scripts\activate):

```bash
python toggle_touch.py          # alterna el estado
python toggle_touch.py on       # fuerza activar
python toggle_touch.py off      # fuerza desactivar
python toggle_touch.py list     # ver estado actual
```