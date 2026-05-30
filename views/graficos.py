import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from models.receitas import ReceitaModel
from models.despesas import DespesaModel


class Graficos(tb.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.receita_model = ReceitaModel()
        self.despesa_model = DespesaModel()

        self.pack(fill=BOTH, expand=True)

        self.criar_interface()

    def criar_interface(self):

        titulo = tb.Label(
            self,
            text="📈 Gráficos Financeiros",
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-dark",
        )
        titulo.pack(pady=15, fill=X)

        # Frame para os gráficos
        frame_graficos = ttk.Frame(self)
        frame_graficos.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Gráfico de Pizza (Receitas vs Despesas)
        frame_pizza = ttk.LabelFrame(frame_graficos, text="📊 Receitas vs Despesas")
        frame_pizza.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)

        self.canvas_pizza = None
        self.desenhar_pizza(frame_pizza)

        # Gráfico de Barras (Histórico)
        frame_barras = ttk.LabelFrame(frame_graficos, text="📈 Histórico Mensal")
        frame_barras.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)

        self.canvas_barras = None
        self.desenhar_barras(frame_barras)

        # Configurar grid
        frame_graficos.grid_rowconfigure(0, weight=1)
        frame_graficos.grid_columnconfigure(0, weight=1)
        frame_graficos.grid_columnconfigure(1, weight=1)

        # Botão para atualizar
        btn_atualizar = tb.Button(
            self,
            text="🔄 Atualizar Gráficos",
            command=self.atualizar_graficos,
            bootstyle="info",
        )
        btn_atualizar.pack(pady=10)

    def desenhar_pizza(self, frame):

        total_receitas = self.receita_model.total_receitas()
        total_despesas = self.despesa_model.total_despesas()

        # Remover canvas anterior
        if self.canvas_pizza:
            self.canvas_pizza.get_tk_widget().destroy()

        fig = Figure(figsize=(5, 4), dpi=100, facecolor="#f0f3f7")
        ax = fig.add_subplot(111)

        valores = [total_receitas, total_despesas]
        labels = [
            f"Receitas\nR$ {total_receitas:,.2f}",
            f"Despesas\nR$ {total_despesas:,.2f}",
        ]
        cores = ["#06a77d", "#d62828"]  # Verde e Vermelho bancário
        explode = (0.05, 0.05)

        if total_receitas == 0 and total_despesas == 0:
            ax.text(
                0.5,
                0.5,
                "Sem dados para exibir",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
            )
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
        else:
            ax.pie(
                valores,
                labels=labels,
                autopct="%1.1f%%",
                colors=cores,
                startangle=90,
                explode=explode,
                textprops={"fontsize": 10, "weight": "bold"},
            )

        ax.set_title(
            "Distribuição de Receitas e Despesas",
            fontsize=12,
            fontweight="bold",
            pad=20,
        )

        self.canvas_pizza = FigureCanvasTkAgg(fig, master=frame)
        self.canvas_pizza.draw()
        self.canvas_pizza.get_tk_widget().pack(fill=BOTH, expand=True)

    def desenhar_barras(self, frame):

        despesas = self.despesa_model.listar()

        # Remover canvas anterior
        if self.canvas_barras:
            self.canvas_barras.get_tk_widget().destroy()

        fig = Figure(figsize=(5, 4), dpi=100, facecolor="#f0f3f7")
        ax = fig.add_subplot(111)

        if despesas:
            # Agrupar despesas por mês
            meses_dict = {}
            for despesa in despesas:
                mes = despesa[2]  # mes
                valor = despesa[4]  # valor
                if mes not in meses_dict:
                    meses_dict[mes] = 0
                meses_dict[mes] += valor

            meses = list(meses_dict.keys())
            valores = list(meses_dict.values())

            bars = ax.bar(
                meses,
                valores,
                color="#00a8e8",
                alpha=0.8,
                edgecolor="#1a3a52",
                linewidth=1.5,
            )

            # Adicionar valores nas barras
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"R$ {height:,.0f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                    fontsize=9,
                )

            ax.set_xlabel("Mês", fontweight="bold")
            ax.set_ylabel("Valor (R$)", fontweight="bold")
            ax.set_title("Despesas por Mês", fontsize=12, fontweight="bold", pad=20)
            ax.tick_params(axis="x", rotation=45)
            ax.grid(axis="y", alpha=0.3)
        else:
            ax.text(
                0.5,
                0.5,
                "Sem dados para exibir",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
            )
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

        self.canvas_barras = FigureCanvasTkAgg(fig, master=frame)
        self.canvas_barras.draw()
        self.canvas_barras.get_tk_widget().pack(fill=BOTH, expand=True)

    def atualizar_graficos(self):

        # Remover todos os widgets
        for widget in self.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                widget.destroy()

        # Recriar interface
        self.criar_interface()
