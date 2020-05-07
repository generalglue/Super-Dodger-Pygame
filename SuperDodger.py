'''
Name: Victor Li
Date: 5/17/2017
Description:
'''

# I - Import and Initialize
import pygame, random, pySprites
pygame.init()
pygame.mixer.init()

def main():
    '''This function defines the main game'''
      
    # DISPLAY
    pygame.display.set_caption("Super High School Level Dodger! v0.1")
    screen = pygame.display.set_mode((640, 480))
    
    # ENTITIES

    # Instantiate music and sound effects
    
    # Background music
    pygame.mixer.music.load('sound/background.mp3')
    pygame.mixer.music.set_volume(0.3)

    # Sound effect when a bomb explodes
    explosionSound = pygame.mixer.Sound("sound/explosion.wav")
    explosionSound.set_volume(0.1)
    
    # Sound effect when the player gets hit by an object
    hitSound = pygame.mixer.Sound("sound/hit.wav")
    hitSound.set_volume(0.5)
    
    # Sound effect when the player gets hit by a stain
    stainHitSound = pygame.mixer.Sound("sound/stainHit.wav")
    stainHitSound.set_volume(0.8)
    
    # Sound effect when the player gets a life-up
    lifeUpSound = pygame.mixer.Sound("sound/lifeUp.wav")
    lifeUpSound.set_volume(0.5)
    
    # Sound effect when the game starts
    startUpSound = pygame.mixer.Sound("sound/startUp.wav")
    startUpSound.set_volume(0.5)
    
    # Sound effect when the game ends
    gameOverSound = pygame.mixer.Sound("sound/gameOver.wav")
    gameOverSound.set_volume(0.5)
    
    # Instantiate the font used for the game
    font = pygame.font.Font("goodbyeDespair.ttf", 30)
    
    # Instantiates the background
    background = pygame.image.load('images/background.png')
    background = background.convert()
    screen.blit(background, (0, 0))
       
    # Instantiate the ground
    ground = pySprites.Ground(screen)
    
    # Instantiate the player
    player = pySprites.Player(screen, ground.returnTopGround())    
    
    # Instantiate the lakitu
    lakitu = pySprites.Lakitu(screen)
    
    # Instantiate a power up
    powerUp = pySprites.PowerUp(screen)
    powerUp.safeSpace()
    # Instantiate the live counter
    liveCounter = pySprites.LiveCounter()
    
    # Instantiate the score keeper
    scoreKeeper = pySprites.ScoreKeeper(screen)    
    
    # Creates list to temporarily store meteors for a row
    tempMeteorRow = []
    
    # Two rows of meteors
    for meteorRow in range(2):
        # Eight meteors per row
        for meteorCol in range(8):
            tempMeteorRow.append(pySprites.Meteor(meteorRow, meteorCol))
            
        # Seperates meteors into groups based on row number
        if meteorRow == 0:
            firstMeteorGroup = pygame.sprite.Group(tempMeteorRow)
        elif meteorRow == 1:
            secondMeteorGroup = pygame.sprite.Group(tempMeteorRow)
        
        # Empty the tempMeteorRow list
        del tempMeteorRow[:]
            
    # Instantiate a sprite group to hold all the meteors
    meteorGroup = pygame.sprite.Group(firstMeteorGroup)
            
    # Instantiate a sprite group to hold all the stains
    stainGroup = pygame.sprite.Group()

    # Instantiate a sprite group to hold all the puddles
    puddleGroup = pygame.sprite.Group()
    
    # Instantiate a sprite group to hold all the bombs
    bombGroup = pygame.sprite.Group()
    
    # Instantiate a sprite group to hold all the explosions
    explosionGroup = pygame.sprite.Group()
    
    # Instantiate a sprite group to hold the power up
    powerUpGroup = pygame.sprite.Group(powerUp)
    
    # Instantiate a sprite group holding all the sprites
    allSprites = pygame.sprite.OrderedUpdates(player, ground, lakitu, stainGroup, puddleGroup, bombGroup, powerUpGroup, explosionGroup, meteorGroup, liveCounter, scoreKeeper)
    
    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
    
    # This variable keeps track if the player is moving to the left
    player_left = False
    
    # This variable keeps track if the player is moving to the right
    player_right = False
    
    # This variable keeps track if a meteor still needs to be created
    minimumMeteor = random.randrange(0,2)
    
    # This variable keeps track if there still needs to be an empty space between meteors
    minimumHole = True
    
    # This variable keeps track if a stain is currently slowing down the player
    stainSlowed = False

    # This variable will be used later for keeping track of the time since last collision
    collisonTime = 0
    
    # This variable will be used later for keeping track how long since the lakitu has thrown an oil stain
    thrownTime = 0
    
    # This variable will keep track how long it would take for the lakitu to throw an oil stain randomly
    throwDelay = random.randrange(1000,6000,1000)
    
    # This variable will keep track how long the stain effect should be 
    stainCollisionTime = 0
       
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
    
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(30)
        # EVENT HANDLING: Player uses arrow keys, left control button and left shift button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                gameOver = font.render("Game Over!", 1, (255, 255, 255))
                screen.blit(gameOver, (242,230))                 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_left = True
                if event.key == pygame.K_RIGHT:
                    player_right = True
                if event.key == pygame.K_LCTRL:
                    player.useMop()
                if event.key == pygame.K_LSHIFT:
                    player.useAxe()
                if event.key == pygame.K_SPACE and player.getStand():
                    player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_left = False
                    player_right = False
                    
        # Go left if variable is set to True
        if player_left:
            player.go_left()
        
        # Go right if variable is set to True    
        if player_right:
            player.go_right()
        
        # Jump if variable is set to True    
        if player.getJump():
            player.jumpFall(5)
        
        # Make the lakitu start the throw animation if time has passed the throwDelay variable
        if pygame.time.get_ticks() - thrownTime > throwDelay:
            lakitu.setThrown(True)
            throwDelay = random.randrange(1000,6000,1000)
            
            # Reset the thrownTime clock
            thrownTime = pygame.time.get_ticks()
            
        # Make the lakitu throw a stain at its 16th sprite image
        if lakitu.getAnimationFrame() == 16:
            stains = pySprites.Stain(lakitu.getCoords())
            stainGroup.add(stains)
            allSprites = pygame.sprite.OrderedUpdates(player, ground, lakitu, stainGroup, puddleGroup, bombGroup, powerUpGroup, explosionGroup, meteorGroup, liveCounter, scoreKeeper)
            screen.blit(background,(0,0))
            
        # Check if any stains have collided with the ground
        stainGround = pygame.sprite.spritecollide(ground, stainGroup, False)
        
        # Create a puddle for each stain that hits the ground and kill the stain
        for eachStain in stainGround:
            puddle = pySprites.Puddle(screen, eachStain.getCoords())
            eachStain.kill()
            puddleGroup.add(puddle)
            allSprites = pygame.sprite.OrderedUpdates(player, ground, lakitu, stainGroup, puddleGroup, bombGroup, powerUpGroup, explosionGroup, meteorGroup, liveCounter, scoreKeeper)
            screen.blit(background,(0,0))
            
        # Check if any stains have collided with the player
        stainHit = pygame.sprite.spritecollide(player, stainGroup, False)
        
        # Slow down the player temporarily if the player hits the stain
        for eachStain in stainHit:
            player.slow(0.35)
            stainHitSound.play()
            eachStain.kill()
            stainSlowed = True
            
            # Reset the stainCollisionTime clock
            stainCollisionTime = pygame.time.get_ticks()

        # Check if a power up has collided with the ground
        powerUpGround = pygame.sprite.spritecollide(ground, powerUpGroup, False)
        
        # Make each power up land
        for eachPowerUp in powerUpGround:
            eachPowerUp.land()
        
        # If the player collides with a power up, gain a life and reset the power up    
        powerUpPlayer = pygame.sprite.spritecollide(player, powerUpGroup, False)
        for powerUp in powerUpPlayer:
            powerUp.safeSpace()
            lifeUpSound.play()
            scoreKeeper.addScore(100)
            liveCounter.gainLife()
            
        # Check if any meteors from the first row collided with the ground
        if pygame.sprite.spritecollide(ground, firstMeteorGroup, False):
            for row in firstMeteorGroup:
                # At least have one meteor present
                if minimumMeteor:
                    row.setRespawn(True)
                    minimumMeteor = False
                else:
                    # At least have one empty space present
                    if minimumHole:
                        row.setRespawn(False)
                        minimumHole = False
                # Reset the positions of the meteor row
                row.reset()
            # Set all variables back to true
            minimumMeteor = True
            minimumHole = True
        
        # Check if the second meteors from the second row collided with the ground 
        hittedGround = pygame.sprite.spritecollide(ground, secondMeteorGroup, False)
        
        for meteor in hittedGround:
            # Reset the positions of the meteor row
            meteor.reset()
                
        # Check if player has collided with the a puddle
        mopHit = pygame.sprite.spritecollide(player, puddleGroup, False)
        
        if mopHit:
            # Slow the player half speed if not currently slowed down
            if not(stainSlowed):
                player.slow(0.5)
            for eachMopHit in mopHit:
                # If the player is currently using the mop, kill the puddle and break out of the loop
                if player.getMop():
                    scoreKeeper.addScore(25)
                    eachMopHit.kill()
                    break

        # Check if a bomb has collided with the ground
        bombGround = pygame.sprite.spritecollide(ground, bombGroup, False)
        
        # For each bomb that collided with the ground
        for bombs in bombGround:
            # Start the ticking bomb                     
            bombs.land(ground.returnTopGround())
            # If the bomb is about to explode, create an explosion and reset bomb
            if bombs.getAnimationFrame() == 4:
                explosion = pySprites.Explosion(screen, bombs.getCoords(), bombs.getBombType())
                bombs.safeSpace()
                explosionGroup.add(explosion)
                explosionSound.play()
                allSprites = pygame.sprite.OrderedUpdates(player, ground, lakitu, stainGroup, puddleGroup, bombGroup, powerUpGroup, explosionGroup, meteorGroup, liveCounter, scoreKeeper)
                screen.blit(background,(0,0))                
     
        # Check if player has collided with the a bomb
        bombHit = pygame.sprite.spritecollide(player, bombGroup, False)
        
        if bombHit:
            for eachBombHit in bombHit:
                # If the player is currently using the axe, kill the bomb and break out of the loop
                if player.getAxe():
                    eachBombHit.safeSpace()
                    scoreKeeper.addScore(50)
                    break
                
        for aBomb in bombGroup:
            if (random.randrange(200)) == 1 and aBomb.getSafeSpace() == True:
                aBomb.reset()
                
        for aPowerUp in powerUpGroup:
            if (random.randrange(1000)) == 1 and aPowerUp.getSafeSpace() == True:
                aPowerUp.reset()
        # Check if player collided with any explosions
        if pygame.sprite.spritecollide(player, explosionGroup, False) and not(player.getInvincible()):
            # Set player to be invincible and lose a life
            player.setInvincible(True)
            hitSound.play()
            liveCounter.loseLife(2)
            
            # Reset the collisionTime clock
            collisonTime = pygame.time.get_ticks()
            
        # Check if player collided with any meteor
        if pygame.sprite.spritecollide(player, meteorGroup, False) and not(player.getInvincible()):
            # Set player to be invincible and lose a life
            player.setInvincible(True)
            hitSound.play()
            liveCounter.loseLife(1)
            
            # Reset the collisionTime clock
            collisonTime = pygame.time.get_ticks()
        
        # Takes three seconds before you are no longer invisible
        if pygame.time.get_ticks() - collisonTime > 3000:
            player.setInvincible(False)
            
        # Takes three seconds before a stain effect wears off
        if pygame.time.get_ticks() - stainCollisionTime > 3000 and not(mopHit):
            player.slow(1)
            stainSlowed = False
        
        # Create a bomb every time the score is divisible by 2000, 5 bombs maximum
        if scoreKeeper.getScore() % 1500 == 0 and scoreKeeper.getScore() < 10000:
                bomb = pySprites.Bomb(screen, random.randrange(0,5))
                bombGroup.add(bomb)
                allSprites = pygame.sprite.OrderedUpdates(player, ground, lakitu, stainGroup, puddleGroup, bombGroup, powerUpGroup, explosionGroup, meteorGroup, liveCounter, scoreKeeper)
                screen.blit(background,(0,0)) 
        
        # Second meteor group is spawned when the score reaches 7500        
        if scoreKeeper.getScore() == 5000:
            meteorGroup.add(secondMeteorGroup)
            allSprites = pygame.sprite.OrderedUpdates(player, ground, lakitu, stainGroup, puddleGroup, bombGroup, powerUpGroup, explosionGroup, meteorGroup, liveCounter, scoreKeeper)
            screen.blit(background,(0,0))
        
        # Show the start-up screen once
        if scoreKeeper.getScore() == 0:
            gameStart = font.render("Ready?", 1, (255, 255, 255))
            screen.blit(gameStart, (265,230))  
        if scoreKeeper.getScore() == 1:            
            startUpSound.play()
            pygame.time.delay(6000)
            pygame.mixer.music.play(-1)
                      
        # Add the score by 1 each time the loop instantiates    
        scoreKeeper.addScore(1)
        
        # Blit the Game-over screen if lives are zero
        if liveCounter.getLife() <= 0:
            keepGoing = False
            gameOver = font.render("Game Over!", 1, (255, 255, 255))
            screen.blit(gameOver, (242,230))    
            
        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
          
    # Unhide the mouse pointer     
    pygame.mouse.set_visible(True)
 
    # Play the GameOver music and go back to the start menu
    pygame.mixer.music.fadeout(0)
    gameOverSound.play()
    pygame.time.delay(7000)
    startMenu()     
     
