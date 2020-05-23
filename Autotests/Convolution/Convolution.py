"""This file contains autotests for TALibTestConvolution"""

import allure
import pytest
import soundfile
import subprocess
import os
import sys

"""VARIABLES"""
RES_PATH = "C:/TestResources/TAN_Resources/"
last_output_name=""

"""STEPS"""

@allure.step
def step_launch_process(command):
    if sys.platform.startswith("win"):
        # to supress windows errors
        import ctypes
        SEM_NOGPFAULTERRORBOX = 0x0002
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
        subprocess_flags = 0x8000000
    else:
        subprocess_flags = 0
    process = subprocess.Popen(command, creationflags=subprocess_flags)
    return process

@allure.step
def step_check_return_code(process):
    streamdata = process.communicate()[0]
    rc = process.returncode
    assert rc == 0

@allure.step
def step_turn_files_to_array(file, gold_file):
    return soundfile.read(file), soundfile.read(gold_file)

@allure.step
def step_calculate_metrics(data, gold):
    x, y, xy, xx, yy, sq_diff = (0,0,0,0,0,0)
    n = len(data)
    for i, j in zip(data, gold):
        x += i[0]; x += i[1]
        y += j[0]; y += j[1]
        xy += i[0]*j[0]; xy += i[1]*j[1]
        xx += i[0]**2; xx += i[1]**2
        yy += j[0]**2; yy += j[1]**2
        sq_diff += (i[0]-j[0])**2; sq_diff += (i[1]-j[1])**2
    rmse = (sq_diff/n)**0.5
    correaltion = (n*xy-x*y)/(((n*xx-x**2)*(n*yy-y**2))**0.5)
    return rmse, correaltion

@allure.step
def step_validate_rmse(rmse):
    pass

@allure.step
def step_validate_correlation(correlation):
    pass

"""TESTS"""
@allure.sub_suite("Smoke")
@allure.parent_suite(os.environ['ENVNAME'])
class TestSmoke:
    @allure.title("CONV_SM_001")
    @allure.description("""
    Overlap Add GPU
    """)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-53', 'GPU-OV causes error')
    @pytest.mark.xfail(condition=lambda: True, reason='Error after outputing file')
    def test_conv_001(self):
        process = step_launch_process(["../../TAN/TALibTestConvolution.exe", "GPU-OV", 
        RES_PATH + "Originals/smokeIn.wav", "../../TAN/Results/conv_001.wav", 
        RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../../TAN/Results/conv_001.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
        allure.attach.file('../../TAN/Results/conv_001.wav','output.wav', extension='wav')
        
    @allure.title("CONV_SM_002")
    @allure.description("""
    Uniform Partitioned GPU
    """)
    def test_conv_002(self):
        process = step_launch_process(["../../TAN/TALibTestConvolution.exe", "GPU-UN", 
        RES_PATH + "Originals/smokeIn.wav", "../../TAN/Results/conv_002.wav", 
        RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../../TAN/Results/conv_002.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
        allure.attach.file('../../TAN/Results/conv_002.wav','output.wav', extension='wav')

    @allure.title("CONV_SM_003")
    @allure.description("""
    Non-uniform partitioned GPU
    """)
    def test_conv_003(self):
        process = step_launch_process(["../../TAN/TALibTestConvolution.exe", "GPU-NU", 
        RES_PATH + "Originals/smokeIn.wav", "../../TAN/Results/conv_003.wav", 
        RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../../TAN/Results/conv_003.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
        allure.attach.file('../../TAN/Results/conv_003.wav','output.wav', extension='wav')

    @allure.title("CONV_SM_004")
    @allure.description("""
    Overlap Add CPU
    """)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_004(self):
        process = step_launch_process(["../../TAN/TALibTestConvolution.exe", "CPU-OV", 
        RES_PATH + "Originals/smokeIn.wav", "../../TAN/Results/conv_004.wav", 
        RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../../TAN/Results/conv_004.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
        allure.attach.file('../../TAN/Results/conv_004.wav','output.wav', extension='wav')

    @allure.title("CONV_SM_005")
    @allure.description("""
    Uniform partitioned CPU
    """)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_005(self):
        process = step_launch_process(["../../TAN/TALibTestConvolution.exe", "CPU-UN", 
        RES_PATH + "Originals/smokeIn.wav", "../../TAN/Results/conv_005.wav", 
        RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../../TAN/Results/conv_005.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
        allure.attach.file('../../TAN/Results/conv_005.wav','output.wav', extension='wav')

    @allure.title("CONV_SM_006")
    @allure.description("""
    Non-uniform partitioned CPU
    """)
    @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
    @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
    def test_conv_006(self):
        process = step_launch_process(["../../TAN/TALibTestConvolution.exe", "CPU-NU", 
        RES_PATH + "Originals/smokeIn.wav", "../../TAN/Results/conv_006.wav", 
        RES_PATH + "IRs/testresponse.wav"])
        step_check_return_code(process)
        data, gold = step_turn_files_to_array("../../TAN/Results/conv_006.wav", RES_PATH + "GoldSamples/conv_001.wav")
        rmse, correlation = step_calculate_metrics(data[0], gold[0])
        step_validate_rmse(rmse)
        step_validate_correlation(correlation)
        allure.attach.file('../../TAN/Results/conv_006.wav','output.wav', extension='wav')

"""FIXTURES"""

@pytest.fixture(scope='module')
def attachOutput():
    yield
    allure.attach.file('../../TAN/Results/'+last_output_name,'output.wav', extension='wav')