import httpx

from app.ai.base import ProveedorIAError, ProveedorLLM, RespuestaLLM
from app.core.config import get_settings

URL_CHAT = "https://api.openai.com/v1/chat/completions"


class OpenAIProveedor(ProveedorLLM):
    nombre = "openai"

    def __init__(self, api_key: str, modelo: str | None = None):
        self.api_key = api_key
        self.modelo = modelo or "gpt-4o-mini"

    def generar(self, prompt_sistema: str, prompt_usuario: str, json_mode: bool = False) -> RespuestaLLM:
        body = {
            "model": self.modelo,
            "messages": [
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            "temperature": 0.3,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}

        try:
            resp = httpx.post(
                URL_CHAT,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=body,
                timeout=get_settings().ai_timeout_seg,
            )
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise ProveedorIAError(f"OpenAI falló: {exc}") from exc

        data = resp.json()
        usage = data.get("usage", {})
        return RespuestaLLM(
            texto=data["choices"][0]["message"]["content"],
            modelo=data.get("model", self.modelo),
            tokens_entrada=usage.get("prompt_tokens", 0),
            tokens_salida=usage.get("completion_tokens", 0),
        )
