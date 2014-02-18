
from livewires import games, color
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
        #self.destroy()
        print("don't destroy lowest level grid")
    
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
                destroyer = Destroyer(self.x, self.y)
                games.screen.add(destroyer)
                self.elevate()
                self.inputDelay = 10

class PlayerSelector(games.Sprite):
    player1 = 1
    player2 = 2
    images = {player1 : games.load_image("graphics/chars/charSelector.png"),
              player2 : games.load_image("graphics/chars/charSelector2.png")}
    inputDelay = 10
    selected = None
    def __init__(self, x, y, player):
        super(PlayerSelector, self).__init__(image = PlayerSelector.images[player],
                                       x = x,
                                       y = y)
        self.inputDelay = PlayerSelector.inputDelay

    def update(self):
        if self.inputDelay > 0:
            self.inputDelay -= 1
        else:
            if self.selected == None:
                if games.keyboard.is_pressed(games.K_LEFT):
                    if self.x - 200 > 0:
                        self.x = self.x - 200
                        self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_RIGHT):
                    if self.x + 200 < 850:
                        self.x = self.x + 200
                        self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_SPACE):
                    if self.x == 125:
                        self.selected = 1
                        print("Character selected = Leia")
                        self.inputDelay = 25
                    if self.x == 325:
                        self.selected = 2
                        print("Character selected = Peach")
                        self.inputDelay = 25
                    if self.x == 525:
                        self.selected = 3
                        print("Character selected = Helen")
                        self.inputDelay = 25
                    if self.x == 725:
                        self.selected = 4
                        print("Character selected = Jasmine")
                        self.inputDelay = 25
            else:
                self.destroy()

class CharacterIcon(games.Sprite):
    leia = 1
    peach = 2
    helen = 3
    jasmine = 4
    images = {leia : games.load_image("graphics/chars/charSelectLeia.png", transparent = False),
              peach : games.load_image("graphics/chars/charSelectPeach.png", transparent = False),
              helen : games.load_image("graphics/chars/charSelectHelen.png", transparent = False),
              jasmine : games.load_image("graphics/chars/charSelectJasmine.png", transparent = False)}
    def __init__(self, x, y, character):
        super(CharacterIcon, self).__init__(
            image = CharacterIcon.images[character],
            x = x, y = y)
                     

        
class Pointer(games.Sprite):
    image = games.load_image("graphics/menuPointer.png")
    inputDelay = 25
    def __init__(self, x, y):
         super(Pointer, self).__init__(image = Pointer.image,
                                       x = x, y = y)

    def update(self):
        if self.inputDelay > 0:
            self.inputDelay -= 1
        else:
            if self.y == 695:
                if games.keyboard.is_pressed(games.K_UP):
                    self.y = self.y - 50
                    self.inputDelay = 10
                if games.keyboard.is_pressed(games.K_SPACE):
                    print("Exit")
                    self.inputDelay = 25
            if self.y == 645:
                if games.keyboard.is_pressed(games.K_DOWN):
                    self.y = self.y + 50
                    self.inputDelay = 10
                if games.keyboard.is_pressed(games.K_SPACE):
                    self.playerSelect()
                    self.die()
                    self.inputDelay = 25

    def playerSelect(self):
        charSelectBackground = games.load_image("graphics/menuCharSelect.png")
        games.screen.background = charSelectBackground

        for i in range(4):
            char = CharacterIcon(x = 125 + (200 * i), y = 295, character = i + 1)
            games.screen.add(char)

        player_message = games.Text(value = "Player 1 Select",
                                       size = 50,
                                       color = color.yellow,
                                       x = 325,
                                       y = 500)
        games.screen.add(player_message)
            
        p1Selector = PlayerSelector(x = 125, y = 294, player = 1)
        games.screen.add(p1Selector)

        
        p2Selector = PlayerSelector(x = 125, y = 294, player = 2)
        games.screen.add(p2Selector)

            
    def newGame(self):
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
        
    def die(self):
        self.destroy()

class Game(object):
    """the game"""
    def __init__(self):
        #create empty grid
        background = games.load_image("graphics/menuMain.png")

    def mainMenu(self):
        wall_image = games.load_image("graphics/menuMain.png", transparent = False)
        games.screen.background = wall_image
        pointer = Pointer(x = 370, y = 695)
        games.screen.add(pointer)
        games.screen.mainloop()

def main():
    gameStart = Game()
    gameStart.mainMenu()
    #menuStart = Menu()
    #menuStart.menu()
    

main()
