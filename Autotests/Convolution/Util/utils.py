import os
import sys
import ctypes
import subprocess
import soundfile
import pytest
import allure
import random
import json
import string


"""VARIABLES"""
if sys.platform.startswith("win"):
    RES_PATH = "C:/TestResources/TanAssets/"
else:
    RES_PATH = os.getenv("HOME") + "/JN/TestResources/TanAssets/"
last_output_name = ""


"""FIXTURES"""
@pytest.fixture(scope="session")
def resultsDir():
    if(not os.path.exists("../Results")):
        os.mkdir("../Results")
    yield

@pytest.fixture(scope='function')
def attachOutput():
    yield
    global last_output_name
    allure.attach.file(last_output_name, 'output.wav', extension='wav')


"""STEPS"""
@allure.step
def step_launch_process(command):
    if sys.platform.startswith("win"):
        # to supress windows errors
        SEM_NOGPFAULTERRORBOX = 0x0002
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)
        subprocess_flags = 0x8000000
    else:
        subprocess_flags = 0
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess_flags)
    print(process.communicate()[0].decode('utf-8'))
    print(process.communicate()[1].decode('utf-8'))
    global last_output_name
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
    pass