def startMenu():
    ''' This function is the main menu of the game '''
    
    # DISPLAY
    pygame.display.set_caption("Super High School Level Dodger! v0.1")
    screen = pygame.display.set_mode((640, 480))
    
    # ENTITIES
    startButton = pySprites.Button(screen, 0)
    controlButton = pySprites.Button(screen, 1)
    quitButton = pySprites.Button(screen, 2)
    

    
    # Instantiates the background
    background = pygame.image.load('images/StartMenu.png')
    background = background.convert()
    screen.blit(background, (0, 0))
    
    # Instantiate the control screen
    controlScreen = pySprites.ControlMenu()
    
    buttonGroup = pygame.sprite.Group(startButton, controlButton, quitButton)
    allSprites = pygame.sprite.Group(buttonGroup)
    
    # Instantiate the background music
    pygame.mixer.music.load('sound/menu.mp3')
    pygame.mixer.music.set_volume(0.3)    
    pygame.mixer.music.play(-1)
    
    # Instantiate sound effect when selecting a button
    menuSelect = pygame.mixer.Sound("sound/menuSelect.wav")
    menuSelect.set_volume(0.2)
                          
    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True    
    clicked = False
    controlMenu = False
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(30)
        
        # EVENT HANDLING: Player uses arrow keys, left control button and left shift button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    controlMenu = False
        
        for eachButton in buttonGroup:
            if eachButton.getRect().collidepoint(pygame.mouse.get_pos()):
                eachButton.setEnlarge(True)
            else:
                eachButton.setEnlarge(False)
                
            if pygame.mouse.get_pressed()[0] and eachButton.rect.collidepoint(pygame.mouse.get_pos()) and not(clicked):
                menuSelect.play()
                clicked = True
                
                if eachButton.getButtonType() == 0:
                    keepGoing = False
                    main()
                    
                elif eachButton.getButtonType() == 1:
                    controlMenu = True
                    
                elif eachButton.getButtonType() == 2:
                    keepGoing = False
                
            if controlMenu:
                allSprites = pygame.sprite.Group(controlScreen)
            else:
                screen.blit(background, (0, 0))
                allSprites = pygame.sprite.Group(buttonGroup)
                
        # REFRESH SCREEN
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
        
    # Close the game window
    pygame.quit()    
    
# Call the startMenu function
startMenu()