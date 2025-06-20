import sgs
import datetime
import pandas as pd

class WebBCB():

    def setWbcb(self, wbcb):
        self.wbcb = wbcb
    
    def getWbcb(self):
        return self.wbcb
    
    def setValor(self, valor):
        self.valor = valor

    def getValor(self):
        return self.valor

    #Retorna o valor da série pela data informada
    def GetValorSerie(self, serie, dataInicio):
        try:
            if dataInicio == None:
                print("Necessário uma data inicio para retorno da série!")
                return None
            else:
                self.wbcb = sgs.SGS()
                self.valor = self.wbcb.get_valores_series(serie, dataInicio, dataInicio)
            return self.valor
        except:
            print("Verifique se a séria selecionada existe ou data está correta!")
            return None

    #Retorna o ultimo valor atualizado da série
    def GetUltimoValor(self, serie):
        try:
            self.wbcb = sgs.SGS()
            self.valor = self.wbcb.get_valores_series(serie, datetime.date, datetime.date)
            return self.valor
        except:
            print("Verifiquei se a série selecionada existe!")
            return None

    #Retorna o valores da sério entre um período
    def GetValorSerie_Periodo(self, serie, dataInicio, dataFim):
        try:
            if dataFim <= dataInicio:
                print("A data fim deve sempre ser maior que a data inicio!")
                return None
            else:
                self.wbcb = sgs.SGS()
                self.valor = self.wbcb.get_valores_series(serie, dataInicio, dataFim)
                
                listaValores = list()
                for valores in self.valor.get_values():
                    listaValores.append(valores[1])   
                
                return listaValores
        except:
            print("Verifique se a série selecionada existe ou se o período está correto!")
            return None