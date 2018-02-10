import time
import manage_db
from pyfingerprint.pyfingerprint import PyFingerprint
import serial
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)
exitFact = False
while True:
    exitFact = False
    data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
    if(str(data) == "1"):
        arduino.writelines("1")
        while(True):
            data = arduino.readline()[:-2]
            if(str(data) != "0" and str(data) != ''):
                userId = int(data)
                # manage_db.update_work_clock_in(userId)
                userRow = manage_db.findUser(userId)
                if(userRow != 0):
                    arduino.writelines(str(userRow[1]).encode())
                    worklogStatus = manage_db.work_clock_in(userRow[0])
                    if(worklogStatus != "already clockin"):
                        time.sleep(2)
                        arduino.writelines((str(worklogStatus)))
                    else:
                        time.sleep(2)
                        arduino.writelines(str(worklogStatus))
                else:
                    arduino.writelines("not found")
                    time.sleep(1)
                    arduino.writelines("please try again")
                break

    if(str(data) == "2"):
        print(str(data))
        arduino.writelines("2")
        acCode = ""
        while(True):
            data = arduino.readline()[:-2]
            if(str(data) == "exit"):
                print("exit")
                exitFact = True
                break
            if(str(data) == "done"):
                break
            if(data):
                acCode = acCode + str(data)
        if(exitFact == False):
            print(acCode)
            user = manage_db.getNonUserActivated(acCode)
            arduino.writelines(user[1].encode())
            time.sleep(2)
            arduino.writelines(str(user[0]).encode())
            while(True):
                data = arduino.readline()[:-2]
                if (str(data) == "Enroll Done"):
                    print("Done")
                    manage_db.updateEnroll(manage_db.getArduinoId(),user[0])
                    break

# import time
# import socket
# import manage_db
# from pyfingerprint.pyfingerprint import PyFingerprint
#
# PI_IP = "169.254.193.226"
# ARDUINO_IP = "169.254.193.227"
# UDP_PORT = 8888
# MESSAGE = "Hello, World!"
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((PI_IP, UDP_PORT))
# while(True):
#     data, addr = sock.recvfrom(2048)
#     if(data):
#         if(data == "2" and manage_db.is_connected() == True):
#             print(data)
#             sock.sendto("ready", (ARDUINO_IP, UDP_PORT))
#             while(True):
#                 data, addr = sock.recvfrom(2048)
#                 if(data):
#                     if(int(data) == 360):
#                         break
#                     if(int(data) != 360):
#                         user = manage_db.getActivatedCode(int(data))
#                         print(str(user[1]))
#                         sock.sendto(str(user[1]), (ARDUINO_IP, UDP_PORT))
#                         break
#             data, addr = sock.recvfrom(2048)
#             if(data):
#                 if(str(data) == "successful"):
#                     manage_db.updateEnroll(user[0])





# from werkzeug.wrappers import Request, Response
#
# @Request.application
# def application(request):
#     finger = request.args.get('params')
#     finger = str(finger).replace("'","")
#     print(finger)
#     return Response("Parameter: %s" % request.args.get('finger'))
#
# if __name__ == '__main__':
#     from werkzeug.serving import run_simple
#     run_simple('169.254.193.226', 4000, application)


# data, addr = sock.recvfrom(2048)
# data = "01,65,16,93,00,FF,FE,C0,7E,C0,0E,80,06,80,02,80,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,80,00,80,00,C0,00,E0,06,00,00,00,00,00,00,00,00,00,00,00,00,00,00,4F,1E,18,9A,47,B8,C0,FB,43,3A,D8,DB,2B,9D,EF,01,FF,FF,FF,FF,02,00,82,47,A0,C3,72,4B,A1,D9,F2,40,AA,C2,18,41,2C,99,F8,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,09,19,EF,01,FF,FF,FF,FF,02,00,82,03,01,61,17,8F,00,FF,FE,FF,FE,F0,7E,E0,1E,E0,06,C0,02,C0,00,C0,00,80,00,80,00,80,00,80,00,80,00,C0,00,C0,00,E0,02,F8,06,00,FF,FF,FF,FF,FF,FF,FF,FF,FF,FF,FF,00,00,00,00,3B,12,59,FE,14,A5,03,7E,4E,2E,2B,7E,29,B1,99,BE,38,B4,C3,3E,65,35,55,5E,60,BD,D5,9E,30,BF,59,1E,5F,C3,AA,7E,5A,AC,55,9F,17,30,82,BF,48,BF,40,3F,4A,97,2C,7C,48,9A,57,DC,67,19,40,BA,75,B5,D3,BA,6C,19,D6,7B,75,B3,6B,73,31,5E,EF,01,FF,FF,FF,FF,08,00,82,46,B5,40,3B,22,3E,42,78,42,37,59,19,20,3F,59,13,20,16,43,6E,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,05,B7"
#
# fingerLine = [line.rstrip('\n') for line in open('/home/developer/Desktop/localDB/user_finger1')]
# fingerLine = str(fingerLine).replace("[", "")
# fingerLine = str(fingerLine).replace("'", "")
# fingerLine = str(fingerLine).replace("]", "")
# fingerLine = str(fingerLine).split(",")
# index_finger = array.array('i', (0 for i in range(0, 512)))
# input_finger = array.array('i', (0 for i in range(0, 512)))
# data = str(data).split(",")
# count = 0
# print(len(data))
# while (count < len(data)):
#     input_finger[count] = int(data[count], 16)
#     count += 1
# print(input_finger)
# # input_finger2 = array.array('i', (0 for i in range(0, len(fingerLine)-1)))
# # print(len(data))
# # for i in range(len(data) -1):
# #     if(i < 200 and data[i] != ''):
# #         input_finger2[i] = int(data[i],16)
# # print(input_finger2)
# # file = open("/home/developer/Desktop/section1", "w")
# # file.write(str(input_finger2))
# # file.close()



# try:
#     f = PyFingerprint('/dev/ttyUSB1', 57600, 0xFFFFFFFF, 0x00000000)
#
#     if (f.verifyPassword() == False):
#         raise ValueError('The given fingerprint sensor password is wrong!')
#
# except Exception as e:
#     print('The fingerprint sensor could not be initialized!')
#     print('Exception message: ' + str(e))
#     exit(1)
#
# print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))
#
# try:
#     count = 1
#     while (count < 120):
#         index_finger[count-1] = int(fingerLine[count])
#         count += 1
#     print(index_finger)
#     f.uploadCharacteristics(0x02, index_finger)
#
#     print('waiting for finger')
#     f.uploadCharacteristics(0x01, input_finger)
#     f.convertImage(0x01)
#
#     if (f.compareCharacteristics() != 0):
#
#         print("Status:" + str(f.compareCharacteristics()/3))
#     else:
#         print("Authorization: Failed. Please Try Again")
#
# except Exception as e:
#     print('Operation failed!')
#     print('Exception message: ' + str(e))
#     exit(1)
#
# data = None