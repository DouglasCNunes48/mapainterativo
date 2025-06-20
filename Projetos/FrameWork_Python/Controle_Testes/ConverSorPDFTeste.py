import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))),
import ConversorPDF

if __name__ == '__main__':
    cvPDF = ConversorPDF.ConverterPDF()
    cvPDF.ConverterPDFParaExcel_UnicaPagina('M:\Fundos\Paulo Gallo\Accounts Statement - from 01-Jan-2015 to 14-May-2019.pdf')