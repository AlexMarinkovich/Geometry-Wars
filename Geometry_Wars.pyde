import random
add_library('minim')

def setup():
    global key_a, key_d, key_w, key_s, mouse_clicked, key_pressed
    global gameScreen, font, hitboxes, player_name, max_name_length, leaderboards_y_scroll, num_rankings
    global menu_background_image, how_to_play_image, upgrade_image
    global ship_image, basic_invader_image, follower_invader_image, mini_invader_image, boss_invader_image, arrow_invader_image, zigzag_invader_image, accelerator_invader_image
    global splitter_invader_image, icicle_invader_image, dasher_invader_image, dashing_invader_image
    global shoot_sound, ricochet_sound, invader_spawn_sound, play_music, cantina_music
    
    minim = Minim(this)
    upgrade_screen_sound = minim.loadFile("star_wars_cantina.mp3")
    shoot_sound = minim.loadSample("shoot_sound.mp3") # load sample if you want to play the sound more than once at a single time
    shoot_sound.setGain(-5) 
    ricochet_sound = minim.loadSample("ricochet_sound.mp3")
    invader_spawn_sound = minim.loadFile("invader_spawn_sound.mp3")
    invader_spawn_sound.setGain(-5) 
    play_music = minim.loadFile("geometry_wars_evolved.mp3")
    play_music.setGain(-15) 
    cantina_music = minim.loadFile("star_wars_cantina.mp3")
    cantina_music.setGain(-15)
    
    size(1200,750)
    frameRate(60)
    
    hitboxes = False
    
    key_a = False
    key_d = False
    key_w = False
    key_s = False
    mouse_clicked = False
    key_pressed = False
    
    gameScreen = 0
    
    player_name = ""
    max_name_length = 32
    leaderboards_y_scroll = 0
    num_rankings = 0
    get_highscores()
    
    menu_background_image = loadImage("menu_background.png")
    how_to_play_image = loadImage("gameinterface.png")
    upgrade_image = loadImage("tools.png")
    
    ship_image = loadImage("ship.png")
    basic_invader_image = loadImage("basic_invader.png")
    mini_invader_image = loadImage("mini_invader.png")
    follower_invader_image = loadImage("follower_invader.png")
    boss_invader_image = loadImage("boss_invader.png")
    arrow_invader_image = loadImage("arrow_invader.png")
    zigzag_invader_image = loadImage("zigzag_invader.png")
    accelerator_invader_image = loadImage("accelerator_invader.png")
    splitter_invader_image = loadImage("splitter_invader.png")
    icicle_invader_image = loadImage("icicle_invader.png")
    dasher_invader_image = loadImage("dasher_invader.png")
    dashing_invader_image = loadImage("dashing_invader.png")
    
    font = loadFont("font.vlw")
    textFont(font)
    
def start():
    global ship_x, ship_y, ship_width, ship_height, ship_speed, ship_hp
    global invaders, invader_load_time, frame_counter, game_time, upgrades_available
    global bullets, bullet_speed, bullet_diameter, shoot_time, shoot_delay, spread_shot, spread_angle, burst_shot, burst_time, burst_counter, bullet_hp, ricochet_count
    global border_left, border_right, border_top, border_bottom, current_score
    
    border_left = 30
    border_right = width-border_left
    border_top = 30
    border_bottom = height-border_top  
    
    ship_width = 50
    ship_height = 50
    ship_x = width/2 - ship_width/2
    ship_y = height/2 - ship_height/2
    ship_speed = 6
    ship_hp = 3
    
    bullets = [] # [bullet_x, bullet_y, movement_angle, bullet_speed, bullet_diameter, ricochet_count, bullet_hp]
    bullet_speed = 12
    bullet_diameter = 15

    shoot_time = 15 # how many frames before you can shoot again
    shoot_delay = 0 # counts frames for shoot_time
    
    spread_shot = 1 # number of bullets per shot
    spread_angle = 5 # angle between each bullet in a spreadshot
    
    burst_shot = 1 # number of shots in each burst
    burst_time = 3 # number of frames between each shot in a burst
    burst_counter = 0 # counts numbers of shots for a burst shot
    
    ricochet_count = 0 # number of times a bullet can ricochet off the border
    bullet_hp = 1 # number of times a bullet can hit an invader before getting destroyed
    
    invaders = [] # [x, y, movement_angle, y_velocity, width, height, image, hp, score, invader_type] 
    invader_load_time = 50 # number of frames after an invader spawns when it can't be shot and can't damage the player
    
    frame_counter = 0 # counts frames for game_time
    game_time = 0 # amount of seconds passed after pressing play
    
    upgrades_available = game_time // 60
    
    play_music.rewind()
    play_music.loop() # for some reason you have to loop at first for minim to realize it is rewinded, then you have to loop again to play at the desired time in the mp3
    play_music.setLoopPoints(game_time*1000, 185600)
    play_music.loop()
    play_music.setLoopPoints(55350,185600) # after looping, dont play the first part in the song to make it seamlessly feel like an endless song
    
    current_score = 0
        
def draw():
    global gameScreen, mouse_clicked, key_pressed
    
    background(0)
    if gameScreen == 0:
        menuScreen()
    elif gameScreen == 1:
        playScreen()
    elif gameScreen == 2:
        howtoScreen()
    elif gameScreen == 3:
        pauseScreen()
    elif gameScreen == 4:
        gameOverScreen()
    elif gameScreen == 5:
        upgradeScreen()
    elif gameScreen == 6:
        saveScoreScreen()
    elif gameScreen == 7:
        leaderboardsScreen()
    
    if mouse_clicked == True: # mouse_clicked only returns true if the mouse was clicked on that frame
        mouse_clicked = False
    if key_pressed == True: # key_pressed only returns true if a key was pressed on that frame
        key_pressed = False
    
