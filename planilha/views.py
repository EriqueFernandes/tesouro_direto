from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import wget
import pandas as pd
import json
from scipy.stats import norm
# %matplotlib inline
import matplotlib.pyplot as plt
import matplotlib
import tornado
import tkinter
import requests
# import threading

# Create your views here.
plt.close('all')
# matplotlib.use('Agg')
# matplotlib.use('SVG')
BASE_DIR = Path(__file__).resolve().parent.parent
envio = str(BASE_DIR)
if os.path.isfile(envio+"/PrecoTaxaTesouroDireto.csv") == False:
    wget.download('https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv')
#     lista_arquivos = os.listdir(caminho)
# requests.get('https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv')
#     for arquivo in lista_arquivos:
#         if arquivo == "PrecoTaxaTesouroDireto.csv":
#             os.rename(caminho+arquivo, envio+"/"+arquivo)

def attArquivo(request):
    # caminho = "C:/Users/eriqu/Downloads/"
    # if os.path.isfile(caminho+"PrecoTaxaTesouroDireto.csv") == True:
    #     os.remove(caminho+"PrecoTaxaTesouroDireto.csv")

    if os.path.isfile(envio+"/PrecoTaxaTesouroDireto.csv") == True:
        os.remove(envio+"/PrecoTaxaTesouroDireto.csv")

    # navegador = webdriver.Chrome()
    # navegador.get('https://www.tesourotransparente.gov.br/ckan/dataset/taxas-dos-titulos-ofertados-pelo-tesouro-direto/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1?_gl=1*1yaakk9*_ga*MTYyMTE1MjM0MS4xNjk1NzUxODYw*_ga_95FH8RQ7M0*MTY5NjE5OTE1NS41LjEuMTY5NjE5OTE4Ni4yOS4wLjA')
    # navegador.find_element(By.XPATH, '//*[@id="content"]/div[2]/section/div/div[1]/ul/li/a').click()
    # sleep(5)
    # navegador.quit()
    wget.download('https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv')
    
    # lista_arquivos = os.listdir(caminho)
    
    # for arquivo in lista_arquivos:
    #     if arquivo == "PrecoTaxaTesouroDireto.csv":
    #         os.rename(caminho+arquivo, envio+"/"+arquivo)
    
    return redirect('painel')

arquivo = pd.read_csv('PrecoTaxaTesouroDireto.csv', sep=';')
df = pd.DataFrame(arquivo[(arquivo['Tipo Titulo']=='Tesouro IPCA+') & (arquivo['Data Vencimento']=='15/05/2045')])

df.rename(columns={'Tipo Titulo':'Tipo_Titulo', 'Data Vencimento':'Data_Vencimento', 'Data Base':'Data_Base', 'Taxa Compra Manha':'Taxa_Compra_Manha', 'Taxa Venda Manha':'Taxa_Venda_Manha','PU Compra Manha':'PU_Compra_Manha', 'PU Venda Manha':'PU_Venda_Manha', 'PU Base Manha': 'PU_Base_Manha'}, inplace=True)
df['Taxa_Compra_Manha'] = df['Taxa_Compra_Manha'].str.replace(',','.').astype(float)
df['Taxa_Venda_Manha'] = df['Taxa_Venda_Manha'].str.replace(',','.').astype(float)
df['PU_Base_Manha'] = df['PU_Base_Manha'].str.replace(',','.').astype(float)
df['PU_Compra_Manha'] = df['PU_Compra_Manha'].str.replace(',','.').astype(float)

