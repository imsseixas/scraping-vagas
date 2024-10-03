Web Scraping de Vagas no LinkedIn usando Python
Este repositório contém um código de automação desenvolvido como parte de um teste para uma vaga de emprego. Ele utiliza Python e a biblioteca Selenium para realizar web scraping de vagas de emprego no LinkedIn, extraindo informações relevantes como:

Nome da vaga
Nome da empresa contratante
Tipo e modelo de contratação
Nível de experiência exigido
Número de candidaturas
Data da postagem
Local sede da empresa
Número de funcionários e seguidores
URL da vaga e da empresa
URL para candidatura
Funcionamento do Script
O script percorre todas as vagas disponíveis em uma página específica do LinkedIn, coleta os dados, e os salva em um arquivo CSV. Ele também navega até as páginas de cada empresa associada às vagas para capturar detalhes adicionais.

Tecnologias Utilizadas:
Python
Selenium para automação do navegador
CSV para salvar os dados extraídos
WebDriver Manager para gerenciar o ChromeDriver
Observações:
O script faz pausas programadas para evitar bloqueios do site devido ao excesso de requisições.
O scraping foi configurado para extrair o máximo de dados possíveis sem precisar logar em uma conta do LinkedIn.
