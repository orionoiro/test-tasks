from PIL import Image


def resize(width: int, height: int, file):
    im = Image.open(file)
    img_type = im.format
    im = im.resize((width, height))
    im.save('new_image', format=img_type)
