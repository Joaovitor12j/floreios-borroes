from abc import ABC, abstractmethod
from typing import Any


class Livro(ABC):
    def __init__(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        secao: str,
        preco_base: float,
        quantidade: int,
    ) -> None:
        self.__isbn = self.__validar_isbn(isbn)
        self.titulo = titulo
        self.autor = autor
        self.secao = secao
        self.preco_base = preco_base
        self.quantidade = quantidade

    @property
    def isbn(self) -> str:
        return self.__isbn

    @staticmethod
    def __validar_isbn(isbn: str) -> str:
        digitos = isbn.replace("-", "").replace(" ", "")
        if len(digitos) not in (10, 13) or not digitos.isdigit():
            raise ValueError(f"ISBN inválido: {isbn!r}")
        return digitos

    @abstractmethod
    def calcular_preco(self) -> float:
        ...

    @abstractmethod
    def descricao_catalogo(self) -> str:
        ...

    def _descricao_base(self) -> str:
        return f"{self.titulo}, de {self.autor} [{self.secao}]"

    def corresponde_estado_conservacao(self, estado: object | None) -> bool:
        return estado is None

    def to_dict(self) -> dict[str, Any]:
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "secao": self.secao,
            "preco_base": self.preco_base,
            "quantidade": self.quantidade,
        }

    @staticmethod
    def from_dict(dados: dict[str, Any]) -> "Livro":
        from dominio.livro_novo import LivroNovo
        from dominio.livro_raro import LivroRaro
        from dominio.livro_usado import LivroUsado

        fabricas = {
            "novo": LivroNovo.from_dict,
            "usado": LivroUsado.from_dict,
            "raro": LivroRaro.from_dict,
        }
        tipo = dados["tipo"]
        if tipo not in fabricas:
            raise ValueError(f"Tipo de livro desconhecido: {tipo!r}")
        return fabricas[tipo](dados)
