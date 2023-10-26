import pygame
import sys
import math

pygame.init()

# Configurações da tela
largura = 1680
altura = 1050
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação gravitacional Com Massa fixa Central")

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)

# CFG bolinhas
raio = 20
massa_bolinhas = 1.0
massa_central = 2000.0
aceleracao_gravitacional = 3.6
bolinhas = [{"x": largura // 2, "y": altura // 2, "velocidade_x": 0, "velocidade_y": 0}]

trajetorias = [[]]

# Rastreio mov
bolinha_em_movimento = False

# Distancia entre as duas
def calcular_distancia(bola1, bola2):
    return math.sqrt((bola1["x"] - bola2["x"]) ** 2 + (bola1["y"] - bola2["y"]) ** 2)

# Calcula entre as duas
def calcular_forca_gravitacional(bolinha1, bolinha2):
    dist = calcular_distancia(bolinha1, bolinha2)
    if dist == 0:
        return 0, 0
    direcao = math.atan2(bolinha2["y"] - bolinha1["y"], bolinha2["x"] - bolinha1["x"])
    forca = (massa_bolinhas * massa_central * aceleracao_gravitacional) / (dist ** 2)
    forca_x = forca * math.cos(direcao)
    forca_y = forca * math.sin(direcao)
    return forca_x, forca_y

# TXT screen
def exibir_texto(texto, x, y, tamanho=24, cor=branco):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, cor)
    tela.blit(texto_surface, (x, y))

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if not bolinha_em_movimento:
                    bolinha_em_movimento = True
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                if bolinha_em_movimento:
                    bolinha_em_movimento = False
                    trajetorias[0] = []

        # R reset
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                if not bolinha_em_movimento:
                    bolinhas[0]["x"] = largura // 2
                    bolinhas[0]["y"] = altura // 2
                    bolinhas[0]["velocidade_x"] = 0
                    bolinhas[0]["velocidade_y"] = 0
                    trajetorias[0] = []

    if bolinha_em_movimento:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bolinhas[0]["velocidade_x"] = (mouse_x - bolinhas[0]["x"]) / 10
        bolinhas[0]["velocidade_y"] = (mouse_y - bolinhas[0]["y"]) / 10

    for bolinha in bolinhas:
        forca_x, forca_y = calcular_forca_gravitacional(bolinha, {"x": largura // 2, "y": altura // 2})
        bolinha["velocidade_x"] += forca_x / massa_bolinhas
        bolinha["velocidade_y"] += forca_y / massa_bolinhas

        bolinha["x"] += bolinha["velocidade_x"]
        bolinha["y"] += bolinha["velocidade_y"]

        trajetorias[0].append((bolinha["x"], bolinha["y"]))
        if len(trajetorias[0]) > 1000:
            trajetorias[0].pop(0)

    tela.fill(preto)

    for bolinha in bolinhas:
        pygame.draw.circle(tela, branco, (int(bolinha["x"]), int(bolinha["y"])), raio)

        if bolinha_em_movimento and len(trajetorias[0]) > 1:
            pygame.draw.lines(tela, branco, False, trajetorias[0], 2)

    pygame.draw.circle(tela, branco, (largura // 2, altura // 2), raio * 3)

    # Exibir informações no canto da tela
    exibir_texto(f"Posição: ({int(bolinhas[0]['x'])}, {int(bolinhas[0]['y'])})", 10, 10)
    exibir_texto(f"Velocidade: ({bolinhas[0]['velocidade_x']:.2f}, {bolinhas[0]['velocidade_y']:.2f})", 10, 40)
    exibir_texto("Trajetória da Bolinha", 10, 70)

    pygame.display.flip()
    pygame.time.delay(10)
