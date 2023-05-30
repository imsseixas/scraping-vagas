#Codigo completo - Ítalo Matheus Souza Seixas
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import re

# Atualizar o webdriver automaticamente
servico = Service(ChromeDriverManager().install())

# Define a URL da página de busca de vagas
URL_BUSCA_VAGAS = 'https://www.linkedin.com/jobs/search?keywords=agro&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

# Acessa a página de busca de vagas
navegador = webdriver.Chrome(service=servico)
navegador.get(URL_BUSCA_VAGAS)
navegador.maximize_window()

# Espera a página de resultados de busca carregar completamente
time.sleep(5)


# Desce a barra de rolagem até o final da página para carregar mais vagas
while True:
    # Salva a posição atual da barra de rolagem
    posicao_atual = navegador.execute_script('return window.pageYOffset;')

    # Desce a barra de rolagem para o final da página
    navegador.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    # Aguarda um tempo para o conteúdo adicional ser carregado
    time.sleep(2)

    # Verifica se a barra de rolagem não se moveu mais
    nova_posicao = navegador.execute_script('return window.pageYOffset;')
    if nova_posicao == posicao_atual:
        try:
            navegador.find_element(By.XPATH,'//*[@id="main-content"]/section[2]/button').click()
        except:
            break

# Abre o arquivo CSV em modo de escrita e escreve o cabeçalho
with open('vagas.csv', mode='w', newline='') as arquivo_csv:
    cabecalho = ['URL da vaga', 'Nome da vaga', 'Nome da Empresa Contratante', 'URL da empresa contratante', 'Modelo de contratação', 'Tipo de contratação', 'Nível de experiência',
                'Número de candidaturas para vaga', 'Data da postagem da vaga', 'Horário do scraping', 'Número de funcionários da empresa', 'Número de seguidores da empresa', 'Local sede da empresa', 'Site da empresa', 'Sobre nós', 
                'URL da candidatura']
    escritor_csv = csv.writer(arquivo_csv)
    escritor_csv.writerow(cabecalho)

    # Define a janela que deve permanecer aberta durante o processo
    primeira_guia = navegador.current_window_handle

    # Percorre todas as vagas encontradas na página
    vagas = navegador.find_elements(By.XPATH, '//*[@id="main-content"]/section[2]/ul/li[position()]/div/a')
    
    # Extrai as informações da vaga
    for vaga in vagas:
        if vaga.get_attribute('href') is not None:
            pagina = vaga.get_attribute('href')
            navegador.execute_script("window.open(arguments[0], '_blank');", pagina)
            time.sleep(1)
            navegador.switch_to.window(navegador.window_handles[-1])
            time.sleep(5)

            # Extrai as informações da pagina da vaga que não precisam ser verificadas se existem
            link_vaga = navegador.current_url
            
            nome_da_vaga = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h1').text

            nome_empresa = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a').text
            
            tipo_contratacao = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[2]/span').text
            
            nivel_contratacao = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[1]/span').text
            
            data_postagem = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[1]').text
            
            url_candidatura = navegador.find_element(By.XPATH,'//*[@id="teriary-cta-container"]/div/a').get_attribute('href')

            # Extrai as informações da pagina da vaga que nem sempre aparecem
            try:
                url_da_empresa = navegador.find_element(By.XPATH,'//*[@id="teriary-cta-container"]/div/a').get_attribute('href')
            except:
                url_da_empresa = 'Não possui'
            
            try:
                 modelo_contratacao = navegador.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[1]/span[1]/span[3]').text
            except:
                modelo_contratacao = 'Não possui modelo de contratação sem logar em uma conta'

            try:
                candidaturas = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[2]').text
            except:
                candidaturas = 'Não possui o número de candidaturas'
            
            # Abre a pagina da empresa
            navegador.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a').click()
            time.sleep(3)
            navegador.switch_to.window(navegador.window_handles[2])
            navegador.switch_to.active_element.send_keys(Keys.ESCAPE)
            time.sleep(1)

            # Função para tratar a string com informação de funcionarios
            try:
                numero_de_funcionarios_bruto = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/section/div/div[2]/div[2]/ul/li/div/a').text
                extracao_numero_funcionarios = re.findall(r'\d+', numero_de_funcionarios_bruto)
                numero_funcionarios = ".".join(extracao_numero_funcionarios)
            except:
                numero_funcionarios = 'Não possui o número de funcionários'
            # Função para tratar a string com informação do local e a quantidade de seguidores
            try:
                local_sede_e_numero_seguidores = navegador.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/section/div/div[2]/div[1]/h3').text
                local_sede_bruto = re.findall(r'\D+', local_sede_e_numero_seguidores)
                local_sede = local_sede_bruto[0]
                numero_seguidores = re.findall(r'\d+', local_sede_e_numero_seguidores)
                numero_seguidores = ".".join(numero_seguidores)
            except:
                local_sede_e_numero_seguidores = 'Não possui o local da sede da empresa'

            #Variavel para determinar a hora do sistema
            agora = datetime.now()
            dia_hora = agora.strftime("%m/%d/%y %H:%M")

            # Escreve as informações da vaga no arquivo CSV
            linha = [link_vaga, nome_da_vaga, nome_empresa, url_da_empresa, modelo_contratacao, tipo_contratacao, nivel_contratacao, candidaturas, data_postagem, dia_hora, numero_funcionarios,numero_seguidores,local_sede, url_candidatura]
            escritor_csv.writerow(linha)

            # Fecha as guias exessivas gerada pela automação
            guias = navegador.window_handles
            for guia in guias:
                if guia != primeira_guia:
                    navegador.switch_to.window(guia)
                    navegador.close()
            navegador.switch_to.window(primeira_guia)
            
            # 60 segundos para fazer a proxima request pois o site estava bloqueando as solicitações
            time.sleep(60)


# Fecha o navegador
navegador.quit()
