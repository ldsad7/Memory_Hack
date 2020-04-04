from PIL import Image
import numpy as np
import cv2

alpha = 0.4

img2 = cv2.imread('__car_1.jpg')
img1 = cv2.imread('car_2.jpg')

r,c,z = img1.shape

out_img = np.zeros(img1.shape,dtype=img1.dtype)
out_img[:,:,0] = (alpha * img1[:,:,0]) + ((1-alpha) * img2[:,:,0])
out_img[:,:,1] = (alpha * img1[:,:,1]) + ((1-alpha) * img2[:,:,1])
out_img[:,:,2] = (alpha * img1[:,:,2]) + ((1-alpha) * img2[:,:,2])
'''
# if want to loop over the whole image
for y in range(r):
    for x in range(c):
        out_img[y,x,0] = (alpha * img1[y,x,0]) + ((1-alpha) * img2[y,x,0])
        out_img[y,x,1] = (alpha * img1[y,x,1]) + ((1-alpha) * img2[y,x,1])
        out_img[y,x,2] = (alpha * img1[y,x,2]) + ((1-alpha) * img2[y,x,2])
'''

# im1 = Image.open("__car_1.jpg")
# im2 = Image.open("car_2.jpg")
# blended = Image.blend(im1, im2, alpha=0.5)
# blended.save("blended.png")

# from PIL import Image
# import glob

# foreground_name = 'car_2.jpg'
# foreground = Image.open(foreground_name)
# foreground = foreground.convert('RGBA')

# for file_name in glob.glob('*.jpg'):
#     print (file_name)
#     background_name = file_name
#     background = Image.open(background_name)

#     x = int((background.size[0] / 2) - (foreground.size[0] / 2))
#     y = int((background.size[1] / 2) - (foreground.size[1] / 2))

#     background = background.convert('RGBA')
#     background.paste(foreground, (x, y), mask = foreground)
#     background = background.convert('RGB')
#     background.save('__' + background_name.split('.')[0] + '.jpg','JPEG')

# print('Gotovo bla-a')

# out_img = img2.copy()

# out_img = cv2.add(img1, img2)
# cv2.addWeighted(out_img, 0.5, img1, 0.5, img2)

# cv2.imshow('Output',out_img)
# cv2.waitKey(0)