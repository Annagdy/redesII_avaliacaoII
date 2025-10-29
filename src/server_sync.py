import socket
import time


HOST = "0.0.0.0"
PORT = 3211


def handle_client_connection(conn: socket.socket, addr: tuple) -> None:
    print(f"Conexão estabelecida com {addr}")
    try:
        data = b""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk
            if b"." in data:
                break
        print(f"Dados recebidos: {data.decode('utf-8')}")
        request_number = data.decode('utf-8').split("número ")[1].split('.')[0]
        response = [
            "\r\n",
            "HTTP/1.1 200 OK\r\n",
            "Content-Type: text/plain\r\n",
            "Connection: close",
            "\r\n\r\n",
            f"Dados recebidos com sucesso do número {request_number}."
        ]

        time.sleep(1)

        conn.sendall("".join(response).encode('utf-8'))
    except Exception as e:
        print(f"[SÍNCRONO] Ocorreu um erro ao lidar com a conexão de {addr}: {e}")
    finally:
        print(f"[SÍNCRONO] Fechando conexão com {addr}")
        conn.close()
    print(f"[SÍNCRONO] Resposta enviada para {addr}")


def start_sync_server() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[SÍNCRONO] Servidor sequencial síncrono ouvindo em {HOST}:{PORT}...")

        while True:
            connection, addr = server_socket.accept()
            handle_client_connection(connection, addr)


if __name__ == "__main__":
    start_sync_server()
