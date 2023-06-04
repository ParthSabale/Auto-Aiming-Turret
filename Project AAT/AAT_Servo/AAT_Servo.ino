// 1) Include servo Lib and define 2 servo x and y givrs intial position 90 deg
// 2) Start serial comm betw opencv and Arduino with pin no 9,10 for pan (360 degree)& tilt(180 degree) servo
// 3) define variable a for movement in L,R,U and D direction

#include<Servo.h>                     
Servo x,y;                          
int a;                               
int horizontal=90;                    
int vertical=90;
void setup() {
Serial.begin(9600);                  

x.attach(9);                         
y.attach(10);
delay(1000);
}

void loop() {
if(Serial.available()>0)             

{
  a=Serial.read();                   
  if(a=='1')                        
  {
    printf('Aim');                   
  }
  else if(a=='2')                
  {
   horizontal=horizontal+2;
   x.write(horizontal);
   delay(15);
   Serial.println("Suspicious movement detected.............");
    }
  else if(a=='3')            
  {
   horizontal=horizontal-2;
   x.write(horizontal);
   delay(15);
   Serial.println("Suspicious movement detected.............");  
    }
  else if(a=='4')            
  {
   vertical=vertical+2;
   y.write(vertical);
   delay(15);
   Serial.println("Suspicious movement detected.............");   
    }
  else if(a=='5')                 
  {
   vertical=vertical-2;
   y.write(vertical);
   delay(15);
   Serial.println("Suspicious movement's detected.............");
    }

  }
}
