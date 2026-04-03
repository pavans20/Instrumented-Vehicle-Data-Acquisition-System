import serial
from time import sleep, strftime
from datetime import datetime

# Configure the serial connection (update the port as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Update the port if necessary

class GPS:
    def __init__(self):
        UPDATE_100_msec = "$PMTK220,100*2F\r\n"  # Set the update rate to 100ms
        MEAS_100_msec = "$PMTK300,100,0,0,0,0*2C\r\n"  # Set measurement rate to match update rate
        BAUD_57600 = "$PMTK251,57600*2C\r\n"
        GNRMC_ONLY = "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n"

        ser.write(str.encode(BAUD_57600))
        sleep(1)
        ser.baudrate = 57600

        ser.write(str.encode(UPDATE_100_msec))
        sleep(1)

        ser.write(str.encode(MEAS_100_msec))
        sleep(1)

        ser.write(str.encode(GNRMC_ONLY))
        sleep(1)

        ser.flushInput()
        ser.flushOutput()
        print("GPS is Initialized with 100ms update rate")

# Instantiate the GPS class
myGPS = GPS()

timestamped_filename = datetime.now().strftime("gps_data_%Y%m%d_%H%M%S.txt")
# Open a file to save the GPS data
with open(timestamped_filename, "w") as file:
    try:
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
            timestamp = strftime("%Y-%m-%d %H:%M:%S")
            #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            file.write(f"{timestamp}, {NMEA1}\n")
            file.write(f"{timestamp}, {NMEA2}\n")

            # Make sure the data is written to the file immediately
            file.flush()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        ser.close()  # Close the serial connection properly

