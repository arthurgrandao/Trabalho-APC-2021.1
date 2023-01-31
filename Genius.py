"""
Arthur Grandão de Mello
211039250
"""

import pyxel
from random import choice

# Globais
CORES = ["Azul", "Vermelho", "Verde" , "Amarelo"]                                           #Lista de cores para o sorteio
LARGURA, ALTURA = 120, 80                                                                   #Largura e altura da tela
rodada, pts = 1, 0                                                                          #Variáveis de controle
rodando, ligado, intervalo =  False, False, False                                           #Variáveis de controle
vez_computador, vez_jogador = False, False                                                  #Variáveis de controle
b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW   #Cores das teclas
v, tamanho_barra_limite = 20, 20                                                            #Velocidade do sorteio e tamanho da barra de tempo
cj, cc, ce, cl = 0, rodada * v, 0, 0                                                        #Contadores de frames (jogador, computador, espera e limite)
ia, jogador = [], []                                                                        #Listas das jogadas

with open("highscore.txt", "r") as arquivo:
    hs = int(arquivo.readline())                                                            #Recorde da máquina
    arquivo.close()


def som(cor): # Função que reproduz o som das teclas ao serem clicadas e no sorteio.
    pyxel.load('my_resource.pyxres')
    
    # De acordo com a cor que está sendo selecionada o jogo reproduz um determinado som.
    if cor == "Verde": 
        pyxel.play(0, 2)              
    elif cor == "Amarelo":
        pyxel.play(0, 1)
    elif cor == "Azul":
        pyxel.play(0, 3)
    elif cor == "Vermelho":
        pyxel.play(0, 0)


def highscore(): # Função que salva o recorde so jogador
    global hs

    # Caso o jogador quebre o recorde, o programa irá arquivá-lo num arquivo .txt
    if pts > hs:
        hs = pts
        with open("highscore.txt", "w") as arquivo:
            arquivo.write(str(hs))
            arquivo.close()


def tempo_limite(): # Função que limita o tempo de ação do jogador.
    global cl, tamanho_barra_limite

    # O cl é inciado em outras funções e aqui sofre a contagem regressiva
    if cl > 0:
        cl -= 1
    
    elif cl == 0:
        pyxel.quit()
        print("Saiu por inatividade.")

    # Reduz a barra de tempo
    if cl % 15 == 0:
        tamanho_barra_limite -= 1


def display(): # Função que forma o background do jogo.
    global b, r, g ,y
    
    # Fundo
    pyxel.cls(pyxel.COLOR_BLACK)
    # Tecla verde
    pyxel.rect(0, 0, (LARGURA/2)-2, (ALTURA/2)-2, g) # (0, 0, 58, 38)
    # Tecla amarela
    pyxel.rect(0, (ALTURA/2)+2, (LARGURA/2)-2, (ALTURA/2)-2, y) # (0, 42, 58, 38)
    # Tecla vermelha
    pyxel.rect((LARGURA/2)+2, (ALTURA/2)+2, (LARGURA/2)-2, (ALTURA/2)+2, r) # (62, 42, 58, 42)
    # Tecla azul
    pyxel.rect((LARGURA/2)+2, 0, (LARGURA/2)-2, (ALTURA/2)-2, b) # (62, 0, 58, 38)
    # Placar central
    pyxel.circ(LARGURA/2, ALTURA/2, 13, pyxel.COLOR_BLACK) # (60, 40)
    pyxel.text((LARGURA/2)-9, (ALTURA/2)-5, f"Pts:{pts}\nHS:{hs}", pyxel.COLOR_WHITE) # (51, 35)
    # Barra de tempo
    pyxel.rect((LARGURA/2)-10, (ALTURA/2)-7, tamanho_barra_limite, 1, pyxel.COLOR_LIGHTBLUE)
    # Mensagem de iniciar
    if not rodando:
        pyxel.text(3, (ALTURA/2)-30, "Pressione Espaco para iniciar\n        Esc para sair", pyxel.COLOR_WHITE)


def clique_jogador(): # Função que implementa o a mecânica do clique durante a vez do jogador.
    global jogador, b, r, g ,y, cj, cl, tamanho_barra_limite

    clique = ""

    if ligado:
        px, py = pyxel.mouse_x, pyxel.mouse_y # Posição do mouse
        
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON): # Registra o clique
            
            # Os ifs abaixo conferem a posição do clique e o associam a uma tecla
            
            if px <= (LARGURA/2)-2 and py <= (ALTURA/2)-2: # Tecla verde
                # Os dois items abaixo são zerados para reiniciarem caso já tivessem sido ativados anteriormente
                b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW # 
                cj, cl = 0, 0
                
                tamanho_barra_limite = 20 # Reseta a barra de tempo
                cl += 300 # Ativação do contador de limite (300 frames = 10 segundos) 
                cj += 10 # Ativação do contador da jogada, que faz com que as teclas fiquem em destaque por cerca de 1/3 segundos 
                clique = "Verde" # Atribuição da cor
                som(clique) # Geração do som
                jogador.append(clique) # Adição a lista que forma a sua jogada
                
               
            elif px <= (LARGURA/2)-2 and py >= (ALTURA/2)+2: # Tecla amarela
                b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW
                cj, cl = 0, 0
                
                tamanho_barra_limite = 20
                cl += 300
                cj += 10
                clique = "Amarelo"
                som(clique)
                jogador.append(clique)
                
            
            elif px >= (LARGURA/2)+2 and py <= (ALTURA/2)-2: # Tecla azul
                b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW 
                cj, cl = 0, 0
                
                tamanho_barra_limite = 20
                cl += 300
                cj += 10             
                clique = "Azul"
                som(clique)
                jogador.append(clique)
                
            
            elif px >= (LARGURA/2)+2 and py >= (ALTURA/2)+2: #Tecla vermelha 
                b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW
                cj, cl = 0, 0

                tamanho_barra_limite = 20
                cl += 300
                cj += 10
                clique = "Vermelho"
                som(clique)
                jogador.append(clique)
                
        
    # Processo de contagem do cj
    if cj == 0:
        b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW
    
    elif cj > 0:
        if clique == "Verde":
            b, r, y = pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK               
        elif clique == "Amarelo":
            r, g, b = pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK
        elif clique == "Azul":
            r, g, y = pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK
        elif clique == "Vermelho":
            b, g, y = pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK   
        
        cj -= 1


