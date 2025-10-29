import socket
import hashlib
import time
import threading



SERVER_IP_SYNC = "58.17.00.01"
SERVER_PORT_SYNC = 3211

SERVER_IP_ASYNC = "58.17.00.02"
SERVER_PORT_ASYNC = 3212


REGISTRATION_NUMBER = 20229005817
NAME = "Anna Beatriz Barbosa de Godoy"

MAX_REQUESTS = 10

start_time = [0]*MAX_REQUESTS
end_time = [0]*MAX_REQUESTS


def generate_custom_id(registration_number: int, name: str) -> str:

    custom_id = f"{registration_number} {name}"
    custom_id_hash = hashlib.sha1(custom_id.encode("utf-8")).hexdigest()

    return custom_id_hash


def send_request(server_ip: str, server_port: int, message: str, registration_number: int, name: str) -> None:

    custom_id = generate_custom_id(registration_number, name)
    request_message = [
        "\r\n",
        "GET / HTTP/1.1\r\n",
        f"Host: {server_ip}\r\n",
        f"X-Custom-ID: {custom_id}\r\n",
        "Connection: close\r\n",
        "\r\n"
    ]
    request_message.append(message)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.connect((server_ip, server_port))
            connection.sendall("".join(request_message).encode('utf-8'))
            response_data = b""
            while True:
                chunk = connection.recv(1024)
                if not chunk:
                    break
                response_data += chunk
            print("[CLIENTE] Resposta do servidor:", response_data.decode('utf-8'))

    except ConnectionRefusedError:
        print(f"[CLIENTE] Falha ao conectar ao servidor {server_ip}:{server_port}.")
        print("[CLIENTE] Verifique se o servidor está em execução e tente novamente.")
        exit(1)

    except Exception as e:
        print(f"[CLIENTE] Ocorreu um erro: {e}")


def send_request_async(server_ip: str, server_port: int, message: str, registration_number: int, name: str, number_request: int) -> None:
    def make_request():
        start_time[number_request - 1] = time.time()
        custom_id = generate_custom_id(registration_number, name)
        request_message = [
            "\r\n",
            "GET / HTTP/1.1",
            f"Host: {server_ip}",
            f"X-Custom-ID: {custom_id}",
            "Connection: close",
            "\r\n"
        ]
        request_message.append(message)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
                connection.connect((server_ip, server_port))
                connection.sendall("".join(request_message).encode('utf-8'))
                response_data = b""
                while True:
                    chunk = connection.recv(1024)
                    if not chunk:
                        break
                    response_data += chunk
                print("[CLIENTE] Resposta do servidor:", response_data.decode('utf-8'))
                end_time[number_request - 1] = time.time()
                print(f"[CLIENTE] Tempo de resposta para a requisição {number_request}: {end_time[number_request - 1] - start_time[number_request - 1]:.4f} segundos")

        except ConnectionRefusedError:
            print(f"[CLIENTE] Falha ao conectar ao servidor {server_ip}:{server_port}.")
            print("[CLIENTE] Verifique se o servidor está em execução e tente novamente.")
            exit(1)

        except Exception as e:
            print(f"[CLIENTE] Ocorreu um erro: {e}")


    thread = threading.Thread(target=make_request)
    thread.start()


def menu():
    print("Selecione o tipo de servidor para se conectar:")
    print(f"1 - Enviar {MAX_REQUESTS} requisições[sync] para o servidor Síncrono")
    print(f"2 - Enviar {MAX_REQUESTS} requisições[sync] para o servidor Assíncrono")
    print(f"3 - Enviar {MAX_REQUESTS} requisições[async] para o servidor Síncrono")
    print(f"4 - Enviar {MAX_REQUESTS} requisições[async] para o servidor Assíncrono")
    print("0 - Sair do programa")
    result = input("Digite 1, 2 , 3, 4 ou 0: ")
    # result = "1"
    return result

if __name__ == "__main__":
    choice = menu()
    if choice not in ["1", "2", "3", "4"]:
        print("Escolha inválida. Encerrando o programa.")
        exit(1)

    elif choice == "1":
        for i in range(1, MAX_REQUESTS+1):
            MESSAGE = f"Olá, este é um teste de comunicação[sync] com o servidor síncrono número {i}."
            start_time[i - 1] = time.time()
            send_request(SERVER_IP_SYNC, SERVER_PORT_SYNC, MESSAGE, (REGISTRATION_NUMBER + i), NAME)
            end_time[i - 1] = time.time()
            print(f"[CLIENTE] Tempo de resposta para a requisição {i}: {end_time[i - 1] - start_time[i - 1]:.4f} segundos")

    elif choice == "2":
        for i in range(1, MAX_REQUESTS+1):
            MESSAGE = f"Olá, este é um teste de comunicação[sync] com o servidor assíncrono número {i}."
            start_time[i - 1] = time.time()
            send_request(SERVER_IP_ASYNC, SERVER_PORT_ASYNC, MESSAGE, (REGISTRATION_NUMBER + i), NAME)
            end_time[i - 1] = time.time()
            print(f"[CLIENTE] Tempo de resposta para a requisição {i}: {end_time[i - 1] - start_time[i - 1]:.4f} segundos")

    elif choice == "3":
        for i in range(1, MAX_REQUESTS+1):
            MESSAGE = f"Olá, este é um teste de comunicação[async] com o servidor síncrono número {i}."
            send_request_async(SERVER_IP_SYNC, SERVER_PORT_SYNC, MESSAGE, (REGISTRATION_NUMBER + i), NAME, i)

    elif choice == "4":
        for i in range(1, MAX_REQUESTS+1):
            MESSAGE = f"Olá, este é um teste de comunicação[async] com o servidor assíncrono número {i}."
            send_request_async(SERVER_IP_ASYNC, SERVER_PORT_ASYNC, MESSAGE, (REGISTRATION_NUMBER + i), NAME, i)




    print("[CLIENTE] Todas as requisições foram enviadas.")
