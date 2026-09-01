import httpx

from app.ai.base import ProveedorIAError, ProveedorLLM, RespuestaLLM
from app.core.config import get_settings

URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


class GeminiProveedor(ProveedorLLM):
    nombre = "gemini"

    def __init__(self, api_key: str, modelo: str | None = None):
        self.api_key = api_key
        self.modelo = modelo or "gemini-3.6-flash"

    def generar(self, prompt_sistema: str, prompt_usuario: str, json_mode: bool = False) -> RespuestaLLM:
        body = {
            "systemInstruction": {"parts": [{"text": prompt_sistema}]},
            "contents": [{"role": "user", "parts": [{"text": prompt_usuario}]}],
            "generationConfig": {
                "temperature": 0.3,
                **({"responseMimeType": "application/json"} if json_mode else {}),
            },
        }

        try:
            resp = httpx.post(
                f"{URL_BASE}/{self.modelo}:generateContent",
                headers={"x-goog-api-key": self.api_key},
                json=body,
                timeout=get_settings().ai_timeout_seg,
            )
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            detalle = ""
            if exc.response is not None:
                try:
                    detalle = exc.response.json().get("error", {}).get("message", "")
                except Exception:
                    detalle = exc.response.text[:200]
            raise ProveedorIAError(f"Gemini falló: {exc} {detalle}") from exc

        data = resp.json()
        try:
            texto = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as exc:
            raise ProveedorIAError(f"Respuesta de Gemini sin contenido: {data}") from exc

        usage = data.get("usageMetadata", {})
        return RespuestaLLM(
            texto=texto,
            modelo=data.get("modelVersion", self.modelo),
            tokens_entrada=usage.get("promptTokenCount", 0),
            tokens_salida=usage.get("candidatesTokenCount", 0),
        )
