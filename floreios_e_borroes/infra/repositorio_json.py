import json
from pathlib import Path

from dominio.item_acervo import Livro


class RepositorioJson:
    def __init__(self, caminho_arquivo: Path | str) -> None:
        self._caminho = Path(caminho_arquivo)

    def carregar(self) -> list[Livro]:
        if not self._caminho.exists():
            return []
        with self._caminho.open("r", encoding="utf-8") as arquivo:
            registros = json.load(arquivo)
        return [Livro.from_dict(registro) for registro in registros]

    def salvar(self, livros: list[Livro]) -> None:
        registros = [livro.to_dict() for livro in livros]
        with self._caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(registros, arquivo, ensure_ascii=False, indent=2)
