from datetime import datetime
from typing import Any


class ItemVenda:
    def __init__(self, isbn: str, titulo: str, quantidade: int, preco_unitario: float) -> None:
        self.isbn = isbn
        self.titulo = titulo
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def subtotal(self) -> float:
        return round(self.preco_unitario * self.quantidade, 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
        }

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> "ItemVenda":
        return cls(
            isbn=dados["isbn"],
            titulo=dados["titulo"],
            quantidade=dados["quantidade"],
            preco_unitario=dados["preco_unitario"],
        )


class Venda:
    def __init__(
        self,
        cliente_email: str,
        cliente_nome: str,
        itens: list[ItemVenda],
        data_hora: datetime | None = None,
    ) -> None:
        self.cliente_email = cliente_email
        self.cliente_nome = cliente_nome
        self.itens = itens
        self.data_hora = data_hora if data_hora is not None else datetime.now()

    def total(self) -> float:
        return round(sum(item.subtotal() for item in self.itens), 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cliente_email": self.cliente_email,
            "cliente_nome": self.cliente_nome,
            "itens": [item.to_dict() for item in self.itens],
            "data_hora": self.data_hora.isoformat(),
            "total": self.total(),
        }

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> "Venda":
        return cls(
            cliente_email=dados["cliente_email"],
            cliente_nome=dados["cliente_nome"],
            itens=[ItemVenda.from_dict(item) for item in dados["itens"]],
            data_hora=datetime.fromisoformat(dados["data_hora"]),
        )
