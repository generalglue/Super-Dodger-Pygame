'''
Name: Victor Li
Date: 5/5/2017
Description:
'''
import pygame, random
pygame.mixer.init()

# Sound effect when the player uses its pickaxe
pickAxeSound = pygame.mixer.Sound("sound/pickAxeHit.wav")
pickAxeSound.set_volume(0.5)

# Sound effect when the player uses its mop
mopSound = pygame.mixer.Sound("sound/mopHit.wav")
mopSound.set_volume(0.5)

class Player(pygame.sprite.Sprite):
    ''' This class defines the sprite the player controls in the game.'''
    
    def __init__(self, screen, yPosition):
        '''This initalizer takes the screen surface as a paraemter, initalizes
        the image and rect attributes and other variables used for the player'''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # List of sprite images used by the class
        self.__playerImage = ['images/playerStandingLeft.gif', 'images/playerStandingRight.gif', 'images/playerLeft.gif', 'images/playerRight.gif', 'images/playerMopRight.gif', 'images/playerMopRight2.gif'\
                              , 'images/playerMopLeft.gif', 'images/playerMopLeft2.gif', 'images/playerAxeRight.gif', 'images/playerAxeRight2.gif', 'images/playerAxeLeft.gif', 'images/playerAxeLeft2.gif', 'images/playerHit.gif']
        
        # Set the image and rect attributes for the player
        self.image = pygame.image.load(self.__playerImage[1])
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2, yPosition)
        
        # Set instance variables
        
        self.__screen = screen
        self.__currentSpeed = 6
        self.__savedSpeed = self.__currentSpeed
        self.__velocity = 0
        self.__currentPosition = self.rect.center
        
        self.__standState = True
        self.__jumpState = False
        self.__axeState = False
        self.__mopState = False
        self.__invincibleState = False
        self.__mineSprite = False
        
        # These variables are returned to check if the player is currently using a mop, pickaxe or none
        self.__animationMop = False
        self.__animationAxe = False
        
        # Posture determines whether the in-between animations should be played on the right/left side in
        # the update() method.
        # 0 = Idle/Walking Left, 1 = Mining/Mopping Left, 2 = Idle/Walking Right, 3 = Mining/Mopping Right 
        self.__posture = 0
        
        # This allows me to count the time for switching sprite images
        self.__startTime = pygame.time.get_ticks()
    
    def go_left(self):
        ''' This method will make the player's sprite go left by the walking speed,
        change the posture and the sprite image.'''
        
        self.image = pygame.image.load(self.__playerImage[2])
        self.rect.left -= self.__currentSpeed
        self.__posture = 2
        
        
     
    def go_right(self):
        ''' This method will make the player's sprite go right by the walking speed,
        change the posture and the sprite image.'''        
        
        self.image = pygame.image.load(self.__playerImage[3])
        self.rect.right += self.__currentSpeed
        self.__posture = 0
        
        
    def slow(self, slowMultipler):
        ''' This method will slow the player's speed multipled by the slowMultipler '''
        self.__currentSpeed = self.__savedSpeed * slowMultipler
        
    def useMop(self):
        '''This method sets the mopState variable to True and changes the posture and 
        sprite image.'''
        
        self.__mopState = True
        if self.__posture == 0:
            self.image = pygame.image.load(self.__playerImage[4])
            self.__posture = 1        
        elif self.__posture == 2:
            self.image = pygame.image.load(self.__playerImage[6])
            self.__posture = 3

    def useAxe(self):
        '''This method sets the axeState variable to True and changes the posture and
        sprite image.'''
        
        self.__axeState = True
        
        if self.__posture == 0:
            self.image = pygame.image.load(self.__playerImage[8])
            
            # Moved the sprite image a little, as the new sprite image is not the same size as the other sprites,
            # There will be would be a noticable shift in the sprite image if not.
            self.rect.right += 8
            
            self.__posture = 1
            
        elif self.__posture == 2:
            self.image = pygame.image.load(self.__playerImage[10])
            
            # Moved the sprite image a little, as the new sprite image is not the same size as the other sprites,
            # There will be would be a noticable shift in the sprite image if not.            
            self.rect.right -= 8
            
            self.__posture = 3

    def jump(self):
        ''' This method will increase its velocity to 25, sets the jumpState to True
        and sets the standState to False'''
        
        self.__standState = False
        self.__jumpState = True
        self.__velocity = 30

    def jumpFall(self, gravity):
        ''' This method makes the player jump/fall by subtracting the player's rect bottom 
        by the velocity and also decreases the velocity by the gravity parameter '''
        
        self.rect.bottom -= self.__velocity
        self.__velocity -= gravity
        
    def getJump(self):
        ''' This method will return the jumpState variable '''
        
        return self.__jumpState
          
    def getStand(self):
        ''' This method will return the standState variable '''
        return self.__standState
    
    def getMop(self):
        ''' This method will return the mopState variable '''
        return self.__animationMop
    
    def getAxe(self):
        ''' This method will return the axeState variable '''
        return self.__animationAxe
    
    def setInvincible(self, stateBool):
        ''' This method will set the invincibleState to a bool based on the parameter '''
        self.__invincibleState = stateBool
        
    def getInvincible(self):
        ''' This method returns the invincibleState variable '''
        return self.__invincibleState
        
    def update(self):
        ''' This method will make the player stay in the screen boundaries, update the sprite image
        for in-between animations while moving, and stop the player from falling.'''
        
        self.__animationMop = False
        self.__animationAxe = False
        
        # If player reached left border, move the player back to the edge
        if (self.rect.left <= 0):
            self.rect.left = 0        
            
        # If player reached right border, move the player back to the edge
        if (self.rect.right >= self.__screen.get_width()):
            self.rect.right = self.__screen.get_width()
        
        # If finished jumping, disable jumping and re-enable jumping, and set the velocity back to 0
        if self.__velocity == -35 and self.__jumpState == True:
            self.__velocity = 0
            self.__jumpState = False
            self.__standState = True        
        
        # If the player is currently invincible, update the sprite image with an invincibility image
        if self.__invincibleState:
            self.image = pygame.image.load(self.__playerImage[12])      
        
        # In-between sprite image switches for left and right walking/idle
        if pygame.time.get_ticks() - self.__startTime >= 250 and (self.__posture == 0 or self.__posture == 2):
            
            # If one of the many mining sprites were blit before walking, move the sprite image based on posture #, 
            # As there would be a noticable shift if not.            
            if self.__mineSprite:
                if self.__posture == 0:
                    self.rect.right -= 13
                else:
                    self.rect.right += 13
                self.__mineSprite = False
                
            # Update with right sided walking sprite images
            if self.__posture == 0:
                self.image = pygame.image.load(self.__playerImage[1])
                
            # Update with left sided walking sprite images
            else:
                self.image = pygame.image.load(self.__playerImage[0])
                
            # Reset the timer
            self.__startTime = pygame.time.get_ticks()
        
        # In-between sprite images for left and right mining/mopping        
        if pygame.time.get_ticks() - self.__startTime >= 500 and (self.__posture == 1 or self.__posture == 3):
            
            # Update with right sided mining/mopping sprite images
            if self.__posture == 1:
                if self.__mopState:
                    self.image = pygame.image.load(self.__playerImage[5])
                    # Moves the sprite so it looks like the player moves during animation
                    self.rect.right += 5
                    self.__animationMop = True
                    mopSound.play()
                elif self.__axeState:
                    self.image = pygame.image.load(self.__playerImage[9])
                    # Moves the sprite so it looks like the player moves during animation
                    self.rect.right += 10
                    self.__mineSprite = True
                    self.__animationAxe = True
                    pickAxeSound.play()
                # Changes the posture to right side walking/idle
                self.__posture = 0
            
            # Update with left sided mining/mopping sprite images    
            if self.__posture == 3:
                if self.__mopState:
                    self.image = pygame.image.load(self.__playerImage[7])
                    # Moves the sprite so it looks like the player moves during animation
                    self.rect.right -= 5
                    self.__animationMop = True
                    mopSound.play()
                elif self.__axeState:
                    self.image = pygame.image.load(self.__playerImage[11])
                    # Moves the sprite so it looks like the player moves during animation
                    self.rect.right -= 10
                    self.__mineSprite = True
                    self.__animationAxe = True
                    pickAxeSound.play()
                # Changes the posture to left side walking/idle
                self.__posture = 2
                
            # Set the axeState variable and mopState variable to False so there will be no iteration
            self.__axeState = False
            self.__mopState = False
            
            # Reset the timer
            self.__startTime = pygame.time.get_ticks()
            
        # Saves the current position of the sprite        
        self.__currentPosition = self.rect.center
        
        # Obtain the new/updated sprite image rect attributes
        self.rect = self.image.get_rect()
        
        # Uses saved position and moves the sprite to that location, as everytime you get_rect(),
        # the sprite will always move back to (0,0)
        self.rect.center = self.__currentPosition
        
