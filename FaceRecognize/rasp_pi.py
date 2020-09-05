
# from imutils.video import VideoStream
import time
# import cv2
# import numpy as np
from datetime import datetime
import os
# import urllib.request
# import face_recognition
import json
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from requests.packages import urllib3
# --------------------------------------------------------------
cred = credentials.Certificate("deviot-may-cham-cong-firebase-adminsdk-4j9vd-c20046ba51.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://deviot-may-cham-cong.firebaseio.com'})
def AddNew():
    tmp_vr = []
    # FireBase_Com.Init()
    addMember = db.reference('addMember')
    addTab = addMember.get()
    # print(addTab)
    # json_addTab = json.dumps(addTab)
    # for key, value in addTab.items():
    #     tmp_vr.append(value)
    dbNewUsrID = db.reference('addMember/NewUsrID')
    dbappRq = db.reference('addMember/appRequest')
    NewUsrID = dbNewUsrID.get()
    appRq = dbappRq.get()
    print("NewUsrID",NewUsrID)
    print("appRequest",appRq)
    return str(addTab),NewUsrID,appRq
def ReverseDay(day = ''):
    # 2020-08-27
    ls_par = day.split('-')
    output = ''
    for i in range (0, len(ls_par)):
        if (output != ''):
            output = output + '-' + ls_par[len(ls_par)-1-i]
        else:
            output = output + ls_par[len(ls_par)-1-i]
    print(output)
    return output
def SendData(UsrID=''):
    today = ReverseDay(str(datetime.datetime.today()).split(" ")[0])
    # Send data
    diemdanh = db.reference(str('diemdanh/'+today))
    print("str('diemdanh/'+today)",str('diemdanh/'+today))
    # diemdanh = db.reference(str('diemdanh/13-08-2020'))
    rq = diemdanh.child(UsrID)
    now = datetime.datetime.now()
    timeEnter = '0'
    timeExit = '0'
    hour = int(str(now).split(' ')[1].split(':')[0])
    this_time = str(now).split(' ')[1].split('.')[0]
    print(this_time)
    # print('hour = ',hour)
    print('this time',this_time)
    if (hour > 8 and hour < 10):
        timeEnter = this_time
        result = rq.update({'timeEnter':timeEnter})
    elif (hour > 16 and hour < 18):
        timeExit = this_time
        result = rq.update({'timeExit':timeExit})
def Authen(uid = []):
    i = 0
    list_UserID = []
    list_UserRFID = []
    str_uid = str(uid)
    list_UserID,list_UserFaceID = GetAuthenData()
    print(list_UserFaceID)
    try: 
        for ls in list_UserFaceID:
            cmp_stt = str(ls).find(str_uid)
            if (cmp_stt != -1):
                result = 1
                break
            else:
                result = 0
                i = i+1
        if (result == 1):
            print("ACCESS GRANTED!!!")
        else:
            print("ACESS DENIED")
        print("\ni = ",i)
        print(list_UserID)
        UsrID = list_UserID[i]
    except:
        print("       ")
        UsrID = ''
    i= 0
    return result,UsrID
def GetAuthenData():
    # FireBase_Com.Init()
    list_UserID = []
    list_UserFaceID = []
    list_UserInfo = []
    #Get data
    employees = db.reference('employees')
    dayTab = employees.get()
    json_dayTab = json.dumps(dayTab)
    for key, value in dayTab.items():
        list_UserID.append(key)
        list_UserInfo.append(value)
    for id in list_UserID:
        db_faceid = db.reference(str('employees/' + str(id) + '/FaceID'))
        faceid_ = db_faceid.get()
        list_UserFaceID.append(faceid_)
    return list_UserID,list_UserFaceID
def UpdateFaceInfo(UsrID = '', FaceID = ''):
    # FireBase_Com.Init()
    employees = db.reference(str('employees/'+UsrID))
    result = employees.update({'FaceID':FaceID})
def PushDataToFirebase(FaceID = ''):
    # Connect to firebase
    # cred = credentials.Certificate("deviot-may-cham-cong-firebase-adminsdk-4j9vd-c20046ba51.json")
    # firebase_admin.initialize_app(cred,{'databaseURL':'https://deviot-may-cham-cong.firebaseio.com'})
    addTab,NewUsrID,appRq = AddNew()
    if (appRq == 2):
        UpdateFaceInfo(NewUsrID,FaceID)
    else:
        result,UsrID = Authen(FaceID)
        if (result == 1):
            SendData(UsrID)
            print("Access Granted")
        else:
            print("Access Denied")
    db_reset_appRq = db.reference('addMember')
    rs = db_reset_appRq.update({'appRequest':0})
def GetImageID():
    dbImgID = db.reference('addMember/idAnh')
    idAnh = dbImgID.get()
    return idAnh
if __name__ == "__main__":
    # PushDataToFirebase("xyz")
    GetImageID()

# End of Hieu's code
# -----------------------------------------------------------------

# new_img='v_tuan.jpg'
# new_txt='V_TUAN.txt'
# classNames = ['a_tuan', 'd_tuan', 'giang', 'hieu',
#                'huong', 'tung','v_tuan']
# tentxt = ['/home/pi/face_recog/a_tuan.txt', '/home/pi/face_recog/d_tuan.txt', '/home/pi/face_recog/giang.txt',
#           '/home/pi/face_recog/hieu.txt', '/home/pi/face_recog/huong.txt','/home/pi/face_recog/tung.txt','/home/pi/face_recog/v_tuan.txt']

# file_path='/home/pi/face_recog/data'
# url='https://scontent.fhph1-2.fna.fbcdn.net/v/t1.15752-0/p280x280/118153126_973863373026959_6770969568872295849_n.jpg?_nc_cat=105&_nc_sid=b96e70&_nc_ohc=oaIndy_1x9kAX-5UHVg&_nc_ht=scontent.fhph1-2.fna&_nc_tp=6&oh=5da57d8f75ddcacd1f5d5e38d8fecbe2&oe=5F655CD7'
# full_path=os.path.sep.join([file_path, new_img])
# urllib.request.urlretrieve(url,full_path)

# # import face_recognition
# path = '/home/pi/face_recog/data'

# path_img=os.path.sep.join([path, new_img])
# Img = cv2.imread(path_img,1)
# img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
# encode = face_recognition.face_encodings(img)[0]
# np.savetxt(new_txt, encode)
# print('da save')


# # path = 'data/'
# # images = []
# # myList = os.listdir(path)
# # print(myList)
# # for cl in myList:
# #     curImg = cv2.imread(f'{path}/{cl}')
# #     images.append(curImg)
# # tentxt=['a_tuan.txt', 'd_tuan.txt', 'giang.txt', 'hieu.txt','huong.txt','tung.txt','v_tuan.txt']
# #
# # def findEncodings(images,tentxt):
# #     for (img, tentxt2) in zip(images,tentxt):
# #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #         encode = face_recognition.face_encodings(img)[0]
# #         np.savetxt(tentxt2,encode)
# # encodeListKnown = findEncodings(images,tentxt)

# nameList = []
# # vs = VideoStream(src=1).start()
# vs = VideoStream(usePiCamera=True).start()
# nameList = []
# time.sleep(2.0)
# tt1 = True

# encodeListKnown = []
# for i2 in tentxt:
#     i3 = np.loadtxt(i2)
#     encodeListKnown.append(i3)
# encodeListKnown = np.array(encodeListKnown)


# while True:
#     name = ''
#     while True:
#         frame = vs.read()
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
#         rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
#                                           minNeighbors=5, minSize=(30, 30),
#                                           flags=cv2.CASCADE_SCALE_IMAGE)
#         boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#         boxes = np.array(boxes)

#         if (len(boxes) != 1):
#             cv2.putText(frame, 'khong co ai', (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
#                        1, (0,0 , 255), 2)
#             cv2.imshow('frame',frame)
#             key = cv2.waitKey(1)& 0xFF
#             continue
#         else:
#             a = int(boxes[:, 0])
#             b = int(boxes[:, 1])
#             c = int(boxes[:, 2])
#             d = int(boxes[:, 3])
#             face=frame[b:d,a:c]
#             face=np.array(face)
#             # print(type(face))
#             (fh,fw)=face.shape[:2]
#             # print(fw)
#             if fw < 80:
#                 continue

#             # start = time.time()

#             cv2.putText(frame, 'STOP', (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
#                        1, (0,0 , 255), 2)
#             cv2.imshow('frame',frame)
#             key = cv2.waitKey(1)& 0xFF
#             time.sleep(1)
#             frame=vs.read()
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
#             rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
#                                               minNeighbors=5, minSize=(30, 30),
#                                               flags=cv2.CASCADE_SCALE_IMAGE)
#             boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#             boxes = np.array(boxes)

#             if (len(boxes) == 1):
#                 a = int(boxes[:, 0])
#                 b = int(boxes[:, 1])
#                 c = int(boxes[:, 2])
#                 d = int(boxes[:, 3])
#                 boxes1 = [(a, b, c, d)]
#                 break
#             else:
#                 continue

#     encodesCurFrame = face_recognition.face_encodings(frame, boxes1)
#     matches = face_recognition.compare_faces(encodeListKnown, encodesCurFrame, tolerance=0.5)
#     faceDis = face_recognition.face_distance(encodeListKnown, encodesCurFrame)
#     matchIndex = np.argmin(faceDis)
#     if matches[matchIndex]:
#         name = classNames[matchIndex].upper()
#         millis=str(round(time.time()*1000))
#         ID=name+millis
#         if name=='':
#             continue
#         with open('/home/pi/face_recog/lich_cham_cong.txt', 'a') as f:
#             # myDataList = f.readlines()
#             if name not in nameList:
#                 nameList.append(name)
#                 f.writelines(f'{name}\n')

#     while(True):
#         frame = vs.read()
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
#         rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
#                                           minNeighbors=5, minSize=(30, 30),
#                                           flags=cv2.CASCADE_SCALE_IMAGE)
#         boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#         boxes = np.array(boxes)
#         # end = time.time()
#         # tg = end - start
#         # print(tg)

#         if (len(boxes) == 1):
#             a = int(boxes[:, 0])
#             b = int(boxes[:, 1])
#             c = int(boxes[:, 2])
#             d = int(boxes[:, 3])
#             cv2.putText(frame, name, (d + 6, c - 6), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 0), 2)
#             cv2.rectangle(frame, (d, a), (b, c), (0, 255, 0), 2)
#             cv2.imshow('frame', frame)
#             cv2.waitKey(1)
#         else:
#             break


# from imutils.video import VideoStream
# import time
# import cv2
# import numpy as np
# # from datetime import datetime
# import os
# import urllib.request
# import face_recognition
#
# new_img='v_tuan.jpg'
# new_txt='V_TUAN.txt'
# classNames = ['a_tuan', 'd_tuan', 'giang', 'hieu',
#                'huong', 'tung','v_tuan']
# tentxt = ['a_tuan.txt', 'd_tuan.txt', 'giang.txt',
#           'hieu.txt', 'huong.txt','tung.txt','v_tuan.txt']
#
# file_path='data'
# url='https://scontent.fhph1-2.fna.fbcdn.net/v/t1.15752-0/p280x280/118153126_973863373026959_6770969568872295849_n.jpg?_nc_cat=105&_nc_sid=b96e70&_nc_ohc=oaIndy_1x9kAX-5UHVg&_nc_ht=scontent.fhph1-2.fna&_nc_tp=6&oh=5da57d8f75ddcacd1f5d5e38d8fecbe2&oe=5F655CD7'
# full_path=os.path.sep.join([file_path, new_img])
# urllib.request.urlretrieve(url,full_path)
#
# # import face_recognition
# path = 'data'
#
# path_img=os.path.sep.join([path, new_img])
# Img = cv2.imread(path_img,1)
# img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
# encode = face_recognition.face_encodings(img)[0]
# np.savetxt(new_txt, encode)
# print('da save')
#
#
# # path = 'data/'
# # images = []
# # myList = os.listdir(path)
# # print(myList)
# # for cl in myList:
# #     curImg = cv2.imread(f'{path}/{cl}')
# #     images.append(curImg)
# # tentxt=['a_tuan.txt', 'd_tuan.txt', 'giang.txt', 'hieu.txt','huong.txt','tung.txt','v_tuan.txt']
# #
# # def findEncodings(images,tentxt):
# #     for (img, tentxt2) in zip(images,tentxt):
# #         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# #         encode = face_recognition.face_encodings(img)[0]
# #         np.savetxt(tentxt2,encode)
# # encodeListKnown = findEncodings(images,tentxt)
#
# nameList = []
# vs = VideoStream(src=1).start()
# # vs = VideoStream(usePiCamera=True).start()
# nameList = []
# time.sleep(2.0)
# tt1 = True
#
# encodeListKnown = []
# for i2 in tentxt:
#     i3 = np.loadtxt(i2)
#     encodeListKnown.append(i3)
# encodeListKnown = np.array(encodeListKnown)
#
#
# while True:
#     name = ''
#     while True:
#         t = 0
#         t1=0
#         frame = vs.read()
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#         rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
#                                           minNeighbors=5, minSize=(30, 30),
#                                           flags=cv2.CASCADE_SCALE_IMAGE)
#         boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#         boxes = np.array(boxes)
#
#         if (len(boxes) != 1):
#             cv2.putText(frame, 'khong co ai', (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
#                        1, (0,0 , 255), 2)
#             cv2.imshow('frame',frame)
#             key = cv2.waitKey(1)& 0xFF
#             continue
#         else:
#             a = int(boxes[:, 0])
#             b = int(boxes[:, 1])
#             c = int(boxes[:, 2])
#             d = int(boxes[:, 3])
#             face=frame[b:d,a:c]
#             face=np.array(face)
#             # print(type(face))
#             (fh,fw)=face.shape[:2]
#             # print(fw)
#             if fw < 80:
#                 continue
#
#             # start = time.time()
#
#             cv2.putText(frame, 'STOP', (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
#                        1, (0,0 , 255), 2)
#             cv2.imshow('frame',frame)
#             key = cv2.waitKey(1)& 0xFF
#             time.sleep(1)
#             frame=vs.read()
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#             rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
#                                               minNeighbors=5, minSize=(30, 30),
#                                               flags=cv2.CASCADE_SCALE_IMAGE)
#             boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#             boxes = np.array(boxes)
#
#             if (len(boxes) == 1):
#                 a = int(boxes[:, 0])
#                 b = int(boxes[:, 1])
#                 c = int(boxes[:, 2])
#                 d = int(boxes[:, 3])
#                 boxes1 = [(a, b, c, d)]
#                 break
#             else:
#                 continue
#
#     encodesCurFrame = face_recognition.face_encodings(frame, boxes1)
#     matches = face_recognition.compare_faces(encodeListKnown, encodesCurFrame, tolerance=0.5)
#     faceDis = face_recognition.face_distance(encodeListKnown, encodesCurFrame)
#     # print(min(faceDis))
#     matchIndex = np.argmin(faceDis)
#     if matches[matchIndex]:
#         name = classNames[matchIndex].upper()
#         millis=str(round(time.time()*1000))
#         ID=name+millis
#         # print(name1)
#         if name=='':
#             continue
#         # print(name)
#         with open('lich_cham_cong.txt', 'a') as f:
#             # myDataList = f.readlines()
#             if name not in nameList:
#                 nameList.append(name)
#                 f.writelines(f'{name}\n')
#
#     while(True):
#         frame = vs.read()
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#         rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
#                                           minNeighbors=5, minSize=(30, 30),
#                                           flags=cv2.CASCADE_SCALE_IMAGE)
#         boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#         boxes = np.array(boxes)
#         # end = time.time()
#         # tg = end - start
#         # print(tg)
#
#         if (len(boxes) == 1):
#             a = int(boxes[:, 0])
#             b = int(boxes[:, 1])
#             c = int(boxes[:, 2])
#             d = int(boxes[:, 3])
#             cv2.putText(frame, name, (d + 6, c - 6), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 0), 2)
#             cv2.rectangle(frame, (d, a), (b, c), (0, 255, 0), 2)
#             cv2.imshow('frame', frame)
#             cv2.waitKey(1)
#         else:
#             break

