import serial
import time

# Replace 'COM3' with your Arduino's serial port
arduino_port = 'COM8'  # For Linux/Mac, it might be '/dev/ttyUSB0' or '/dev/ttyACM0'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

time.sleep(2)  # Allow time for the connection to initialize

def send_command(command):
    print(f"Sending command: {command}")
    ser.write(command.encode())  # Send the command to Arduino
    time.sleep(0.1)  # Wait a bit for Arduino to process the command

try:
    while True:
        print("Enter command (G/Y/R <light number>, A<G/Y/R> for all lights, or O):")
        user_input = input().strip().upper()

        if len(user_input) == 2 and (user_input.startswith('G') or user_input.startswith('Y') or user_input.startswith('R')):
            command = user_input[0]
            try:
                light_number = int(user_input[1])
                if 1 <= light_number <= 4:
                    send_command(f"{command}{light_number}")
                else:
                    print("Invalid light number. Must be between 1 and 4.")
            except ValueError:
                print("Invalid command format. Use G/Y/R followed by a light number (1-4).")
        elif user_input == 'O':
            send_command('O')
        elif len(user_input) == 2 and user_input[0] == 'A' and (user_input[1] == 'G' or user_input[1] == 'Y' or user_input[1] == 'R'):
            send_command(f"A{user_input[1]}")
        else:
            print("Invalid command. Use G/Y/R <light number>, A<G/Y/R> for all lights, or O.")
except KeyboardInterrupt:
    print("Program terminated")
finally:
    ser.close()

# ARDUINO CODE
# // Arrays to store pin numbers for each color
# int greenPins[] = {11, 8, 5, 2};  // Assuming G1 is on pin 11
# int yellowPins[] = {12, 9, 6, 3};
# int redPins2[] = {13, 10, 7, 4};
#
# void setup() {
#   Serial.begin(9600);  // Initialize serial communication
#
#   // Set all pins as outputs
#   for (int i = 0; i < 14; i++) {
#     pinMode(i, OUTPUT);
#   }
#
#   // Turn on all red lights by default
#   for (int i = 0; i < 4; i++) {
#     digitalWrite(redPins2[i], HIGH);
#   }
# }
#
# void loop() {
#   if (Serial.available() > 0) {
#     char command = Serial.read();
#     Serial.print("Received command: ");
#     Serial.println(command);
#
#     if (command == 'G' || command == 'Y' || command == 'R') {
#       int lightNumber = Serial.parseInt();  // Read the light number
#       Serial.print("Light number: ");
#       Serial.println(lightNumber);
#
#       switch (command) {
#         case 'G':
#           greenLight(lightNumber);
#           break;
#         case 'Y':
#           yellowLight(lightNumber);
#           break;
#         case 'R':
#           redLight(lightNumber);
#           break;
#       }
#     } else if (command == 'A') {  // 'A' for "All"
#       char color = Serial.read();
#       Serial.print("Set all to color: ");
#       Serial.println(color);
#       switch (color) {
#         case 'G':
#           setAllLights('G');
#           break;
#         case 'Y':
#           setAllLights('Y');
#           break;
#         case 'R':
#           setAllLights('R');
#           break;
#         default:
#           Serial.println("Invalid color command for all lights.");
#           break;
#       }
#     } else if (command == 'O') {
#       // Turn off all lights
#       for (int i = 0; i < 4; i++) {
#         digitalWrite(greenPins[i], LOW);
#         digitalWrite(yellowPins[i], LOW);
#         digitalWrite(redPins2[i], HIGH);  // Default to red
#       }
#       Serial.println("All lights turned off");
#     } else {
#       // Invalid command, handle accordingly
#       Serial.println("Invalid command");
#     }
#   }
# }
#
# void greenLight(int lightNumber) {
#   Serial.print("Green light ");
#   Serial.println(lightNumber);
#
#   if (lightNumber >= 1 && lightNumber <= 4) {
#     for (int i = 0; i < 4; i++) {
#       digitalWrite(greenPins[i], i + 1 == lightNumber ? HIGH : LOW);
#       digitalWrite(yellowPins[i], LOW);
#       digitalWrite(redPins2[i], i + 1 == lightNumber ? LOW : HIGH);
#     }
#     delay(500);  // Adjust delay as needed
#   }
# }
#
# void yellowLight(int lightNumber) {
#   Serial.print("Yellow light ");
#   Serial.println(lightNumber);
#
#   if (lightNumber >= 1 && lightNumber <= 4) {
#     for (int i = 0; i < 4; i++) {
#       digitalWrite(yellowPins[i], i + 1 == lightNumber ? HIGH : LOW);
#       digitalWrite(greenPins[i], LOW);
#       digitalWrite(redPins2[i], i + 1 == lightNumber ? LOW : HIGH);
#     }
#     delay(500);  // Adjust delay as needed
#   }
# }
#
# void redLight(int lightNumber) {
#   Serial.print("Red light ");
#   Serial.println(lightNumber);
#
#   if (lightNumber >= 1 && lightNumber <= 4) {
#     for (int i = 0; i < 4; i++) {
#       digitalWrite(redPins2[i], i + 1 == lightNumber ? HIGH : LOW);
#       digitalWrite(greenPins[i], LOW);
#       digitalWrite(yellowPins[i], LOW);
#     }
#     delay(500);  // Adjust delay as needed
#   }
# }
#
# void setAllLights(char color) {
#   for (int i = 0; i < 4; i++) {
#     switch (color) {
#       case 'G':
#         digitalWrite(greenPins[i], HIGH);
#         digitalWrite(yellowPins[i], LOW);
#         digitalWrite(redPins2[i], LOW);
#         break;
#       case 'Y':
#         digitalWrite(greenPins[i], LOW);
#         digitalWrite(yellowPins[i], HIGH);
#         digitalWrite(redPins2[i], LOW);
#         break;
#       case 'R':
#         digitalWrite(greenPins[i], LOW);
#         digitalWrite(yellowPins[i], LOW);
#         digitalWrite(redPins2[i], HIGH);
#         break;
#     }
#   }
#   delay(500);  // Adjust delay as needed
# }
