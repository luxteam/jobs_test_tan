"""This file contains autotests for TALibTestConvolution"""

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

@allure.parent_suite("Convolution")
@allure.suite(get_gpu() + " " + platform.system() + " " + platform.release())
@allure.sub_suite("Smoke")
@pytest.mark.usefixtures("resultsDir", "attachOutput")
class TestSmoke:
    @allure.title("CONV_SM_001")
    @allure.description("""Overlap Add GPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-53', 'GPU-OV causes error')
    @pytest.mark.xfail(condition=lambda: True, reason='Error after outputing file')
    def test_conv_001(self):
        runConvolution("GPU-OV", "smokeIn.wav", "conv_001.wav", "testresponse.wav", "conv_001.wav")

    @allure.title("CONV_SM_002")
    @allure.description("""Uniform Partitioned GPU""")
    @pytest.mark.timeout(150)
    def test_conv_002(self):
        runConvolution("GPU-UN", "smokeIn.wav", "conv_002.wav", "testresponse.wav", "conv_001.wav")

    @allure.title("CONV_SM_003")
    @allure.description("""Non-uniform partitioned GPU""")
    @pytest.mark.timeout(150)
    def test_conv_003(self):
        runConvolution("GPU-NU", "smokeIn.wav", "conv_003.wav", "testresponse.wav", "conv_001.wav")

    @allure.title("CONV_SM_004")
    @allure.description("""Overlap Add CPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_004(self):
        runConvolution("CPU-OV", "smokeIn.wav", "conv_004.wav", "testresponse.wav", "conv_001.wav")

    @allure.title("CONV_SM_005")
    @allure.description("""Uniform partitioned CPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_005(self):
        runConvolution("CPU-UN", "smokeIn.wav", "conv_005.wav", "testresponse.wav", "conv_001.wav")

    @allure.title("CONV_SM_006")
    @allure.description("""Non-uniform partitioned CPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_006(self):
        runConvolution("CPU-NU", "smokeIn.wav", "conv_006.wav", "testresponse.wav", "conv_001.wav")
