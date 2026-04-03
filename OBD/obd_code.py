import csv
import time
import datetime as dt
import obd

connection = obd.OBD('/dev/ttyUSB1')  # auto-connects to USB or RF port
file_count = 0  # Initialize a file counter

try:
    while True:
        # Create a new CSV file every 5 minutes
        name1 = f"test{file_count}.csv"
        with open(name1, 'w+', newline='') as file:
            header = ["SPEED (Km/H)", "RPM (Rev/Min)", "ENGINE_LOAD (%)", "DATE", "TIME"]
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()

            # Record the start time for 5 minutes
            t_end = time.time() + 5 * 60  # 5 minutes from now

            while time.time() < t_end:
                # Query OBD-II commands
                cmd = obd.commands.SPEED
                response = connection.query(cmd)
                cmd1 = obd.commands.RPM
                response1 = connection.query(cmd1)
                cmd2 = obd.commands.ENGINE_LOAD
                response2 = connection.query(cmd2)

                # Get the current time and date
                dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                ind_time = dt_India.strftime('%H:%M:%S') + f".{dt_India.microsecond // 1000:03d}"
                ind_date = dt_India.strftime('%Y-%m-%d')

                # Write data to CSV
                writer.writerow({
                    "SPEED (Km/H)": response.value.magnitude if response.value else "N/A",
                    "RPM (Rev/Min)": response1.value.magnitude if response1.value else "N/A",
                    "ENGINE_LOAD (%)": response2.value.magnitude if response2.value else "N/A",
                    "DATE": ind_date,
                    "TIME": ind_time
                })

            file_count += 1  # Increment the file counter for the next file

except KeyboardInterrupt:
    print("Data collection stopped by user.")

print("end")

