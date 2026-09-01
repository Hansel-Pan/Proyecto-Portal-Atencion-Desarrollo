import logging
from functools import lru_cache

from app.ai.base import ProveedorLLM
from app.ai.gemini_provider import GeminiProveedor
from app.ai.mock_provider import MockProveedor
from app.ai.ollama_provider import OllamaProveedor
from app.ai.openai_provider import OpenAIProveedor
from app.core.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache
def obtener_proveedor() -> ProveedorLLM:
    s = get_settings()
    match s.ai_provider:
        case "openai":
            if not s.openai_api_key:
                logger.warning("OPENAI_API_KEY vacía: se usa el proveedor mock temporalmente")
                return MockProveedor()
            return OpenAIProveedor(s.openai_api_key, s.ai_model)
        case "gemini":
            if not s.gemini_api_key:
                logger.warning("GEMINI_API_KEY vacía: se usa el proveedor mock temporalmente")
                return MockProveedor()
            return GeminiProveedor(s.gemini_api_key, s.ai_model)
        case "ollama":
            return OllamaProveedor(s.ollama_base_url, s.ai_model)
        case _:
            return MockProveedor()
