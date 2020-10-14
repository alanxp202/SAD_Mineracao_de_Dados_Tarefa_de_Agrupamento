import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#Efetua a leitura do CSV de apenas 1000 entradas e de determinadas colunas
df = pd.read_csv('Base-INFLUD-14-09-2020.csv', sep=';', nrows=1000,  usecols = ['SG_UF_NOT','FEBRE','TOSSE','GARGANTA', 
                 'DISPNEIA', 'DESC_RESP', 'SATURACAO', 'FATOR_RISC', 'CLASSI_FIN', 'EVOLUCAO'])


#Extrai da base de dados apenas os estados das 1000 entradas
def df_estados():

    index_estados = []

    for dado in df.SG_UF_NOT:
        index_estados.append(dado)

    return index_estados


pessoa_por_estado = df_estados()
uf_estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA',
      'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

#Calcula o numero de pessoas agrupadas pelo seu estado de registro de dados
def count_pessoas():
    pessoa = []
    for uf in uf_estados:
        pessoa.append(pessoa_por_estado.count(uf))
    return pessoa


#Cria um novo DataFrame contendo informações escolhidas para analise pelo estado
def novo_dataframe(dados):

    #definir novo dataframe organizando as pessoas por estado
    new_df= pd.DataFrame(columns=['Pessoas', 'Febre', 'Tosse', 'Dor de Garganta', 'Falta de ar (Dispneia)', 
                     'Desconforto Respiratório', 'Saturação O²< 95%', 'Fator de Risco', 'COVID-19', 
                     'Outras doenças', 'Óbito por COVID-19'], index=uf_estados)
    
    return new_df


new_df = novo_dataframe(df)

#Adciona no novo DataFrame, as informações das pessoas presentes em cada estado do país
def add_pessoa_por_estado():
    pessoa = count_pessoas()
    new_df['Pessoas'] = pessoa


#Adciona no novo DataFrame, as demais informações escolhidas para analise, das pessoas em cada estado do país
def add_dados():

    ct_febre =[]
    ct_tosse = []
    ct_garganta = []
    ct_dispneia = []
    ct_desc_resp = []
    ct_saturacao = []
    ct_fator_risc = []
    ct_classi_fin = []
    ct_outr_doec = []
    ct_obtb_covid = []
    total =[]
    ct_f = ct_t = ct_g = ct_d = ct_df = ct_s = ct_fr = ct_cf = ct_od = ct_oc = 0

    for uf in uf_estados:
        for index, row in df.iterrows():
            if row['SG_UF_NOT'] == uf: 
                if row['FEBRE'] == 1:
                    ct_f+=1
                if row['TOSSE'] == 1:
                    ct_t+=1
                if row['GARGANTA'] == 1:
                    ct_g+=1
                if row['DISPNEIA'] == 1:
                    ct_d+=1
                if row['DESC_RESP'] == 1:
                    ct_df+=1
                if row['SATURACAO'] == 1:
                    ct_s+=1
                if row['FATOR_RISC'] == 'S':
                    ct_fr+=1
                if row['CLASSI_FIN'] == 5:
                    ct_cf+=1
                else:
                    ct_od+=1
                if row['CLASSI_FIN'] == 5 and row['EVOLUCAO'] == 2:
                    ct_oc+=1              

        ct_febre.append(ct_f)
        ct_tosse.append(ct_t)
        ct_garganta.append(ct_g)
        ct_dispneia.append(ct_d)
        ct_desc_resp.append(ct_df)
        ct_saturacao.append(ct_s)
        ct_fator_risc.append(ct_fr)
        ct_classi_fin.append(ct_cf)
        ct_outr_doec.append(ct_od)
        ct_obtb_covid.append(ct_oc)
        ct_f = ct_t = ct_g = ct_d = ct_df = ct_s = ct_fr = ct_cf = ct_od = ct_oc = 0

    new_df['Febre'] = ct_febre
    new_df['Tosse'] = ct_tosse
    new_df['Dor de Garganta'] = ct_garganta
    new_df['Falta de ar (Dispneia)'] = ct_dispneia
    new_df['Desconforto Respiratório'] = ct_desc_resp
    new_df['Saturação O²< 95%'] = ct_saturacao
    new_df['Fator de Risco'] = ct_fator_risc
    new_df['COVID-19'] = ct_classi_fin
    new_df['Outras doenças'] = ct_outr_doec
    new_df['Óbito por COVID-19'] = ct_obtb_covid

    #print(new_df)


#Realiza a normalização dados obtidos no novo DataFrame
def normaliza_dados():

    new_df_norm = (new_df-new_df.min())/(new_df.max()-new_df.min())
    return new_df_norm


add_pessoa_por_estado()
add_dados()
tabela_normalizada = normaliza_dados()

def k_means():
    
    kmeans = KMeans(n_clusters=3).fit(tabela_normalizada)
    centroids = kmeans.cluster_centers_
    
    print('Os melhores centroides serão:')
    print(pd.DataFrame(centroids))

    plt.scatter(tabela_normalizada['Pessoas'], tabela_normalizada['Óbito por COVID-19'], c= kmeans.labels_.astype(float), s=100, alpha=0.5)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=10)
    plt.title('Pessoas que Vieram a óbito por COVID-19 e os centroids')
    plt.xlabel('Óbito por COVID-19')
    plt.ylabel('Pessoas')
    plt.show()

k_means()