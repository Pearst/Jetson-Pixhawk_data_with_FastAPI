# -*- coding: UTF-8 -*-
from __future__ import print_function

from dronekit import connect, Command, LocationGlobal, VehicleMode, LocationGlobalRelative
import time
import numpy as np
from fastapi import FastAPI
from typing import Optional
import threading

print("Baglaniliyor")
global vehicle
vehicle = connect("com15", wait_ready=True, timeout=100)
print("baglandi")

# point4 = LocationGlobalRelative(38.7950358, 35.6152222, 7)

takeoff_done = threading.Event()

def takeoff():
    altitude = 3
    print("motorlar arm ediliyor")


    vehicle.armed = True
    time.sleep(5)
    vehicle.mode = VehicleMode("GUIDED")
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("kalkis yapiliyor...")
    vehicle.simple_takeoff(altitude)

    while True:
        #print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= altitude * 0.95:
            print("Hedef yükseklige ulasildi")
            takeoff_done.set()
            break
        time.sleep(1)


def land():
    takeoff_done.wait()
    print("10 sn sonra iniş yapılacak")
    time.sleep(10)

    print("Now let's land")
    vehicle.mode = VehicleMode("LAND")


vehicle.wait_ready('autopilot_version')
app = FastAPI()

class data_str:
    name: Optional[str]
    data: Optional[str]

    def __init__(self, name, data):
        self.name = name
        self.data = data
class data_number:
    name: Optional[str]
    data: Optional[float]

    def __init__(self, name, data):
        self.name = name
        self.data = data
class data_boolen:
    name: Optional[str]
    data: Optional[bool]

    def __init__(self, name, data):
        self.name = name
        self.data = data


def update_pxdata():
    pxdata = [
        data_str('Otopilot yazılım versiyonu', vehicle.version),
        data_number('Ana versiyon numarası', vehicle.version.major),
        data_number('Alt versiyon numarası', vehicle.version.minor),
        data_number('Yama versiyon numarası', vehicle.version.patch),
        data_str('Yayın Türü', vehicle.version.release_type()),
        data_str('Yayın Version', vehicle.version.release_version()),
        data_boolen('Sürüm kararlı mı?', vehicle.version.is_stable()),
        data_boolen('MISSION_FLOAT mesaj tipini destekler', vehicle.capabilities.mission_float),
        data_boolen('PARAM_FLOAT mesaj tipini destekler', vehicle.capabilities.param_float),
        data_boolen('MISSION_INT mesaj tipini destekler', vehicle.capabilities.mission_int),
        data_boolen('COMMAND_INT mesaj tipini destekler', vehicle.capabilities.command_int),
        data_boolen('PARAM_UNION mesaj tipini destekler', vehicle.capabilities.param_union),
        data_boolen('dosya transferi için ftp destekler', vehicle.capabilities.ftp),
        data_boolen('Harici bilgisayar attitude yönetme destekler', vehicle.capabilities.set_attitude_target),
        data_boolen('local NED framedeki hız ve pozisyon hedeflerini yönetme destekler', vehicle.capabilities.set_attitude_target_local_ned),
        data_boolen('global scaled integersdaki hız ve pozisyon hedeflerini ayarlamayı destekler', vehicle.capabilities.set_altitude_target_global_int),
        data_boolen('arazi protokolü ve veri işlemeyi destekler', vehicle.capabilities.terrain),
        data_boolen('doğrudan aktüatör kontrolünü destekler', vehicle.capabilities.set_actuator_target),
        data_boolen('Uçuş sonlandırma komutunu destekler', vehicle.capabilities.flight_termination),
        data_boolen('Onboard (araç üzerinde) kumpas kalbrasyonu destekler', vehicle.capabilities.compass_calibration),
        data_number('Hız (x, y, z)',vehicle.velocity),  # test et
        data_number('Mesafe Ölçer Uzaklığı', vehicle.rangefinder.distance),  # test et
        data_number('Mesafe Ölçer Voltajı', vehicle.rangefinder.voltage),  # test et
        data_boolen('EKF Tamam mı?', vehicle.ekf_ok),
        data_boolen('ARM olabilir mi?', vehicle.is_armable),
        data_str('Sistem Durumu', vehicle.system_status.state),
        data_number('Yer Hızı(Aracın yeryüzüne göre hızı)', vehicle.groundspeed),
        data_number('Hava Hızı(Aracın havaya göre hızı)', vehicle.airspeed),
        data_str('Mod(Aracın mevcut modu)', vehicle.mode.name),
        data_str('Arm (Aracı arm etmek için kullanılan parametre)', vehicle.armed),
        data_number('Heading', vehicle.heading),
        data_str('Küresel Konum', vehicle.location.global_frame),  # test et
        data_str('Küresel Konum(Bağıl Yükseklik)', vehicle.location.global_relative_frame),  # test et
        data_str('Yerel Konum', vehicle.location.local_frame),  # test et
        data_str('Batarya', vehicle.battery),  # test et
        data_str('Mesafe Ölçer', vehicle.rangefinder),  # test et
        data_str('Yükseklik', vehicle.attitude),  # test et
        data_str('GPS (Durum ve Uydu Sayısı)', vehicle.gps_0)
    ]
    return pxdata

def konuma_git(konum):                                           #girilen gps konumuna 2 metre kalana kadar git
    vehicle.airspeed = 3
    vehicle.groundspeed = 7
    point = konum
    print("Koordinat noktasına ilerliyorum")
    vehicle.simple_goto(point)
    while True:
        current_loc = [vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon]
        x = [point.lat, point.lon]
        ali = np.array(np.absolute(current_loc)) - np.array(np.absolute(x))
        mesafe = ali * 111000
        a = mesafe[0]
        b = mesafe[1]
        kalan_mesafe1 = (a ** 2) + (b ** 2)
        kalan_mesafe = np.sqrt(kalan_mesafe1)
        print("kalan mesafe: %s" % kalan_mesafe)
        time.sleep(1)
        if (kalan_mesafe < 2):
            print("Hedef noktaya ulaşıldı")
            break

takeoff = threading.Thread(target=takeoff, daemon=True)
takeoff.start()
land = threading.Thread(target=land, daemon=True)
land.start()
#konuma_git(point4)

@app.get("/")
def get_data():
    pixhawk_data = update_pxdata()
    return pixhawk_data

