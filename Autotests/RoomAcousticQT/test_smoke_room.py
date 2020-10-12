"""This file contains autotests for TALibDopplerTest"""

import os
import sys
import ctypes
import subprocess
import soundfile
import pytest
import allure
import platform

from Util.utils import *
from Util.system_info import get_gpu

"""TESTS"""

@allure.parent_suite("RoomAcousticQT")
@allure.suite(get_gpu() + " " + platform.system() + " " + platform.release())
@allure.sub_suite("Smoke")
@pytest.mark.usefixtures("resultsDir", "attachOutput")
class TestSmoke:
    
    @allure.title("ROOM_SM_001")
    @allure.description("""Default""")
    @pytest.mark.timeout(30)
    def test_room_001(self):
        runRoomAcoustic("DefaultRoomTest.xml", "room_001.wav", "Room1.wav")
    
    @allure.title("ROOM_SM_002")
    @allure.description("""7 sources OA""")
    @pytest.mark.timeout(120)
    def test_room_002(self):
        runRoomAcoustic("lowLoad.xml", "lowLoadOA.wav", "Room2.wav")
    
    @allure.title("ROOM_SM_003")
    @allure.description("""20 sources OA""")
    @pytest.mark.timeout(120)
    def test_room_003(self):
        runRoomAcoustic("mediumLoad.xml", "mediumLoadOA.wav", "Room3.wav")
    
    @allure.title("ROOM_SM_004")
    @allure.description("""40 sources OA""")
    @pytest.mark.timeout(120)
    def test_room_004(self):
        runRoomAcoustic("highLoad.xml", "highLoadOA.wav", "Room4.wav")
    
    @allure.title("ROOM_SM_005")
    @allure.description("""64 sources""")
    @pytest.mark.timeout(120)
    def test_room_005(self):
        runRoomAcoustic("maxLoad.xml", "maxLoadOA.wav", "Room5.wav")