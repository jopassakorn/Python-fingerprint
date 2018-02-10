#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(12, 13);
#include "Wire.h"
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x3f, 16 , 2);
#include "Keypad.h"

const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns
char keys[ROWS][COLS] = {
{'1','2','3'},
{'4','5','6'},
{'7','8','9'},
{'*','0','#'}
};
byte rowPins[ROWS] = {8, 7, 6, 5}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {4, 3, 2}; //connect to the column pinouts of the keypad
 
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);
char key;
uint8_t opv;
boolean exit_fact;

void setup()  
{
  Serial.begin(9600);
  lcd.begin();

  // set the data rate for the sensor serial port
  finger.begin(57600);
  
  if (finger.verifyPassword()) {
  } else {
    while (1) { delay(1); }
  }
}

void loop()                     // run over and over again
{
  lcd.clear();
  lcd.print("Clock-in press 1");
  lcd.setCursor(0,1);
  lcd.print("Enroll Press 2");
  exit_fact = false;
  String intputWord = " ";
  opv = 0;
  key = '0';
  Serial.println(readKeypad());
  delay(3000);
  opv = Serial.parseInt();
  if(opv == 0){
    lcd.clear();
    lcd.print("Server doesn't response");
    lcd.setCursor(0,1);
    lcd.print("Please try again");
  }
  if (opv == 1) {// ID #0 not allowed, try again!
    getFingerprintID();
    if(finger.confidence == 0){
      lcd.clear();
      lcd.print("user not found!");
      lcd.setCursor(0,1);
      lcd.print("Please try again");
    }else{
      Serial.println(finger.fingerID);
      lcd.clear();
      lcd.print("Found:");
      while(intputWord == " "){
        while(Serial.available()) {
          intputWord = Serial.readString();// read the incoming data as string
        }
      }
      lcd.setCursor(6,0);
      lcd.print(intputWord);
      intputWord = " ";
      while(intputWord == " "){
        while(Serial.available()) {
          intputWord = Serial.readString();// read the incoming data as string
        }
      }
      lcd.setCursor(0,1);
      lcd.print(intputWord);
    }
    delay(2000);
    Serial.println();
  }
  if (opv == 2) {// ID #0 not allowed, try again!
    lcd.clear();
    lcd.print("Press * exit # enter");
    lcd.setCursor(0,1);
    lcd.print("AC Code:");

    int count = 8;
    char code;
    lcd.setCursor(count,1);
    while(true){
      key = readKeypad();
      if(key == '#'){
        Serial.println("done");
        break;
      }else if(key == '*'){
        Serial.println("exit"); //tell pi to exit enrollment
        exit_fact = true;
        break;
      }else{
        lcd.setCursor(count,1);
        lcd.print(key);
        Serial.println(key);
        count++;
      }
    }
    while(true){
      if(exit_fact){
        lcd.clear();
        lcd.print("Exiting..");
        lcd.setCursor(0,1);
        lcd.print("Wait a moment");
        break;
      }
      while(intputWord == " "){
          lcd.clear();
          lcd.print("User:");
        while(Serial.available()) {
          intputWord = Serial.readString();// read the incoming data as string
          lcd.setCursor(5,0);
          lcd.print(intputWord);
        }
        delay(500);
      }
      opv = 0;
      while(opv == 0){
        opv = Serial.parseInt();
      }
      lcd.setCursor(0,1);
      lcd.print("Enroll at pos:");
      lcd.setCursor(14,1);
      lcd.print(opv);
      delay(2000);
      getFingerprintEnroll(opv);
      opv = 0;
      break;
    }
  }
}

char readKeypad(void) {
  char key = keypad.getKey();
  while(key == NO_KEY){
    key = keypad.getKey();
  }
  return key;
}

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  lcd.clear();
  lcd.print("Print your finger");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      break;
    case FINGERPRINT_NOFINGER:

      break;
    case FINGERPRINT_PACKETRECIEVEERR:

      break;
    case FINGERPRINT_IMAGEFAIL:

      break;
    default:

      break;
    }
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      break;
    case FINGERPRINT_IMAGEMESS:
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      return p;
    case FINGERPRINT_FEATUREFAIL:
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      return p;
    default:
      return p;
  }
  
  // OK converted!
  p = finger.fingerFastSearch();
  if (p == FINGERPRINT_OK) {
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    return p;
  } else {
    return p;
  }
}

uint8_t getFingerprintEnroll(uint8_t id) {

  int p = -1;
  lcd.clear();
  lcd.print("Print your finger");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
      break;
    case FINGERPRINT_NOFINGER:

      break;
    case FINGERPRINT_PACKETRECIEVEERR:

      break;
    case FINGERPRINT_IMAGEFAIL:

      break;
    default:

      break;
    }
  }
  lcd.clear();
  lcd.print("Remove finger");
  delay(2000);
  // OK success!

  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:

      break;
    case FINGERPRINT_IMAGEMESS:

      return p;
    case FINGERPRINT_PACKETRECIEVEERR:

      return p;
    case FINGERPRINT_FEATUREFAIL:

      return p;
    case FINGERPRINT_INVALIDIMAGE:

      return p;
    default:
      return p;
  }
  

  delay(2000);
  p = 0;
  lcd.clear();
  lcd.print("Print the same");
  lcd.setCursor(0,1);
  lcd.print("finger again");
  while (p != FINGERPRINT_NOFINGER) {
    p = finger.getImage();
  }
  p = -1;

  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:

      break;
    case FINGERPRINT_NOFINGER:

      break;
    case FINGERPRINT_PACKETRECIEVEERR:

      break;
    case FINGERPRINT_IMAGEFAIL:

      break;
    default:

      break;
    }
  }

  // OK success!

  p = finger.image2Tz(2);
  switch (p) {
    case FINGERPRINT_OK:
      break;
    case FINGERPRINT_IMAGEMESS:

      return p;
    case FINGERPRINT_PACKETRECIEVEERR:

      return p;
    case FINGERPRINT_FEATUREFAIL:

      return p;
    case FINGERPRINT_INVALIDIMAGE:

      return p;
    default:

      return p;
  }
  
  // OK converted!
  Serial.print("Creating model for #");  Serial.println(id);
  
  p = finger.createModel();
  if (p == FINGERPRINT_OK) {

  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    
    return p;
  } else if (p == FINGERPRINT_ENROLLMISMATCH) {
    lcd.clear();
    lcd.print("Finger did not match!");
    delay(5000);
    return p;
  } else {

    return p;
  }   
  
  Serial.print("ID "); Serial.println(id);
  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK) {
    lcd.clear();
    lcd.print("Enroll Complete");
    Serial.println("Enroll Done");
    delay(5000);
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {

    return p;
  } else if (p == FINGERPRINT_BADLOCATION) {

    return p;
  } else if (p == FINGERPRINT_FLASHERR) {

    return p;
  } else {

    return p;
  }   
}
