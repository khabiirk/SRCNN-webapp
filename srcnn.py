import sys
import gunicorn
import keras
import cv2
import numpy as np
import matplotlib
import math
from matplotlib import pyplot as plt
import os
from PIL import Image

def psnr(target, ref):
         
    # assume RGB image
    target_data = target.astype(float)
    ref_data = ref.astype(float)

    diff = ref_data - target_data
    diff = diff.flatten('C')

    rmse = math.sqrt(np.mean(diff ** 2.))

    return 20 * math.log10(255. / rmse)
def compare_images(target, ref):
    
    return psnr(target, ref)

    
    
def modcrop(img, scale):
    #print(img)
    tmpsz = img.shape
    sz = tmpsz[0:2]
    sz = sz - np.mod(sz, scale)
    img = img[0:sz[0], 1:sz[1]]
    return img


def shave(image, border):
    img = image[border: -border, border: -border]
    return img

class SRCNN:
    def __init__(self):
        self.model = keras.models.load_model('model/mo.h5')
        self.model.load_weights('model/3051crop_weight_200.h5')
    

    def predict(self, request):
        

        r = Image.open(request)
        

        
        #print(file)
        degraded = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)
        # preprocess the image with modcrop

        degraded = modcrop(degraded, 3)
        temp = cv2.cvtColor(degraded, cv2.COLOR_BGR2YCrCb)
        Y = np.zeros((1, temp.shape[0], temp.shape[1], 1), dtype=float)
        Y[0, :, :, 0] = temp[:, :, 0].astype(float) / 255
        
        # perform super-resolution with srcnn
        pre = self.model.predict(Y, batch_size=1)
        
        # post-process output
        pre *= 255
        pre[pre[:] > 255] = 255
        pre[pre[:] < 0] = 0
        pre = pre.astype(np.uint8)
        
        # copy Y channel back to image and convert to BGR
        temp = shave(temp, 6)
        temp[:, :, 0] = pre[0, :, :, 0]
        output = cv2.cvtColor(temp, cv2.COLOR_YCrCb2BGR)
        degraded = shave(degraded.astype(np.uint8), 6)
        score = compare_images(degraded, output)
        retval, buffer_img = cv2.imencode('.png', output)
        #cv2.imwrite('/Users/khabiirkhodabaccus/Desktop/tutorial/SRCNN-webapp/static/tmp.png', output)
       
        # return image
        return buffer_img, score


# o = SRCNN()
# output = o.predict('8.png')
# print(output)
# #cv2.imwrite('test.png', output)
# fig, axs = plt.subplots(1, 3, figsize=(20, 8))
# axs[0].imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
