from database import Database


class DespesaModel:

    def __init__(self):
        self.db = Database()

    def adicionar(self, data, mes, nome, valor):

        sql = """
        INSERT INTO despesas (data, mes, nome, valor)
        VALUES (?, ?, ?, ?)
        """

        self.db.executar(sql, (data, mes, nome, valor))

    def listar(self):

        sql = "SELECT * FROM despesas"
        return self.db.buscar(sql)

    def excluir(self, id_despesa):

        sql = "DELETE FROM despesas WHERE id=?"
        self.db.executar(sql, (id_despesa,))

    def editar(self, id_despesa, data, mes, nome, valor):

        sql = """
        UPDATE despesas SET data=?, mes=?, nome=?, valor=? WHERE id=?
        """
        self.db.executar(sql, (data, mes, nome, valor, id_despesa))

    def total_despesas(self):

        sql = "SELECT SUM(valor) FROM despesas"
        resultado = self.db.buscar(sql)

        return resultado[0][0] if resultado[0][0] else 0
