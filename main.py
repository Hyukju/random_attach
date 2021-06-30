import os 
import numpy as np
import random
import cv2
import colorsys
import matplotlib.pyplot as plt 

CANVAS_WIDTH = 300
CANVAS_HEIGHT = 300
CANVAS_MARGIN = 300//3
RECT_MIN_WIDTH = 50
RECT_MAX_WIDTH = 100
RECT_MIN_HEIGHT = 50
RECT_MAX_HEIGHT = 100
SUM_IOUS_MIN = 0.0
SUM_IOUS_MAX = 0.001

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


def get_random_rect(rect=None):
    if rect == None:
        width =  np.random.randint(RECT_MIN_WIDTH, RECT_MAX_WIDTH)
        height =  np.random.randint(RECT_MIN_HEIGHT, RECT_MAX_HEIGHT)
    else:
        width = rect[2]
        height = rect[3]

    x = np.random.randint(CANVAS_MARGIN, CANVAS_WIDTH - CANVAS_MARGIN)
    y = np.random.randint(CANVAS_MARGIN, CANVAS_HEIGHT - CANVAS_MARGIN)

    return x, y, width, height

def get_random_rects(num_rects=None, in_rects=None, use_debug=False):
    assert not (num_rects==None and in_rects==None)

    out_rects = []
    # get first rect
    if in_rects == None:
        out_rects.append(get_random_rect())
    else:
        out_rects.append(get_random_rect(in_rects[0]))
        num_rects = len(in_rects)

    back = np.zeros((CANVAS_HEIGHT,CANVAS_WIDTH))

    # insert first rect in background
    for out_rect in out_rects:
        x, y, width, height = out_rect[0],out_rect[1],out_rect[2],out_rect[3]
        back[y:y+height, x:x+width] = 1    

    try:
        for i in range(1,num_rects):

            # get random width, height of other rects     
            if in_rects == None:  
                width =  np.random.randint(RECT_MIN_WIDTH, RECT_MAX_HEIGHT)
                height =  np.random.randint(RECT_MIN_HEIGHT, RECT_MAX_HEIGHT)
            else:
                in_rect = in_rects[i]
                width = in_rect[2]
                height = in_rect[3]

            # get zero point in background
            zero_y, zero_x = np.where(back == 0)
        
            # get indices of zeros points
            zero_indices = list(range(len(zero_x)))

            if use_debug:
                print('# zero_indices = ', len(zero_indices))
                # check rects postions
                cv2.namedWindow('preview',0)
                cv2.imshow('preview', back)
                cv2.waitKey(1000) # ms            
            
            while True:   
                sum_ious = 0   
                # get random index in zero positions
                idx = random.choice(zero_indices)
                x = zero_x[idx]
                y = zero_y[idx]

                if use_debug:
                    print('x, y, width, height = {0},{1},{2},{3}'.format(x, y, width, height))

                # check rect size and position
                if x + width < CANVAS_WIDTH and y + height < CANVAS_HEIGHT:
                    # calculate iou sum to adjust overlap for each rect
                    for out_rect in out_rects:
                        iou = cal_iou(out_rect, [x, y, width, height])
                        sum_ious += iou  

                        if use_debug:
                            print('sum ious = {0:.4f}'.format(sum_ious))    
                                            
                    if sum_ious >= SUM_IOUS_MIN and sum_ious <= SUM_IOUS_MAX:                
                        back[y:y+height, x:x+width,] = 1                          
                        out_rects.append([x, y, width, height])
                        break
                # remove selected index before update
                zero_indices.remove(idx)
    except Exception as e:
        print(e)
        out_rects = None        
    finally:
        if use_debug:
            cv2.destroyWindow('preview')
           
    return out_rects

def convert_rectangle_to_polygon(x,y,width, height):
    # rect(x, y, width, height) -> poly xs = [left, right, right, left], ys =[top, top, bottom, bottom]
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
 

def draw(backgroud, rects):
    for rect in rects:        
        color = random_color()
        backgroud = cv2.fillPoly(backgroud, [rect],  color)
    
    cv2.namedWindow('rects',0)
    cv2.imshow('rects', backgroud)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__=='__main__':

    for _ in range(10):
        background = np.zeros((300,300,3), dtype='uint8')

        rects = [] 
        polys = []
    
        rects = get_random_rects(4, use_debug=True)

        for rect in rects:
            poly = convert_rectangle_to_polygon(*rect)
            polys.append(poly)

        draw(background.copy(), np.array(polys))
  

        
        

    
