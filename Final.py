###########################################
# -- In progress                          #
#    different types of land              #
#    shoot across land or not
#    treasure/buffs
# 3. Add animations and sounds            #
#                                         #
# 4. Add background to gameplay messages  #
#                                         #
# 5. Finalize objective/win
#   -Don't try to select your princess
#    after she is freed. No stats or
#     abilities so the game freezes.   
#
#                                         #
#    ##Handled##                          #
#  1. All sprites can currently           #  
#    move outside the play grid           #
#                                         #
# 2. Input delay is "wonky" -check        #
#                                         #      
###########################################

from livewires import games, color
import random

games.init(screen_width = 850, screen_height = 850, fps = 50)

class Grid(games.Sprite):
    null = 0
    ocean = 1
    land = 2
    castle = 3
    images = {null : games.load_image("graphics/grid/emptyGrid.png"),
              ocean : games.load_image("graphics/grid/emptyOcean.png"),
              land : games.load_image("graphics/grid/emptyLand.png"),
              castle : games.load_image("graphics/grid/castle.png")}
   
    def __init__(self, x, y, nature):
        super(Grid, self).__init__(image = Grid.images[nature],
                                    x = x, y = y)
        self.nature = nature
        self.owner = 0

    def die(self):
        self.destroy()

class Shot(games.Sprite):
    image = games.load_image("graphics/shot.png")
    def __init__(self, direction, ship):
        super(Shot, self).__init__(image = Shot.image)
        self.direction = direction
        self.ship = ship
        self.shipAttacked = ship
        self.x = ship.x
        self.y = ship.y
        self.nature = 0
        if self.direction == "up":
            self.dy = -3
            self.dx = 0
            self.angle = 90
        if self.direction == "down":
            self.dy = 3
            self.dx = 0
            self.angle = 270
        if self.direction == "left":
            self.dy =0
            self.dx = -3
            self.angle = 180
        if self.direction == "right":
            self.dy = 0
            self.dx = 3
      
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.angle = self.angle
        for sprite in self.overlapping_sprites:
            if sprite.nature >=5:
                if sprite.owner != self.ship.owner:
                    self.shipAttacked = sprite
                    sprite.HEALTH -= self.ship.ATTACK
                    self.die()

    def die(self):
        if self.shipAttacked.y > 400:
            yOffset = -30
        elif self.shipAttacked.y <= 400:
            yOffset = 30
        damage = games.Message(value = self.ship.ATTACK,
                  size = 30,
                  color = color.red,
                  x = self.shipAttacked.x,
                  y = self.shipAttacked.y + yOffset,
                  lifetime = 2 * games.screen.fps,
                  is_collideable = False)
        games.screen.add(damage)
        self.destroy()

class Treasure(games.Sprite):
    image = games.load_image("graphics/chars/treasure.png")
    nature = 9
    def __init__(self, x, y):
        super(Treasure, self).__init__(image = Treasure.image, x = x, y = y)
    


class Princess(games.Sprite):
    leia = 1
    peach = 2
    helen = 3
    jasmine = 4
    MOVE = 0
    ATTACK = 0
    RANGE = 0
    HEALTH = 1
    NAME = "Princess"
    images = {leia : games.load_image("graphics/chars/freeLeia.png"),
              peach : games.load_image("graphics/chars/freePeach.png"),
              helen : games.load_image("graphics/chars/freeHelen.png"),
              jasmine : games.load_image("graphics/chars/freeJasmine.png")}   
    nature = 8
    def __init__(self, x, y, char, owner, game):
        super(Princess, self).__init__(image = Princess.images[char], x = x, y = y)
        self.game = game

    def update(self):
        for sprite in self.overlapping_sprites:
            if sprite.nature >= 5 and sprite.nature <= 7:
                self.game.gameOver()
    
    
class Ship(games.Sprite):
    hasMoved = False
    hasAttacked = False
    def update(self):
        if self.HEALTH <= 0:
            self.die()
        
            
    def attack(self, direction):
        shot = Shot(direction, self)
        games.screen.add(shot)
        
    def die(self):
        self.destroy()
        
