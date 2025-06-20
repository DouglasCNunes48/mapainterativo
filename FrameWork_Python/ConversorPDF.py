import pdftables_api as pdfConverter
    
class ConverterPDF(): 

    def ConverterPDFParaExcel_UnicaPagina(self, Endereco):
        arquivoExcel = pdfConverter.Client('5xyfripskm21',timeout=(60,3600))
        try:
            arquivoExcel.xlsx_single(Endereco, Endereco.replace('.pdf','.xlsx'))
            return arquivoExcel
        except:
            print("Erro ao converter arquivo para Excel!")
            return None

    def ConverterPDFParaExcel_VariasPaginas(self, Endereco):
        arquivoExcel = pdfConverter.Client('5xyfripskm21',timeout=(60,3600))
        try:
            arquivoExcel.xlsx_multiple(Endereco, Endereco.replace('.pdf','.xlsx'))
            return arquivoExcel
        except:
            print("Erro ao converter arquivo para Excel!")
            return None

    def ConverterPDFParaCSV(self, Endereco):
        arquivoCSV = pdfConverter.Client('paulo.gallo',timeout=(60,3600))
        try:
            arquivoCSV.csv(Endereco, Endereco.replace('.pdf','.csv'))
            return arquivoCSV
        except:
            print("Erro ao converter arquivo para CSV!")
            return None