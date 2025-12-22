import tkinter as tk
from tkinter import ttk
from datetime import datetime

cor_fundo = "#d9d9d9"
cor_texto_erro = "#8b0000"
cor_texto_sucesso = "#006400"
cor_botao = "#5b7cba"


class sistemaProdutos:
    def __init__(self):
        self.produtos = []
        self.contador_id = 1

        self.root = tk.Tk()
        self.root.title("Sistema de Produtos")
        self.root.geometry("800x600")

        self.frame_login = tk.Frame(self.root)
        self.frame_principal = tk.Frame(self.root, bg=cor_fundo)

        self.criar_tela_login()
        self.criar_tela_principal()

        self.frame_login.pack(fill="both", expand=True)
        self.root.mainloop()

    def criar_tela_login(self):
        lbl_title = tk.Label(
            self.frame_login, text="Login de Usuário", font=("TimesNewRoman", 18))
        lbl_title.pack(pady=40)

        frm_form = tk.Frame(self.frame_login)
        frm_form.pack()

        tk.Label(frm_form, text="Usuário:").grid(
            row=0, column=0, padx=5, pady=5)
        self.ent_usuario = tk.Entry(frm_form)
        self.ent_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_senha = tk.Entry(frm_form, show="*")
        self.ent_senha.grid(row=1, column=1, padx=5, pady=5)

        btn_entrar = tk.Button(self.frame_login, text="Entrar",
                               command=self.login, width=15, bg=cor_botao, fg="white")
        btn_entrar.pack(pady=20)

        self.lbl_msg_login = tk.Label(self.frame_login, text="", fg="red")
        self.lbl_msg_login.pack()

    def login(self):
        usuario = self.ent_usuario.get()
        senha = self.ent_senha.get()

        if usuario and senha:
            self.frame_login.pack_forget()
            self.frame_principal.pack(fill="both", expand=True)
        else:
            self.lbl_msg_login.config(
                text="Por favor, preencha todos os campos.")

    def criar_tela_principal(self):
        frame_top = tk.Frame(self.frame_principal,
                             bg=cor_fundo, pady=20, padx=20)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="Nome do Produto:",
                 bg=cor_fundo).grid(row=0, column=0, sticky="w")
        self.ent_nome = tk.Entry(frame_top, width=20)
        self.ent_nome.grid(row=1, column=0, padx=5)

        tk.Label(frame_top, text="Descrição:", bg=cor_fundo).grid(
            row=0, column=1, sticky="w")
        self.ent_descricao = tk.Entry(frame_top, width=30)
        self.ent_descricao.grid(row=1, column=1, padx=5)

        tk.Label(frame_top, text="Validade:", bg=cor_fundo).grid(
            row=0, column=2, sticky="w")
        self.ent_validade = tk.Entry(frame_top, width=15)
        self.ent_validade.insert(0, "DD/MM/AAAA")
        self.ent_validade.bind("<FocusIn>", lambda e: self.limpar_placeholder(
            self.ent_validade, "DD/MM/AAAA"))
        self.ent_validade.grid(row=1, column=2, padx=5)

        tk.Label(frame_top, text="Quantidade:", bg=cor_fundo).grid(
            row=0, column=3, sticky="w")
        self.ent_quantidade = tk.Entry(frame_top, width=10)
        self.ent_quantidade.grid(row=1, column=3, padx=5)

        btn_cadastrar = tk.Button(frame_top, text="Cadastrar", bg=cor_botao, fg="white",
                                  font=("TimesNewRoman", 10, "bold"), command=self.validar_e_cadastrar)
        btn_cadastrar.grid(row=2, column=1, pady=15, sticky="ew")

        self.lbl_mensagem = tk.Label(
            frame_top, text="", bg=cor_fundo, font=("TimesNewRoman", 10))
        self.lbl_mensagem.grid(
            row=3, column=0, columnspan=4, sticky="w", padx=5)

        frame_tabela = tk.Frame(self.frame_principal)
        frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        colunas = ("n", "nome", "descricao", "validade", "quantidade")
        self.tree = ttk.Treeview(
            frame_tabela, columns=colunas, show="headings")

        self.tree.heading("n", text="N°")
        self.tree.heading("nome", text="Nome do Produto")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("validade", text="Validade")
        self.tree.heading("quantidade", text="Quantidade")

        self.tree.column("n", width=50, anchor="center")
        self.tree.column("nome", width=150)
        self.tree.column("descricao", width=250)
        self.tree.column("validade", width=100, anchor="center")
        self.tree.column("quantidade", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

    def limpar_placeholder(self, widget, texto):
        if widget.get() == texto:
            widget.delete(0, tk.END)

    def mostrar_mensagem(self, mensagem, tipo):
        cor = cor_texto_sucesso if tipo == "sucesso" else cor_texto_erro
        self.lbl_mensagem.config(text=mensagem, fg=cor)
        self.root.after(3000, lambda: self.lbl_mensagem.config(text=""))

    def validar_e_cadastrar(self):
        nome = self.ent_nome.get().strip()
        descricao = self.ent_descricao.get().strip()
        validade_str = self.ent_validade.get().strip()
        quantidade_str = self.ent_quantidade.get().strip()

        erros = False

        if not nome or not descricao or not validade_str or not quantidade_str:
            erros = True

        if len(nome) < 3 or len(descricao) < 3:
            erros = True

        if not quantidade_str.isdigit() or int(quantidade_str) <= 0:
            erros = True

        try:
            data_validade = datetime.strptime(validade_str, "%d/%m/%Y")
            hoje = datetime.now()
            if data_validade <= hoje.replace(hour=0, minute=0, second=0, microsecond=0):
                erros = True
        except:
            erros = True

        if erros:
            self.mostrar_mensagem(
                "Campos inválidos. Corrija e tente novamente.", "erro")
        else:
            novo_produto = {
                "id": self.contador_id,
                "nome": nome,
                "descricao": descricao,
                "validade": validade_str,
                "quantidade": int(quantidade_str)
            }

            self.produtos.append(novo_produto)
            self.contador_id += 1

            self.atualizar_tabela()
            self.mostrar_mensagem("Produto cadastrado com sucesso!", "sucesso")
            self.limpar_campos()

    def limpar_campos(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_descricao.delete(0, tk.END)
        self.ent_validade.delete(0, tk.END)
        self.ent_validade.insert(0, "DD/MM/AAAA")
        self.ent_quantidade.delete(0, tk.END)

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for p in self.produtos:
            self.tree.insert("", "end", values=(
                p["id"], p["nome"], p["descricao"], p["validade"], p["quantidade"]))


if __name__ == "__main__":
    sistemaProdutos()