class Cruiser(Ship):
    leia = 1
    peach = 2
    helen = 3
    jasmine = 4
    MOVE = 5
    ATTACK = 2
    RANGE = 6
    HEALTH = 3
    NAME = "Cruiser"
    images = {leia : games.load_image("graphics/ships/1/Cruiser.png"),
              peach : games.load_image("graphics/ships/2/Cruiser.png"),
              helen : games.load_image("graphics/ships/3/Cruiser.png"),
              jasmine : games.load_image("graphics/ships/4/Cruiser.png")}
    def __init__(self, x, y, char, owner, other, game):
        super(Cruiser, self).__init__(image = Cruiser.images[char], x = x, y = y)
        self.nature = 5
        self.owner = owner
        self.game = game
              
class Destroyer(Ship):
    leia = 1
    peach = 2
    helen = 3
    jasmine = 4
    MOVE = 3
    ATTACK = 3
    RANGE = 4
    HEALTH = 5
    NAME = "Destroyer"
    images = {leia : games.load_image("graphics/ships/1/Destroyer.png"),
              peach : games.load_image("graphics/ships/2/Destroyer.png"),
              helen : games.load_image("graphics/ships/3/Destroyer.png"),
              jasmine : games.load_image("graphics/ships/4/Destroyer.png")}
    def __init__(self, x, y, char, owner, other, game):
        super(Destroyer, self).__init__(image = Destroyer.images[char], x = x, y = y)
        self.nature = 6
        self.owner = owner
        self.game = game
                
class Carrier(Ship):
    leia = 1
    peach = 2
    helen = 3
    jasmine = 4
    MOVE = 2
    ATTACK = 1
    RANGE = 10
    HEALTH = 10
    NAME = "Carrier"
    images = {leia : games.load_image("graphics/ships/1/Carrier.png"),
              peach : games.load_image("graphics/ships/2/Carrier.png"),
              helen : games.load_image("graphics/ships/3/Carrier.png"),
              jasmine : games.load_image("graphics/ships/4/Carrier.png")}
    def __init__(self, x, y, char, owner, other, game):
        super(Carrier, self).__init__(image = Carrier.images[char], x = x, y = y)
        self.char = char
        self.other = other
        self.nature = 7
        self.owner = owner
        self.game = game

    def die(self):
        self.destroy()
        self.createPrincess()

    def createPrincess(self):
        p = Princess(self.x, self.y, self.other, self.owner, self.game)
        games.screen.add(p)
        
        

class Menu(games.Sprite):
    image = games.load_image("graphics/menuBackground.png", transparent = False)
    def __init__(self, sprite):
        if sprite.x < 100:
            menuX = 100
        if sprite.y < 200:
            menuY = 200
        if sprite.x > 750:
            menuX = 750
        if sprite.y > 650:
            menuY = 650
        if sprite.x >= 100 and sprite.x <= 750:
            menuX = sprite.x
        if sprite.y >= 200 and sprite.y <= 650:
            menuY = sprite.y
            
        super(Menu, self).__init__(image = Menu.image,
                                   x = menuX,
                                   y = menuY)
        self.sprite = sprite
        self.nature = 0
        
