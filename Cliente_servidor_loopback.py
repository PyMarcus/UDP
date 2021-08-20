# criando um cliente servidor  udp na propria máquina (loopback)

# local host
import socket
import argparse
from datetime import datetime

# definindo o tamanho maior que o datagrama udp
max_bytes = 65535


# criando o servidor:
def server(port):
    # estabelecendo o socket e especificando nele que é da familia de protocolos internet e udp
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # atribuindo um endereço e porta ao servidor:
    sock.bind(('127.0.0.1', port))
    # mostrando onde está ouvindo (endereço local do próprio serv)
    print(f'Ouvindo em {sock.getsockname()}')

    # criando loop para ler as mensagens
    while True:
        # determinando o tamanho máximo das msg, esperando o cliente para pegar o endereço e porta do mesmo
        data, address = sock.recvfrom(max_bytes)
        text = data.decode('ascii')
        print(f'O cliente em {address} diz {text}')
        text = f'Seus dados tiveram {len(data)} bytes de tamanho'
        data = text.encode('ascii')
        # enviando para o servidor de destino
        sock.sendto(data, address)

# criando o cliente:
def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = f'Enviada em {datetime.now()}'
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.0.1', port))
    x = str(input('>>> '))
    d = x.encode('ascii')
    sock.sendto(d, ('127.0.0.1', port))
    print(f'O sistema operacional me deu o endereco {sock.getsockname()}')
    data, address = sock.recvfrom(max_bytes)
    text = data.decode('ascii')
    print(f'O servidor {address} respondeu {text}')


# atribuindo a porta:
if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Envie e recebe UDP localmente')
    parser.add_argument('role', choices=choices, help='Troque role para iniciar')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060)
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
