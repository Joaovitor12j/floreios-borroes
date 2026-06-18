from pathlib import Path

from infra.repositorio_caixa_json import RepositorioCaixaJson
from infra.repositorio_json import RepositorioJson
from infra.repositorio_usuarios_json import RepositorioUsuariosJson
from servicos.caixa import Caixa
from servicos.catalogo import Catalogo
from servicos.estoque import Estoque
from servicos.usuarios import Usuarios
from ui.app_tkinter import App

CAMINHO_ACERVO = Path(__file__).resolve().parent / "dados" / "acervo.json"
CAMINHO_USUARIOS = Path(__file__).resolve().parent / "dados" / "usuarios.json"
CAMINHO_CAIXA = Path(__file__).resolve().parent / "dados" / "caixa.json"


def main() -> None:
    repositorio = RepositorioJson(CAMINHO_ACERVO)
    estoque = Estoque(repositorio.carregar())
    catalogo = Catalogo(estoque)

    repositorio_usuarios = RepositorioUsuariosJson(CAMINHO_USUARIOS)
    usuarios = Usuarios(repositorio_usuarios.carregar())

    repositorio_caixa = RepositorioCaixaJson(CAMINHO_CAIXA)
    vendas = repositorio_caixa.carregar()
    caixa = Caixa(estoque)

    def _persistir_venda(venda):
        vendas.append(venda)
        repositorio_caixa.salvar(vendas)

    app = App(
        catalogo,
        estoque,
        usuarios,
        caixa,
        persistir_acervo=lambda: repositorio.salvar(estoque.livros),
        persistir_usuarios=lambda: repositorio_usuarios.salvar(usuarios.usuarios),
        persistir_venda=_persistir_venda,
    )
    app.mainloop()


if __name__ == "__main__":
    main()
