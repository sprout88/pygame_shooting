# player.py
import pygame
import math

# 기본 플레이어 클래스
class Player:
    def __init__(self, x, y, radius, speed, collision_manager):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = 0
        self.collision_manager = collision_manager

    def draw(self, surface):
        # 플레이어 원 그리기
        pygame.draw.circle(surface, pygame.Color('red'), (int(self.x), int(self.y)), self.radius)

        # 플레이어 앞에 직선 그리기
        line_length = 100  # 직선의 길이
        line_end_x = self.x + line_length * math.cos(math.radians(-self.angle))
        line_end_y = self.y - line_length * math.sin(math.radians(-self.angle))
        pygame.draw.line(surface, pygame.Color('green'), (int(self.x), int(self.y)), (int(line_end_x), int(line_end_y)), 2)

    def move(self, keys):
        dx = dy = 0
        if keys[pygame.K_UP]:
            dx = self.speed * math.cos(math.radians(-self.angle))
            dy = self.speed * math.sin(math.radians(-self.angle))
        if keys[pygame.K_DOWN]:
            dx = -self.speed * math.cos(math.radians(-self.angle))
            dy = -self.speed * math.sin(math.radians(-self.angle))

        new_x = self.x + dx
        new_y = self.y - dy  # Y축 반전
        new_rect = pygame.Rect(new_x - self.radius, new_y - self.radius, 2 * self.radius, 2 * self.radius)

        if not self.collision_manager.check_collision(new_rect):
            self.x, self.y = new_x, new_y

    def rotate(self, direction):
        self.angle += direction

    def shoot(self):
        return Bullet(self.x, self.y, self.angle)

# 빠른 플레이어 클래스
class FastPlayer(Player):
    def __init__(self, x, y, radius, collision_manager):
        super().__init__(x, y, radius, speed=10, collision_manager=collision_manager)

    def draw(self, surface):
        pygame.draw.circle(surface, pygame.Color('red'), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, pygame.Color('white'), (int(self.x), int(self.y)), self.radius, 3)
        # 플레이어 앞에 직선 그리기
        line_length = 100  # 직선의 길이
        line_end_x = self.x + line_length * math.cos(math.radians(-self.angle))
        line_end_y = self.y - line_length * math.sin(math.radians(-self.angle))
        pygame.draw.line(surface, pygame.Color('green'), (int(self.x), int(self.y)), (int(line_end_x), int(line_end_y)), 2)

# 무거운 플레이어 클래스
class HeavyPlayer(Player):
    def __init__(self, x, y, radius, collision_manager):
        super().__init__(x, y, radius, speed=3, collision_manager=collision_manager)

    def draw(self, surface):
        pygame.draw.circle(surface, pygame.Color('red'), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, pygame.Color('blue'), (int(self.x), int(self.y)), self.radius, 3)

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
        self.rect.y -= self.dy

    def draw(self, surface):
        draw_rotated_bullet(surface, pygame.Color('red'), self.rect.center, self.width, self.height, self.angle)

# 총알 그래픽 설정
def draw_rotated_bullet(surface, color, center, width, height, angle):
    bullet_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(bullet_surface, color, (0, 0, width, height))
    rotated_bullet = pygame.transform.rotate(bullet_surface, -angle)
    rotated_rect = rotated_bullet.get_rect(center=center)
    surface.blit(rotated_bullet, rotated_rect.topleft)
