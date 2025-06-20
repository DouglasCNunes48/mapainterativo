import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))),
import ConexaoBanco

if __name__ == '__main__':
    db = ConexaoBanco.Conexao()
    db.Conectar("{SQL Server}","10.25.2.110","DB_ConciliacaoFundos","SysConciFundos","jive@2018")

    db.Executar_Commando_SQL("CREATE TABLE tblTeste(" +
                            "Nome NVARCHAR(20), Idade INT)")

    if db.Executar_Commando_SQL("INSERT INTO tblTeste VALUES(?, ?)", "Paul", 26):
        print("Cadastro realizado com sucesso!")
        
        db.Pegar_Commando_SQL("SELECT * FROM tblTeste WHERE Idade=?", 26)
        db.Executar_Commando_SQL("DELETE FROM tblTeste WHERE Nome=?", "Paul")
        db.Executar_Commando_SQL("DROP TABLE tblTeste")