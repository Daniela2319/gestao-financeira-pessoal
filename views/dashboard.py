import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime

from models.receitas import ReceitaModel
from models.despesas import DespesaModel


class Dashboard(tb.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.receita_model = ReceitaModel()
        self.despesa_model = DespesaModel()

        ## self.pack(fill=BOTH, expand=True)

        self.criar_interface()

    def criar_interface(self):

        titulo = tb.Label(self, text="Dashboard Financeiro", font=("Arial", 24, "bold"))
        titulo.pack(pady=20)

        self.frame_cards = tb.Frame(self)
        self.frame_cards.pack(fill=X, padx=20)

        self.card_receitas = tb.LabelFrame(self.frame_cards, text="Receitas")
        self.card_receitas.pack(side=LEFT, padx=10, fill=BOTH, expand=True)

        self.lbl_receitas = tb.Label(
            self.card_receitas, text="R$ 0,00", font=("Arial", 20, "bold")
        )
        self.lbl_receitas.pack(pady=20)

        self.card_despesas = tb.LabelFrame(self.frame_cards, text="Despesas")
        self.card_despesas.pack(side=LEFT, padx=10, fill=BOTH, expand=True)

        self.lbl_despesas = tb.Label(
            self.card_despesas, text="R$ 0,00", font=("Arial", 20, "bold")
        )
        self.lbl_despesas.pack(pady=20)

        self.card_saldo = tb.LabelFrame(self.frame_cards, text="Saldo")
        self.card_saldo.pack(side=LEFT, padx=10, fill=BOTH, expand=True)

        self.lbl_saldo = tb.Label(
            self.card_saldo, text="R$ 0,00", font=("Arial", 20, "bold")
        )
        self.lbl_saldo.pack(pady=20)

        # Notebook para abas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Aba Receitas
        self.criar_aba_receitas()

        # Aba Despesas
        self.criar_aba_despesas()

        self.atualizar_dashboard()

    def criar_aba_receitas(self):

        frame_receitas = ttk.Frame(self.notebook)
        self.notebook.add(frame_receitas, text="Receitas")

        # Formulário
        frame_form = ttk.LabelFrame(frame_receitas, text="Adicionar Receita")
        frame_form.pack(fill=X, padx=10, pady=10)

        ttk.Label(frame_form, text="Nome:").grid(
            row=0, column=0, sticky=W, padx=5, pady=5
        )
        self.entry_nome_receita = ttk.Entry(frame_form, width=30)
        self.entry_nome_receita.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Valor:").grid(
            row=1, column=0, sticky=W, padx=5, pady=5
        )
        self.entry_valor_receita = ttk.Entry(frame_form, width=30)
        self.entry_valor_receita.grid(row=1, column=1, padx=5, pady=5)

        btn_salvar_receita = ttk.Button(
            frame_form, text="Salvar", command=self.salvar_receita
        )
        btn_salvar_receita.grid(row=2, column=1, sticky=E, padx=5, pady=10)

        # Treeview
        frame_tree = ttk.Frame(frame_receitas)
        frame_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        ttk.Label(
            frame_tree, text="Receitas Registradas", font=("Arial", 12, "bold")
        ).pack(fill=X, pady=5)

        self.tree_receitas = ttk.Treeview(
            frame_tree, columns=("ID", "Nome", "Valor"), height=10, show="tree headings"
        )

        self.tree_receitas.column("#0", width=0, stretch=tk.NO)
        self.tree_receitas.column("ID", anchor=CENTER, width=50)
        self.tree_receitas.column("Nome", anchor=W, width=200)
        self.tree_receitas.column("Valor", anchor=E, width=100)

        self.tree_receitas.heading("#0", text="", anchor=W)
        self.tree_receitas.heading("ID", text="ID", anchor=CENTER)
        self.tree_receitas.heading("Nome", text="Nome", anchor=W)
        self.tree_receitas.heading("Valor", text="Valor", anchor=E)

        self.tree_receitas.pack(fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            frame_tree, orient=VERTICAL, command=self.tree_receitas.yview
        )
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree_receitas.configure(yscrollcommand=scrollbar.set)

        # Botões de ação
        frame_btn = ttk.Frame(frame_receitas)
        frame_btn.pack(fill=X, padx=10, pady=10)

        btn_editar_receita = ttk.Button(
            frame_btn, text="Editar", command=self.editar_receita
        )
        btn_editar_receita.pack(side=LEFT, padx=5)

        btn_excluir_receita = ttk.Button(
            frame_btn, text="Excluir", command=self.excluir_receita
        )
        btn_excluir_receita.pack(side=LEFT, padx=5)

        btn_atualizar_receita = ttk.Button(
            frame_btn, text="Atualizar", command=self.atualizar_receitas
        )
        btn_atualizar_receita.pack(side=LEFT, padx=5)

        self.atualizar_receitas()

    def criar_aba_despesas(self):

        frame_despesas = ttk.Frame(self.notebook)
        self.notebook.add(frame_despesas, text="Despesas")

        # Formulário
        frame_form = ttk.LabelFrame(frame_despesas, text="Adicionar Despesa")
        frame_form.pack(fill=X, padx=10, pady=10)

        ttk.Label(frame_form, text="Data:").grid(
            row=0, column=0, sticky=W, padx=5, pady=5
        )
        self.entry_data_despesa = ttk.Entry(frame_form, width=15)
        self.entry_data_despesa.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data_despesa.grid(row=0, column=1, sticky=W, padx=5, pady=5)

        ttk.Label(frame_form, text="Mês:").grid(
            row=0, column=2, sticky=W, padx=5, pady=5
        )
        self.entry_mes_despesa = ttk.Entry(frame_form, width=15)
        self.entry_mes_despesa.insert(0, datetime.now().strftime("%m/%Y"))
        self.entry_mes_despesa.grid(row=0, column=3, sticky=W, padx=5, pady=5)

        ttk.Label(frame_form, text="Nome:").grid(
            row=1, column=0, sticky=W, padx=5, pady=5
        )
        self.entry_nome_despesa = ttk.Entry(frame_form, width=30)
        self.entry_nome_despesa.grid(
            row=1, column=1, columnspan=3, sticky=EW, padx=5, pady=5
        )

        ttk.Label(frame_form, text="Valor:").grid(
            row=2, column=0, sticky=W, padx=5, pady=5
        )
        self.entry_valor_despesa = ttk.Entry(frame_form, width=30)
        self.entry_valor_despesa.grid(
            row=2, column=1, columnspan=3, sticky=EW, padx=5, pady=5
        )

        btn_salvar_despesa = ttk.Button(
            frame_form, text="Salvar", command=self.salvar_despesa
        )
        btn_salvar_despesa.grid(row=3, column=3, sticky=E, padx=5, pady=10)

        # Treeview
        frame_tree = ttk.Frame(frame_despesas)
        frame_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        ttk.Label(
            frame_tree, text="Despesas Registradas", font=("Arial", 12, "bold")
        ).pack(fill=X, pady=5)

        self.tree_despesas = ttk.Treeview(
            frame_tree,
            columns=("ID", "Data", "Mês", "Nome", "Valor"),
            height=10,
            show="tree headings",
        )

        self.tree_despesas.column("#0", width=0, stretch=tk.NO)
        self.tree_despesas.column("ID", anchor=CENTER, width=50)
        self.tree_despesas.column("Data", anchor=CENTER, width=80)
        self.tree_despesas.column("Mês", anchor=CENTER, width=80)
        self.tree_despesas.column("Nome", anchor=W, width=150)
        self.tree_despesas.column("Valor", anchor=E, width=100)

        self.tree_despesas.heading("#0", text="", anchor=W)
        self.tree_despesas.heading("ID", text="ID", anchor=CENTER)
        self.tree_despesas.heading("Data", text="Data", anchor=CENTER)
        self.tree_despesas.heading("Mês", text="Mês", anchor=CENTER)
        self.tree_despesas.heading("Nome", text="Nome", anchor=W)
        self.tree_despesas.heading("Valor", text="Valor", anchor=E)

        self.tree_despesas.pack(fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            frame_tree, orient=VERTICAL, command=self.tree_despesas.yview
        )
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree_despesas.configure(yscrollcommand=scrollbar.set)

        # Botões de ação
        frame_btn = ttk.Frame(frame_despesas)
        frame_btn.pack(fill=X, padx=10, pady=10)

        btn_editar_despesa = ttk.Button(
            frame_btn, text="Editar", command=self.editar_despesa
        )
        btn_editar_despesa.pack(side=LEFT, padx=5)

        btn_excluir_despesa = ttk.Button(
            frame_btn, text="Excluir", command=self.excluir_despesa
        )
        btn_excluir_despesa.pack(side=LEFT, padx=5)

        btn_atualizar_despesa = ttk.Button(
            frame_btn, text="Atualizar", command=self.atualizar_despesas
        )
        btn_atualizar_despesa.pack(side=LEFT, padx=5)

        self.atualizar_despesas()

    def salvar_receita(self):

        nome = self.entry_nome_receita.get()
        valor = self.entry_valor_receita.get()

        if not nome or not valor:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            valor = float(valor)
            self.receita_model.adicionar(nome, valor)
            self.entry_nome_receita.delete(0, END)
            self.entry_valor_receita.delete(0, END)
            self.atualizar_receitas()
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Receita adicionada com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número!")

    def salvar_despesa(self):

        data = self.entry_data_despesa.get()
        mes = self.entry_mes_despesa.get()
        nome = self.entry_nome_despesa.get()
        valor = self.entry_valor_despesa.get()

        if not data or not mes or not nome or not valor:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            valor = float(valor)
            self.despesa_model.adicionar(data, mes, nome, valor)
            self.entry_data_despesa.delete(0, END)
            self.entry_data_despesa.insert(0, datetime.now().strftime("%d/%m/%Y"))
            self.entry_mes_despesa.delete(0, END)
            self.entry_mes_despesa.insert(0, datetime.now().strftime("%m/%Y"))
            self.entry_nome_despesa.delete(0, END)
            self.entry_valor_despesa.delete(0, END)
            self.atualizar_despesas()
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Valor deve ser um número!")

    def atualizar_receitas(self):

        for item in self.tree_receitas.get_children():
            self.tree_receitas.delete(item)

        receitas = self.receita_model.listar()
        for receita in receitas:
            self.tree_receitas.insert(
                "", END, values=(receita[0], receita[1], f"R$ {receita[2]:.2f}")
            )

    def atualizar_despesas(self):

        for item in self.tree_despesas.get_children():
            self.tree_despesas.delete(item)

        despesas = self.despesa_model.listar()
        for despesa in despesas:
            self.tree_despesas.insert(
                "",
                END,
                values=(
                    despesa[0],
                    despesa[1],
                    despesa[2],
                    despesa[3],
                    f"R$ {despesa[4]:.2f}",
                ),
            )

    def excluir_receita(self):

        selecionado = self.tree_receitas.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma receita para excluir!")
            return

        item = self.tree_receitas.item(selecionado[0])
        id_receita = item["values"][0]

        if messagebox.askyesno("Confirmação", "Deseja realmente excluir?"):
            self.receita_model.excluir(id_receita)
            self.atualizar_receitas()
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Receita excluída com sucesso!")

    def excluir_despesa(self):

        selecionado = self.tree_despesas.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma despesa para excluir!")
            return

        item = self.tree_despesas.item(selecionado[0])
        id_despesa = item["values"][0]

        if messagebox.askyesno("Confirmação", "Deseja realmente excluir?"):
            self.despesa_model.excluir(id_despesa)
            self.atualizar_despesas()
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Despesa excluída com sucesso!")

    def atualizar_dashboard(self):

        total_receitas = self.receita_model.total_receitas()
        total_despesas = self.despesa_model.total_despesas()

        saldo = total_receitas - total_despesas

        # CORES DO DASHBOARD - Modifique aqui para mudar as cores
        self.lbl_receitas.config(
            text=f"R$ {total_receitas:.2f}", foreground="blue"
        )  # Azul para Receita
        self.lbl_despesas.config(
            text=f"R$ {total_despesas:.2f}", foreground="red"
        )  # Vermelho para Despesa
        self.lbl_saldo.config(text=f"R$ {saldo:.2f}")

        if saldo >= 0:
            self.lbl_saldo.config(foreground="green")
        else:
            self.lbl_saldo.config(foreground="red")

    def editar_receita(self):

        selecionado = self.tree_receitas.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma receita para editar!")
            return

        item = self.tree_receitas.item(selecionado[0])
        id_receita = item["values"][0]
        nome_atual = item["values"][1]
        valor_atual = item["values"][2].replace("R$ ", "")

        # Janela de edição
        janela_edit = tk.Toplevel(self)
        janela_edit.title("Editar Receita")
        janela_edit.geometry("350x200")
        janela_edit.transient(self)
        janela_edit.grab_set()

        ttk.Label(janela_edit, text="Nome:").grid(
            row=0, column=0, sticky=W, padx=10, pady=10
        )
        entry_nome = ttk.Entry(janela_edit, width=25)
        entry_nome.insert(0, nome_atual)
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(janela_edit, text="Valor:").grid(
            row=1, column=0, sticky=W, padx=10, pady=10
        )
        entry_valor = ttk.Entry(janela_edit, width=25)
        entry_valor.insert(0, valor_atual)
        entry_valor.grid(row=1, column=1, padx=10, pady=10)

        def salvar_edicao():
            nome = entry_nome.get()
            valor = entry_valor.get()

            if not nome or not valor:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            try:
                valor = float(valor)
                self.receita_model.editar(id_receita, nome, valor)
                self.atualizar_receitas()
                self.atualizar_dashboard()
                janela_edit.destroy()
                messagebox.showinfo("Sucesso", "Receita editada com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Valor deve ser um número!")

        btn_salvar = ttk.Button(janela_edit, text="Salvar", command=salvar_edicao)
        btn_salvar.grid(row=2, column=1, sticky=E, padx=10, pady=10)

    def editar_despesa(self):

        selecionado = self.tree_despesas.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma despesa para editar!")
            return

        item = self.tree_despesas.item(selecionado[0])
        id_despesa = item["values"][0]
        data_atual = item["values"][1]
        mes_atual = item["values"][2]
        nome_atual = item["values"][3]
        valor_atual = item["values"][4].replace("R$ ", "")

        # Janela de edição
        janela_edit = tk.Toplevel(self)
        janela_edit.title("Editar Despesa")
        janela_edit.geometry("350x300")
        janela_edit.transient(self)
        janela_edit.grab_set()

        ttk.Label(janela_edit, text="Data:").grid(
            row=0, column=0, sticky=W, padx=10, pady=10
        )
        entry_data = ttk.Entry(janela_edit, width=25)
        entry_data.insert(0, data_atual)
        entry_data.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(janela_edit, text="Mês:").grid(
            row=1, column=0, sticky=W, padx=10, pady=10
        )
        entry_mes = ttk.Entry(janela_edit, width=25)
        entry_mes.insert(0, mes_atual)
        entry_mes.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(janela_edit, text="Nome:").grid(
            row=2, column=0, sticky=W, padx=10, pady=10
        )
        entry_nome = ttk.Entry(janela_edit, width=25)
        entry_nome.insert(0, nome_atual)
        entry_nome.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(janela_edit, text="Valor:").grid(
            row=3, column=0, sticky=W, padx=10, pady=10
        )
        entry_valor = ttk.Entry(janela_edit, width=25)
        entry_valor.insert(0, valor_atual)
        entry_valor.grid(row=3, column=1, padx=10, pady=10)

        def salvar_edicao():
            data = entry_data.get()
            mes = entry_mes.get()
            nome = entry_nome.get()
            valor = entry_valor.get()

            if not data or not mes or not nome or not valor:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            try:
                valor = float(valor)
                self.despesa_model.editar(id_despesa, data, mes, nome, valor)
                self.atualizar_despesas()
                self.atualizar_dashboard()
                janela_edit.destroy()
                messagebox.showinfo("Sucesso", "Despesa editada com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Valor deve ser um número!")

        btn_salvar = ttk.Button(janela_edit, text="Salvar", command=salvar_edicao)
        btn_salvar.grid(row=4, column=1, sticky=E, padx=10, pady=10)
