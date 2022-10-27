import pygame
import pygame_menu
from main import main_function


# initializing the constructor
pygame.init()

# screen resolution
res = (720, 720)

# opens up a window
screen = pygame.display.set_mode(res)

def get_url_and_start():
    url = url_camera_phone.get_value()
    start('CAMERA_PHONE',url)



def start(device,url):
    main_function(device,url)


# Camera_Phone menu
phone_menu = pygame_menu.Menu('Camera Phone', 720, 720,
                    theme=pygame_menu.themes.THEME_BLUE)
url_camera_phone = phone_menu.add.text_input('Enter the url: ',default='http://10.1.18.99:4747/video')
phone_menu.add.button('Start',get_url_and_start)
# second menu
second_menu = pygame_menu.Menu('Select device', 720, 720,
                    theme=pygame_menu.themes.THEME_BLUE)

second_menu.add.button('Camera_Laptop',start,'CAMERA_LAPTOP','')
second_menu.add.button('Camera_Phone',phone_menu)
second_menu.add.button('Video',start,'VIDEO','')
second_menu.add.button('Exit', pygame_menu.events.EXIT)
# second_menu.add.selector('Select device: ',
#                 [('Camera_Laptop', 'CAMERA_LAPTOP'),
#                 ('Camera_Phone', 'CAMERA_PHONE'),
#                 ('Video', 'VIDEO'),
#                 ],
#                 onchange=set_device,
#                 selector_id='select_device'
#                 )

# second_menu.add.button('Start', start,DEVICE)
# second_menu.add.button('Quit', pygame_menu.events.EXIT)



# main menu
menu = pygame_menu.Menu('Welcome', 720, 720,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Enter your name: ', default='User')
menu.add.button('Next',second_menu)
menu.add.button('Exit',pygame_menu.events.EXIT)
menu.mainloop(screen)