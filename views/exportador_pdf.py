from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime

from models.receitas import ReceitaModel
from models.despesas import DespesaModel


class ExportadorPDF:

    def __init__(self):
        self.receita_model = ReceitaModel()
        self.despesa_model = DespesaModel()

    def exportar(self, caminho_arquivo):

        doc = SimpleDocTemplate(
            caminho_arquivo,
            pagesize=letter,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )

        story = []
        styles = getSampleStyleSheet()

        # Título
        titulo = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1F4E78"),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        )

        story.append(Paragraph("RELATÓRIO FINANCEIRO", titulo))
        story.append(Spacer(1, 0.3 * inch))

        # Data de Exportação
        data_exp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data_style = ParagraphStyle(
            "DataExportacao",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER,
        )
        story.append(Paragraph(f"Exportado em: {data_exp}", data_style))
        story.append(Spacer(1, 0.2 * inch))

        # Resumo Financeiro
        story.append(self.criar_resumo(styles))
        story.append(Spacer(1, 0.3 * inch))

        # Tabela de Receitas
        story.append(Paragraph("Receitas Registradas", styles["Heading2"]))
        story.append(Spacer(1, 0.1 * inch))
        story.append(self.criar_tabela_receitas())
        story.append(PageBreak())

        # Tabela de Despesas
        story.append(Paragraph("Despesas Registradas", styles["Heading2"]))
        story.append(Spacer(1, 0.1 * inch))
        story.append(self.criar_tabela_despesas())

        doc.build(story)
        return True

    def criar_resumo(self, styles):

        total_receitas = self.receita_model.total_receitas()
        total_despesas = self.despesa_model.total_despesas()
        saldo = total_receitas - total_despesas

        dados = [
            ["Descrição", "Valor"],
            ["Total de Receitas", f"R$ {total_receitas:.2f}"],
            ["Total de Despesas", f"R$ {total_despesas:.2f}"],
            ["Saldo", f"R$ {saldo:.2f}"],
        ]

        tabela = Table(dados, colWidths=[3 * inch, 2 * inch])

        estilo = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("ALIGN", (0, 1), (0, -1), "LEFT"),
                ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica-Bold"),
            ]
        )

        tabela.setStyle(estilo)
        return tabela

    def criar_tabela_receitas(self):

        receitas = self.receita_model.listar()

        dados = [["ID", "Nome", "Valor"]]

        for receita in receitas:
            dados.append([str(receita[0]), receita[1], f"R$ {receita[2]:.2f}"])

        if len(dados) == 1:
            dados.append(["", "Sem registros", ""])

        tabela = Table(dados, colWidths=[0.7 * inch, 3.5 * inch, 1.3 * inch])

        estilo = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C6E0B4")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("ALIGN", (0, 1), (0, -1), "CENTER"),
                ("ALIGN", (1, 1), (1, -1), "LEFT"),
                ("ALIGN", (2, 1), (2, -1), "RIGHT"),
            ]
        )

        tabela.setStyle(estilo)
        return tabela

    def criar_tabela_despesas(self):

        despesas = self.despesa_model.listar()

        dados = [["ID", "Data", "Mês", "Nome", "Valor"]]

        for despesa in despesas:
            dados.append(
                [
                    str(despesa[0]),
                    despesa[1],
                    despesa[2],
                    despesa[3],
                    f"R$ {despesa[4]:.2f}",
                ]
            )

        if len(dados) == 1:
            dados.append(["", "", "", "Sem registros", ""])

        tabela = Table(
            dados, colWidths=[0.7 * inch, 1 * inch, 0.9 * inch, 2.4 * inch, 1.3 * inch]
        )

        estilo = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F4B084")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("ALIGN", (0, 1), (0, -1), "CENTER"),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("ALIGN", (2, 1), (2, -1), "CENTER"),
                ("ALIGN", (3, 1), (3, -1), "LEFT"),
                ("ALIGN", (4, 1), (4, -1), "RIGHT"),
            ]
        )

        tabela.setStyle(estilo)
        return tabela
