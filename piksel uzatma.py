import numpy as np
import cv2


def ratio_calculator(top, bottom, right, left, step):
    return (255 - top) / step, (255 - bottom) / step, (255 - right) / step, (255 - left) / step


def whiten_imge(img, piksel):

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


    new_img = np.concatenate((top_add, img, bottom_add), axis=0)
    right_add = np.concatenate((right_top_corner, right_add, right_bottom_corner), axis=0)
    left_add = np.concatenate((left_top_corner, left_add, left_bottom_corner), axis=0)
    new_img = np.concatenate((left_add, new_img, right_add), axis=1)

    cv2.imshow('new_img', new_img)
    #cv2.imwrite('whitened_image.jpg', new_img)
    cv2.waitKey()
    cv2.destroyAllWindows()

img = cv2.imread('messi.jpg')
whiten_imge(img, 100)
