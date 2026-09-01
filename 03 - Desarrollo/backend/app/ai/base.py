import json
from abc import ABC, abstractmethod
from dataclasses import dataclass


class ProveedorIAError(RuntimeError):
    pass


def extraer_json(texto: str) -> dict:
    texto = texto.strip()
    if "```" in texto:
        entre_cercas = texto.split("```")[1]
        if entre_cercas.startswith("json"):
            entre_cercas = entre_cercas[4:]
        texto = entre_cercas.strip()
    inicio, fin = texto.find("{"), texto.rfind("}")
    if inicio == -1 or fin <= inicio:
        raise ValueError("La respuesta no contiene un objeto JSON")
    return json.loads(texto[inicio : fin + 1])


@dataclass
class RespuestaLLM:
    texto: str
    modelo: str
    tokens_entrada: int = 0
    tokens_salida: int = 0


class ProveedorLLM(ABC):
    nombre: str = "base"

    @abstractmethod
    def generar(self, prompt_sistema: str, prompt_usuario: str, json_mode: bool = False) -> RespuestaLLM:
        raise NotImplementedError
