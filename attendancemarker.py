import cv2
import pickle
from numpy import load,asarray,expand_dims
from tensorflow.keras.models import load_model
from mtcnn.mtcnn import MTCNN
from tensorflow.keras.preprocessing.image import load_img,img_to_array
import os
import xlsxwriter as xls

detector = MTCNN()
facemodel=load_model('models/facenet_keras.h5')
model=pickle.load(open('models/predicition_model.h5', 'rb'))
reg_nums=load('dataset/reg_nums.npz')['arr_0']

attendance={}


def make_sheet(d):
    workbook = xls.Workbook('newinput/attendance.xlsx')
    worksheet = workbook.add_worksheet()
    row=0
    for key,val in d.items():
        worksheet.write(row,0,key)
        worksheet.write(row,1,val)
        row += 1
    workbook.close()
def get_embedding(face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = expand_dims(face_pixels, axis=0)
    yhat = facemodel.predict(samples)
    return yhat[0]

def mark(imgpath):
    image = load_img(imgpath)
    image=img_to_array(image)

    faces = detector.detect_faces(image)
    for face in faces:
        x, y, w, h = face['box']
        student=image[y:y + h,x:x + w,]
        student=cv2.resize(student,(160,160))
        faceembd=get_embedding(student)
        regno=reg_nums[model.predict([faceembd])[0]]
        attendance[regno]="P"
def get_attendance(path):
    for no in reg_nums:
        attendance[no]='A'
    inames=os.listdir(path)
    for iname in inames:
        mark(path+iname)
    make_sheet(attendance)
