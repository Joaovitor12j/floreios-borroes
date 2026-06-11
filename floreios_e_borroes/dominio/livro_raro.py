from enum import Enum
from typing import Any

from dominio.item_acervo import Livro


class GrauRaridade(Enum):
    INCOMUM = "Incomum"
    RARO = "Raro"
    MUITO_RARO = "Muito raro"
    EXTREMAMENTE_RARO = "Extremamente raro"

    def fator_agio(self) -> float:
        fatores = {
            GrauRaridade.INCOMUM: 1.5,
            GrauRaridade.RARO: 2.0,
            GrauRaridade.MUITO_RARO: 3.5,
            GrauRaridade.EXTREMAMENTE_RARO: 6.0,
        }
        return fatores[self]


class LivroRaro(Livro):
    def __init__(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        secao: str,
        preco_base: float,
        quantidade: int,
        grau_raridade: GrauRaridade,
    ) -> None:
        super().__init__(isbn, titulo, autor, secao, preco_base, quantidade)
        self.grau_raridade = grau_raridade

    def calcular_preco(self) -> float:
        return round(self.preco_base * self.grau_raridade.fator_agio(), 2)

    def descricao_catalogo(self) -> str:
        return f"{self._descricao_base()} (Raro — {self.grau_raridade.value})"

    def to_dict(self) -> dict[str, Any]:
        dados = super().to_dict()
        dados["tipo"] = "raro"
        dados["grau_raridade"] = self.grau_raridade.name
        return dados

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> "LivroRaro":
        return cls(
            isbn=dados["isbn"],
            titulo=dados["titulo"],
            autor=dados["autor"],
            secao=dados["secao"],
            preco_base=dados["preco_base"],
            quantidade=dados["quantidade"],
            grau_raridade=GrauRaridade[dados["grau_raridade"]],
        )
