import pygame
pygame.init()

width = 600
height = 600
clock=pygame.time.Clock()
fps=60

display=pygame.display.set_mode((width,height))
pygame.display.set_caption("Project1")
sprite_image=pygame.image.load('Images/player2.png')
sprite_rect=sprite_image.get_rect()
bg_image=pygame.image.load('Images/bg2.png')
bg_rect=bg_image.get_rect()

class Hero:
    def __init__(self,name):
        self.image = pygame.image.load("Images/player1.png")
        self.image = pygame.transform.scale(self.image, (60, 70))
        self.rect = self.image.get_rect()
        self.right_edge_touching = False
        self.left_edge_touching = True

    #def greet(self):
        #print("Yo, I'm"+self.name)
    def homework1(self):
        x = 0
        y = 0
        speed = 10
        x += speed

        if self.rect.right > width:
            self.right_edge_touching = True
            self.left_edge_touching = False
            print("touching right edge")
        elif self.rect.left < 0:
            self.left_edge_touching = True
            self.right_edge_touching = False
            print("touching left edge")

        if self.right_edge_touching == True and self.left_edge_touching == False:
            self.rect.x -= x
        if self.right_edge_touching == False and self.right_edge_touching == False:
            self.rect.x += x

        display.blit(self.image, self.rect)
class Car:
    def __init__(self,brand,model,year):
        self.image=pygame.image.load("Images/M4 comp.jpg")
        self.image = pygame.transform.scale(self.image, (141, 113))
        self.rect = self.image.get_rect()
        self.brand=brand
        self.model=model
        self.year=year
    def update(self):
        display.blit(self.image, self.rect)
    def display_info(self):
        print(f"Car info: {self.brand} {self.model}, {self.year}")

hero1=Hero("Steve")
hero2=Hero("Bob")
car1 = Car("BMW", "M4 competition", "2024")

car1.display_info()

#hero1.greet()

run=True
while run:
    clock.tick(fps)

    display.blit(bg_image,bg_rect)
    hero1.homework1()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()