class GamePointer(games.Sprite):
    image = games.load_image("graphics/gamePointer.png")
    inputDelay = 25
    def __init__(self, menu, messageArray, selector, turn, game):
         super(GamePointer, self).__init__(image = GamePointer.image,
                                       x = menu.x - 65, y = menu.y + 71)
         self.nature = 0
         self.menu = menu
         self.messageArray = messageArray
         self.selector = selector
         self.turn = turn
         self.game = game

    def update(self):
        if self.inputDelay > 0:
            self.inputDelay -= 1
        else:
            if self.y == self.menu.y + 31:
                if games.keyboard.is_pressed(games.K_SPACE):
                    self.close()
                    self.selector.moveShip()
                    self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_DOWN):
                    self.y += 20
                    self.inputDelay = 25
            elif self.y == self.menu.y + 51:
                if games.keyboard.is_pressed(games.K_UP):
                    self.y -= 20
                    self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_DOWN):
                    self.y += 20
                    self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_SPACE):
                    self.close()
                    self.selector.attack()
                    self.inputDelay = 25
            elif self.y == self.menu.y + 71:
                if self.turn:
                    if games.keyboard.is_pressed(games.K_UP):
                        self.y -= 20
                        self.inputDelay = 25
                    if games.keyboard.is_pressed(games.K_DOWN):
                        self.y += 20
                        self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_SPACE):
                    self.close()
                    self.inputDelay = 25
            elif self.y == self.menu.y + 91:
                if games.keyboard.is_pressed(games.K_UP):
                    self.y -= 20
                    self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_SPACE):
                    self.endTurn()
                    self.inputDelay = 25
                    
    def close(self):
        for message in self.messageArray:
            message.destroy()
        self.destroy()
        self.menu.destroy()
        self.selector.inputDelay = 25
        self.selector.canMove = True

    def endTurn(self):
        count = 0
        winner = 0
        if self.game.playerTurn == 1:
            self.game.playerTurn = 2
            for ship in self.game.p2Ships:
                ship.hasMoved = False
                ship.hasAttacked = False
            for ship in self.game.p1Ships:
                count += 1
                winner = 2
        else:
            self.game.playerTurn = 1
            for ship in self.game.p1Ships:
                ship.hasMoved = False
                ship.hasAttacked = False
            for ship in self.game.p2Ships:
                count += 1
                winner = 2

        if count == 0:
            self.game.gameOver(winner)

        player_switch = games.Message(value = "Player " + str(self.game.playerTurn) + " Turn",
                              size = 65,
                              color = color.black,
                              x = games.screen.width/2,
                              y = games.screen.height/2,
                              lifetime = 3 * games.screen.fps,
                              is_collideable = False)
        games.screen.add(player_switch)
        self.close()
  
    def die(self):
        self.destroy()

class TargettingCursor(games.Sprite):
    image = games.load_image("graphics/target.png")

    def __init__(self, x, y, ship, selector):
        super(TargettingCursor, self).__init__(image = TargettingCursor.image,
                                               x = x,
                                               y = y)
        self.nature = 0
        self.inputDelay = 25
        self.selector = selector
        self.shipAttacking = ship

    def update(self):
        if self.inputDelay > 0:
            self.inputDelay -= 1
        elif self.inputDelay == 0:
            if self.y == self.selector.y:
                if games.keyboard.is_pressed(games.K_LEFT) and self.x > 50:
                    self.x = self.x - 50
                    self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_RIGHT) and self.x < 800:
                    self.x = self.x + 50
                    self.inputDelay = 25
            if self.x == self.selector.x:
                if games.keyboard.is_pressed(games.K_UP) and self.y > 50:
                    self.y = self.y - 50
                    self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_DOWN) and self.y < 800:
                    self.y = self.y + 50
                    self.inputDelay = 25
            if games.keyboard.is_pressed(games.K_c):
                self.destroy()
                self.selector.canMove = True
                self.shipAttacking.hasAttacked = False
            if games.keyboard.is_pressed(games.K_SPACE):
                self.lowest = 0
                for sprite in self.overlapping_sprites:
                    self.lowest += 1
                moveSum = abs(self.x - self.selector.x)/50 + abs(self.y - self.selector.y)/50
                if moveSum <= self.shipAttacking.RANGE and self.overlapping_sprites[self.lowest - 1].nature >= 5 and self.overlapping_sprites[self.lowest - 1].owner != self.shipAttacking.owner:
                    directionX = self.x - self.selector.x
                    directionY = self.y - self.selector.y
                    if directionX < 0:
                        direction = "left"
                    elif directionX > 0:
                        direction = "right"
                    if directionY < 0:
                        direction = "up"
                    elif directionY > 0:
                        direction = "down"
                    self.destroy()
                    self.selector.canMove = True
                    self.shipAttacking.attack(direction)
                    self.shipAttacking.hasAttacked = True
                    self.inputDelay = 25
                    self.selector.inputDelay = 25
                else:
                    out_of_range = games.Message(value = "Invalid Target!",
                              size = 40,
                              color = color.black,
                              x = games.screen.height/2,
                              y = games.screen.width/2,
                              lifetime = 2 * games.screen.fps,
                              is_collideable = False)
                    games.screen.add(out_of_range)
                self.inputDelay = 25

        
