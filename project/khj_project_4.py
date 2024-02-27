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

#폰트 정의
game_font = pygame.font.Font(None, 40) #폰트 객체 생성 (폰트, 크기)
#게임 시작
game_start = "press enter to start"
#게임 결과
game_result = "GAME OVER"
#게임 제목
game_title = "201618973 GAME"
#1.사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__)


#배경(시작화면 and 배경화면)
start_bg = pygame.image.load(os.path.join(current_path,"start_bg.png"))
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
character_speed = 0.5

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
enemy_height = enemy_size[1]

#enemy2 만들기
enemy2 = pygame.image.load(os.path.join(current_path, "enemy2.png"))
enemy2_size = enemy2.get_rect().size
enemy2_width = enemy2_size[0]
enemy2_height = enemy2_size[1]

#item 만들기
item = pygame.image.load(os.path.join(current_path, "item.png"))
item_size = item.get_rect().size
item_width = item_size[0]
item_height = item_size[1]

#무기 연속 발사 
weapons = []
#enemy1 연속 생성
enemys = []
#enemy2 연속 생성
enemys2 = []
#item 연속 생성
items = []
#무기 속도
weapon_speed = 15 
#enemy 속도
enemy_speed = 2
#enemy2 속도
enemy2_speed = 1
#item 속도
item_speed = 3

# 무기 삭제위한 변수
weapon_remove = -1
# enemy1 삭제위한 변수
enemy_remove = -1
# enemy2 삭제위한 변수
enemy2_remove = -1
#item 삭제 위한 변수
item_remove = -1

