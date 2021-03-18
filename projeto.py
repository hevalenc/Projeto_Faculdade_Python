"""
Importei os módulos 'CSV', para gerar os comandos de escrita e leitura de arquivos CSV,  e 'DATETIME' para cadastrar
a data de locação dos filmes
"""

import csv
from datetime import datetime, date

"""
Criei a função 'CRIAR_DB' para simplificar a programação e criar os arquivos necessários para salvar as informações
dos clientes, dos filmes e dos empréstimos, desta forma evita a gravação de cabeçalhos toda vez que for gravar novas
informações nos arquivos.
"""

def criar_db():
    with open('clientes.csv', 'w', newline='') as clientes:
        fieldnames = ['Nome' , 'RG' , 'CPF']
        dict_writer = csv.DictWriter(clientes, fieldnames=fieldnames, delimiter=';', lineterminator= '\r')
        dict_writer.writeheader()

    with open('filmes.csv', 'w', newline='') as filmes:
        fieldnames = ['Código', 'Tipo', 'Título', 'Lançamento']
        dict_writer = csv.DictWriter(filmes, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
        dict_writer.writeheader()

    with open('emprestimos.csv', 'w', newline='') as emprestimos:
        fieldnames = ['CPF', 'Nome', 'Título', 'Empréstimo', 'Situação', 'Dias']
        dict_writer = csv.DictWriter(emprestimos, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
        dict_writer.writeheader()

"""
Criei a função 'CADASTRO_CLIENTE' para simplificar a programação e permitir cadastrar novos clientes e gravar as
informações no arquivo 'clientes.csv' sem sobregravar os dados já existentes. Utilizei o DictWriter para permitir
gravar as informações em uma tabela que pode ser visualizado no Excel.
"""

def cadastro_cliente():
    nome = input('Cadastre o nome do cliente: ')
    print('Cadastrar o CPF e o RG sem os separadores "." e "-"')
    cpf = input('Cadastre o CPF: ')
    cpf_contador = len(cpf)

    """
    Criei um verificador do tamanho do CPF e do RG digitados para estabelecer um padrão, para isto usei o comando 'len'
    """

    while cpf_contador != 11:
        cpf = input('Você digitou o CPF incorreto. Cadastre novamente: ')
        cpf_contador = len(cpf)
    rg = input('Cadastre o RG: ')
    rg_contador = len(rg)
    while rg_contador != 9:
        rg = input('Você digitou o RG incorreto. Cadastre novamente: ')
        rg_contador = len(rg)
    lista_clientes = {'Nome': nome, 'RG' : rg, 'CPF' : cpf}

    with open('clientes.csv', 'a', newline='') as clientes:
        dict_writer = csv.DictWriter(clientes, fieldnames=lista_clientes.keys(), delimiter=';', lineterminator= '\n')
        dict_writer.writerow(lista_clientes)

"""
Criei a função 'CONSULTA_CLIENTE' para simplificar a programação e acessar os dados gravados para imprimi-los na tela
em forma de dicionários.
"""

def consulta_cliente():
    with open('clientes.csv','r') as clientes:
        reader = csv.DictReader(clientes, delimiter=';')
        for row in reader:
            print(row)

"""
Criei a função 'CADASTRO_FILME' para simplificar a programação e permitir cadastrar novos filmes e gravar as
informações no arquivo 'filmes.csv' sem sobregravar os dados já existentes. Utilizei o DictWriter para permitir
gravar as informações em uma tabela que pode ser visualizado no Excel.
"""

def cadastro_filme():
    codigo = input('Cadastre um novo código numérico: ')
    tipo = input('Este filme é "VHS" ou "DVD": ')
    titulo = input('Qual é o nome do Filme: ')
    lancamento = input('Ano de lançamento: ')
    lista_filmes = {'Código' : codigo , 'Tipo' : tipo, 'Título' : titulo, 'Lançamento' : lancamento}

    with open('filmes.csv', 'a', newline='') as filmes:
        dict_writer = csv.DictWriter(filmes, fieldnames=lista_filmes.keys(), delimiter=';', lineterminator='\n')
        dict_writer.writerow(lista_filmes)

"""
Criei a função 'CONSULTA_FILME' para simplificar a programação e acessar os dados gravados para imprimi-los na tela
em forma de dicionários.
"""

def consulta_filme():
    with open('filmes.csv','r') as filmes:
        reader = csv.DictReader(filmes, delimiter=';')
        for row in reader:
            print(row)

"""
Criei a função 'CADASTRO_EMPRÉSTIMO' para simplificar a programação e permitir cadastrar novas locações de filmes e
gravar as informações no arquivo 'emprestimos.csv' sem sobregravar os dados já existentes. Utilizei o DictWriter para
permitir gravar as informações em uma tabela que pode ser visualizado no Excel.
"""

def cadastro_emprestimo():

    """
    Criei dois dicionários vazios para receber os dados necessários dos arquivos 'clientes.csv' e 'filmes.csv' para
    permitir a manipulação dos dados para gerar os comandos para registro de empréstimos.
    """

    clientes_convertido = {}
    filmes_convertido = {}

    with open('clientes.csv') as clientes:
        reader = csv.DictReader(clientes, delimiter=';')
        for row in reader:
            nome1 = row['Nome']
            cpf1 = row['CPF']
            convertido = {nome1:cpf1}
            clientes_convertido.update(convertido)
    with open('filmes.csv') as filmes:
        reader = csv.DictReader(filmes, delimiter=';')
        for row in reader:
            codigo1 = row['Código']
            titulo1 = row['Título']
            convertido1 = {codigo1:titulo1}
            filmes_convertido.update(convertido1)

    """
    Criei um comando para verificar se o 'cliente' e o 'código do filme' digitados constam nos respectivos arquivos CSV
    """

    nome = input('Digite o nome do cliente: ')
    while nome not in clientes_convertido.keys():
        nome = input('Cliente inexistente. \n => Digite novamente: ')
    for k,v in clientes_convertido.items():
        if nome == k:
            cpf = v
    codigo = input('Digite o código do filme: ')
    while codigo not in filmes_convertido.keys():
        codigo = input('Código inexistente. \n => Digite novamente: ')
    for k,v in filmes_convertido.items():
        if codigo == k:
            titulo = v

    """
    Utilizei a função Datetime para permitir formatar a entrada de datas e fazer o cálculo entre a data de locação e a
    data atual, gerando a diferença de dias para verificação de 'atrasos' na devolução.
    """

    data_loc = input('Digite a data de locação (dd/mm/aa): ')
    data_convertida = datetime.strptime(data_loc, '%d/%m/%y')
    data_atual = date.today()
    data_dif = data_atual - data_convertida.date()
    if data_dif.days >= 7:
        situacao = 'Atrasado'
    else:
        situacao = 'Em dia'
    lista_emprestimo = {'CPF' : cpf, 'Nome' : nome, 'Título' : titulo, 'Empréstimo' : data_loc, 'Situação' : situacao, 'Dias' : data_dif.days}

    with open('emprestimos.csv', 'a', newline='') as emprestimos:
        dict_writer = csv.DictWriter(emprestimos, fieldnames=lista_emprestimo.keys(), delimiter=';', lineterminator= '\n')
        dict_writer.writerow(lista_emprestimo)

"""
Criei a função 'CONSULTA_EMPRESTIMO' para simplificar a programação e acessar os dados gravados para imprimi-los na tela
em forma de dicionários.
"""

def consulta_emprestimo():
    with open('emprestimos.csv','r') as emprestimo:
        reader = csv.DictReader(emprestimo, delimiter=';')
        for row in reader:
            print(row)

"""
Criei um laço infinito com o comando 'while' para permitir a navegação entre as funções sem ocorrer a finalização do
programa e retornando sempre para a página principal. Para finalizar o programa será necessário acessar a última linha
de comando do laço, que é a opção 'sair'.
"""

while True:
    print('*** Locadora de Filmes ACME ***')
    print('\nMenu:'
          '\n1 - Criar banco de dados'
          '\n2 - Cadastro de clientes'
          '\n3 - Cadastro de filmes'
          '\n4 - Cadastro de empréstimos'
          '\n5 - Consulta'
          '\n6 - Sair\n')

    selecao = int(input('Digite a opção desejada: '))

    if selecao == 1:
        criar_db()
        print('\nArquivos criados!!\n')

    if selecao == 2:
        print('\n*** Cadastro de Clientes ***\n')
        cadastro_cliente()

    elif selecao == 3:
        print('\n*** Cadastro de Filmes ***\n')
        cadastro_filme()

    elif selecao == 4:
        print('\n*** Cadastro de Empréstimo de Filmes ***\n')
        cadastro_emprestimo()

    elif selecao == 5:
        print('\n*** Consulta de arquivos ***\n')
        print('Cadastro dos Clientes:')
        consulta_cliente()
        print('\nCadastro dos Filmes:')
        consulta_filme()
        print('\nCadastro de Locação:')
        consulta_emprestimo()

    elif selecao == 6:
        print('Fim do programa.')
        break
