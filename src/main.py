# app.py
from datetime import timedelta
import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(
    page_title='Análise Agrícola',
    page_icon='🌾',
    layout='wide'
)
st.title('Análise Agrícola de temperatura e umidade 🌾')
st.write('Bem-vindo ao aplicativo.')
st.markdown("""
Este aplicativo permite visulizar o dataset e observar a flutuação da media da temperatura e umidade
""")
st.header('1. Carregando os Dados')
df = pd.read_csv("dados_data_temp_umidade_out_nov.csv", sep=",")
# arrumando o dataset
df = df.ffill()
df['DATA_MEDICAO'] = pd.to_datetime(df['DATA_MEDICAO'], dayfirst=True)
df['DATA_MEDICAO'] = df['DATA_MEDICAO'].dt.strftime('%d/%m/%y')
#df['TEMPERATURA_MEDIA'] = df['TEMPERATURA_MEDIA'].str.replace(',', '.').astype(float)
#df['UMIDADE_MEDIA'] = df['UMIDADE_MEDIA'].str.replace(',', '.').astype(float)
# Visualizando o dataset e mostrando suas informações
st.header('visualizando os dados')
st.dataframe(df.head())
st.header('2. Carregando os Dados')
st.subheader('Informações sobre o dataset')
st.write('Dimensões do dataset: ')
st.write(f'linhas: {df.shape[0]}, colunas: {df.shape[1]}')
st.subheader('Informações sobre o dataset')
st.subheader('Tipos de dados')
df_types = pd.DataFrame({
    'Coluna': df.columns,
    'Tipos de dados': df.dtypes.astype(str)
})
st.write(df_types)


st.header('3. Grafico')
# fazendo o grafico de linhas com temperatura e umidade
df = df
graph = st.line_chart(data=df, x="DATA_MEDICAO", y=['UMIDADE_MEDIA', 'TEMPERATURA_MEDIA'], color=['#FF0000', '#0000FF'])
st.write("Adcionar nova entrada de temperatura e umidade")
temperatura = st.number_input("Digite a temperatura: ")
umidade = st.number_input("Digite a umidade: ")

# pegando a ultima data da medicao para ser usado na proxima inserção
#ultima_data = pd.to_datetime(df['DATA_MEDICAO'].max())
ultima_data = pd.to_datetime(df['DATA_MEDICAO'].iloc[-1], dayfirst=True)
#st.write(ultima_data)
#proxima_data = (ultima_data + pd.Timedelta(days=1))
proxima_data = ultima_data + pd.DateOffset(days=1)
#st.write(proxima_data)
proxima_data = proxima_data.strftime('%d/%m/%Y')
#st.write(proxima_data)

# fazendo os botões
left, middle = st.columns(2)
if left.button("Enviar dados", use_container_width=True):
    if temperatura > 35 or umidade < 45:
        bombas = 1
    else:
        bombas = 0
    # construindo o dataframe pra ser concatenado ao anterior
    df2 = pd.DataFrame({
        'DATA_MEDICAO': [proxima_data],
        'TEMPERATURA_MEDIA': [temperatura],
        'UMIDADE_MEDIA': [umidade],
        'FOSFORO': [np.random.randint(0, 2)],
        'POTASSIO': [np.random.randint(0, 2)],
        'BOMBAS_LIGADAS': [bombas]
    })
    graph.add_rows(df2)
    df = pd.concat([df, df2], ignore_index=True)

if middle.button("Gerar dados aleatorios", use_container_width=True):
    temperatura_med = np.random.uniform(15, 40)
    temperatura_med = np.round(temperatura_med, 1)
    umidade_med = np.random.uniform(40, 90)
    umidade_med = np.round(umidade_med, 1)

    if temperatura_med > 35 or umidade_med < 45:
        bombas = 1
    else:
        bombas = 0
    # construindo o dataframe pra ser concatenado ao anterior
    df2 = pd.DataFrame({
        'DATA_MEDICAO': [proxima_data],
        'TEMPERATURA_MEDIA': [temperatura_med],
        'UMIDADE_MEDIA': [umidade_med],
        'FOSFORO': [np.random.randint(0, 2)],
        'POTASSIO': [np.random.randint(0, 2)],
        'BOMBAS_LIGADAS': [bombas]
    })
    graph.add_rows(df2)
    df = pd.concat([df, df2], ignore_index=True)
# mostrando o dataset e dps exportando ele
st.subheader("Dataset")
st.dataframe(df)
df.to_csv("dados_data_temp_umidade_out_nov.csv", index=False)