class Ground(pygame.sprite.Sprite):
    ''' This class defines the ground sprite used for collision detecting and for the player to
    stand on '''
    
    def __init__(self, screen):
        ''' Initalizer 'takes the screen surface as parameters to set the rect attributes '''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set image and rect attributes for the Ground
        self.image = pygame.image.load('images/ground.gif')
        self.rect = self.image.get_rect()
        self.rect.bottom = screen.get_height()
        self.__topGround = self.rect.top - 31
        
    def returnTopGround(self):
        ''' This method returns the topGround variable '''
        return self.__topGround
    
class LiveCounter(pygame.sprite.Sprite):
    ''' This class defines the live counter which keeps track of the lives remaining'''
    
    def __init__(self):
        ''' Initalizer initalizes the instance variable used to count number of lives '''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # List of sprite images used by the class
        self.__livesImages = ['images/fiveHearts.gif', 'images/fourHearts.gif', 'images/threeHearts.gif', 'images/twoHearts.gif', 'images/oneHeart.gif', 'images/noHeart.gif']
        
        
        # This instance variable counts which image the sprite should load
        self.__animationCount = 0       
        
        # Set the sprite's image and sets the rect attributes
        self.image = pygame.image.load(self.__livesImages[self.__animationCount])
        self.rect = self.image.get_rect()
        self.rect.top = 5        
        
        # Set lives instance variables
        self.__lives = 5
        
    def loseLife(self, live):
        ''' This method will remove a life from the player '''
        for eachTime in range(live):
            if self.__lives > 0:    
                self.__animationCount += 1
                self.__lives -= 1
        
    def gainLife(self):
        ''' This method will add a life to the player '''
        if self.__lives < 5:
            self.__animationCount -= 1
            self.__lives += 1
        
    def getLife(self):
        ''' This method will return the lives variable '''
        return self.__lives
    
    def update(self):
        ''' This method will update the live counter sprite image based on the remaining number of lives '''
        if self.__animationCount >= 0 and self.__animationCount <= 5:
            self.image = pygame.image.load(self.__livesImages[self.__animationCount])
        
