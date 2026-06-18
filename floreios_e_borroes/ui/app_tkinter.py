import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk
from typing import Any

from dominio.item_acervo import Livro
from dominio.livro_raro import GrauRaridade
from dominio.livro_usado import EstadoConservacao
from dominio.usuario import Administrador, Cliente, Usuario
from dominio.venda import Venda
from servicos.caixa import Caixa
from servicos.catalogo import Catalogo
from servicos.estoque import Estoque
from servicos.usuarios import EmailJaCadastradoError, Usuarios

COR_FUNDO = "#F4ECD8"
COR_CARTAO = "#FFFDF7"
COR_DESTAQUE = "#5C3A21"
COR_DESTAQUE_CLARO = "#7A5230"
COR_TEXTO = "#3B2412"
COR_TEXTO_CLARO = "#FBF6EC"

FONTE_TITULO = ("Georgia", 18, "bold")
FONTE_SUBTITULO = ("Georgia", 13, "bold")
FONTE_CORPO = ("Helvetica", 10)
FONTE_CORPO_NEGRITO = ("Helvetica", 10, "bold")

SECAO_TODAS = "Todas as seções"
ESTADO_TODOS = "Todos os estados"

TIPO_NOVO = "Novo"
TIPO_USADO = "Usado"
TIPO_RARO = "Raro"

ROTULO_PARA_TIPO = {TIPO_NOVO: "novo", TIPO_USADO: "usado", TIPO_RARO: "raro"}
TIPO_PARA_ROTULO = {tipo: rotulo for rotulo, tipo in ROTULO_PARA_TIPO.items()}


