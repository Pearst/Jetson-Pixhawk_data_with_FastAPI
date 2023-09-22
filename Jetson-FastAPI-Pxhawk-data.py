# -*- coding: UTF-8 -*-
from __future__ import print_function

from pymavlink import mavutil
from dronekit import connect, VehicleMode
import time
import asyncio
from fastapi import FastAPI
from typing import Optional

print("Baglaniliyor")

# jetson nano usb connection with pixhawk(gnds should be connected eachother)
global vehicle
vehicle = connect("com15", wait_ready=True, timeout=100)

print("baglandi")
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



def update_pxdata(list):
    pxdata = [
        data_str('Otopilot yazılım versiyonu', vehicle.version),
        data_number('Ana versiyon numarası', list[0]),
        data_number('Alt versiyon numarası', list[1]),
        data_number('Yama versiyon numarası', list[2]),
        data_str('Yayın Türü', list[3]),
        data_str('Yayın Version', list[4]),
        data_boolen('Sürüm kararlı mı?', list[5]),
        data_boolen('MISSION_FLOAT mesaj tipini destekler', list[6]),
        data_boolen('PARAM_FLOAT mesaj tipini destekler', list[7]),
        data_boolen('MISSION_INT mesaj tipini destekler', list[8]),
        data_boolen('COMMAND_INT mesaj tipini destekler', list[9]),
        data_boolen('PARAM_UNION mesaj tipini destekler', list[10]),
        data_boolen('dosya transferi için ftp destekler', list[11]),
        data_boolen('Harici bilgisayar attitude yönetme destekler', list[12]),
        data_boolen('local NED framedeki hız ve pozisyon hedeflerini yönetme destekler',
                    list[13]),
        data_boolen('global scaled integersdaki hız ve pozisyon hedeflerini ayarlamayı destekler',
                    list[14]),
        data_boolen('arazi protokolü ve veri işlemeyi destekler', list[15]),
        data_boolen('doğrudan aktüatör kontrolünü destekler', list[16]),
        data_boolen('Uçuş sonlandırma komutunu destekler', list[17]),
        data_boolen('Onboard (araç üzerinde) kumpas kalbrasyonu destekler', list[18]),
        data_number('Hız (x, y, z)', list[19]),  #test et
        data_number('Mesafe Ölçer Uzaklığı', list[20]), #test et
        data_number('Mesafe Ölçer Voltajı', list[21]),   #test et
        data_boolen('EKF Tamam mı?', list[22]),
        data_boolen('ARM olabilir mi?', list[23]),
        data_str('Sistem Durumu', list[24]),
        data_number('Yer Hızı(Aracın yeryüzüne göre hızı)', list[25]),
        data_number('Hava Hızı(Aracın havaya göre hızı)', list[26]),
        data_str('Mod(Aracın mevcut modu)', list[27]),
        data_str('Arm (Aracı arm etmek için kullanılan parametre)', list[28]),
        data_number('Heading (Aracın Baktığı Yön [0-360]"0-kuzey, 90-doğu, 180-güney, 270-batı")', list[29]),
        data_str('Küresel Konum', vehicle.location.global_frame),   #test et
        data_str('Küresel Konum(Bağıl Yükseklik)', vehicle.location.global_relative_frame),  #test et
        data_str('Yerel Konum', vehicle.location.local_frame), #test et
        data_str('Batarya', vehicle.battery),  #test et
        data_str('Mesafe Ölçer', vehicle.rangefinder),  #test et
        data_str('Yükseklik', vehicle.attitude),  #test et
        data_str('GPS (Durum ve Uydu Sayısı)', vehicle.gps_0)

    ]

    return pxdata

list=[]


@app.get("/")
def get_str_data():
    while True:
        list.append(vehicle.version.major)
        list.append(vehicle.version.minor)
        list.append(vehicle.version.patch)
        list.append(vehicle.version.release_type())
        list.append(vehicle.version.release_version())
        list.append(vehicle.version.is_stable())
        list.append(vehicle.capabilities.mission_float)
        list.append(vehicle.capabilities.param_float)
        list.append(vehicle.capabilities.mission_int)
        list.append(vehicle.capabilities.command_int)
        list.append(vehicle.capabilities.param_union)
        list.append(vehicle.capabilities.ftp)
        list.append(vehicle.capabilities.set_attitude_target)
        list.append(vehicle.capabilities.set_attitude_target_local_ned)
        list.append(vehicle.capabilities.set_altitude_target_global_int)
        list.append(vehicle.capabilities.terrain)
        list.append(vehicle.capabilities.set_actuator_target)
        list.append(vehicle.capabilities.flight_termination)
        list.append(vehicle.capabilities.compass_calibration)
        list.append(vehicle.velocity)
        list.append(vehicle.rangefinder.distance)
        list.append(vehicle.rangefinder.voltage)
        list.append(vehicle.ekf_ok)
        list.append(vehicle.is_armable)
        list.append(vehicle.system_status.state)
        list.append(vehicle.groundspeed)
        list.append(vehicle.airspeed)
        list.append(vehicle.mode.name)
        list.append(vehicle.armed)
        list.append(vehicle.heading)

        pixhawk_data = update_pxdata(list)
        list.clear()

        return pixhawk_data

if __name__ == "__main__":
    # Uygulamayı başlat

    app.run()
