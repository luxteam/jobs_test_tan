set PATH=c:\python35\;c:\python35\scripts\;%PATH%

python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install --upgrade -r requirements.txt

if %1 == FULL (pytest --alluredir=../allure-results ../Autotests/Convolution/ ../Autotests/Doppler/) else (pytest --alluredir=../allure-results ../Autotests/%1/)
REM allure generate -c ../allure-results -o ../Report