import pygame
pygame.init()
import json

width = 600 #800 in code
height = 600 #800 in code
tile_size = 30 #40 in code
clock=pygame.time.Clock()
fps=60
game_over = 0
lives = 3

display=pygame.display.set_mode((width,height))
pygame.display.set_caption("Project1")
sprite_image=pygame.image.load('Images/player1.png')
sprite_rect=sprite_image.get_rect()
bg_image=pygame.image.load('Images/bg2.png')
bg_rect=bg_image.get_rect()

with open("Levels/level1.json", "r") as file:
    world_data = json.load(file)

level = 1
max_level = 4
def reset_level():
    player.rect.x = 95
    player.rect.y = height - 130
    lava_group.empty()
    exit_group.empty()
    with open(f"Levels/level{level}.json", "r") as file:
        world_data = json.load(file)
    world = World(world_data)
    return world

class Player:
    def __init__(self):
        self.image = pygame.image.load("Images/player1.png")
        self.image = pygame.transform.scale(self.image, (24,28))
        self.rect = self.image.get_rect()
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        self.is_ghost = False
        self.ghost_image = pygame.image.load("Images/ghost.png")
        self.ghost_image = pygame.transform.scale(self.ghost_image, (29, 24))
        for num in range (1,3):
            img_right = pygame.image.load(f"Images/player{num}.png")
            img_right = pygame.transform.scale(img_right, (24,28))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
            self.image = self.images_right[self.index]
        self.rect.x = 95
        self.rect.y = height-130
        self.gravity = 0
        self.jumped = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    def update(self):
        global game_over
        global lives
        x = 0
        y = 0
        animation_speed = 10 #walk_speed in lesson

        if game_over == 0:
            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE] or key[pygame.K_i] and self.jumped==False:
                self.gravity=-12
                self.jumped=True
            if key[pygame.K_LEFT] or key[pygame.K_j]:
                x -= 4
                self.direction = -1
                self.counter += 1
            if key[pygame.K_l] or key[pygame.K_RIGHT]:
                x = 4
                self.direction = 1
                self.counter +=1

            if self.counter > animation_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                else:
                    self.image = self.images_left[self.index]
            self.gravity += 1
            if self.gravity > 15:
                self.gravity = 15
            y += self.gravity
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x+x, self.rect.y, self.width, self.height):
                    x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y, self.width, self.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity > 0:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False
            if self.rect.bottom > height:
                self.rect.bottom = height
                self.jumped = False
            self.rect.x += x
            self.rect.y += y
            if pygame.sprite.spritecollide(self,lava_group, False):
                game_over = -1
                self.is_ghost = True
                self.image = self.ghost_image
                lives -= 1
                print(lives)
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
        elif game_over == -1 and self.is_ghost:
            self.rect.y -= 1
            if self.rect.y <= -50:
                player.rect.x = 95
                player.rect.y = height - 130
                game_over = 0
        display.blit(self.image, self.rect)
class World:
    def __init__(self,data):
        dirt_img1 = pygame.image.load("Images/1dirt.png")
        grass_img2 = pygame.image.load("Images/2grass.png")
        swamp_img3 = pygame.image.load("Images/3water.png")
        sand_img4 = pygame.image.load("Images/4sand.png")
        diamond_img6 = pygame.image.load("Images/6diamond.png")

        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2 or tile == 3 or tile == 4 or tile == 6:
                    images = {1:dirt_img1, 2:grass_img2, 3:swamp_img3, 4:sand_img4, 6:diamond_img6}
                    img = pygame.transform.scale(images[tile],(tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 7:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    exit_ = Exit(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    exit_group.add(exit_)
                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            display.blit(tile[0], tile[1])
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("Images/7lava.png")
        self.image = pygame.transform.scale(img,
                                            (tile_size,tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Button:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center=(x, y))
    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image, self.rect)
        return action
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("Images/5exit.png")
        self.image = pygame.transform.scale(img,(tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 30 #find a general formula for this(correlating to height in 166)

exit_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
world = World(world_data)
player = Player()
restart_btn = Button(width//2, height//2, "Images/restart_btn.png")
start_btn = Button(width//2 - 150, height//2, "Images/start_btn.png")
exit_btn = Button(width//2 + 150, height//2, "Images/exit_btn.png")

run = True
main_menu = True
while run:
    clock.tick(fps)
    display.blit(bg_image,bg_rect)
    if main_menu:
        if start_btn.draw():
            main_menu = False
            level = 1
            world = reset_level()
        if exit_btn.draw():
            run = False
    else:
        world.draw()
        lava_group.draw(display)
        exit_group.draw(display)
        player.update()
        lava_group.update()

        if game_over == -1:
            if restart_btn.draw():
                player = Player()
                #world = World(world_data)
                world = reset_level()
                game_over = 0
        if game_over == 1:
            game_over = 0
            if level < max_level:
                level += 1
                world = reset_level()
            else:
                print("Finish")
                main_menu = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if lives == 0:
        main_menu = True
        lives = 3
    pygame.display.update()
pygame.quit()