class MovePointer(games.Sprite):
    image = games.load_image("graphics/movePointer.png")

    def __init__(self, x, y, ship, selector):
        super(MovePointer, self).__init__(image = MovePointer.image,
                                          x = x,
                                          y = y)
        self.nature = 0
        self.shipToMove = ship
        self.inputDelay = 25
        self.selector = selector
        self.lowest = 0

    def update(self):
        if self.inputDelay > 0:
            self.inputDelay -= 1
        elif self.inputDelay == 0:
            if games.keyboard.is_pressed(games.K_LEFT) and self.x > 50:
                self.x = self.x - 50
                self.inputDelay = 25
            if games.keyboard.is_pressed(games.K_RIGHT) and self.x < 800:
                self.x = self.x + 50
                self.inputDelay = 25
            if games.keyboard.is_pressed(games.K_UP) and self.y > 50:
                self.y = self.y - 50
                self.inputDelay = 25
            if games.keyboard.is_pressed(games.K_DOWN) and self.y < 800:
                self.y = self.y + 50
                self.inputDelay = 25
            if games.keyboard.is_pressed(games.K_c):
                self.destroy()
                self.shipToMove.hasMoved == False
                self.selector.canMove = True
            if games.keyboard.is_pressed(games.K_SPACE):
                self.lowest = 0
                for sprite in self.overlapping_sprites:
                    self.lowest += 1
                moveSum = abs(self.x - self.selector.x)/50 + abs(self.y - self.selector.y)/50
                if moveSum <= self.shipToMove.MOVE and self.overlapping_sprites[self.lowest - 1].nature == 1 or self.overlapping_sprites[self.lowest-1].nature == 8:
                    self.destroy()
                    self.shipToMove.hasMoved = True
                    self.selector.canMove = True
                    self.shipToMove.x = self.x
                    self.shipToMove.y = self.y
                    self.shipToMove.hasMoved = True
                else:
                    out_of_range = games.Message(value = "Move out of range!",
                              size = 40,
                              color = color.black,
                              x = games.screen.height/2,
                              y = games.screen.width/2,
                              lifetime = 2 * games.screen.fps,
                              is_collideable = False)
                    games.screen.add(out_of_range)
                self.inputDelay = 25
                

