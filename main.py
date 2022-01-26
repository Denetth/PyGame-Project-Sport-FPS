from player import Player
from sprite_objects import *
from raycast import raycasting_walls
from drawing import Drawing
from interaction import Interaction
from time import sleep

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()
score = 0

sprites = Sprites()
player = Player(sprites)
drawing = Drawing(sc, player, clock)
interaction = Interaction(player, sprites, drawing)
f = open("highscore.txt", mode="rt", encoding="utf-8")
highscore = str(f.read())
f.close()

sc.fill((0, 180, 210))

class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('calibri', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def draw_menu():
    font = pygame.font.SysFont('calibri', 60)
    greenButton.draw(sc, (0, 0, 0))
    redButton.draw(sc, (0, 0, 0))
    text = font.render(f'Highscore: {highscore}', 0, (255, 255, 255))
    sc.blit(text, (10, 5))


def draw_game():
    global score
    sleep(0.01)
    player.movement()
    drawing.background()
    walls, wall_shot = raycasting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.object_list])
    drawing.fps(clock)
    drawing.score(interaction.object_interaction())
    score = interaction.object_interaction()
    drawing.player_weapon([wall_shot, sprites.sprite_shot])

    interaction.object_interaction()
    interaction.npc_action()

    pygame.display.flip()
    clock.tick()


greenButton = Button((0, 255, 0), 450, 250, 250, 100, "Start")
redButton = Button((255, 0, 0), 450, 450, 250, 100, "Quit")

game_state = "menu"
run = True
while run:
    if game_state == "menu":
        sc.fill((0, 0, 0))
        draw_menu()
    elif game_state == "game":
        pygame.mouse.set_visible(False)
        sc.fill((0, 0, 0))
        draw_game()

    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if player.is_pushed():
            if int(highscore) < score:
                f = open("highscore.txt", mode="w")
                f.write(str(score))
                f.close()
            quit()

        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if greenButton.isOver(pos):
                    game_state = "game"
                if redButton.isOver(pos):
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if greenButton.isOver(pos):
                    greenButton.color = (105, 105, 105)
                else:
                    greenButton.color = (0, 255, 0)
                if redButton.isOver(pos):
                    redButton.color = (105, 105, 105)
                else:
                    redButton.color = (255, 0, 0)
