#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

U8G2_SH1106_128X64_NONAME_F_HW_I2C display(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

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

int autoMove = 1; // Movement direction for the second paddle
int score = 0;   // Score count

bool gameOver = false; // Game state flag

void setup() {
  pinMode(POTENTIOMETER_PIN, INPUT);
  display.begin();
  display.setPowerSave(0); // Turn on the display
  display.clearBuffer();  // Clear the display buffer
  
  Serial.begin(9600); // Initialize serial communication for printing score
  
  displayWelcomeMessage(); // Display welcome message on the OLED screen
  delay(2000); // Delay for 2 seconds before starting the game
  
  randomSeed(analogRead(0)); // Seed the random number generator
  resetBall();
}

void loop() {
  if (gameOver) {
    display.clearBuffer();
    display.setFont(u8g2_font_ncenB14_tr);
    display.setCursor(20, SCREEN_HEIGHT / 2 - 10);
    display.print("Game Over");
    display.sendBuffer();
    
    if (Serial.available()) {
      char restartInput = Serial.read();
      if (restartInput == 'y') {
        score = 0;
        gameOver = false;
        resetBall();
        display.clearBuffer();
        displayWelcomeMessage();
        delay(2000);
      }
    }
    
    return; // Stop updating the game
  }
  potValue = analogRead(POTENTIOMETER_PIN);
  paddle1Y = map(potValue, 0, 4095 - paddleHeight, 0, SCREEN_HEIGHT - paddleHeight);
  paddle1Y = constrain(paddle1Y, 0, SCREEN_HEIGHT - paddleHeight); // Restrict paddle1Y within screen bounds
  
  paddle2Y = ballY - paddleHeight / 2; // Update the second paddle's position based on the ball's Y position
  
  ballX += ballSpeedX;
  ballY += ballSpeedY;
  
  if (ballX <= 0) {
    ballSpeedX = abs(ballSpeedX); // Reset ball speed and position if it goes off the left side
    ballX = 0;
    gameOver = true; // Set game over flag
  }
  
  if (ballX >= SCREEN_WIDTH - ballSize) {
    ballSpeedX = -abs(ballSpeedX); // Reset ball speed and position if it goes off the right side
    ballX = SCREEN_WIDTH - ballSize;
    gameOver = true; // Set game over flag
  }
  
  if (ballY <= 0 || ballY >= SCREEN_HEIGHT - ballSize) {
    ballSpeedY *= -1; // Reverse ball's Y direction if it hits top or bottom
  }
  
  if (ballX <= paddleWidth && ballY + ballSize >= paddle1Y && ballY <= paddle1Y + paddleHeight) {
    ballSpeedX = abs(ballSpeedX); 
    score++;                                            // Increment the score count
    Serial.println("Score: " + String(score));           // Print the score to the serial monitor
  }
  
  if (ballX + ballSize >= SCREEN_WIDTH - paddleWidth && ballY + ballSize >= paddle2Y && ballY <= paddle2Y + paddleHeight) {
    ballSpeedX = -abs(ballSpeedX);
  }
  
  display.clearBuffer();
  
  display.drawBox(0, paddle1Y, paddleWidth, paddleHeight);
  display.drawBox(SCREEN_WIDTH - paddleWidth, paddle2Y, paddleWidth, paddleHeight);
  
  display.drawBox(ballX, ballY, ballSize, ballSize);
  
  display.sendBuffer();
  
  delay(10);
}

void displayWelcomeMessage() {
  display.clearBuffer();
  display.setFont(u8g2_font_ncenB14_tr);
  display.setCursor(20, (SCREEN_HEIGHT - 16) / 2);
  display.print("Welcome to");
  display.setCursor(10, (SCREEN_HEIGHT - 16) / 2 + 12);
  display.print("Ping Pong");
  display.sendBuffer();
}

void resetBall() {
  ballX = SCREEN_WIDTH / 2 - ballSize / 2;
  ballY = random(0, SCREEN_HEIGHT - ballSize + 1);
  
  if (random(0, 2) == 0) {
    ballSpeedX = -1;
  } else {
    ballSpeedX = 1;
  }
  
  if (random(0, 2) == 0) {
    ballSpeedY = -1;
  } else {
    ballSpeedY = 1;
  }
}