def computador(): # Função que implementa a mecânica do sorteio das cores do computador.
    global r, g, y, b, cc, v, cl, cor_vez, vez_computador, vez_jogador, tamanho_barra_limite

    cor = ""
    
    # Sorteio das cores que formarão a jogada do computador
    if len(ia) < rodada: 
        cor = choice(CORES) 
        ia.append(cor)
        cc = rodada*v

    if cc == 0: # Fim do sorteio 
        b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW # Reinicialização das cores
        
        tamanho_barra_limite = 20 # Reseta a barra de tempo
        cl += 300 # Ativação do contador de limite (300 frames = 10 segundos) 
        
        vez_computador, vez_jogador = False, True # Alteração das variáveis de controle de vez 

    elif cc > 0:
        #Processo que determina a cor que deve ser mostrada no sorteio durante o jogo
        for x in range(rodada, 0, -1):
            if x*v == cc: # x * velocidade do sorteio = contador do computador
                b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW
                cor_vez = ia[rodada - x] # Atribui a cor desejada 
                som(cor_vez) # Geração do som

        """
        O contador do computador é igual a rodada * velocidade pois a rodada é equivalente a número de cores sorteadas.
        o processo acima determina qual cor deve ser mostrada para cada valor do cc. Ex: 80 <= cc <= 120 -> cor_vez = "Amarelo" e assim por diante.
        Esses intervalos são determinado pelo v.
        """
        # Destaque das cores
        if cor_vez == "Verde":
            b, r, y = pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK               
        elif cor_vez == "Amarelo":
            r, g, b = pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK
        elif cor_vez == "Azul":
            r, g, y = pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK
        elif cor_vez == "Vermelho":
            b, g, y = pyxel.COLOR_BLACK, pyxel.COLOR_BLACK, pyxel.COLOR_BLACK
        
        cc -= 1


def resultado(): # Função que checa se o jogador passou ou não de fase.
    global jogador, rodada, pts, tamanho_barra_limite, rodando, vez_jogador, intervalo, ce, v, ia, b, r, g, y
    
    if jogador == ia: # Passou
        vez_jogador, intervalo = False, True

        # Reduz a velocidade a cada dois pontos. 
        # O v>8, do segundo and, se dá porque a velocidade menor que 8 não se torna possível distinguir a quantidade de cores repetidas pelo som.
        if pts % 2 == 0 and pts != 0 and v > 8: 
            v -= 2

        rodada += 1 
        ce += 45 # Inicialização do intervalo
        jogador, pts = [], rodada - 1 # Reinicialização da lista do jogador e determinação dos pontos
        highscore() # Checagem de recorde
    
    elif len(jogador) > 0:
        if jogador != ia[:len(jogador)]: # Compara a lista do jogador com a lista do computador, porém com o mesmo tamanho da lista do jogador
            highscore() # Registra o recorde
    
            # Traz essas variáves ao estado original
            b, r, g, y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW
            tamanho_barra_limite = 20
            rodando, vez_jogador = False, False 
            jogador, ia = [], []
            rodada, pts = 1, 0

                   
def espera(): # Função que realiza o tempo de intervalo após passar de nível
    global ce, cj, vez_computador, intervalo, b, r, g ,y

    if intervalo:
        # Contador do tempo de intervalo
        if ce == 0:
            intervalo, vez_computador = False, True
        elif ce > 0:
            ce -= 1

        # Esse aqui serve para que a o processo de destaque do clique não seja interrompido pelo intervalo
        if cj > 0:
            cj -= 1
        elif cj == 0:
            b, r, g ,y = pyxel.COLOR_DARKBLUE, pyxel.COLOR_RED, pyxel.COLOR_GREEN, pyxel.COLOR_YELLOW
        

def update(): # Lógica do jogo
    global ligado, rodando, vez_computador, cl, pts
    
    # Como o jogo procede
    if rodando:
        if vez_computador:
            ligado, cl = False, 0
            computador()
    
        if vez_jogador:
            ligado = True
            clique_jogador()
            tempo_limite()
        
        resultado()
        espera()
    
    # Para iniciar pressione espaço
    else:
        if pyxel.btnp(pyxel.KEY_SPACE):
            rodando, vez_computador = True, True
    
def draw(): # Desenha o jogo
    display()


pyxel.init(LARGURA, ALTURA, caption="Genius")
pyxel.mouse(True) # Mostra o cursor do mouse na tela
pyxel.run(update, draw)