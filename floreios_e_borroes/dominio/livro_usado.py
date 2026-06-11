from enum import Enum
from typing import Any

from dominio.item_acervo import Livro


class EstadoConservacao(Enum):
    SEMINOVO = "Seminovo"
    BOM = "Bom"
    REGULAR = "Regular"
    DESGASTADO = "Desgastado"

    def fator_depreciacao(self) -> float:
        fatores = {
            EstadoConservacao.SEMINOVO: 0.85,
            EstadoConservacao.BOM: 0.70,
            EstadoConservacao.REGULAR: 0.55,
            EstadoConservacao.DESGASTADO: 0.40,
        }
        return fatores[self]


class LivroUsado(Livro):
    def __init__(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        secao: str,
        preco_base: float,
        quantidade: int,
        estado_conservacao: EstadoConservacao,
    ) -> None:
        super().__init__(isbn, titulo, autor, secao, preco_base, quantidade)
        self.estado_conservacao = estado_conservacao

    def calcular_preco(self) -> float:
        return round(self.preco_base * self.estado_conservacao.fator_depreciacao(), 2)

    def descricao_catalogo(self) -> str:
        return f"{self._descricao_base()} (Usado — {self.estado_conservacao.value})"

    def corresponde_estado_conservacao(self, estado: EstadoConservacao | None) -> bool:
        return estado is None or self.estado_conservacao is estado

    def to_dict(self) -> dict[str, Any]:
        dados = super().to_dict()
        dados["tipo"] = "usado"
        dados["estado_conservacao"] = self.estado_conservacao.name
        return dados

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> "LivroUsado":
        return cls(
            isbn=dados["isbn"],
            titulo=dados["titulo"],
            autor=dados["autor"],
            secao=dados["secao"],
            preco_base=dados["preco_base"],
            quantidade=dados["quantidade"],
            estado_conservacao=EstadoConservacao[dados["estado_conservacao"]],
        )
