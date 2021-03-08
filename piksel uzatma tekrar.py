import numpy as np
import cv2


def ratio_calculator(top, bottom, right, left, step):
    return (255 - top) / step, (255 - bottom) / step, (255 - right) / step, (255 - left) / step


piksel = 100
img = cv2.imread('cigkofte.jfif')
#cv2.imshow('orig', img)
#img = cv2.resize(img, (50, 50))
#print(img)
#print(img.dtype)

top = img[0]
bottom = img[-1]
right = img[:, -1]
left = img[:, 0]

top_add = list()
bottom_add = list()
right_add = np.zeros((len(right), piksel, 3), dtype='uint8')
left_add = np.zeros((len(left), piksel, 3), dtype='uint8')
for i in range(piksel):
    top_inc_ratio, bottom_inc_ratio, right_inc_ratio, left_inc_ratio = ratio_calculator(top, bottom, right, left, piksel - i)  # to increase precision against uint8 format
    top = top + top_inc_ratio
    bottom = bottom + bottom_inc_ratio
    right = right + right_inc_ratio
    left = left + left_inc_ratio

    top_add.append(top)
    bottom_add.append(bottom)
    right_add[:, i] = right
    left_add[:, piksel - 1 - i] = left

top_add = np.array(top_add[::-1], dtype='uint8')
bottom_add = np.array(bottom_add, dtype='uint8')
#print(top_add)
#print(top_add.shape)

right_top_horz = right_add[0]
right_top_vert = top_add[:, -1]
right_bottom_horz = right_add[-1]
right_bottom_vert = bottom_add[:, -1]
left_top_horz = left_add[0]
left_top_vert = top_add[:, 0]
left_bottom_horz = left_add[-1]
left_bottom_vert = bottom_add[:, 0]

right_top_corner = np.zeros((piksel, piksel, 3), dtype='uint8')
right_bottom_corner = np.zeros((piksel, piksel, 3), dtype='uint8')
left_top_corner = np.zeros((piksel, piksel, 3), dtype='uint8')
left_bottom_corner = np.zeros((piksel, piksel, 3), dtype='uint8')

for i in range(piksel):
    right_top_corner[-i -1:, i] = right_top_horz[i]
    right_top_corner[i, :-i -1] = right_top_vert[i]
    right_bottom_corner[:i, i] = right_bottom_horz[i]
    right_bottom_corner[i, :i +1] = right_bottom_vert[i]
    left_bottom_corner[:-i -1, i] = left_bottom_horz[i]
    left_bottom_corner[i, -i -1:] = left_bottom_vert[i]
    left_top_corner[i:, i] = left_top_horz[i]
    left_top_corner[i, i:] = left_top_vert[i]

#cv2.imshow('right_top_c', right_top_corner)
#cv2.imshow('right_bottom_c', right_bottom_corner)
#cv2.imshow('left_bottom_c', left_bottom_corner)
#cv2.imshow('left_top_c', left_top_corner)


new_img = np.concatenate((top_add, img, bottom_add), axis=0)
right_add = np.concatenate((right_top_corner, right_add, right_bottom_corner), axis=0)
left_add = np.concatenate((left_top_corner, left_add, left_bottom_corner), axis=0)
new_img = np.concatenate((left_add, new_img, right_add), axis=1)

cv2.imshow('new_img', new_img)
#cv2.imwrite('walter_white.jpg', new_img)
cv2.waitKey()

"""
for i in range(piksel):
    top_inc_ratio, bottom_inc_ratio, right_inc_ratio, left_inc_ratio = ratio_calculator(top, bottom, right, left, piksel - i)  # to increase precision against uint8 format
    top = cv2.add(top, top_inc_ratio)
    bottom = cv2.add(bottom, bottom_inc_ratio)
    right = cv2.add(right, right_inc_ratio)
    left = cv2.add(left, left_inc_ratio)

    top_add.append(top)
    bottom_add.append(bottom)
    right_add[:, i] = right
    left_add[:, piksel - 1 - i] = left




cv2.imshow('den', new_img)
cv2.waitKey()

for i in range(len(right_top_horz)):
    #print(ratio2(255, right_top_point, 200 - i))
    right_top_point = cv2.add(right_top_point, ratio2(255, right_top_point, 200 - i)).ravel()  # right top point vektör haline geliyor ??
    #print(right_top_point)
    right_corner[len(right_top_horz) -1 -i, i] = right_top_point

    for j in range(i):
        #print(right_top_horz[j])
        #print(right_top_point)
        #print(ratio2(right_top_point.ravel(), right_top_horz[j], i - j))
        right_top_horz[i] = cv2.add(right_top_horz[i], ratio2(right_top_point.ravel(), right_top_horz[i], i - j)).ravel()
        right_corner[-j - 1, i] = right_top_horz[i]


threshold köşegenlerden uzatmalar olcak
mantık ise uzatılan kısımların nihai olarak bu thresholdlara gelmesi olcak
uzamış kenarların pikselleri ile köşegene kadar olan kısımlar mantık olarak aynı olacak
çünkü adım sayısı aynı olmuş oluyor 


bir yarıyı bulup onun simetrisini almak bile yeterli
print(top_add[:, -1])
print(right_add[0])

if top_add[:, -1].all() == right_add[0].all():
    print('true')



img = cv2.imread('den.jfif')
cv2.imshow('orig', img)
#img = cv2.resize(img, (8, 10))
#print(img)
#print(img.dtype)

top = img[0]
#print(top)

bottom = img[-1]
#print(bottom)

right = img[:, -1]

left = img[:, 0]

def ratio_calculator(top, bottom, right, left, step):
    return (255 - top) // step, (255 - bottom) // step, (255 - right) // step, (255 - left) // step


top_add = list()
bottom_add = list()
right_add = np.zeros((len(right), 200, 3))
left_add = np.zeros((len(left), 200, 3))
for i in range(200):
    top_inc_ratio, bottom_inc_ratio, right_inc_ratio, left_inc_ratio = ratio_calculator(top, bottom, right, left, 200 - i)  # to increase precision against uint8 format
    top = cv2.add(top, top_inc_ratio)
    bottom = cv2.add(bottom, bottom_inc_ratio)
    right = cv2.add(right, right_inc_ratio)
    left = cv2.add(left, left_inc_ratio)

    top_add.append(top)
    bottom_add.append(bottom)
    right_add[:, i] = right
    left_add[:, 200 - 1 - i] = left

top_add = np.array(top_add[::-1])
bottom_add = np.array(bottom_add, dtype='uint8')
right_add = right_add.astype('uint8')
left_add = left_add.astype('uint8')

#print(right_add.shape)
#print(left_add.shape)

new_img = np.concatenate((top_add, img), axis=0)
new_img = np.concatenate((new_img, bottom_add), axis=0)

right_add = np.concatenate((right_add, np.zeros((200, 200, 3), dtype='uint8')), axis=0)
right_add = np.concatenate((np.zeros((200, 200, 3), dtype='uint8'), right_add), axis=0)
left_add = np.concatenate((left_add, np.zeros((200, 200, 3), dtype='uint8')), axis=0)
left_add = np.concatenate((np.zeros((200, 200, 3), dtype='uint8'), left_add), axis=0)
new_img = np.concatenate((new_img, right_add), axis=1)
new_img = np.concatenate((left_add, new_img), axis=1)
"""