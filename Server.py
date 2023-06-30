from functools import partial
from http.server import SimpleHTTPRequestHandler, test
import subprocess
import threading
import base64
import os
import shutil
import json

class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        global Users
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
        else:
            name,ps=base64.b64decode(self.headers.get("Authorization")[6:].encode()).decode().split(":")
            if not name in Users:
                os.mkdir(f"./Test_dr/{name}")
                shutil.copyfile("Lab1.ipynb", f"./Test_dr/{name}/Lab1.ipynb")
                Users[name]=ps
                with open('Users.json', 'w') as fp:
                    json.dump(Users, fp)
            if Users[name]==ps:
                self.send_response(307)
                self.send_header('Location',f"http://127.0.0.1:8080/notebooks/Test_dr/{name}/Lab1.ipynb")
                self.end_headers()
            else:
                self.do_AUTHHEAD()
def Start():
    global free_ports
    cmd='....\\jupyter-notebook.exe' #Адрес к jupyter-notebook
    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, stdout=PIPE, stderr=subprocess.STDOUT, close_fds=True)
    while True:
        s = p.stdout.readline()
        if not s:
            print("End")
            break

if __name__ == "__main__":
    with open('Users.json') as json_file:
        Users = json.load(json_file)
    audio_thread = threading.Thread(target=Start)
    audio_thread.start()
    handler_class = partial(AuthHTTPRequestHandler)
    test(HandlerClass=handler_class, port=8000, bind="127.0.0.1")