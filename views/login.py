import tkinter as tk
import ttkbootstrap as tb
from tkinter import ttk, messagebox


class LoginView:
    """Interface de Login do Sistema"""

    def __init__(self, root, auth_model, callback_login_sucesso):
        self.root = root
        self.auth_model = auth_model
        self.callback_login_sucesso = callback_login_sucesso
        self.usuario_logado = None

    def criar_interface_login(self):
        """Cria a tela de login"""
        # Limpar widgets anteriores
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_principal = tb.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Logo/Título
        titulo = tb.Label(
            frame_principal,
            text="🔐 Sistema de Controle de Despesas",
            font=("Arial", 20, "bold"),
        )
        titulo.pack(pady=30)

        # Frame do formulário
        frame_form = ttk.LabelFrame(frame_principal, text="Login", padding=20)
        frame_form.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Username
        ttk.Label(frame_form, text="Usuário:", font=("Arial", 11)).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.entry_username = ttk.Combobox(frame_form, width=40, font=("Arial", 11))
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        self.entry_username.focus()

        # Preencher combobox com usuários existentes
        usuarios = self.auth_model.listar_usuarios()
        self.entry_username["values"] = usuarios

        # Password
        ttk.Label(frame_form, text="Senha:", font=("Arial", 11)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        self.entry_senha = ttk.Entry(frame_form, width=40, font=("Arial", 11), show="*")
        self.entry_senha.grid(row=1, column=1, padx=10, pady=10)

        # Bind Enter para login
        self.entry_username.bind("<Return>", lambda e: self.fazer_login())
        self.entry_senha.bind("<Return>", lambda e: self.fazer_login())

        # Frame de botões
        frame_botoes = ttk.Frame(frame_form)
        frame_botoes.grid(row=2, column=0, columnspan=2, pady=20)

        btn_login = tb.Button(
            frame_botoes,
            text="Login",
            command=self.fazer_login,
            bootstyle="success",
            width=15,
        )
        btn_login.pack(side=tk.LEFT, padx=5)

        btn_registrar = tb.Button(
            frame_botoes,
            text="Registrar Novo Usuário",
            command=self.mostrar_registro,
            bootstyle="info",
            width=20,
        )
        btn_registrar.pack(side=tk.LEFT, padx=5)

    def fazer_login(self):
        """Realiza o login do usuário"""
        username = self.entry_username.get().strip()
        senha = self.entry_senha.get()

        if not username or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
            return

        sucesso, resultado = self.auth_model.login(username, senha)

        if sucesso:
            self.usuario_logado = username
            messagebox.showinfo("Sucesso", f"Bem-vindo, {username}!")
            self.callback_login_sucesso(username)
        else:
            messagebox.showerror("Erro", resultado)
            self.entry_senha.delete(0, tk.END)
            self.entry_username.focus()

    def mostrar_registro(self):
        """Abre janela para registrar novo usuário"""
        janela = tk.Toplevel(self.root)
        janela.title("Registrar Novo Usuário")
        janela.geometry("500x400")
        janela.resizable(False, False)

        frame = ttk.Frame(janela, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Novo Usuário:", font=("Arial", 11, "bold")).pack(
            anchor=tk.W, pady=(0, 5)
        )
        entry_novo_user = ttk.Entry(frame, width=40, font=("Arial", 11))
        entry_novo_user.pack(anchor=tk.W, pady=(0, 15), fill=tk.X)

        ttk.Label(frame, text="Senha:", font=("Arial", 11, "bold")).pack(
            anchor=tk.W, pady=(0, 5)
        )
        entry_nova_senha = ttk.Entry(frame, width=40, font=("Arial", 11), show="*")
        entry_nova_senha.pack(anchor=tk.W, pady=(0, 15), fill=tk.X)

        ttk.Label(frame, text="Confirmar Senha:", font=("Arial", 11, "bold")).pack(
            anchor=tk.W, pady=(0, 5)
        )
        entry_confirmar_senha = ttk.Entry(frame, width=40, font=("Arial", 11), show="*")
        entry_confirmar_senha.pack(anchor=tk.W, pady=(0, 25), fill=tk.X)

        def registrar():
            novo_user = entry_novo_user.get().strip()
            nova_senha = entry_nova_senha.get()
            confirmar_senha = entry_confirmar_senha.get()

            if not novo_user or not nova_senha:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return

            if len(nova_senha) < 4:
                messagebox.showwarning(
                    "Atenção", "Senha deve ter no mínimo 4 caracteres!"
                )
                return

            if nova_senha != confirmar_senha:
                messagebox.showerror("Erro", "As senhas não correspondem!")
                return

            sucesso, mensagem = self.auth_model.criar_usuario(novo_user, nova_senha)

            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                janela.destroy()
                self.criar_interface_login()
            else:
                messagebox.showerror("Erro", mensagem)

        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(fill=tk.X, pady=(10, 0))

        btn_cancelar = tb.Button(
            frame_botoes,
            text="Cancelar",
            command=janela.destroy,
            bootstyle="secondary",
            width=15,
        )
        btn_cancelar.pack(side=tk.LEFT, padx=5)

        btn_registrar = tb.Button(
            frame_botoes,
            text="Registrar",
            command=registrar,
            bootstyle="success",
            width=15,
        )
        btn_registrar.pack(side=tk.LEFT, padx=5)

    def obter_usuario_logado(self):
        """Retorna o usuário logado atualmente"""
        return self.usuario_logado
