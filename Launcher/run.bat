set PATH=c:\python35\;c:\python35\scripts\;%PATH%
python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install -r requirements.txt
pytest ../Autotests/Convolution/Convolution.py --alluredir=../allure-results