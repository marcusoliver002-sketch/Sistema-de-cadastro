import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


class Config:
    CORES = {
        "fundo": "#d9d9d9",
        "erro": "#8b0000",
        "sucesso": "#006400",
        "btn_azul": "#5b7cba",
        "btn_vermelho": "#d9534f",
        "btn_verde": "#28a745",
        "cabecalho": "#e1e1e1"
    }
    ARQUIVOS = {
        "usuarios": "usuarios.json",
        "produtos": "produtos.json"
    }


class GerenciadorDados:
    @staticmethod
    def carregar(arquivo):
        if not os.path.exists(arquivo):
            return []
        try:
            with open(arquivo, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def salvar(dados, arquivo):
        with open(arquivo, "w", encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)


class TelaLogin(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.usuarios = GerenciadorDados.carregar(Config.ARQUIVOS["usuarios"])
        self.criar_interface_login()

    def criar_interface_login(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Login de Usuário", font=(
            "Times New Roman", 18)).pack(pady=40)

        frm_form = tk.Frame(self)
        frm_form.pack()

        tk.Label(frm_form, text="Usuário:").grid(
            row=0, column=0, padx=5, pady=5)
        self.ent_usuario = tk.Entry(frm_form)
        self.ent_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_senha = tk.Entry(frm_form, show="*")
        self.ent_senha.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Entrar", command=self.fazer_login,
                  width=15, bg=Config.CORES["btn_azul"], fg="white").pack(pady=10)

        tk.Button(self, text="Criar Nova Conta", command=self.criar_interface_cadastro,
                  width=15, bg=Config.CORES["btn_verde"], fg="white").pack(pady=5)

    def criar_interface_cadastro(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Novo Usuário", font=(
            "Times New Roman", 18)).pack(pady=40)

        frm_form = tk.Frame(self)
        frm_form.pack()

        tk.Label(frm_form, text="Novo Usuário:").grid(row=0, column=0)
        self.ent_novo_user = tk.Entry(frm_form)
        self.ent_novo_user.grid(row=0, column=1, pady=5)

        tk.Label(frm_form, text="Senha:").grid(row=1, column=0)
        self.ent_nova_senha = tk.Entry(frm_form, show="*")
        self.ent_nova_senha.grid(row=1, column=1, pady=5)

        tk.Label(frm_form, text="Confirmar:").grid(row=2, column=0)
        self.ent_confirma = tk.Entry(frm_form, show="*")
        self.ent_confirma.grid(row=2, column=1, pady=5)

        frm_botoes = tk.Frame(self)
        frm_botoes.pack(pady=20)

        tk.Button(frm_botoes, text="Salvar", command=self.salvar_usuario,
                  bg=Config.CORES["btn_azul"], fg="white").pack(side=tk.LEFT, padx=5)

        tk.Button(frm_botoes, text="Voltar", command=self.criar_interface_login,
                  bg=Config.CORES["btn_vermelho"], fg="white").pack(side=tk.LEFT, padx=5)

    def fazer_login(self):
        user = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()

        for u in self.usuarios:
            if u['usuario'] == user and u['senha'] == senha:
                self.controller.mostrar_tela("TelaPrincipal")
                return

        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def salvar_usuario(self):
        user = self.ent_novo_user.get().strip()
        senha = self.ent_nova_senha.get().strip()
        confirma = self.ent_confirma.get().strip()

        if not user or not senha:
            messagebox.showerror("Erro", "Preencha tudo.")
            return
        if senha != confirma:
            messagebox.showerror("Erro", "Senhas não conferem.")
            return

        if any(u['usuario'] == user for u in self.usuarios):
            messagebox.showerror("Erro", "Usuário já existe.")
            return

        self.usuarios.append({"usuario": user, "senha": senha})
        GerenciadorDados.salvar(self.usuarios, Config.ARQUIVOS["usuarios"])
        messagebox.showinfo("Sucesso", "Usuário criado!")
        self.criar_interface_login()


class TelaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Config.CORES["fundo"])
        self.controller = controller
        self.produtos = []
        self.contador_id = 1

        self.criar_widgets()
        self.carregar_produtos()

    def carregar_produtos(self):
        self.produtos = GerenciadorDados.carregar(Config.ARQUIVOS["produtos"])
        if self.produtos:
            self.contador_id = max(p['id'] for p in self.produtos) + 1
        self.atualizar_tabela()

    def criar_widgets(self):
        frm_top = tk.Frame(self, bg=Config.CORES["fundo"], pady=20)
        frm_top.pack(fill="x")

        container_inputs = tk.Frame(frm_top, bg=Config.CORES["fundo"])
        container_inputs.pack(fill="x", padx=20)

        campos = [("Nome:", 1), ("Descrição:", 2),
                  ("Preço (R$):", 1), ("Validade:", 1), ("Qtd:", 1)]
        self.entradas = {}

        for i, (texto, peso) in enumerate(campos):
            container_inputs.grid_columnconfigure(i, weight=peso)

            lbl = tk.Label(container_inputs, text=texto,
                           bg=Config.CORES["fundo"], font=("Arial", 10))
            lbl.grid(row=0, column=i, sticky="w", padx=5)

            ent = tk.Entry(container_inputs, font=("Arial", 10))
            ent.grid(row=1, column=i, sticky="ew", padx=5, pady=(0, 5))

            chave = texto.replace(":", "").replace(" (R$)", "")
            self.entradas[chave] = ent

        self.entradas["Validade"].bind("<KeyRelease>", self.formatar_data)

        container_botoes = tk.Frame(frm_top, bg=Config.CORES["fundo"])
        container_botoes.pack(pady=15)

        tk.Button(container_botoes, text="Cadastrar", bg=Config.CORES["btn_azul"], fg="white", font=("Arial", 10, "bold"),
                  command=self.cadastrar, width=15).pack(side=tk.LEFT, padx=10)

        tk.Button(container_botoes, text="Limpar", bg=Config.CORES["btn_vermelho"], fg="white", font=("Arial", 10, "bold"),
                  command=self.limpar_campos, width=10).pack(side=tk.LEFT, padx=10)

        tk.Button(container_botoes, text="Apagar Tudo", bg=Config.CORES["btn_vermelho"], fg="white", font=("Arial", 10, "bold"),
                  command=self.apagar_tudo, width=12).pack(side=tk.LEFT, padx=10)

        tk.Button(container_botoes, text="Sair", command=lambda: self.controller.mostrar_tela("TelaLogin"),
                  width=10, font=("Arial", 10)).pack(side=tk.LEFT, padx=10)

        self.lbl_msg = tk.Label(
            frm_top, text="", bg=Config.CORES["fundo"], font=("Arial", 10, "bold"))
        self.lbl_msg.pack(pady=5)

        container_tabela = tk.Frame(self, bg=Config.CORES["fundo"])
        container_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        colunas = ("ID", "Nome", "Descrição", "Preço", "Validade", "Qtd")
        self.tree = ttk.Treeview(
            container_tabela, columns=colunas, show="headings")

        larguras = [50, 200, 350, 100, 100, 80]
        for col, larg in zip(colunas, larguras):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=larg, anchor="center")

        scrollbar = ttk.Scrollbar(
            container_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def formatar_data(self, event):
        if event.keysym.lower() == "backspace":
            return
        ent = self.entradas["Validade"]
        texto = ent.get()
        if len(texto) in (2, 5):
            ent.insert(tk.END, "/")
        elif len(texto) > 10:
            ent.delete(10, tk.END)

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for p in self.produtos:
            self.tree.insert("", "end", values=(
                p['id'], p['nome'], p['descricao'], p['preco'], p['validade'], p['quantidade']
            ))

    def limpar_campos(self):
        for ent in self.entradas.values():
            ent.delete(0, tk.END)
        self.entradas["Nome"].focus_set()

    def cadastrar(self):
        dados = {k: v.get().strip() for k, v in self.entradas.items()}

        if any(not v for v in dados.values()):
            self.msg("Preencha todos os campos", "erro")
            return

        try:
            preco = float(dados["Preço"].replace(",", "."))
            qtd = int(dados["Qtd"])

            data_validade = datetime.strptime(dados["Validade"], "%d/%m/%Y")
            if data_validade <= datetime.now():
                self.msg("Produto vencido ou data inválida", "erro")
                return

        except ValueError:
            self.msg("Erro nos valores numéricos ou data", "erro")
            return

        novo_prod = {
            "id": self.contador_id,
            "nome": dados["Nome"],
            "descricao": dados["Descrição"],
            "preco": f"R$ {preco:.2f}",
            "validade": dados["Validade"],
            "quantidade": qtd
        }

        self.produtos.append(novo_prod)
        self.contador_id += 1
        GerenciadorDados.salvar(self.produtos, Config.ARQUIVOS["produtos"])

        self.atualizar_tabela()
        self.limpar_campos()
        self.msg("Produto Cadastrado!", "sucesso")

    def apagar_tudo(self):
        if messagebox.askyesno("Confirmar", "Deseja apagar todos os produtos?"):
            self.produtos = []
            self.contador_id = 1
            GerenciadorDados.salvar(self.produtos, Config.ARQUIVOS["produtos"])
            self.atualizar_tabela()

    def msg(self, texto, tipo):
        cor = Config.CORES["sucesso"] if tipo == "sucesso" else Config.CORES["erro"]
        self.lbl_msg.config(text=texto, fg=cor)
        self.after(3000, lambda: self.lbl_msg.config(text=""))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Produtos OOP")
        self.geometry("1100x650")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (TelaLogin, TelaPrincipal):
            nome_classe = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[nome_classe] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.mostrar_tela("TelaLogin")

    def mostrar_tela(self, nome_tela):
        frame = self.frames[nome_tela]
        frame.tkraise()

        if nome_tela == "TelaPrincipal":
            frame.carregar_produtos()


if __name__ == "__main__":
    app = App()
    app.mainloop()
