# -*- coding: utf-8 -*-
__verson__ = 2.0
__copyright__ = "Yinru Ye(320180940480), Wanfeng Zhu(320180940691),"
"Qiyuan Zhang(320180940541), Haoqiu Yan(320180940440) Copyright 2019"

import numpy as np
import cv2
import os
import image


def cmp_hash(hash1, hash2):
    pixel_difference = 0
    if len(hash1) != len(hash2):
        return (-1)
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            pixel_difference = pixel_difference + 1
    return pixel_difference


def template_select(target):
    l_template = image.Template(r'templates\l_template.jpg')
    f_template = image.Template(r'templates\f_template.jpg')
    templates = [l_template, f_template]
    # Extract the finger part of the target picture
    target_skin = target.skin_recognition('target')
    matches_index = []
    # Traverse the template, one by one with the target picture
    target_skin_hash = target_skin.hash()
    for i in templates:
        n = cmp_hash(i.hash(), target_skin_hash)
        matches_index.append(n)
    matches_index_c = sorted(matches_index)
    match = matches_index_c[0]
    n1 = 0
    for a in matches_index:
        if a == match:
            best_match = templates[n1]
        n1 = n1 + 1
    return best_match  # Path to the best matching template


def flann_creator():
    index_params = dict(algorithm=0, trees=5)
    search_params = dict(checks=50)
    flann_fitter = cv2.FlannBasedMatcher(index_params, search_params)
    return flann_fitter


def match(template, target, target_skin, flann_fitter):
    # Read template feature points
    template_path = template.image_path
    tem_descriptor_file = template_path.replace(template_path.split('.')[-1], "npy")
    template_des = np.load(tem_descriptor_file)
    # Call the function to extract the feature points keypoints and descriptors of the target picture
    target_kp = target_skin.descriptor()[0]
    target_des = target_skin.descriptor()[1]
    matches = flann_fitter.knnMatch(template_des, target_des, k=2)
    # Leave highly matched feature points
    good = []
    # Discard matches greater than 0.7
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    if len(good) < 4:  # Set the minimum number of feature point matches to 4, if less than 4, it returns "two pictures are not relevant"
        print("Not enough matches are found - %d/%d" % (len(good), 4))
    dst_pts = np.float32([target_kp[m.trainIdx].pt for m in good])  # Key points after matching, unfiltered
    x_min = min(dst_pts[:, 0])
    y_min = min(dst_pts[:, 1])
    x_max = max(dst_pts[:, 0])
    y_max = max(dst_pts[:, 1])
    if x_max > target.row:
        x_max = target.row
    if y_max > target.col:
        y_max = target.col
    left_down_point = (x_min, y_min)  # Bottom left and top right corners of the rectangle
    right_up_point = (x_max, y_max)
    x = int((x_max+x_min)/2)
    y = int((y_max+y_min)/2)
    middle = (x,y)
    # Draw rectangle
    shown = target.color_read
    cv2.rectangle(shown, left_down_point, right_up_point, (255, 214, 125),10)
    # The name of the template that matches the target, plus text
    letter = template_path.split('\\')[-1].split('_')[0]
    cv2.putText(shown, str.upper(letter), middle, cv2.FONT_HERSHEY_SIMPLEX, 8, (255, 214, 125), 10)
    # Reduce the target picture proportionally to avoid overflowing the screen
    resized = cv2.resize(shown, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
    return resized


def run(target_path):
    # Extract the skin color part of the target picture
    target = image.Target(target_path)
    target_skin = target.skin_recognition('target')
    # Choose the template that best matches the target picture
    best_match = template_select(target)
    # createc flann filter
    flan_fitter = flann_creator()
    # Match the target picture with the template picture
    result = match(best_match, target, target_skin, flan_fitter)
    letter = str.upper(best_match.image_path.split('\\')[-1].split('_')[0])
    root_path = 'gesture_recognition/'
    import datetime
    nowTime = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    path = root_path + '{}_{}.jpg'.format(letter, nowTime)
    if os.path.exists(root_path):
        pass
    else:
        os.makedirs(root_path)
    cv2.imwrite(path, result)
    print("Target has been saved in ", path)
    return result

