import pygame
import math

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D 슈팅 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # 플레이어 색상
GREEN = (0, 255, 0)  # 직선 색상

# 플레이어 설정
player_radius = 30  # 플레이어 원의 반지름
player_speed = 5
player_angle = 0

# 총알 설정
bullet_width = 10
bullet_height = 5
bullet_speed = 7
bullets = []  # 총알과 방향을 저장할 리스트

# 쿨다운 설정
fire_rate = 500  # 총알 발사 쿨다운 시간 (밀리초 단위)
last_fire_time = pygame.time.get_ticks()

# 플레이어 초기 위치
player_centerx = SCREEN_WIDTH // 2
player_centery = SCREEN_HEIGHT // 2

# 총알 그래픽 설정
def draw_rotated_bullet(surface, color, center, width, height, angle):
    """회전된 총알을 그립니다."""
    bullet_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(bullet_surface, color, (0, 0, width, height))
    rotated_bullet = pygame.transform.rotate(bullet_surface, -angle)
    rotated_rect = rotated_bullet.get_rect(center=center)
    surface.blit(rotated_bullet, rotated_rect.topleft)

# 게임 루프 변수
running = True
clock = pygame.time.Clock()

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # 현재 시간
    current_time = pygame.time.get_ticks()

    # 회전 설정
    if keys[pygame.K_LEFT]:
        player_angle += 5
    if keys[pygame.K_RIGHT]:
        player_angle -= 5

    # 이동 설정
    if keys[pygame.K_UP]:
        dx = player_speed * math.cos(math.radians(-player_angle))
        dy = player_speed * math.sin(math.radians(-player_angle))
        player_centerx += dx
        player_centery -= dy  # Y축 반전

    if keys[pygame.K_DOWN]:
        dx = -player_speed * math.cos(math.radians(-player_angle))
        dy = -player_speed * math.sin(math.radians(-player_angle))
        player_centerx += dx
        player_centery -= dy  # Y축 반전

    # 총알 발사
    if keys[pygame.K_SPACE]:
        if current_time - last_fire_time >= fire_rate:
            bullet_dx = bullet_speed * math.cos(math.radians(-player_angle))
            bullet_dy = bullet_speed * math.sin(math.radians(-player_angle))
            bullet_rect = pygame.Rect(player_centerx - bullet_width // 2, player_centery - bullet_height // 2, bullet_width, bullet_height)
            bullets.append((bullet_rect, (bullet_dx, bullet_dy), player_angle))
            last_fire_time = current_time  # 마지막 발사 시간 업데이트

    # 총알 이동
    for i in range(len(bullets) - 1, -1, -1):
        bullet_rect, (bullet_dx, bullet_dy), bullet_angle = bullets[i]
        bullet_rect.x += bullet_dx
        bullet_rect.y -= bullet_dy  # Y축 반전
        if (bullet_rect.x < 0 or bullet_rect.x > SCREEN_WIDTH or bullet_rect.y < 0 or bullet_rect.y > SCREEN_HEIGHT):
            bullets.pop(i)

    # 화면 업데이트
    screen.fill(BLACK)

    # 플레이어 원 그리기
    pygame.draw.circle(screen, RED, (int(player_centerx), int(player_centery)), player_radius)

    # 플레이어 방향에 직선 그리기
    line_length = 100  # 직선의 길이
    line_end_x = player_centerx + line_length * math.cos(math.radians(-player_angle))
    line_end_y = player_centery - line_length * math.sin(math.radians(-player_angle))
    pygame.draw.line(screen, GREEN, (int(player_centerx), int(player_centery)), (int(line_end_x), int(line_end_y)), 2)

    # 총알 그리기
    for bullet_rect, _, bullet_angle in bullets:
        draw_rotated_bullet(screen, RED, bullet_rect.center, bullet_width, bullet_height, bullet_angle)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