class Meteor(pygame.sprite.Sprite):
    ''' This class defines the meteor sprite in which the player has to avoid colliding with '''

    def __init__(self, rowNum, colNum):
        ''' Initalizer takes the rowNum and colNum parameters to set the position of it on the screen '''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)
      
        # List of sprite images used by the class
        self.__meteorImages = ['images/meteorOne.gif', 'images/meteorTwo.gif', 'images/meteorThree.gif', 'images/meteorFour.gif', 'images/meteorFive.gif',\
                           'images/meteorSix.gif', 'images/meteorSeven.gif', 'images/meteorEight.gif', 'images/meteorNine.gif']
    
        # This instance variable counts which image the sprite should load
        self.__animationCount = 0
    
        # Set the sprite's image and sets the rect attributes
        self.image = pygame.image.load(self.__meteorImages[self.__animationCount])
        self.rect = self.image.get_rect()
        self.rect.left = ((colNum)*80)
        
        # Set instance variables
        self.__rowNum = rowNum + 1
        self.setSpeed()
        self.setRespawn(random.randrange(0,2))
        self.reset()
        
    def setSpeed(self):
        ''' This method sets the speed of the meteor '''
        if self.__rowNum == 1:
            self.__meteorSpeed = 5
        elif self.__rowNum == 2:
            self.__meteorSpeed = random.randrange(1,4)
            
    def setRespawn(self, boolSpawn):
        ''' This method sets whether the meteor should respawn on the next impact '''
        if boolSpawn:
            self.__respawn = True
        else:
            self.__respawn = False            
    
    def reset(self):
        ''' This method resets the position of the meteor '''
        self.rect.centery = -78
        
        if self.__rowNum == 1:
            if self.__respawn:
                self.setSpeed()
            else:
                self.__meteorSpeed = 0
                
            self.setRespawn(random.randrange(0,2))
        
        elif self.__rowNum == 2:
                self.setSpeed()
        
    def update(self):
        ''' This method will update the live counter sprite image based on the remaining number of lives
        and will update the y position based on the meteor speed'''
        
        self.__animationCount += 1
        
        self.image = pygame.image.load(self.__meteorImages[self.__animationCount])
        if self.__animationCount == 8:
            self.__animationCount = 0
            
        self.rect.centery += self.__meteorSpeed
        