class App(tk.Tk):
    def __init__(
        self,
        catalogo: Catalogo,
        estoque: Estoque,
        usuarios: Usuarios,
        caixa: Caixa,
        persistir_acervo: Callable[[], None],
        persistir_usuarios: Callable[[], None],
        persistir_venda: Callable[[Venda], None],
    ) -> None:
        super().__init__()
        self.title("Floreios e Borrões")
        self.geometry("1024x640")
        self.configure(background=COR_FUNDO)

        self._usuario_atual: Usuario | None = None

        self._configurar_estilo()
        self._montar_navegacao()

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self._telas: dict[str, ttk.Frame] = {
            "login": TelaLogin(
                container,
                usuarios,
                ao_autenticar=self._ao_autenticar,
                ir_para_cadastro=lambda: self.mostrar_tela("cadastro"),
            ),
            "cadastro": TelaCadastro(
                container,
                usuarios,
                persistir_usuarios,
                ao_autenticar=self._ao_autenticar,
                voltar_para_login=lambda: self.mostrar_tela("login"),
            ),
            "cliente": TelaCliente(
                container,
                catalogo,
                estoque,
                caixa,
                usuario_atual=lambda: self._usuario_atual,
                persistir_acervo=persistir_acervo,
                persistir_venda=persistir_venda,
            ),
            "admin": TelaAdministrador(container, estoque, persistir_acervo),
        }
        for tela in self._telas.values():
            tela.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela("login")

    def mostrar_tela(self, nome: str) -> None:
        tela = self._telas[nome]
        tela.tkraise()
        tela.atualizar()

    def _ao_autenticar(self, usuario: Usuario) -> None:
        self._usuario_atual = usuario
        self._atualizar_navegacao()
        self.mostrar_tela("admin" if isinstance(usuario, Administrador) else "cliente")

    def _sair(self) -> None:
        self._usuario_atual = None
        self._telas["cliente"].limpar_carrinho()
        self._atualizar_navegacao()
        self._telas["login"].limpar()
        self.mostrar_tela("login")

    def _montar_navegacao(self) -> None:
        barra = ttk.Frame(self, style="Navegacao.TFrame", padding=(16, 10))
        barra.pack(fill="x")

        ttk.Label(barra, text="Floreios e Borrões", style="Titulo.TLabel").pack(side="left")

        self._area_navegacao = ttk.Frame(barra, style="Navegacao.TFrame")
        self._area_navegacao.pack(side="left", padx=(24, 0))

        self._area_usuario = ttk.Frame(barra, style="Navegacao.TFrame")
        self._area_usuario.pack(side="right")
        self._atualizar_navegacao()

    def _atualizar_navegacao(self) -> None:
        for filho in self._area_navegacao.winfo_children():
            filho.destroy()
        for filho in self._area_usuario.winfo_children():
            filho.destroy()

        if self._usuario_atual is None:
            return

        if isinstance(self._usuario_atual, Administrador):
            ttk.Button(
                self._area_navegacao, text="Catálogo", command=lambda: self.mostrar_tela("cliente")
            ).pack(side="left", padx=(0, 8))
            ttk.Button(
                self._area_navegacao, text="Estoque", command=lambda: self.mostrar_tela("admin")
            ).pack(side="left")

        texto = f"{self._usuario_atual.nome} · {self._usuario_atual.nivel_acesso().capitalize()}"
        ttk.Label(self._area_usuario, text=texto, style="Titulo.TLabel").pack(side="left", padx=(0, 12))
        ttk.Button(self._area_usuario, text="Sair", command=self._sair).pack(side="left")

    def _configurar_estilo(self) -> None:
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure("TFrame", background=COR_FUNDO)
        estilo.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO, font=FONTE_CORPO)
        estilo.configure("Navegacao.TFrame", background=COR_DESTAQUE)
        estilo.configure("Titulo.TLabel", font=FONTE_TITULO, foreground=COR_TEXTO_CLARO, background=COR_DESTAQUE)

        estilo.configure("TButton", background=COR_DESTAQUE, foreground=COR_TEXTO_CLARO, font=FONTE_CORPO, padding=6)
        estilo.map("TButton", background=[("active", COR_DESTAQUE_CLARO)])

        estilo.configure("Cartao.TFrame", background=COR_CARTAO, relief="ridge", borderwidth=1)
        estilo.configure("Cartao.TLabel", background=COR_CARTAO, font=FONTE_CORPO)
        estilo.configure("CartaoTitulo.TLabel", background=COR_CARTAO, font=FONTE_SUBTITULO, foreground=COR_DESTAQUE)

        estilo.configure("Treeview", background=COR_CARTAO, fieldbackground=COR_CARTAO, font=FONTE_CORPO, rowheight=24)
        estilo.configure("Treeview.Heading", font=FONTE_CORPO_NEGRITO, foreground=COR_DESTAQUE, background=COR_FUNDO)


class TelaLogin(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        usuarios: Usuarios,
        ao_autenticar: Callable[[Usuario], None],
        ir_para_cadastro: Callable[[], None],
    ) -> None:
        super().__init__(master, padding=16)
        self._usuarios = usuarios
        self._ao_autenticar = ao_autenticar
        self._ir_para_cadastro = ir_para_cadastro

        self._var_email = tk.StringVar()
        self._var_senha = tk.StringVar()

        self._montar()

    def atualizar(self) -> None:
        pass

    def limpar(self) -> None:
        self._var_email.set("")
        self._var_senha.set("")

    def _montar(self) -> None:
        cartao = ttk.Frame(self, style="Cartao.TFrame", padding=24)
        cartao.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(cartao, text="Entrar", style="CartaoTitulo.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
        )

        ttk.Label(cartao, text="E-mail", style="Cartao.TLabel").grid(row=1, column=0, columnspan=2, sticky="w")
        campo_email = ttk.Entry(cartao, textvariable=self._var_email, width=30)
        campo_email.grid(row=2, column=0, columnspan=2, sticky="we", pady=(0, 12))

        ttk.Label(cartao, text="Senha", style="Cartao.TLabel").grid(row=3, column=0, columnspan=2, sticky="w")
        campo_senha = ttk.Entry(cartao, textvariable=self._var_senha, show="•", width=30)
        campo_senha.grid(row=4, column=0, columnspan=2, sticky="we", pady=(0, 16))
        campo_senha.bind("<Return>", lambda _evento: self._entrar())

        ttk.Button(cartao, text="Entrar", command=self._entrar).grid(
            row=5, column=0, columnspan=2, sticky="we", pady=(0, 8)
        )
        ttk.Button(cartao, text="Criar conta de cliente", command=self._ir_para_cadastro).grid(
            row=6, column=0, columnspan=2, sticky="we"
        )

    def _entrar(self) -> None:
        email = self._var_email.get().strip()
        senha = self._var_senha.get()

        if not email or not senha:
            messagebox.showerror("Dados inválidos", "Informe e-mail e senha.")
            return

        usuario = self._usuarios.autenticar(email, senha)
        if usuario is None:
            messagebox.showerror("Falha no login", "E-mail ou senha incorretos.")
            return

        self.limpar()
        self._ao_autenticar(usuario)


