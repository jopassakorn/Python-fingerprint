import schedule
import mysql.connector
import time
from mysql.connector import Error
import datetime as dt
from manage_db import *

def updateClockIn():
    while (is_connected() == False):
        print("try again in 5 seconds")
        time.sleep(5)
    if(is_connected()):
        try:
            conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)
            cursor = conn.cursor()
            lines = [line.rstrip('\n') for line in open(path + 'clockin_backup')]
            for line in lines:
                cursor.execute(line)
                print(line)
            conn.commit()
            conn.close()
            file = open(path + 'clockin_backup',"w")
            file.close()
        except Error as e:
            print(e)

def localUpdate():
    try:
        conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)
        while(conn.is_connected() == False):
            print("cannot connect to MySQL database")
            print("Connect again in 60 seconds")
            time.sleep(60)
        if conn.is_connected():
            print('Connected to MySQL database')
        cursor = conn.cursor()
        query = (
        "SELECT * FROM `section` WHERE semester = " + getCurrentSemester() + " and year = "
            + getCurrentYear() +" and started < '"+ str(getTomorrowDate()) +"' and ended > '" + str(getTomorrowDate()) + "' and day = " + getDayOfWeek())
        cursor.execute(query)
        file = open(path + "section", "w")
        for(sections) in cursor:
            print(sections)
            result = str(sections[0]) + "," + str(sections[1]) + "," + str(sections[2]) + "," + str(sections[3])\
                     + "," + str(sections[4]) + "," + str(sections[5]) + "," + str(sections[6]) + "," + \
                     str(sections[7]) + "," + str(sections[8]) + "," + str(sections[9]) + "\n"
            file.write(result)
        file.close()

        query = ("SELECT * FROM `subject`")
        cursor.execute(query)
        file = open(path + "subject", "w")
        for (subject) in cursor:
            result = str(subject[0]) + "," + str(subject[1]) + "," + str(subject[2]) + "," + str(
                subject[3] + "," + str(subject[4]) + "," + str(subject[5]) + "," + str(subject[6]) + "\n")
            file.write(result)
        file.close()

        query = ("SELECT * FROM `user`")
        cursor.execute(query)
        file = open(path + "user", "w")
        for (users) in cursor:
            userFinger = users[4]
            if(userFinger == ''):
                userFinger = '0'
            result = str(users[0]) + "," + str(users[1]) + "," + str(users[2]) + "," + str(
                users[3] + "," + str(userFinger) + "," + str(users[5]) + "\n")
            file.write(result)
        file.close()

        file = open(path + "section","r")
        wFile = open(path + "sectionlog","w")
        lines = [line.rstrip('\n') for line in open(path + 'section')]
        for line in lines:
            query = ("SELECT * FROM `section_log` WHERE section_id = " + str(line.split(",")[0]) + " and work_date = " + str(getTodayDate()))
            print(query)
            cursor.execute(query)
            result = cursor.fetchone()
            if(result != None):
                wFile.write(str(result[0]) + "," + str(result[1]) + "," + str(result[2]) + "," + str(result[3]) + "," + str(result[4]) + "\n")
        file.close()

        file = open(path + "fingerprint_scanner","w")
        query = ("SELECT * FROM `fingerprint`")
        cursor.execute(query)
        for line in cursor:
            finger = str(line[0]) + "," + str(line[1]) + "," + str(line[2]) + "\n"
            file.write(finger)
        file.close()

        file = open(path + "worklog", "w")
        query = ("SELECT * FROM `work_log` where work_date = " + str(getTodayDate()))
        cursor.execute(query)
        for line in cursor:
            worklog = str(line[0]) + "," + str(line[1]) + "," + str(line[2]) + "," + str(line[3]) + "," + str(line[4]) + "," + str(line[5]) + "," + str(line[6]) + "\n"
            file.write(worklog)
        file.close()

    except Error as e:
        print(e)

    finally:
        conn.close()

def updateAbsentWorklog():
    while(is_connected() == False):
        time.sleep(60)
    if(is_connected()):
        try:
            conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)
            cursor = conn.cursor()
            query = ("UPDATE work_log set status = 'absent' where work_date = " + getTodayDate() + " and status = 'waiting'")
            cursor.execute(query)
            print(query)
            conn.commit()
            conn.close()
        except Error as e:
            print(e)

def updateAbsentSectionlog():
    while(is_connected() == False):
        time.sleep(60)
    if(is_connected()):
        try:
            conn = mysql.connector.connect(host=host,
                                       database='attendance',
                                       user=mySqlUser,
                                       password=mySqlPassword)
            cursor = conn.cursor()
            query = ("UPDATE section_log set status = 'absent' where work_date = " + getTodayDate() + " and status = 'waiting'")
            cursor.execute(query)
            print(query)
            conn.commit()
            conn.close()
        except Error as e:
            print(e)

def getTomorrowDate():
    tomorrowDate = dt.date.today() + dt.timedelta(days=1)
    return tomorrowDate

localUpdate
schedule.every(5).minutes.do(updateClockIn)
schedule.every().day.at("17:01").do(updateAbsentSectionlog)
schedule.every().day.at("17:01").do(updateAbsentWorklog)
schedule.every().day.at("06:00").do(localUpdate)

while 1:
    schedule.run_pending()
    time.sleep(1)