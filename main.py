from subprocess import Popen

commands = [
    "C:\\Users\\DimaPC\\PycharmProjects\\video\\venv\\Scripts\\python.exe server.py",
    "C:\\Users\\DimaPC\\PycharmProjects\\video\\venv\\Scripts\\python.exe client.py 5556",
    "C:\\Users\\DimaPC\\PycharmProjects\\video\\venv\\Scripts\\python.exe client.py 5557"
]


procs = [ Popen(i) for i in commands ]
for p in procs:
   p.wait()