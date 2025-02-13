import pygame

WIDTH, HEIGHT = 700, 800

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MineSweeper")

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                event.__reduce_ex__()

if __name__ == "__main__":
    main()