class Puddle(pygame.sprite.Sprite):
    ''' This class defines the puddle created when a stain collides with the ground '''
    
    def __init__(self, screen, groundX):
        ''' Initalizer takes the screen surface as a parameter and the ground's x parameter
        to set the rect attributes'''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the image for the sprite and rect attributes
        self.image = pygame.image.load('images/puddle.gif')
        self.rect = self.image.get_rect()
        self.rect.centerx = groundX
        self.rect.bottom= screen.get_height()
        
class Lakitu(pygame.sprite.Sprite):
    ''' This class defines the lakitu sprite that throws oil stains towards the player '''
    
    def __init__(self, screen):
        ''' Initalizer takes the screen surface as a parameter to set rect attributes '''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # List of sprite images used by the class
        self.__lakituImages = ['images/lakitu.gif', 'images/lakituThrow1.gif', 'images/lakituThrow2.gif', 'images/lakituThrow3.gif', 'images/lakituThrow4.gif', 'images/lakituThrow5.gif', \
                               'images/lakituThrow6.gif', 'images/lakituThrow7.gif', 'images/lakituThrow8.gif', 'images/lakituThrow9.gif', 'images/lakituThrow10.gif', 'images/lakituThrow11.gif', \
                               'images/lakituThrow12.gif', 'images/lakituThrow13.gif', 'images/lakituThrow14.gif', 'images/lakituThrow15.gif', 'images/lakituThrow16.gif', 'images/lakituThrow17.gif']

        # Set the sprite's image and sets the rect attributes
        self.__animationCount = 0  
        self.image = pygame.image.load(self.__lakituImages[self.__animationCount])
        
        self.rect = self.image.get_rect()
        self.rect.top = 20
        self.rect.left = 240  
        
        # Set instance variables
        self.__screen = screen
        self.__startTime = pygame.time.get_ticks()
        self.__thrown = False
        self.__speed = 5
        
    def throw(self):
        ''' This method updates the sprite image to make it look like lakitu is throwing oil stains '''
        
        if pygame.time.get_ticks() - self.__startTime >= 30:
            self.__animationCount += 1
            self.image = pygame.image.load(self.__lakituImages[self.__animationCount])
            if self.__animationCount == 17:
                self.__animationCount = 0
                self.__thrown = False
                
            self.__startTime = pygame.time.get_ticks()
            
    def getAnimationFrame(self):
        ''' This method returns the animationCount variable '''
        return self.__animationCount
    
    def setThrown(self, boolThrow):
        ''' This method changes the boolThrow variable '''
        self.__thrown = boolThrow
        
    def getCoords(self):
        ''' This method returns the bottom left rect attribute of the lakitu '''
        return self.rect.bottomleft
    
    def update(self):
        ''' This method moves the sprite to the left by the speed variable '''
        self.rect.left += self.__speed
        
        if (self.rect.right >= self.__screen.get_width()) or (self.rect.left <= 0):
            self.__speed = -(self.__speed)
            
        if self.__thrown:
            self.throw()
            
