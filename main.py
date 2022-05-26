from multiprocessing import Process
from client import listen

# import subprocess
#
# subprocess.Popen(["python", "/home/hlukhau/PycharmProjects/video/client.py", "5556"])
# subprocess.Popen(["python", "/home/hlukhau/PycharmProjects/video/client.py", "5557"])
# subprocess.Popen(["python", "/home/hlukhau/PycharmProjects/video/client.py", "5558"])

proc1 = Process(target=listen, args=('5556', '', ''))
proc1.start()

proc2 = Process(target=listen, args=('5557', '', ''))
proc2.start()

proc3 = Process(target=listen, args=('5558', '', ''))
proc3.start()



