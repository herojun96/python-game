import pygame
import os
import random
#######################################################################
#기본 초기화(반드시 해야 하는 것들)
pygame.init() #초기화

#화면 크기 설정
screen_width=800 #가로크기
screen_height=500 #세로크기
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("khj game") #게임 이름

#FPS
clock = pygame.time.Clock()
##########################################################################




#1.사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)


#배경
bg = pygame.image.load(os.path.join(current_path, "bg.png"))
#캐릭터 만들기
character = pygame.image.load(os.path.join(current_path, "character.png"))
character_rect = character.get_rect()
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = character_width
character_y_pos = (screen_height/2) - (character_height/2)
#캐릭터 스피드
character_speed = 0.9

#이동할 좌표
to_x = 0 
to_y = 0

#무기 만들기
weapon = pygame.image.load(os.path.join(current_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#enemy1 만들기
enemy = pygame.image.load(os.path.join(current_path, "enemy1.png"))
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]





#무기 연속 발사 
weapons = []
#enemy1 연속 생성
enemys = []

#무기 속도
weapon_speed = 15 
#enemy 속도
enemy_speed = 4


# 무기 삭제위한 변수
weapon_remove = -1
# enemy1 삭제위한 변수
enemy_remove = -1


#1초마다 재기 위한 변수
time_check = 1


#시작 시간
start_ticks = pygame.time.get_ticks()  # 시작 tick 을 받아옴



running =True
while running:
    dt= clock.tick(60) #게임화면 초당 프레임수

    
 
    
    #2. 이벤트 처리(키보드, 마우스 등) 
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running= False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x +=character_speed
            elif event.key == pygame.K_UP:
                to_y -=character_speed
            elif event.key == pygame.K_DOWN:
                to_y +=character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + character_width
                weapon_y_pos = character_y_pos +(character_width/2) - (weapon_width/2)
                weapons.append([weapon_x_pos, weapon_y_pos])        


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x =0 
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y =0

    elapsed_time = (pygame.time.get_ticks() - start_ticks) /1000
       
        # enemy1 1초마다 생성
    print(int(elapsed_time))
    if (int(elapsed_time)) == time_check :
        enemy_x = 790
        enemy_y = random.randrange(0,screen_height)
        enemys.append([enemy_x, enemy_y])
        time_check +=1 
       
     

    #3. 게임 캐릭터 위치 정의
    character_x_pos += to_x *dt
    character_y_pos += to_y *dt

    #무기 위치 조정
    weapons = [[w[0]+ weapon_speed, w[1] ] for w in weapons]  #무기의 위치를 옆으로
    #enemy1 위치 조정
    enemys = [[k[0]-enemy_speed, k[1] ] for k in enemys] #enemy 위치를 반대로
    
    

    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos =0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    #세로 경계값 처리 
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height -character_height:
        character_y_pos = screen_height -character_height


    #4. 충돌 처리
    character_rect = character.get_rect()    
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    #enemy1에 의한 충동
    for enemy_idx, enemy_val in enumerate(enemys):
        enemy_pos_x = enemy_val[0]
        enemy_pos_y = enemy_val[1]

        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_pos_x
        enemy_rect.top = enemy_pos_y

        if character_rect.colliderect(enemy_rect):
            running = False

        
        
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x = weapon_val[0]
            weapon_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x
            weapon_rect.top = weapon_y
            if weapon_rect.colliderect(enemy_rect):
                weapon_remove = weapon_idx
                enemy_remove = enemy_idx
                break
     
    if weapon_remove != -1:
        del weapons[weapon_remove]
        weapon_remove = -1
    if enemy_remove != -1:
        del enemys[enemy_remove]
        enemy_remove = -1
        
    #5.화면에 그리기
    screen.blit(bg,(0,0))
    screen.blit(character,(character_x_pos,character_y_pos))
    for enemy_x, enemy_y in enemys:
        screen.blit(enemy,(enemy_x,enemy_y))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos, weapon_y_pos))

    pygame.display.update() 


pygame.quit()