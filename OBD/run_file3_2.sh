#!/bin/bash

#cd IV_DATA
mkdir $(date -Iseconds | sed -E s/:/_/g)
cd $(date -Iseconds | sed -E s/:/_/g)
python3 /home/sanjita/OBD/obd_code.py&
#python /home/iv-project/Cameras.py &
