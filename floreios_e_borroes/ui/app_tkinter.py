import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk
from typing import Any

from dominio.item_acervo import Livro
from dominio.livro_raro import GrauRaridade
from dominio.livro_usado import EstadoConservacao
from servicos.catalogo import Catalogo
from servicos.estoque import Estoque

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
    def __init__(self, catalogo: Catalogo, estoque: Estoque, persistir: Callable[[], None]) -> None:
        super().__init__()
        self.title("Floreios e Borrões")
        self.geometry("1024x640")
        self.configure(background=COR_FUNDO)

        self._configurar_estilo()
        self._montar_navegacao()

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self._telas: dict[str, ttk.Frame] = {
            "cliente": TelaCliente(container, catalogo),
            "admin": TelaAdministrador(container, estoque, persistir),
        }
        for tela in self._telas.values():
            tela.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela("cliente")

    def mostrar_tela(self, nome: str) -> None:
        tela = self._telas[nome]
        tela.tkraise()
        tela.atualizar()

    def _montar_navegacao(self) -> None:
        barra = ttk.Frame(self, style="Navegacao.TFrame", padding=(16, 10))
        barra.pack(fill="x")

        ttk.Label(barra, text="Floreios e Borrões", style="Titulo.TLabel").pack(side="left")
        ttk.Button(barra, text="Administração", command=lambda: self.mostrar_tela("admin")).pack(
            side="right", padx=(8, 0)
        )
        ttk.Button(barra, text="Catálogo", command=lambda: self.mostrar_tela("cliente")).pack(side="right")

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


class TelaCliente(ttk.Frame):
    def __init__(self, master: tk.Misc, catalogo: Catalogo) -> None:
        super().__init__(master, padding=16)
        self._catalogo = catalogo

        self._termo = tk.StringVar()
        self._secao = tk.StringVar(value=SECAO_TODAS)
        self._estado = tk.StringVar(value=ESTADO_TODOS)

        self._montar_filtros()
        self._montar_lista()

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

    def _montar_lista(self) -> None:
        moldura = ttk.Frame(self)
        moldura.pack(fill="both", expand=True)

        canvas = tk.Canvas(moldura, background=COR_FUNDO, highlightthickness=0)
        rolagem = ttk.Scrollbar(moldura, orient="vertical", command=canvas.yview)
        self._lista = ttk.Frame(canvas)

        self._lista.bind("<Configure>", lambda _evento: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self._lista, anchor="nw")
        canvas.configure(yscrollcommand=rolagem.set)

        canvas.pack(side="left", fill="both", expand=True)
        rolagem.pack(side="right", fill="y")

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
