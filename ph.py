from PIL import Image, ImageEnhance
import numpy as np
import cv2

def open_and_resize_image(input, max_height, max_width):
    img = Image.open(input)
    if img.height > max_height and img.height > img.width:
        # vertical image
        percentage_decrease = (max_height * 100) / img.height / 100
        new_height = round(img.height * percentage_decrease)
        new_width = round(img.width * percentage_decrease)
        img = img.resize((new_width, new_height))

    if (img.width > max_width and img.width > img.height) or (img.width == img.height and img.width > max_width):
        # Horizontal image
        percentage_decrease = (max_width * 100) / img.width / 100
        new_height = round(img.height * percentage_decrease)
        new_width = round(img.width * percentage_decrease)
        img = img.resize((new_width, new_height))
    img.save('new_size.jpg', 'JPEG')
    return img

def bright(source_name, result_name, brightness):
    source = Image.open(source_name)
    result = Image.new('RGB', source.size)
    for x in range(source.size[0]):
        for y in range(source.size[1]):
            r, g, b = source.getpixel((x, y))

            red = int(r * brightness)
            red = min(255, max(0, red))

            green = int(g * brightness)
            green = min(255, max(0, green))

            blue = int(b * brightness)
            blue = min(255, max(0, blue))

            result.putpixel((x, y), (red, green, blue))
    result.save(result_name, "JPEG")

if __name__ == "__main__":
    im1 = Image.open('car_1.jpg')
    im1 = im1.convert('RGBA')
    im2 = Image.open('car_2.jpg')
    im2 = im2.convert('RGBA')
    im2 = im2.resize(im1.size)
    # print(im2.split())
    alpha = ImageEnhance.Brightness(im2.split()[3]).enhance(0.30)
    im2.putalpha(alpha)
    # img2 = cv2.imread('car_2.jpg')
    # height, width = img2.shape[:2]
    # print(img2.shape[:2])
    # open_and_resize_image('car_1.jpg', height, width)
    Image.alpha_composite(im1, im2).save("test3.png")
