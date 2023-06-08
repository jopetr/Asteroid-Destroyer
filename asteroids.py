import pygame
import math
from random import random as random
from random import randint as randint
import csv

def center_dist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((x1-x2)**2 + (y1-y2)**2)**0.5



def generate_asteroids(num, width, height, curr_ticks):
    asteroids = []
    deployment_delay = 1000 + curr_ticks
    for i in range(num):
        if i>0:
            deployment_delay += random()*3000
        asteroid_size = 70 + random()*30
        positions = [0, 1, 2, 3]
        start = randint(0, 3)
        positions.remove(start)
        end = positions[randint(0, 2)]
        if start == 0:
            start = (random()*width,  -1*asteroid_size/2)
        elif start == 1:
            start = (random()*width, height + asteroid_size/2)
        elif start == 2:
            start = (-1*asteroid_size/2, random()*height)
        else:
            start = (width + asteroid_size/2, random()*height)
            
        if end == 0:
            end = (random()*width, -1*asteroid_size/2)
        elif end == 1:
            end = (random()*width, height + asteroid_size/2)
        elif end == 2:
            end = (-1*asteroid_size/2, random()*height)
        else:
            end = (width + asteroid_size/2, random()*height)
        image_choice = randint(0, 4)
        asteroids.append([start, end, start, asteroid_size, -1, 0, image_choice, deployment_delay])
    return asteroids

def load_high_scores():
    with open('csv/high_scores.csv') as csvfile:
        scores = csv.reader(csvfile, delimiter=' ', quotechar='|')
        high_scores = []
        for row in scores:
            high_scores.append(int(row[0]))
        return high_scores

