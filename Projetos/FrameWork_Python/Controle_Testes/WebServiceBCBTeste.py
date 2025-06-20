import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))),
import WebServiceBCB

if __name__ == '__main__':
    wb = WebServiceBCB.WebBCB()
    listaValores = wb.GetValorSerie_Periodo(1,"01/02/2019","20/02/2019")
    ultValor = wb.GetUltimoValor(1)
    valorData = wb.GetValorSerie(1,"01/02/2019")