import serial
from datetime import datetime
from time import sleep, strftime

# Configure the serial connection (update the port as needed)
ser = serial.Serial('/dev/ttyUSB1', 9600)  # Update the port if necessary

class GPS:
    def __init__(self):
        UPDATE_200_msec = "$PMTK220,200*2C\r\n"
        MEAS_200_msec = "$PMTK300,1000,0,0,0,0*2F\r\n"
        BAUD_57600 = "$PMTK251,57600*2C\r\n"
        GNRMC_ONLY = "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n"

        ser.write(str.encode(BAUD_57600))
        sleep(1)
        ser.baudrate = 57600

        ser.write(str.encode(UPDATE_200_msec))
        sleep(1)

        ser.write(str.encode(MEAS_200_msec))
        sleep(1)

        ser.write(str.encode(GNRMC_ONLY))
        sleep(1)

        ser.flushInput()
        ser.flushOutput()
        print("GPS is Initialized")

# Instantiate the GPS class
myGPS = GPS()

# Open a file to save the GPS data
with open("gps_data.txt", "w") as file:
    while True:
        ser.flushInput()
        while ser.inWaiting() == 0:
            pass
        NMEA1 = ser.readline().decode('utf-8').strip()
        while ser.inWaiting() == 0:
            pass
        NMEA2 = ser.readline().decode('utf-8').strip()
        
        # Print the GPS data
        print(NMEA1)
        print(NMEA2)

        # Save the GPS data to the file with a timestamp
        #timestamp = strftime("%Y-%m-%d %H:%M:%S")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        file.write(f"{timestamp}, {NMEA1}\n")
        file.write(f"{timestamp}, {NMEA2}\n")

        # Make sure the data is written to the file immediately
        file.flush()


