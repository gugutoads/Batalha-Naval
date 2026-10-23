import random
import os
import msvcrt
import pyfiglet

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

class Tabuleiro:
    def __init__(self):
        self.casas = [[0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      ]
        

    def receber_ataque(self, ponto, jogador):
        if type(self.casas[ponto[0]][ponto[1]]) == Navio:
            navio = self.casas[ponto[0]][ponto[1]]
            navio.vida -= 1
            print("\nAcertou Navio!\n")
            if navio.esta_afundado(jogador):
                print("Navio Afundado! ⚓💥\n")
            self.casas[ponto[0]][ponto[1]] = 1
            return True
        
        elif self.casas[ponto[0]][ponto[1]] == 2 or self.casas[ponto[0]][ponto[1]] == 1:
            print("casa já atacada!")
            return False
        else:
            self.casas[ponto[0]][ponto[1]] = 2
            return True

    def posicionar1(self, navio, ponto):
        pont = 0
        if ponto[0] + navio.largura - 1 < 7:
            while pont < navio.largura:
                if self.casas[ponto[0] + pont][ponto[1]] != 0:
                    return False
                pont += 1
            #posiciona o navio se estiver tudo em conforme 
            pont = 0
            while pont < navio.largura:
                self.casas[ponto[0] + pont][ponto[1]] = navio  
                pont+=1     
            return True
        else:
            return False

    def posicionar2(self, navio, ponto):
        pont = 0
        if ponto[1] + navio.largura - 1 < 7:
            while pont < navio.largura:
                if self.casas[ponto[0]][ponto[1] + pont] != 0:
                    return False
                pont += 1
            #posiciona o navio se estiver tudo em conforme
            pont = 0
            while pont < navio.largura:
                self.casas[ponto[0]][ponto[1] + pont] = navio  
                pont+=1   
            return True
        else:
            return False

    def posicionar3(self, navio, ponto):
        pont = 0
        if ponto[0] - (navio.largura - 1) > -1:
            while pont < navio.largura:
                if self.casas[ponto[0] - pont][ponto[1]] != 0:
                    return False
                pont += 1
            pont = 0
            while pont < navio.largura:
                self.casas[ponto[0] - pont][ponto[1]] = navio  
                pont+=1 
            return True
        else:
            return False

    def posicionar4(self, navio, ponto):
        pont = 0
        if ponto[1] - (navio.largura - 1) > -1:
            while pont < navio.largura:
                if self.casas[ponto[0]][ponto[1] - pont] != 0:
                    return False
                pont += 1
            pont = 0
            while pont < navio.largura:
                self.casas[ponto[0]][ponto[1] - pont] = navio  
                pont+=1
            return True
        else:
            return False

    def verificar_navio_cabe(self, navio, ponto):
        if self.posicionar1(navio, ponto):
            return True
        elif self.posicionar2(navio, ponto):
            return True    
        elif self.posicionar3(navio, ponto):
            return True    
        elif self.posicionar4(navio, ponto):
            return True
        else:
            False

    def posicionar_navio_random(self, navio):
        ponto = [random.randint(0,6), random.randint(0,6)]
        x = 0
        while x < 1000:
            if self.verificar_navio_cabe(navio, ponto):   
               return True
            else:
                ponto = [random.randint(0,6), random.randint(0,6)]
                x += 1


class Navio:
    def __init__(self, largura):
        self.largura = largura
        self.vida = largura

    def esta_afundado(self, jogador):
        if self.vida == 0:
            jogador.vida -= 1
            return True
        return False
            
    

class Jogador:
    def __init__(self, frota, nome):
        self.vida = len(frota)
        self.nome = nome

    registro_ataques = []

    def verificar_derrota(self):
        if self.vida == 0:
            return True
        else:
            return False

    def selecionar_casa(self, navio = None, tabuleiro=None):
        coluna = None
        linha = None
        if navio:
            casa = input(f"\nQual casa deseja colocar o navio de tamanho [{navio.largura}] (ex: A1): ").upper().replace(" ","")
        if tabuleiro:
            casa = input(f"\nQual casa deseja atacar (ex: A1): ").upper().replace(" ","")
        if len(casa) > 2:
            return False 
          
        for char in casa:
            if char.isalpha() and char in ["A","B","C","D","E","F","G"]:
                coluna = ord(char) - ord('A')
            elif char.isdigit() and int(char) in [1,2,3,4,5,6,7]:
                linha = int(char) - 1
            else:
                return False
        
        if coluna != None and linha != None:
            return [linha, coluna, casa]
        
        return False

    def posicionar_manual(self, tabuleiro, navio):
        ponto = self.selecionar_casa(navio = navio)
        #se a casa for válida
        if ponto:
            direcao = input("Qual direção deseja colocar o navio (horizontal ou vertical): ").lower().replace(" ","")

            if direcao == "horizontal":
                direcao2 = input(f"A partir da casa {ponto[2]}, quer colocar em qual direção (esquerda ou direita): ").lower().replace(" ","")
                ponto.pop()

                if direcao2 == "direita":     
                    if tabuleiro.posicionar2(navio, ponto):
                        print("\nnavio posicionado\n")
                        printar_tabuleiro(tabuleiro)
                        return True
                    print("\nNão foi possível colocar navio")
                    return False
                
                elif direcao2 == "esquerda":
                    if tabuleiro.posicionar4(navio,ponto):
                        print("\nnavio posicionado\n")
                        printar_tabuleiro(tabuleiro)
                        return True 
                    print("\nNão foi possível colocar navio")
                    return False
                
                else:
                    print("Direção inválida")
                    return False
                
            elif direcao == "vertical":
                direcao2 = input(f"A partir da casa {ponto[2]}, quer colocar em qual direção (cima ou baixo): ").lower().replace(" ","")
                ponto.pop()
            
                if direcao2 == "baixo":
                    if tabuleiro.posicionar1(navio, ponto):
                        print("\nnavio posicionado\n")
                        printar_tabuleiro(tabuleiro)
                        return True 
                    print("\nNão foi possível colocar navio")
                    return False
                
                elif direcao2 == "cima":
                    if tabuleiro.posicionar3(navio, ponto):
                        print("\nnavio posicionado\n")
                        printar_tabuleiro(tabuleiro)
                        return True 
                    print("\nNão foi possível colocar navio")
                    return False
                
                else:
                   print("Direção inválida")
                   return False 

            print("Direção inválida")
            return False
        else:
            print("Casa inválida")
        
    def atacar(self, tabuleiro, jogador):
        ponto = self.selecionar_casa(tabuleiro = tabuleiro)
        if ponto:
            self.registro_ataques.append(ponto[2])
            ponto.pop()      
            if tabuleiro.receber_ataque(ponto, jogador):
                if tabuleiro.casas[ponto[0]][ponto[1]] == 1:
                    printar_tabuleiro(tabuleiro, inicio=False)
                    return False
                
                print("\nErrou!")
                return True
            else:
                return False
        else:
            print("Casa inválida")
            return False



def printar_tabuleiro(tabuleiro, inicio = True):
    print("   A  B  C  D  E  F  G")
    for i, l in enumerate(tabuleiro.casas):
        print(i + 1, end = " ")
        for k, c in enumerate(l):
            if tabuleiro.casas[i][k] == 1:
                print("💥", end=" ")
            elif tabuleiro.casas[i][k] == 2:
                print("❌", end=" ")
            elif tabuleiro.casas[i][k] != 0:
                if inicio:
                    print("🚢", end=" ")
                else:
                    print("🌊", end=" ")
            else:   
                print("🌊", end=" ")
        print()


 

tabuleiro1 = Tabuleiro()
tabuleiro2 = Tabuleiro()

j1navio1 = Navio(5)
j1navio2 = Navio(4)
j1navio3 = Navio(3)
j1navio4 = Navio(2)
j1navio5 = Navio(2)
j2navio1 = Navio(5)
j2navio2 = Navio(4)
j2navio3 = Navio(3)
j2navio4 = Navio(2)
j2navio5 = Navio(2)

frota1 = [j1navio1,j1navio2,j1navio3,j1navio4,j1navio5]
frota2 = [j2navio1,j2navio2,j2navio3,j2navio4,j2navio5]
jogador1= Jogador(frota1, "Jogador 1")
jogador2= Jogador(frota2, "Jogador 2")


limpar_tela()
print(pyfiglet.figlet_format("Batalha Naval", font="cosmike"))
print("=" * 40)
print("JOGADOR 1 POSICIONE A SUA FROTA")
print("=" * 40)
print("\nPorta-Aviões[5]: 🚢🚢🚢🚢🚢 ")
print("Encouraçado[4]:    🚢🚢🚢🚢 ")
print("submarino[3]:        🚢🚢🚢 ")
print("bote[2]:               🚢🚢 ")
print("bote[2]:               🚢🚢")
print()
printar_tabuleiro(tabuleiro1)

print('\npreenchar automático (1)')
print('preencher manual (2)')

sucesso = False
while not sucesso:
    print("\nOpção: ", )
    opcao = msvcrt.getch().decode('utf-8')
    if opcao not in ["1","2"]:
        print("Opção inválida, digite novamente")
    else:
        sucesso = True
print(opcao)

if int(opcao) == 1:
    for navio in frota1:
        tabuleiro1.posicionar_navio_random(navio)
    print("\nSua frota:")
    printar_tabuleiro(tabuleiro1)
    input("\nAperte [Enter] para continuar")
else:
    for navio in frota1:
        sucesso = False
        while not sucesso:
            if jogador1.posicionar_manual(tabuleiro1, navio):
                sucesso = True
            else:
                print("Posicione o navio novamente")
    input("\nAperte [Enter] para continuar")

limpar_tela()
print(pyfiglet.figlet_format("Batalha Naval", font="cosmike"))
print("=" * 40)
print("JOGADOR 2 POSICIONE A SUA FROTA")
print("=" * 40)
print("\nPorta-Aviões[5]: 🚢🚢🚢🚢🚢 ")
print("Encouraçado[4]:    🚢🚢🚢🚢 ")
print("submarino[3]:        🚢🚢🚢 ")
print("bote[2]:               🚢🚢 ")
print("bote[2]:               🚢🚢")
print()
printar_tabuleiro(tabuleiro2)

print('\npreenchar automático (1)')
print('preencher manual (2)')

sucesso = False
while not sucesso:
    print("\nOpção: ", )
    opcao = msvcrt.getch().decode('utf-8')
    if opcao not in ["1","2"]:
        print("Opção inválida, digite novamente")
    else:
        sucesso = True
print(opcao)

if int(opcao) == 1:
    for navio in frota2:
        tabuleiro2.posicionar_navio_random(navio)
    print("\nSua frota:")
    printar_tabuleiro(tabuleiro2)
    print("\nFrota posicionada!")
    input("\nAperte [Enter] para continuar")
else:
    for navio in frota2:
        sucesso = False
        while not sucesso:
            if jogador2.posicionar_manual(tabuleiro2, navio):
                sucesso = True
            else:
                print("Posicione o navio novamente")
    print("\nFrota posicionada!")
    input("\nAperte [Enter] para continuar")

victory = False
vencedor = None
tubuleiro_perdedor= None
while not victory:  
    limpar_tela()
    print("=" * 40)
    print(f"RODADA DE ATAQUE JOGADOR 1")
    print("=" * 40)
    print()
    printar_tabuleiro(tabuleiro2, inicio=False)
    sucesso = False
    while not sucesso:
        if jogador1.atacar(tabuleiro2, jogador2):
            sucesso = True
        #verrifica derrota a cada jogada repetida
        if jogador2.verificar_derrota():
            sucesso= True

    if jogador2.verificar_derrota():
        vencedor = jogador1
        victory = True
        break

    print()
    printar_tabuleiro(tabuleiro2, inicio=False)

    input("\nAperte [Enter] para continuar")
    limpar_tela()
    print("=" * 40)
    print(f"RODADA DE ATAQUE JOGADOR 2")
    print("=" * 40)
    print()
    printar_tabuleiro(tabuleiro1, inicio=False)
    sucesso = False
    while not sucesso:
        if jogador2.atacar(tabuleiro1, jogador1):
            sucesso = True
        #verrifica derrota a cada jogada repetida
        if jogador2.verificar_derrota():
            sucesso= True

    if jogador1.verificar_derrota():
        vencedor = jogador2
        victory = True
        break

    print()
    printar_tabuleiro(tabuleiro1, inicio=False)
    input("\nAperte [Enter] para continuar")

print()
print("=" * 40)
print("FIM DE JOGO")
print("=" * 40)
print(f"\nVENCEDOR: {vencedor.nome}!!!🎉")
print(f'\n registro ataques: {set(vencedor.registro_ataques)}')