#1초마다 재기 위한 변수
time_check = 1
time_check2 = 5
time_check3 = 10
#시작 시간
start_ticks = pygame.time.get_ticks()  # 시작 tick 을 받아옴
#놓친 enemy수
enemy_pass = 0
running =True
start = False
while running:
    dt= clock.tick(200) #게임화면 초당 프레임수


    # 처음 시작 화면(엔터를 누르면 게임이 시작됨)
    if start == False:
        game_initial = game_font.render(game_start, True, (255, 0, 0))
        game_title2 = game_font.render(game_title, True, (255,255,0))
        screen.blit(start_bg, (0,0))
        screen.blit(game_initial, (250, 400))
        screen.blit(game_title2,(250,200))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = True
                    start_ticks = pygame.time.get_ticks()  # 시작 tick 을 받아옴
            if event.type == pygame.QUIT:
                running= False


    #경과 시간
    elapsed_time = (pygame.time.get_ticks() - start_ticks) /1000


    
    #2. 이벤트 처리(키보드, 마우스 등) 
    if start:
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

            
        
        # enemy1 1초마다 생성
        if int(elapsed_time) == int(time_check) :
            enemy_x = 790
            enemy_y = random.randrange(enemy_height,screen_height-enemy_height)  
            enemys.append([enemy_x, enemy_y])
            time_check +=1 
            
        
        #enemy2 5초마다 생성 and enemy2는 2번 공격 명중시켜야 제거
        if int(elapsed_time) == time_check2 :
            enemy2_x = 790
            enemy2_y = random.randrange(enemy2_height,screen_height-enemy2_height)
            if elapsed_time != 20:
                enemys2.append([enemy2_x, enemy2_y]) 
                enemys2.append([enemy2_x, enemy2_y])
            time_check2 += 5
        
        # 10초 마다 아이템 생성(놓친 enemy수를 0으로 초기화 시켜주는 아이템)
        if int(elapsed_time) == time_check3 :
            item_x = 790
            item_y = random.randrange(enemy2_height,screen_height-enemy2_height)
            if elapsed_time != 20:
                items.append([item_x, item_y])
            time_check3 += 10
        

        #3. 게임 캐릭터 위치 정의
        character_x_pos += to_x *dt
        character_y_pos += to_y *dt

        #무기 위치 조정
        weapons = [[w[0]+ weapon_speed, w[1] ] for w in weapons]  #무기의 위치를 옆으로
        #enemy1 위치 조정
        enemys = [[k[0]-enemy_speed, k[1] ] for k in enemys] #enemy 위치를 반대로
        #enemy2 위치 조정
        enemys2 = [[k[0]-enemy2_speed, k[1] ] for k in enemys2] #enemy2 위치를 반대로
        #item 위치 조정
        items =  [[k[0]-item_speed, k[1] ] for k in items]
    


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


        #아이템 먹기
        for item_idx, item_val in enumerate(items):
            item_pos_x = item_val[0]
            item_pos_y = item_val[1]

            item_rect = item.get_rect()
            item_rect.left = item_pos_x
            item_rect.top = item_pos_y

            if character_rect.colliderect(item_rect):
                enemy_pass = 0
                item_remove = item_idx



        #enemy1에 의한 충돌
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

        #enemy2에 의한 충돌
        for enemy2_idx, enemy2_val in enumerate(enemys2):
            enemy2_pos_x = enemy2_val[0]
            enemy2_pos_y = enemy2_val[1]

            enemy2_rect = enemy2.get_rect()
            enemy2_rect.left = enemy2_pos_x
            enemy2_rect.top = enemy2_pos_y

            if character_rect.colliderect(enemy2_rect):
                running = False

            
            
            for weapon_idx, weapon_val in enumerate(weapons):
                weapon_x = weapon_val[0]
                weapon_y = weapon_val[1]

                weapon_rect = weapon.get_rect()
                weapon_rect.left = weapon_x
                weapon_rect.top = weapon_y
                if weapon_rect.colliderect(enemy2_rect):
                    weapon_remove = weapon_idx
                    enemy2_remove = enemy2_idx
                    break

        #충돌후 이미지 삭제
        if weapon_remove != -1:
            del weapons[weapon_remove]
            weapon_remove = -1
        if enemy2_remove != -1:
            del enemys2[enemy2_remove]
            enemy2_remove = -1
        if enemy_remove != -1:
            del enemys[enemy_remove]
            enemy_remove = -1
        if item_remove != -1:
            del items[item_remove]
            item_remove = -1


        #놓친 enemy 세기
        for enemy_idx, enemy_val in enumerate(enemys):
            enemy_pos_x = enemy_val[0]
            enemy_pos_y = enemy_val[1]

            if enemy_pos_x <= 0:
                enemy_pass += 1
                del enemys[enemy_idx]
        #놓친 enemy2 세기(기본 2이로 취급, 한방 맞추고 놓치면 1로 취급)
        for enemy2_idx, enemy2_val in enumerate(enemys2):
            enemy2_pos_x = enemy2_val[0]
            enemy2_pos_y = enemy2_val[1]

            if enemy2_pos_x <= 0:
                enemy_pass += 1
                del enemys2[enemy2_idx]
        
        #5.화면에 그리기
        screen.blit(bg,(0,0))
        screen.blit(character,(character_x_pos,character_y_pos))
        for enemy_x, enemy_y in enemys:
            screen.blit(enemy,(enemy_x,enemy_y))

        for enemy2_x, enemy2_y in enemys2:
            screen.blit(enemy2,(enemy2_x,enemy2_y))
        
        for weapon_x_pos, weapon_y_pos in weapons:
            screen.blit(weapon,(weapon_x_pos, weapon_y_pos))

        for item_x_pos, item_y_pos in items:
            screen.blit(item,(item_x_pos, item_y_pos))


 
        #놓친 enemy수 화면에 표시
        enemy_pass_font = game_font.render(str(enemy_pass),True, (255,255,255))
        screen.blit(enemy_pass_font,(10,10))

        

        #놓친 enemy가 30이 되면 게임오버시키고 화면에 메시지 출력
        if enemy_pass == 5:
            game_result = "GAME OVER"
            running = False
    
        #20초후에 2라운드로 넘어가기 and 난이도 up
        if int(elapsed_time) == 20 :
            while len(enemys) != 0 :
                for a,b in enumerate(enemys2) :
                    del enemys2[a]
                for i,j in enumerate(enemys) :
                    del enemys[i]
                for i,j in enumerate(items) :
                    del items[i]
            
            enemy_speed *= 1.5
            enemy2_speed *= 1.5
            next_stage = game_font.render("s t a g e 2",True,(255, 0, 0))
            screen.blit(start_bg,(0,0))
            screen.blit(next_stage,(300, screen_height/2))
            pygame.display.update()
            pygame.time.delay(2000)
            time_check += 2
            time_check2 += 2
            time_check3 += 2
            print(int(elapsed_time))
            print(time_check2)
            enemy_pass = 0
        #40초 버티면 게임 클리어
        if int(elapsed_time) == 42 :
            stage_clear = game_font.render("congratulations! all clear!",True,(255, 0, 0))
            screen.blit(start_bg,(0,0))
            screen.blit(stage_clear,(200, screen_height/2))
            pygame.display.update()
            pygame.time.delay(2000)
            start = False
            running = False

        pygame.display.update()

#게임 클리어 못했을시 출력화면
if start == True:
    game_over = game_font.render(game_result, True, (255, 0, 0))
    screen.blit(game_over, (300, screen_height/2))
    pygame.display.update()


#2초 대기
if start == True:
    pygame.time.delay(2000)

    


pygame.quit()