class Selector(games.Sprite):
    leia = 1
    peach = 2
    helen = 3
    jasmine = 4
    images = {leia : games.load_image("graphics/selector1.png"),
              peach : games.load_image("graphics/selector2.png"),
              helen : games.load_image("graphics/selector3.png"),
              jasmine : games.load_image("graphics/selector4.png")}
    inputDelay = 10
    
    def __init__(self, x, y, Game):
        super(Selector, self).__init__(image = Selector.images[1],
                                       x = x,
                                       y = y)
        self.inputDelay = Selector.inputDelay
        self.game = Game
        self.canMove = True
        self.nature = 0
        
    def update(self):
        if self.game.playerTurn == 1:
            self.image = self.images[self.game.player1]
        else:
            self.image = self.images[self.game.player2]

        if self.inputDelay > 0:
            self.inputDelay -= 1
        elif self.inputDelay == 0 and self.canMove:
            if games.keyboard.is_pressed(games.K_LEFT) and self.x > 50:
                self.x = self.x - 50
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_RIGHT) and self.x < 800:
                self.x = self.x + 50
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_UP) and self.y > 50:
                self.y = self.y - 50
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_DOWN) and self.y < 800:
                self.y = self.y + 50
                self.inputDelay = 10
            if games.keyboard.is_pressed(games.K_SPACE):
                for sprite in self.overlapping_sprites:
                    if sprite.nature >= 5:
                        if sprite.owner == self.game.playerTurn:
                            self.turnMenu(sprite)
                        else:
                            self.statusMenu(sprite)
                self.inputDelay = 25

    def attack(self):
        self.canMove = False
        self.inputDelay = 25
        for sprite in self.overlapping_sprites:
            if sprite.nature > 4:
                shipAttacking = sprite
        if shipAttacking.hasAttacked == False:
            tc = TargettingCursor(self.x, self.y, shipAttacking, self)
            games.screen.add(tc)
        else:
            already_attacked = games.Message(value = "Ship already attacked.",
                          size = 65,
                          color = color.black,
                          x = games.screen.width/2,
                          y = games.screen.height/2,
                          lifetime = 3 * games.screen.fps,
                          is_collideable = False)
            games.screen.add(already_attacked)
            self.canMove = True

    def moveShip(self):
        self.canMove = False
        self.inputDelay = 25
        for sprite in self.overlapping_sprites:
            if sprite.nature > 4:
                shipToMove = sprite
        if shipToMove.hasMoved == False:
            movePointer = MovePointer(self.x, self.y, shipToMove, self)
            games.screen.add(movePointer)
        else:
            already_moved = games.Message(value = "Ship already moved.",
                          size = 65,
                          color = color.black,
                          x = games.screen.width/2,
                          y = games.screen.height/2,
                          lifetime = 3 * games.screen.fps,
                          is_collideable = False)
            games.screen.add(already_moved)
            self.canMove = True
                    
                
    def turnMenu(self, sprite):
        self.canMove = False
        messageArray = []
        tMenu = Menu(sprite)
        games.screen.add(tMenu)
        c = games.Text(value = "Class: " + tMenu.sprite.NAME,
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 75,
                        top = tMenu.y - 115,
                        is_collideable = False)
        messageArray.append(c)
        o = games.Text(value = "Owner: player " + str(tMenu.sprite.owner),
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 75,
                        top = tMenu.y - 95,
                        is_collideable = False)
        messageArray.append(o)
        h = games.Text(value = "Health: " + str(tMenu.sprite.HEALTH),
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 75,
                        top = tMenu.y - 75,
                        is_collideable = False)
        messageArray.append(h)
        m = games.Text(value = "Move: " + str(tMenu.sprite.MOVE),
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 75,
                        top = tMenu.y - 55,
                        is_collideable = False)
        messageArray.append(m)
        a = games.Text(value = "Attack: " + str(tMenu.sprite.ATTACK),
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 75,
                        top = tMenu.y - 35,
                        is_collideable = False)
        messageArray.append(a)
        r = games.Text(value = "Range: " + str(tMenu.sprite.RANGE),
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 75,
                        top = tMenu.y - 15,
                        is_collideable = False)
        messageArray.append(r)
        options = games.Text(value = "--- Options ---",
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 75,
                        top = tMenu.y,
                        is_collideable = False)
        messageArray.append(options)
        Move = games.Text(value = "Move",
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 50,
                        top = tMenu.y + 25,
                        is_collideable = False)
        messageArray.append(Move)
        Attack = games.Text(value = "Attack",
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 50,
                        top = tMenu.y + 45,
                        is_collideable = False)
        messageArray.append(Attack)
        Close = games.Text(value = "Close",
                        size = 20,
                        color = color.white,
                        left = tMenu.x - 50,
                        top = tMenu.y + 65,
                        is_collideable = False)
        messageArray.append(Close)
        EndTurn = games.Text(value = "End Turn",
                             size = 20,
                             color = color.white,
                             left = tMenu.x - 50,
                             top = tMenu.y + 85,
                             is_collideable = False)
        messageArray.append(EndTurn)
        for message in messageArray:
            games.screen.add(message)
        pointer = GamePointer(tMenu, messageArray, self, True, self.game)
        games.screen.add(pointer)

    def statusMenu(self, sprite):
        self.canMove = False
        messageArray = []
        sMenu = Menu(sprite)
        games.screen.add(sMenu)
        c = games.Text(value = "Class: " + sMenu.sprite.NAME,
                        size = 20,
                        color = color.white,
                        left = sMenu.x - 75,
                        top = sMenu.y - 115,
                        is_collideable = False)
        messageArray.append(c)
        o = games.Text(value = "Owner: player " + str(sMenu.sprite.owner),
                        size = 20,
                        color = color.white,
                        left = sMenu.x - 75,
                        top = sMenu.y - 95,
                        is_collideable = False)
        messageArray.append(o)
        h = games.Text(value = "Health: " + str(sMenu.sprite.HEALTH),
                        size = 20,
                        color = color.white,
                        left = sMenu.x - 75,
                        top = sMenu.y - 75,
                        is_collideable = False)
        messageArray.append(h)
        m = games.Text(value = "Move: " + str(sMenu.sprite.MOVE),
                        size = 20,
                        color = color.white,
                        left = sMenu.x - 75,
                        top = sMenu.y - 55,
                        is_collideable = False)
        messageArray.append(m)
        a = games.Text(value = "Attack: " + str(sMenu.sprite.ATTACK),
                        size = 20,
                        color = color.white,
                        left = sMenu.x - 75,
                        top = sMenu.y - 35,
                        is_collideable = False)
        messageArray.append(a)
        r = games.Text(value = "Range: " + str(sMenu.sprite.RANGE),
                        size = 20,
                        color = color.white,
                        left = sMenu.x - 75,
                        top = sMenu.y - 15,
                        is_collideable = False)
        messageArray.append(r)
        Close = games.Text(value = "Close",
                        size = 20,
                        color = color.white,
                        left = sMenu.x - 50,
                        top = sMenu.y + 65,
                        is_collideable = False)
        messageArray.append(Close)
        for message in messageArray:
            games.screen.add(message)
        pointer = GamePointer(sMenu, messageArray, self, False, self.game)
        games.screen.add(pointer)
                
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
        
