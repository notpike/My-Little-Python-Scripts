import socket
s = socket.socket()
s.settimeout(2)

user = "root"
passwd = "password"

length = str(len(user) + len(passwd) + 5)

req = """POST /python/login1.php HTTP/1.1
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

req3 = user + "&p=" + passwd


target = 'ad.samsclass.info'

s.connect((target, 80))
s.send(req + length + req2 + req3)
#s.send('HEAD / HTTP/1.1\nHost: ' + target + '\n\n')
print s.recv(1024)
s.close()
