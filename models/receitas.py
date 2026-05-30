from database import Database


class ReceitaModel:

    def __init__(self):
        self.db = Database()

    def adicionar(self, nome, valor):

        sql = "INSERT INTO receitas (nome, valor) VALUES (?, ?)"
        self.db.executar(sql, (nome, valor))

    def listar(self):

        sql = "SELECT * FROM receitas"
        return self.db.buscar(sql)

    def excluir(self, id_receita):

        sql = "DELETE FROM receitas WHERE id=?"
        self.db.executar(sql, (id_receita,))

    def editar(self, id_receita, nome, valor):

        sql = "UPDATE receitas SET nome=?, valor=? WHERE id=?"
        self.db.executar(sql, (nome, valor, id_receita))

    def total_receitas(self):

        sql = "SELECT SUM(valor) FROM receitas"
        resultado = self.db.buscar(sql)

        return resultado[0][0] if resultado[0][0] else 0
