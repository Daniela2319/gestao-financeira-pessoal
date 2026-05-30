import bcrypt
from database import Database


class AuthModel:
    """Gerencia autenticação e usuários do sistema"""

    def __init__(self):
        self.db = Database()
        self._criar_tabela_usuarios()

    def _criar_tabela_usuarios(self):
        """Cria tabela de usuários se não existir"""
        sql = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha_hash BLOB NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.db.executar(sql)

    def _hash_senha(self, senha):
        """Hash seguro da senha usando bcrypt"""
        return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

    def _verificar_senha(self, senha, senha_hash):
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash)

    def criar_usuario(self, username, senha):
        """Cria novo usuário com senha criptografada"""
        try:
            senha_hash = self._hash_senha(senha)
            sql = "INSERT INTO usuarios (username, senha_hash) VALUES (?, ?)"
            self.db.executar(sql, (username, senha_hash))
            return True, "Usuário criado com sucesso!"
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return False, "Usuário já existe!"
            return False, f"Erro ao criar usuário: {str(e)}"

    def listar_usuarios(self):
        """Lista todos os usuários"""
        sql = "SELECT username FROM usuarios"
        resultado = self.db.buscar(sql)
        return [linha[0] for linha in resultado]

    def login(self, username, senha):
        """Valida login do usuário"""
        try:
            sql = "SELECT id, username, senha_hash FROM usuarios WHERE username = ?"
            resultado = self.db.buscar(sql, (username,))

            if not resultado:
                return False, "Usuário não encontrado!"

            usuario_id, user, senha_hash = resultado[0]

            if self._verificar_senha(senha, senha_hash):
                return True, usuario_id
            else:
                return False, "Senha incorreta!"
        except Exception as e:
            return False, f"Erro ao fazer login: {str(e)}"

    def usuario_existe(self):
        """Verifica se já existe algum usuário cadastrado"""
        try:
            sql = "SELECT COUNT(*) FROM usuarios"
            resultado = self.db.buscar(sql)
            return resultado[0][0] > 0
        except:
            return False

    def alterar_senha(self, username, senha_atual, senha_nova):
        """Altera a senha do usuário"""
        try:
            # Verifica senha atual
            sql = "SELECT senha_hash FROM usuarios WHERE username = ?"
            resultado = self.db.buscar(sql, (username,))

            if not resultado:
                return False, "Usuário não encontrado!"

            senha_hash = resultado[0][0]
            if not self._verificar_senha(senha_atual, senha_hash):
                return False, "Senha atual incorreta!"

            # Atualiza para nova senha
            nova_senha_hash = self._hash_senha(senha_nova)
            sql = "UPDATE usuarios SET senha_hash = ? WHERE username = ?"
            self.db.executar(sql, (nova_senha_hash, username))

            return True, "Senha alterada com sucesso!"
        except Exception as e:
            return False, f"Erro ao alterar senha: {str(e)}"
