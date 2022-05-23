import mysql.connector
import ast
from os.path import join, dirname, realpath

config_path = join(dirname(realpath(__file__)), 'banco.inf')

class UsaBanco:
    """pega as configuracoes de conexao ao banco de dados no arquivo banco.inf e cria
    um gerenciador de contexto para usar na aplicacao"""
    def __init__(self):
        self.config = ast.literal_eval(open(config_path).read())

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self,exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
