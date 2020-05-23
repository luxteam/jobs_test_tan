"""This file contains autotests for TALibTestConvolution"""

import os
import sys
import ctypes
import subprocess
import soundfile
import pytest
import allure


"""VARIABLES"""
RES_PATH = "C:/TestResources/TanResources/"
METHODS_LIST = ["CPU-OV", "CPU-NU", "CPU-ON", "GPU-OV", "GPU-NU", "GPU-UN"]
last_output_name = ""


"""STEPS"""
@allure.step
def step_launch_process(command):
    if sys.platform.startswith("win"):
        # Don't display the Windows GPF dialog if the invoked program dies.
        # See comp.os.ms-windows.programmer.win32
        # How to suppress crash notification dialog?, Jan 14,2004 -
        # Raymond Chen's response [1]
        SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
        subprocess_flags = 0x8000000 #win32con.CREATE_NO_WINDOW?
    else:
        subprocess_flags = 0
    process = subprocess.Popen(command, creationflags=subprocess_flags)
    last_output_name = command[3]
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
    assert correlation > 0.95

"""TESTS"""

# @allure.title("CONV_SM_001")
# @allure.description("""
# Overlap Add GPU
# Bedroom Closet
# """)
# @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-53', 'GPU-OV causes error')
# @pytest.mark.xfail(condition=lambda: True, reason='Error after outputing file')
# def test_src_001():
#     process = step_launch_process(["../../TAN_Resources/TALibTestConvolution.exe", "GPU-OV", 
#     "../../TAN_Resources/Originals/01_Original.wav", "../../TAN_Resources/Results/src_001.wav", 
#     "../../TAN_Resources/IRs/02_IR_Bedroom_Closet.wav"])
#     step_check_return_code(process)
#     data, gold = step_turn_files_to_array("../../TAN_Resources/Results/src_001.wav", "../../TAN_Resources/Originals/02_Bedroom_Closet.wav")
#     rmse, correlation = step_calculate_metrics(data[0], gold[0])
#     step_validate_rmse(rmse)
#     step_validate_correlation(correlation)
#     allure.attach.file('../../TAN_Resources/Results/src_001.wav','output.wav', extension='wav')
    
# @allure.title("CONV_SM_002")
# @allure.description("""
# Uniform Partitioned GPU
# Bedroom Closet
# """)
# def test_src_002():
#     process = step_launch_process(["../../TAN_Resources/TALibTestConvolution.exe", "GPU-UN", 
#     "../../TAN_Resources/Originals/01_Original.wav", "../../TAN_Resources/Results/src_002.wav", 
#     "../../TAN_Resources/IRs/02_IR_Bedroom_Closet.wav"])
#     step_check_return_code(process)
#     data, gold = step_turn_files_to_array("../../TAN_Resources/Results/src_002.wav", "../../TAN_Resources/Originals/02_Bedroom_Closet.wav")
#     rmse, correlation = step_calculate_metrics(data[0], gold[0])
#     step_validate_rmse(rmse)
#     step_validate_correlation(correlation)
#     allure.attach.file('../../TAN_Resources/Results/src_002.wav','output.wav', extension='wav')

# @allure.title("CONV_SM_003")
# @allure.description("""
# Non-uniform partitioned GPU
# Bedroom Closet
# """)
# def test_src_003():
#     process = step_launch_process(["../../TAN_Resources/TALibTestConvolution.exe", "GPU-NU", 
#     "../../TAN_Resources/Originals/01_Original.wav", "../../TAN_Resources/Results/src_003.wav", 
#     "../../TAN_Resources/IRs/02_IR_Bedroom_Closet.wav"])
#     step_check_return_code(process)
#     data, gold = step_turn_files_to_array("../../TAN_Resources/Results/src_003.wav", "../../TAN_Resources/Originals/02_Bedroom_Closet.wav")
#     rmse, correlation = step_calculate_metrics(data[0], gold[0])
#     step_validate_rmse(rmse)
#     step_validate_correlation(correlation)
#     allure.attach.file('../../TAN_Resources/Results/src_003.wav','output.wav', extension='wav')

