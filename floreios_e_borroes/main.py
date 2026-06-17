from pathlib import Path

from infra.repositorio_json import RepositorioJson
from infra.repositorio_usuarios_json import RepositorioUsuariosJson
from servicos.catalogo import Catalogo
from servicos.estoque import Estoque
from servicos.usuarios import Usuarios
from ui.app_tkinter import App

CAMINHO_ACERVO = Path(__file__).resolve().parent / "dados" / "acervo.json"
CAMINHO_USUARIOS = Path(__file__).resolve().parent / "dados" / "usuarios.json"


def main() -> None:
    repositorio = RepositorioJson(CAMINHO_ACERVO)
    estoque = Estoque(repositorio.carregar())
    catalogo = Catalogo(estoque)

    repositorio_usuarios = RepositorioUsuariosJson(CAMINHO_USUARIOS)
    usuarios = Usuarios(repositorio_usuarios.carregar())

    app = App(
        catalogo,
        estoque,
        usuarios,
        persistir_acervo=lambda: repositorio.salvar(estoque.livros),
        persistir_usuarios=lambda: repositorio_usuarios.salvar(usuarios.usuarios)
    )
    app.mainloop()


if __name__ == "__main__":
    main()