class TelaCadastro(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        usuarios: Usuarios,
        persistir_usuarios: Callable[[], None],
        ao_autenticar: Callable[[Usuario], None],
        voltar_para_login: Callable[[], None],
    ) -> None:
        super().__init__(master, padding=16)
        self._usuarios = usuarios
        self._persistir_usuarios = persistir_usuarios
        self._ao_autenticar = ao_autenticar
        self._voltar_para_login = voltar_para_login

        self._var_nome = tk.StringVar()
        self._var_email = tk.StringVar()
        self._var_senha = tk.StringVar()
        self._var_confirmar_senha = tk.StringVar()

        self._montar()

    def atualizar(self) -> None:
        pass

    def limpar(self) -> None:
        for variavel in (self._var_nome, self._var_email, self._var_senha, self._var_confirmar_senha):
            variavel.set("")

    def _montar(self) -> None:
        cartao = ttk.Frame(self, style="Cartao.TFrame", padding=24)
        cartao.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(cartao, text="Criar conta de cliente", style="CartaoTitulo.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 16)
        )

        linha = self._criar_campo(cartao, 1, "Nome", self._var_nome)
        linha = self._criar_campo(cartao, linha, "E-mail", self._var_email)
        linha = self._criar_campo(cartao, linha, "Senha", self._var_senha, ocultar=True)
        linha = self._criar_campo(cartao, linha, "Confirmar senha", self._var_confirmar_senha, ocultar=True)

        ttk.Button(cartao, text="Cadastrar", command=self._cadastrar).grid(
            row=linha, column=0, columnspan=2, sticky="we", pady=(8, 8)
        )
        linha += 1
        ttk.Button(cartao, text="Já tenho conta — voltar ao login", command=self._voltar).grid(
            row=linha, column=0, columnspan=2, sticky="we"
        )

    def _criar_campo(
        self, master: tk.Misc, linha: int, rotulo: str, variavel: tk.StringVar, ocultar: bool = False
    ) -> int:
        ttk.Label(master, text=rotulo, style="Cartao.TLabel").grid(row=linha, column=0, columnspan=2, sticky="w")
        entrada = ttk.Entry(master, textvariable=variavel, width=30, show="•" if ocultar else "")
        entrada.grid(row=linha + 1, column=0, columnspan=2, sticky="we", pady=(0, 12))
        return linha + 2

    def _voltar(self) -> None:
        self.limpar()
        self._voltar_para_login()

    def _cadastrar(self) -> None:
        nome = self._var_nome.get().strip()
        email = self._var_email.get().strip()
        senha = self._var_senha.get()
        confirmar_senha = self._var_confirmar_senha.get()

        if not nome or not email or not senha:
            messagebox.showerror("Dados inválidos", "Nome, e-mail e senha são obrigatórios.")
            return
        if senha != confirmar_senha:
            messagebox.showerror("Dados inválidos", "As senhas não coincidem.")
            return

        try:
            cliente = self._usuarios.cadastrar_cliente(nome=nome, email=email, senha=senha)
        except EmailJaCadastradoError as erro:
            messagebox.showerror("Erro ao cadastrar", str(erro))
            return

        self._persistir_usuarios()
        self.limpar()
        messagebox.showinfo("Conta criada", "Cadastro realizado com sucesso. Você já está logado.")
        self._ao_autenticar(cliente)


