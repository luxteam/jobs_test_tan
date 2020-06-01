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
@allure.sub_suite("Sources")
@pytest.mark.usefixtures("resultsDir", "attachOutput")
class TestSources:
    @allure.title("CONV_SRC_001")
    @allure.description("""Overlap Add GPU
    NoAngel FishbowlCondenser""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-53', 'GPU-OV causes error')
    @pytest.mark.xfail(condition=lambda: True, reason='Error after outputing file')
    def test_src_001(self):
        runConvolution("GPU-OV", "NoAngel.wav", "src_001.wav", "Body/Fishbowl-condenser.wav", "NoAngelFishbowlCondenser.wav")
        
    @allure.title("CONV_SRC_002")
    @allure.description("""Uniform Partitioned GPU
    NoAngel FishbowlCondenser""")
    @pytest.mark.timeout(150)
    def test_src_002(self):
        runConvolution("GPU-UN", "NoAngel.wav", "src_002.wav", "Body/Fishbowl-condenser.wav", "NoAngelFishbowlCondenser.wav")

    @allure.title("CONV_SRC_003")
    @allure.description("""Non-uniform partitioned GPU
    NoAngel FishbowlCondenser""")
    @pytest.mark.timeout(150)
    def test_src_003(self):
        runConvolution("GPU-NU", "NoAngel.wav", "src_003.wav", "Body/Fishbowl-condenser.wav", "NoAngelFishbowlCondenser.wav")

    @allure.title("CONV_SRC_004")
    @allure.description("""Overlap Add CPU
    NoAngel FishbowlCondenser""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_src_004(self):
        runConvolution("CPU-OV", "NoAngel.wav", "src_004.wav", "Body/Fishbowl-condenser.wav", "NoAngelFishbowlCondenser.wav")

    @allure.title("CONV_SRC_005")
    @allure.description("""Uniform partitioned CPU
    NoAngel FishbowlCondenser""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_src_005(self):
        runConvolution("CPU-UN", "NoAngel.wav", "src_005.wav", "Body/Fishbowl-condenser.wav", "NoAngelFishbowlCondenser.wav")

    @allure.title("CONV_SRC_006")
    @allure.description("""Non-uniform partitioned CPU
    NoAngel FishbowlCondenser""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_src_006(self):
        runConvolution("CPU-NU", "NoAngel.wav", "src_006.wav", "Body/Fishbowl-condenser.wav", "NoAngelFishbowlCondenser.wav")

    @allure.title("CONV_SRC_007")
    @allure.description("""Overlap Add GPU
    NoAngel AON-18""")
    @pytest.mark.timeout(300)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-53', 'GPU-OV causes error')
    @pytest.mark.xfail(condition=lambda: True, reason='Error after outputing file')
    def test_src_007(self):
        runConvolution("GPU-OV", "NoAngel.wav", "src_007.wav", "Spaces/18.wav", "NoAngelAON18.wav")
        
    @allure.title("CONV_SRC_008")
    @allure.description("""Uniform Partitioned GPU""")
    @pytest.mark.timeout(300)
    def test_src_008(self):
        runConvolution("GPU-UN", "NoAngel.wav", "src_008.wav", "Spaces/18.wav", "NoAngelAON18.wav")

    @allure.title("CONV_SRC_009")
    @allure.description("""Non-uniform partitioned GPU""")
    @pytest.mark.timeout(300)
    def test_src_009(self):
        runConvolution("GPU-NU", "NoAngel.wav", "src_009.wav", "Spaces/18.wav", "NoAngelAON18.wav")

    @allure.title("CONV_SRC_010")
    @allure.description("""Overlap Add CPU""")
    @pytest.mark.timeout(300)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_src_010(self):
        runConvolution("CPU-OV", "NoAngel.wav", "src_010.wav", "Spaces/18.wav", "NoAngelAON18.wav")

    @allure.title("CONV_SRC_011")
    @allure.description("""Uniform partitioned CPU""")
    @pytest.mark.timeout(300)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_src_011(self):
        runConvolution("CPU-UN", "NoAngel.wav", "src_011.wav", "Spaces/18.wav", "NoAngelAON18.wav")

    @allure.title("CONV_SRC_012")
    @allure.description("""Non-uniform partitioned CPU""")
    @pytest.mark.timeout(300)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_src_012(self):
        runConvolution("CPU-NU", "NoAngel.wav", "src_012.wav", "Spaces/18.wav", "NoAngelAON18.wav")
