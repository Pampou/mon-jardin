from pygame.locals import *
import pygame
import random

pygame.init()

jardin = []

def loadImage(imageURL, transparency):
	if transparency == True:
		image = pygame.image.load(imageURL).convert_alpha()
	else:
		image = pygame.image.load(imageURL).convert()
	return image

class Garden():
    def __init__(self):
        self.terrainList = []
        self.plantList = []
        x = 0
        y = 0
        while x < 20 :
            self.terrainList.append([])
            while y < 15 :
                self.terrainList.append(1)
                y += 1
            y = 0
            x += 1

class Text():
    def __init__(self, text, font, red, green, blue, redBack = None, greenBack = None, blueBack = None):
        if (redBack == None and greenBack == None and blueBack == None):
            self.text = font.render(text, True, (red, green, blue))
        else:
            self.text = font.render(text, True, (red, green, blue), (redBack, greenBack, blueBack))
        self.x = 0
        self.y = 0
    def draw(self, window):
        window.blit(self.text,(self.x,self.y))

class Item():
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.amount = 1
        self.font = pygame.font.Font(None, 17)
    def draw(self, window, x, y):
        window.blit(self.image, (x,y))
        if self.amount > 1:
            self.amountText = Text(str(self.amount), self.font, 255, 255, 255, 0, 0, 0)
            self.amountText.x = x
            self.amountText.y = y
            self.amountText.draw(window)
        
class Inventory():
    def __init__(self):
        self.items = []
        self.posx = 16
        self.posy = 510
        x = 0
        y = 0
        while x < 10 :
            self.items.append([])
            while y < 2 :
                self.items[x].append(None)
                y += 1
            y = 0
            x += 1
    def draw(self, window):
        x = 0
        y = 0
        while x < 10 :
            while y < 2 :
                if self.items[x][y] != None:
                    self.items[x][y].draw(window, self.posx + x*32, self.posy + y*32)
                y += 1
            y = 0
            x += 1                 

window = pygame.display.set_mode((800,600))

pygame.display.set_caption("My Garden v0.0")

plant1Image = loadImage("img/plant1.png", True)
flower1Image = loadImage("img/flower1.png", True)
lavande1Image = loadImage("img/lavande1.png", True)
puits1Image = loadImage("img/puits1.png", True)

pygame.display.set_icon(puits1Image)

background = loadImage("img/background.png", False)



font = pygame.font.Font(None, 17)

inventaireText = Text("Inventaire", font, 255, 255, 255)
inventaireText.x = 16
inventaireText.y = 490


itemPlant1 = Item("plant1", plant1Image)
itemPlant1.amount = 5

itemFlower1 = Item("flower1", flower1Image)
itemFlower1.amount = 8

inventory = Inventory()
inventory.items[0][0] = itemPlant1
inventory.items[1][0] = itemFlower1

continuer = 1

while continuer:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = 0
        window.blit(background,(0,0))
        inventaireText.draw(window)
        inventory.draw(window)
        pygame.display.flip()