class PlayerSelector(games.Sprite):
    p1 = 1
    p2 = 2
    images = {p1 : games.load_image("graphics/chars/charSelector.png"),
              p2 : games.load_image("graphics/chars/charSelector2.png")}
    inputDelay = 25
    selected = None
    character = ""
    def __init__(self, game, x, y, selector):
        super(PlayerSelector, self).__init__(image = PlayerSelector.images[selector],
                                       x = x,
                                       y = y)
        self.inputDelay = PlayerSelector.inputDelay
        self.game = game
        self.selector = selector

    def update(self):
        if self.inputDelay > 0:
            self.inputDelay -= 1
        else:
            if self.selected == None:
                if games.keyboard.is_pressed(games.K_LEFT):
                    if self.x - 200 > 0:
                        self.x = self.x - 200
                        self.inputDelay = 15
                if games.keyboard.is_pressed(games.K_RIGHT):
                    if self.x + 200 < 850:
                        self.x = self.x + 200
                        self.inputDelay = 15
                if games.keyboard.is_pressed(games.K_SPACE):
                    self.inputDelay = 15
                    if self.x == 125:
                        self.selected = 1
                        self.character = "Leia"
                        self.die()
                    if self.x == 325:
                        self.selected = 2
                        self.character = "Peach"
                        self.die()
                    if self.x == 525:
                        self.selected = 3
                        self.character = "Helen of Troy"
                        self.die()
                    if self.x == 725:
                        self.selected = 4
                        self.character = "Jasmine"
                        self.die()

    def die(self):
        if (self.selector == 1):
            self.game.player1 = self.selected
            self.game.p1_message.value += self.character
            self.game.p1_message.left = 325
            self.game.player2Select()
        elif (self.selector == 2):
            self.game.player2 = self.selected
            self.game.p2_message.value += self.character
            self.game.p2_message.left = 325
            self.game.transition1()
        self.destroy()

