import json
from pathlib import Path

from dominio.venda import Venda


class RepositorioCaixaJson:
    def __init__(self, caminho_arquivo: Path | str) -> None:
        self._caminho = Path(caminho_arquivo)

    def carregar(self) -> list[Venda]:
        if not self._caminho.exists():
            return []
        with self._caminho.open("r", encoding="utf-8") as arquivo:
            registros = json.load(arquivo)
        return [Venda.from_dict(registro) for registro in registros]

    def salvar(self, vendas: list[Venda]) -> None:
        registros = [venda.to_dict() for venda in vendas]
        with self._caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(registros, arquivo, ensure_ascii=False, indent=2)
