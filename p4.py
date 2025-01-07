import pygame, os, random, time

pygame.init()

# Definirea variabilelor
lungime = 840
inaltime = 680
marime_poze = 128
coloane = 5
randuri = 4
distanta_poze = 10
margine_stanga = (lungime - ((marime_poze + distanta_poze) * coloane)) // 2
margine_sus = (inaltime - ((marime_poze + distanta_poze) * randuri)) // 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
fundal_final=(150,200,100)
selection1 = None
selection2 = None
timp_intoarcere_poze= None 

# Timp si incercari
timp_inceput = time.time()
incercari = 0

# Definirea ecranului si a iconitei
ecran = pygame.display.set_mode((lungime, inaltime))
pygame.display.set_caption('Memory Game')
iconita = pygame.image.load(r'C:\Users\pc\Desktop\proiect python\images\1.jpg')
pygame.display.set_icon(iconita)

# Incarcarea imaginii de fundal
fundal = pygame.image.load(r'C:\Users\pc\Desktop\proiect python\Background.jpg')
fundal = pygame.transform.scale(fundal, (lungime, inaltime))
fundalRect = fundal.get_rect()

# Font 
font = pygame.font.Font(None, 36)

# LISTE POZE
poze = []
for item in os.listdir(r'C:\Users\pc\Desktop\proiect python\images'):
    poze.append(item.split('.')[0])
pozeCopy = poze.copy()
poze.extend(pozeCopy)
pozeCopy.clear()
random.shuffle(poze)

# Incarcarea fiecarei imagini in memorie
poze_joc= []
poze_jocRect = []
poze_ascunse = []
for item in poze:
    poza = pygame.image.load(fr'C:\Users\pc\Desktop\proiect python\images/{item}.jpg')
    poza = pygame.transform.scale(poza, (marime_poze, marime_poze))
    poze_joc.append(poza)
    pozaRect = poza.get_rect()
    poze_jocRect.append(pozaRect)

for i in range(len(poze_jocRect)):
    poze_jocRect[i][0] = margine_stanga + ((marime_poze + distanta_poze) * (i % coloane))
    poze_jocRect[i][1] = margine_sus + ((marime_poze + distanta_poze) * (i // coloane))
    poze_ascunse.append(False)

# Text
def text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    ecran.blit(text_surface, (x, y))

gameLoop = True
while gameLoop:
    # Incarcare fundal
    ecran.blit(fundal, fundalRect)

    # Timp, incercari, afisare
    cat_timp_a_trecut = int(time.time() - timp_inceput)
    text(f"Timp: {cat_timp_a_trecut}s", 10, 10, (154, 245, 18))
    text(f"incercari: {incercari}", 10, 40, (255, 68, 187))

    # Verificare intoarcere imagini
    if timp_intoarcere_poze and time.time() >= timp_intoarcere_poze:
        poze_ascunse[selection1] = False
        poze_ascunse[selection2] = False
        selection1, selection2 = None, None
        timp_intoarcere_poze= None

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not timp_intoarcere_poze:  # ignora click pana se intorc imaginile
                for item in poze_jocRect:
                    if item.collidepoint(event.pos):
                        if not poze_ascunse[poze_jocRect.index(item)]:
                            if selection1 is not None:
                                selection2 = poze_jocRect.index(item)
                                poze_ascunse[selection2] = True
                                incercari += 1  
                            else:
                                selection1 = poze_jocRect.index(item)
                                poze_ascunse[selection1] = True

    
    for i in range(len(poze)):
        if poze_ascunse[i]:
            ecran.blit(poze_joc[i], poze_jocRect[i])
        else:
            pygame.draw.rect(ecran, WHITE, (poze_jocRect[i][0], poze_jocRect[i][1], marime_poze, marime_poze))

    # verifica daca 2 imagini sunt selectate
    if selection1 is not None and selection2 is not None and not timp_intoarcere_poze:
        if poze[selection1] == poze[selection2]:
            selection1, selection2 = None, None
        else:
            timp_intoarcere_poze= time.time() + 1 
    
    # Verifica conditia de castig
    if all(poze_ascunse):
        gameLoop = False
        print(f"Bravo frate! L-ai facut in {cat_timp_a_trecut}s cu doar {incercari} incercari \(°o°)/")
       #Afisare mesaj final
        ecran.fill(fundal_final)  
        text("Bravo frate!", lungime // 2 - 150, inaltime // 2 - 50, (0,0,255))
        text(f"L-ai facut in {cat_timp_a_trecut}s", lungime // 2 - 120, inaltime // 2, (255,220,0))
        text(f"cu doar {incercari} incercari", lungime // 2 - 130, inaltime // 2 + 50, (255,0,0))
        pygame.display.update()
        pygame.time.wait(5000)  #asteapta 5 secunde pentru a inchide

    pygame.display.update()

pygame.quit()
