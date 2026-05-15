from datetime import datetime, timezone

_ICONOS = {200: "✅", 201: "✅", 400: "⚠️", 401: "🔒", 402: "💰", 403: "🚫", 404: "❓", 500: "💥"}


def log(status_code: int, ruta: str, detalle: str = ""):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    icono = _ICONOS.get(status_code, "•")
    print(f"  {icono} [{ts}] {status_code} {ruta}  {detalle}")
