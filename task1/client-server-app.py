import socket
import argparse
import eliza


parser = argparse.ArgumentParser(prog='Client-server app with sockets',
                                 description='', epilog='')

parser.add_argument('--protocol', default='TCP')
parser.add_argument('--role', default='client')

args = parser.parse_args()


def tcp_server():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    while True:
        bot = eliza.Eliza()
        bot.load('doctor.txt')
        server_socket.listen()
        conn, addr = server_socket.accept()
        with conn:
            conn.send((bot.initial()+'\n> ').encode())
            message = ''
            while True:
                message = conn.recv(1024).decode()
                response = bot.respond(message)
                if response:
                    response += '\n> '
                # print(message, response)
                if not response or message == 'bye\n' \
                                or message == 'goodbye\n' \
                                or message == 'quit\n':
                    conn.send((bot.final()+'\n').encode())
                    break
                conn.send(response.encode())
    server_socket.close()

def tcp_client():
    host = socket.gethostname()
    port = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        response = s.recv(1024).decode()
        print(response, end='')
        while response.lower().split('.')[0] != 'goodbye':
            message = input()
            s.send(message.encode())
            response = s.recv(1024).decode()
            print(response, end='')

def udp_server():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    while True:
        bot = eliza.Eliza()
        bot.load('doctor.txt')
        message, addr = server_socket.recvfrom(1024)
        server_socket.sendto((bot.initial()+'\n> ').encode(), addr)
        while True:
            message, addr = server_socket.recvfrom(1024)
            message = message.decode()
            response = bot.respond(message)
            if response:
                response += '\n> '
            if not response or message == 'bye\n' \
                            or message == 'goodbye\n' \
                            or message == 'quit\n':
                server_socket.sendto((bot.final()+'\n').encode(), addr)
                break
            server_socket.sendto(response.encode(), addr)
    server_socket.close()

def udp_client():
    host = socket.gethostname()
    port = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        message = 'Hello'
        s.sendto(message.encode(), (host, port))
        response, addr = s.recvfrom(1024)
        response = response.decode()
        print(response, end='')
        while response.lower().split('.')[0] != 'goodbye':
            message = input()
            s.sendto(message.encode(), (host, port))
            response, addr = s.recvfrom(1024)
            response = response.decode()
            print(response, end='')


if __name__ == '__main__':
    if args.protocol == 'TCP':
        if args.role == 'client':
            tcp_client()
        elif args.role == 'server':
            tcp_server()
        else:
            print('Incorrect role argument')
    elif args.protocol == 'UDP':
        if args.role == 'client':
            udp_client()
        elif args.role == 'server':
            udp_server()
        else:
            print('Incorrect role argument')
    else:
        print('Incorrect protocol')

