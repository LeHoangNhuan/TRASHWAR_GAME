# %%
import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

# Kích thước cửa sổ
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TRASHWAR")

# Tải hình ảnh nền và điều chỉnh kích thước
background_image = pygame.image.load("VỤ TRỤ.png")
background_image = pygame.transform.scale(background_image, (width, height))
start_screen_image = pygame.image.load("VNE-NASA-9751-1556939984.jpg")
start_screen_image = pygame.transform.scale(start_screen_image, (width, height))
# Màu sắc
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
light_sea_blue = (32,178,170)

# Tải hình ảnh robot và điều chỉnh kích thước
player_image = pygame.image.load("robot.png")
player_image = pygame.transform.scale(player_image, (150,150))

# Tải hình ảnh garbagemonster và điều chỉnh kích thước
garbagemonster_image = pygame.image.load("garbagemonster.png")
garbagemonster_image = pygame.transform.scale(garbagemonster_image, (100, 100))

# Tải hình túi rác và điều chỉnh kích thước
egg_image = pygame.image.load("garbagebag.png")
egg_image = pygame.transform.scale(egg_image, (40, 40))

# Tải hình ảnh vụ nổ và điều chỉnh kích thước
explode_image = pygame.image.load("boom.png")
explode_image = pygame.transform.scale(explode_image, (50, 50))

# Tải hình ảnh viên đạn (laser)
bullet_image = pygame.image.load("laser.png")
bullet_image = pygame.transform.scale(bullet_image, (15, 25))
# Tốc độ mặc định ban đầu
garbagemonster_speed = 2
eggs_speed = 1
player_speed = 5
bullet_speed = 5

# Biến theo dõi level
current_level = 1
level_threshold = 10  # Số điểm cần đạt để tăng level

# Biến thông báo khi level thay đổi
show_level_up_message = False
level_up_timer = 0
level_up_duration = 60  # Thời gian hiển thị thông báo (tính bằng frame, ví dụ: 60 frame ~ 1 giây)

# Tải âm thanh
pygame.mixer.music.load("game_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")
intro_sound = pygame.mixer.Sound("game_intro.mp3")
# Biến trạng thái game over
game_over_flag = False
# Vị trí và tốc độ robot
player_width, player_height = 50, 50
player_x = width // 2 - 70
player_y = height - 150

# Danh sách đạn và tốc độ
bullets = []
bullet_cooldown = 0  # Khởi tạo thời gian cooldown

# Kích thước và tốc độ garbagemonster
garbagemonster_width, garbagemonster_height = 50, 50

# Kích thước và tốc độ trứng
eggs_width, eggs_height = 30, 30
eggs = []
eggs_spawn_timer = 60

# Biến điểm số
score = 0
font = pygame.font.SysFont(None, 30)

# Đồng hồ điều chỉnh FPS
clock = pygame.time.Clock()

# Thời gian nổ
explode_duration = 30

# Tạo font chữ
font_normal = pygame.font.SysFont(None,50)
font_large = pygame.font.SysFont(None,90)  # Font chữ lớn 

# Biến trạng thái nổ của robot
player_exploded = False
player_explode_timer = 30


# Hàm hiển thị điểm số
def display_score(score):
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, 10))
# Hàm tăng độ khó
def increase_difficulty(score):
    global current_level, garbagemonster_speed, eggs_speed
    global show_level_up_message, level_up_timer
    if score >= current_level * level_threshold:
        current_level += 1
        garbagemonster_speed += 1  # Tăng tốc độ garbagemonster
        eggs_speed += 0.5           # Tăng tốc độ trứng
        # Hiển thị thông báo level up
        show_level_up_message = True
        level_up_timer = level_up_duration

# Hàm kết thúc trò chơi
def game_over():
    global game_over_flag
    game_over_flag = True

# Tạo hàng garbagemonster
def create_garbagemonster():
    return {
        'x': random.randint(0, width - garbagemonster_width),
        'y': 0,
        'speed_x': random.choice([-1, 1]) * garbagemonster_speed,
        'speed_y': 0,
        'egg_spawn_timer': random.randint(60, 120),
        'exploded': False,
        'explode_timer': explode_duration
    }

