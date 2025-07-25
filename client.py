import socket
import os
import threading

SERVER_IP = "127.0.0.1"  # IP do servidor
SERVER_PORT = 1234
CLIENT_PORT = 1235
PUBLIC_FOLDER = "public"
DOWNLOADS_FOLDER = "downloads"


def listen_for_downloads():
    """Escuta na porta 1235 e envia arquivos quando outro cliente pede."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", CLIENT_PORT))
    server.listen(5)
    print(f"[CLIENTE] Aguardando downloads na porta {CLIENT_PORT}...")

    while True:
        conn, addr = server.accept()
        data = conn.recv(1024).decode().strip()
        parts = data.split()
        if parts[0] == "GET":
            filename = parts[1]
            offset_start = int(parts[2])
            offset_end = int(parts[3]) if len(parts) > 3 else None

            filepath = os.path.join(PUBLIC_FOLDER, filename)
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    f.seek(offset_start)
                    data = f.read() if offset_end is None else f.read(offset_end - offset_start)
                    conn.sendall(data)
        conn.close()


def connect_to_server():
    """Conecta-se ao servidor Napster-like."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))

    ip_address = client.getsockname()[0]
    client.sendall(f"JOIN {ip_address}\n".encode())
    print(client.recv(1024).decode())

    # Enviar arquivos da pasta /public
    if not os.path.exists(PUBLIC_FOLDER):
        os.makedirs(PUBLIC_FOLDER)

    for filename in os.listdir(PUBLIC_FOLDER):
        path = os.path.join(PUBLIC_FOLDER, filename)
        if os.path.isfile(path):
            size = os.path.getsize(path)
            msg = f"CREATEFILE {filename} {size}\n"
            client.sendall(msg.encode())
            print(client.recv(1024).decode())

    return client


def baixar_arquivo(ip, filename):
    """Baixa arquivo de outro cliente."""
    if not os.path.exists(DOWNLOADS_FOLDER):
        os.makedirs(DOWNLOADS_FOLDER)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, CLIENT_PORT))
    client.sendall(f"GET {filename} 0\n".encode())

    filepath = os.path.join(DOWNLOADS_FOLDER, filename)
    with open(filepath, "wb") as f:
        while True:
            data = client.recv(4096)
            if not data:
                break
            f.write(data)
    client.close()
    print(f"[DOWNLOAD] Arquivo salvo em: {filepath}")


def menu(client):
    """Menu interativo do cliente."""
    while True:
        print("\n--- MENU CLIENTE ---")
        print("1. Buscar arquivo")
        print("2. Baixar arquivo")
        print("3. Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            padrao = input("Digite o padrão de busca: ")
            client.sendall(f"SEARCH {padrao}\n".encode())

            client.settimeout(1)
            try:
                while True:
                    resposta = client.recv(1024).decode().strip()
                    if not resposta:
                        break
                    print(resposta)
            except socket.timeout:
                client.settimeout(None)

        elif opcao == "2":
            ip = input("Digite o IP do cliente que possui o arquivo: ")
            filename = input("Digite o nome do arquivo: ")
            baixar_arquivo(ip, filename)

        elif opcao == "3":
            client.sendall(b"LEAVE\n")
            print(client.recv(1024).decode())
            break


if __name__ == "__main__":
    threading.Thread(target=listen_for_downloads, daemon=True).start()
    cliente = connect_to_server()
    menu(cliente)
    cliente.close()
