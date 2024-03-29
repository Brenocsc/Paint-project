import pygame, sys, math, primitives
from primitives import *
from pynput.mouse import Listener
from pynput.keyboard import Key, Listener
from pynput import mouse
from pynput.mouse import Button
from threading import Thread

#Variaveis de curva
selected_point = None
curving = False
#control_points = [(300,100), (300,500), (450,500), (500,150)]
control_points = [(0,0),(0,0),(0,0)]
#Variaveis de controle
clicked = False
start = (0, 0)
primitivas = {'Linha', 'Circulo', 'Retangulo', 'Quadrado', 'Polilinha', 'Curva'} #Apenas para referencia, desnecessario
cores = [(0,0,0),(140,140,140),(255,0,0),(255,51,51),(255,255,0),(0,255,0),(0,230,255),(0,80,255),(255,0,255),(255,160,10),(255,10,160),(10,255,120),(130,130,130),(255,255,255),(0,0,255),(255,200,10)]
atual = 0 #Primitiva atual sendo desenhada
atualcor = 0 #Cor atual sendo usada
c = 0
colorindo = False
oldAtual = 0
#Implementacao da interface
#Esqueleto
linha(screen_size[0] >> 2, 0, screen_size[0] >> 2, screen_size[1], foreground)#viewport left
linha(screen_size[0] >> 2, screen_size[1] >> 4,screen_size[0], screen_size[1] >> 4,foreground)# viewport top
for i in range((screen_size[0] >> 2) + 10, (screen_size[0] >> 2) + 538, 33):
    retangulo(i, 3, i+29, 32, foreground)
    colorir(i+1,4,cores[c])
    c = c+1
for i in range(len(primitivas)):
    y = screen_size[1] // len(primitivas) * (i + 1)
    linha(0, y, screen_size[0] >> 2, y, foreground)
retangulo((screen_size[0] >> 2) + 556, 5, (screen_size[0] >> 2) + 581, 30,foreground)
retangulo((screen_size[0] >> 2) + 561, 10, (screen_size[0] >> 2) + 576, 25,foreground)
colorir((screen_size[0] >> 2) + 563,12,cores[atualcor])

