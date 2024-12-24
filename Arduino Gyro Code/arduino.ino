#include "Wire.h"       
#include "I2Cdev.h"     
#include "MPU6050.h"  
#include <SoftwareSerial.h>
SoftwareSerial bluetooth(1,0); // RX, TX pins for HC-05  

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;
int state_x, state_y;
int old_state_x, old_state_y;

struct MyData {
  byte X;
  byte Y;
  byte Z;
};

MyData data;

void setup()
{
  bluetooth.begin(9600);  // Start Bluetooth communication
  // Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  //pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.X = map(ax, -16000, 16000, 0, 50); // X axis data
   data.Y = map(ay, -16000, 16000, 0, 50); 
  data.Z = map(az, -16000, 16000, 0, 50);  // Y axis data
  // Serial.print("Axis X = ");
  // Serial.print(data.X);
  // Serial.print("  ");
  // Serial.print("Axis Y = ");
  // Serial.print( data.Y);
  // Serial.print("  ");
  // Serial.print("Axis Z  = ");
  // Serial.println(data.Z);
  
  old_state_x = state_x;
  old_state_y = state_y;

  //x axis yaane left w right
  if (data.X>15 && data.X<=35){state_x=0;}  
  if (data.X>35 && data.X<=42){state_x=1;}
  if (data.X>42 && data.X<=55){state_x=2;}
  if (data.X>10 && data.X<=15){state_x=3;}
  if (data.X>0 && data.X<=10){state_x=4;}
  //y axis yaane up w down
  if ( data.Y>15 &&  data.Y<=35){state_y=0;}
  if ( data.Y>35 &&  data.Y<=42){state_y=5;}
  if ( data.Y>42 &&  data.Y<=55){state_y=6;}
  if ( data.Y>10 &&  data.Y<=15){state_y=7;}
  if ( data.Y>0 &&  data.Y<=10){state_y=8;}

  //hyade bass ta ytba3 bass lamma yghayer state
  if (state_x!=old_state_x){
    switch (state_x) {
      case 0:
        //Serial.println("Neutral");        
        bluetooth.println("Neutral");
        break; 
      case 1:
        //Serial.println("Slight Left");
        bluetooth.println("Slight Left");
        break;
      case 2:
        //Serial.println("Hard Left");
        bluetooth.println("Hard Left");
        break;
      case 3:
        //Serial.println("Slight Right");
        bluetooth.println("Slight Right");
        break;
      case 4:
        //Serial.println("Hard Right");
        bluetooth.println("Hard Right");
        break;
      default:
        //Serial.println("ERROR");
        bluetooth.println("ERROR");
        break;
    }}
  if(state_y!=old_state_y){
    switch(state_y){
      case 0:
        //Serial.println("Neutral");
        bluetooth.println("Neutral");
        break; 
      case 5:
        //Serial.println("Slight Up");
        bluetooth.println("Slight Up");
        break;
      case 6:
        //Serial.println("Hard Up");
        bluetooth.println("Hard Up");
        break;
      case 7:
        //Serial.println("Slight Down");
        bluetooth.println("Slight Down");
        break;
      case 8:
        //Serial.println("Hard Down");
        bluetooth.println("Hard Down");
        break;
      default:
        //Serial.println("ERROR");
        bluetooth.println("ERROR");
        break;
    }
  }

  delay(50);

}