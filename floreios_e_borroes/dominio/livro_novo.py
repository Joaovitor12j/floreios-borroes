from typing import Any

from dominio.item_acervo import Livro


class LivroNovo(Livro):
    def calcular_preco(self) -> float:
        return self.preco_base

    def descricao_catalogo(self) -> str:
        return f"{self._descricao_base()} (Novo)"

    def to_dict(self) -> dict[str, Any]:
        dados = super().to_dict()
        dados["tipo"] = "novo"
        return dados

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> "LivroNovo":
        return cls(
            isbn=dados["isbn"],
            titulo=dados["titulo"],
            autor=dados["autor"],
            secao=dados["secao"],
            preco_base=dados["preco_base"],
            quantidade=dados["quantidade"],
        )
