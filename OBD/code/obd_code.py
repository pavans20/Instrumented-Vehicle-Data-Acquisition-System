import obd

import csv
import time
import datetime as dt
connection = obd.OBD('/dev/ttyUSB0') # auto-connects to USB or RF port
for i in range(10):
    dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    ind_time = dt_India.strftime('%H:%M:%S')
    ind_date = dt_India.strftime('%Y-%m-%d')
    #ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S')
    #ind_date = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
    #cmd = obd.commands.SPEED
    #response = connection.query(cmd)
    #cmd1=obd.commands.RPM
    #response1=connection.query(cmd1)
    #cmd2=obd.commands.ENGINE_LOAD
    #response2=connection.query(cmd)
    t_end = time.time() + 12
    # data to be written row-wise in csv file
    #data = [response.value,response1.value,response2.value]
    #data=["SPEED (Km/H)","RPM (Rev/Min)","ENGINE_LOAD (%)","DATE","TIME"]
    name1="test"+str(i)
    # opening the csv file in 'w+' mode
    file = open(name1+'.csv', 'w+', newline ='')

    # writing the data into the file
    with file:   
        write = csv.writer(file)
        #write.writerows(data)
        #data = [response.value,response1.value,response2.value]
        #write.writerows(data)
        header = ["SPEED (Km/H)","RPM (Rev/Min)","ENGINE_LOAD (%)","ACCELERATOR_POS_D (%)","ACCELERATOR_POS_E (%)","ACCELERATOR_POS_F (%)","DATE","TIME"]
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        # writing data row-wise into the csv file
        while time.time() < t_end:
            cmd = obd.commands.SPEED
            response = connection.query(cmd)
            cmd1=obd.commands.RPM
            response1=connection.query(cmd1)
            cmd2=obd.commands.ENGINE_LOAD
            response2=connection.query(cmd2)
            cmd3 = obd.commands.ACCELERATOR_POS_D
            response3=connection.query(cmd3)
            cmd4 = obd.commands.ACCELERATOR_POS_E
            response4=connection.query(cmd4)
            cmd5 = obd.commands.ACCELERATOR_POS_F
            response5=connection.query(cmd5)
            dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            ind_time = dt_India.strftime('%H:%M:%S')
            ind_date = dt_India.strftime('%Y-%m-%d')
            #writer.writeheader()
            writer.writerow({"SPEED (Km/H)":response.value.magnitude,
                             "RPM (Rev/Min)":response1.value.magnitude,
                             "ENGINE_LOAD (%)":response2.value.magnitude,
                             "ACCELERATOR_POS_D (%)":response3.value.magnitude,
                             "ACCELERATOR_POS_E (%)":response4.value.magnitude,
                             "ACCELERATOR_POS_F (%)":response5.value.magnitude,
                             "DATE":ind_date,
                             "TIME":ind_time})
            
print("end")    
        