def save_high_scores(scores = [0,0,0,0,0]):
    new_scores = scores
    new_scores.sort(reverse=True)
    new_high_scores = []
    for i in range(5):
        new_high_scores.append([str(new_scores[i])])
    with open('csv/high_scores.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_high_scores)
    return new_scores[0:4]

def run_menu(height, width, display_surface, started_yet):
    pygame.mixer.music.set_volume(1.0)
    all_scores = load_high_scores()
    image = pygame.image.load("images/surface.png").convert()
    image = pygame.transform.scale(image, (height, width))

    black_image = pygame.image.load("images/black_screen.png").convert()
    black_image = pygame.transform.scale(black_image, (height, width))

    star = pygame.image.load("images/star.png").convert_alpha()

    title = pygame.image.load("images/title.png").convert_alpha()

    start0 = pygame.image.load("images/start0.png").convert_alpha()
    start0 = pygame.transform.scale(start0, (250, 100))
    start1 = pygame.image.load("images/start1.png").convert_alpha()
    start1 = pygame.transform.scale(start1, (250, 100))
    start0_rect = start0.get_rect()
    start1_rect = start1.get_rect()
    start0_rect.center = (width/2, 650)
    start1_rect.center = start0_rect.center

    high_scores = pygame.image.load("images/high_scores.png").convert_alpha()
    high_scores = pygame.transform.scale(high_scores, (200, 80))

    play_again0 = pygame.image.load("images/play_again0.png").convert_alpha()
    play_again0 = pygame.transform.scale(play_again0, (250, 100))
    play_again1 = pygame.image.load("images/play_again1.png").convert_alpha()
    play_again1 = pygame.transform.scale(play_again1, (250, 100))
    play_again0_rect = play_again0.get_rect()
    play_again1_rect = play_again1.get_rect()
    play_again0_rect.center = (width/2, 650)
    play_again1_rect.center = play_again0_rect.center


    number_images = []

    start_clicked = False
    for i in range(10):
        number_images.append(pygame.image.load("images/"+str(i)+".png").convert_alpha())
        number_images[i] = pygame.transform.scale(number_images[i], (20, 20))

    stars = []
    for i in range(100):
        star_size = round(1+random()*9)
        star_x = round(10 + random()*(width - 10))
        star_y = round(10 + random()*(height - 10))
        s_tick = round(random()*10000)
        e_tick = s_tick+round(random()*2000+500)
        stars.append([star_size, star_x, star_y, s_tick, e_tick])
    clock = pygame.time.Clock()
    start_ticks = -1
    start_time = -1
    start_game = False

    while not start_game:
        clicked = False
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
        curr_ticks = pygame.time.get_ticks()
        if start_ticks == -1:
            start_ticks = curr_ticks

        display_surface.blit(start0, start0_rect)
        
        display_surface.blit(image, (0, 0))
        for s in stars:
            ticks = pygame.time.get_ticks()
            star_size = s[0]
            s_tick = s[3]
            e_tick = s[4]
            if ticks > e_tick:
                s[3] = s[4] + round(random()*10000)
                s[4] = s[3] + round(random()*2000+500)
                s[1] = round(10 + random()*(width - 10))
                s[2] = round(10 + random()*(height - 10))
            elif ticks > s_tick:
                loop_point = 2*(ticks - s_tick)/(e_tick-s_tick)
                alpha = 0
                if loop_point <=1:
                    alpha = round(255*(loop_point))
                else:
                    alpha = round(255*(1-(loop_point-1)))
                
                custom_star = pygame.transform.scale(star, (star_size, star_size))
                custom_star.set_alpha(alpha)
                display_surface.blit(custom_star, (s[1], s[2]))
            
        display_surface.blit(title, (width/2-500/2, 50))
        if not started_yet:
            if start0_rect.collidepoint(pygame.mouse.get_pos()):
                display_surface.blit(start1, start1_rect)
                if clicked == True and not start_clicked:
                    start_time = curr_ticks
            else:
                display_surface.blit(start0, start0_rect)
        else:
            if play_again0_rect.collidepoint(pygame.mouse.get_pos()):
                display_surface.blit(play_again1, play_again1_rect)
                if clicked == True and not start_clicked:
                    start_time = curr_ticks
            else:
                display_surface.blit(play_again0, play_again0_rect)

        display_surface.blit(high_scores, (width/2-200/2, 225))

        for j in range(5):
            score = all_scores[j]
            score_len = math.floor(math.log(score+1, 10))+1
            text_len = score_len*20 + (score_len-1)*5
            temp1 = score
            for i in range(score_len):
                temp2 = temp1%10
                display_surface.blit(number_images[int(temp2)], ((width/2+text_len/2-(i+1)*20-i*5), 325+40*j))
                temp1 = (temp1-temp2)/10

        if start_time!=-1:
            if (start_time + 1000)>=curr_ticks:
                alpha = 255*(curr_ticks - start_time)/1000
                black_image.set_alpha(alpha)
                display_surface.blit(black_image, (0,0))
                pygame.mixer.music.set_volume(1.0 - (curr_ticks - start_time)/1000)
            else:
                black_image.set_alpha(255)
                display_surface.blit(black_image, (0,0))
                start_game = True
                pygame.mixer.music.set_volume(1.0 - (curr_ticks - start_time)/1000)

        if (start_ticks + 1000)>=curr_ticks:
            alpha = 255 - 255*(curr_ticks - start_ticks)/1000
            black_image.set_alpha(alpha)
            display_surface.blit(black_image, (0,0))
        
        pygame.display.flip()
        clock.tick(60)
    

def run_game(height, width, display_surface):
    
    
    #Sounds
    all_scores = load_high_scores()
    
    laser_sound = pygame.mixer.Sound('sounds/laser.wav')
    thruster_sound = pygame.mixer.Sound('sounds/thruster.wav')
    collision_sound = pygame.mixer.Sound('sounds/starship_collision.wav')
    game_over_sound = pygame.mixer.Sound('sounds/game_over.wav')
    explosion_sounds = []
    for i in range(4):
        explosion_sounds.append(pygame.mixer.Sound('sounds/explosion'+str(i)+'.wav'))

    
     
    image = pygame.image.load("images/surface.png").convert()
    image = pygame.transform.scale(image, (height, width))

    black_image = pygame.image.load("images/black_screen.png").convert()
    black_image = pygame.transform.scale(black_image, (height, width))
    
    ship_size = 80
    starship = pygame.image.load("images/starship.png").convert_alpha()
    starship = pygame.transform.scale(starship, (ship_size, ship_size))

    high_scores_image = pygame.image.load("images/high_scores.png").convert_alpha()

    thrusters = pygame.image.load("images/starshipthrusters.png").convert_alpha()
    thrusters = pygame.transform.scale(thrusters, (ship_size, ship_size))

    lasers = pygame.image.load("images/starshiplasers.png").convert_alpha()
    lasers = pygame.transform.scale(lasers, (ship_size, ship_size))

    blasts = pygame.image.load("images/blasts.png").convert_alpha()
    blasts = pygame.transform.scale(blasts, (ship_size, ship_size))

    star = pygame.image.load("images/star.png").convert_alpha()

    game_over_image = pygame.image.load("images/game_over.png").convert_alpha()
    new_high_score_image = pygame.image.load("images/new_high_score.png").convert_alpha()

    number_images = []
    for i in range(10):
        number_images.append(pygame.image.load("images/"+str(i)+".png").convert_alpha())
        number_images[i] = pygame.transform.scale(number_images[i], (20, 20))

    big_number_images = []
    for i in range(10):
        big_number_images.append(pygame.image.load("images/"+str(i)+".png").convert_alpha())
        big_number_images[i] = pygame.transform.scale(big_number_images[i], (50, 50))

    asteroid_images = []
    asteroid_images.append(pygame.image.load("images/asteroid1.png").convert_alpha())
    asteroid_images.append(pygame.image.load("images/asteroid2.png").convert_alpha())
    asteroid_images.append(pygame.image.load("images/asteroid3.png").convert_alpha())
    asteroid_images.append(pygame.image.load("images/asteroid4.png").convert_alpha())
    asteroid_images.append(pygame.image.load("images/asteroid5.png").convert_alpha())

    explosion_images = []
    explosion_images.append(pygame.image.load("images/explosion1.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion2.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion3.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion4.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion5.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion6.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion7.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion8.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion9.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion10.png").convert_alpha())
    explosion_images.append(pygame.image.load("images/explosion11.png").convert_alpha())

    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_image = pygame.transform.scale(life_image, (width/25, height/25))

    stars = []
    for i in range(100):
        star_size = round(1+random()*9)
        star_x = round(10 + random()*(width - 10))
        star_y = round(10 + random()*(height - 10))
        s_tick = round(random()*10000)
        e_tick = s_tick+round(random()*2000+500)
        stars.append([star_size, star_x, star_y, s_tick, e_tick])
    clock = pygame.time.Clock()
    prev_angle = 0
    max_velocity = 3
    velocity = 1
    thrusters_in_use = False
    lasers_in_use = False
    lasers_shot = False
    blasts_list = []
    starship_position = (width/2, height/2)
    move_forward = False
    rotate_left = False
    rotate_right = False
    turn_speed = 3

    asteroid_velocity = 0.001

    asteroids_remaining = 6
    asteroids = generate_asteroids(asteroids_remaining, width, height, pygame.time.get_ticks())
    wave = 1
    lives = 3
    starship_collision = False
    starship_collision_tick = 0
    score = 0

    explosions = []

    end_tick = -1

    thruster_used = False
    new_high_score = False
    start_ticks = -1
    game_ended = False
    while not game_ended:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()  
            if event.type == pygame.KEYDOWN:
                if event.key == ord('w'):
                    thrusters_in_use = True
                    move_forward = True
                    velocity = max_velocity
                if event.key == ord('a'):
                    rotate_right = True
                if event.key == ord('d'):
                    rotate_left = True
                if event.key == pygame.K_RETURN:
                    lasers_in_use = True
                    lasers_shot = True
                pygame.event.clear()
            if event.type == pygame.KEYUP:
                if event.key == ord('w'):
                    thrusters_in_use = False
                    move_forward = False
                    thruster_used = False
                if event.key == ord('a'):
                    rotate_right = False
                if event.key == ord('d'):
                    rotate_left = False
                if event.key == pygame.K_RETURN:
                    lasers_in_use = False
                pygame.event.clear()

        curr_ticks = pygame.time.get_ticks()
        if start_ticks == -1:
            start_ticks = curr_ticks
        
        if asteroids_remaining == 0 and len(asteroids)==0:
            wave+=1
            asteroid_velocity+=0.0003
            asteroids_remaining = 6 + 2*(wave-1)
            asteroids = generate_asteroids(asteroids_remaining, width, height, curr_ticks)

        if starship_collision and curr_ticks>=(starship_collision_tick+3000) and lives>1:
            prev_angle = 0
            thrusters_in_use = False
            lasers_in_use = False
            lasers_shot = False
            blasts_list = []
            starship_position = (width/2, height/2)
            move_forward = False
            rotate_left = False
            rotate_right = False
            velocity = 0
            asteroids = generate_asteroids(asteroids_remaining, width, height, curr_ticks)
            starship_collision = False
            lives-=1
        
        curr_angle = prev_angle
            
       
        if not starship_collision:
            if rotate_left and not rotate_right:
                curr_angle -= turn_speed
            elif rotate_right and not rotate_left:
                curr_angle += turn_speed
        if velocity>0 and not starship_collision:
            
            ang = (curr_angle-90)*(math.pi*2)/360
            x, y = starship_position
            x -= math.cos(ang)*velocity
            y += math.sin(ang)*velocity
            if x<-10:
                x=-10
            elif x>(width+10):
                x=width+10
            if y<-10:
                y=-10
            elif y>(height+10):
                y=height+10
            starship_position = (x, y)
            if not move_forward:
                velocity -= 0.02
                if velocity < 0.4:
                    velocity = 0.4

        display_surface.blit(image, (0, 0))

        for s in stars:
            ticks = pygame.time.get_ticks()
            star_size = s[0]
            s_tick = s[3]
            e_tick = s[4]
            if ticks > e_tick:
                s[3] = s[4] + round(random()*10000)
                s[4] = s[3] + round(random()*2000+500)
                s[1] = round(10 + random()*(width - 10))
                s[2] = round(10 + random()*(height - 10))
            elif ticks > s_tick:
                loop_point = 2*(ticks - s_tick)/(e_tick-s_tick)
                alpha = 0
                if loop_point <=1:
                    alpha = round(255*(loop_point))
                else:
                    alpha = round(255*(1-(loop_point-1)))
                
                custom_star = pygame.transform.scale(star, (star_size, star_size))
                custom_star.set_alpha(alpha)
                display_surface.blit(custom_star, (s[1], s[2]))

        
        
        rotated_starship = pygame.transform.rotate(starship, curr_angle)
        starship_rect = rotated_starship.get_rect()
        starship_rect.center = (starship_position[0], starship_position[1])
        display_surface.blit(rotated_starship, starship_rect)

        if thrusters_in_use and not starship_collision:
            
            if not thruster_used:
                pygame.mixer.Sound.play(thruster_sound)
                thruster_used = True
            rotated_thrusters = pygame.transform.rotate(thrusters, curr_angle)
            thrusters_rect = rotated_thrusters.get_rect()
            thrusters_rect.center = (starship_position[0], starship_position[1])
            display_surface.blit(rotated_thrusters, thrusters_rect)

        if lasers_in_use and not starship_collision:
            rotated_lasers = pygame.transform.rotate(lasers, curr_angle)
            lasers_rect = rotated_lasers.get_rect()
            lasers_rect.center = (starship_position[0], starship_position[1])
            display_surface.blit(rotated_lasers, lasers_rect)
        
        if lasers_shot and not starship_collision:
            blasts_list.append([curr_angle, starship_position[0], starship_position[1]])
            pygame.mixer.Sound.play(laser_sound)
            lasers_shot = False
        
        if len(blasts_list)>0:
            remove_list = []
            for i in range(len(blasts_list)):
                    angle = blasts_list[i][0]
                    if not starship_collision:
                        ang = (angle-90)*(math.pi*2)/360
                    rotated_blasts = pygame.transform.rotate(blasts, angle)
                    blasts_rect = rotated_blasts.get_rect()
                    blasts_rect.center = (round(blasts_list[i][1]),round(blasts_list[i][2]))
                    if not starship_collision:
                        blasts_list[i][1] -= math.cos(ang)*10
                        blasts_list[i][2] += math.sin(ang)*10
                        removed_yet = False
                        if (blasts_list[i][1]>(width+10) or blasts_list[i][1]<(-10) or blasts_list[i][2]>(height + 10) or blasts_list[i][2]<(-10)):
                            remove_list.append(i)
                            removed_yet = True
                        else:
                            asteroids_remove_list = []
                            for j in range(len(asteroids)):
                                a = asteroids[j]
                                prox = False
                                if center_dist(starship_rect.center, a[2])<=ship_size/2:
                                    prox = not removed_yet and center_dist(blasts_rect.center, a[2])<(ship_size/2+a[3]/2)
                                else:
                                    prox = not removed_yet and center_dist(blasts_rect.center, a[2])<(ship_size/3+a[3]/2)
                                if prox:
                                    #asteroids.append([start, end, start, asteroid_size, -1, 0, image_choice, deployment_delay])
                                    asteroids_remaining -= 1
                                    score+=10
                                    explosions.append([a[2], 0, a[3]])
                                    asteroids_remove_list.append(j)
                                    remove_list.append(i)
                            new_asteroids = []
                            for j in range(len(asteroids)):
                                if j not in asteroids_remove_list:
                                    new_asteroids.append(asteroids[j])
                            asteroids = new_asteroids
                    display_surface.blit(rotated_blasts, blasts_rect)
            new_blasts_list = []
            for i in range(len(blasts_list)):
                if i not in remove_list:
                    new_blasts_list.append(blasts_list[i])
            blasts_list = new_blasts_list

        remove_list = []
        for i in range(len(explosions)):
            x, y = explosions[i][0]
            explosion = explosions[i][1]
            asteroid_size = explosions[i][2]
            if explosion>=0:
                if explosion == 0:
                    pygame.mixer.Sound.play(explosion_sounds[randint(0,3)])
                explosion_size = asteroid_size + (asteroid_size/2)*(explosion/21)
                explosion_image = pygame.transform.scale(explosion_images[math.floor(explosion/2)], (explosion_size, explosion_size))
                explosion_image = pygame.transform.rotate(explosion_image, random()*360)
                explosion_rect = explosion_image.get_rect()
                explosion_image.set_alpha(200)
                explosion_rect.center = (x, y)
                display_surface.blit(explosion_image, explosion_rect)
                explosion += 1
                if explosion > 21:
                    remove_list.append(i)
                explosions[i][1] = explosion
        new_explosions = []
        for i in range(len(explosions)):
            if i not in remove_list:
                new_explosions.append(explosions[i])
        explosions = new_explosions
        
        remove_list = []
        for i in range(len(asteroids)):
            
            a = asteroids[i]
            if a[7]<curr_ticks:
                sx, sy = a[0]
                ex, ey = a[1]
                x, y = a[2]

                asteroid_size = a[3]
                explosion = a[4]
                angle = a[5]
                
                asteroid_image = pygame.transform.scale(asteroid_images[a[6]], (asteroid_size, asteroid_size))
                asteroid_image = pygame.transform.rotate(asteroid_image, angle)
                
                asteroid_rect = asteroid_image.get_rect()
                asteroid_rect.center = (x, y)
                display_surface.blit(asteroid_image, asteroid_rect)

                
                
                if not starship_collision and center_dist(starship_rect.center, a[2]) < (0.7*(asteroid_size+ship_size)/2):
                    starship_collision = True
                    starship_collision_tick = curr_ticks
                    pygame.mixer.Sound.play(collision_sound)
                
                if not starship_collision:
                    
                    a[5] += 0.5
                    pos = (((sx-x)**2 + (sy-y)**2)**0.5)/(((sx-ex)**2 + (sy-ey)**2)**0.5)
                    if (pos>1):
                        positions = [0, 1, 2, 3]
                        start = randint(0, 3)
                        positions.remove(start)
                        end = positions[randint(0, 2)]
                        if start == 0:
                            start = (random()*width, -1*asteroid_size/2)
                        elif start == 1:
                            start = (random()*width, height + asteroid_size/2)
                        elif start == 2:
                            start = (-1*asteroid_size/2, random()*height)
                        else:
                            start = (width + asteroid_size/2, random()*height)

                        if end == 0:
                            end = (random()*width, -1*asteroid_size/2)
                        elif end == 1:
                            end = (random()*width, height + asteroid_size/2)
                        elif end == 2:
                            end = (-1*asteroid_size/2, random()*height)
                        else:
                            end = (width + asteroid_size/2, random()*height)
                        a[0] = start
                        a[1] = end
                        a[2] = start
                    else:
                        pos += asteroid_velocity*(((height**2 + width**2)**0.5)/(((sx-ex)**2 + (sy-ey)**2)**0.5))
                        x = (ex-sx)*pos+sx
                        y = (ey-sy)*pos+sy
                        a[2] = (x, y)
        if score == 0:
            display_surface.blit(number_images[0], (width-30, 10))
        else:
            score_len = math.floor(math.log(score, 10))+1
            temp1 = score
            for i in range(score_len):
                temp2 = temp1%10
                display_surface.blit(number_images[int(temp2)], ((width-25-25*i), 10))
                temp1 = (temp1-temp2)/10
                
                
        for i in range(lives):
            if end_tick==-1:
                if i==(lives-1) and starship_collision:
                    alpha = 255*((1000-(curr_ticks-starship_collision_tick)%1000)/1000)
                    life_image_fading = life_image.copy()
                    life_image_fading.set_alpha(alpha)
                    display_surface.blit(life_image_fading, (20+i*35, 10))
                else:
                    display_surface.blit(life_image, (20+i*35, 10))
            else:
                if curr_ticks<(end_tick+3000):
                    alpha = 255*((1000-(curr_ticks-starship_collision_tick)%1000)/1000)
                    life_image_fading = life_image.copy()
                    life_image_fading.set_alpha(alpha)
                    display_surface.blit(life_image_fading, (20+i*35, 10))

        if lives == 1 and starship_collision:
            if end_tick == -1:
                end_tick = curr_ticks
                pygame.mixer.Sound.play(game_over_sound)
                all_scores.append(score)
                high_scores = save_high_scores(all_scores)
                if score in high_scores and score>0:
                    new_high_score = True
            display_surface.blit(game_over_image, (width/2-500/2, 300))
            if new_high_score:
                pos = ((curr_ticks - end_tick)%2000)/1000
                if pos >= 1:
                    pos = 2 - pos
                score_width = 200+50*pos
                new_high_score_im = pygame.transform.scale(new_high_score_image, (score_width, 0.4*score_width))
                new_high_score_rect = new_high_score_im.get_rect()
                new_high_score_rect.center = (width/2, 300)
                display_surface.blit(new_high_score_im, new_high_score_rect)
            if score == 0:
                display_surface.blit(big_number_images[0], (width/2-25, 500))
            else:
                score_len = math.floor(math.log(score, 10))+1
                text_len = score_len*50 + (score_len-1)*12
                temp1 = score
                for i in range(score_len):
                    temp2 = temp1%10
                    display_surface.blit(big_number_images[int(temp2)], ((width/2+text_len/2-(i+1)*50-i*12), 500))
                    temp1 = (temp1-temp2)/10

        if (start_ticks + 1000)>=curr_ticks:
            alpha = 255 - 255*(curr_ticks - start_ticks)/1000
            black_image.set_alpha(alpha)
            black_rect = black_image.get_rect()
            display_surface.blit(black_image, (0,0))

        if end_tick != -1 and end_tick+5000<=curr_ticks:
            alpha = 255*(curr_ticks - (end_tick+5000))/1000
            black_image.set_alpha(alpha)
            black_rect = black_image.get_rect()
            display_surface.blit(black_image, (0,0))
            if curr_ticks>=(end_tick+6000):
                game_ended = True

        pygame.display.flip()
        prev_angle = curr_angle
        clock.tick(60)

if __name__ == "__main__":
    
    pygame.init()
    pygame.mixer.music.load('sounds/menu.wav')
    height = 800  
    width = 800
    display_surface = pygame.display.set_mode((height, width))
    pygame.display.set_caption('Asteroid Destroyer')
    started_yet = False
    while True:
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1.0)
        run_menu(height, width, display_surface, started_yet)
        pygame.mixer.music.pause()
        started_yet = True
        run_game(height, width, display_surface)
        pygame.mixer.music.unpause()