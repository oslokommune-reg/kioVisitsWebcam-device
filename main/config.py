#Config file for raspberry pi camera or sensor
#See readme file before setup
#API keys are kept in apiConfig.py which is stored in AWS S3. 

# Enter device name in prod.env to send corret variable values to main script.
#*****************************************************************
import os
class DeviceConfig:
    def __init__(self):
        # Use env override if set, else keep existing default
        self.device_name = os.getenv("DEVICE_NAME", "GrefsenGjenvinningSensor")
#*****************************************************************




#Common value for all cameras
class CommonConfig:
    def __init__(self):
        self.picture_width = 1280
        self.picture_height = 720
        self.crop_width = 1280
        self.crop_height = 240


def get_device_class(device_name):
    
    #---------------All Cameras below here----------------
    if device_name == "GrefsenCamera":
        class GrefsenCamera:
            def __init__(self):
                self.station_id = 29
                self.picture_title = "'Grefsen gjenvinningsstasjon kl. '"
                self.public_picture_name = "grefsen_now.jpg"
                self.open_hour = 6
                self.close_hour = 21
                self.open_hour_weekend = 6
                self.close_hour_weekend = 21
                self.enable_camera = 1
                self.enable_sensor = 0
                self.enable_blur = 1
                self.device_id = "GREGJ_RPI_CAM_QUE"
                self.sensor_id = None
                self.plassering_id = None
                self.enable_double_sensor = None
        return GrefsenCamera()

    elif device_name == "HaraldrudCamera":
        class HaraldrudCamera:
            def __init__(self):
                self.station_id = 41
                self.picture_title = "'Haraldrud gjenvinningsstasjon kl. '"
                self.public_picture_name = "haraldrud_now.jpg"
                self.open_hour = 6
                self.close_hour = 21
                self.open_hour_weekend = 6
                self.close_hour_weekend = 21
                self.enable_camera = 1
                self.enable_sensor = 0
                self.enable_blur = 0
                self.device_id = "HARGJ_RPI_CAM_QUE"
                self.sensor_id = None
                self.plassering_id = None
                self.enable_double_sensor = None

        return HaraldrudCamera()
    
    elif device_name == "SmestadCamera":
        class SmestadCamera:
            def __init__(self):
                self.station_id = 82
                self.picture_title = "'Smestad gjenvinningsstasjon kl. '"
                self.public_picture_name = "smestad_now.jpg"
                self.open_hour = 6
                self.close_hour = 21
                self.open_hour_weekend = 6
                self.close_hour_weekend = 21
                self.enable_camera = 1
                self.enable_sensor = 0
                self.enable_blur = 0
                self.device_id = "SMEGJ_RPI_CAM_QUE"
                self.sensor_id = None
                self.plassering_id = None
                self.enable_double_sensor = None

        return SmestadCamera()

    elif device_name == "GronmoCamera":
        class GronmoCamera:
            def __init__(self):
                self.station_id = 10
                self.picture_title = "'Grønmo gjenvinningsstasjon kl. '"
                self.public_picture_name = "gronmo_now.jpg"
                self.open_hour = 6
                self.close_hour = 21
                self.open_hour_weekend = 6
                self.close_hour_weekend = 21
                self.enable_camera = 1
                self.enable_sensor = 0
                self.enable_blur = 0
                self.device_id = "GROGJ_RPI_CAM_QUE"
                self.sensor_id = None
                self.plassering_id = None
                self.enable_double_sensor = None

        return GronmoCamera()

    elif device_name == "HUACamera":
        class HUACamera:
            def __init__(self):
                self.station_id = 10
                self.picture_title = "'Haraldrud utsortering kl. '"
                self.public_picture_name = "hua_now.jpg"
                self.open_hour = 6
                self.close_hour = 21
                self.open_hour_weekend = 6
                self.close_hour_weekend = 21
                self.enable_camera = 1
                self.enable_sensor = 0
                self.enable_blur = 0
                self.device_id = "HUA_RPI_CAM_QUE"
                self.sensor_id = None
                self.plassering_id = None
                self.enable_double_sensor = None

        return HUACamera()

    #---------------All Sensors below here----------------

    elif device_name == "HaraldrudGjenvinningSensor":
        class HaraldrudGjenvinningSensor:
            def __init__(self):
                self.station_id = 41
                self.plassering_id = 1
                self.sensor_id = 1
                self.open_hour = 7
                self.close_hour = 21
                self.open_hour_weekend = 9
                self.close_hour_weekend = 21
                self.enable_camera = 0
                self.enable_sensor = 1
                self.enable_blur = 0
                self.device_id = "HARGJ_RPI_SENSOR_GATE"
                self.picture_title = None
                self.public_picture_name = None
                self.enable_double_sensor = 1 # Two sensors installed, but only one calibrated. Exept all other stations, USB1 is the one active. therefore double sensor needs to be enabled.


        return HaraldrudGjenvinningSensor()

    elif device_name == "SmestadSensor":
        class SmestadSensor:
            def __init__(self):
                self.station_id = 82
                self.plassering_id = 1
                self.sensor_id = 4
                self.open_hour = 7
                self.close_hour = 21
                self.open_hour_weekend = 9
                self.close_hour_weekend = 21
                self.enable_camera = 0
                self.enable_sensor = 1
                self.enable_blur = 0
                self.device_id = "SMEGJ_RPI_SENSOR_GATE"
                self.picture_title = None
                self.public_picture_name = None
                self.enable_double_sensor = None

        return SmestadSensor()

    elif device_name == "HaraldrudHageSensor":
        class HaraldrudHageSensor:
            def __init__(self):
                self.station_id = 31
                self.plassering_id = 1
                self.sensor_id = 2
                self.open_hour = 7
                self.close_hour = 21
                self.open_hour_weekend = 9
                self.close_hour_weekend = 21
                self.enable_camera = 0
                self.enable_sensor = 1
                self.enable_blur = 0
                self.device_id = "HARHA_RPI_SENSOR_GATE"
                self.picture_title = None
                self.public_picture_name = None
                self.enable_double_sensor = None

        return HaraldrudHageSensor()

    elif device_name == "GronmoGjenvinningSensor":
        class GronmoGjenvinningSensor:
            def __init__(self):
                self.station_id = 10
                self.plassering_id = 1
                self.sensor_id = 3
                self.open_hour = 7
                self.close_hour = 21
                self.open_hour_weekend = 9
                self.close_hour_weekend = 21
                self.enable_camera = 0
                self.enable_sensor = 1
                self.enable_blur = 0
                self.device_id = "GROGJ_RPI_SENSOR_GATE"
                self.picture_title = None
                self.public_picture_name = None
                self.enable_double_sensor = None

        return GronmoGjenvinningSensor()

    elif device_name == "GrefsenGjenvinningSensor":
        class GrefsenGjenvinningSensor:
            def __init__(self):
                self.station_id = 29
                self.plassering_id = 1
                self.sensor_id = 8
                self.open_hour = 7
                self.close_hour = 21
                self.open_hour_weekend =7
                self.close_hour_weekend = 21
                self.enable_camera = 0
                self.enable_sensor = 1
                self.enable_blur = 0
                self.device_id = "GREGJ_RPI_SENSOR_GATE"
                self.picture_title = None
                self.public_picture_name = None
                self.enable_double_sensor = None

        return GrefsenGjenvinningSensor()
    
    elif device_name == "RyenGjenvinningSensor":
        class RyenGjenvinningSensor:
            def __init__(self):
                self.station_id = 86
                self.plassering_id = 1
                self.sensor_id = 5
                self.open_hour = 7
                self.close_hour = 21
                self.open_hour_weekend = 7
                self.close_hour_weekend = 21
                self.enable_camera = 0
                self.enable_sensor = 1
                self.enable_blur = 0
                self.device_id = "RYEGJ_RPI_SENSOR_GATE"
                self.picture_title = None
                self.public_picture_name = None
                self.enable_double_sensor = 0

        return RyenGjenvinningSensor()

    else:
        raise ValueError("Invalid device name specified in the configuration.")



