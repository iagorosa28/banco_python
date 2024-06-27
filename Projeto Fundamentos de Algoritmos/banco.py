#Iago Rosa de Oliveira - 24123056 4
#Humberto de Oliveira Pellegrini - 24123065 5

from datetime import datetime
import json
import os

clientes = dict()

if os.path.isfile("clientes.json"):    
    with open("clientes.json", "r") as f:
        if os.path.getsize("clientes.json") > 0:
            clientes = json.load(f)

#data pro extrato
data = datetime.now()
data_str= f"Data: {data.year:04d}/{data.month:02d}/{data.day:02d} {data.hour:02d}:{data.minute:02d}"

def novo_cliente():   

    #verificando o cnpj
    cnpj = int(input("Digite o CNPJ: "))
    cnpj = str(cnpj)
    if cnpj in clientes:
        print("CNPJ ja existente!")
    else:
        #recebendo os dados do cliente
        nome = input("Digite a razao social: ")
        tipo_conta = input("Digite o tipo de conta: ")
        while tipo_conta != "comum" and tipo_conta != "plus":
            tipo_conta = input("Escolha entre comum ou plus: ")
        valor_inicial = float(input("Digite o valor inicial da conta: "))
        senha = int(input("Digite a senha da conta: "))
    
        tarifa = 0
    
        eventos = []
        pagamentos_automaticos = []
    
        #armazenando os dados do cliente
        cliente = [nome, tipo_conta, valor_inicial, senha, eventos, pagamentos_automaticos]
        clientes[cnpj] = cliente
    
        #marcando o extrato
        extrato = f"{data_str}; + {valor_inicial:.2f}; Tarifa:{tarifa: .2f}; Saldo:{valor_inicial: .2f}"
        clientes[cnpj][4].append(extrato)

        print("Cliente cadastrado!")

def apaga_cliente():
    
    #analisando o cnpj do cliente
    cnpj = input("Para apagar a conta digite o CNPJ dela: ")
    if cnpj in clientes:
        #apagando o cliente
        del clientes[cnpj]
        print("A conta do CNPJ %s foi apagada" % cnpj)
    else:
        print("CNPJ invalido!")

def listar_clientes():
    
    #Listando todos os clientes e seus dados
    for cnpj, cliente in clientes.items():
        print("CNPJ: %s / Razao social: %s / Tipo conta: %s / Verba: R$ %.2f / Senha: %s / Debito automatico: %s" % (cnpj,cliente[0],cliente[1],cliente[2],cliente[3],cliente[5]))

def debito():
    
    #analisando o cnpj e a senha do cliente
    cnpj = input("Digite o CNPJ: ")
    senha = int(input("Digite a senha: "))
    cliente = clientes.get(cnpj)
    if cliente is None:
        print("CNPJ invalido!")
    else:
        if senha == cliente[3]:
            #debitando o valor
            valor_debito = float(input("Digite o valor a ser debitado: "))
            #analisando o tipo de cliente
            #cliente comum
            if cliente[1] == "comum" and cliente[2] - valor_debito*1.05 >= -1000:
                cliente[2] = cliente[2] - valor_debito*1.05
                print("Debitado na conta do CNPJ %s o valor de R$ %.2f" % (cnpj, valor_debito))
                print("Novo saldo da conta: R$ %.2f" % cliente[2])
                #armazenando operacoes no extrato
                tarifa = valor_debito*0.05
                saldo = cliente[2]
                extrato = f"{data_str}; - {valor_debito:.2f}; Tarifa:{tarifa: .2f}; Saldo:{saldo: .2f}"
                clientes[cnpj][4].append(extrato)
            #cliente plus
            elif cliente[1] == "plus" and cliente[2] - valor_debito*1.03 >= -5000:
                cliente[2] = cliente[2] - valor_debito*1.03
                print("Debitado na conta do CNPJ %s o valor de R$ %.2f" % (cnpj, valor_debito))
                print("Novo saldo da conta: R$ %.2f" % cliente[2])
                #armazenando operacoes no extrato
                tarifa = valor_debito*0.03
                saldo = cliente[2]
                extrato = f"{data_str}; - {valor_debito:.2f}; Tarifa:{tarifa: .2f}; Saldo:{saldo: .2f}"
                clientes[cnpj][4].append(extrato)
            else:
                print("Saldo insuficiente!")
        else:
            print("Senha invalido!")

def deposito():
    
    #analisando o cnpj do cliente
    cnpj = input("Digite o CNPJ para depositar: ")
    cliente = clientes.get(cnpj)
    if cliente is None:
        print("CNPJ invalido!")
    else:
        #depositando o valor na conta do cliente
        valor_deposito = float(input("Digite o valor a ser depositado: "))
        cliente[2] = cliente[2] + valor_deposito
        print("Deposito de R$ %.2f na conta do CNPJ %s" % (valor_deposito, cnpj))
        print("Novo saldo da conta: R$ %.2f" % cliente[2])
        #armazenando operacoes no extrato
        tarifa = 0
        saldo = cliente[2]
        extrato = f"{data_str}; + {valor_deposito:.2f}; Tarifa:{tarifa: .2f}; Saldo:{saldo: .2f}"
        clientes[cnpj][4].append(extrato)

