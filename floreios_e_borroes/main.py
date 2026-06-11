from pathlib import Path

from infra.repositorio_json import RepositorioJson
from servicos.catalogo import Catalogo
from servicos.estoque import Estoque
from ui.app_tkinter import App

CAMINHO_ACERVO = Path(__file__).resolve().parent / "dados" / "acervo.json"


def main() -> None:
    repositorio = RepositorioJson(CAMINHO_ACERVO)
    estoque = Estoque(repositorio.carregar())
    catalogo = Catalogo(estoque)

    app = App(catalogo, estoque, persistir=lambda: repositorio.salvar(estoque.livros))
    app.mainloop()


if __name__ == "__main__":
    main()
