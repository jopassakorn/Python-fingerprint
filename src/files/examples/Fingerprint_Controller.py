import serial                                                              #Serial imported for Serial communication
import time
import hashlib
import struct
from pyfingerprint.pyfingerprint import PyFingerprint

def enrollFinger(id):
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if (f.verifyPassword() == False):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while (f.readImage() == False):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if (positionNumber >= 0):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while (f.readImage() == False):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if (f.compareCharacteristics() == 0):
            raise Exception('Fingers do not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate(id)
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        return positionNumber

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def clockIn(id):
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if (f.verifyPassword() == False):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while (f.readImage() == False):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if (positionNumber == -1):
            print('No match found!')
            return 0
        else:
            if(str(id) == str(positionNumber)):
                return str(accuracyScore)

        ## OPTIONAL stuff
        ##

        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def compareCharacteristic(finger1,finger2):
    finger1 = str(finger1).split(",")
    finger2 = str(finger2).split(",")
    if(len(finger1) > len(finger2)):
        count = 0
        result = 0
        notEqual = 0
        while(len(finger2) > count):
            if(finger1[count] == finger2[count]):
                result += 1
            if (finger1[count] != finger2[count]):
                notEqual += 1
            count+= 1
    if(len(finger2) > len(finger1)):
        count = 0
        result = 0
        notEqual = 0
        while (len(finger1) > count):
            if (finger1[count] == finger2[count]):
                result += 1
            if (finger1[count] != finger2[count]):
                notEqual += 1
            count += 1
    if (len(finger2) == len(finger1)):
        count = 0
        result = 0
        notEqual = 0
        while (len(finger1) > count):
            if (finger1[count] == finger2[count]):
                result += 1
            if (finger1[count] != finger2[count]):
                notEqual += 1
            count += 1
    return result - notEqual
