import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from pyfingerprint.pyfingerprint import PyFingerprint
import array
import string

# path = "LOCAL_DB_DIR"
# host = "HOST_URL"
# mySqlUser = "MYSQL_USERNAME"
# mySqlPassword = "MYSQL_PASSWORD"

def findUser(userId):
    if (is_connected() == False):
        lines = [line.rstrip('\n') for line in open(path + 'user')]
        for line in lines:
            spLine = line.split(',')
            if (spLine[0] == str(userId)):
                return spLine
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)
        if (is_connected()):
            cursor = conn.cursor()
            query = ("SELECT * FROM `user` WHERE id = " + str(userId))
            cursor.execute(query)
            result = cursor.fetchall()
            if(len(result) == 0):
                return 0
            conn.close()
            return result[0] #return user tuple from db

    except Error as e:
        print(e)
        return False

def updateEnroll(fingerprint,userId):
    query = ("UPDATE `activated` set activate_status = 1 where fingerprint_id = " + str(fingerprint) + " and user_id =" + str(userId))
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)
        print(query)
        if(is_connected()):
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()

    except Error as e:
        print(e)
        return False

def getArduinoId():
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)

        if conn.is_connected():
            cursor = conn.cursor()
            query = ("SELECT * FROM `fingerprint` WHERE fingerprint_id = 'arduino'")
            cursor.execute(query)
            result = cursor.fetchone()
            if(len(result) == 0):
                return 0
            conn.close()
            return result[0]

    except Error as e:
        print(e)
        return False

def getNonUserActivated(activatedCode):
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)

        if conn.is_connected():
            cursor = conn.cursor()
            query = ("SELECT * FROM `user` WHERE activated_code = " + str(activatedCode))
            cursor.execute(query)
            result = cursor.fetchone()
            if(len(result) == 0):
                return 0
            conn.close()
            return result

    except Error as e:
        print(e)
        return False

# def getHighestId():
#     try:
#         conn = mysql.connector.connect(host=host,
#                                        database='attendance',
#                                        user=mySqlUser,
#                                        password=mySqlPassword)
#
#         if conn.is_connected():
#             cursor = conn.cursor()
#             query = ("SELECT max(finger) FROM attendance.user")
#             cursor.execute(query)
#             result = cursor.fetchone()[0]
#             if(result == None):
#                 return 1
#             conn.close()
#             return result

    except Error as e:
        print(e)
        return False

def work_clock_in(userId):
    nowTime = str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":00"
    nowSec = datetime.now().hour * 3600 + datetime.now().minute * 60
    worklogLines = [line.rstrip('\n') for line in open(path + 'worklog')]
    status = ""
    for worklogLine in worklogLines:
        worklogLine = str(worklogLine).split(",")
        if(worklogLine[1] == str(userId) and worklogLine[2] != "waiting"):
            status = "already clockin"
            break
        if(worklogLine[1] == str(userId) and worklogLine[2] == "waiting"):
            lines = [line.rstrip('\n') for line in open(path + 'section')]
            for line in lines:
                spLine = line.split(',')
                if (spLine[2] == userId):
                    if(int(spLine[4]) > 34201):
                        break
                    if(int(spLine[4]) < 34201):
                        if(nowSec < int(spLine[4])):
                            status = "ontime"
                        if(nowSec > int(spLine[4])):
                            status = "late"
    if(status == ""):
        if(nowSec < 34201):
            status = "ontime"
        else:
            status = "late"
    if(status != "already clockin"):
        update_work_clock_in(userId,status)
    return status