class Pointer(games.Sprite):
    image = games.load_image("graphics/menuPointer.png")
    inputDelay = 25
    def __init__(self, game, x, y):
         super(Pointer, self).__init__(image = Pointer.image,
                                       x = x, y = y)
         self.game = game

    def update(self):
        if self.inputDelay > 0:
            self.inputDelay -= 1
        else:
            if self.y == 695:
                if games.keyboard.is_pressed(games.K_UP):
                    self.y = self.y - 50
                    self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_SPACE):
                    print("Exit")
                    self.inputDelay = 25
            if self.y == 645:
                if games.keyboard.is_pressed(games.K_DOWN):
                    self.y = self.y + 50
                    self.inputDelay = 25
                if games.keyboard.is_pressed(games.K_SPACE):
                    self.game.player1Select()
                    self.die()
                    self.inputDelay = 25

    def die(self):
        self.destroy()

class Enter(games.Sprite):
    image = games.load_image("graphics/enter.png")
    delay = 50
    def __init__(self, game, x, y, dest):
        super(Enter, self).__init__(image = Enter.image, x = x, y = y)
        self.game = game
        self.dest = dest

    def update(self):
        if self.delay > 0:
            self.delay -= 1
        else:
            if games.keyboard.is_pressed(games.K_p):
                if self.dest == 0:
                    self.game.transition2()
                if self.dest == 1:
                    self.game.load()
                self.destroy()
            
                    
