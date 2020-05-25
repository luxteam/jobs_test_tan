# Autotests for TAN project

To run autotests, first make sure: 
1) Your TanResources folder is located in C:/TestResources/ (for windows) or in $CIS_TOOLS/../TestResources/ (for unix)
2) You have pip installed
3) You have placed TAN executables in autotests root directory and folder with executables is called TAN

To run autotests:
1) Go to Launcher folder
2) Use run.bat {arg} or run.sh {arg}

Examples of run.bat usage:
1) .\run.bat Convolution --- runs all test groups from /Autotests/Convolution folder
2) .\run.bat Convolution/test_smoke_convolution.py --- runs Smoke test group for Convolution
3) .\run.bat Doppler --- runs all test groups from /Autotests/Doppler folder
4) .\run.bat FULL --- runs all autotests