# def work_clock_in(finger):
#     try:
#         f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
#
#         if (f.verifyPassword() == False):
#             raise ValueError('The given fingerprint sensor password is wrong!')
#
#     except Exception as e:
#         print('The fingerprint sensor could not be initialized!')
#         print('Exception message: ' + str(e))
#         exit(1)
#
#     try:
#         f.getTemplateIndex(0)
#         lines = [line.rstrip('\n') for line in open(path + 'user')]
#         for line in lines:
#             spLine = line.split(',')
#             fingerLine = [line.rstrip('\n') for line in open(path + 'user_finger' + spLine[0])]
#             fingerLine = str(fingerLine).replace("[", "")
#             fingerLine = str(fingerLine).replace("'", "")
#             fingerLine = str(fingerLine).replace("]", "")
#             fingerLine = str(fingerLine).split(",")
#             index_finger = array.array('i', (0 for i in range(0, len(fingerLine) - 1)))
#             count = 0
#             while (count < len(fingerLine) - 1):
#                 index_finger[count] = int(fingerLine[count])
#                 count += 1
#             print(index_finger)
#             f.uploadCharacteristics(0x02, index_finger)
#
#             conpareFinger = array.array('i', (0 for i in range(0, len(finger) - 1)))
#             compareFingerStr = str(finger).split(",")
#             count2 = 0
#             while (count2 < len(compareFingerStr) - 1):
#                 conpareFinger[count2] = int(compareFingerStr[count2])
#                 count2 += 1
#             print(conpareFinger)
#             f.uploadCharacteristics(0x01, conpareFinger)
#             if (f.compareCharacteristics() != 0):
#                 print("Found user: " + spLine[1] + " " + spLine[2])
#                 worklogLines = [line.rstrip('\n') for line in open(path + 'worklog')]
#                 for worklogLine in worklogLines:
#                     worklogLine = str(worklogLine).split(",")
#                     if(worklogLine[1] == spLine[0] and worklogLine[2] == "waiting"):
#                         update_work_clock_in(finger,spLine)
#                         return True
#                     else:
#                         print("user already clocked in")
#                         return True
#             else:
#                 print("Authorization: Failed. Please Try Again")
#
#     except Exception as e:
#         print('Operation failed!')
#         print('Exception message: ' + str(e))
#         exit(1)

def update_work_clock_in(userId, status):
    # status = ""
    nowTime = str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":00"
    nowSec = datetime.now().hour * 3600 + datetime.now().minute * 60
    # userId = user[0]
    #
    # lines = [line.rstrip('\n') for line in open(path + 'worklog')]
    # for line in lines:
    #     spLine = line.split(',')
    #     if (spLine[1] == userId and spLine[2] == "waiting"):
    #         lines = [line.rstrip('\n') for line in open(path + 'section')]
    #         if(lines != None):
    #             for line in lines:
    #                 spLine = line.split(",")
    #                 if(int(spLine[4]) < 36000):
    #                     if(int(spLine[2]) == int(userId)):
    #                         if(nowSec < int(spLine[4])):
    #                             status = "ontime"
    #                             break
    #                         if(nowSec > int(spLine[4])):
    #                             status = "late"
    #                             break
    # if(status == ""):
    #     if(nowSec < 34201):
    #         status = "ontime"
    #     if(nowSec > 34201):
    #         status = "late"

    query = ("UPDATE work_log set status = '" + status + "', clock_in_time ='" + str(nowTime) + "', clock_in_sec = " + str(nowSec) + " where user_id = " + str(userId) + " and work_date = " + getTodayDate())
    print(query)
    if(is_connected()):
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
    if(is_connected() == False):
        wFile1 = open(path + "clockin_backup", "a")
        wFile1.write(query + "\n")
        wFile1.close()

    wFile = open(path + "worklog_backup", "w")
    lines = [line.rstrip('\n') for line in open(path + 'worklog')]
    for line in lines:
        spLine = line.split(',')
        if (str(spLine[1]) == str(userId)):
            wFile.write(str(spLine[0]) + "," + str(spLine[1]) + "," + status + "," + str(spLine[3]) + "," + str(
                spLine[4]) + "," + str(spLine[5]) + "," + str(spLine[6]) + "\n")
        if (str(spLine[1]) != str(userId)):
            wFile.write(
                str(spLine[0]) + "," + str(spLine[1]) + "," + str(spLine[2]) + "," + str(spLine[3]) + "," + str(
                    spLine[4]) + "," + str(spLine[5]) + "," + str(spLine[6]) + "\n")
    wFile.close()
    os.rename(path + "worklog_backup", path + "worklog")


def is_connected():
    try:
        iscon = False
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)

        if conn.is_connected():
            iscon = True
        conn.close()
        return iscon
    except Error as e:
        print(e)
        return False

