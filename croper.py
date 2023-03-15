import random
from PIL import Image, ImageFilter
from config import blurValue

def croper(file_name, mode):
    ### для автоматической обрезки
    img = Image.open(f'photos/{file_name}')
    width, height = img.size
    newHeight = (width//16)*9
    new_image = img.crop((0, (height-newHeight)//2, width, (height - ((height-newHeight)//2))))
    new_image = new_image.filter(ImageFilter.GaussianBlur(blurValue))
    new_image = new_image.resize((int((height/9)*16), height))
    widthLast = int((height/9)*16)
    new_image.paste(img, (int((widthLast - width)/2), 0))
    if mode == "crop":
        new_image = new_image.resize((900, 506))
    fileName = random.randint(9999, 999999)
    new_image.save(f'photos/{fileName}.png')

    widthToReturn, heightToReturn = new_image.size
    return [f"{fileName}.png", f"{widthToReturn}:{heightToReturn}"]