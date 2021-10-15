import numpy as np
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas
import logging
logger = logging.getLogger(__name__)


def action(command_type, message, root):
    # is_exist <lantern window>
    try:
        root.deiconify()
        condition = False
    except Exception as e:
        _exception = e
        condition = True
    # switch commands
    if command_type == 'ON':
        if condition:
            # create the lantern area
            # Зачем создавать новое окно? Логичней было бы создать
            # одно глобальное окно и обновлять его цвет, или прятать при необходимости.
            root = Tk()
            root.title = "lantern"
            frame = Frame(root)
            frame.grid()
            light = np.zeros([200, 200, 3], dtype=np.int8)
            light[:, :, 0:1] = 240
            light[:, :, 2] = 120
            img = Image.fromarray(light, 'RGB')
            # add image on window
            canvas = Canvas(root, height=200, width=200)
            photo = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor='nw', image=photo)
            canvas.grid(row=1, column=1)
            root.update()
        else:
            logging.warning("You tried to command 'ON', but lantern is already running")
    # elif
    if command_type == 'OFF':
        if condition:
            logging.warning("You tried to command 'OFF', but lantern isn't running")
        else:
            # Всю работу с окнами и графикой надо было вынести в отдельный класс.
            root.destroy()
    # elif
    if command_type == 'COLOR':
        if condition:
            logging.warning("You tried to command 'COLOR', but lantern isn't running")
        else:
            # get color values
            # Парсинг сообщения размазан по двум файлам. Сложно отлаживать и поддерживать.
            length = int.from_bytes(message[1:3], "big")
            value = message[3:3 + length]
            red = value[0]
            green = value[1]
            blue = value[2]
            light = np.zeros([200, 200, 3], dtype=np.int8)
            light[:, :, 0] = red
            light[:, :, 1] = green
            light[:, :, 2] = blue
            img = Image.fromarray(light, 'RGB')
            # add image on figure
            # Копипаста.
            canvas = Canvas(root, height=200, width=200)
            photo = ImageTk.PhotoImage(img)
            canvas.create_image(0, 0, anchor='nw', image=photo)
            canvas.grid(row=1, column=1)
            root.update()

        # add new command here

    return root
