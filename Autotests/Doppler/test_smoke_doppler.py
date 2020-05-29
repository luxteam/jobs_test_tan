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
@allure.sub_suite("Smoke")
@allure.suite("Doppler")
@allure.parent_suite(get_gpu() + " " + platform.system() + " " + platform.release())
@pytest.mark.usefixtures("resultsDir", "attachOutput")
class TestSmoke:
    @allure.title("DOPP_SM_001")
    @allure.description("""Simple GPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https:\\\\adc.luxoft.com\\jira\\browse\\STVITT-77', 'GPU mode doesn\'t work')
    def test_dopp_001(self):
        process = step_launch_process(["..\\TAN\\TALibDopplerTest.exe", RES_PATH + "Rooms\\default.xml",
        RES_PATH + "Originals\\smokeIn.wav", "..\\Results\\dopp_001.wav", "1", "GPU"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("..\\Results\\dopp_001.wav", RES_PATH + "GoldSamples\\dopp_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
        
    @allure.title("DOPP_SM_002")
    @allure.description("""Simple CPU""")
    @pytest.mark.timeout(150)
    def test_dopp_002(self):
        process = step_launch_process(["..\\TAN\\TALibDopplerTest.exe", RES_PATH + "Rooms\\default.xml",
        RES_PATH + "Originals\\smokeIn.wav", "..\\Results\\dopp_002.wav", "1", "CPU"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("..\\Results\\dopp_002.wav", RES_PATH + "GoldSamples\\dopp_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)

    @allure.title("DOPP_SM_003")
    @allure.description("""Max bounces = 2 GPU""")
    @allure.issue('https:\\\\adc.luxoft.com\\jira\\browse\\STVITT-77', 'GPU mode doesn\'t work')
    @pytest.mark.timeout(150)
    def test_dopp_003(self):
        process = step_launch_process(["..\\TAN\\TALibDopplerTest.exe", RES_PATH + "Rooms\\default.xml",
        RES_PATH + "Originals\\smokeIn.wav", "..\\Results\\dopp_003.wav", "2", "GPU"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("..\\Results\\dopp_003.wav", RES_PATH + "GoldSamples\\dopp_003.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)

    @allure.title("DOPP_SM_004")
    @allure.description("""Max bounces = 2 CPU""")
    @pytest.mark.timeout(150)
    def test_dopp_004(self):
        process = step_launch_process(["..\\TAN\\TALibDopplerTest.exe", RES_PATH + "Rooms\\default.xml",
        RES_PATH + "Originals\\smokeIn.wav", "..\\Results\\dopp_004.wav", "2", "CPU"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("..\\Results\\dopp_004.wav", RES_PATH + "GoldSamples\\dopp_003.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
