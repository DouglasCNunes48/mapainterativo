# -*- coding: utf-8 -*-
"""
Created on Fri May 26 11:53:50 2023

@author: douglas.nunes
"""

import requests
import pandas as pd
import json
import time

# Caminho para o arquivo empreendimento.csv
caminho_arquivo = r'C:\Users\douglas.nunes\OneDrive - CBRE, Inc\Projeto SharePoint²\Extranet\Building Insight\Portal_Ires\Realizado_impostos\empreendimento.csv'

# Leitura do arquivo CSV e criação do DataFrame
df_empreendimento = pd.read_csv(caminho_arquivo)

# Obtendo a lista de códigos de empreendimento
codigos_empreendimentos = df_empreendimento['cd_empreendimento'].tolist()

# URL para acessar a tabela de despesas
url_despesas = 'https://services3.livefacilities.com.br/mobile/api/prestacaoContas/despesas'

# Realizar login e obter id_pessoafisica e id_sessao
request_url = 'https://services3.livefacilities.com.br/mobile/api/login/loginsistema/'
livefacilities_apptoken = '1DF81E17-D766-4701-A16C-82BD6F51E377'

headers = {
    'Content-Type': 'application/xml',
    'livefacilities-apptoken': livefacilities_apptoken,
}

xml_login = '''<?xml version="1.0" encoding="UTF-8" ?>
<Login>
  <nm_sistema>CBR</nm_sistema>
  <id_pessoafisica>0</id_pessoafisica>
  <id_sessao>0</id_sessao>
  <id_chavedispositivo>0</id_chavedispositivo>
  <nm_usuario>douglas.nunes</nm_usuario>
  <nm_senha>0M1529</nm_senha>
</Login>
'''

response = requests.post(request_url, data=xml_login, headers=headers)
response.raise_for_status()  # Lança uma exceção se a resposta indicar um erro HTTP
response_json = json.loads(response.text)
print(response_json)

# Parse do XML de resposta
id_sessao = response_json['id_sessao']
id_pessoafisica = response_json['id_pessoafisica']

# DataFrame com id_sessao e id_pessoafisica
df_login = pd.DataFrame({
'id_sessao': [id_sessao],
'id_pessoafisica': [id_pessoafisica]
})

# Loop para realizar a requisição de cada código de empreendimento
df_despesas = pd.DataFrame()

for codigo in codigos_empreendimentos:
    xml_despesas = f'''<?xml version="1.0" encoding="UTF-8" ?>
    <pacote>
        <infoLogin>
            <nm_sistema>CBR</nm_sistema>
            <id_pessoafisica>{id_pessoafisica}</id_pessoafisica>
            <id_sessao>{id_sessao}</id_sessao>
            <id_chavedispositivo>apiipms</id_chavedispositivo>
        </infoLogin>
        <cd_condominio>18</cd_condominio>
        <dt_inicio>2023-01-01</dt_inicio>
        <dt_fim>2023-01-05</dt_fim>
        <sn_competencia>0</sn_competencia>
    </pacote>
    '''

    response_despesas = requests.post(url_despesas, data=xml_despesas, headers=headers)
    response_despesas.raise_for_status()
    response_despesas_json = json.loads(response_despesas.text)

    # Extrair os campos desejados do XML de resposta
    for despesa in response_despesas_json['PrestacaoContasDespesas']:
        dt_vencimento = despesa['dt_vencimento']
        dt_pagamento = despesa['dt_pagamento']
        tx_historico = despesa['tx_historico']
        valor = despesa['valor']
        nm_centrocusto = despesa['nm_centrocusto']
        id_centrocusto = despesa['id_centrocusto']
        id_conta1 = despesa['id_conta1']
        nm_conta1 = despesa['nm_conta1']
        nu_integracao1 = despesa['nu_integracao1']
        id_conta2 = despesa['id_conta2']
        nm_conta2 = despesa['nm_conta2']
        nu_integracao2 = despesa['nu_integracao2']
        id_conta3 = despesa['id_conta3']
        nm_conta3 = despesa['nm_conta3']
        nu_integracao3 = despesa['nu_integracao3']

        # Adicionar as informações ao DataFrame df_despesas
        df_despesas = df_despesas.append({
            "cd_condominio": codigo,
            "dt_vencimento": dt_vencimento,
            "dt_pagamento": dt_pagamento,
            "tx_historico": tx_historico,
            "valor": valor,
            "nm_centrocusto": nm_centrocusto,
            "id_centrocusto": id_centrocusto,
            "id_conta1": id_conta1,
            "nm_conta1": nm_conta1,
            "nu_integracao1": nu_integracao1,
            "id_conta2": id_conta2,
            "nm_conta2": nm_conta2,
            "nu_integracao2": nu_integracao2,
            "id_conta3": id_conta3,
            "nm_conta3": nm_conta3,
            "nu_integracao3": nu_integracao3
            }, ignore_index=True)
        
# Verificar se a lista_despesa não está vazia antes de criar o DataFrame
        if not df_despesas.empty:
            
# Salvar o DataFrame df_despesas em um arquivo CSV
            df_despesas.to_csv('despesas_imposto.csv', index=False)
        
        print("Arquivo despesas_imposto.csv gerado com sucesso.")
        
# Aguardar 10 segundos antes da próxima requisição
        time.sleep(3)
else:
    print("A lista de despesas está vazia")