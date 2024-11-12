#============================================================================================================
#                    ATIVIDADE FASE 3 - Capítulo 1 - Construindo uma máquina agrícola
#============================================================================================================
#                                      GESTÃO DE DADOS PLANTAÇÃO
#------------------------------------------------------------------------------------------------------------
"""
# Autor.....: Diego Nunes Veiga
# RM........: 560658
# Turma.....: Graduação - 1TIAOR
# Data......: 11/11/2024
# Assunto...: Construindo uma máquina agrícola
# Função....: Realizar a conexão com o banco de dados possibilitando cadastrar, consultar, atualizar e excluir
              dados coletados dos sensores da plantação integrados com o ESP32
"""

#============================================================================================================
#                        INFORMAÇÕES COLETADAS PARA DESENVOLVIMENTO DO SOFTWARE
#============================================================================================================

# O software em Python é responsável por executar as operações CRUD no banco de dados, focando na coleta de dados de
# sensores e de um controlador IoT instalado na área de cultivo. O sistema armazena informações sobre os níveis de
# fósforo e potássio, umidade do solo, pH do solo e o status de funcionamento da bomba d’água. O objetivo é oferecer
# uma solução completa para a extração e armazenamento de dados, conforme proposto na Fase 3 do projeto da startup
# FarmTech Solutions

# Guardaremos os seguintes dados
#   * Data registrada (dd/mm/aaaa) - Utilizado para controle de momento de registro dos dados
#   * Fosforo - nivel do insumo presente no solo, classificado como normal ou baixo
#   * Potássio - nivel do insumo presente no solo, classificado como normal ou baixo
#   * Umidade do solo (%) - quantidade de água presente no solo
#   * pH do solo - nível de pH atual do solo da plantação
#   * Bomba de água - status de funcionamento da bomba de água, classificada como ligada e desligada

# O Software traz alguns benefícios como a interação completa com o banco de dados e recursos como:
#   * Cadastro de novas leituras dos sensores e status da bomba
#   * Atualização de registros existentes no banco de dados
#   * Exclusão de um registro existente no banco de dados
#   * Consulta completa de todos os registros no banco de dados
#   * Limpeza completa do banco de dados

#============================================================================================================
#                                       PROCEDIMENTOS E FUNÇÕES
#============================================================================================================

# Importação dos módulos
import os
import oracledb
import pandas as pd


# Apresentação do software
def Apresentacao():
    print("=" * 80)
    print(" " * 25 + "GESTÃO DE DADOS PLANTAÇÃO")
    print("=" * 80)


# Apresentação do menu inicial
def MenuInicial():
    print("\nSelecione a operação que deseja executar:")
    print(f'''
       1 - Inserir registro
       2 - Atualizar registro
       3 - Excluir registro
       4 - Exibir dados registrados
       5 - Excluir dados registrados
       6 - SAIR''')


# Validação do comando de menu
def ValidaComando(cmd:int) -> int:
    while cmd not in range(1, 7):
        print("Comando inválido!")
        cmd = int(input("Digite novamente o comando:"))
    return cmd


# Cadastro do novo lote no banco de dados
def NovoDado() -> None:
    try:
        print("Preencha os dados para registro no sistema")
        Dt = input("Data registro: ")
        P = input("Fósforo: ")
        K = input("Potássio: ")
        U = float(input("Umidade(%): "))
        pH = float(input("pH do Solo: "))
        Ba = input("Bomba de água: ")
        bd_comando.execute(f""" INSERT INTO plantacao (dataregistro,fosforo,potassio,umidade,phsolo,bomba)
                                VALUES ('{Dt}','{P}','{K}','{U}','{pH}','{Ba}') """)
        conn.commit()
        print("\nOs dados foram armazenados...\n")

    except ValueError:
        print("\nA variável não é numérica\n")
    except:
        print("\nErro de transferência de dados\n")



# Procura lote para realizar a atualização
def ProcuraDado() -> int:
    try:
        lista = []
        cmd = int(input("Qual registro deseja buscar?:"))
        bd_comando.execute("SELECT * FROM plantacao WHERE id = {}".format(cmd))
        data = bd_comando.fetchall()

        for dt in data:
            lista.append(dt)

        if len(lista) == 0: # se não há o id
            print("\nNenhum registro encontrado!\n")
            cmd = -1
        else:
            print("\nArquivo de Registro...: {} existente\n".format(cmd))

    except:
        print("\nErro de transferência de dados\n")
        cmd = -1
    return cmd


