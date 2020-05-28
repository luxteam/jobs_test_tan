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
from system_info import get_gpu

"""TESTS"""

@allure.parent_suite(get_gpu() + " " + platform.system() + " " + platform.release())
@allure.suite("Convolution")
@allure.sub_suite("Smoke")
@pytest.mark.usefixtures("resultsDir", "attachOutput")
class TestSmoke:
    @allure.title("CONV_SM_001")
    @allure.description("""Overlap Add GPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-53', 'GPU-OV causes error')
    @pytest.mark.xfail(condition=lambda: True, reason='Error after outputing file')
    def test_conv_001(self):
        process = step_launch_process(["../TAN/cmake-TALibTestConvolution-bin/TALibTestConvolution.exe", "GPU-OV", 
            RES_PATH + "Originals/smokeIn.wav", "../Results/conv_001.wav", 
            RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../Results/conv_001.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
        
    @allure.title("CONV_SM_002")
    @allure.description("""Uniform Partitioned GPU""")
    @pytest.mark.timeout(150)
    def test_conv_002(self):
        process = step_launch_process(["../TAN/cmake-TALibTestConvolution-bin/TALibTestConvolution.exe", "GPU-UN", 
            RES_PATH + "Originals/smokeIn.wav", "../Results/conv_002.wav", 
            RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../Results/conv_002.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)

    @allure.title("CONV_SM_003")
    @allure.description("""Non-uniform partitioned GPU""")
    @pytest.mark.timeout(150)
    def test_conv_003(self):
        process = step_launch_process(["../TAN/cmake-TALibTestConvolution-bin/TALibTestConvolution.exe", "GPU-NU", 
            RES_PATH + "Originals/smokeIn.wav", "../Results/conv_003.wav", 
            RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../Results/conv_003.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)

    @allure.title("CONV_SM_004")
    @allure.description("""Overlap Add CPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_004(self):
        process = step_launch_process(["../TAN/cmake-TALibTestConvolution-bin/TALibTestConvolution.exe", "CPU-OV", 
            RES_PATH + "Originals/smokeIn.wav", "../Results/conv_004.wav", 
            RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../Results/conv_004.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)

    @allure.title("CONV_SM_005")
    @allure.description("""Uniform partitioned CPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_005(self):
        process = step_launch_process(["../TAN/cmake-TALibTestConvolution-bin/TALibTestConvolution.exe", "CPU-UN", 
            RES_PATH + "Originals/smokeIn.wav", "../Results/conv_005.wav", 
            RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../Results/conv_005.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)

    @allure.title("CONV_SM_006")
    @allure.description("""Non-uniform partitioned CPU""")
    @pytest.mark.timeout(150)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_006(self):
        process = step_launch_process(["../TAN/cmake-TALibTestConvolution-bin/TALibTestConvolution.exe", "CPU-NU", 
            RES_PATH + "Originals/smokeIn.wav", "../Results/conv_006.wav", 
            RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../Results/conv_006.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