def menuScreen():
    global gameScreen
    
    image(menu_background_image,0,0,width,height)
    textAlign(CENTER)
    fill(255, 165, 0)
    textSize(150)
    text("Geometry Wars", 600, 125)
    fill(255)
            
    if (mouseX >= 490 and mouseX <= 720) and (mouseY >= 175 and mouseY <= 250):
        textSize(100)
        if mouse_clicked == True:
            play_music.loop()
            start()
            gameScreen = 1
    else:
        textSize(75)
    text("PLAY", 600, 250)

    if (mouseX >= 490 and mouseX <= 720) and (mouseY >= 325 and mouseY <= 400):
        textSize(100)
        if mouse_clicked == True:
            gameScreen = 2
    else:
        textSize(75)
    text("HELP", 600, 400)
        
    if (mouseX >= 250 and mouseX <= 950) and (mouseY >= 475 and mouseY <= 550):
        textSize(100)
        if mouse_clicked == True:
            gameScreen = 7
    else:
        textSize(75)
    text("LEADERBOARDS", 600, 550)
    
    if (mouseX >= 500 and mouseX <= 700) and (mouseY >= 625 and mouseY <= 700):
        textSize(100)
        if mouse_clicked == True:
            exit()
    else:
        textSize(75)
    text("EXIT", 600, 700)

def howtoScreen():
    global gameScreen, how_to_play_image
    
    image(how_to_play_image, 0, 0, width, height)
    
    fill(255)
    textAlign(LEFT)
    
    if (mouseX >= 25 and mouseX <= 85) and (mouseY >= 20 and mouseY <= 70):
        textSize(50)
        if mouse_clicked == True:
            gameScreen = 0
    else:
        textSize(25)
    text("BACK", 25, 70)
    
