ARQUIVO_DE_DADOS="insumos.json"

ESTOQUE = []
DISTRIBUICAO_ESTADOS = []
ULTIMO_CODIGO = 0;

def cadastrar_insumos():
    global ULTIMO_CODIGO

    print("Cadastro de Insumos\nDigite as informações do Insumo:\n")

    while(True):
        tipo_item = input("Informe o tipo do item: \n1 - Vacina\n2 - Medicamento, \n3 - EPI\n").lower()
        if(tipo_item in ["1","2","3", "vacina", "epi", "medicamento"]):
            limpar_tela()
            break
        print("Tipo de Item Inválido\n")   
    
    # DEFINIÇÕES DOS TIPOS
    ATRIBUTOS = [
        "Nome",
        "Valor Unitario",
        "Quantidade",
        "Data de Vencimento",
        "Nome do fabricante"]

    novo_item = {}

    novo_item['Código'] = ULTIMO_CODIGO +1

    if(tipo_item in ["1","vacina"]):
        ATRIBUTOS += [
        "Tipo de Vacina",
        "Quantidade de doses",
        "Intervalo entre doses (em dias)"
        ]

        novo_item["Tipo"] = "Vacina"
    
    elif(tipo_item in ["2", "medicamento"]):
        ATRIBUTOS +=  [
        "Dosagem",
        "Forma de administração",
        "Forma de disponibilização"]

        novo_item["Tipo"] = "Medicamento"

    elif(tipo_item) in ["3","epi"]:
        ATRIBUTOS += ["Tipo de EPI","Descrição"]
        novo_item["Tipo"] = "EPI"
    print("\n")

    print(f"Cadastrando {novo_item['Tipo']}")



    for chave in ATRIBUTOS:
        novo_item[chave] = input(f"{chave}: ");
        #TODO: checar se quantidade é um número e validar as informações
    
    
    ULTIMO_CODIGO += 1
    ESTOQUE.append(novo_item);
    print(f"Item de Código {len(ESTOQUE)} Cadastrado com Sucesso")
    enter_para_prosseguir()


def consultar_insumos_estoque():
    print("CONSULTA DE INSUMOS NO ESTOQUE\n")
    if(not existem_insumos_cadastrados_no_estoque()):
        enter_para_prosseguir()
        return False
    
    print(f"Total de Itens no estoque: {len(ESTOQUE)}")
    for item in ESTOQUE:
        print(f"Cód:{item['Código']} - Tipo: {item['Tipo']} - Item: {item['Nome']} - Qtd:{item['Quantidade']} ")
    enter_para_prosseguir()

def consultar_detalhes_insumos_estoque():
    print(f"CONSULTA DE DETALHES DE INSUMOS NO ESTOQUE")
    if(not existem_insumos_cadastrados_no_estoque()):
        enter_para_prosseguir()
        return False

    while(True):
        try:
            cod = int(input("Digite o código do insumo: "))
            item = ESTOQUE[cod]
            break
            
        except:
            print("\ncódigo inválido, tente novamente digitando um código válido")
            enter_para_prosseguir()
            return False

    print("\nINFORMAÇÕES DO ITEM SELECIONADO:\n")
    for k in item:
        print(f"{k}:{item[k]}");

    enter_para_prosseguir();


def consultar_insumos_estoque_por_tipo():
    while(True):
        tipo_item = input("Informe o tipo do item: \n1 - Vacina\n2 - Medicamento, \n3 - EPI\n").lower()
        if(tipo_item in ["1","2","3", "vacina", "epi", "medicamento"]):
            limpar_tela()
            break
        print("Tipo de Item Inválido\n")

    if(tipo_item in ["1","vacina"]):
        tipo = "Vacina"
    elif(tipo_item in ["2", "medicamento"]):
        tipo = "medicamento"
    elif(tipo_item) in ["3","epi"]:
        tipo = "EPI"

    itens = [i for i in ESTOQUE if i["Tipo"] == tipo]

    if(not itens):
        print(f"não existem itens do tipo {tipo} cadastrados no estoque")
        enter_para_prosseguir()
        return False
    print(f"Existem {len(itens)} itens do tipo {tipo}:")

    for item in itens:
        print(f"Cód:{item['Código']} - Tipo: {item['Tipo']} - Item: {item['Nome']} - Qtd:{item['Quantidade']} ")
    enter_para_prosseguir()

