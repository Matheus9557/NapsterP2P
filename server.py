import socket
import threading

all_files = {}  # {ip: [ {filename, size}, ... ]}


def handle_client(conn, addr):
    ip_address = addr[0]
    print(f"[+] Conexão de {ip_address}")

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            print(f"[RECEBIDO de {ip_address}]: {data}")
            parts = data.split()
            command = parts[0].upper()

            if command == "JOIN":
                all_files[ip_address] = []
                conn.sendall(b"CONFIRMJOIN\n")

            elif command == "CREATEFILE":
                size = int(parts[-1])
                filename = " ".join(parts[1:-1])
                all_files[ip_address].append({"filename": filename, "size": size})
                conn.sendall(f"CONFIRMCREATEFILE {filename}\n".encode())

            elif command == "DELETEFILE":
                filename = " ".join(parts[1:])
                all_files[ip_address] = [
                    f for f in all_files[ip_address] if f["filename"] != filename
                ]
                conn.sendall(f"CONFIRMDELETEFILE {filename}\n".encode())

            elif command == "SEARCH":
                pattern = " ".join(parts[1:])
                for ip, files in all_files.items():
                    for f in files:
                        if pattern in f["filename"]:
                            resposta = f"FILE {f['filename']} {ip} {f['size']}\n"
                            conn.sendall(resposta.encode())

            elif command == "LEAVE":
                if ip_address in all_files:
                    del all_files[ip_address]
                conn.sendall(b"CONFIRMLEAVE\n")
                break

        except Exception as e:
            print(f"[ERRO] {e}")
            break

    conn.close()
    if ip_address in all_files:
        del all_files[ip_address]
    print(f"[-] {ip_address} desconectado")


def main():
    host = "0.0.0.0"
    port = 1234
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[SERVIDOR] Escutando na porta {port}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
