# config.sh


export DEVICE_ID=$(cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2)

echo "Running from device ${DEVICE_ID}"