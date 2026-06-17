import json
from pathlib import Path

from dominio.usuario import Usuario


class RepositorioUsuariosJson:
    def __init__(self, caminho_arquivo: Path | str) -> None:
        self._caminho = Path(caminho_arquivo)

    def carregar(self) -> list[Usuario]:
        if not self._caminho.exists():
            return []
        with self._caminho.open("r", encoding="utf-8") as arquivo:
            registros = json.load(arquivo)
        return [Usuario.from_dict(registro) for registro in registros]

    def salvar(self, usuarios: list[Usuario]) -> None:
        registros = [usuario.to_dict() for usuario in usuarios]
        with self._caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(registros, arquivo, ensure_ascii=False, indent=2)