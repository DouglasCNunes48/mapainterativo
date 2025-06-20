import pyodbc

class Conexao():

    #Propriedades
    def setConectar(self, cnn):
        self.cnn = cnn    

    def getConnectar(self):
        return self.cnn

    def setCursor(self, cursor):
        self.cursor = cursor

    def getCursor(self):
        return self.cursor

    def setDataSet(self, dataSet):
        self.dataset = dataSet

    def getDataSet(self):
        return self.dataset

    #Métodos e funções
    def Conectar(self, drive, servidor, banco, usuario, senha):
        try:
            strConexao ="DRIVER="+drive+';SERVER='+servidor+';DATABASE='+banco+';UID='+usuario+';PWD='+senha
            self.cnn = pyodbc.connect(strConexao, autocommit=False)
        except:
            print("Erro ao se conectar ao banco de dados!")
        return self.cnn

    def getDesconectar(self):
        return self.cnn.close()

    def Executar_Commando_SQL(self, Comando, *args):
        try:
            self.cursor = self.cnn.cursor()
            if len(args) > 0:
                self.cursor.execute(Comando, list(args))
            else:
                self.cursor.execute(Comando)
            
            self.cnn.commit()
            self.cursor.close()
            
            return True
        except:
            print("Erro ao executar comando SQL, validar se a syntax está correta ou os campos/tabela incorretos")
            self.cnn.rollback()
            return False

    def Pegar_Commando_SQL(self, Comando, *args):
        try:
            self.cursor = self.cnn.cursor()

            if  len(args) > 0:
                self.cursor.execute(Comando, list(args)) 
            else:
                self.cursor.execute(Comando)
            
            self.dataset = self.cursor.fetchall()    
            
            self.cursor.close()
            return self.dataset
        except:
            print("Erro ao executar comando SQL, validar se a syntax está correta ou os campos/tabela incorretos")
            return None