def distribuir_insumos_para_estado():
    limpar_tela()
    print("Distribuir Insumos para Estado:")
    while(True):
        try:
            cod_item = int(input("Digite o código do item:"))
            indice_item = encontrar_item_no_estoque(cod_item)
            item = ESTOQUE[indice_item]
            break
        except:
            print("código do item não é um número ou não existe")
    
    print("você deseja distribuir o item:\n")
    print(f"Cód:{item['Código']} - Tipo: {item['Tipo']} - Item: {item['Nome']} - Qtd:{item['Quantidade']} ")
    
    while(True):
        qtd = int(input("quantos deste item você deseja distribuir?"))
        if(item['Quantidade'] - qtd < 0 ):
            print("não de pode remover mais itens do que o disponível")
            continue;
        break;
    
    estado = input("Para qual estado será distribuido ")
    # remover do estoque.
    ESTOQUE[indice_item]["Quantidade"] -= qtd
    # adicionar no estado
    try:
        indice_item_no_estado = encontrar_item_no_estado(estado, cod_item)
        DISTRIBUICAO_ESTADOS[estado][indice_item_no_estado]['Quantidade'] += qtd
    except:
        adicionar_item_no_estado(estado, item)


def adicionar_item_no_estado(estado, item):
    DISTRIBUICAO_ESTADOS[estado].append(item)

def encontrar_item_no_estado(estado, cod):
    try:
        indice = [i for i in range(len(DISTRIBUICAO_ESTADOS[estado])) if DISTRIBUICAO_ESTADOS[estado][i]['Código'] == cod]
        return indice[0] if indice else 9999999
    except: 
        return false;
    
def encontrar_item_no_estoque(cod):
    indice = [i for i in range(len(ESTOQUE)) if ESTOQUE[i]['Código'] == cod]
    return indice[0] if indice else False

def existem_insumos_cadastrados_no_estoque():
    if(ESTOQUE):
        return True
    print("Não existem insumos cadastrados no estoque")
    return False;

def enter_para_prosseguir():
    input("\nPressione enter para prosseguir...")
    limpar_tela()

def limpar_tela():
    import os   
    os.system('cls' if os.name == 'nt' else 'clear')


def salvar():
    import json
    with open(ARQUIVO_DE_DADOS, 'w') as arquivo:
        dados = {"ESTOQUE": ESTOQUE, "DISTRIBUICAO_ESTADOS":DISTRIBUICAO_ESTADOS, "ULTIMO_CODIGO":ULTIMO_CODIGO}

        json.dump(dados,arquivo)
        print("dados salvos com sucesso! \n")
        enter_para_prosseguir()

def carregar():
    import json
    global ESTOQUE
    global DISTRIBUICAO_ESTADOS
    global ULTIMO_CODIGO
    try:
        with open(ARQUIVO_DE_DADOS, 'r') as arquivo:
            dados = json.load(arquivo)
            ESTOQUE = dados["ESTOQUE"]
            DISTRIBUICAO_ESTADOS = dados["DISTRIBUICAO_ESTADOS"]
            ULTIMO_CODIGO = dados["ULTIMO_CODIGO"]
            print("dados cerregados com sucesso! \n")
    except:
        pass

def sair():
    import sys;
    limpar_tela()

    salve = input("Deseja salvar as alterações no banco de dados? (S/N)")
    if(salve in ['s','S']):
        salvar()
    print("\n\nObrigado por usar o SISGI!\n\n")
    sys.exit()



def menu():
    while(True):
        limpar_tela()
        print("\n\nSISGI - SISTEMA DE GERÊNCIA DE INSUMOS")
        op = input(\
        """\n\nEscolha uma Opção:
        1 - Cadastrar insumo.
        2 - Consultar insumos disponíveis no estoque.
        3 - Consultar detalhes dos insumos disponíveis.
        4 - Consultar insumos no estoque por tipo.
        5 - Consultar insumos distribuidos por estado.
        6 - Consultar descrição dos insumos distribuidos para os estados.
        7 - Consultar todos os insumos distribuidos para estados por tipo.
        8 - Consultar todos os insumos distribuidos para um estado específico.
        9 - Entregar/Distribuir Insumos do estoque para um estado.
        10 - Salvar Alterações
        11 - Sair
        ->""")
        OPCOES = {
            "1": cadastrar_insumos,
            "2": consultar_insumos_estoque,
            "3": consultar_detalhes_insumos_estoque,
            "4": consultar_insumos_estoque_por_tipo,
            "9": distribuir_insumos_para_estado,
            "10": salvar,
            "11": sair,
        }
        if(op in OPCOES):
            limpar_tela()
            OPCOES[op]();
        else:
            print("Opção Inválida")

if __name__ == '__main__':
    carregar()
    menu()