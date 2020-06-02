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
@allure.sub_suite("Multiple IRs")
@pytest.mark.usefixtures("resultsDir", "attachOutput")
class TestSmoke:
    @allure.title("CONV_MLT_001")
    @allure.description("""Overlap Add GPU Vocal Whisper Hollow""")
    @pytest.mark.timeout(300)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-53', 'GPU-OV causes error')
    @pytest.mark.xfail(condition=lambda: True, reason='Error after outputing file')
    def test_multi_001(self):
        runConvolutionMulti("GPU-OV", "Dry-Vocal.wav", "multi_001.wav", "Dry-Vocal-Whisper-Hollow.wav", "Body/Whisper-dynamic.wav", "Body/Hollow-dynamic.wav")

    @allure.title("CONV_MLT_002")
    @allure.description("""Uniform Partitioned GPU Vocal Whisper Hollow""")
    @pytest.mark.timeout(300)
    def test_multi_002(self):
        runConvolutionMulti("GPU-UN", "Dry-Vocal.wav", "multi_002.wav", "Dry-Vocal-Whisper-Hollow.wav", "Body/Whisper-dynamic.wav", "Body/Hollow-dynamic.wav")

    @allure.title("CONV_MLT_003")
    @allure.description("""Non-uniform partitioned GPU Vocal Whisper Hollow""")
    @pytest.mark.timeout(300)
    def test_multi_003(self):
        runConvolutionMulti("GPU-NU", "Dry-Vocal.wav", "multi_003.wav", "Dry-Vocal-Whisper-Hollow.wav", "Body/Whisper-dynamic.wav", "Body/Hollow-dynamic.wav")

    @allure.title("CONV_MLT_004")
    @allure.description("""Overlap Add CPU Vocal Whisper Hollow""")
    @pytest.mark.timeout(300)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_multi_004(self):
        runConvolutionMulti("CPU-OV", "Dry-Vocal.wav", "multi_004.wav", "Dry-Vocal-Whisper-Hollow.wav", "Body/Whisper-dynamic.wav", "Body/Hollow-dynamic.wav")

    @allure.title("CONV_MLT_005")
    @allure.description("""Uniform partitioned CPU Vocal Whisper Hollow""")
    @pytest.mark.timeout(300)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_multi_005(self):
        runConvolutionMulti("CPU-UN", "Dry-Vocal.wav", "multi_005.wav", "Dry-Vocal-Whisper-Hollow.wav", "Body/Whisper-dynamic.wav", "Body/Hollow-dynamic.wav")

    @allure.title("CONV_MLT_006")
    @allure.description("""Non-uniform partitioned CPU Vocal Whisper Hollow""")
    @pytest.mark.timeout(300)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_multi_006(self):
        runConvolutionMulti("CPU-NU", "Dry-Vocal.wav", "multi_006.wav", "Dry-Vocal-Whisper-Hollow.wav", "Body/Whisper-dynamic.wav", "Body/Hollow-dynamic.wav")
