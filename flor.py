import pygame
import math
import random
import sys

pygame.init()
WIDTH, HEIGHT = 700, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ramo de Girasoles 🌻")
clock = pygame.time.Clock()
FPS = 60

# Colores
NAVY = (10, 25, 50)
STEM = (40, 115, 60)
YELLOW = (255, 200, 0)
BROWN = (90, 50, 30)
RIBBON = (200, 0, 80)

GOLDEN_ANGLE = 2.3999632297  # espiral de semillas

# Fuente
pygame.font.init()
font = pygame.font.SysFont("Arial", 36, bold=True)

class Sunflower:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.target_size = size
        self.size = 1
        self.growth_speed = 0.5

    def update(self):
        if self.size < self.target_size:
            self.size += self.growth_speed

    def draw(self, surf):
        center_r = int(self.size * 0.35)
        petal_len = int(self.size * 1.1)
        petal_w = int(self.size * 0.45)

        # pétalos
        for i in range(24):
            angle = (2*math.pi/24)*i
            dx, dy = math.cos(angle), math.sin(angle)
            px = self.x + dx * (center_r + petal_len*0.3)
            py = self.y + dy * (center_r + petal_len*0.3)
            petal = pygame.Surface((petal_len, petal_w), pygame.SRCALPHA)
            pygame.draw.ellipse(petal, YELLOW, (0, 0, petal_len, petal_w))
            rot = pygame.transform.rotate(petal, -math.degrees(angle))
            rect = rot.get_rect(center=(px, py))
            surf.blit(rot, rect)

        # centro
        pygame.draw.circle(surf, BROWN, (self.x, self.y), center_r)
        for k in range(40):
            r = center_r * math.sqrt(k/40) * 0.85
            theta = k*GOLDEN_ANGLE
            sx = int(self.x + r*math.cos(theta))
            sy = int(self.y + r*math.sin(theta))
            pygame.draw.circle(surf, (60, 30, 20), (sx, sy), 2)

# Generar ramo con centro
def create_bouquet():
    flowers = []
    center_x, center_y = WIDTH//2, HEIGHT//2 - 150  # girasol central bajado un poco

    # girasol central (un poco más grande)
    flowers.append(Sunflower(center_x, center_y, 70))

    # girasoles alrededor
    for i in range(6):
        angle = i * (2*math.pi/6)
        r = random.randint(100, 130)
        x = center_x + int(r*math.cos(angle))
        y = (HEIGHT//2 - 100) + int(r*math.sin(angle)) - 40
        size = random.randint(45, 55)
        flowers.append(Sunflower(x, y, size))

    return flowers

flowers = create_bouquet()

def draw_stems_and_ribbon(surf):
    base_x, base_y = WIDTH//2, HEIGHT//2 + 100

    # tallos desde cada flor hasta el lazo
    for f in flowers:
        pygame.draw.line(surf, STEM, (f.x, f.y+20), (base_x, base_y), 6)

    # lazo
    pygame.draw.circle(surf, RIBBON, (base_x, base_y), 22)
    pygame.draw.ellipse(surf, RIBBON, (base_x-35, base_y-12, 35, 25))
    pygame.draw.ellipse(surf, RIBBON, (base_x, base_y-12, 35, 25))

    # tallo principal debajo del lazo
    pygame.draw.line(surf, STEM, (base_x, base_y), (base_x, base_y+100), 10)

def draw_text(surf):
    text = font.render("Para ti :3", True, YELLOW)  # texto en amarillo dorado
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT-120))
    surf.blit(text, text_rect)

# Loop principal
running = True
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(NAVY)

    # tallos y lazo
    draw_stems_and_ribbon(screen)

    # flores que crecen
    for f in flowers:
        f.update()
        f.draw(screen)

    # texto
    draw_text(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