def clock_in_to_text(sectionlogId,clock_in_sec):
    now = datetime.now()
    nowSec = (now.hour * 3600) + (now.minute * 60)
    status = ""
    if (nowSec < int(clock_in_sec) + 900):
        status = "present"
    if (nowSec > int(clock_in_sec) + 900):
        status = "late"
    query = ("UPDATE `section_log` set status = '" + status + "', clock_in_sec = '" + str(
        nowSec) + "' where id = " + str(sectionlogId))
    file = open(path + "clockin_backup","a")
    file.write(query + "\n")
    file.close()

    wFile = open(path + "sectionlog_backup", "w")
    lines = [line.rstrip('\n') for line in open(path + 'sectionlog')]
    for line in lines:
        spLine = line.split(',')
        if (spLine[0] == sectionlogId):
            wFile.write(str(spLine[0]) + "," + str(spLine[1]) + "," + status + "," + str(spLine[3]) + "," + str(
                spLine[4]) + "\n")
        if(spLine[0] != sectionlogId):
            wFile.write(str(spLine[0]) + "," + str(spLine[1]) + "," + str(spLine[2]) + "," + str(spLine[3]) + "," + str(
                spLine[4]) + "\n")
    wFile.close()
    os.rename(path + "sectionlog_backup",path + "sectionlog")
    return status

def clock_in(sectionlogId,clock_in_sec):
    global  conn
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)

        if conn.is_connected():
            print('Connected to MySQL database')
        now = datetime.now()
        nowSec = (now.hour * 3600) + (now.minute * 60)
        status = ""
        if(nowSec < int(clock_in_sec) + 900):
            status = "present"
        if(nowSec > int(clock_in_sec) + 900):
            status = "late"
        cursor = conn.cursor()
        query = ("UPDATE `section_log` set status = '" + status + "', clock_in_sec = '" + str(nowSec) + "' where id = " + str(sectionlogId))
        cursor.execute(query)
        conn.commit()
        conn.close()

        wFile = open(path + "sectionlog_backup", "w")
        lines = [line.rstrip('\n') for line in open(path + 'sectionlog')]
        for line in lines:
            spLine = line.split(',')
            if (str(spLine[0]) == str(sectionlogId)):
                wFile.write(str(spLine[0]) + "," + str(spLine[1]) + "," + status + "," + str(spLine[3]) + "," + str(
                    spLine[4]) + "\n")
            if (str(spLine[0]) != str(sectionlogId)):
                wFile.write(
                    str(spLine[0]) + "," + str(spLine[1]) + "," + str(spLine[2]) + "," + str(spLine[3]) + "," + str(
                        spLine[4]) + "\n")
        wFile.close()
        os.rename(path + "sectionlog_backup", path + "sectionlog")
        return status
    except Error as e:
        print(e)

def isAllActivated(userId):
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)

        if conn.is_connected():
            cursor = conn.cursor()
            query = ("SELECT * FROM `activated` WHERE user_id = " + str(userId) + " and activated_status = 0")
            cursor.execute(query)
            result = cursor.fetchall()
            if (len(result) == 0):
                return True
            conn.close()
            return False  # return user tuple from db

    except Error as e:
        print(e)
        return False

def registerFinger(userId):
    global conn
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)

        if conn.is_connected():
            print('Connected to MySQL database')
        cursor = conn.cursor()
        query = (
                "UPDATE `activated` set `activate_status` = b'1' where fingerprint_id = 1 and user_id = " + str(userId))
        print(query)
        cursor.execute(query)
        conn.commit()
        if isAllActivated(userId):
            query = (
                    "UPDATE `user` set `activated_code` = '4123153' where id = " + str(userId))
            cursor.execute(query)
            conn.commit()
        conn.close()
    except Error as e:
        print(e)

def getNowClass():
    global conn
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)

        if conn.is_connected():
            print('Connected to MySQL database')
        cursor = conn.cursor()
        query = ("SELECT * FROM `fingerprint` where fingerprint_id = 'pi-server'")
        cursor.execute(query)
        fingerprint_id = cursor.fetchone()[0]
        print(fingerprint_id)
        query = (
        "SELECT * FROM `section` WHERE sec_started " + getCurrentHour() + " and semester = " + getCurrentSemester() + " and year = "
            + getCurrentYear() + " and day = " + getDayOfWeek() + " and room_id = " + str(fingerprint_id))
        print(query)
        cursor.execute(query)
        row = cursor.fetchone()
        if(row == None):
            return None
        sectionRow = row
        print(sectionRow)
        query = "SELECT * FROM `subject` WHERE id = " + str(row[1])
        cursor.execute(query)
        row = cursor.fetchone()
        subjectRow = row
        query = "SELECT * FROM `section_log` WHERE section_id = " + str(sectionRow[0]) + " and work_date = " + getTodayDate()
        print(query)
        cursor.execute(query)
        row = cursor.fetchone()
        sectionLogRow = row
        query = "SELECT * FROM `user` WHERE id = " + str(
            sectionRow[2])
        cursor.execute(query)
        userRow = cursor.fetchone()
        result = [userRow, subjectRow, sectionRow, sectionLogRow]
        conn.close()

        return result

    except Error as e:
        print(e)


