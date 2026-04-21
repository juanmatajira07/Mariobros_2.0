import pygame
import sys
import math

# ---------------------------------------------------------
# 1. Configuración Inicial y Constantes
# ---------------------------------------------------------
pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

SKY_BLUE = (135, 206, 235)
MARIO_RED = (220, 20, 60)
GROUND_GREEN = (34, 139, 34)
COIN_GOLD = (255, 215, 0)
TEXT_BLACK = (0, 0, 0)
ALIEN_GREEN = (50, 205, 50)
LASER_RED = (255, 69, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario Clásico - Aventura Espacial")
clock = pygame.time.Clock()

# ---------------------------------------------------------
# 2. Clases del Juego
# ---------------------------------------------------------
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.6
        self.on_ground = False

    def move(self, dx, dy, platforms):
        self.rect.x += dx
        self.check_collision(dx, 0, platforms)
        
        self.rect.y += dy
        self.check_collision(0, dy, platforms)

    def check_collision(self, dx, dy, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                if dx < 0:
                    self.rect.left = platform.rect.right
                
                if dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                if dy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0                

    def update(self, platforms):
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15
            
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = self.jump_power
            
        self.move(self.vel_x, self.vel_y, platforms)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, surface):
        pygame.draw.rect(surface, MARIO_RED, self.rect)


class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        pygame.draw.rect(surface, GROUND_GREEN, self.rect)


class Goal:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        pygame.draw.rect(surface, COIN_GOLD, self.rect)


class Laser:
    def __init__(self, x, y, vel_x, vel_y):
        self.rect = pygame.Rect(x, y, 10, 10) 
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, surface):
        pygame.draw.rect(surface, LASER_RED, self.rect)


class Alien:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.shoot_cooldown = 0 

    def update(self, player_centerx, player_centery, lasers):
        if self.shoot_cooldown <= 0:
            dx = player_centerx - self.rect.centerx
            dy = player_centery - self.rect.centery
            angle = math.atan2(dy, dx)
            
            speed = 7 
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            lasers.append(Laser(self.rect.centerx, self.rect.centery, vel_x, vel_y))
            self.shoot_cooldown = 90 
        else:
            self.shoot_cooldown -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, ALIEN_GREEN, self.rect)

# ---------------------------------------------------------
# 3. Gestor de Niveles
# ---------------------------------------------------------
def cargar_nivel(nivel):
    if nivel == 1:
        player_pos = (50, HEIGHT - 100)
        platforms = [
            Platform(0, HEIGHT - 40, WIDTH, 40),
            Platform(200, 450, 100, 20),
            Platform(350, 350, 100, 20),
            Platform(550, 250, 100, 20),
            Platform(700, 150, 100, 20)
        ]
        goal = Goal(730, 110, 40, 40)
        alien = Alien(580, 210)
        return player_pos, platforms, goal, alien
        
    elif nivel == 2:
        player_pos = (50, HEIGHT - 100)
        platforms = [
            Platform(0, HEIGHT - 40, WIDTH, 40),
            Platform(150, 500, 80, 20),
            Platform(350, 300, 80, 20),
            Platform(600, 400, 80, 20),
            Platform(220,400,40,20)
        ]
        goal = Goal(620, 360, 40, 40)
        alien = Alien(370, 260)
        return player_pos, platforms, goal, alien

    elif nivel == 3:
        player_pos = (50, HEIGHT - 100)
        platforms = [
            Platform(0, HEIGHT - 40, WIDTH, 40),
            Platform(50, 400, 100, 20),
            Platform(250, 300, 100, 20),
            Platform(50, 200, 100, 20),
            Platform(250, 100, 100, 20)
        ]
        goal = Goal(280, 60, 40, 40)
        alien = Alien(280, 260) 
        return player_pos, platforms, goal, alien

    elif nivel == 4:
        player_pos = (50, HEIGHT - 100)
        platforms = [
            Platform(0, HEIGHT - 40, 300, 40),
            Platform(500, HEIGHT - 40, 300, 40),
            Platform(350, 400, 100, 20),
            Platform(150, 250, 100, 20)
        ]
        goal = Goal(700, HEIGHT - 80, 40, 40)
        alien = Alien(550, HEIGHT - 80)
        return player_pos, platforms, goal, alien

    elif nivel == 5:
        player_pos = (50, 500)
        platforms = [
            Platform(30, 550, 80, 20),
            Platform(200, 450, 60, 20),
            Platform(350, 350, 60, 20),
            Platform(500, 250, 60, 20),
            Platform(650, 150, 100, 20)
        ]
        goal = Goal(680, 110, 40, 40)
        alien = Alien(355, 310)
        return player_pos, platforms, goal, alien

    else:
        return None, None, None, None

# ---------------------------------------------------------
# 4. Función Principal (Game Loop)
# ---------------------------------------------------------
def main():
    nivel_actual = 1
    juego_terminado = False
    
    player_pos, platforms, goal, alien = cargar_nivel(nivel_actual)
    player = Player(player_pos[0], player_pos[1])
    lasers = [] 
    
    font = pygame.font.SysFont(None, 48)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # GIT COMMIT: Añadir botón de desarrollador (Tecla N) para saltar nivel
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n: # Al presionar la letra N
                    if not juego_terminado:
                        nivel_actual += 1
                        datos_nuevo_nivel = cargar_nivel(nivel_actual)
                        
                        if datos_nuevo_nivel[0] is None:
                            juego_terminado = True
                        else:
                            player_pos, platforms, goal, alien = datos_nuevo_nivel
                            player.rect.topleft = player_pos
                            lasers.clear()

        if not juego_terminado:
            player.update(platforms)
            alien.update(player.rect.centerx, player.rect.centery, lasers)
            
            for laser in lasers[:]:
                laser.update()
                
                # Borrar láseres fuera de pantalla
                if laser.rect.left < 0 or laser.rect.right > WIDTH or laser.rect.top < 0 or laser.rect.bottom > HEIGHT:
                    lasers.remove(laser)
                # Chocar con láser
                elif laser.rect.colliderect(player.rect):
                    lasers.remove(laser)
                    player.rect.topleft = player_pos # Volver al inicio del nivel
                    lasers.clear()

            # Chocar con marciano
            if player.rect.colliderect(alien.rect):
                player.rect.topleft = player_pos
                lasers.clear()

            # Caer al vacío
            if player.rect.top > HEIGHT:
                player.rect.topleft = player_pos 
                lasers.clear()

            # Tocar la meta (Cambio de nivel)
            if player.rect.colliderect(goal.rect):
                nivel_actual += 1
                datos_nuevo_nivel = cargar_nivel(nivel_actual)
                
                if datos_nuevo_nivel[0] is None:
                    juego_terminado = True
                else:
                    player_pos, platforms, goal, alien = datos_nuevo_nivel
                    player.rect.topleft = player_pos
                    lasers.clear()

        # Dibujado
        screen.fill(SKY_BLUE) 
        
        if not juego_terminado:
            goal.draw(screen)
            for plat in platforms:
                plat.draw(screen)
            alien.draw(screen)
            for laser in lasers:
                laser.draw(screen)
            player.draw(screen)
        else:
            # Mensaje final
            win_text = font.render("¡HAS GANADO EL JUEGO!", True, TEXT_BLACK)
            screen.blit(win_text, (WIDTH//2 - 200, HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()