class TelaCliente(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        catalogo: Catalogo,
        estoque: Estoque,
        caixa: Caixa,
        usuario_atual: Callable[[], Usuario | None],
        persistir_acervo: Callable[[], None],
        persistir_venda: Callable[[Venda], None],
    ) -> None:
        super().__init__(master, padding=16)
        self._catalogo = catalogo
        self._estoque = estoque
        self._caixa = caixa
        self._usuario_atual = usuario_atual
        self._persistir_acervo = persistir_acervo
        self._persistir_venda = persistir_venda

        self._carrinho: dict[str, int] = {}

        self._termo = tk.StringVar()
        self._secao = tk.StringVar(value=SECAO_TODAS)
        self._estado = tk.StringVar(value=ESTADO_TODOS)

        self._montar_filtros()
        self._montar_corpo()

    def _eh_cliente(self) -> bool:
        return isinstance(self._usuario_atual(), Cliente)

    def atualizar(self) -> None:
        self._combo_secao["values"] = (SECAO_TODAS, *self._catalogo.secoes_disponiveis())

        for filho in self._lista.winfo_children():
            filho.destroy()

        livros = self._catalogo.pesquisar(
            termo=self._termo.get(),
            secao=self._secao_selecionada(),
            estado_conservacao=self._estado_selecionado(),
        )
        for livro in livros:
            self._criar_cartao(livro)

        if self._eh_cliente():
            self._painel_carrinho.grid()
            self._atualizar_carrinho()
        else:
            self._painel_carrinho.grid_remove()

    def _montar_filtros(self) -> None:
        filtros = ttk.Frame(self)
        filtros.pack(fill="x", pady=(0, 12))

        ttk.Label(filtros, text="Buscar por título, autor ou seção").grid(row=0, column=0, sticky="w")
        campo_busca = ttk.Entry(filtros, textvariable=self._termo, width=32)
        campo_busca.grid(row=1, column=0, sticky="we", padx=(0, 12))
        campo_busca.bind("<Return>", lambda _evento: self.atualizar())

        ttk.Label(filtros, text="Seção").grid(row=0, column=1, sticky="w")
        self._combo_secao = ttk.Combobox(filtros, textvariable=self._secao, state="readonly", width=18)
        self._combo_secao.grid(row=1, column=1, sticky="we", padx=(0, 12))
        self._combo_secao.bind("<<ComboboxSelected>>", lambda _evento: self.atualizar())

        ttk.Label(filtros, text="Estado de conservação").grid(row=0, column=2, sticky="w")
        valores_estado = (ESTADO_TODOS, *(estado.value for estado in EstadoConservacao))
        combo_estado = ttk.Combobox(
            filtros, textvariable=self._estado, state="readonly", values=valores_estado, width=18
        )
        combo_estado.grid(row=1, column=2, sticky="we", padx=(0, 12))
        combo_estado.bind("<<ComboboxSelected>>", lambda _evento: self.atualizar())

        ttk.Button(filtros, text="Buscar", command=self.atualizar).grid(row=1, column=3, sticky="w")

    def _montar_corpo(self) -> None:
        corpo = ttk.Frame(self)
        corpo.pack(fill="both", expand=True)
        corpo.columnconfigure(0, weight=3)
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(0, weight=1)

        self._montar_lista(corpo)
        self._montar_painel_carrinho(corpo)

    def _montar_lista(self, master: tk.Misc) -> None:
        moldura = ttk.Frame(master)
        moldura.grid(row=0, column=0, sticky="nsew")

        canvas = tk.Canvas(moldura, background=COR_FUNDO, highlightthickness=0)
        rolagem = ttk.Scrollbar(moldura, orient="vertical", command=canvas.yview)
        self._lista = ttk.Frame(canvas)

        self._lista.bind("<Configure>", lambda _evento: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self._lista, anchor="nw")
        canvas.configure(yscrollcommand=rolagem.set)

        canvas.pack(side="left", fill="both", expand=True)
        rolagem.pack(side="right", fill="y")

    def _montar_painel_carrinho(self, master: tk.Misc) -> None:
        self._painel_carrinho = ttk.Frame(master, style="Cartao.TFrame", padding=12)
        self._painel_carrinho.grid(row=0, column=1, sticky="ns", padx=(12, 0))

        ttk.Label(self._painel_carrinho, text="Carrinho", style="CartaoTitulo.TLabel").pack(
            anchor="w", pady=(0, 8)
        )

        self._lista_carrinho = ttk.Frame(self._painel_carrinho, style="Cartao.TFrame")
        self._lista_carrinho.pack(fill="both", expand=True)

        self._label_total = ttk.Label(self._painel_carrinho, text="Total: R$ 0.00", style="Cartao.TLabel")
        self._label_total.pack(anchor="w", pady=(8, 8))

        ttk.Button(self._painel_carrinho, text="Finalizar compra", command=self._finalizar_compra).pack(fill="x")

    def _secao_selecionada(self) -> str | None:
        secao = self._secao.get()
        return None if secao in (SECAO_TODAS, "") else secao

    def _estado_selecionado(self) -> EstadoConservacao | None:
        valor = self._estado.get()
        for estado in EstadoConservacao:
            if estado.value == valor:
                return estado
        return None

    def _criar_cartao(self, livro: Livro) -> None:
        cartao = ttk.Frame(self._lista, style="Cartao.TFrame", padding=12)
        cartao.pack(fill="x", expand=True, padx=4, pady=6)

        ttk.Label(cartao, text=livro.descricao_catalogo(), style="CartaoTitulo.TLabel").pack(anchor="w")
        ttk.Label(cartao, text=f"Preço: R$ {livro.calcular_preco():.2f}", style="Cartao.TLabel").pack(anchor="w")

        status = "Em estoque" if livro.quantidade > 0 else "Indisponível"
        ttk.Label(cartao, text=f"{status} ({livro.quantidade} unidade(s))", style="Cartao.TLabel").pack(anchor="w")

        if self._eh_cliente() and livro.quantidade > 0:
            linha_compra = ttk.Frame(cartao, style="Cartao.TFrame")
            linha_compra.pack(anchor="w", pady=(8, 0))

            var_quantidade = tk.StringVar(value="1")
            ttk.Spinbox(linha_compra, from_=1, to=livro.quantidade, textvariable=var_quantidade, width=5).pack(
                side="left", padx=(0, 8)
            )
            ttk.Button(
                linha_compra,
                text="Adicionar ao carrinho",
                command=lambda isbn=livro.isbn, var=var_quantidade: self._adicionar_ao_carrinho(isbn, var),
            ).pack(side="left")

    def _adicionar_ao_carrinho(self, isbn: str, var_quantidade: tk.StringVar) -> None:
        try:
            quantidade = int(var_quantidade.get())
        except ValueError:
            messagebox.showerror("Quantidade inválida", "Informe um número inteiro.")
            return
        if quantidade <= 0:
            messagebox.showerror("Quantidade inválida", "A quantidade deve ser maior que zero.")
            return

        livro = self._estoque.buscar_por_isbn(isbn)
        if livro is None or livro.quantidade < quantidade:
            messagebox.showerror("Estoque insuficiente", "Quantidade indisponível em estoque.")
            self.atualizar()
            return

        self._carrinho[isbn] = self._carrinho.get(isbn, 0) + quantidade
        self._atualizar_carrinho()

    def _atualizar_carrinho(self) -> None:
        for filho in self._lista_carrinho.winfo_children():
            filho.destroy()

        total = 0.0
        for isbn, quantidade in list(self._carrinho.items()):
            livro = self._estoque.buscar_por_isbn(isbn)
            if livro is None:
                del self._carrinho[isbn]
                continue
            subtotal = livro.calcular_preco() * quantidade
            total += subtotal

            linha = ttk.Frame(self._lista_carrinho, style="Cartao.TFrame")
            linha.pack(fill="x", pady=2)
            ttk.Label(linha, text=f"{livro.titulo} x{quantidade}", style="Cartao.TLabel").pack(side="left")
            ttk.Label(linha, text=f"R$ {subtotal:.2f}", style="Cartao.TLabel").pack(side="left", padx=(8, 8))
            ttk.Button(
                linha, text="Remover", command=lambda isbn=isbn: self._remover_do_carrinho(isbn)
            ).pack(side="right")

        self._label_total.configure(text=f"Total: R$ {total:.2f}")

    def _remover_do_carrinho(self, isbn: str) -> None:
        self._carrinho.pop(isbn, None)
        self._atualizar_carrinho()

    def limpar_carrinho(self) -> None:
        self._carrinho.clear()

    def _finalizar_compra(self) -> None:
        cliente = self._usuario_atual()
        if not isinstance(cliente, Cliente):
            return

        if not self._carrinho:
            messagebox.showinfo("Carrinho vazio", "Adicione livros ao carrinho antes de finalizar.")
            return

        try:
            venda = self._caixa.finalizar_venda(cliente, dict(self._carrinho))
        except ValueError as erro:
            messagebox.showerror("Não foi possível concluir a compra", str(erro))
            self.atualizar()
            return

        self._persistir_acervo()
        self._persistir_venda(venda)
        self._carrinho.clear()
        messagebox.showinfo("Compra realizada", f"Compra finalizada com sucesso. Total: R$ {venda.total():.2f}")
        self.atualizar()