def painel(request):
    plt.close('all')
    # th = threading.Thread(target=grafico_movel)
    # th.start()
    # th.join()
    # df['Data_Base'] = df['Data_Base'].str.replace('/','-')
    
    df['Data_Base'] = pd.to_datetime(df['Data_Base'], format="%d/%m/%Y")
    df.sort_values(['Data_Base'], inplace=True, ascending=False)
    df['Data_Base'] = df['Data_Base'].dt.strftime('%d/%m/%Y')
    df['Data_Base'] = df['Data_Base'].astype(str)
    # df['Data_Base'] = pd.to_datetime(df['Data_Base'], unit='ns')
    json_records = df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    # print(context)
    
    q1i = round(df['Taxa_Compra_Manha'].quantile(.25),3)
    q1f = round(df['Taxa_Venda_Manha'].quantile(.25),3)
    q1b = round(df['PU_Base_Manha'].quantile(.25),3)
    q2i = round(df['Taxa_Compra_Manha'].quantile(.50),3)
    q2f = round(df['Taxa_Venda_Manha'].quantile(.50),3)
    q2b = round(df['PU_Base_Manha'].quantile(.50),3)
    q3i = round(df['Taxa_Compra_Manha'].quantile(.75),3)
    q3f = round(df['Taxa_Venda_Manha'].quantile(.75),3)
    q3b = round(df['PU_Base_Manha'].quantile(.75),3)
    q4i = round(df['Taxa_Compra_Manha'].quantile(1),3)
    q4f = round(df['Taxa_Venda_Manha'].quantile(1),3)
    q4b = round(df['PU_Base_Manha'].quantile(1),3)

    # print(norm.ppf(0.85, loc=1.25, scale=0.5))
    media_taxa = round(df['Taxa_Compra_Manha'].mean(),3)
    media_pu = round(df['PU_Compra_Manha'].mean(),3)
    desvio_taxa = round(df['Taxa_Compra_Manha'].std(),3)
    desvio_pu = round(df['PU_Compra_Manha'].std(),3)

    inv_taxa = norm.ppf(0.85, media_taxa, desvio_taxa).round(3)
    inv_pu = norm.ppf(0.85, media_pu, desvio_pu).round(3)

    context = {'d':data, 'qnt_linhas':df[df.columns[0]].count(), 'q1i':q1i, 'q1f':q1f, 'q1b':q1b, 'q2i':q2i, 'q2f':q2f, 'q2b':q2b, 'q3i':q3i, 'q3f':q3f, 'q3b':q3b, 'q4i':q4i, 'q4f':q4f, 'q4b':q4b, 'media_taxa':media_taxa, 'media_pu':media_pu, 'desvio_taxa':desvio_taxa, 'desvio_pu':desvio_pu,
    'inv_taxa':inv_taxa, 'inv_pu': inv_pu}

    return render(request, 'painel.html', context)

def grafico_movel(request):
    # matplotlib.use('Agg')
    plt.close('all')
    if request.method == 'POST':
        # matplotlib.use('Agg')
        plt.close('all')
        # if os.path.isfile(envio+"/templates/static/img/imagem.png") == True:
        #     os.remove(envio+"/templates/static/img/imagem.png")
        # if os.path.isfile(envio+"/templates/static/img/imagem2.png") == True:
        #     os.remove(envio+"/templates/static/img/imagem2.png")
        plt.close('all')
        valor_tempo = int(request.POST.get('intervalo_movel'))
        valor_qnt = int(request.POST.get('qnt_movel'))
        df_aux = df.iloc[:(valor_qnt+1)-valor_tempo]
        df_aux['movel_taxa'] = df_aux['Taxa_Compra_Manha'].rolling(valor_tempo).mean()
        df_aux['movel_pu'] = df_aux['PU_Compra_Manha'].rolling(valor_tempo).mean()
        # plt.subplot()
        
        # grafico = df_aux.plot(kind='scatter', x='Data_Base', y='movel_taxa', color='g', figsize=(10,5), title="Taxa Móvel")
        # plt.xlabel('')
        # plt.xticks([])
        # plt.subplot()
        # grafico3 = df_aux.plot(kind='line', x='Data_Base', y='movel_taxa', color='g', figsize=(10,5), title="Taxa Móvel")
        # plt.yscale('log')
        # plt.title('Taxa Móvel')
        # df_aux.plot(kind='line', y='movel_pu', color='k', figsize=(10,5))
        # grafico.set_xticklabels(df_aux.Data_Base, rotation=90)
        # grafico.set_xticks(np.arange(len(df_aux.Data_Base)))
        # ax = df_aux['movel_pu'].plot(secondary_y=True, color='k')
        # plt.subplot(2,1,2)
        # grafico2 = df_aux.plot(kind='scatter', marker='o' , x='Data_Base', y='movel_pu', color='r', figsize=(10,5), title="PU Móvel")
        # add.labels(df_aux['Data_Base'], df_aux['movel_pu'])
        # plt.xlabel('')
        # plt.xticks([])
        matplotlib.use('Agg')
        # plt.draw()
        
        # matplotlib.use('SVG')
        grafico3 = df_aux.plot(kind='line', marker='o' , x='Data_Base', y='movel_taxa', color='g', figsize=(10,5), title="Taxa Móvel")
        # plt.xlabel('')
        # plt.xticks([])
        plt.savefig(envio+'templates/static/img/imagem.png')
        plt.close('all')
        grafico2 = df_aux.plot(kind='line', marker='o' , x='Data_Base', y='movel_pu', color='r', figsize=(10,5), title="PU Móvel")
        # plt.xlabel('')
        # plt.xticks([])
        plt.savefig(envio+'templates/static/img/imagem2.png')
        plt.close('all')
    return redirect('painel', permanent=True)

# th = threading.Thread(target=painel)
# th.start()
# th.join()

# plt.close('all')
# matplotlib.use('Agg')
