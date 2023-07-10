#include <Wire.h>
#include <U8g2lib.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

void readArray(const int[][2]);
int currentx[] = { 0 };
int pushButton = 23;
int potentiometer = 15;
int bulletSpeed = 6;
int bulletY = 59;
int buttonState;
int lastButton;
int currButton = LOW;
int prevx = 0;
long xcord = 0;
int iterations = 0;
int objectSpeed = 1;
int score = 0;
int health = 5;
int junkArray[4][2] = { {}, {}, {}, {} };
int junkArray2[2][2] = { {}, {} };
U8G2_SH1106_128X64_NONAME_F_HW_I2C display(U8G2_R0, U8X8_PIN_NONE);


void setup(void) {
  Serial.begin(9600);
  display.begin();
  pinMode(pushButton, INPUT);
  pinMode(potentiometer, INPUT);
  for (int i = 0; i < 4; ++i) {
    junkArray[i][0] = random(0, 123);
    junkArray[i][1] = 0;
  }
  for (int i = 0; i < 2; ++i) {
    junkArray2[i][0] = random(0, 123);
    junkArray2[i][1] = 0;
  }
}

void loop(void) {
  iterations = iterations + 1;
  lastButton = buttonState;
  buttonState = digitalRead(pushButton);
  int analogOutput = analogRead(potentiometer);
  prevx = xcord;
  xcord = map(analogOutput, 0, 4095, 112, 0);
  if (prevx != xcord && (bulletY >= 59 || bulletY <=0)) {
    currentx[0] = xcord + 8;
  }
  if (lastButton == HIGH && buttonState == LOW) {
    currButton = !currButton;
  }
  if (currButton == LOW) {
    bulletY = 59;
  }
  for (int i = 0; i < 4; ++i) {
    if (iterations %2 == 0) {
      junkArray[i][1] = junkArray[i][1] + objectSpeed;
    }
    for (int k = 0; k < 16; ++k) {
      if (junkArray[i][0] + k > xcord && junkArray[i][0] + k + 5 < xcord + 16) {
        if (junkArray[i][1] + 3 == 55) {
          junkArray[i][0] = random(1, 125);
          junkArray[i][1] = 0;
          health = health - 1;
          return;
        }
      }
    }

    for (int j = 0; j < 6; ++j) {
      if (bulletY + j == junkArray[i][1] + 3) {
        if (currentx[0] >= junkArray[i][0] && currentx[0] <= junkArray[i][0] + 10) {
          Serial.println("DESTROY");
          junkArray[i][0] = random(1, 125);
          junkArray[i][1] = 0;
          if (bulletY != 59) {
            score = score + 100;
          }
        }
      }
    }
  }
  for (int i = 0; i < 2; ++i) {
    if (iterations %2 == 0) {
      junkArray2[i][1] = junkArray2[i][1] + objectSpeed;
    }
    for (int k = 0; k < 16; ++k) {
      if (junkArray2[i][0] + k - 3 > xcord && junkArray2[i][0] + k + 3< xcord + 16) {
        if (junkArray2[i][1] + 3 == 55) {
          junkArray2[i][0] = random(1, 123);
          junkArray2[i][1] = 0;
          health = health - 1;
          return;
        }
      }
    }

    for (int j = 0; j < 6; ++j) {
      if (bulletY + j == junkArray2[i][1]) {
        if (currentx[0] >= junkArray2[i][0] - 3 && currentx[0] <= junkArray2[i][0] + 3) {
          junkArray2[i][0] = random(1, 123);
          junkArray2[i][1] = 0;
          if (bulletY != 59) {
            score = score + 200;
          }
        }
      }
    }
  }

  for (int i = 0; i < 4; ++i) {
    if (junkArray[i][1] >= 61) {
      junkArray[i][0] = random(0, 125);
      junkArray[i][1] = 0;
    }
  }
  for (int i = 0; i < 2; ++i) {
    if (junkArray2[i][1] >= 61) {
      junkArray2[i][0] = random(0, 123);
      junkArray2[i][1] = 0;
    }
  }
  display.firstPage();
  if (health < 1) {
    display.clearBuffer();
    char buffer3[8];
    sprintf(buffer3, "%d", score);
    display.setFont(u8g2_font_ncenB14_tr);
    display.drawStr(3, 35, "Game over!");
    display.setFont(u8g2_font_6x10_tn);
    display.drawStr(60,45, buffer3);
    display.sendBuffer();
    return;
  }
  do {
    char buffer[40];
    char buffer2[3];
    sprintf(buffer, "%d", score);
    sprintf(buffer2, "%d", health);
    display.setFont(u8g2_font_6x10_tn);
    display.drawStr(10, 15, buffer);
    display.drawStr(110, 15, buffer2);
    display.drawBox(xcord, 59, 16, 5);
    if (currButton == HIGH) {
      bulletY = bulletY - bulletSpeed;
      display.drawBox(currentx[0], bulletY, 1, 3);
    }
    for (int i = 0; i < 4; ++i) {
      display.drawBox(junkArray[i][0], junkArray[i][1], 10, 3);
    }
    for (int i = 0; i < 2; ++i) {
      display.drawCircle(junkArray2[i][0], junkArray2[i][1], 3);
    }
  } while (display.nextPage());
}