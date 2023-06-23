#include <U8g2lib.h>
#include <Wire.h>

// Constants
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Objects
U8G2_SH1106_128X64_NONAME_F_HW_I2C display(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

// Variables
int paddle1Y = 0;
int paddle2Y = 0;
int paddleHeight = 16;
int paddleWidth = 2;

int ballX = 0;
int ballY = 0;
int ballSize = 4;
int ballSpeedX = 1;
int ballSpeedY = 1;

bool gameOver = false;

void setup() {
  // Setup code
}

 if (gameOver) {
    // Game over code
  }

  // Update paddle positions
  // - Retrieve input values from sensors or controls
  // - Map the input values to the desired paddle position within the screen height
  // - Update the paddle positions accordingly

  // Update ball position
  // - Modify the ball's position by adding the current ball speed to its coordinates
  // - The ball speed determines the direction and magnitude of the position change

  // Check for collisions
  // - Check if the ball has hit any of the game boundaries (left, right, top, or bottom)
  // - If the ball hits a boundary, adjust its position and speed accordingly
  // - Check if the ball collides with the paddles
  //   - If the ball hits the first paddle, update its speed, increment the score, and display it
  //   - If the ball hits the second paddle, update its speed
  // - The collision detection can be done by comparing the ball's position and size with the paddles' positions and sizes

  // Render display
  // - Clear the display buffer
  // - Draw the paddles and ball on the display buffer based on their current positions and sizes
  // - Send the display buffer to the OLED screen for rendering

  // Delay to control the game speed
}


void displayWelcomeMessage() {
  // Display welcome message
}

void resetBall() {
  // Reset ball position and speed
}


