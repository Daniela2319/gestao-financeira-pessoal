import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from datetime import datetime

from ttkbootstrap.scrolled import ScrolledFrame

from views.dashboard import Dashboard
from views.graficos import Graficos
from views.exportador_excel import ExportadorExcel
from views.exportador_pdf import ExportadorPDF
from views.login import LoginView
from auth import AuthModel


class App(tb.Window):

    def __init__(self):

        super().__init__(themename="darkly")

        self.title("Sistema Financeiro")
        self.geometry("1400x800")
        self.resizable(True, True)

        # Inicializar autenticação
        self.auth_model = AuthModel()
        self.usuario_logado = None

        # Se não houver usuário, mostrar tela de login
        if not self.auth_model.usuario_existe():
            self.mostrar_configuracao_inicial()
        else:
            self.mostrar_login()

    def mostrar_configuracao_inicial(self):
        """Mostra tela para criar o primeiro usuário"""
        # Limpar tela
        for widget in self.winfo_children():
            widget.destroy()

        login_view = LoginView(self, self.auth_model, self.ao_fazer_login)
        login_view.criar_interface_login()

    def mostrar_login(self):
        """Mostra tela de login"""
        # Limpar tela
        for widget in self.winfo_children():
            widget.destroy()

        login_view = LoginView(self, self.auth_model, self.ao_fazer_login)
        login_view.criar_interface_login()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def ao_fazer_login(self, username):
        """Callback executado após login bem-sucedido"""
        self.usuario_logado = username
        self.limpar_tela()
        self.criar_interface()

    def criar_interface(self):
        # Frame principal com sidebar
        frame_principal = ttk.Frame(self)
        frame_principal.pack(fill=BOTH, expand=True)

        # SIDEBAR (Menu Lateral)
        self.sidebar = ttk.Frame(frame_principal, width=250)
        self.sidebar.pack(side=LEFT, fill=Y, padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        # Usuário logado
        lbl_usuario = ttk.Label(
            self.sidebar, text=f"👤 {self.usuario_logado}", font=("Arial", 10, "bold")
        )
        lbl_usuario.pack(pady=10, padx=15)

        ttk.Separator(self.sidebar, orient=HORIZONTAL).pack(fill=X, padx=15, pady=5)

        # Título do Sidebar
        lbl_titulo = ttk.Label(
            self.sidebar, text="FINANCEIRO", font=("Arial", 18, "bold")
        )
        lbl_titulo.pack(pady=20, padx=15)

        # Separador
        ttk.Separator(self.sidebar, orient=HORIZONTAL).pack(fill=X, padx=15, pady=5)

        # Botões de Navegação
        self.btn_dashboard = ttk.Button(
            self.sidebar, text="📊 Dashboard", command=self.mostrar_dashboard
        )
        self.btn_dashboard.pack(fill=X, padx=10, pady=10)

        self.btn_graficos = ttk.Button(
            self.sidebar, text="📈 Gráficos", command=self.mostrar_graficos
        )
        self.btn_graficos.pack(fill=X, padx=10, pady=10)

        self.btn_exportar = ttk.Button(
            self.sidebar, text="📥 Exportar", command=self.mostrar_exportar
        )
        self.btn_exportar.pack(fill=X, padx=10, pady=10)

        # Espaço vazio
        ttk.Label(self.sidebar, text="").pack(expand=True)

        # Botões inferiores
        ttk.Separator(self.sidebar, orient=HORIZONTAL).pack(fill=X, padx=15, pady=5)

        btn_logout = ttk.Button(
            self.sidebar, text="🔓 Logout", command=self.fazer_logout
        )
        btn_logout.pack(fill=X, padx=10, pady=5)

        btn_sair = ttk.Button(self.sidebar, text="❌ Sair", command=self.quit)
        btn_sair.pack(fill=X, padx=10, pady=5)

        # Frame de Conteúdo
        self.frame_conteudo = ScrolledFrame(frame_principal, autohide=False)

        self.frame_conteudo.pack(side=RIGHT, fill=BOTH, expand=True)

        # Iniciar com o Dashboard
        self.mostrar_dashboard()

    def limpar_conteudo(self):

        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):

        self.limpar_conteudo()
        self.dashboard = Dashboard(self.frame_conteudo)
        self.dashboard.pack(fill=BOTH, expand=True)

    def mostrar_graficos(self):

        self.limpar_conteudo()
        self.graficos = Graficos(self.frame_conteudo)
        self.graficos.pack(fill=BOTH, expand=True)

    def mostrar_exportar(self):

        self.limpar_conteudo()
        frame_exportar = ttk.Frame(self.frame_conteudo)
        frame_exportar.pack(fill=BOTH, expand=True)

        titulo = ttk.Label(
            frame_exportar, text="Exportar Dados", font=("Arial", 20, "bold")
        )
        titulo.pack(pady=20)

        frame_opcoes = ttk.LabelFrame(frame_exportar, text="Escolha o formato")
        frame_opcoes.pack(padx=20, pady=20, fill=X)

        btn_excel = ttk.Button(
            frame_opcoes, text="📊 Exportar para Excel", command=self.exportar_excel
        )
        btn_excel.pack(pady=10, padx=20)

        btn_pdf = ttk.Button(
            frame_opcoes, text="📄 Exportar para PDF", command=self.exportar_pdf
        )
        btn_pdf.pack(pady=10, padx=20)

    def exportar_excel(self):

        caminho = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"relatorio_financeiro_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
        )

        if caminho:
            try:
                exportador = ExportadorExcel()
                exportador.exportar(caminho)
                messagebox.showinfo(
                    "Sucesso", f"Arquivo Excel exportado com sucesso!\n{caminho}"
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")

    def exportar_pdf(self):

        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"relatorio_financeiro_{datetime.now().strftime('%d_%m_%Y')}.pdf",
        )

        if caminho:
            try:
                exportador = ExportadorPDF()
                exportador.exportar(caminho)
                messagebox.showinfo(
                    "Sucesso", f"Arquivo PDF exportado com sucesso!\n{caminho}"
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")

    def fazer_logout(self):
        """Realiza logout do usuário"""
        resposta = messagebox.askyesno("Confirmar", "Deseja realmente fazer logout?")
        if resposta:
            self.usuario_logado = None
            self.mostrar_login()


if __name__ == "__main__":

    app = App()
    app.mainloop()
