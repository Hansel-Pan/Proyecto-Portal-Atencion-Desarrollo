import httpx

from app.ai.base import ProveedorIAError, ProveedorLLM, RespuestaLLM
from app.core.config import get_settings


class OllamaProveedor(ProveedorLLM):
    nombre = "ollama"

    def __init__(self, base_url: str, modelo: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.modelo = modelo or "llama3.2"

    def generar(self, prompt_sistema: str, prompt_usuario: str, json_mode: bool = False) -> RespuestaLLM:
        body = {
            "model": self.modelo,
            "messages": [
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            "stream": False,
            "options": {"temperature": 0.3},
        }
        if json_mode:
            body["format"] = "json"

        try:
            resp = httpx.post(
                f"{self.base_url}/api/chat",
                json=body,
                timeout=get_settings().ai_timeout_seg,
            )
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise ProveedorIAError(f"Ollama falló: {exc}") from exc

        data = resp.json()
        return RespuestaLLM(
            texto=data["message"]["content"],
            modelo=data.get("model", self.modelo),
            tokens_entrada=data.get("prompt_eval_count", 0),
            tokens_salida=data.get("eval_count", 0),
        )
