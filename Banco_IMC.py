import sqlite3

class Banco_IMC():

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        c = self.conn.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='pacientes' ''')
        if c.fetchone()[0]==0:
            print("created")
            c.execute("""
            CREATE TABLE pacientes (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    peso INTEGER NOT NULL,
                    altura INTEGER NOT NULL);""")
    def __del__(self):
        self.conn.close()
        
    def insert(self, nome, endereco, peso, altura):
        c = self.conn.cursor()
        try:
            c.execute(f"""
            INSERT INTO pacientes (nome, endereco, peso, altura)
            VALUES ('{nome}', '{endereco}', {peso}, {altura})
            """)
            self.conn.commit()
        except:
            raise Exception('Valores inseridos são inválidos')

    def return_by_id(self,Id):
        c = self.conn.cursor()
        try:
            c.execute(f"""
            SELECT * FROM pacientes
            WHERE id = {Id} """)
            return c.fetchall()[0]
        except:
            return None;
