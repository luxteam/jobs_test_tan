set PATH=c:\python35\;c:\python35\scripts\;%PATH%

python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install -r requirements.txt

pytest --alluredir=../allure-results %1
REM allure generate -c ../allure-results -o ../Report