def playScreen():
    global gameScreen, gameplay_background
    
    invader_waves()
    move_ship()
    move_bullets()
    move_invaders()
    do_borders()    
    do_ship()
    do_bullets()
    do_invaders()
    do_collisions()
        
    if (mouseX >= 45 and mouseX <= 75) and (mouseY >= 55 and mouseY <= 95):
        pause_button_width = 15
        pause_button_height = 60
        if mouse_clicked == True:
            gameplay_background = get()
            gameScreen = 3
    else:
        pause_button_width = 10
        pause_button_height = 40
    
    # pause button design
    stroke(255)
    fill(255)
    rect(45, 55, pause_button_width, pause_button_height)
    rect(65, 55, pause_button_width, pause_button_height)
    
    # show game time
    textAlign(CENTER,CENTER)
    textSize(40)
    text(game_time // 600, 560, 70) # game time in minutes tens column
    text(game_time // 60 % 10, 580, 70) # game time in minutes ones column
    text(":", 600, 69)
    text(game_time // 10 % 6, 620, 70) # game time in seconds tens column
    text(game_time % 10, 640, 70) # game time in seconds ones column
    
    # show score
    textAlign(RIGHT)
    textSize(25)
    text("Score", 1100, 70)
    text(current_score, 1100, 100)
    
    #go to upgradeScreen
    textAlign(LEFT)
    fill(255)
    textSize(25)
    text("Press E to Upgrade", border_left + 5, border_bottom - 5)
    if keyPressed and (key == 'e' or key == 'E'):
        gameplay_background = get()
        cantina_music.loop()
        gameScreen = 5
    
    # show if upgrade is available
    if upgrades_available > 0:
        fill(255,255,0)
        textAlign(CENTER)
        text("Upgrade Available!", ship_mid_x, ship_mid_y+60)
        
def pauseScreen():   
    global gameScreen
    
    # pause play music
    play_music.pause()
    
    # gameplay background
    tint(255, 128)
    image(gameplay_background, 0, 0, width, height)
    noTint()
    
    fill(0,128)
    stroke(255)
    rectMode(CENTER)
    rect(600, 350, 300, 500)
    
    fill(255)
    textAlign(CENTER)
    if (mouseX >=  570 and mouseX <= 630) and (mouseY >= 185 and mouseY <= 200):
        textSize(50)
        if mouse_clicked == True:
            play_music.loop()
            gameScreen = 1
    else:
        textSize(25)
    text("BACK", 600, 200)
        
    if (mouseX >=  570 and mouseX <= 630) and (mouseY >= 285 and mouseY <= 300):
        textSize(50)
        if mouse_clicked == True:
            start()
            gameScreen = 1
    else:
        textSize(25)
    text("RETRY", 600, 300)
        
    if (mouseX >=  570 and mouseX <= 630) and (mouseY >= 385 and mouseY <= 400):
        textSize(50)
        if mouse_clicked == True:
            gameScreen = 0
    else:
        textSize(25)
    text("MENU", 600, 400)
        
    textSize(23)
    text("Credits to:", 600, 500)
    text("Emiliano & Alexander", 600, 530)

def upgradeScreen():
    global upgrades_available, gameScreen, upgrade_image, ship_hp, bullet_hp, shoot_time, spread_shot, burst_shot, ricochet_count
    
    play_music.pause()
    
    image(gameplay_background, 0, 0, width, height)
    
    tint(255,220)
    image(upgrade_image, 0, 0, width, height)
    noTint()
    
    textSize(40)
    textAlign(LEFT)
    fill(255)
    if keyPressed and (key == '1' or key == '2' or key == '3' or key == '4' or key == '5') and upgrades_available == 0:
        fill(255,0,0)
    text("Upgrades Available:", 50, 520)
    text(upgrades_available, 520, 520)
    textSize(25)
    
    fill(255)
    text("Press Q to go back", border_left, border_top)
    if keyPressed and (key == 'q' or key == 'Q'):
        cantina_music.pause()
        cantina_music.rewind()
        play_music.loop()
        gameScreen = 1
    
    if upgrades_available > 0:
        if key_pressed and (key == '1'):
            burst_shot += 2
            shoot_time *= 1.3
            
        elif key_pressed and (key == '2'):
            ricochet_count += 1
            
        elif key_pressed and (key == '3'):
            spread_shot += 2
            shoot_time *= 1.5
            
        elif key_pressed and (key == '4'):
            bullet_hp += 1
        
        elif key_pressed and (key == '5'):
            shoot_time /= 1.4
        
        else:
            return
        upgrades_available -= 1
        ship_hp = 3
        
def gameOverScreen():
    global gameScreen
    
    play_music.pause()
    
    # gameplay background
    tint(255, 80)
    image(gameplay_background, 0, 0, width, height)
    noTint()
    fill(0)
    stroke(0,100,150,128)
    strokeWeight(2)
    rect(ship_mid_x-30, ship_y-40, 60, 15)
    
    textAlign(CENTER)
    textSize(100)
    fill(255,0,0)
    text("GAME OVER", 600, 150)
    
    fill(0,255,255)
    textSize(50)
    text("SCORE: " + str(current_score), 600, 225)
    fill(255,255,0)
    text("Time Survived: " + str(game_time//600) + str(game_time//60%10) + ":" + str(game_time//10%6) + str(game_time%10) , 600, 300)
    
    fill(255)
    if (mouseX >= 490 and mouseX <= 700) and (mouseY >= 365 and mouseY <= 410):
        textSize(150)
        if mouse_clicked == True:
            start()
            gameScreen = 1
    else:
        textSize(75)
    text("RETRY", 600, 410)
    
    # save score button
    if (mouseX >= 400 and mouseX <= 800) and (mouseY >= 480 and mouseY <= 525):
        if mouse_clicked:
            gameScreen = 6
        textSize(150)
    else:
        textSize(70)
    text("SAVE SCORE", 600, 525)
    
    if (mouseX >= 500 and mouseX <= 690) and (mouseY >= 595 and mouseY <= 640):
        textSize(150)
        if mouse_clicked == True:
            gameScreen = 0
    else:
        textSize(75)
    text("MENU", 600, 640)

def saveScoreScreen():
    global player_name, gameScreen
    
    fill(255,255,0)
    textAlign(CENTER)
    textSize(80)
    text("Save To Leaderboards", 600, 100)
    
    fill(255)
    textSize(40)
    text("Score: " + str(current_score), 600, 400)
    text("Time Survived: " + str(game_time//600) + str(game_time//60%10) + ":" + str(game_time//10%6) + str(game_time%10) , 600, 475)
    
    if key_pressed:
        if key != CODED and key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz" and len(player_name) < max_name_length:
            player_name += key.upper()
        elif key == BACKSPACE:
            player_name = player_name[0:len(player_name)-1]
    
    text("Enter Name:", 600, 250)
    fill(255,255,0)
    text(player_name, 600, 325)
    
    if (mouseX >= 500 and mouseX <= 690) and (mouseY >= 555 and mouseY <= 600):
        if len(player_name) > 0 and mouse_clicked == True:
            save_highscore()
            get_highscores()
            player_name = ""
            gameScreen = 7
            
        elif mousePressed and len(player_name) == 0:
            fill(255,0,0)
        textSize(150)
    else:
        textSize(70)
    text("Save", 600, 600)

def save_highscore():
    
    read_highscores = open("highscores.txt","r")
    current_highscores = open("highscores.txt","a")
    
    if read_highscores.read(1):
        current_highscores.write("\n" + player_name + "," + str(game_time) + "," + str(current_score))
    else:
        current_highscores.write(player_name + "," + str(game_time) + "," + str(current_score))
    
    read_highscores.close()
    current_highscores.close()

def get_highscores():
    
    all_highscores = []
    for value in open("highscores.txt","r"):
        all_highscores.append(value.split(","))
    
    for value in all_highscores:
        value[1] = int(value[1])
        value[2] = int(value[2])
     
    bubble_sort(all_highscores,2)
    
def bubble_sort(the_list, item_num):
    global sorted_highscores
    for i in range(len(the_list)-1):
        if the_list[i][item_num] > the_list[i+1][item_num]:
            the_list[i], the_list[i+1] = the_list[i+1], the_list[i]
    
    if all(the_list[i][item_num] <= the_list[i+1][item_num] for i in range(len(the_list)-1)):
        sorted_highscores = the_list
        #return the_list # for some reason this crashes, no idea why after half an hour of testing, doesn't crash on replit
        
    else:
        bubble_sort(the_list, item_num)

def leaderboardsScreen():
    global gameScreen, num_rankings, leaderboards_y_scroll
    
    textSize(30)
    for rank,value in enumerate(sorted_highscores[::-1]):
        textAlign(LEFT)
        text(str(rank+1) + ". " + str(value[0]), 160, 250+rank*50 + leaderboards_y_scroll)
        textAlign(CENTER)
        text(str(int(value[1])//600) + str(int(value[1])//60%10) + ":" + str(int(value[1])//10%6) + str(int(value[1])%10), 750, 250+rank*50 + leaderboards_y_scroll)
        textAlign(RIGHT)
        text(str(value[2]), 1040, 250+rank*50 + leaderboards_y_scroll)
        
        num_rankings = rank+1
    
    rectMode(CORNER)
    stroke(20)
    fill(20)
    rect(0,0,width,205)
    rect(0,0,150,height)
    rect(1050,0,150,height)
    rect(0,625,width,125)
    stroke(255)
    noFill()
    rect(150, 205, 900, 420)
    
    fill(255)
    textAlign(LEFT)
    text("Name", 150, 195)
    textAlign(CENTER)
    text("Time Survived", 750, 195)
    textAlign(RIGHT)
    text("Score", 1050, 195)
    
    fill(255)
    textAlign(CENTER)
    textSize(100)
    text("Leaderboards", 600, 120)
    textAlign(LEFT)
    textSize(25)
    text("Use Scroll Wheel", 60, 710)
    stroke(255)
    triangle(160,640, 190,640, 175,675)
    
    if (mouseX >= 500 and mouseX <= 690) and (mouseY >= 665 and mouseY <= 710):
        textSize(150)
        if mouse_clicked == True:
            leaderboards_y_scroll = 0
            gameScreen = 0
    else:
        textSize(75)
    textAlign(CENTER)
    text("MENU", 600, 710)

def invader_waves():
    global frame_counter, game_time, upgrades_available
        
    #spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
    #spawn_invader("mini_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
    #spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
    #for i in range(23):    
            #spawn_invader("arrow_invader", border_left+i*50, border_top+1, PI)
    #spawn_invader("zigzag_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
    #spawn_invader("accelerator_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
    #spawn_invader("splitter_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
    #spawn_invader("dasher_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
    
    if frame_counter == 0:
        if game_time == 1:
            for i in range(3):
                spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                spawn_invader("mini_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                
        elif game_time == 6:
            for i in range(5):
                spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
        
        elif game_time == 10:
            for i in range(3):
                spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                spawn_invader("mini_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
        
        elif game_time == 15:
            for i in range(3):
                spawn_invader("mini_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                spawn_invader("arrow_invader", find_spawnable_position(0), find_spawnable_position(1), random.choice([0,HALF_PI,PI,PI*1.5]))
                
        elif game_time == 19 or game_time == 21 or game_time == 23:
            spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
            for i in range(3):
                spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0) 
        
        elif game_time == 27:
            if random.randint(1,2) == 1:
                for i in range(12):    
                    spawn_invader("arrow_invader", border_left+5, border_top+i*55+10, HALF_PI)
            else:
                for i in range(12):    
                    spawn_invader("arrow_invader", border_right-45, border_top+i*55+10, PI*1.5)
                    
        elif game_time == 33:
            for i in range(4):    
                spawn_invader("zigzag_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
        
        elif game_time == 39 or game_time == 40 or game_time == 41:
            spawn_invader("basic_invader", border_left+1, border_top+1, random.uniform(HALF_PI, PI))
            spawn_invader("basic_invader", border_right-21, border_top+1, random.uniform(PI, PI*1.5))
            spawn_invader("basic_invader", border_right-21, border_bottom-21, random.uniform(PI*1.5, TWO_PI))
            spawn_invader("basic_invader", border_left+1, border_bottom-21, random.uniform(0, HALF_PI))
            
        elif game_time == 46:
            for i in range(4):
                spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                spawn_invader("arrow_invader", find_spawnable_position(0), find_spawnable_position(1), random.choice([0,HALF_PI,PI,PI*1.5]))
        
        elif game_time >= 50 and game_time <= 58 and game_time % 2 == 0:
            spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
            spawn_invader("arrow_invader", find_spawnable_position(0), find_spawnable_position(1), random.choice([0,HALF_PI,PI,PI*1.5]))
            spawn_invader("zigzag_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
        
        # 1 minute ############################################################################################################################################## 
        
        elif game_time >= 64 and game_time < 80 and game_time % 4 == 0:
            for i in range(4):
                spawn_invader("accelerator_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                
                if random.randint(1,2) == 1:
                    for i in range(2):
                        spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                else:
                    spawn_invader("zigzag_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
            
        elif game_time >= 80 and game_time < 100 and game_time % 4 == 0:
            spawn_invader("splitter_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
            
            for i in range(4):
                if random.randint(1,2) == 1:
                        spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                else:
                    spawn_invader("arrow_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
        
        elif game_time >= 100 and game_time <= 105:
            spawn_invader("follower_invader", border_left+1, border_top+1, random.uniform(HALF_PI, PI))
            spawn_invader("follower_invader", border_right-51, border_top+1, random.uniform(PI, PI*1.5))
            spawn_invader("follower_invader", border_right-51, border_bottom-51, random.uniform(PI*1.5, TWO_PI))
            spawn_invader("follower_invader", border_left+1, border_bottom-51, random.uniform(0, HALF_PI))
        
        elif game_time >= 110 and game_time <= 118:
            spawn_invader("follower_invader", border_left+1, border_top+1, random.uniform(HALF_PI, PI))
            spawn_invader("follower_invader", border_right-51, border_top+1, random.uniform(PI, PI*1.5))
            spawn_invader("follower_invader", border_right-51, border_bottom-51, random.uniform(PI*1.5, TWO_PI))
            spawn_invader("follower_invader", border_left+1, border_bottom-51, random.uniform(0, HALF_PI))
        
        # 2 minutes ##############################################################################################################################################   
        
        elif game_time >= 124 and game_time < 140 and game_time % 4 == 0:
            for i in range(3):
                spawn_invader("dasher_invader", find_spawnable_position(0), find_spawnable_position(1), 0)   
                spawn_invader("follower_invader",find_spawnable_position(0), find_spawnable_position(1), 0)  
                spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))   
       
        elif game_time >= 140 and game_time <= 142 or game_time >= 150 and game_time <= 153:
            if random.randint(1,2) == 1:
                if random.randint(1,2) == 1:
                    for i in range(20):    
                        spawn_invader("arrow_invader", border_left+i*57+6, border_top+1, PI)
                else:
                    for i in range(20):    
                        spawn_invader("arrow_invader", border_left+i*57+6, border_bottom-51, TWO_PI)
            else:
                if random.randint(1,2) == 1:  
                    for i in range(15):    
                        spawn_invader("arrow_invader", border_left+5, border_top+i*45+5, HALF_PI)
                else:
                    for i in range(15):    
                        spawn_invader("arrow_invader", border_right-50, border_top+i*45+5, PI*1.5)
        
        # 3 minutes ##############################################################################################################################################     
        
        elif game_time >= 159 and game_time < 180 and game_time % 3 == 0:
            for i in range(3):
                spawn_invader(random.choice(["zigzag_invader","accelerator_invader"]), find_spawnable_position(0), find_spawnable_position(1), 0)
            spawn_invader("splitter_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
            
        elif game_time >= 183 and game_time < 200 and (game_time+2) % 5 == 0:
            for i in range(6):
                spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                spawn_invader("mini_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                spawn_invader("arrow_invader", find_spawnable_position(0), find_spawnable_position(1), random.choice([0,HALF_PI,PI,PI*1.5]))
                spawn_invader("zigzag_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                spawn_invader("accelerator_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
        
        elif game_time >= 202 and game_time < 220 and game_time % 3 == 0:
            for i in range(3):
                spawn_invader("splitter_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                spawn_invader("dasher_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                if random.randint(1,2) == 1:
                    spawn_invader("mini_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                else:
                    spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                    
        elif game_time >= 222 and game_time < 236:
            spawn_invader("zigzag_invader", border_left+1, border_top+1, random.uniform(HALF_PI, PI))
            spawn_invader("zigzag_invader", border_right-41, border_top+1, random.uniform(PI, PI*1.5))
            spawn_invader("zigzag_invader", border_right-41, border_bottom-41, random.uniform(PI*1.5, TWO_PI))
            spawn_invader("zigzag_invader", border_left+1, border_bottom-41, random.uniform(0, HALF_PI))
            spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                          
        # 4 minutes ##############################################################################################################################################       
         
        elif game_time >= 243 and game_time < 260:
            spawn_invader("arrow_invader",ship_mid_x, ship_mid_y+100, 0)
            spawn_invader("arrow_invader",ship_mid_x+100, ship_mid_y, PI*1.5)
            spawn_invader("arrow_invader",ship_mid_x, ship_mid_y-100, PI)
            spawn_invader("arrow_invader",ship_mid_x-100, ship_mid_y, HALF_PI)
            if game_time >= 250:
                for i in range(game_time-249):
                    spawn_invader("mini_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                    
        elif game_time >= 264 and game_time < 280 and game_time % 3 == 0:
            for i in range(10):
                if random.randint(1,2) == 1:
                    spawn_invader("dasher_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                else:
                    spawn_invader("accelerator_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                    
            if random.randint(1,2) == 1:
                if random.randint(1,2) == 1:
                    for i in range(20):    
                        spawn_invader("arrow_invader", border_left+i*57+6, border_top+1, PI)
                else:
                    for i in range(20):    
                        spawn_invader("arrow_invader", border_left+i*57+6, border_bottom-51, TWO_PI)
            else:
                if random.randint(1,2) == 1:  
                    for i in range(15):    
                        spawn_invader("arrow_invader", border_left+5, border_top+i*45+5, HALF_PI)
                else:
                    for i in range(15):    
                        spawn_invader("arrow_invader", border_right-50, border_top+i*45+5, PI*1.5)
           
        elif game_time >= 282 and game_time < 300 and game_time % 2 == 0:
            for i in range(4):
                spawn_invader("splitter_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                spawn_invader("basic_invader", find_spawnable_position(0), find_spawnable_position(1), random.uniform(0,TWO_PI))
                spawn_invader("dasher_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                if random.randint(1,2) == 1:
                    spawn_invader("zigzag_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
                else:
                    spawn_invader("follower_invader", find_spawnable_position(0), find_spawnable_position(1), 0)
        
        # 5 minutes ##############################################################################################################################################
        elif game_time >= 306 and game_time % 3 == 0:
            for i in range((game_time - 300) / 3 + 15):
                spawn_invader(random.choice(["basic_invader", "mini_invader", "follower_invader", "arrow_invader", "zigzag_invader", "accelerator_invader", "splitter_invader", "dasher_invader"]), find_spawnable_position(0), find_spawnable_position(1), 0)
            
    # time counter in seconds
    frame_counter += 1
    if frame_counter == 60:
        frame_counter = 0
        game_time += 1
        
        # upgrade system
        if game_time % 60 == 0:
            upgrades_available += 1

def find_spawnable_position(axis):
    global spawning_position_x
    
    if axis == 0:
        spawning_position_x = random.randint(border_left, border_right)
        return spawning_position_x
    if axis == 1:
        if spawning_position_x in range (int(ship_x)-200, int(ship_x)+ship_width+200):
            spawning_position_y = random.choice(list(range(border_top, int(ship_y-200))) + list(range(int(ship_y+ship_height+200), border_bottom)))
        else:
            spawning_position_y = random.randint(border_top, border_bottom)
        return spawning_position_y
    
def spawn_invader(invader_type, x_position, y_position, movement_angle):
    # [x, y, movement_angle, speed, width, height, image, hp, score, invader_type, loading_time]
    
    if invader_type != "icicle_invader":
        invader_spawn_sound.rewind()
        invader_spawn_sound.play()
    
    if invader_type == "basic_invader": 
        invaders.append([x_position, y_position, movement_angle, 2, 30, 30, basic_invader_image, 1, 100, invader_type, invader_load_time])
    
    elif invader_type == "mini_invader":
        invaders.append([x_position, y_position, movement_angle, 3, 20, 20, mini_invader_image, 1, 150, invader_type, invader_load_time])
    
    elif invader_type == "follower_invader":
        invaders.append([x_position, y_position, movement_angle, 3, 50, 50, follower_invader_image, 1, 200, invader_type, invader_load_time])
    
    elif invader_type == "arrow_invader":
        invaders.append([x_position, y_position, movement_angle, 6, 40, 50, arrow_invader_image, 1, 150, invader_type, invader_load_time])
        
    elif invader_type == "zigzag_invader":
        invaders.append([x_position, y_position, movement_angle, 5, 30, 40, zigzag_invader_image, 1, 300, invader_type, invader_load_time, random.choice([-1,1]) ]) # zig zag direction
    
    elif invader_type == "accelerator_invader":
        invaders.append([x_position, y_position, movement_angle, 2, 40, 40, accelerator_invader_image, 1, 300, invader_type, invader_load_time, 0, 0]) # spinning angle, spinning speed
    
    elif invader_type == "splitter_invader":
        invaders.append([x_position, y_position, movement_angle, 2, 60, 60, splitter_invader_image, 1, 250, invader_type, invader_load_time, 0, 0.01]) # spinning angle, spinning speed
    
    elif invader_type == "icicle_invader":
        invaders.append([x_position, y_position, movement_angle, 6, 20, 25, icicle_invader_image, 1, 100, invader_type, 0]) # 0 second load time
    
    elif invader_type == "dasher_invader":
        invaders.append([x_position, y_position, movement_angle, 0, 40, 50, dasher_invader_image, 1, 400, invader_type, invader_load_time, random.randint(-20,20)]) # counts frames for dashing and not dashing
    
def do_invaders():
    
    for invader in invaders: # [x, y, movement_angle, speed, width, height, image, hp, score, invader_type]
        invader_mid_x = invader[0]+invader[4]/2
        invader_mid_y = invader[1]+invader[5]/2
        
        # makes invaders go from translucent to opaque as they go through their loading phase
        if invader[10] != 0 and invader[9] != "accelerator_invader": 
            #tint(255, -invader[10] * 200/invader_load_time + 255)
            pass # tinting every frame caused a lot of lag
            
        elif invader[9] == "accelerator_invader":
            tint(255, invader[3]*30, 0)
        rectMode(CORNER)
        
        # draw invaders with rotation
        pushMatrix()
        translate(invader[0] + invader[4]/2, invader[1] + invader[5]/2)
        if invader[9] != "accelerator_invader" and invader[9] != "splitter_invader":
            rotate(invader[2]+PI) # facing the player rotation
        else:
            rotate(invader[11]) # spinning rotation
            invader[11] += invader[12]
        image(invader[6], 0-invader[4]/2, 0-invader[5]/2, invader[4], invader[5])
        popMatrix()
        noTint()
        
        # red lined hitbox of invaders
        if hitboxes == True:
            stroke(255,0,0)
            strokeWeight(1)
            noFill()
            circle(invader_mid_x, invader_mid_y, invader[4])
            #rect(invader[0], invader[1], invader[4], invader[5])

def move_invaders():            
    
    for invader in invaders: # [x, y, movement_angle, speed, width, height, image, hp, score, invader_type]
        invader_mid_x = invader[0]+invader[4]/2
        invader_mid_y = invader[1]+invader[5]/2
        
        # invader load time
        if invader[10] > 0:
            invader[10] -= 1
        
        else: # invader movement and special functionalities goes below
            
            # makes these invaders face towards and follow the player 
            if invader[9] == "follower_invader" or invader[9] == "zigzag_invader" or invader[9] == "accelerator_invader" or (invader[9] == "dasher_invader" and invader[11] < 90):
                if invader_mid_y - ship_mid_y != 0:
                    invader[2] = atan((ship_mid_x-invader_mid_x) / float(invader_mid_y-ship_mid_y))
                
                if ship_mid_y > invader_mid_y:
                    invader[2] += PI
                elif ship_mid_x < invader_mid_x:
                    invader[2] += TWO_PI
            
            # dasher invader dash functionality
            if invader[9] == "dasher_invader":
                invader[11] += 1
                
                if invader[11] == 90: # start dash
                    invader[3] = 15 
                    invader[6] = dashing_invader_image
                
                elif invader[11] > 140: # slow down dash
                    invader[3] -= 0.3
                
                if invader[11] == 180: # stop dash
                    invader[3] = 0
                    invader[6] = dasher_invader_image
                    invader[11] = 0
                
            # zigzag movement for zigzag invader    
            if invader[9] == "zigzag_invader":
                invader[2] += QUARTER_PI * invader[11]
                if random.randint(1,30) == 1:
                    invader[11] *= -1 # 1/30 chance to switch zigzag direction every frame, freakishly random!
                
            # invaders movement
            invader[0] += cos(invader[2]-HALF_PI) * invader[3]
            invader[1] += sin(invader[2]-HALF_PI) * invader[3]
        
            # spinning speed and acceleration for accelerator invader
            if invader[9] == "accelerator_invader":
                invader[3] += 0.01
                invader[12] = invader[3] / 40
                
def do_ship():
    global ship_mid_x, ship_mid_y, ship_rotation
    
    ship_mid_x = ship_x + ship_width/2
    ship_mid_y = ship_y + ship_height/2
    
    # calculate ship rotation to point to mouse
    if ship_mid_y - mouseY != 0: # stops division by zero
        ship_rotation = atan((mouseX-ship_mid_x) / float(ship_mid_y-mouseY))
        if mouseY > ship_mid_y:
            ship_rotation += PI
        elif mouseX < ship_mid_x:
            ship_rotation += TWO_PI # makes no negative radian numbers for rotation, helpful for other code based on ship_rotation
        
    else: # if division by zero would happen, instead rotation by these fixed amounts
        if mouseX >= ship_x + ship_height / 2:
            ship_rotation = PI * 0.5
        elif mouseX < ship_x + ship_height / 2:
            ship_rotation = PI * 1.5
    
    # draw ship with rotation
    pushMatrix() 
    translate(ship_x + ship_width / 2, ship_y + ship_height / 2)    
    rotate(ship_rotation)
    rectMode(CORNER)
    image(ship_image, 0-ship_width/2-5, 0-ship_height/2-5, ship_width+10, ship_height+10)
    popMatrix()
    
    # hp bar    
    fill(50, 205, 50)
    noStroke()
    rect(ship_mid_x-30, ship_y-40, 20*ship_hp, 15)
    noFill()
    stroke(0,100,150)
    strokeWeight(2)
    rect(ship_mid_x-30, ship_y-40, 60, 15)
    
    # red lined hitbox of ship
    if hitboxes == True:
        noFill()
        strokeWeight(1)
        stroke(255,0,0)
        circle(ship_mid_x, ship_mid_y, ship_width)
        #rect(ship_x, ship_y, ship_width, ship_height)

def move_ship():
    global ship_x, ship_y
    
    # ship movement with wasd keys
    ship_movement_angle = [] # used for calculating the average angle of where the ship is going so you can move in 8 different directions with equal speeds
    
    if key_a == True:
        ship_movement_angle.append(1.5*PI)
    if key_d == True:
        ship_movement_angle.append(0.5*PI)
    if key_w == True:
        if key_a == True:
            ship_movement_angle.append(2*PI) # sometimes 360 degrees is needed for w key for the average angle
        else:
            ship_movement_angle.append(0*PI) # sometimes 0 degrees is needed for w key for the average angle
    if key_s == True:
        ship_movement_angle.append(1*PI)
        
    if (key_a or key_d or key_w or key_s) and not (key_a and key_d and key_w and key_s): # prevents division by zero
        ship_movement_angle = sum(ship_movement_angle) / len(ship_movement_angle)
        ship_x += cos(ship_movement_angle-HALF_PI) * ship_speed
        ship_y += sin(ship_movement_angle-HALF_PI) * ship_speed
    
def do_bullets():
    global bullets, bullet_y, bullet_speed, shoot_delay, burst_counter
    
    # creates delay between each shot
    if shoot_delay > 0:
        shoot_delay -= 1
    elif shoot_delay <= 0 and mousePressed:
        shoot_sound.trigger()
        
        # creates the angle between bullets in a spreadshot
        for n in range(spread_shot): 
            if n % 2 == 0:
                n = n * -1
            n = (n+1)/2
            
            # creates bullets
            bullets.append([ship_mid_x - ship_width/2 * cos(ship_rotation + (HALF_PI)), # [bullet_x, bullet_y, movement_angle, bullet_speed, bullet_diameter, ricochet_count, bullet_hp]
                                ship_mid_y - ship_height/2 * sin(ship_rotation + (HALF_PI)),
                                ship_rotation + ((spread_angle*n)*PI/180),
                                bullet_speed,
                                bullet_diameter,
                                ricochet_count,
                                bullet_hp]) 
        
        # creates a burst shot
        burst_counter += 1
        if burst_counter == burst_shot:
            shoot_delay = shoot_time
            burst_counter = 0
        else:
            shoot_delay = burst_time - 1
    
    # draw bullets
    fill(255)
    strokeWeight(3)
    stroke(255,0,0)
    for i in bullets:
        circle(i[0], i[1], i[4])

def move_bullets():
    for i in bullets:
        i[0] += cos(i[2]-0.5*PI) * i[3]
        i[1] += sin(i[2]-0.5*PI) * i[3]

def do_collisions():
    global ship_hp, bullets, ship_x, ship_y, ship_width, ship_height, invaders, gameScreen, current_score, gameplay_background
    
    # collision between bullets and enemy
    for bullet in bullets:
        for invader in invaders:
            if invader[10] == 0:
                invader_mid_x = invader[0]+invader[4]/2
                invader_mid_y = invader[1]+invader[5]/2
                if sqrt((bullet[0] - invader_mid_x)**2 + (bullet[1] - invader_mid_y)**2) <= bullet_diameter/2 + invader[4]/2:
                    invader[7] -= 1
                    if invader[7] <= 0 and bullet in bullets:
                        
                        if invader[9] == "splitter_invader": # splitter invader spawns 4 icicle invaders when destroyed
                            for i in range(4):
                                spawn_invader("icicle_invader", invader[0], invader[1], random.uniform(0,TWO_PI))
                        
                        current_score += invader[8]
                        invaders.remove(invader)
                    bullet[6] -= 1
                    if bullet[6] <= 0 and bullet in bullets:
                        bullets.remove(bullet)
                        
    # collision for between ship and enemy
    for invader in invaders:
        if invader[10] == 0:
            invader_mid_x = invader[0]+invader[4]/2
            invader_mid_y = invader[1]+invader[5]/2
            if sqrt((ship_mid_x - invader_mid_x)**2 + (ship_mid_y - invader_mid_y)**2) <= ship_width/2 + invader[4]/2:
                invaders.remove(invader)
                ship_hp -= 1
                if ship_hp <= 0:
                    gameplay_background = get()
                    gameScreen = 4
                    
def do_borders():
    global ship_x, ship_y, ship_width, ship_height, ship_speed, invaders
    
    # border design
    stroke(0,100,150)
    noFill()
    strokeWeight(2)
    rect(border_left-1, border_top-1, border_right-border_left+2, border_bottom-border_top+2) # inner border rectangle
    rect(border_left-8, border_top-8, border_right-border_left+16, border_bottom-border_top+16) # outer border rectangle
    
    # ship can't leave borders
    if ship_x <= border_left:
        ship_x = border_left
        
    if ship_x + ship_width >= border_right:
        ship_x = border_right - ship_width 
        
    if ship_y <= border_top:
        ship_y = border_top
        
    if ship_y + ship_height >= border_bottom:
        ship_y = border_bottom - ship_height
    
    # if bullets hit border, remove bullets or bounce bullets if they have ricochet upgrade
    for bullet in bullets: 
        if bullet[0] - bullet[4]/2 <= border_left or bullet[0] + bullet[4]/2 >= border_right or bullet[1] - bullet[4]/2 <= border_top or bullet[1] + bullet[4]/2 >= border_bottom:
            
            # ricochet code
            if bullet[5] > 0:
                if bullet[0] - bullet[4]/2 <= border_left: # bounce off left border
                    bullet[0] = border_left + bullet[4]/2
                    bullet[2] += (PI-bullet[2]) * 2 
                    
                elif bullet[0] + bullet[4]/2 >= border_right: # bounce off right border
                    bullet[0] = border_right - bullet[4]/2
                    bullet[2] += (PI-bullet[2]) * 2 
                    
                elif bullet[1] - bullet[4]/2 <= border_top: # bounces off top border
                    bullet[1] = border_top + bullet[4]/2
                    bullet[2] += (HALF_PI-bullet[2]) * 2 
                    
                elif bullet[1] + bullet[4]/2 >= border_bottom: # bounce off bottom border
                    bullet[1] = border_bottom - bullet[4]/2
                    bullet[2] += (HALF_PI-bullet[2]) * 2 
                
                ricochet_sound.trigger()    
                bullet[5] -= 1 # counts ricochet_count down after bounce
            
            else:
                bullets.remove(bullet) # if no more ricochets left, remove bullet when it hits border
    
    # bounces invaders off border
    for invader in invaders:
        if invader[0] <= border_left: # bounce off left border
            invader[0] = border_left + 1
            if invader[10] == 0:
                invader[2] += (PI-invader[2]) * 2
            
        if invader[0] + invader[4] > border_right: # bounce off right border
            invader[0] = border_right - invader[4] - 1
            if invader[10] == 0:
                invader[2] += (PI-invader[2]) * 2
            
        if invader[1] <= border_top: # bounces off top border
            invader[1] = border_top + 1
            if invader[10] == 0:
                invader[2] += (HALF_PI-invader[2]) * 2
            
        if invader[1] + invader[5] > border_bottom: # bounce off bottom border
            invader[1] = border_bottom - invader[5] - 1
            if invader[10] == 0:
                invader[2] += (HALF_PI-invader[2]) * 2
    
def keyPressed():
    global key_a, key_d, key_w, key_s, gameScreen, gameplay_background, key_pressed
    if key == "a" or key == "A":
        key_a = True
    if key == "d" or key == "D":
        key_d = True
    if key == "w" or key == "W":
        key_w = True
    if key == "s" or key == "S":
        key_s = True
    
    key_pressed = True
    
    # alternate between pause and play with space key
    if gameScreen == 1 and key == " ": 
        gameScreen = 3
    elif gameScreen == 3 and key == " ": 
        gameScreen = 1
        play_music.loop()
    else:
        return
    gameplay_background = get()
    
def keyReleased():
    global  key_a, key_d, key_w, key_s
    if key == "a" or key == "A":
        key_a = False
    if key == "d" or key == "D":
        key_d = False
    if key == "w" or key == "W":
        key_w = False
    if key == "s" or key == "S":
        key_s = False
    
def mouseClicked():
    global mouse_clicked
    mouse_clicked = True
    
def mouseWheel(event):
    global leaderboards_y_scroll
    if gameScreen == 7:
        leaderboards_y_scroll += event.getCount()*-25
        
        # no scrolling beyond the list of names
        if leaderboards_y_scroll > 0 or num_rankings <= 8:
            leaderboards_y_scroll = 0
        elif leaderboards_y_scroll < (num_rankings-8) * -50:
            leaderboards_y_scroll = (num_rankings-8) * -50
        
        
        
        
