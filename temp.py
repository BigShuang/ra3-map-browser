import tkinter as tk
from PIL import Image

from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

ImageFile.MAXBLOCK = 800 * 800

img_p = "D:\Documents\Red Alert 3\other\(as)maqinuo1.6ee\(as)maqinuo1.6ee_art.tga"

img = Image.open(img_p)
img.resize((200, 200))
img.show()