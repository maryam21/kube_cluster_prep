#/!/bin/bash

now_t=$(date +%s)
touch cpu_pressure_$now_t.csv
echo "time,stall" > cpu_pressure_$now_t.csv

touch io_pressure_$now_t.csv
echo "time,stall" > io_pressure_$now_t.csv

while true; do
    echo "$(date +%s),$(cat /proc/pressure/cpu | cut -d "=" -f 5)" >> cpu_pressure_$now_t.csv
    echo "$(date +%s),$(cat /proc/pressure/io | head -n 1 | cut -d "=" -f 5)" >> io_pressure_$now_t.csv
    sleep 30
done