class Stain(pygame.sprite.Sprite):
    ''' This class defines the oil stain sprite that is thrown by the lakitu and creates a puddle
    if collided with the ground or slows the palyer down if collided '''
    
    def __init__(self, stainCoords):
        ''' Initalizer takes the stainCoords parameter to set the rect position of the stain '''
               
        # Call the sprite __init__() method               
        pygame.sprite.Sprite.__init__(self)
        
        # List of sprite images used by the class  
        self.__stainImages = ['images/stainOne.gif', 'images/stainTwo.gif','images/stainOne.gif', 'images/stainTwo.gif','images/stainOne.gif', 'images/stainTwo.gif',]
        
        # Set the sprite's image and sets the rect attributes
        self.__animationCount = 0
        self.image = pygame.image.load(self.__stainImages[self.__animationCount])
        self.rect = self.image.get_rect()
        self.rect.bottomleft = stainCoords

        # Set instance variables 
        self.__stainSpeed = 3
            
    def getCoords(self):
        ''' This method returns the x coordinate rect attribute of the sprite '''
        return self.rect.centerx
    
    def update(self):
        ''' This method will update the y position of the sprite by its instance variable speed and update the sprite image '''
        
        self.__animationCount += 1
        
        self.image = pygame.image.load(self.__stainImages[self.__animationCount])
        if self.__animationCount == 5:
            self.__animationCount = 0
            
        self.rect.top += self.__stainSpeed    

class Bomb(pygame.sprite.Sprite):
    ''' This class defines a bomb that drops down from the top of the screen and spawns an explosion when collided with
    either the player of the ground '''
    
    def __init__(self, screen, bombInt):
        ''' Initalizer takes the screen surface parameters to set location of the scorekeeper and the bombInt to create
        the correct bomb type'''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.__bombInt = bombInt
        self.setBombType()
        self.__screen = screen
        self.__inAir = True
        self.__safeSpace = False
        # This allows me to count the time for switching sprite images
        self.__startTime = pygame.time.get_ticks()
        
        # Choose the bomb colour
        if self.__bombType == 1:
            self.pinkBomb()
        else:
            self.blackBomb()
        
        self.__animationCount = 0
        # Sets the image and the rect attributes
        self.image = pygame.image.load(self.__bombImage[self.__animationCount])
        self.rect = self.image.get_rect()
        self.rect.centery = -100
        self.rect.left = random.randrange(0,640)
        
        self.__previousX = self.rect.centerx
            
        # Set x and y direction of bomb
        self.setSpeed()

    def pinkBomb(self):
        ''' This method sets the images of the bomb to a pink colour '''
        self.__bombImage = ['images/pinkBomb.gif', 'images/pinkBomb1.gif', 'images/pinkBomb2.gif', 'images/pinkBomb3.gif', 'images/pinkBomb4.gif']
        
    def blackBomb(self):
        ''' This method sets the images of the bomb to a black colour '''
        self.__bombImage = ['images/blackBomb.gif', 'images/blackBomb1.gif', 'images/blackBomb2.gif', 'images/blackBomb3.gif', 'images/blackBomb4.gif']
        
    def setBombType(self):
        ''' This method sets the bomb type '''
        if self.__bombInt == 0:
            self.__bombType = 1
        else:
            self.__bombType = 0
            
    def reset(self):
        self.__safeSpace = False
        self.__bombInt = random.randrange(0,5)
        self.setBombType()
        
        if self.__bombType == 1:
            self.pinkBomb()
        else:
            self.blackBomb()
            
        self.__animationCount = 0
        self.image = pygame.image.load(self.__bombImage[self.__animationCount])
        self.__inAir = True
        self.rect.bottom = 0
        self.rect.left = random.randrange(0,640)
        
        self.setSpeed()
        
    def setSpeed(self):
        if self.__bombType == 0:
            self.__dx = 0
            self.__dy = random.randrange(5, 11)
        elif self.__bombType == 1:
            self.__dx = random.randrange(-5,6)
            self.__dy = random.randrange(5, 11)
        
    def getCoords(self):
        ''' This method returns the x coordinate rect attribute of the sprite '''
        return self.rect.centerx    
    
    def safeSpace(self):
        ''' This method moves the bomb to the top of tbe screen'''
        self.rect.centery = -100
        self.__safeSpace = True

    def getSafeSpace(self):
        ''' This method returns the safeSpace variable '''
        return self.__safeSpace
    
    def getAnimationFrame(self):
        ''' This method returns the animationCount variable '''
        return self.__animationCount    

    def getBombType(self):
        ''' This method returns the bombType variable '''
        return self.__bombType
    
    def land(self, groundY):
        self.__dx = 0
        self.__dy = 0
        self.__inAir = False
        
        if pygame.time.get_ticks() - self.__startTime >= 1500:
            self.__animationCount += 1
            self.__previousX = self.rect.centerx
            self.image = pygame.image.load(self.__bombImage[self.__animationCount])            
            self.__startTime = pygame.time.get_ticks()
            
        self.rect = self.image.get_rect()
        self.rect.bottom = groundY + 33
        self.rect.centerx = self.__previousX
        
    def update(self):

        # Move the bomb by the direction speed
        self.rect.centery += self.__dy
        self.rect.centerx += self.__dx
        
        # If bomb reached left border, move the bomb back to the edge
        if (self.rect.left <= 0):
            self.rect.left = 0        
            
        # If bomb reached right border, move the bomb back to the edge
        if (self.rect.right >= self.__screen.get_width()):
            self.rect.right = self.__screen.get_width()          
            
        # If the direction speed is 0 and is still in the air, randomize the speed once more
        if self.__inAir and self.__bombType == 1:
            if self.__dx == 0:
                self.__dx = random.randrange(-10, 11)
            elif self.__dy == 0:
                self.__dy = random.randrange(1, 11)
                
