cd C:\user\jon\code\pysparrow_root\trunk\build_and_install
xcopy ..\pySPARROW\waterbody.py pySPARROW\waterbody.py /Y
xcopy ..\pySPARROW\utils.py pySPARROW\utils.py /Y
xcopy ..\pySPARROW\reach.py pySPARROW\reach.py /Y
xcopy ..\pySPARROW\network.py pySPARROW\network.py /Y
xcopy ..\pySPARROW\database.py pySPARROW\database.py /Y
python setup.py bdist_egg
easy_install dist/pySPARROW-0.4-py2.4.egg
pause