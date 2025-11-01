import pygame
pygame.init()

# --- Налаштування ---
width, height = 800, 600
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping-Pong до 15 очок")
clock = pygame.time.Clock()

# --- Об’єкти ---
ball = pygame.Rect(width // 2 - 10, height // 2 - 10, 20, 20)
ball_speed = [4, 4]

left_paddle = pygame.Rect(30, height // 2 - 40, 10, 80)
right_paddle = pygame.Rect(width - 40, height // 2 - 40, 10, 80)
speed_paddle = 5

left_score = 0
right_score = 0
font = pygame.font.Font(None, 60)
game_over = False

# --- Звуки ---
pygame.mixer.init()
try:
    hit_sound = pygame.mixer.Sound("tennis-ball-hit-386155.mp3")
except:
    hit_sound = None
try:
    pygame.mixer.music.load("winning-elevation-111355 (1).mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
except:
    print("⚠️ Файл музики не знайдено.")

# --- Функції ---
def reset_ball(direction):
    ball.center = (width // 2, height // 2)
    ball_speed[0] = 4 * direction
    ball_speed[1] = 4

# --- Основний цикл ---
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            left_score = right_score = 0
            game_over = False
            reset_ball(1)

    keys = pygame.key.get_pressed()
    if not game_over:
        # --- Керування ---
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= speed_paddle
        if keys[pygame.K_s] and left_paddle.bottom < height:
            left_paddle.y += speed_paddle
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= speed_paddle
        if keys[pygame.K_DOWN] and right_paddle.bottom < height:
            right_paddle.y += speed_paddle

        # --- Рух м’яча ---
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # --- Відбивання від верхнього та нижнього краю ---
        if ball.top <= 0 or ball.bottom >= height:
            ball_speed[1] = -ball_speed[1]
            if hit_sound:
                hit_sound.play()

        # --- Відбивання від ракеток ---
        if ball.colliderect(left_paddle):
            ball_speed[0] = abs(ball_speed[0])
            if hit_sound:
                hit_sound.play()

        if ball.colliderect(right_paddle):
            ball_speed[0] = -abs(ball_speed[0])
            if hit_sound:
                hit_sound.play()

        # --- Перевірка на гол ---
        if ball.left <= 0:
            right_score += 1
            reset_ball(1)
        if ball.right >= width:
            left_score += 1
            reset_ball(-1)

        # --- Перевірка перемоги ---
        if left_score == 15 or right_score == 15:
            game_over = True

    # --- Малювання ---
    screen.fill(black)
    pygame.draw.rect(screen, white, (0, 0, width, 40))          # Верхня межа
    pygame.draw.rect(screen, white, (0, height - 20, width, 20)) # Нижня межа
    pygame.draw.line(screen, white, (width // 2, 0), (width // 2, height), 1)

    pygame.draw.rect(screen, blue, left_paddle, border_radius=5)
    pygame.draw.rect(screen, red, right_paddle, border_radius=5)
    pygame.draw.ellipse(screen, white, ball)

    # --- Рахунок ---
    score_text = font.render(f"{left_score} : {right_score}", True, black)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 5))

    # --- Повідомлення про перемогу ---
    if game_over:
        winner = "Лівий" if left_score == 15 else "Правий"
        msg = font.render(f"Переміг {winner} гравець!", True, white)
        tip = pygame.font.Font(None, 40).render("Натисни Enter, щоб почати знову", True, white)
        screen.blit(msg, (width // 2 - msg.get_width() // 2, height // 2 - 40))
        screen.blit(tip, (width // 2 - tip.get_width() // 2, height // 2 + 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()