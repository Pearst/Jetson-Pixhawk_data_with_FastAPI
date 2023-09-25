# -*- coding: UTF-8 -*-
from __future__ import print_function

from pymavlink import mavutil
from dronekit import connect, VehicleMode
import time
connection_string="127.0.0.1:14550"

print("Baglaniliyor")
global vehicle
vehicle = connect("/dev/serial/by-id/usb-Hex_ProfiCNC_CubeOrange_310024001551393334373535-if00")

print("baglandi")


def arm_ol_ve_yuksel(hedef_yukseklik):
	while vehicle.is_armable==False:
		print("Arm ici gerekli sartlar saglanamadi.")
		time.sleep(1)
	print("Iha su anda armedilebilir")
	
	vehicle.mode=VehicleMode("GUIDED")
	while vehicle.mode=='GUIDED':
		print('Guided moduna gecis yapiliyor')
		time.sleep(1.5)

	print("Guided moduna gecis yapildi")
	vehicle.armed=True
	while vehicle.armed is False:
		print("Arm icin bekleniliyor")
		time.sleep(1)

	print("Ihamiz arm olmustur")
	
	vehicle.simple_takeoff(hedef_yukseklik)
	while vehicle.location.global_relative_frame.alt<=hedef_yukseklik*0.94:
		print("Su anki yukseklik{}".format(vehicle.location.global_relative_frame.alt))
		time.sleep(0.5)
	print("Takeoff gerceklesti")


arm_ol_ve_yuksel(5)

print("irtifaya ulaşıldı")
time.sleep(5)

vehicle.mode=VehicleMode("LAND")
time.sleep(30)

