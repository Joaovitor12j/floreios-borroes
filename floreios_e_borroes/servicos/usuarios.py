from dominio.usuario import Cliente, Usuario

class EmailJaCadastradoError(Exception):
    pass

class Usuarios:
    def __init__(self, usuarios: list[Usuario] | None = None):
        self._usuarios: list[Usuario] = usuarios if usuarios is not None else []

    @property
    def usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def buscar_por_email(self, email: str) -> Usuario | None:
        email_normalizado = email.strip().lower()
        for usuario in self.usuarios:
            if usuario.email.strip().lower() == email_normalizado:
                return usuario
        return None

    def autenticar(self, email: str, senha: str) -> Usuario | None:
        usuario = self.buscar_por_email(email)
        if usuario is not None and usuario.verifica_senha(senha):
            return usuario
        return None

    def adicionar(self, usuario: Usuario) -> None:
        if self.buscar_por_email(usuario.email) is not None:
            raise EmailJaCadastradoError(f"Email ja cadastrado")
        self._usuarios.append(usuario)

    def cadastrar_cliente(self, nome: str, email: str, senha: str) -> Cliente:
        cliente = Cliente(nome, email, senha)
        self.adicionar(cliente)
        return cliente