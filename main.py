import pygame
import random
import os


pygame.init()

done = False
clock = pygame.time.Clock()


screen = pygame.display.set_mode((535, 454))
pygame.display.set_caption("Rotation Game")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def load_image(name):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname).convert()
    return image


img = load_image('bg.jpg')


window_width = img.get_rect().w
window_height = img.get_rect().h
sq_w = window_width // 5
sq_h = window_height // 4


class Pixel(pygame.sprite.Sprite):
    def __init__(self, image, coords):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.direction = 0
        for i in range(random.randrange(3)):
            self.update()

    def update(self):
        self.image = pygame.transform.rotate(self.image, -90)
        self.direction += 1
        if self.direction > 3:
            self.direction = 0


image_g = pygame.sprite.RenderPlain()


def generate_pixels(picture):
    global image_g
    for i in range(5):
        for j in range(4):
            x = i * sq_w
            y = j * sq_h
            part = pygame.Surface((sq_w, sq_h))
            part.blit(picture, (0, 0), (x, y, sq_w, sq_h))
            p = Pixel(part, [x, y])
            image_g.add(p)


generate_pixels(img)


def win():
    i = 0
    for p in image_g:
        if p.direction == 0:
            i += 1
        else:
            break
    if i == 16:
        return True
    else:
        return False


mouse_pos = [-1, -1]

# ---Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            for s in image_g:
                if s.rect.collidepoint(mouse_pos):
                    s.update()
            done = win()

    image_g.draw(screen)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
