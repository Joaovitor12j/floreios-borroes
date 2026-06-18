from functools import singledispatchmethod
from typing import Any

from dominio.item_acervo import Livro


class Estoque:
    def __init__(self, livros: list[Livro] | None = None) -> None:
        self._livros: list[Livro] = livros if livros is not None else []

    @property
    def livros(self) -> list[Livro]:
        return list(self._livros)

    def buscar_por_isbn(self, isbn: str) -> Livro | None:
        for livro in self._livros:
            if livro.isbn == isbn:
                return livro
        return None

    def disponivel(self, isbn: str) -> bool:
        livro = self.buscar_por_isbn(isbn)
        return livro is not None and livro.quantidade > 0

    @singledispatchmethod
    def adicionar(self, item: object, quantidade: int = 0) -> None:
        raise TypeError(f"Tipo não suportado para adicionar ao estoque: {type(item)!r}")

    @adicionar.register
    def _(self, item: Livro, quantidade: int = 0) -> None:
        existente = self.buscar_por_isbn(item.isbn)
        if existente is None:
            self._livros.append(item)
        else:
            existente.quantidade += item.quantidade

    @adicionar.register
    def _(self, item: str, quantidade: int = 0) -> None:
        livro = self.buscar_por_isbn(item)
        if livro is None:
            raise ValueError(f"Livro com ISBN {item!r} não encontrado no estoque")
        livro.quantidade += quantidade

    def vender(self, isbn: str, quantidade: int) -> None:
        livro = self.buscar_por_isbn(isbn)
        if livro is None:
            raise ValueError(f"Livro com ISBN {isbn!r} não encontrado no estoque")
        if quantidade <= 0:
            raise ValueError("A quantidade vendida deve ser maior que zero")
        if livro.quantidade < quantidade:
            raise ValueError(
                f"Estoque insuficiente para o ISBN {isbn!r}: disponível {livro.quantidade}, solicitado {quantidade}"
            )
        livro.quantidade -= quantidade

    def remover(self, isbn: str) -> None:
        livro = self.buscar_por_isbn(isbn)
        if livro is None:
            raise ValueError(f"Livro com ISBN {isbn!r} não encontrado no estoque")
        self._livros.remove(livro)

    def atualizar(self, livro: Livro) -> None:
        existente = self.buscar_por_isbn(livro.isbn)
        if existente is None:
            raise ValueError(f"Livro com ISBN {livro.isbn!r} não encontrado no estoque")
        self._livros[self._livros.index(existente)] = livro

    def adicionar_a_partir_de_dict(self, dados: dict[str, Any]) -> Livro:
        livro = Livro.from_dict(dados)
        self.adicionar(livro)
        return livro

    def atualizar_a_partir_de_dict(self, dados: dict[str, Any]) -> Livro:
        livro = Livro.from_dict(dados)
        self.atualizar(livro)
        return livro
