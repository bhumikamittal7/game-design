#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define POTENTIOMETER_PIN 4
int potValue = 0;

int paddle1Y = 0;
int paddle2Y = 0;
int paddleHeight = 16;
int paddleWidth = 2;
int paddleSpeed = 2;

int ballX = 0;
int ballY = 0;
int ballSize = 4;
int ballSpeedX = 1;
int ballSpeedY = 1;

void setup() {
  pinMode(POTENTIOMETER_PIN, INPUT);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Change I2C address if necessary
  display.clearDisplay();
}

void loop() {
  potValue = analogRead(POTENTIOMETER_PIN);
  paddle1Y = map(potValue, 0, 1023, 0, SCREEN_HEIGHT - paddleHeight);
  
  paddle2Y = (SCREEN_HEIGHT / 2) - (paddleHeight / 2); // Adjust the second paddle's position
  
  ballX += ballSpeedX;
  ballY += ballSpeedY;
  
  if (ballX <= 0) {
    ballSpeedX = 1; // Reset ball speed and position if it goes off the left side
    ballX = 0;
  }
  
  if (ballX >= SCREEN_WIDTH - ballSize) {
    ballSpeedX = -1; // Reset ball speed and position if it goes off the right side
    ballX = SCREEN_WIDTH - ballSize;
  }
  
  if (ballY <= 0 || ballY >= SCREEN_HEIGHT - ballSize) {
    ballSpeedY *= -1; // Reverse ball's Y direction if it hits top or bottom
  }
  
  // Check collision with paddles
  if (ballX <= paddleWidth && ballY + ballSize >= paddle1Y && ballY <= paddle1Y + paddleHeight) {
    ballSpeedX *= -1; // Reverse ball's X direction if it hits the first paddle
  }
  
  if (ballX + ballSize >= SCREEN_WIDTH - paddleWidth && ballY + ballSize >= paddle2Y && ballY <= paddle2Y + paddleHeight) {
    ballSpeedX *= -1; // Reverse ball's X direction if it hits the second paddle
  }
  
  display.clearDisplay();
  
  display.fillRect(0, paddle1Y, paddleWidth, paddleHeight, WHITE);
  display.fillRect(SCREEN_WIDTH - paddleWidth, paddle2Y, paddleWidth, paddleHeight, WHITE);
  
  display.fillRect(ballX, ballY, ballSize, ballSize, WHITE);
  
  display.display();
  
  delay(10);
}
