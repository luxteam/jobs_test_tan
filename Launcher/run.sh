set PATH=c:\python35\;c:\python35\scripts\;%PATH%

python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install -r requirements.txt

if [ $1 == "FULL" ] then
    pytest --alluredir=../allure-results ../Autotests/Convolution/ ../Autotests/Doppler/
else
    pytest --alluredir=../allure-results ../Autotests/$1/