class Explosion(pygame.sprite.Sprite):
    ''' This class defines an explosion that is created when a bomb explodes '''
    
    def __init__(self, screen, groundX, bombType):
        ''' Initalizer takes the screen surface as a parameter and the ground's x parameter
        to set the rect attributes'''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the image for the sprite and rect attributes
        if bombType == 0:
            self.__explosionImage = ['images/circleExplosion.gif', 'images/circleExplosion1.gif', 'images/circleExplosion2.gif', 'images/circleExplosion3.gif', 'images/circleExplosion4.gif', 'images/circleExplosion5.gif', 'images/circleExplosion6.gif',\
                                     'images/circleExplosion7.gif', 'images/circleExplosion8.gif', 'images/circleExplosion9.gif', 'images/circleExplosion10.gif', 'images/circleExplosion11.gif', 'images/circleExplosion12.gif',\
                                     'images/circleExplosion13.gif', 'images/circleExplosion14.gif']
        else:
            self.__explosionImage = ['images/lineExplosion.gif', 'images/lineExplosion1.gif', 'images/lineExplosion2.gif', 'images/lineExplosion3.gif', 'images/lineExplosion4.gif']
            
        self.__bombType = bombType
        self.__animationCount = 0
        self.__startTime = pygame.time.get_ticks()
        
        self.image = pygame.image.load(self.__explosionImage[self.__animationCount])
        self.rect = self.image.get_rect()
        if bombType == 0:
            self.rect.centerx = groundX
        else:
            self.rect.centerx = 320
        self.rect.bottom= screen.get_height() - 30
        
    def update(self):

        if self.__animationCount == 14 and self.__bombType == 0:
            self.kill()
        
        elif self.__animationCount == 4 and self.__bombType == 1:
            self.kill()
            
        if pygame.time.get_ticks() - self.__startTime >= 50:
            self.__animationCount += 1
            self.image = pygame.image.load(self.__explosionImage[self.__animationCount])
            self.__startTime = pygame.time.get_ticks()
    
