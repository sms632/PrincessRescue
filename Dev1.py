
from livewires import games
import random

games.init(screen_width = 850, screen_height = 850, fps = 50)

class Grid(games.Sprite):
    image = games.load_image("graphics/emptyGrid.png")
    name = "Empty"

    def __init__(self, x, y):
        super(Grid, self).__init__(image = Grid.image,
                                    x = x, y = y)
        self.name = Grid.name

    def die(self):
        self.destroy()
    
class Ocean(games.Sprite):
    image = games.load_image("graphics/emptyOcean.png")
    canMove = True
    name = "Ocean"

    def __init__(self, x, y):
        super(Ocean, self).__init__(image = Ocean.image,
                                    x = x,
                                    y = y)
        self.name = Ocean.name

class Land(games.Sprite):
    image = games.load_image("graphics/emptyLand.png")
    canMove = False
    name = "Land"

    def __init__(self, x, y):
        super(Land, self).__init__(image = Land.image,
                                    x = x,
                                    y = y)
        self.name = Land.name

class Ship(games.Sprite):
    """ A player controlled ship"""
    canMove = True
    
    def die(self):
        self.destroy()

class Cruiser(Ship):

    def die(self):
        self.destroy()

class Carrier(Ship):
    def die(self):
        self.destroy()

class Destroyer(Ship):
    image = games.load_image("graphics/ships/Leia/Destroyer.png")
    name = "Destroyer"
    
    def __init__(self, x, y):
        super(Destroyer, self).__init__(image = Destroyer.image,
                                        x = x,
                                        y = y)
        self.name = Destroyer.name
    def die(self):
        self.destroy()
    
        

        
class Selector(games.Sprite):
    image = games.load_image("graphics/selector.png")
    inputDelay = 10
    def __init__(self, Grid):
        super(Selector, self).__init__(image = Selector.image,
                                       x = Grid.x,
                                       y = Grid.y)
        self.inputDelay = Selector.inputDelay
        
    def update(self):
        if self.inputDelay > 0:
            self.inputDelay -= 1
        elif self.inputDelay == 0:
            if games.keyboard.is_pressed(games.K_LEFT):
                self.x = self.x - 50
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_RIGHT):
                self.x = self.x + 50
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_UP):
                self.y = self.y - 50
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_DOWN):
                self.y = self.y + 50
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_SPACE):
                print(self.overlapping_sprites[0].name)
                print(self.x)
                print(self.y)
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_d):
                for sprite in self.overlapping_sprites:
                    sprite.die()
            #add ocean at curser
            if games.keyboard.is_pressed(games.K_o):
                ocean = Ocean(self.x, self.y)
                games.screen.add(ocean)
                self.elevate()
                self.inputDelay = 10
            #add land at curser
            if games.keyboard.is_pressed(games.K_p):
                land = Land(self.x, self.y)
                games.screen.add(land)
                self.elevate()
                self.inputDelay = 10
            #add destroyer
            if games.keyboard.is_pressed(games.K_i):
                des = Destroyer(self.x, self.y)
                games.screen.add(des)
                self.elevate()
                self.inputDelay = 10
                
                
            
        


class Pointer(object):
    def __init__(self):
         background = games.load_image("graphics/pointer.png", transparent = False)       

class Menu(object):
    def __init__(self):
        background = games.load_image("graphics/menuBackground.png", transparent = False)

    def show(self):
        games.screen.add(background)

class Game(object):
    """the game"""
       
                
    def newGameMenu(self):
        menu_image = games.load_image("graphics/MenuBackground.png", transparent = False)

    def play(self):
        #create empty grid
        x = 0
        y = 0
        

        #add basic grid
        for i in range(16):
            x = x + 50
            y = 0
            for j in range(16):
                y = y + 50
                grid = Grid(x, y)
                games.screen.add(grid)
                
        #add selection curser
        selector = Selector(grid)
        games.screen.add(selector)
        wall_image = games.load_image("graphics/testBack.png", transparent = False)
        games.screen.background = wall_image

        
        games.screen.mainloop()




def main():
    gameStart = Game()
    gameStart.play()
    

main()
