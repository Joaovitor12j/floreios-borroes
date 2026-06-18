from dominio.usuario import Cliente
from dominio.venda import ItemVenda, Venda
from servicos.estoque import Estoque


class Caixa:
    def __init__(self, estoque: Estoque) -> None:
        self._estoque = estoque

    def finalizar_venda(self, cliente: Cliente, itens_carrinho: dict[str, int]) -> Venda:
        if not itens_carrinho:
            raise ValueError("O carrinho está vazio")

        itens_venda: list[ItemVenda] = []
        for isbn, quantidade in itens_carrinho.items():
            livro = self._estoque.buscar_por_isbn(isbn)
            if livro is None:
                raise ValueError(f"Livro com ISBN {isbn!r} não encontrado no estoque")
            if livro.quantidade < quantidade:
                raise ValueError(
                    f"Estoque insuficiente para {livro.titulo!r}: "
                    f"disponível {livro.quantidade}, solicitado {quantidade}"
                )
            itens_venda.append(
                ItemVenda(
                    isbn=livro.isbn,
                    titulo=livro.titulo,
                    quantidade=quantidade,
                    preco_unitario=livro.calcular_preco(),
                )
            )

        for isbn, quantidade in itens_carrinho.items():
            self._estoque.vender(isbn, quantidade)

        return Venda(cliente_email=cliente.email, cliente_nome=cliente.nome, itens=itens_venda)