# Atualiza lote existente
def AtualizaDado(registro: int) -> None:
    try:
        print("Preencha os dados para atualizar no sistema")
        Dt = input("Data registro: ")
        P = input("Fósforo: ")
        K = input("Potássio: ")
        U = float(input("Umidade(%): "))
        pH = float(input("pH do Solo: "))
        Ba = input("Bomba de água: ")

        bd_comando.execute(f"UPDATE plantacao SET dataregistro='{Dt}', fosforo='{P}', potassio='{K}', umidade='{U}', phsolo='{pH}', bomba='{Ba}' WHERE id = '{registro}'")
        conn.commit()
        print("\nOs dados foram atualizados...\n")

    except ValueError:
        print("A variável não é numérica\n")


# Comando para excluir lote
def ExcluiDado(registro: int) -> None:
    try:
        bd_comando.execute(f"DELETE FROM plantacao WHERE id ='{registro}'")
        conn.commit()
        print("\nO registro foi apagado\n")

    except:
        print("\nErro de transferência de dados\n")


# Apresenta lista de todos os lotes registrados
def ListaCompleta() -> None:
    lista = []
    bd_comando.execute('SELECT * FROM plantacao')
    tabela = bd_comando.fetchall()

    for dt in tabela:
        lista.append(dt)

    # ordena a lista
    lista = sorted(lista)

    # Formatação para apresentar todas a tabela sem exceção
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', None)

    # Gera um DataFrame com os dados da lista utilizando o Pandas
    DadosFormatados = pd.DataFrame.from_records(lista, columns=["ID","Data registro","Fósforo","Potássio","Umidade(%)","pH Solo","Bomba água"], index='ID')

    if DadosFormatados.empty:
        print("Nenhum registro encontrado!\n")
    else:
        print(DadosFormatados)


# Exclui todos os registros existentes no banco de dados
def ExcluiCompleto() -> None:
    print("!!!!! O COMANDO IRA EXCLUIR SEU BANCO DE DAODOS POR COMPLETO !!!!!")
    cmd = input("Confirma a exclusão? [S]im ou [N]ÃO?")

    if cmd.upper() == "S":
        bd_comando.execute("DELETE FROM plantacao")
        conn.commit()
        bd_comando.execute(" ALTER TABLE plantacao MODIFY(ID GENERATED AS IDENTITY (START WITH 1)) ")
        conn.commit()
        print("\nTodos os registros foram excluídos!\n")

    else:
        print("\nOperação cancelada!\n")


#============================================================================================================
#                                          PROGRAMA PRINCIPAL
#============================================================================================================

#Usuário para acessar o banco de dados
user = "RM560658"
password = "010199"
server = 'oracle.fiap.com.br:1521/ORCL'


#----------------------------------------------------------------------------------------------------------


# Realiza conexão com o servidor do banco de dados
try:
    conn = oracledb.connect(user=user, password=password, dsn=server)
    bd_comando = conn.cursor()

except Exception as e:
    print("Erro: ", e)
    conexao = False
else:
     conexao = True

# Execução do Menu enquanto não for solicitado encerramento
while conexao:

    # Limpa terminal operacional
    os.system('cls')

    # Apresentação do menu de interação
    Apresentacao()
    MenuInicial()

    # Entrada do comando de navegação e validação
    try:
        comando = int(input("\nDigite o comando:"))
        menu = ValidaComando(comando)
    except ValueError:
        print("A variável digitada não é numérica")
    else:

        #Limpa terminal operacional
        os.system('cls')

        # Escolha do menu conforme comando
        match menu:

            # ================================ Inserir lote ========================================
            case 1:
                print("----- INSERE NOVO DADO -----\n")
                NovoDado()

            # =============================== Atualizar lote =======================================
            case 2:
                print("----- ATUALIZA DADO -----\n")
                busca1 = ProcuraDado()
                if busca1 != -1:
                    AtualizaDado(busca1)

            # ================================= Excluir lote =======================================
            case 3:
                print("----- EXCLUIR DADO -----\n")
                busca2 = ProcuraDado()
                if busca2 != -1:
                    ExcluiDado(busca2)

            # =========================== Exibir lotes registrados =================================
            case 4:
                print("----- EXIBIR DADOS REGISTRADOS -----\n")
                ListaCompleta()

            # ========================== Excluir lotes registrados =================================
            case 5:
                print("----- EXCLUIR DADOS REGISTRADOS -----\n")
                ExcluiCompleto()

            # ============================== Sair do programa ======================================
            case 6:
                print("\nEncerrando a interface de usuário...até a proxima!")
                conexao = False

    if conexao:
        #Pausa para verificação dos comandos
        input("Pressione ENTER")