class TelaAdministrador(ttk.Frame):
    def __init__(self, master: tk.Misc, estoque: Estoque, persistir: Callable[[], None]) -> None:
        super().__init__(master, padding=16)
        self._estoque = estoque
        self._persistir = persistir
        self._isbn_em_edicao: str | None = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._montar_tabela()
        self._montar_formulario()

    def atualizar(self) -> None:
        for item in self._tabela.get_children():
            self._tabela.delete(item)

        for livro in self._estoque.livros:
            dados = livro.to_dict()
            self._tabela.insert(
                "",
                "end",
                iid=dados["isbn"],
                values=(
                    dados["isbn"],
                    dados["titulo"],
                    dados["autor"],
                    dados["secao"],
                    TIPO_PARA_ROTULO[dados["tipo"]],
                    f"{livro.calcular_preco():.2f}",
                    dados["quantidade"],
                ),
            )

    def _montar_tabela(self) -> None:
        colunas = ("isbn", "titulo", "autor", "secao", "tipo", "preco", "quantidade")
        rotulos = {
            "isbn": "ISBN",
            "titulo": "Título",
            "autor": "Autor",
            "secao": "Seção",
            "tipo": "Tipo",
            "preco": "Preço (R$)",
            "quantidade": "Qtd.",
        }

        self._tabela = ttk.Treeview(self, columns=colunas, show="headings", selectmode="browse")
        for coluna in colunas:
            self._tabela.heading(coluna, text=rotulos[coluna])
            self._tabela.column(coluna, width=110, anchor="w")

        self._tabela.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        self._tabela.bind("<<TreeviewSelect>>", self._ao_selecionar_linha)

    def _montar_formulario(self) -> None:
        formulario = ttk.Frame(self, style="Cartao.TFrame", padding=16)
        formulario.grid(row=0, column=1, sticky="ns")

        ttk.Label(formulario, text="Cadastro de Livro", style="CartaoTitulo.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )

        self._var_isbn = tk.StringVar()
        self._var_titulo = tk.StringVar()
        self._var_autor = tk.StringVar()
        self._var_secao = tk.StringVar()
        self._var_preco = tk.StringVar()
        self._var_quantidade = tk.StringVar()
        self._var_tipo = tk.StringVar(value=TIPO_NOVO)
        self._var_estado = tk.StringVar(value=EstadoConservacao.BOM.name)
        self._var_raridade = tk.StringVar(value=GrauRaridade.INCOMUM.name)

        linha = self._criar_campo(formulario, 1, "ISBN", self._var_isbn)
        linha = self._criar_campo(formulario, linha, "Título", self._var_titulo)
        linha = self._criar_campo(formulario, linha, "Autor", self._var_autor)
        linha = self._criar_campo(formulario, linha, "Seção", self._var_secao)
        linha = self._criar_campo(formulario, linha, "Preço base (R$)", self._var_preco)
        linha = self._criar_campo(formulario, linha, "Quantidade", self._var_quantidade)

        ttk.Label(formulario, text="Tipo", style="Cartao.TLabel").grid(row=linha, column=0, sticky="w")
        combo_tipo = ttk.Combobox(
            formulario,
            textvariable=self._var_tipo,
            state="readonly",
            values=(TIPO_NOVO, TIPO_USADO, TIPO_RARO),
            width=22,
        )
        combo_tipo.grid(row=linha, column=1, sticky="we", pady=4)
        combo_tipo.bind("<<ComboboxSelected>>", lambda _evento: self._atualizar_campo_especifico())
        linha += 1

        self._frame_especifico = ttk.Frame(formulario, style="Cartao.TFrame")
        self._frame_especifico.grid(row=linha, column=0, columnspan=2, sticky="we")
        linha += 1

        botoes = ttk.Frame(formulario, style="Cartao.TFrame")
        botoes.grid(row=linha, column=0, columnspan=2, sticky="we", pady=(16, 0))
        ttk.Button(botoes, text="Novo", command=self._limpar_formulario).pack(
            side="left", expand=True, fill="x", padx=(0, 4)
        )
        ttk.Button(botoes, text="Salvar", command=self._salvar).pack(side="left", expand=True, fill="x", padx=4)
        ttk.Button(botoes, text="Excluir", command=self._excluir).pack(
            side="left", expand=True, fill="x", padx=(4, 0)
        )

        self._atualizar_campo_especifico()

    def _criar_campo(self, master: tk.Misc, linha: int, rotulo: str, variavel: tk.StringVar) -> int:
        ttk.Label(master, text=rotulo, style="Cartao.TLabel").grid(row=linha, column=0, sticky="w")
        ttk.Entry(master, textvariable=variavel, width=24).grid(row=linha, column=1, sticky="we", pady=4)
        return linha + 1

    def _atualizar_campo_especifico(self) -> None:
        for filho in self._frame_especifico.winfo_children():
            filho.destroy()

        tipo = self._var_tipo.get()
        if tipo == TIPO_USADO:
            ttk.Label(self._frame_especifico, text="Estado de conservação", style="Cartao.TLabel").grid(
                row=0, column=0, sticky="w"
            )
            ttk.Combobox(
                self._frame_especifico,
                textvariable=self._var_estado,
                state="readonly",
                values=tuple(estado.name for estado in EstadoConservacao),
                width=22,
            ).grid(row=0, column=1, sticky="we", pady=4)
        elif tipo == TIPO_RARO:
            ttk.Label(self._frame_especifico, text="Grau de raridade", style="Cartao.TLabel").grid(
                row=0, column=0, sticky="w"
            )
            ttk.Combobox(
                self._frame_especifico,
                textvariable=self._var_raridade,
                state="readonly",
                values=tuple(grau.name for grau in GrauRaridade),
                width=22,
            ).grid(row=0, column=1, sticky="we", pady=4)

    def _ao_selecionar_linha(self, _evento: tk.Event) -> None:
        selecionados = self._tabela.selection()
        if not selecionados:
            return
        livro = self._estoque.buscar_por_isbn(selecionados[0])
        if livro is not None:
            self._preencher_formulario(livro)

    def _preencher_formulario(self, livro: Livro) -> None:
        dados = livro.to_dict()
        self._isbn_em_edicao = dados["isbn"]

        self._var_isbn.set(dados["isbn"])
        self._var_titulo.set(dados["titulo"])
        self._var_autor.set(dados["autor"])
        self._var_secao.set(dados["secao"])
        self._var_preco.set(str(dados["preco_base"]))
        self._var_quantidade.set(str(dados["quantidade"]))
        self._var_tipo.set(TIPO_PARA_ROTULO[dados["tipo"]])

        if dados["tipo"] == "usado":
            self._var_estado.set(dados["estado_conservacao"])
        elif dados["tipo"] == "raro":
            self._var_raridade.set(dados["grau_raridade"])

        self._atualizar_campo_especifico()

    def _limpar_formulario(self) -> None:
        self._isbn_em_edicao = None
        for variavel in (
            self._var_isbn,
            self._var_titulo,
            self._var_autor,
            self._var_secao,
            self._var_preco,
            self._var_quantidade,
        ):
            variavel.set("")

        self._var_tipo.set(TIPO_NOVO)
        self._var_estado.set(EstadoConservacao.BOM.name)
        self._var_raridade.set(GrauRaridade.INCOMUM.name)
        self._atualizar_campo_especifico()

        for item in self._tabela.selection():
            self._tabela.selection_remove(item)

    def _coletar_dados_formulario(self) -> dict[str, Any]:
        dados: dict[str, Any] = {
            "isbn": self._var_isbn.get().strip(),
            "titulo": self._var_titulo.get().strip(),
            "autor": self._var_autor.get().strip(),
            "secao": self._var_secao.get().strip(),
            "preco_base": float(self._var_preco.get()),
            "quantidade": int(self._var_quantidade.get()),
            "tipo": ROTULO_PARA_TIPO[self._var_tipo.get()],
        }
        if dados["tipo"] == "usado":
            dados["estado_conservacao"] = self._var_estado.get()
        elif dados["tipo"] == "raro":
            dados["grau_raridade"] = self._var_raridade.get()
        return dados

    def _validar_campos_obrigatorios(self) -> str | None:
        campos = (
            self._var_isbn.get(),
            self._var_titulo.get(),
            self._var_autor.get(),
            self._var_secao.get(),
            self._var_preco.get(),
            self._var_quantidade.get(),
        )
        if any(not campo.strip() for campo in campos):
            return "Todos os campos são obrigatórios."
        return None

    @staticmethod
    def _validar_valores(dados: dict[str, Any]) -> str | None:
        if dados["preco_base"] <= 0:
            return "O preço base deve ser maior que zero."
        if dados["quantidade"] < 0:
            return "A quantidade não pode ser negativa."
        return None

    def _salvar(self) -> None:
        erro = self._validar_campos_obrigatorios()
        if erro is not None:
            messagebox.showerror("Dados inválidos", erro)
            return

        try:
            dados = self._coletar_dados_formulario()
        except ValueError:
            messagebox.showerror("Dados inválidos", "Preço base e quantidade devem ser numéricos.")
            return

        erro = self._validar_valores(dados)
        if erro is not None:
            messagebox.showerror("Dados inválidos", erro)
            return

        try:
            if self._estoque.buscar_por_isbn(dados["isbn"]) is None:
                self._estoque.adicionar_a_partir_de_dict(dados)
            else:
                self._estoque.atualizar_a_partir_de_dict(dados)
        except ValueError as erro:
            messagebox.showerror("Erro ao salvar", str(erro))
            return

        self._persistir()
        self._limpar_formulario()
        self.atualizar()

    def _excluir(self) -> None:
        if self._isbn_em_edicao is None:
            return
        self._estoque.remover(self._isbn_em_edicao)
        self._persistir()
        self._limpar_formulario()
        self.atualizar()