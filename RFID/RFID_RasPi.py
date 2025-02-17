import os
import threading
from threading import Thread
import RPi.GPIO as GPIO
# import MFRC522
from pirc522 import RFID
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from requests.packages import urllib3
import datetime
from time import sleep
import signal
# from flask import Flask, render_template
from smbus2 import SMBus
from mlx90614 import MLX90614
# from firebase import firebase
# Variable define 
hooman = ''
run = True
# -----------------------------------
rdr = RFID()
util = rdr.util()
util.debug = True
GPIO.setmode(GPIO.BOARD)
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()
signal.signal(signal.SIGINT, end_read)
class Tools():
    def ReadIMGFile(path_to_file = ''):
        result = ''
        try:
            file = open(path_to_file,'r')
            line = file.readline()
            result = line
            os.remove(path_to_file)
            FaceIDReady = 1
        except:
            FaceIDReady = 0
        FaceIDReady = 0
        return FaceIDReady,result
    def GetKeyFromString(stringg = ''):
        uid_0 = int(stringg.split('-')[0])
        uid_1 = int(stringg.split('-')[1])
        uid_2 = int(stringg.split('-')[2])
        uid_3 = int(stringg.split('-')[3])
        uid_4 = int(stringg.split('-')[4])
        uid = [uid_0,uid_1,uid_2,uid_3,uid_4]
        return uid
    def GetStringFromList(uid_list = []):
        txt_uid = str(str(uid_list[0]) + '-' + str(uid_list[1]) + '-' + str(uid_list[2]) + '-' + str(uid_list[3]) + '-' + str(uid_list[4]))
        txt_uid = txt_uid.replace('[','').replace(']','')
        return txt_uid