# Danh sách garbagemonster
garbagemonster_row = [create_garbagemonster() for _ in range(4)]
# Hàm hiển thị màn hình bắt đầu
font_title = pygame.font.Font("PressStart2P-Regular.ttf", 50)  # Font lớn cho tiêu đề
font_instruction = pygame.font.Font("PressStart2P-Regular.ttf", 20)  # Font nhỏ hơn cho hướng dẫn
def show_start_screen():
    pygame.mixer.music.stop() #Dừng nhạc nền hiện tại
    intro_sound.play(-1) # Bắt đầu intro (lặp vô hạn)
    screen.blit(start_screen_image ,(0,0))
    title_text = font_title.render("TRASH WAR", True, white)
    start_text = font_instruction.render("Press any key to start", True, white)
    screen.blit(title_text, (width // 2 - 240, height // 2 - 50))
    screen.blit(start_text, (width // 2 - 240, height // 2 + 20))
    
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
                intro_sound.stop() #Dừng intro ngay khi người chơi bắt đầu game
                pygame.mixer.music.play(-1)  # Bắt đầu nhạc nền (lặp vô hạn)
# Gọi hàm màn hình bắt đầu
show_start_screen()

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Gọi hàm tăng độ khó
    increase_difficulty(score)
    

    # logic đạn
    if bullet_cooldown > 0:
        bullet_cooldown -= 1
    # Xử lý phím bấm khi robot chưa phát nổ
    keys = pygame.key.get_pressed()
    if not player_exploded:
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < height - player_height:
            player_y += player_speed
        if keys[pygame.K_SPACE] and bullet_cooldown == 0:
            bullets.append({'x': player_x + player_width // 2+75, 'y': player_y, 'image': bullet_image})
            bullets.append({'x': player_x + player_width // 2+18, 'y': player_y, 'image': bullet_image})
            bullet_cooldown = 15

    # Di chuyển đạn
    for bullet in bullets:
        bullet['y'] -= 5
        if bullet['y'] < 0:
            bullets.remove(bullet)

    # Di chuyển garbagemonster
    for garbagemonster in garbagemonster_row:
        if not garbagemonster['exploded']:
            garbagemonster['x'] += garbagemonster['speed_x']
            garbagemonster['y'] += garbagemonster['speed_y']

            if garbagemonster['x'] <= 0 or garbagemonster['x'] >= width - garbagemonster_width:
                garbagemonster['speed_x'] *= -1
                garbagemonster['y'] += garbagemonster_height

            garbagemonster['egg_spawn_timer'] -= 1
            if garbagemonster['egg_spawn_timer'] <= 0:
                eggs.append({'x': garbagemonster['x'] + garbagemonster_width // 2 - eggs_width // 2, 'y': garbagemonster['y'] + garbagemonster_height})
                garbagemonster['egg_spawn_timer'] = random.randint(60, 120)

            # Kiểm tra va chạm giữa robot và garbagemonster
            if (
                player_x < garbagemonster['x'] + garbagemonster_width and
                player_x + player_width > garbagemonster['x'] and
                player_y < garbagemonster['y'] + garbagemonster_height and
                player_y + player_height > garbagemonster['y']
            ):
                player_exploded = True

            # Kiểm tra va chạm giữa đạn và garbagemonster
            for bullet in bullets:
                if (
                    garbagemonster['x'] < bullet['x'] < garbagemonster['x'] + garbagemonster_width and
                    garbagemonster['y'] < bullet['y'] < garbagemonster['y'] + garbagemonster_height
                ):
                    bullets.remove(bullet)
                    garbagemonster['exploded'] = True
                    garbagemonster['explode_timer'] = explode_duration
                    score += 1

    for egg in eggs:
        egg['y'] += eggs_speed

        # Kiểm tra va chạm giữa robot và trứng
        if (
            player_x < egg['x'] < player_x + player_width and
            player_y < egg['y'] < player_y + player_height
        ):
            player_exploded = True
            eggs.remove(egg)  # Loại bỏ quả trứng đã gây nổ

    # Vẽ nền
    screen.blit(background_image, (0, 0))
    # Hiển thị thông báo "Update Level" nếu cần
    if show_level_up_message:
        level_up_text = font_large.render("UPDATE LEVEL!", True, white)
        screen.blit(level_up_text, (width // 2 - level_up_text.get_width() // 2, height // 2 - 50))
        level_up_timer -= 1
        if level_up_timer <= 0:
            show_level_up_message = False

    # Hiển thị robot hoặc vụ nổ nếu robot va chạm
    if player_exploded:
        screen.blit(explode_image, (player_x, player_y))
        player_explode_timer -= 1
        if player_explode_timer <= 0:
            game_over()
    else:
        screen.blit(player_image, (player_x, player_y))

    # Hiển thị garbagemonster hoặc vụ nổ khi garbagemonster bị bắn
    for garbagemonster in garbagemonster_row:
        if garbagemonster['exploded']:
            if garbagemonster['explode_timer'] > 0:
                screen.blit(explode_image, (garbagemonster['x'], garbagemonster['y']))
                garbagemonster['explode_timer'] -= 1
            else:
                # Hồi sinh garbagemonster ở vị trí mới
                garbagemonster_row[garbagemonster_row.index(garbagemonster)] = create_garbagemonster()
        else:
            screen.blit(garbagemonster_image, (garbagemonster['x'], garbagemonster['y']))

    # Vẽ đạn
    for bullet in bullets:
        screen.blit(bullet['image'], (bullet['x'], bullet['y']))

    # Vẽ trứng
    for egg in eggs:
        screen.blit(egg_image, (egg['x'], egg['y']))

    # Hiển thị điểm số
    display_score(score)

    # Hiển thị màn hình Game Over
    font_large = pygame.font.Font("PressStart2P-Regular.ttf", 30)  
    font_normal = pygame.font.Font("PressStart2P-Regular.ttf", 30)
    # DDừng nhạc nền
    
    if game_over_flag:
        pygame.mixer.music.stop()
        game_over_sound.play()
    # Vẽ nền đen
        screen.blit(background_image, (0, 0))

    # Hiển thị chữ "Game" với font lớn
        game_over_text1 = font_title.render("GAME", True, white)
        screen.blit(game_over_text1, (width // 2 - 200, height // 2 - 100))

    # Hiển thị chữ "Over" với font bình thường
        game_over_text2 = font_title.render("OVER", True, white)
        screen.blit(game_over_text2, (width // 2+20, height // 2 - 100))
    # Hiển thị điểm số
        score_text = font_normal.render("Score:" + str(score), True, white)
        screen.blit(score_text, (width//2-100,height//2-40))

    # Hiển thị văn bản Play again
        Playagain_text = font_normal.render("Play again?", True, light_sea_blue)
        screen.blit(Playagain_text, (width // 2 - 150, height // 2 ))

    # Hiển thị nút Yes
        yes_text = font_normal.render("Yes", True, white)
        screen.blit(yes_text, (width // 2 - 120, height // 2+50))

    # Hiển thị nút No
        no_text = font_normal.render("No", True, white)
        screen.blit(no_text, (width // 2 + 60, height // 2+50))

    # Kiểm tra sự kiện click chuột
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

        # Tọa độ của chữ "Yes"
            yes_x = width // 2 - 110
            yes_y = height // 2 + 45
            yes_text.get_width()
            yes_width = yes_text.get_width()
            yes_height = yes_text.get_height()

        # Tọa độ của chữ "No"
            no_x = width // 2 + 55
            no_y = height // 2 + 45
            no_width = no_text.get_width()
            no_height = no_text.get_height()

        # Kiểm tra nếu click vào "Yes"
            if yes_x <= mouse_pos[0] <= yes_x + yes_width and yes_y <= mouse_pos[1] <= yes_y + yes_height:
            # Reset game
                player_exploded = False
                player_explode_timer = 30
                game_over_flag = False
                score = 0
                bullets.clear()
                eggs.clear()
                player_x = width // 2 - 25  # Đặt lại vị trí robot
                player_y = height - 150
                garbagemonster_row = [create_garbagemonster() for _ in range(4)]  # Tạo lại danh sách garbagemonster

                pygame.mixer.music.stop()
                pygame.mixer.music.play(-1)  # Phát nhạc nền (lặp vô hạn)

        # Kiểm tra nếu click vào "No"
            elif no_x <= mouse_pos[0] <= no_x + no_width and no_y <= mouse_pos[1] <= no_y + no_height:
                pygame.quit()
                sys.exit()

    # Cập nhật màn hình
    pygame.display.flip()

    # Giới hạn FPS
    clock.tick(60)


