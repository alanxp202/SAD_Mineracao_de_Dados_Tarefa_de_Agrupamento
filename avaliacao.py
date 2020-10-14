import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#Efetua a leitura do CSV de apenas 1000 entradas e de determinadas colunas
df = pd.read_csv('Base-INFLUD-14-09-2020.csv', sep=';', nrows=1000,  usecols = ['SG_UF_NOT','CLASSI_FIN', 'EVOLUCAO'])


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
    new_df= pd.DataFrame(columns=['Pessoas', 'Óbito por COVID-19'], index=uf_estados)
    
    return new_df


new_df = novo_dataframe(df)

#Adciona no novo DataFrame, as informações das pessoas presentes em cada estado do país
def add_pessoa_por_estado():
    pessoa = count_pessoas()
    new_df['Pessoas'] = pessoa


#Adciona no novo DataFrame, as demais informações escolhidas para analise, das pessoas em cada estado do país
def add_dados():

    ct_obtb_covid = []
    ct_oc = 0

    for uf in uf_estados:
        for index, row in df.iterrows():
            if row['SG_UF_NOT'] == uf: 
                if row['CLASSI_FIN'] == 5 and row['EVOLUCAO'] == 2:
                    ct_oc+=1              

        ct_obtb_covid.append(ct_oc)
        ct_oc = 0

    new_df['Óbito por COVID-19'] = ct_obtb_covid
    print('\nTabela com os dados agrupados por estado')
    print(new_df)

#Realiza a normalização dados obtidos no novo DataFrame
def normaliza_dados():

    new_df_norm = (new_df-new_df.min())/(new_df.max()-new_df.min())
    return new_df_norm


add_pessoa_por_estado()
add_dados()
tabela_normalizada = normaliza_dados()

print('\nTabela com os dados normalizados')
print(tabela_normalizada)

def k_means():
    
    kmeans = KMeans(n_clusters=3).fit(tabela_normalizada)
    centroids = kmeans.cluster_centers_
    
    print('\nOs melhores centroides serão:')
    print(pd.DataFrame(centroids))

    plt.scatter(tabela_normalizada['Pessoas'], tabela_normalizada['Óbito por COVID-19'], c= kmeans.labels_.astype(float), s=100, alpha=0.5)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=10)
    plt.title('Pessoas que Vieram a óbito por COVID-19 e os centroids')
    plt.xlabel('Óbito por COVID-19')
    plt.ylabel('Pessoas')
    plt.show()

k_means()