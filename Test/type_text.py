import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((300, 100))
base_font = pygame.font.Font(None, 20)
text = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            text = event.dict.get("unicode", "")