class ScoreKeeper(pygame.sprite.Sprite):
    ''' This class defines the scoreboard in where you keep track of the current score '''
    
    def __init__(self, screen):
        ''' Initalizer takes the screen surface parameters to set location of the scorekeeper '''
        
        # Call the sprite __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Sets the font used for the sprite
        self.__font = pygame.font.Font('goodbyeDespair.ttf', 18)
        
        # Set instance variables
        self.__score = 0
        self.__screen = screen
        self.__message = ""
        
    def addScore(self, amount):
        ''' This method increases the score by the parameter '''
        self.__score += amount
        
    def getScore(self):
        ''' This method returns the score instance variable '''
        return self.__score
    
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        
        # The text that contains the score that constantly update
        self.__message = "Score: %.f" % (self.__score)
        
        # Renders the score and sets the position of the scoreboard
        self.image = self.__font.render(self.__message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centery = 45
        self.rect.left = 2
        
        # Make the font smaller once it reaches 10000 score 
        if self.__score > 10000:
            self.__font = pygame.font.Font('goodbyeDespair.ttf', 16)
            
class PowerUp(pygame.sprite.Sprite):
    ''' This class defines the power-up that gives the player a live if collided '''
    
    def __init__(self, screen):
        ''' Initalizer takes the screen surface parameters to set the location for the power-up '''
        
        # Call the sprite __init__() method               
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('images/powerUp.gif')
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(0,640)
        
        # Set instance variables 
        self.__fallSpeed = 2
        self.__landBool = False
        self.__safeSpace = False
        self.__startTime = pygame.time.get_ticks()
        
    def land(self):
        if not(self.__landBool):
            self.__startTime = pygame.time.get_ticks()
        self.__fallSpeed = 0
        self.__landBool = True
    
    def safeSpace(self):
        self.__fallSpeed = 0
        self.rect.centerx = -100
        self.__safeSpace = True
        
    def getSafeSpace(self):
        return self.__safeSpace
    
    def reset(self):
        self.rect.left = random.randrange(0,640)
        self.rect.centery = 0
        self.__landBool = False
        self.__safeSpace = False
        self.__fallSpeed = 2
        
    def update(self):
        self.rect.centery += self.__fallSpeed
        
        if pygame.time.get_ticks() - self.__startTime >= 3000 and self.__landBool:
            self.safeSpace()
        
class Button(pygame.sprite.Sprite):
    ''' This class is a button used in the main menu '''
    
    def __init__(self, screen, buttonType):
        ''' Intializer takes screen parameters to set position and buttonType to determine
        which button image should be used '''
        
        # Call the sprite __init__() method               
        pygame.sprite.Sprite.__init__(self)
        
        self.__buttonImages = ['images/startButton.png', 'images/controlButton.png', 'images/quitButton.png', 'images/startButtonEnlarge.png', 'images/controlButtonEnlarge.png', 'images/quitButtonEnlarge.png']
        self.image = pygame.image.load(self.__buttonImages[buttonType])
        self.rect = self.image.get_rect()
            
        # Create instance variables
        self.__buttonType = buttonType
        self.__enlargeBool = False
        
        self.minimize()
        
    def enlarge(self):
        if self.__buttonType == 0:
            self.image = pygame.image.load(self.__buttonImages[3])
            self.rect.center = (295, 200)
        elif self.__buttonType == 1:
            self.image = pygame.image.load(self.__buttonImages[4])
            self.rect.center = (295, 280)
        elif self.__buttonType == 2:
            self.image = pygame.image.load(self.__buttonImages[5])
            self.rect.center = (295, 360)
            
    def minimize(self):
        if self.__buttonType == 0:
            self.image = pygame.image.load(self.__buttonImages[0])
            self.rect.center = (320, 200)
        elif self.__buttonType == 1:
            self.image = pygame.image.load(self.__buttonImages[1])
            self.rect.center = (320, 280)
        elif self.__buttonType == 2:
            self.image = pygame.image.load(self.__buttonImages[2])
            self.rect.center = (320, 360)
    def setEnlarge(self, enlarge):
        self.__enlargeBool = enlarge
        
    def getRect(self):
        return self.rect
    
    def getButtonType(self):
        return self.__buttonType
        
    def update(self):
        if self.__enlargeBool:
            self.enlarge()
        else:
            self.minimize()
            
class ControlMenu(pygame.sprite.Sprite):
    ''' This class is a picture of the controls '''
    
    def __init__(self):
        
        # Call the sprite __init__() method               
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('images/controls.png')
        self.rect = self.image.get_rect()
        