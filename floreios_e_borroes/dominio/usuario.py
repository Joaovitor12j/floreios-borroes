from abc import ABC, abstractmethod
from typing import Any


class Usuario(ABC):
    def __init__(self, nome: str, email: str, senha: str) -> None:
        self.nome = nome
        self.email = email
        self.senha = senha

    @abstractmethod
    def nivel_acesso(self) -> str:
        ...

    def verifica_senha(self, senha: str) -> bool:
        return self.senha == senha

    def to_dict(self) -> dict[str, Any]:
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
        }

    @staticmethod
    def from_dict(dados: dict[str, Any]) -> "Usuario":
        fabricas = {
            "cliente": Cliente.from_dict,
            "administrador": Administrador.from_dict,
        }
        tipo = dados["tipo"]
        if tipo not in fabricas:
            raise ValueError(f"tipo de usuario desconhecido: {tipo!r}")
        return fabricas[tipo](dados)


class Cliente(Usuario):
    def nivel_acesso(self) -> str:
        return "cliente"

    def to_dict(self) -> dict[str, Any]:
        dados = super().to_dict()
        dados["tipo"] = "cliente"
        return dados

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> "Cliente":
        return cls(nome=dados["nome"], email=dados["email"], senha=dados["senha"])


class Administrador(Usuario):
    def __init__(self, nome: str, email: str, senha: str, cargo: str = "Administrador") -> None:
        super().__init__(nome, email, senha)
        self.cargo = cargo

    def nivel_acesso(self) -> str:
        return "administrador"

    def to_dict(self) -> dict[str, Any]:
        dados = super().to_dict()
        dados["tipo"] = "administrador"
        dados["cargo"] = self.cargo
        return dados

    @classmethod
    def from_dict(cls, dados: dict[str, Any]) -> "Administrador":
        return cls(
            nome=dados["nome"],
            email=dados["email"],
            senha=dados["senha"],
            cargo=dados.get("cargo", "Administrador"),
        )