def getDetailFromLocalDB():
    lines = [line.rstrip('\n') for line in open(path + 'fingerprint_scanner')]
    fingerprint_id = ""
    for line in lines:
        spLine = line.split(",")
        if (spLine[1] == "pi-server"):
            fingerprint_id = spLine[0]

    lines = [line.rstrip('\n') for line in open(path + 'section')]
    sectionRow = []
    count = 0
    for line in lines:
        spLine = line.split(",")
        if (spLine[5] == getDayOfWeek() and calSecStarted(spLine[4]) and spLine[3] == fingerprint_id):
            sectionRow = spLine

    subjectRow = []
    if(sectionRow.__len__() != 0):
        lines = [line.rstrip('\n') for line in open(path + 'subject')]
        for line in lines:
            spLine = line.split(",")
            if (spLine[0] == sectionRow[1]):
                subjectRow = spLine

        userRow = ["", "", "", "", ""]
        lines = [line.rstrip('\n') for line in open(path + 'user')]
        for line in lines:
            spLine = line.split(",")
            if (spLine[0] == sectionRow[2]):
                file = open(path + "user_finger" + spLine[0], "r")
                fingerLine = file.readlines()
                userRow[0] = spLine[0]
                userRow[1] = spLine[1]
                userRow[2] = spLine[2]
                userRow[3] = spLine[3]
                userRow[4] = fingerLine

        sectionLogRow = []
        lines = [line.rstrip('\n') for line in open(path + 'sectionlog')]
        for line in lines:
            spLine = line.split(",")
            if (spLine[1] == sectionRow[0]):
                sectionLogRow = spLine
    if(sectionRow.__len__() == 0):
        userRow = None
        subjectRow = None
        sectionRow = None
        sectionLogRow = None
    result = [userRow, subjectRow, sectionRow, sectionLogRow]
    return result

def getUserByAcCode(code):
    global conn
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)

        if conn.is_connected():
            print('Connected to MySQL database')
        cursor = conn.cursor()
        query = ("SELECT * FROM `user` WHERE activated_code = " + str(code))
        print(query)
        cursor.execute(query)
        user = cursor.fetchone()
        if(user.__len__() == 0):
            print("no user found")
            conn.close()
            return None
        if(user.__len__() > 0):
            conn.close()
            return user

    except Error as e:
        print(e)

def getRoom(id):
    lines = [line.rstrip('\n') for line in open(path + 'fingerprint_scanner')]
    for line in lines:
        spLine = line.split(",")
        if (spLine[1] == id):
            return spLine[2]

def getCurrentSemester():
    currentMonth = datetime.now().month
    if(currentMonth < 10 and currentMonth > 4):
        return str(1)
    else:
        return str(2)

def getCurrentYear():
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    if (currentMonth < 4):
        currentYear = currentYear - 1;
    return str(currentYear)

def getCurrentHour():
    currentHour = datetime.now().hour
    if(currentHour < 12):
        return '< 43200'
    else:
        return '> 43200'
def getTodayDate():
    month = datetime.now().month
    if(month < 10):
        strmonth = "0" + str(month)
    return("'" + str(datetime.now().year) + '-' + strmonth + '-' + str(datetime.now().day) + "'")
def getDayOfWeek():
    dayOfWeek = datetime.now().weekday()
    return str(dayOfWeek)
def calSecStarted(secstart):
    currentHour = datetime.now().hour
    if(currentHour < 12 and int(secstart) < 43200):
        return True
    if(currentHour > 12 and int(secstart) > 43200):
        return True

def filter_out_junk(text):
    return ''.join(x for x in text if x in set(string.printable))


if __name__ == "__main__":
    print(work_clock_in(1))