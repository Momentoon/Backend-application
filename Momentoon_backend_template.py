import os
import cv2
import torch
import numpy as np
import torch.nn as nn
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage
cred = credentials.Certificate() # Your api key needed to placed on here
default_app = firebase_admin.initialize_app(cred,{'storageBucket': 'Your bucket name here'}) # your api key and your firebase storageBucket
bucket_name = "" #Your bucket name here

from torch.nn import functional as F
import pyrebase

path_UF = "./unfiltered" #Unfiltered, original image
path_BU = "./archive"
path_RS = "./storage"
codeToDownload = 'temp'
model_list = [] # TODO: Inserting model, currently we have only one temporary model.


path_filtered = "images/FILTERED/"
path_archive = "images/ARCHIVE/"


path_to_temporary_save_folder = "" # Need to change it on your local environment
#for i in range(0,2):
while 1:

    for file in all_files:

                if 'UPLOAD/'+codeToDownload in file.name:
                    z=storage.child(file.name).get_url(None)
                    storage.child(file.name).download(""+path_UF+"/"+file.name.replace("images/UPLOAD","") )
                    storage.delete(file.name)
                    for file in os.listdir(path_UF):
                        if codeToDownload in file:
                            if(file[4] == '1'): #You can modify 1 with other identifier language, but must matched with the frontend code.
                                load_path = os.path.join(path_UF, file)
                                save_path = os.path.join(path_to_temporary_save_folder, "Result"+file)
                                raw_image = cv2.imread(load_path)

                                tempx, tempy, tempz= raw_image.shape
                                raw_image = cv2.resize(raw_image ,(256,256), interpolation = cv2.INTER_AREA)
                                cv2.imwrite(save_path, raw_image)

                                #Inference code here : The Inference module code should has path_to_temporary_save_folder as input, and output folder as path_RS, to enable retrive the filtered picture.

                                os.remove(path_UF+"/"+file)
                                os.remove(path_to_temporary_save_folder+"/"+'Result'+file)

                                sr = cv2.dnn_superres.DnnSuperResImpl_create() #Superresolution file
                                sr.readModel( ) #Resoultion needed, edit it with your Resoultion models, to make it into original size.
                                sr.setModel()
                                load_path = os.path.join(path_RS, "Result"+file)
                                save_path = os.path.join(path_RS, "Result"+file)
                                raw_image = cv2.imread(load_path)
                                result = sr.upsample(raw_image)
                                raw_image = cv2.resize(result ,(tempy ,tempx), interpolation = cv2.INTER_AREA)
                                cv2.imwrite(save_path, raw_image)

                for file in os.listdir(path_RS):
                            storage.child(path_filtered+"FC"+file).put(""+path_RS+"/"+file) # FC : Filter completed, temporary name. It will save filtered image to firebase.
                            os.remove(path_RS+"/"+file) #It removed filtered image in your computer.
