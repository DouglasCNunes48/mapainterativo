from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mechanicalsoup as ms
import pandas as pd
import requests
import smtplib as smtp

def wsCnpjEmpresas(df):
    campos = {
        "Id": "empresaVagas_ds",
        "CNPJ": "cnpj_ds",
        "Razão Social": "razaoSocial_ds",
        "Nome Fantasia": "fantasia_ds",
        "Data Abertura": "dataAbertura_dt",
        "Natureza Jurídica": "naturezaJuridica_ds",
        "Tipo": "tipo_ds",
        "Situação": "situacao_ds",
        "Estado": "estado_ds",
        "Sobre": "sobre_ds"
    }

    dfCnpj = pd.DataFrame(columns=["nomeEmpresa_ds", "campo_ds", "valor_ds"])

    for ind in df.index:
        TimeExecucao(5000)

        empresaPrincipal = str(df['empresa'][ind])
        url = "https://cnpj.biz/procura/" + str(df['empresa'][ind])

        browser = ms.StatefulBrowser()
        browser.open(url)

        if str(browser.page.status_code)[0] != "2":
            div = browser.page.find_all('div', class_='max-w-4xl mx-auto bg-white shadow overflow-hidden sm:rounded-md')
            for divList in div:
                ul = divList.find('ul', class_='divide-y divide-gray-200')
                for li in ul:
                    if li != ' ':
                        ancoras = li.find_all('a')
                        for ancora in ancoras:
                            link = ancora['href']
                            infoEmpresa = requests.get(link)
                            if str(infoEmpresa.status_code)[0] != "2":
                                break

                            soupInfo = BeautifulSoup(infoEmpresa.content, "html.parser")
                            paragrafos = soupInfo.find_all('p')

                            for p in paragrafos:
                                findCaracter = int(str(p.text).find(":"))
                                item = str(p.text)[0:findCaracter]

                                for campo in campos:
                                    if campo == item:
                                        tamanho = int(len(p.text))
                                        findCaracter = int(findCaracter) + 1
                                        columns = campos[campo]
                                        dfCnpj = dfCnpj.append(
                                            {"nomeEmpresa_ds": empresaPrincipal, "campo_ds": columns,
                                             "valor_ds": str(p.text)[findCaracter:tamanho]}, ignore_index=True)
                                        break

    if len(dfCnpj) > 0:
        dfCnpjVagas = pd.merge(df, dfCnpj, on='empresa')
        dfCnpjVagas.to_csv('EmpresasComDados.csv', index=False)
        return dfCnpjVagas
    else:
        return None

def EnvioEmail(destino, assunto, body):
    s = smtp.SMTP(host='smtp.office365.com', port=587)
    s.starttls()
    s.login('seu_email', 'sua_senha')

    msg = MIMEMultipart()
    msg['From'] = 'seu_email'
    msg['To'] = destino
    msg['Subject'] = assunto
    msg.attach(MIMEText(body))

    s.send_message(msg)
    s.quit()

def TimeExecucao(Tempo):
    contador = 0
    while contador <= Tempo:
        contador = contador + 1

# Verifica se o arquivo empresa.csv existe
caminho_arquivo = r'C:\Users\douglas.nunes\Desktop\webscraping\empresa.csv'
try:
    df_empresa = pd.read_csv(caminho_arquivo, error_bad_lines=False)
except FileNotFoundError:
    raise Exception(f"Arquivo empresa.csv não encontrado no caminho: {caminho_arquivo}")
else:
    print("Arquivo empresa.csv lido com sucesso.")


# Verifica se a coluna 'empresa' existe no DataFrame df_empresa
if 'empresa' not in df_empresa.columns:
    raise Exception("Coluna 'empresa' não encontrada no arquivo empresa.csv.")
else:
    print("Coluna 'empresa' encontrada no arquivo empresa.csv.")

# Método main que inicia a execução do código
if __name__ == '__main__':
    dfFinal = wsCnpjEmpresas(df_empresa)
if dfFinal is not None:
    # Define o caminho completo do arquivo de saída
    caminho_saida = r'C:\Users\douglas.nunes\Desktop\webscraping\Leads_Linkedin.csv'

    # Salva o DataFrame em um arquivo CSV
    dfFinal.to_csv(caminho_saida, index=False)
    EnvioEmail('destinatario@example.com', 'Web Scraping Concluído', 'O processo de web scraping foi concluído com sucesso.')
    print("E-mail enviado.")
else:
    print("Nenhum dado coletado.")
