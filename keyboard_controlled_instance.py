import pygame
import math

# 초기화
pygame.init()

# 디스플레이 정보 가져오기
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D 슈팅 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # 플레이어 색상
GREEN = (0, 255, 0)  # 직선 색상
BLUE = (0, 0, 255)  # 벽 색상

# 플레이어 클래스
class Player:
    def __init__(self, x, y, radius, speed, collision_manager):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = 0
        self.collision_manager = collision_manager  # 충돌 관리 객체

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)
        # 플레이어 방향에 직선 그리기
        line_length = 100
        line_end_x = self.x + line_length * math.cos(math.radians(-self.angle))
        line_end_y = self.y - line_length * math.sin(math.radians(-self.angle))
        pygame.draw.line(surface, GREEN, (int(self.x), int(self.y)), (int(line_end_x), int(line_end_y)), 2)

    def move(self, keys):
        dx = dy = 0
        if keys[pygame.K_UP]:
            dx = self.speed * math.cos(math.radians(-self.angle))
            dy = self.speed * math.sin(math.radians(-self.angle))
        if keys[pygame.K_DOWN]:
            dx = -self.speed * math.cos(math.radians(-self.angle))
            dy = -self.speed * math.sin(math.radians(-self.angle))

        # 이동 후의 잠재적인 새 위치
        new_x = self.x + dx
        new_y = self.y - dy  # Y축 반전
        new_rect = pygame.Rect(new_x - self.radius, new_y - self.radius, 2 * self.radius, 2 * self.radius)

        # 새로운 위치가 벽과 충돌하지 않는 경우에만 위치 업데이트
        if not self.collision_manager.check_collision(new_rect):
            self.x, self.y = new_x, new_y

    def rotate(self, direction):
        self.angle += direction

    def shoot(self):
        return Bullet(self.x, self.y, self.angle)

# 총알 클래스
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 5
        self.speed = 7
        self.angle = angle
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.dx = self.speed * math.cos(math.radians(-self.angle))
        self.dy = self.speed * math.sin(math.radians(-self.angle))

    def update(self):
        self.rect.x += self.dx
        self.rect.y -= self.dy  # Y축 반전

    def draw(self, surface):
        draw_rotated_bullet(surface, RED, self.rect.center, self.width, self.height, self.angle)

# 벽을 관리하는 Map 클래스
class Map:
    def __init__(self, walls):
        self.walls = walls
    
    def draw(self, surface):
        for wall in self.walls:
            pygame.draw.rect(surface, BLUE, wall)
    
    def get_walls(self):
        return self.walls

# 충돌 관리 클래스
class CollisionManager:
    def __init__(self, game_map):
        self.game_map = game_map

    def check_collision(self, rect):
        return any(rect.colliderect(wall) for wall in self.game_map.get_walls())

    def check_player_collision(self, player):
        player_rect = pygame.Rect(player.x - player.radius, player.y - player.radius, 2 * player.radius, 2 * player.radius)
        return self.check_collision(player_rect)
    
    def check_bullet_collision(self, bullet):
        return self.check_collision(bullet.rect)

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

# 벽 배열 설정
wall_size = 50
walls = [
    pygame.Rect(100, 100, wall_size, wall_size),
    pygame.Rect(200, 150, wall_size, wall_size),
    pygame.Rect(300, 200, wall_size, wall_size),
    pygame.Rect(400, 250, wall_size, wall_size),
    pygame.Rect(500, 300, wall_size, wall_size),
]
game_map = Map(walls)
collision_manager = CollisionManager(game_map)

# 플레이어와 맵 초기화
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 30, 5, collision_manager)

# 총알 리스트와 쿨다운 설정
bullets = []
fire_rate = 500  # 총알 발사 쿨다운 시간 (밀리초 단위)
last_fire_time = pygame.time.get_ticks()

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # 회전 설정
    if keys[pygame.K_LEFT]:
        player.rotate(5)
    if keys[pygame.K_RIGHT]:
        player.rotate(-5)

    # 이동 설정
    player.move(keys)

    # 총알 발사
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and current_time - last_fire_time >= fire_rate:
        bullets.append(player.shoot())
        last_fire_time = current_time

    # 총알 이동 및 충돌 검사
    for i in range(len(bullets) - 1, -1, -1):
        bullet = bullets[i]
        bullet.update()
        if (bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH or 
            bullet.rect.y < 0 or bullet.rect.y > SCREEN_HEIGHT or 
            collision_manager.check_bullet_collision(bullet)):
            bullets.pop(i)

    # 화면 업데이트
    screen.fill(BLACK)

    # 맵 그리기
    game_map.draw(screen)

    # 플레이어 그리기
    player.draw(screen)

    # 총알 그리기
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
