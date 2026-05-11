import urllib.request
import urllib.parse
import json
from pathlib import Path
import sys

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

def _get_bot_token() -> str:
    config_path = get_base_dir() / "config" / "api_keys.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)["telegram_bot_token"]

# chat_ids conocidos por rol
CHAT_IDS = {
    "reke":   "470743142",
    "german": "GERMAN_CHAT_ID",   # completar cuando Germán linkee su cuenta
    "gaston": "GASTON_CHAT_ID",   # completar cuando Gastón linkee su cuenta
}

def tms_telegram(parameters: dict, player=None, speak=None) -> str:
    mensaje   = parameters.get("mensaje", "")
    destinatario = parameters.get("destinatario", "reke").lower()

    chat_id = CHAT_IDS.get(destinatario)
    if not chat_id or "CHAT_ID" in chat_id:
        return f"No tengo el chat_id de {destinatario} configurado todavía."

    if not mensaje:
        return "No hay mensaje para enviar."

    try:
        token = _get_bot_token()
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": mensaje
        }).encode()
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
        if result.get("ok"):
            return f"Mensaje enviado a {destinatario} por Telegram."
        else:
            return f"Error Telegram: {result.get('description', 'desconocido')}"
    except Exception as e:
        return f"Error al enviar Telegram: {e}"