# @allure.title("CONV_SM_004")
# @allure.description("""
# Overlap Add CPU
# Bedroom Closet
# """)
# @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
# @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
# def test_src_004():
#     process = step_launch_process(["../../TAN_Resources/TALibTestConvolution.exe", "CPU-OV", 
#     "../../TAN_Resources/Originals/01_Original.wav", "../../TAN_Resources/Results/src_004.wav", 
#     "../../TAN_Resources/IRs/02_IR_Bedroom_Closet.wav"])
#     step_check_return_code(process)
#     data, gold = step_turn_files_to_array("../../TAN_Resources/Results/src_004.wav", "../../TAN_Resources/Originals/02_Bedroom_Closet.wav")
#     rmse, correlation = step_calculate_metrics(data[0], gold[0])
#     step_validate_rmse(rmse)
#     step_validate_correlation(correlation)
#     allure.attach.file('../../TAN_Resources/Results/src_004.wav','output.wav', extension='wav')

# @allure.title("CONV_SM_005")
# @allure.description("""
# Uniform partitioned CPU
# Bedroom Closet
# """)
# @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
# @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
# def test_src_005():
#     process = step_launch_process(["../../TAN_Resources/TALibTestConvolution.exe", "CPU-UN", 
#     "../../TAN_Resources/Originals/01_Original.wav", "../../TAN_Resources/Results/src_005.wav", 
#     "../../TAN_Resources/IRs/02_IR_Bedroom_Closet.wav"])
#     step_check_return_code(process)
#     data, gold = step_turn_files_to_array("../../TAN_Resources/Results/src_005.wav", "../../TAN_Resources/Originals/02_Bedroom_Closet.wav")
#     rmse, correlation = step_calculate_metrics(data[0], gold[0])
#     step_validate_rmse(rmse)
#     step_validate_correlation(correlation)
#     allure.attach.file('../../TAN_Resources/Results/src_005.wav','output.wav', extension='wav')

# @allure.title("CONV_SM_006")
# @allure.description("""
# Non-uniform partitioned CPU
# Bedroom Closet
# """)
# @allure.issue('https://adc.luxoft.com/jira/browse/STVITT-54', 'CPU modes don\'t work')
# @pytest.mark.xfail(condition=lambda: True, reason='CPU mode does not work')
# def test_src_006():
#     process = step_launch_process(["../../TAN_Resources/TALibTestConvolution.exe", "CPU-NU", 
#     "../../TAN_Resources/Originals/01_Original.wav", "../../TAN_Resources/Results/src_006.wav", 
#     "../../TAN_Resources/IRs/02_IR_Bedroom_Closet.wav"])
#     step_check_return_code(process)
#     data, gold = step_turn_files_to_array("../../TAN_Resources/Results/src_006.wav", "../../TAN_Resources/Originals/02_Bedroom_Closet.wav")
#     rmse, correlation = step_calculate_metrics(data[0], gold[0])
#     step_validate_rmse(rmse)
#     step_validate_correlation(correlation)
#     allure.attach.file('../../TAN_Resources/Results/src_006.wav','output.wav', extension='wav')

@allure.title("CONV_SM_007")
@allure.description("""
Guitar with Boxboro Vintage (Dynamic)
""")
@pytest.mark.parametrize('method', METHODS_LIST)
@pytest.mark.parametrize('input_response_gold', [
    ("EiroNarethMadworld.wav", "Boxboro Vintage-dynamic.wav", "EiroNarethMadworld.wav")
])
def test_src(method, input_response_gold):
    process = step_launch_process(["../../TAN/TALibTestConvolution.exe", method, 
    RES_PATH + "Originals/" + input_response_gold[0], "../../TAN/Results/"+input_response_gold[0]+"-"+method, 
    RES_PATH + "IRs/" + input_response_gold[1]])
    step_check_return_code(process)
    data, gold = step_turn_files_to_array("../../TAN/Results/"+input_response_gold[0]+"-"+method, RES_PATH + "GoldSamples/"+input_response_gold[2])
    rmse, correlation = step_calculate_metrics(data[0], gold[0])
    step_validate_rmse(rmse)
    step_validate_correlation(correlation)
    allure.attach.file('../../TAN/Results/'+input_response_gold[0]+"-"+method,'output.wav', extension='wav')

"""FIXTURES"""

@pytest.fixture(scope='module')
def attachOutput():
    yield
    allure.attach.file('../../TAN_Resources/Results/'+last_output_name,'output.wav', extension='wav')