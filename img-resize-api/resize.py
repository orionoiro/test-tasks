from PIL import Image


def resize(width: int, height: int, file):
    im = Image.open(file)
    im.resize((width, height))
    print('job added')
    im.save('new_image', format=im.format)
