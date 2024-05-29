import pygame
from pygame.locals import *
import time
from database import UserDatabase

class Clock:
    def __init__(self, minutes, seconds):
        self.last_time = int(time.time())
        self.minutes = minutes
        self.seconds = seconds

    def pack(self):
        return (self.minutes, self.seconds)

    def get(self, time):
        self.minutes = time[0]
        self.seconds = time[1]

    def reset(self):
        self.last_tỉme = time.time()
        self.minutes = 0
        self.seconds = 0

    def update(self):
        second_increase = int(time.time() - self.last_time)
        self.seconds += second_increase
        if self.seconds >= 60:
            self.minutes += 1
            self.seconds -= 60
        if self.minutes == 60:
            self.minutes = 0
        if second_increase != 0:
            self.last_time = int(time.time())

    def display_time(self):
        return f"{self.minutes:02d}:{self.seconds:02d}"

class Button:
    def __init__(self, text, position, size):
        self.text = text
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.default_color = (211,151,68)   
        self.hover_color = (220,20,60) 
        self.click_color = (220,20,60) 
        self.color = self.default_color
        self.FONT = pygame.font.Font(None, 60)
        self.alpha = 255
        self.blink_count = 0
        self.blink_frequency = 20  # Cấu hình tần suất nhấp nháy
        self.blink_color = (220,20,60)   # Màu của hiệu ứng nhấp nháy

    def draw(self, surface):
        button_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        gradient = pygame.Surface((self.size[0], self.size[1] // 2), pygame.SRCALPHA)
        button_surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        button_surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        surface.blit(button_surface, self.position)
        text_surface = self.FONT.render(self.text, True, (211,151,68))  # Màu vàng
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
     
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_color(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover_color
            if pygame.mouse.get_pressed()[0]:
                self.color = self.click_color
        else:
            self.color = self.default_color
        
        # Hiệu ứng nhấp nháy khi nút được nhấn
        if self.color == self.click_color:
            self.blink_count += 1
            if self.blink_count % self.blink_frequency == 0:
                self.blink_color = (255 - self.blink_color[0], 0, 0)  # Thay đổi màu giữa đỏ và trắng
        else:
            self.blink_color = (220,20,60)  # Reset màu nhấp nháy khi không được nhấn

class Button_Image():
    def __init__(self, image_path, pos, scale, volume):
        BASE_PATH = 'assets/button/'
        image = pygame.image.load(BASE_PATH + image_path + '.png')
        self.image = pygame.transform.scale(image, scale)

        image = pygame.image.load(BASE_PATH + image_path + '_clicked.png')
        self.image_clicked = pygame.transform.scale(image, scale)

        self.rect = self.image.get_rect(topleft=pos)
        self.clicked = False

        self.sound = pygame.mixer.Sound('sound/select sound - ver 2.mp3')
        self.sound.set_volume(volume)

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        surface.blit(self.image, self.rect.topleft)

        if self.rect.collidepoint(pos):
            surface.blit(self.image_clicked, self.rect.topleft)
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if action:
            self.sound.play()
        return action

class TextBox:
    def __init__(self, pos, text = '', volume = 1):
        self.pos = pos
        self.font = pygame.font.Font('font/Montserrat-SemiBold.ttf', 40)
        self.text = self.font.render(text, True, (211, 151, 68))
        self.rect = self.text.get_rect(topleft = pos)

    def update(self, text):
        self.text = self.font.render(text, True, (211, 151, 68))
        self.rect = self.text.get_rect(topleft=self.pos)

    def draw(self, screen):
        screen.blit(self.text, self.rect)


class Display():
    def __init__(self, screen, buttons, text_boxes):
        '''
        :param screen:
        :param buttons:
        :param text_boxes: [(info, pos)]
        '''
        self.screen = screen

        # get button
        self.buttons = buttons
        for button in self.buttons.keys():
            self.buttons[button] = Button_Image(button, self.buttons[button][0],(96, 115), self.buttons[button][1])

        # get board
        self.text_boxes = []
        for text_box in text_boxes:
            self.text_boxes.append(TextBox(text_box[1], text_box[0]))
        self.clock = Clock(0, 0)

    def draw_page(self):
        for button in self.buttons:
            if isinstance(button, Button):
                button.draw(self.screen)

    def reset_time(self):
        self.clock.reset()

    def render(self, pause):
        self.draw_page()
        for button in self.buttons.keys():
            if self.buttons[button].draw(self.screen):
                return button

        self.text_boxes[-1].update('Clock: ' + self.clock.display_time())
        if not pause:
            self.clock.update()

        for textbox in self.text_boxes:
            textbox.draw(self.screen)