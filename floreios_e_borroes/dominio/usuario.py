from abc import ABC, abstractmethod


class Usuario(ABC):
    def __init__(self, nome: str, email: str) -> None:
        self.nome = nome
        self.email = email

    @abstractmethod
    def nivel_acesso(self) -> str:
        ...


class Cliente(Usuario):
    def nivel_acesso(self) -> str:
        return "cliente"


class Administrador(Usuario):
    def __init__(self, nome: str, email: str, cargo: str) -> None:
        super().__init__(nome, email)
        self.cargo = cargo

    def nivel_acesso(self) -> str:
        return "administrador"
