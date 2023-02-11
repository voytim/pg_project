import os
import sys

import pygame

pygame.init()
pygame.font.init()
size = width, height = 500, 500
pygame.display.set_caption('Баскетбол')
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ring(pygame.sprite.Sprite):
    r_image = load_image("ring.png")
    image1 = pygame.transform.scale(r_image, (100, 100))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Ring.image1
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 160


class Ball(pygame.sprite.Sprite):
    b_image = load_image("ball.png")
    image1 = pygame.transform.scale(b_image, (50, 50))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Ball.image1
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 400
        self.vx = 0
        self.vy = 0
        self.acc = 100
        self.flying = False

    def check(self, r_x, r_y):
        if self.flying:
            dx = 10
            dy = 40
            state_1 = self.rect.x + 25 > r_x + dx and self.rect.x + 25 < r_x + 100 - dx
            state_2 = self.vy > 0
            state_3 = self.rect.y + 50 > r_y + dy and self.rect.y + 50 < r_y + 10 + dy
            if state_1 and state_2 and state_3:
                self.flying = False
                self.vx = 0
                self.vy = 0

    def start(self, mouse_pos):
        k = 1
        if not self.flying:
            self.vx = (mouse_pos[0] - self.rect.x - 25) * k
            self.vy = (mouse_pos[1] - self.rect.y - 25) * k
            self.flying = True
        else:
            self.vx = 0
            self.vy = 0
            self.rect = self.rect.move(50 - self.rect.x, 400 - self.rect.y)
            self.flying = False

    def update(self, fps):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if self.flying:
            dx = self.vx / fps
            dy = self.vy / fps
            self.rect = self.rect.move(dx, dy)
            self.vy += self.acc / fps
            self.vx -= (self.vx / fps / 100) ** 2


if __name__ == '__main__':
    clock = pygame.time.Clock()
    fps = 30
    all_sprites = pygame.sprite.Group()
    Border(1, 1, 1, height - 1)
    Border(width - 1.5, 1.5, width - 1.5, height - 1.5)
    Border(1.5, height - 1.5, width - 1.5, height - 1.5)
    Border(1, 1, width - 1, 1)

    Ring(all_sprites)
    ball = Ball(all_sprites)

    running = True
    while running:

        # pygame.draw.circle(screen, (255, 255, 255), (179, 147), 10, 2)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.start(event.pos)

        screen.fill(pygame.Color(255, 228, 196))
        # pygame.draw.circle(screen, (0, 0, 0), (179, 147), 5, 2)
        ball.update(fps)
        ball.check(400, 160)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
