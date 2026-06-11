from dominio.item_acervo import Livro
from dominio.livro_usado import EstadoConservacao
from servicos.estoque import Estoque


class Catalogo:
    def __init__(self, estoque: Estoque) -> None:
        self._estoque = estoque

    def listar(self) -> list[Livro]:
        return self._estoque.livros

    def secoes_disponiveis(self) -> list[str]:
        return sorted({livro.secao for livro in self._estoque.livros})

    def buscar(self, termo: str) -> list[Livro]:
        return self.pesquisar(termo=termo)

    def filtrar(
        self,
        secao: str | None = None,
        estado_conservacao: EstadoConservacao | None = None,
    ) -> list[Livro]:
        return self.pesquisar(secao=secao, estado_conservacao=estado_conservacao)

    def pesquisar(
        self,
        termo: str = "",
        secao: str | None = None,
        estado_conservacao: EstadoConservacao | None = None,
    ) -> list[Livro]:
        termo_normalizado = termo.strip().lower()
        return [
            livro
            for livro in self._estoque.livros
            if (secao is None or livro.secao == secao)
            and livro.corresponde_estado_conservacao(estado_conservacao)
            and self._corresponde_termo(livro, termo_normalizado)
        ]

    @staticmethod
    def _corresponde_termo(livro: Livro, termo: str) -> bool:
        if not termo:
            return True
        return (
            termo in livro.titulo.lower()
            or termo in livro.autor.lower()
            or termo in livro.secao.lower()
        )
