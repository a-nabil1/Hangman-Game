import random

import pygame
import os
import math
from ListOfWords import words


#setup
pygame.font.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

#colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE= (138,43,226)
THISTLE= (216,191,216)
BABYBLUE=(137, 207, 240)

#images
images=['hangman0.png', 'hangman1.png','hangman2.png', 'hangman3.png', 'hangman4.png', 'hangman5.png', 'hangman6.png']
hangStat=0


# game mechanics
word=random.choice(words)
currentAns=[]
for letter in word:
    currentAns.append('_')

letterStart=[0]
for i in range(1,len(currentAns)):
    letterStart.append(50*i)

word=word.upper()
print(word)
letterFont = pygame.font.SysFont('comicsans', 42)


#button variables
visibility=True
radius = 20
gap = 15
buttons = []
startx = (WIDTH/2)-(13*radius+6*gap)
starty = 75

alphabet=[]
A=65
for i in range(26):
    x = startx + gap*2 + ((radius*2 + gap) * (i % 13))  # goes to 2nd row after 13 circles
    y = starty + ((i//13)*(2*gap+radius))
    buttons.append([x,y, chr(A +i), True])  #co-ordinates of buttons
    alphabet.append([chr(A +i), True])
print(buttons)


# text
buttonFont = pygame.font.SysFont('comicsans', 22)

#endGame
endFont=pygame.font.SysFont('comicsans', 50)



def draw():
    screen.fill(BABYBLUE)  # background

    #draw hangman
    hangmanImage = pygame.image.load(os.path.join('images', images[hangStat]))
    screen.blit(hangmanImage, (90, 200))

    #drawing buttons and letters
    for i in range(26):
        # coord=buttons[i]
        x,y, ltr, bool = buttons[i]
        # letter, bool = alphabet[i]

        if bool:
            circles=pygame.draw.circle(screen, BLACK, (x,y), radius, 3)  #drawing circles for buttons
            buttonText = buttonFont.render(ltr, 1, BLACK)
            screen.blit(buttonText, (x-(buttonText.get_width()/2),y-(buttonText.get_height()/2)))

    #drawing user answr
    for i in range(len(currentAns)):
        currentText=letterFont.render(currentAns[i], 1, BLACK)
        screen.blit(currentText, (380+letterStart[i], 320))


    pygame.display.update()



def endOfGame(msg):
    pygame.time.delay(1000)
    screen.fill(WHITE)
    endText = endFont.render(msg, 1, RED)
    screen.blit(endText, (WIDTH / 2 - endText.get_width() / 2, HEIGHT / 2 - endText.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)



def main():
    global hangStat

    FPS = 60
    clock = pygame.time.Clock()

    run =True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


            # checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()  #gets x,y pos of mouse

                for i in range(26):  #each i is each button

                    x, y, ltr, bool = buttons[i]  #(x,y) = i-th button position
                    distance= math.sqrt(((x-mouseX)**2)+((y-mouseY)**2))  ##relative to each button

                    if bool:

                        if distance <= radius:
                            (buttons[i])[3] = False  #button will be false

                            for j in range(len(word)):
                                if ltr == word[j].upper():
                                    currentAns.pop(j)
                                    currentAns.insert(j,ltr)


                            if ltr not in word:
                                hangStat = hangStat +1
                                print(hangStat)

        draw()


        #END OF GAME
        finalAns = ''.join(currentAns)
        if hangStat == 6:
            endOfGame("Sorry you ran out of turns")
            break  #break event loop when game finished


        won=True
        if finalAns!=word:
            won=False  #nothing happens if won==false so wont quit game if mouse not clicked


        elif won:
            endOfGame("You Won!")
            break




if __name__ == "__main__":
    main()