def desenhaBotao(indice, pressed=False):
    if indice < 6:
        c1 =  (250, 250, 250)#Frente botao
        c2 = (210, 210, 210) #Fundo botao
        button_height = 5
        x0 = 0
        y0 = (indice * (screen_size[1] // len(primitivas))) + 1
        x1 = (screen_size[0] >> 2) - button_height - 1
        y1 = ((indice + 1) * (screen_size[1] // len(primitivas))) - button_height - 1
        if pressed:
            x0 += button_height
            y0 += button_height
            x1 += button_height
            y1 += button_height
            c1 = (210, 210, 210)
            c2 = (250, 250, 250)
        colorir(x0 + 1, y0 + 1, c2)
        retangulo(x0, y0, x1, y1, c1)
        colorir(x0 + 1, y0 + 1, c1)

    if indice == 0:
        #Linha
        x0 = screen_size[0] >> 5
        y0 = (screen_size[1] // 6) >> 2 
        x1 = (screen_size[0] >> 2) - (screen_size[0] >> 5)
        y1 = (screen_size[1] // 6) - (screen_size[0] >> 5)
        linha(x0, y0, x1, y1, foreground)
    elif indice == 1:
        #Circulo
        x0 = screen_size[0] >> 3 
        y0 = (screen_size[1] // 6) + (screen_size[1] // 12)
        r = screen_size[1] // 24
        circulo(x0, y0, r, foreground)
    elif indice == 2:
        #Retangulo
        x0 = screen_size[0] >> 5
        y0 = ((screen_size[1] // 6) >> 2) + (screen_size[1] // 3)
        x1 = (screen_size[0] >> 2) - (screen_size[0] >> 5)
        y1 = ((screen_size[1] // 6) - (screen_size[0] >> 5)) + (screen_size[1] // 3)# - (screen_size[1] // 6 >> 2))
        retangulo(x0, y0, x1, y1, foreground)
    elif indice == 3:
        #Quadrado
        x0 = (screen_size[0] >> 4) + (screen_size[0] >> 5) 
        y0 = ((screen_size[1] // 6) * 3) + (screen_size[1] // 24)
        size = screen_size[1] // 12
        retangulo(x0, y0, x0 + size, y0 + size, foreground)
    elif indice == 4:
        #Polilinha
        x0 = (screen_size[0] >> 5)
        y0 = ((screen_size[1] // 6) * 5) - screen_size[1] // 24
        x1 = (screen_size[0] >> 5) + (screen_size[0] >> 4)
        y1 = ((screen_size[1] // 6) * 4) + screen_size[1] // 24
        linha(x0, y0, x1, y1, foreground)
        x0 = (screen_size[0] >> 3) + (screen_size[0] >> 5)
        y0 = ((screen_size[1] // 6) * 5) - screen_size[1] // 24
        linha(x1, y1, x0, y0, foreground)
        x0 -= 1
        y0 += 1
        x1 = (screen_size[0] >> 2) - (screen_size[0] >> 5)
        y1 = ((screen_size[1] // 6) * 4) + screen_size[1] // 24
        linha(x0, y0, x1, y1, foreground)
    elif indice == 5:
        #Curva
        x0 = screen_size[0] >> 5
        y0 = ((screen_size[1] // 6) * 5) + 24
        x1 = (screen_size[0] >> 2) - 24 
        y1 = screen_size[1] - 24
        x2 = (screen_size[0] >> 2) - 24 
        y2 = ((screen_size[1] // 6) * 5) + 24
        bezierQuadrado((x0,y0),(x1,y1),(x2,y2), foreground)
    elif indice == 6:
        c = white if not pressed else (210, 210, 210)
        colorir((screen_size[0] >> 2) + 557,12, c) #Fundo botao
        colorir((screen_size[0] >> 2) + 562, 11, cores[atualcor]) #Frente botao


for i in range(len(primitivas)):
    if i == 0:
        desenhaBotao(i, True)
    else:
        desenhaBotao(i)

layer.blit(screen, (0,0))

#Mouse listeners
def on_move(x, y):
    global control_points
    global start
    global atual
    global clicked
    global curving
    mouseX, mouseY = pygame.mouse.get_pos()
    if clicked:
        #Mantem os desenhos dentro da area desenhavel
        if mouseX < screen_size[0] >> 2:
            mouseX = screen_size[0] >> 2
        if mouseY < screen_size[1] >> 4:
            mouseY = screen_size[1] >> 4
        screen.blit(layer, (0,0))

        #Verifica qual operacao fazer quando arrastar o mouse
        if atual == 0: 
            linha(start[0], start[1], mouseX, mouseY, cores[atualcor])
        elif atual == 1:
            r = int(math.sqrt(((mouseX - start[0]) ** 2) + ((mouseY - start[1]) ** 2)))
            #Verifica se o circulo esta dentro da area de desenho
            if r > start[0] - (screen_size[0] >> 2):
                r = start[0] - (screen_size[0] >> 2)
            if r > start[1] - (screen_size[1] >> 4):
                r = start[1] - (screen_size[1] >> 4)
            circulo(start[0], start[1], r, cores[atualcor])
        elif atual == 2:
            retangulo(start[0], start[1], mouseX, mouseY, cores[atualcor])
        elif atual == 3: 
            signal = abs(mouseY - start[1]) // (mouseY - start[1]) if mouseY != start[1] else 1
            if mouseX < start[0]:
                signal = -signal

            if abs(mouseX - start[0]) > abs(start[1] - (screen_size[1] >> 4)) and start[1] > mouseY:
                if mouseX > start[0]:
                     mouseX = start[0] + abs((screen_size[1] >> 4) - start[1])
                else:
                     mouseX = start[0] - abs((screen_size[1] >> 4) - start[1])    
            retangulo(start[0], start[1], mouseX, start[1] + ((mouseX - start[0]) * signal), cores[atualcor])
        elif atual == 4:
            linha(start[0], start[1], mouseX, mouseY, cores[atualcor])
        elif atual == 5:
            if curving == 1:
                linha(start[0], start[1], mouseX, mouseY, cores[atualcor])
            elif curving == 2:
                bezierQuadrado(control_points[0], control_points[1], (mouseX,mouseY), cores[atualcor])
            else:
                curving = 0


def on_click(x, y, button, pressed):
    mouseX, mouseY = pygame.mouse.get_pos()
    global selected_point
    global control_points
    global clicked
    global start
    global atual
    global atualcor
    global curving
    global colorindo
    global oldAtual
    if pressed:
        if mouseX > screen_size[0] >> 2 and mouseY > screen_size[1] >> 4: #Área editável
            start = (mouseX, mouseY)
            if atual == 4: #Desenhando polilinha
                if button == Button.right and clicked:
                    clicked = False
                    screen.blit(layer, (0,0))
                    pygame.display.flip()
                else:
                    layer.blit(screen, (0,0)) 
            if atual == 5: #Desenhando curva
                clicked = True
                if curving == 0:
                    control_points[curving] = (mouseX,mouseY)
                    curving = curving + 1
                elif curving == 1:
                    control_points[curving] = (mouseX,mouseY)
                    curving = curving + 1
                elif curving == 2:
                    control_points[curving] = (mouseX,mouseY)
                    curving = curving + 1
                    layer.blit(screen, (0,0))
                else:
                    clicked = False

            elif atual == 6: #Preencher forma
                colorir(mouseX,mouseY,cores[atualcor])
                pygame.display.flip()
            else: #Outras formas
                if button != Button.right:
                    clicked = True

        elif not clicked and mouseX < screen_size[0] >> 2: #Dentro do menu de formas
            if colorindo:
                colorindo = False
            oldAtual = atual
            atual = mouseY // (screen_size[1] // len(primitivas))
            if oldAtual != atual: 
                desenhaBotao(atual, True)
                desenhaBotao(oldAtual)
                layer.blit(screen, (0,0))
                if atual == 5:
                    curving = 0
            pygame.display.flip()
        elif mouseX > (screen_size[0] >> 2) + 556 and mouseY > 5 and mouseX < (screen_size[0] >> 2) + 581 and mouseY < 30: #Botao preencher
            if not colorindo:
                colorindo = True
                oldAtual = atual
                atual = 6
            else:
                colorindo = False
                atual = oldAtual
                oldAtual = 6
            desenhaBotao(atual, True)
            desenhaBotao(oldAtual)
            pygame.display.flip()
        elif atual == 4: #Polilinha dentro de area indevida
            clicked = False
            screen.blit(layer, (0,0))
            pygame.display.flip()
            pass
        else: #Selecionando cores
            c = 0
            for i in range((screen_size[0] >> 2) + 10, (screen_size[0] >> 2) + 538, 33):
                if mouseX > i and mouseY > 3 and mouseX < i+29 and mouseY < 32:
                    atualcor = c
                    colorir((screen_size[0] >> 2) + 563,12,cores[atualcor])
                    break
                c = c+1
            pygame.display.flip()


    else: #Evento do botao sendo solto
        if atual != 4 and atual != 5:
            clicked = False
            layer.blit(screen, (0,0))


def on_press(key):
    global clicked
    global atual
    if key == Key.esc:
        clicked = False
        screen.blit(layer, (0,0))
        pygame.display.flip()


listener = mouse.Listener( on_move=on_move, on_click=on_click)
listener.start()

def kb_listener(args):
    global on_press
    with Listener(on_press=on_press) as l:
        l.join()


thread = Thread(target = kb_listener, args = (10, ))
thread.daemon = True
thread.start()


#try:
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
#except SystemExit:
#    pygame.quit()
#    thread.exit()
#    sys.exit()