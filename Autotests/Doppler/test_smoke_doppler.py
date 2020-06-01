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

@allure.parent_suite("Doppler")
@allure.suite(get_gpu() + " " + platform.system() + " " + platform.release())
@allure.sub_suite("Smoke")
@pytest.mark.usefixtures("resultsDir", "attachOutput")
class TestSmoke:
    @allure.title("DOPP_SM_001")
    @allure.description("""Simple GPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https:\\\\adc.luxoft.com\\jira\\browse\\STVITT-77', 'GPU mode doesn\'t work')
    def test_dopp_001(self):
        runDoppler("default.xml", "smokeIn.wav", "dopp_001.wav", "1", "GPU", "dopp_001.wav")
        
    @allure.title("DOPP_SM_002")
    @allure.description("""Simple CPU""")
    @pytest.mark.timeout(150)
    def test_dopp_002(self):
        runDoppler("default.xml", "smokeIn.wav", "dopp_002.wav", "1", "CPU", "dopp_001.wav")

    @allure.title("DOPP_SM_003")
    @allure.description("""Max bounces = 2 GPU""")
    @allure.issue('https:\\\\adc.luxoft.com\\jira\\browse\\STVITT-77', 'GPU mode doesn\'t work')
    @pytest.mark.timeout(150)
    def test_dopp_003(self):
        runDoppler("default.xml", "smokeIn.wav", "dopp_003.wav", "2", "GPU", "dopp_003.wav")

    @allure.title("DOPP_SM_004")
    @allure.description("""Max bounces = 2 CPU""")
    @pytest.mark.timeout(150)
    def test_dopp_004(self):
        runDoppler("default.xml", "smokeIn.wav", "dopp_004.wav", "2", "CPU", "dopp_003.wav")
