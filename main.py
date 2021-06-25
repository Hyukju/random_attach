import os 
import numpy as np
import random
import cv2
import colorsys
import matplotlib.pyplot as plt 


def cal_iou(rect1, rect2):
    # rect : left, top, width, height
    x1 = max(rect1[0], rect2[0])
    y1 = max(rect1[1], rect2[1])
    x2 = min(rect1[0] + rect1[2], rect2[0]+rect2[2])
    y2 = min(rect1[1] + rect1[3], rect2[1]+rect2[3])
    
    # intersection area 
    inter = max(0, x2 - x1) * max(0, y2 - y1 )
    area1 = rect1[2] * rect1[3]
    area2 = rect2[2] * rect2[3]
    # union area 
    union = area1 + area2 - inter
    iou = inter / float(union)
    return iou

def read_file_path_list(main_dir):
    dir_list = os.listdir(main_dir)

    file_path_list = []

    for dir_name in dir_list:
        file_list = os.listdir(os.path.join(main_dir,dir_name))
        for file in file_list:
            file_path_list.append(os.path.join(main_dir, dir_name, file))
    
    return file_path_list


def get_random_pill():
    width =  np.random.randint(50, 140)
    height =  np.random.randint(50, 140)

    x = np.random.randint(0, 300 - width)
    y = np.random.randint(0, 300 - height)

    return x, y, width, height


def get_random_pills(n):
    pills = []
    pills.append(get_random_pill())

    back = np.zeros((300,300))

    for pill in pills:
        x, y, width, height = pill[0],pill[1],pill[2],pill[3]
        back[x:x+width, y:y+height] = 1    

    for _ in range(n):
        # plt.imshow(back)
        # plt.show()
        width =  np.random.randint(50, 100)
        height =  np.random.randint(50, 100)

        non_zero_y, non_zero_x = np.nonzero(back)
        
        while True:   
            ious = 0   
            idx = random.choice(range(len(non_zero_x)))
            x = non_zero_x[idx]
            y = non_zero_y[idx]

            if x + width < 300 and y + height < 300:
            
                for pill in pills:
                    iou = cal_iou(pill, [x, y, width, height])
                    ious += iou  
                print(ious)                              
                if ious < 0.1:                
                    back[x:x+width, y:y+height] = 1                          
                    pills.append([x, y, width, height])
                    break

    return pills

def convert_rectangle_to_polygon(x,y,width, height):
    xs = [x, x+width, x+width, x]
    ys = [y, y, y+height, y+height]
    pts = [x for x in zip(xs, ys)]
    return pts

def random_color():  
    h = random.uniform(0, 1)
    hsv = [h, 0.7, 1]
    color = colorsys.hsv_to_rgb(*hsv)
    color = [x * 255 for x in color]
    return color
 

def draw(backgroud, pills):
    for pill in pills:        
        color = random_color()
        print(color)
        backgroud = cv2.fillPoly(backgroud, [pill],  color)
    
    cv2.namedWindow('aa',0)
    cv2.imshow('aa', backgroud)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def random_rotate_and_shfit(x, y, width, height):
    margin = 30

    angle = np.random.randint(0, 360)
    rad = np.radians(angle)
    cos = np.cos(rad)
    sin = np.sin(rad)   
    sx = np.random.randint(margin, 300 - width - margin)
    sy = np.random.randint(margin, 300 - height - margin)

    cx = (x + width)/2
    cy = (y + height)/2

    pts = convert_rectangle_to_polygon(x, y, width, height)

    pts_rs = []

    for i, xy in enumerate(pts):
        x = xy[0]
        y = xy[1]    
        xx = cos * (x - cx) - sin * (y - cy) + sx
        yy = sin * (x - cx) + cos * (y - cy) + sy
        pts_rs.append([xx, yy])
    return pts_rs 
     

background = np.zeros((300,300,3), dtype='uint8')

rect_pills = [] 
poly_pills = []
poly_rs_pills = []

# for _ in range(4):
#     rect = get_random_pill()
#     poly = convert_rectangle_to_polygon(*rect)
#     poly_rs = random_rotate_and_shfit(*rect)

#     rect_pills.append(rect)
#     poly_pills.append(poly)
#     poly_rs_pills.append(poly_rs)

pills = get_random_pills(4)

for pill in pills:
    poly = convert_rectangle_to_polygon(*pill)
    poly_pills.append(poly)

draw(background.copy(), np.array(poly_pills))

# draw(background.copy(), np.array(poly_pills))
# draw(background.copy(), np.array(poly_rs_pills, dtype='int32'))

iou = cal_iou([0,0,100,100], [50,50,100,100])
print(iou)



        
        

    