def extrato():
    
    #analisando o cnpj e a senha
    cnpj = input("Digite o CNPJ para tirar o extrato: ")
    senha = int(input("Digite a senha: "))
    cliente = clientes.get(cnpj)
    extrato = cliente[4]
    if cliente is None:
        print("CNPJ invalido!")
    else:
        if senha == cliente[3]:
            #mostrando o extrato da conta
            print("Nome: ",clientes[cnpj][0])
            print("CNPJ: ",cnpj)
            print("Tipo de conta: ",clientes[cnpj][1])
            for dados in extrato:
                print(dados)
        else:
            print("Senha invalido!")

def transferencia():
    
    #recebendo e analisando os cnpjs e a senha
    cnpj_origem = input("Digite o CNPJ de origem: ")
    senha = int(input("Digite a senha: "))
    cnpj_destino = input("Digite o CNPJ de destino: ")
    cliente = clientes.get(cnpj_origem)
    if cliente is None:
        print("CNPJ origem invalido!")
    else:
        if senha == cliente[3]:
            cliente2 = clientes.get(cnpj_destino)
            if cliente2 is None:
                print("CNPJ destino invalido!")
            else:
                #recebendo o valor da transferencia, debitando da conta origem e depositando na conta destino
                valor_transferencia = float(input("Digite o valor da transferancia: "))
                #analisando o tipo de cliente da conta origem
                #conta de origem comum
                if cliente[1] == "comum" and cliente[2] - valor_transferencia*1.05 >= -1000:
                    cliente[2] = cliente[2] - valor_transferencia*1.05
                    cliente2[2] = cliente2[2] + valor_transferencia
                    print("Transferancia de R$ %.2f do CNPJ %s para o CNPJ %s" % (valor_transferencia, cnpj_origem, cnpj_destino))
                    #armazenando operacoes no extrato
                    tarifa_origem = valor_transferencia*0.05
                    saldo_origem = cliente[2]
                    extrato_origem = f"{data_str}; - {valor_transferencia:.2f}; Tarifa:{tarifa_origem: .2f}; Saldo:{saldo_origem: .2f}"
                    clientes[cnpj_origem][4].append(extrato_origem)
                    tarifa_destino = 0
                    saldo_destino = cliente2[2]
                    extrato_destino = f"{data_str}; + {valor_transferencia:.2f}; Tarifa:{tarifa_destino: .2f}; Saldo:{saldo_destino: .2f}"
                    clientes[cnpj_destino][4].append(extrato_destino)
                #conta de origem plus
                elif cliente[1] == "plus" and cliente[2] - valor_transferencia*1.03 >= -5000:
                    cliente[2] = cliente[2] - valor_transferencia*1.03
                    cliente2[2] = cliente2[2] + valor_transferencia
                    print("Transferancia de R$ %.2f do CNPJ %s para o CNPJ %s" % (valor_transferencia, cnpj_origem, cnpj_destino))
                    #armazenando operacoes no extrato
                    tarifa_origem = valor_transferencia*0.03
                    saldo_origem = cliente[2]
                    extrato_origem = f"{data_str}; - {valor_transferencia:.2f}; Tarifa:{tarifa_origem: .2f}; Saldo:{saldo_origem: .2f}"
                    clientes[cnpj_origem][4].append(extrato_origem)
                    tarifa_destino = 0
                    saldo_destino = cliente2[2]
                    extrato_destino = f"{data_str}; + {valor_transferencia:.2f}; Tarifa:{tarifa_destino: .2f}; Saldo:{saldo_destino: .2f}"
                    clientes[cnpj_destino][4].append(extrato_destino)
                else:
                    print("Saldo insuficiente do CNPJ origem!")
        else:
            print("Senha invalido!")

def debito_automatico():
    
    #analisando cnpj e a senha
    cnpj = input("Digite o CNPJ: ")
    senha = int(input("Digite a senha: "))
    cliente = clientes.get(cnpj)
    if cliente is None:
        print("CNPJ invalido!")
    else:
        if senha == cliente[3]:
            pagamentos_automaticos = cliente[5]
            #indicando a institucao de destino e a quantidade a ser debitado por mes (no dia que sera debitado)
            instituicao = input("Digite o nome da instituicao destino: ")
            qtd_dinheiro_por_mes = float(input("Digite a quantidade a ser debitado por mes: "))
            dia_debito = int(input("Digite o dia que o valor sera depositado: "))
            #armazenando as informacoes na lista de pagamentos automaticos do cliente
            pagamento_automatico = f"Instituicao: {instituicao}; Debito por mes: R$ {qtd_dinheiro_por_mes:.2f}; Dia do debito: {dia_debito}"
            clientes[cnpj][5].append(pagamento_automatico)
            print("Debito automatico cadastrado!")
        else:
            print("Senha invalido!")


def menu():
    #mostrando o menu
    print("1. Novo cliente")
    print("2. Apaga cliente")
    print("3. Listar clientes")
    print("4. Debito")
    print("5. Deposito")
    print("6. Extrato")
    print("7. Transferencia entre contas")
    print("8. Debito automatico")
    print("9. Sair")

#analisando e selecionando as opcoes    
while True:
    menu()
    opcao = int(input("Selecione uma opcao: "))
    if opcao == 1:
        novo_cliente()
    elif opcao == 2:
        apaga_cliente()
    elif opcao == 3:
        listar_clientes()
    elif opcao == 4:
        debito()
    elif opcao == 5:
        deposito()
    elif opcao == 6:
        extrato()
    elif opcao == 7:
        transferencia()
    elif opcao == 8:
        debito_automatico()
    elif opcao == 9:
        break
    else:
        print("Erro, escolha novamente!")

with open("clientes.json","w") as f:
    json.dump(clientes, f)