class RFID:    
    def Init():
        # Hook the SIGINT
        GPIO.setmode(GPIO.BOARD)
        signal.signal(signal.SIGINT, end_read)
        # Create an object of the class MFRC522
        # MIFAREReader = MFRC522.MFRC522()
        run = True
        rdr = RFID()
        util = rdr.util()
        util.debug = True
        # return MIFAREReader
    def Authen(uid = []):
        i = 0
        list_UserID = []
        list_UserRFID = []
        str_uid = str(uid)
        list_UserID,list_UserRFID = FireBase_Com.GetAuthenData()
        try: 
            for ls in list_UserRFID:
                cmp_stt = str(ls).find(str_uid)
                if (cmp_stt != -1):
                    result = 1
                    break
                else:
                    result = 0
                    i = i+1
            if (result == 1):
                print("ACCESS GRANTED!!!")
                UsrID = list_UserID[i]
            else:
                print("ACESS DENIED")
                UsrID = ''
            # print("\ni = ",i)
            # print(list_UserID)
        except Exception as e:
            print(e)
            UsrID = ''
        i= 0
        return result,UsrID
    def AuthenFace(FaceID = []):
        i = 0
        list_UserID = []
        list_UserInfo = []
        list_UserID,list_UserInfo = FireBase_Com.GetAuthenData()
        for ls in list_UserInfo:
            cmp_stt = str(ls).find(FaceID)
            if (cmp_stt != -1):
                result = 1
            else:
                result = 0
                i = i+1
        # if (uid[0] == key[0] and uid[1] == key[1] and uid[2] == key[2] and uid[3] == key[3] and uid[4] == key[4]):
        #     result = 0
        UsrID = list_UserID[i]
        return result,UsrID
    def RFIDTask():
        while (run == True):
            AddSig,NewUsrID,appRq = FireBase_Com.AddNew()
            # print("appRq = ",appRq)
            if (appRq == 0 or appRq == 1):
                print("Looking for card...")
                # Scan for cards    
                # rdr.wait_for_tag()
                (error, data) = rdr.request()
                # If a card is found
                # print('\nError = ',error)
                if (not error):
                    print("\nDetected: " + format(data, "02x"))
                # Get the UID of the card
                (error, uid) = rdr.anticoll()
                # If we have the UID, continue
                if (not error):
                    # Print UID
                    print ("Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3],uid[4]))
                    # This is the default key for authentication
                    # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                    key = [0xAB,0xEB,0xD2,0xFF,0x22,0xB0]
                    # Select the scanned tag
                    print("Setting tag")
                    util.set_tag(uid)
                    # Authenticate
                    if (appRq == 0): #RFID Card
                        txt_uid = Tools.GetStringFromList(uid)
                        AutStt,UsrID = RFID.Authen(txt_uid)
                        print("\nAutStt = ",AutStt)
                        if (AutStt == 1):
                            print("Sending data...")
                            FireBase_Com.SendData(txt_uid,UsrID)
                    elif (appRq == 1): #Add Card
                        print("Add new id card")
                        FireBase_Com.UpdateCardInfo(NewUsrID,Tools.GetStringFromList(uid))
            # elif (appRq == 2):
            #     print("Add new Face ID")
            #     FireBase_Com.UpdateFaceInfo(NewUsrID,FaceID)
class FireBase_Com:
    def Init():
        # cred = credentials.Certificate("test-firebase-7a605-firebase-adminsdk-ge9h3-e2a3245f8b.json")
        # firebase_admin.initialize_app(cred,{'databaseURL':'https://test-firebase-7a605.firebaseio.com'})
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
        # print("NewUsrID",NewUsrID)
        # print("appRequest",appRq)
        return str(addTab),NewUsrID,appRq
    def SendData(txt_uid='',UsrID=''):
        # Init connection
        # cred = credentials.Certificate("test-firebase-7a605-firebase-adminsdk-ge9h3-e2a3245f8b.json")
        # firebase_admin.initialize_app(cred,{'databaseURL':'https://test-firebase-7a605.firebaseio.com'})
        # FireBase_Com.Init()
        today = str(datetime.datetime.today()).split(" ")[0]
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
        # print('hour = ',hour)
        print('this time',this_time)
        if (hour > 8 and hour < 10):
            timeEnter = this_time
            result = rq.update({'timeEnter':timeEnter})
        elif (hour > 16 and hour < 18):
            timeExit = this_time
            result = rq.update({'timeExit':timeExit})
    def GetAuthenData():
        # FireBase_Com.Init()
        list_UserID = []
        list_UserRFID = []
        list_UserInfo = []
        #Get data
        employees = db.reference('employees')
        dayTab = employees.get()
        json_dayTab = json.dumps(dayTab)
        for key, value in dayTab.items():
            list_UserID.append(key)
            list_UserInfo.append(value)
        for id in list_UserID:
            db_rfid = db.reference(str('employees/' + str(id) + '/rfid'))
            rfid_ = db_rfid.get()
            list_UserRFID.append(rfid_)
        return list_UserID,list_UserRFID
    def UpdateCardInfo(UsrID = '', CardID = ''):
        # FireBase_Com.Init()
        employees = db.reference(str('employees/'+UsrID))
        result = employees.update({'rfid':CardID})
        print("Add New Card: Done")
        # Set appRequest to 0
        db_reset_appRq = db.reference('addMember')
        rs = db_reset_appRq.update({'appRequest':0})
    def UpdateFaceInfo(UsrID = '', FaceID = ''):
        # FireBase_Com.Init()
        employees = db.reference(str('employees/'+UsrID))
        result = employees.update({'FaceID':FaceID})
    def TestEvent():
        ttt = db.reference('addMember/appRequest').Event.data
        print(ttt)
class GetTemperature:
    def ReadSensor(sensor):
        # Init MLX90614 sensor
        # print('Raw data chanel 1',sensor.read_temp(reg = 0x04))
        # print('Raw data chanel 2',sensor.read_temp(reg = 0x05))
        # print('Ambient temperature',sensor.read_temp(reg = 0x06))
        # print('Object 1 temperature',sensor.read_temp(reg = 0x07))
        # print('Object 2 temperature',sensor.read_temp(reg = 0x08))
        AmbTemp = sensor.read_temp(reg = 0x06)
        ObjTemp = sensor.read_temp(reg = 0x07)
        sleep(0.01)
        return AmbTemp,ObjTemp
    def EstimateRealObjectTemp(AmbientTemp,ObjectTemp):
        AmbReferList = [18.1,20.7,23.5,27.5,34.0]
        ObjectReferList= [29.5,30.2,31.5,33.5,34.6]
        DeltaTemp = []
        EstimatedTemp = 0
        for i in range (0,len(AmbReferList)-1):
            dt = 36.5 - ObjectReferList[i]
            DeltaTemp.append(dt)
        if (AmbientTemp < 38 and AmbientTemp >= 35):
            EstimatedTemp = ObjectTemp
            # print("\nDebug line -1111")
            return EstimatedTemp
        elif (AmbientTemp < 18.1 or AmbientTemp >= 38):
            EstimatedTemp = -1000
            # EstimatedTemp = -1000
            return EstimatedTemp
        else:
            if (ObjectTemp < 29.5):
                EstimatedTemp = ObjectTemp
                # print("\nDebug line 0000")
                return EstimatedTemp
            elif (ObjectTemp >= 37.5):
                EstimatedTemp = ObjectTemp
                return EstimatedTemp
            else:
                # print("\nDebug line 1111")
                UpperLimit = 0
                RangeIndex = 0
                for m in range(0, len(AmbReferList)):
                    try:
                        tmpUpperLimit = (AmbReferList[m+1] - AmbReferList[m])/2 + AmbReferList[m]
                        # print("\ntmpUpperLimit = ",tmpUpperLimit)
                        # print("\nAmbientTemp = ",AmbientTemp)
                        # print("\nAmbReferList[m] = ",AmbReferList[m])
                        if (AmbientTemp >= AmbReferList[m] and AmbientTemp < UpperLimit):
                            UpperLimit = tmpUpperLimit
                            RangeIndex = m
                            # print("\nRangeIndex = m = ",m)
                            break
                    except IndexError:
                        RangeIndex = len(AmbReferList)
                try: 
                    # print("\nDebug line try")
                    EstimatedTemp = ObjectTemp + DeltaTemp[RangeIndex]
                    # print("\nRangeIndex = ",RangeIndex)
                    # print("\n Delta Temp = ",DeltaTemp[RangeIndex])
                    return EstimatedTemp
                except:
                    # print("\nDebug line 3333")
                    EstimatedTemp = DeltaTemp[len(DeltaTemp)-1] + ObjectTemp
                    return EstimatedTemp
        return EstimatedTemp
    def run():
        bus = SMBus(1)
        ListAmbTemp = []
        ListObjTemp = []
        sensor = MLX90614(bus, address=0x5A)
        SumAmbTemp = 0
        SumObjTemp = 0
        AmbTemp,ObjTemp = GetTemperature.ReadSensor(sensor)
        # print("\nRaw Ambients ",AmbTemp)
        # print("\nRaw Object ",ObjTemp)
        for i in range(0,10):
            AmbTemp,ObjTemp = GetTemperature.ReadSensor(sensor)
            SumAmbTemp = SumAmbTemp + AmbTemp
            SumObjTemp = SumObjTemp + ObjTemp
        # Get average value
        AvgAmbTemp = SumAmbTemp/10
        AvgObjTemp = SumObjTemp/10
        print("\nAmbient Temperature: ", round(AvgAmbTemp,1),"*C")
        # print("\nObject Temperature: ", AvgObjTemp)
        EstimatedTemp = GetTemperature.EstimateRealObjectTemp(AvgAmbTemp,AvgObjTemp)
        ErrorIndex = 0
        if (EstimatedTemp == -1000):
            ErrorIndex = ErrorIndex + 1
            if (ErrorIndex >= 3):
                print("\nOut of Measurement Range, the Ambient Temperature is too hot or too cold")
        elif (EstimatedTemp > 33):
            print("\nObject Temperature: ",round(EstimatedTemp-0.5,1),"*C")
            ErrorIndex = 0
        bus.close()
if __name__ == "__main__":
    print("Starting...")
    # FireBase_Com.Init()
    # RFID.RFIDTask()
    while(1):
        GetTemperature.run()
        sleep(1)

