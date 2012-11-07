# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame
import random

pygame.font.init()

def loadImage(imageURL, transparency):
	if transparency == True:
		image = pygame.image.load(imageURL).convert_alpha()
	else:
		image = pygame.image.load(imageURL).convert()
	return image

class Jardin():
    def __init__(self):
        self.terrainList = []
        self.plantList = []
        self.terrainImage = loadImage("img/terrain.png", False)
        self.grassImage = self.terrainImage.subsurface(0,0,32,32)
        self.waterImage = self.terrainImage.subsurface(32,0,32,32)
        x = 0
        y = 0
        while x < 20 :
            self.terrainList.append([])
            while y < 15 :
                self.terrainList[x].append(1)
                y += 1
            y = 0
            x += 1
    def draw(self, window):
        x = 0
        y = 0
        while x < 20 :
            while y < 15 :
                if self.terrainList[x][y] == 0:
                    window.blit(self.waterImage, (x*32, y*32))
                if self.terrainList[x][y] == 1:
                    window.blit(self.grassImage, (x*32, y*32))
                y += 1
            y = 0
            x += 1
        
        x = 0
        y = 0
        while x < 20 :
            while y < 15 :
                if self.plantList[x][y] != None:
                    self.plantList[x][y].draw(window, x, y)
                y += 1
            y = 0
            x += 1
    def generateBetaTerrain(self):
        x = 0
        y = 0
    	while x < 20 :
            self.plantList.append([])
            while y < 15 :
                self.plantList[x].append(None)
                y += 1
            y = 0
            x += 1
    	
class Plant():
	def __init__(self, name):
		self.name = name
		self.image = loadImage("img/" + name + ".png", True)
	def draw(self, window, x, y):
		window.blit(self.image, (x*32, y*32))


class Text():
    def __init__(self, text, font, red, green, blue, redBack = None, greenBack = None, blueBack = None):
        if (redBack == None and greenBack == None and blueBack == None):
            self.text = font.render(text, True, (red, green, blue))
        else:
            self.text = font.render(text, True, (red, green, blue), (redBack, greenBack, blueBack))
        self.x = 0
        self.y = 0
    def setTextPosition(self, x, y):
    	self.x = x
    	self.y = y    	
    def draw(self, window):
        window.blit(self.text,(self.x,self.y))

class Item():
    def __init__(self, name):
        self.name = name
        self.image = loadImage("img/" + name + ".png", True)
        
        self.amount = 1
        
        self.font = pygame.font.Font(None, 17)
        
        self.absx = None
        self.absy = None
        
    def draw(self, window, x, y):
        window.blit(self.image, (x,y))
        self.absx = x
        self.absy = y
        if self.amount > 1:
            self.amountText = Text(str(self.amount), self.font, 255, 255, 255, 0, 0, 0)
            self.amountText.x = x
            self.amountText.y = y
            self.amountText.draw(window)
    def mouseIsOver(self, mousePosition):
    	condition = False
    	if mousePosition[0] > self.absx and mousePosition[0] < self.absx + 32 and mousePosition[1] > self.absy and mousePosition[1] < self.absy + 32 :
    		condition = True
    	return condition
        
class Inventaire():
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
    def selectFromInventory(self, parent, event):
		if event.type == MOUSEBUTTONDOWN:
			mousePosition = [event.pos[0], event.pos[1]]
	
			if event.button == 1:
				if mousePosition[0] > self.posx and mousePosition[0] < self.posx + 320:
					if mousePosition[1] > self.posy and mousePosition[1] < self.posy + 64:
						x = ((mousePosition[0]+16) - (mousePosition[0]+16)%32)/32-1
						y = ((mousePosition[1]-512) - (mousePosition[1]-512)%32)/32
						if self.items[x][y] != None and self.items[x][y].mouseIsOver(mousePosition) == True:
							parent.gameMode = "putPlant"
							parent.currentSelection = Item(self.items[x][y].name)
							parent.inventoryPositionOfItemSelected = [x, y]
						else:
							parent.gameMode = None                 

class normalGame():
	def __init__(self):
		self.day = 0
		self.font = pygame.font.Font(None, 17)
		
		self.jardin = Jardin()
		self.inventaire = Inventaire()

		self.background = loadImage("img/background.png", False)

		self.inventaire.items[0][0] = Item("plant1")
		self.inventaire.items[0][0].amount = 5
		
		self.inventaire.items[1][0] = Item("lavande1")
		self.inventaire.items[1][0].amount = 8
		
		self.listTexts = {}
		self.listTexts["inventaireText"] = Text("Inventaire", self.font, 255, 255, 255)
		self.listTexts["inventaireText"].setTextPosition(16, 490)
		
		self.listTexts["currentSelection"] = Text("Sélection actuelle".decode('utf-8'), self.font, 255, 255, 255)
		self.listTexts["currentSelection"].setTextPosition(670, 500)
		
		self.jardin.generateBetaTerrain()
		
		self.gameMode = None
		self.currentSelection = None
		self.inventoryPositionOfItemSelected = None
		
	def draw(self, window):
		window.blit(self.background, (0,0))
		self.jardin.draw(window)
		self.inventaire.draw(window)
		self.listTexts["inventaireText"].draw(window)
		self.listTexts["currentSelection"].draw(window)
		if self.gameMode == "putPlant":
			if self.currentSelection != None :				
				self.currentSelection.draw(window, 705, 526)

	def mouseIsOverTheGarden(self, event):
		if event.pos[0] > 0 and event.pos[0] < 640:
			if event.pos[1] > 0 and event.pos[1] < 480:
				return True
	def plantAlreadyPlacedAtThisPosition(self, event):
		mousePosition = [event.pos[0], event.pos[1]]
		x = (mousePosition[0] - mousePosition[0]%32)/32
		y = (mousePosition[1] - mousePosition[1]%32)/32
		if self.jardin.plantList[x][y] == None :
			return True
		else:
			return False

	def putPlantOnGarden(self, event):
		mousePosition = [event.pos[0], event.pos[1]]
		x = (mousePosition[0] - mousePosition[0]%32)/32
		y = (mousePosition[1] - mousePosition[1]%32)/32
		self.jardin.plantList[x][y] = Plant(self.currentSelection.name)
		self.currentSelection = None
		self.gameMode = None

	def removePlantFromInventory(self):
		self.inventaire.items[self.inventoryPositionOfItemSelected[0]][self.inventoryPositionOfItemSelected[1]].amount -= 1
		if self.inventaire.items[self.inventoryPositionOfItemSelected[0]][self.inventoryPositionOfItemSelected[1]].amount == 0:
			self.inventaire.items[self.inventoryPositionOfItemSelected[0]][self.inventoryPositionOfItemSelected[1]] = None
		
	def event(self, event):
		self.inventaire.selectFromInventory(self, event)
		if self.gameMode == "putPlant":
			if event.type == MOUSEBUTTONDOWN:
				if self.mouseIsOverTheGarden(event) == True and self.plantAlreadyPlacedAtThisPosition(event) == True:
					self.putPlantOnGarden(event)
					self.removePlantFromInventory()
					
def normal(window):
	normal = normalGame()
	continuer = 1

	while continuer:
		for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0
			normal.event(event)
			normal.draw(window)
			pygame.display.flip()

def main():
	window = pygame.display.set_mode((800,600))
	pygame.display.set_caption("Mon jardin - v0.0")

	puits1Image = loadImage("img/puits1.png", True)

	pygame.display.set_icon(puits1Image)
	normal(window)

main()