class Game(object):
    """ the game """
    def __init__(self):
        self.p1Ships = []
        self.player1 =  None
        self.p1_message = games.Text(value = "Player 1: ",
                                       size = 50,
                                       color = color.green,
                                       left = 325,
                                       top = 500)
        self.p2Ships = []
        self.player2 = None
        self.p2_message = games.Text(value = "Player 2: ",
                                       size = 50,
                                       color = color.blue,
                                       left = 325,
                                       top = 555)
        self.newGame = None
        self.game_background = games.load_image("graphics/testBack.png", transparent = False)
        self.playerTurn = 1
        
        
    def titleScreen(self):
        title_background = games.load_image("graphics/menuMain.png", transparent = False)
        games.screen.background = title_background
        pointer = Pointer(game = self, x = 370, y = 695)
        games.screen.add(pointer)
        games.screen.mainloop()

    def player1Select(self):
        playerSelect_background = games.load_image("graphics/menuCharSelect.png", transparent = False)
        games.screen.background = playerSelect_background
        for i in range(4):
            char = CharacterIcon(x = 125 + (200 * i), y = 295, character = i + 1)
            games.screen.add(char)
        games.screen.add(self.p1_message)
        games.screen.add(self.p2_message)
        selector = PlayerSelector(game = self, x= 125, y = 294, selector = 1)
        games.screen.add(selector)

    def player2Select(self):
        playerSelect_background = games.load_image("graphics/menuCharSelect.png", transparent = False)
        games.screen.background = playerSelect_background
        for i in range(4):
            char = CharacterIcon(x = 125 + (200 * i), y = 295, character = i + 1)
            games.screen.add(char)
        selector = PlayerSelector(game = self, x= 125, y = 294, selector = 2)
        games.screen.add(selector)

    def transition1(self):
        cont = games.Text(value = "Press [P] to begin",
                  size = 15,
                  color = color.white,
                  left = 325,
                  top = 610)
        games.screen.add(cont)

        ent = Enter(game = self, x = 800, y = 800, dest = 0)
        games.screen.add(ent)


    def transition2(self):
        games.screen.clear()
        game_background = games.load_image("graphics/testBack.png", transparent = False)
        games.screen.background = game_background
        p1Char = CharacterIcon(x = 125, y = 195, character = self.player1)
        games.screen.add(p1Char)
        p2Char = CharacterIcon(x = 725, y = 655, character = self.player2)
        games.screen.add(p2Char)
        Vs = games.Text(value = "Versus!",
                        size = 75,
                        color = color.white,
                        left = 300,
                        top = 400)
        games.screen.add(Vs)
        cont = games.Text(value = "Press [P] to begin",
                          size = 15,
                          color = color.white,
                          left = 300,
                          top = 480)
        games.screen.add(cont)

        ent = Enter(game = self, x = 800, y = 800, dest = 1)
        games.screen.add(ent)
        

    def load(self):
        games.screen.clear()
        #create empty grid
        x = 0
        y = 0
        northCount = 5
        southCount = 0
        count = 0
        
        #add basic Ocean grid
        for i in range(16):
            x = x + 50
            y = 0
            for j in range(16):
                y = y + 50
                grid = Grid(x, y, nature = 1)
                games.screen.add(grid)

        #add north land bank
        x = 0
        y = 0
        for i in range(5):
            x = x + 50
            y = 0
            for j in range(5 - i):
                y = y + 50
                if i == 2 and j == 2:
                    grid = Grid(x, y, nature = 3)
                    games.screen.add(grid)
                    for sprite in grid.overlapping_sprites:
                        if sprite.nature < 2:
                            sprite.die()
                else: 
                    grid = Grid(x, y, nature = 2)
                    games.screen.add(grid)
                    for sprite in grid.overlapping_sprites:
                        if sprite.nature < 2:
                            sprite.die()
        

        #add south land bank
        x = 850
        y = 850
        for i in range(5):
            x -= 50
            y = 850
            for j in range(5 - i):
                y -= 50
                if i == 2 and j == 2:
                    grid = Grid(x, y, nature = 3)
                    games.screen.add(grid)
                    for sprite in grid.overlapping_sprites:
                        if sprite.nature < 2:
                            sprite.die()
                else: 
                    grid = Grid(x, y, nature = 2)
                    games.screen.add(grid)
                    for sprite in grid.overlapping_sprites:
                        if sprite.nature < 2:
                            sprite.die()                    

        #add central island
        i = 250
        j = 250
        for i in range(250,600,50):
            for j in range(250,600,50):
                ran = random.randrange(10)
                if ran <= 3:
                    island = Grid(i, j, nature = 2)
                    games.screen.add(island)
                    for sprite in island.overlapping_sprites:
                        sprite.die()
        

        #add p1 ships
        cru1 = Cruiser(100, 250, self.player1, 1, self.player2, self)
        self.p1Ships.append(cru1)
        cru2 = Cruiser(250, 100, self.player1, 1, self.player2, self)
        self.p1Ships.append(cru2)
        car1 = Carrier(200, 150, self.player1, 1, self.player2, self)
        self.p1Ships.append(car1)
        des1 = Destroyer(150, 200, self.player1, 1, self.player2, self)
        #des1 = Destroyer(600, 700, self.player1, 1, self.player2, self)
        self.p1Ships.append(des1)
        for ship in self.p1Ships:
            games.screen.add(ship)

        #add p2 ships
        cru1 = Cruiser(750, 600, self.player2, 2, self.player1, self)
        self.p2Ships.append(cru1)
        cru2 = Cruiser(600, 750, self.player2, 2, self.player1, self)
        self.p2Ships.append(cru2)
        car1 = Carrier(650, 700, self.player2, 2, self.player1, self)
        self.p2Ships.append(car1)
        des1 = Destroyer(700, 650, self.player2, 2, self.player1, self)
        self.p2Ships.append(des1)

        for ship in self.p2Ships:
            games.screen.add(ship)
        #add selection curser
        wall_image = games.load_image("graphics/testBack.png", transparent = False)
        games.screen.background = wall_image
        self.play()

    def gameOver(winner):
        gameOver = games.load_image("graphics/gameover.png", transparent = False)
        games.screen.clear()
        games.screen.background = gameOver
        

    def play(self):
        x = 450
        y = 450
        selector = Selector(x, y, self)
        games.screen.add(selector)

def main():
    gameStart = Game()
    gameStart.titleScreen()

main()
