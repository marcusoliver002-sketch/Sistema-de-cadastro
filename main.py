import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

COR_FUNDO = "#d9d9d9"
COR_TEXTO_ERRO = "#8b0000"
COR_TEXTO_SUCESSO = "#006400"
COR_BOTAO_AZUL = "#5b7cba"
COR_BOTAO_VERMELHO = "#d9534f"
COR_BOTAO_VERDE = "#28a745"
COR_CABECALHO = "#e1e1e1"

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_PRODUTOS = "produtos.json"

class SistemaProdutos:
    def __init__(self):
        self.usuarios = self.carregar_dados(ARQUIVO_USUARIOS)
        self.produtos = self.carregar_dados(ARQUIVO_PRODUTOS)
        
        if self.produtos:
            self.contador_id = max(p['id'] for p in self.produtos) + 1
        else:
            self.contador_id = 1

        self.root = tk.Tk()
        self.root.title("Sistema de Produtos")
        self.root.geometry("1100x650")

        self.frame_login = tk.Frame(self.root)
        self.frame_cadastro_usuario = tk.Frame(self.root)
        self.frame_principal = tk.Frame(self.root, bg=COR_FUNDO)

        self.criar_tela_login()
        self.criar_tela_cadastro_usuario()
        self.criar_tela_principal()

        self.frame_login.pack(fill="both", expand=True)
        self.root.mainloop()

    def carregar_dados(self, arquivo):
        if not os.path.exists(arquivo):
            return []
        try:
            with open(arquivo, "r") as f:
                return json.load(f)
        except:
            return []

    def salvar_dados(self, dados, arquivo):
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)

    def criar_tela_login(self):
        for widget in self.frame_login.winfo_children():
            widget.destroy()

        lbl_title = tk.Label(
            self.frame_login, text="Login de Usuário", font=("Times New Roman", 18))
        lbl_title.pack(pady=40)

        frm_form = tk.Frame(self.frame_login)
        frm_form.pack()

        tk.Label(frm_form, text="Usuário:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_login_usuario = tk.Entry(frm_form)
        self.ent_login_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_login_senha = tk.Entry(frm_form, show="*")
        self.ent_login_senha.grid(row=1, column=1, padx=5, pady=5)

        btn_entrar = tk.Button(self.frame_login, text="Entrar",
                               command=self.fazer_login, width=15, bg=COR_BOTAO_AZUL, fg="white")
        btn_entrar.pack(pady=10)

        btn_criar_conta = tk.Button(self.frame_login, text="Criar Nova Conta",
                                    command=self.exibir_tela_cadastro, width=15, bg=COR_BOTAO_VERDE, fg="white")
        btn_criar_conta.pack(pady=5)

        self.lbl_msg_login = tk.Label(self.frame_login, text="", fg="red")
        self.lbl_msg_login.pack(pady=5)

    def criar_tela_cadastro_usuario(self):
        lbl_title = tk.Label(
            self.frame_cadastro_usuario, text="Novo Usuário", font=("Times New Roman", 18))
        lbl_title.pack(pady=40)

        frm_form = tk.Frame(self.frame_cadastro_usuario)
        frm_form.pack()

        tk.Label(frm_form, text="Novo Usuário:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_novo_usuario = tk.Entry(frm_form)
        self.ent_novo_usuario.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_nova_senha = tk.Entry(frm_form, show="*")
        self.ent_nova_senha.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frm_form, text="Confirmar Senha:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_confirma_senha = tk.Entry(frm_form, show="*")
        self.ent_confirma_senha.grid(row=2, column=1, padx=5, pady=5)

        frame_botoes = tk.Frame(self.frame_cadastro_usuario)
        frame_botoes.pack(pady=20)

        btn_salvar = tk.Button(frame_botoes, text="Salvar",
                               command=self.salvar_novo_usuario, width=10, bg=COR_BOTAO_AZUL, fg="white")
        btn_salvar.pack(side=tk.LEFT, padx=5)

        btn_voltar = tk.Button(frame_botoes, text="Voltar",
                               command=self.voltar_login, width=10, bg=COR_BOTAO_VERMELHO, fg="white")
        btn_voltar.pack(side=tk.LEFT, padx=5)

    def exibir_tela_cadastro(self):
        self.frame_login.pack_forget()
        self.frame_cadastro_usuario.pack(fill="both", expand=True)

    def voltar_login(self):
        self.frame_cadastro_usuario.pack_forget()
        self.frame_login.pack(fill="both", expand=True)

    def salvar_novo_usuario(self):
        user = self.ent_novo_usuario.get().strip()
        senha = self.ent_nova_senha.get().strip()
        confirma = self.ent_confirma_senha.get().strip()

        if not user or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if senha != confirma:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        for u in self.usuarios:
            if u['usuario'] == user:
                messagebox.showerror("Erro", "Usuário já existe.")
                return

        self.usuarios.append({"usuario": user, "senha": senha})
        self.salvar_dados(self.usuarios, ARQUIVO_USUARIOS)
        
        messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
        self.ent_novo_usuario.delete(0, tk.END)
        self.ent_nova_senha.delete(0, tk.END)
        self.ent_confirma_senha.delete(0, tk.END)
        self.voltar_login()

    def fazer_login(self):
        usuario_digitado = self.ent_login_usuario.get().strip()
        senha_digitada = self.ent_login_senha.get().strip()

        login_sucesso = False
        for u in self.usuarios:
            if u['usuario'] == usuario_digitado and u['senha'] == senha_digitada:
                login_sucesso = True
                break

        if login_sucesso:
            self.frame_login.pack_forget()
            self.frame_principal.pack(fill="both", expand=True)
            self.atualizar_tabela() 
        else:
            self.lbl_msg_login.config(text="Usuário ou senha incorretos.")

    def criar_tela_principal(self):
        frame_top = tk.Frame(self.frame_principal, bg=COR_FUNDO, pady=20, padx=20)
        frame_top.pack(fill="x")

        tk.Label(frame_top, text="Nome:", bg=COR_FUNDO).grid(row=0, column=0, sticky="w")
        self.ent_nome = tk.Entry(frame_top, width=15)
        self.ent_nome.grid(row=1, column=0, padx=5)

        tk.Label(frame_top, text="Descrição:", bg=COR_FUNDO).grid(row=0, column=1, sticky="w")
        self.ent_descricao = tk.Entry(frame_top, width=25)
        self.ent_descricao.grid(row=1, column=1, padx=5)

        tk.Label(frame_top, text="Preço (R$):", bg=COR_FUNDO).grid(row=0, column=2, sticky="w")
        self.ent_preco = tk.Entry(frame_top, width=10)
        self.ent_preco.grid(row=1, column=2, padx=5)

        tk.Label(frame_top, text="Validade:", bg=COR_FUNDO).grid(row=0, column=3, sticky="w")
        self.ent_validade = tk.Entry(frame_top, width=12)
        self.ent_validade.grid(row=1, column=3, padx=5)
        self.ent_validade.bind("<KeyRelease>", self.formatar_data) 

        tk.Label(frame_top, text="Qtd:", bg=COR_FUNDO).grid(row=0, column=4, sticky="w")
        self.ent_quantidade = tk.Entry(frame_top, width=8)
        self.ent_quantidade.grid(row=1, column=4, padx=5)
        
        frame_botoes = tk.Frame(frame_top, bg=COR_FUNDO)
        frame_botoes.grid(row=2, column=0, columnspan=5, pady=15, sticky="ew")

        btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", bg=COR_BOTAO_AZUL, fg="white",
                                  font=("Times New Roman", 10, "bold"), command=self.validar_e_cadastrar)
        btn_cadastrar.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

        btn_limpar = tk.Button(frame_botoes, text="Limpar", bg=COR_BOTAO_VERMELHO, fg="white",
                               font=("Times New Roman", 10, "bold"), command=self.limpar_campos_formulario)
        btn_limpar.pack(side=tk.LEFT, padx=5)

        btn_apagar_tudo = tk.Button(frame_botoes, text="Apagar Tudo", bg=COR_BOTAO_VERMELHO, fg="white",
                                    font=("Times New Roman", 10, "bold"), command=self.apagar_tudo)
        btn_apagar_tudo.pack(side=tk.LEFT, padx=5)

        self.lbl_mensagem = tk.Label(frame_top, text="", bg=COR_FUNDO, font=("Times New Roman", 10))
        self.lbl_mensagem.grid(row=3, column=0, columnspan=5, sticky="w", padx=5)

        container = tk.Frame(self.frame_principal, bg="gray", bd=1)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas_tabela = tk.Canvas(container, bg="white")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas_tabela.yview)
        
        self.frame_grade = tk.Frame(self.canvas_tabela, bg="white")

        self.frame_grade.bind("<Configure>", 
            lambda e: self.canvas_tabela.configure(scrollregion=self.canvas_tabela.bbox("all")))

        self.canvas_tabela.create_window((0, 0), window=self.frame_grade, anchor="nw")
        self.canvas_tabela.configure(yscrollcommand=scrollbar.set)

        self.canvas_tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def formatar_data(self, event):
        if event.keysym.lower() == "backspace": return
        texto = self.ent_validade.get()
        if len(texto) == 2 or len(texto) == 5:
            self.ent_validade.insert(tk.END, "/")
        if len(texto) > 10:
            self.ent_validade.delete(10, tk.END)

    def mostrar_mensagem(self, mensagem, tipo):
        cor = COR_TEXTO_SUCESSO if tipo == "sucesso" else COR_TEXTO_ERRO
        self.lbl_mensagem.config(text=mensagem, fg=cor)
        self.root.after(3000, lambda: self.lbl_mensagem.config(text=""))

    def validar_nome_unico(self, nome):
        for produto in self.produtos:
            if produto['nome'].lower() == nome.lower():
                return False
        return True

    def validar_e_cadastrar(self):
        nome = self.ent_nome.get().strip()
        descricao = self.ent_descricao.get().strip()
        preco_str = self.ent_preco.get().strip().replace(",", ".")
        validade_str = self.ent_validade.get().strip()
        quantidade_str = self.ent_quantidade.get().strip()

        if not nome or not descricao or not preco_str or not validade_str or not quantidade_str:
            self.mostrar_mensagem("Preencha todos os campos.", "erro")
            return

        if len(nome) < 3:
            self.mostrar_mensagem("Nome deve ter min. 3 caracteres.", "erro")
            return

        if not self.validar_nome_unico(nome):
            self.mostrar_mensagem(f"Erro: O produto '{nome}' já existe.", "erro")
            return
        
        try:
            preco = float(preco_str)
            if preco <= 0: raise ValueError
        except ValueError:
            self.mostrar_mensagem("Preço inválido.", "erro")
            return

        if not quantidade_str.isdigit() or int(quantidade_str) <= 0:
            self.mostrar_mensagem("Quantidade inválida.", "erro")
            return

        try:
            data_validade = datetime.strptime(validade_str, "%d/%m/%Y")
            hoje = datetime.now()
            if data_validade <= hoje.replace(hour=0, minute=0, second=0, microsecond=0):
                self.mostrar_mensagem("Data vencida.", "erro")
                return
        except ValueError:
            self.mostrar_mensagem("Data inválida.", "erro")
            return

        self.cadastrar_produto(nome, descricao, preco, validade_str, quantidade_str)

    def cadastrar_produto(self, nome, descricao, preco, validade, quantidade):
        novo_produto = {
            "id": self.contador_id,
            "nome": nome,
            "descricao": descricao,
            "preco": f"R$ {preco:.2f}",
            "validade": validade,
            "quantidade": int(quantidade)
        }

        self.produtos.append(novo_produto)
        self.contador_id += 1
        self.salvar_dados(self.produtos, ARQUIVO_PRODUTOS)

        self.atualizar_tabela()
        self.mostrar_mensagem("Sucesso!", "sucesso")
        self.limpar_campos_formulario()
    
    def apagar_tudo(self):
        resposta = messagebox.askyesno(
            "Confirmação",
            "Tem certeza que deseja apagar TODOS os produtos?"
        )

        if not resposta:
            return

        self.produtos.clear()
        self.contador_id = 1
        self.salvar_dados(self.produtos, ARQUIVO_PRODUTOS)
        self.atualizar_tabela()

        self.mostrar_mensagem("Todos os produtos foram apagados.", "sucesso")

    def limpar_campos_formulario(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_descricao.delete(0, tk.END)
        self.ent_preco.delete(0, tk.END)
        self.ent_validade.delete(0, tk.END)
        self.ent_quantidade.delete(0, tk.END)
        self.ent_nome.focus_set()

    def atualizar_tabela(self):
        for widget in self.frame_grade.winfo_children():
            widget.destroy()

        config_colunas = [
            ("ID", 5), 
            ("Nome", 25), 
            ("Descrição", 45), 
            ("Preço", 15), 
            ("Validade", 15), 
            ("Qtd.", 8)
        ]

        for col, (titulo, largura) in enumerate(config_colunas):
            lbl = tk.Label(self.frame_grade, text=titulo, width=largura, 
                           bg=COR_CABECALHO, font=("Arial", 10, "bold"),
                           relief="solid", borderwidth=1)
            lbl.grid(row=0, column=col, sticky="nsew")

        for i, p in enumerate(self.produtos):
            linha = i + 1
            valores = [p['id'], p['nome'], p['descricao'], p['preco'], p['validade'], p['quantidade']]
            
            for col, valor in enumerate(valores):
                largura = config_colunas[col][1]
                
                alinhamento = "center"
                if col == 1 or col == 2:
                    alinhamento = "w"

                lbl = tk.Label(self.frame_grade, text=valor, width=largura, 
                               bg="white", anchor=alinhamento,
                               relief="solid", borderwidth=1)
                lbl.grid(row=linha, column=col, sticky="nsew")

if __name__ == "__main__":
    SistemaProdutos()