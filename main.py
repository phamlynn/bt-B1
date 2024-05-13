import random
import pygame
from actions.bullet import bulletShot
from actions.colition import isColition, isColitionShip_Enemy
from actions.gameOver import printGameOver
from actions.points import printPoint
from enemy.enemyRol import enemy_func
from pygame import mixer
from player.playerRol import player_func


pygame.init()

def main():
    screen = pygame.display.set_mode((1000,600))
    pygame.display.set_caption("Game cua Lien")
    ico = pygame.image.load('./asset/icons8-flying-saucer-32.png')
    pygame.display.set_icon(ico)

    background = pygame.image.load('./asset/BG.jpg')
    mixer.music.load('./asset/MHTV.mp3')
    mixer.music.play(-1) # phát nhạc lại vô hạn
    musicShot = mixer.Sound('./asset/shot.mp3') # tải âm thanh của đạn bắn
    soundHit = mixer.Sound('./asset/hit.mp3') # âm thanh của đạn bắn vào mục tiêu

    player_image = pygame.image.load('./asset/icons8-launch-64.png')
    enemy_image = pygame.image.load('./asset/enemigo.png')
    bullet_image = pygame.image.load('./asset/icons8-bullet-32.png')

    x = (1000/2)-64 # tọa độ ban đầu của người chơi được tính theo công thức
    y = 500
    x_change = 0 # tốc độ di chuyển theo trục x của người chơi
    y_change = 0 # tốc độ di chuyển theo trục y của người chơi

    x_enemy = [random.randint(0, 1000-64) for _ in range(20)]
    y_enemy = [random.randint(50, 200) for _ in range(20)]
    x_change_enemy = [0.7 for _ in range(20)] # tốc độ di chuyển của kẻ địch trong trục x
    y_change_enemy = [50 for _ in range(20)]


    points = 0
    font = pygame.font.Font(pygame.font.get_default_font(), 40)
    gameOverFont = pygame.font.Font(pygame.font.get_default_font(), 80)
    end = False
    bullet_visible = False
    x_bullet = 0   # vị trí ban đầu của viên đạn trên màn hình 
    y_bullet = 500
    x_change_bullet = 0 # vị trí viên đạn trên trục x sẽ không thay đổi
    y_change_bullet = 2 # vị trí của viên đạn trên màn hình trong mỗi vòng lặp của trò chơi ( vận tốc di chuyển )
    running = True

    while running:
        screen.blit(background, (0,0)) # cài đặt lại trò chơi khi màn hình kết thúc
        
        for event in pygame.event.get(): # xử lý các sự kiện của người chơi ( nút trên bàn phím)
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change-= 1
                if event.key == pygame.K_RIGHT:
                    x_change+= 1
                if event.key == pygame.K_UP:
                    y_change-= 1
                if event.key == pygame.K_DOWN:
                    y_change+= 1
                if event.key == pygame.K_SPACE: # nhấm space để bắn đạn, khi nhấn space thì nhạc của viên đạn bắn sẽ được phát
                    musicShot.play()
                    x_bullet = x # viên đạn sẽ được bắn từ vị trí của nhân vật 
                    y_bullet = y # vị trí ban đầu của viên đạn
                    bullet_visible = bulletShot(bullet_image, screen, bullet_visible, x_bullet, y_bullet) # hình ảnh viên đạn, màn hình trò chơi, bullet_visible: xác định viên đạn có hiển thị lên màn hình hay không, viên đạn được vẽ lên ở vị trí nào  
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        
        x += x_change # cho phép nhân vật di chuyển theo hướng của người chơi 
        y += y_change
                    
        if x <= 0: # nếu nhân vật vượt qua màn hình bên trái, vị trí sẽ được đặt lại bằng 0
            x = 0
        if x >= (1000-64): # nếu nhân vật vượt qua màn hình bên phải
            x = (1000-64)
        if y <= 0:
            y = 0
        if y >= 536:
            y = 536
            
        for e in range(20):
            if isColitionShip_Enemy(x, x_enemy[e], y, y_enemy[e]):
                for k in range(20): # vòng lặp được thực hiện để tiêu diệt máy bay 
                    y_enemy[k] = 1000
                end = True
                break
                     
            x_enemy[e] += x_change_enemy[e] # cập nhật vị trí của tàu, cho phép tàu dy chuyển dựa theo lập trình trước
                    
            if x_enemy[e] <= 0: # nếu tàu vượt qua bên trái thì hướng di chuyển của nó sẽ là 0,7
                x_change_enemy[e] = 0.7
                y_enemy[e] += y_change_enemy[e]
            if x_enemy[e] >= (1000-64):
                x_change_enemy[e] = -0.7    
                y_enemy[e] += y_change_enemy[e]
            
            colition = isColition(x_bullet, x_enemy[e], y_bullet, y_enemy[e])
        
            if colition:
                soundHit.play() # báo hiệu va chạm viên đạn và tàu địch
                y_bullet = 500 # đặt lại vị trí viên đạn cho lần bắn tiếp theo
                x_bullet = 0 # đặt lại vị trí viên đạn cho lần bắn mới 
                bullet_visible = False # ẩn viên đạn
                points += 1
                x_enemy[e] = 1000 # đặt vị trí tàu địch ra khỏi màn hình ( làm cho nó biến mất)
                y_enemy[e] = 1000
                break
                
            
        if sum(x_enemy) >= 20 * 1000:
            printGameOver(gameOverFont, screen)
            musicShot.stop()
            mixer.music.stop()
        
        if y_bullet <= 64:
            y_bullet = 500
            bullet_visible = False
            
        if bullet_visible and not end: #Kiểm tra xem viên đạn có đang hiển thị trên màn hình và trò chơi có đang chạy không
            bullet_visible = bulletShot(bullet_image, screen, bullet_visible, x_bullet, y_bullet)
            y_bullet -= y_change_bullet
        
        elif end:
            printGameOver(gameOverFont, screen)
            musicShot.stop()
            mixer.music.stop()
        
        player_func(player_image, x, y, screen)
        
        printPoint(font, points, screen)

        for e in range(20):
            enemy_func(enemy_image, x_enemy[e], y_enemy[e], screen)
                
        pygame.display.update()

    # Hiển thị thông báo chơi lại
    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Người chơi nhấn Enter để chơi lại
                    running = True
                    points = 0  # Reset điểm số khi chơi lại
                    main()

        screen.fill((0, 0, 0))
        text = gameOverFont.render('Press Enter to play again', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (1024 // 2, 600 // 2)
        screen.blit(text, textRect)
        pygame.display.update()

if __name__ == "__main__":
    main()