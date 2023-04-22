import pygame


BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def send_data(data):
    with open('../data/trans.txt', 'w') as f:
        f.write(data)

# write text 
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# (ширина, высота).
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("My Game")

isrun = True 

# для управления скоростью обновления экрана.
clock = pygame.time.Clock()

pygame.joystick.init()
textPrint = TextPrint()

while isrun:
    # Возможные действия джойстика: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get():  # Пользователь что-то сделал.
        if event.type == pygame.QUIT: 
            isrun = False
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # Не помещайте другие команды рисования
    # выше этого, иначе они будут удалены с помощью этой команды.
    screen.fill(WHITE)
    textPrint.reset()

    # количество джойстиков
    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # Для каждого джойстика:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id () - это метод SDL2
            jid = joystick.get_id()
        textPrint.tprint(screen, "Joystick {}".format(jid))
        textPrint.indent()

        # Получить имя из ОС для контроллера / джойстика.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid () - это метод SDL2
            guid = "Null"
        finally:
            textPrint.tprint(screen, "GUID: {}".format(guid))

        # определение двух осей
        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            if i == 0:
                data = f"y:{toFixed(axis, 3)}"
                send_data(data)
            if i == 1:
                data = f"x:{toFixed(axis, 3)}"
                send_data(data)
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.tprint(screen,
                             "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()

        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        # Положение шляпы. Все или ничего для направления, а не поплавок, как
        # get_axis (). Позиция - это набор значений типа int (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()

    # update display 
    pygame.display.flip()

    # Ограничение до 20 кадров в секунду.
    clock.tick(20)

# debug IDE quit 
pygame.quit()
