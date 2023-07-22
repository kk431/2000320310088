import socket
import json

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_odd_numbers():
    return [num for num in range(1, 24) if num % 2 != 0]

def generate_fibonacci_numbers(n):
    fibonacci = [1, 2]
    while len(fibonacci) < n:
        next_num = fibonacci[-1] + fibonacci[-2]
        fibonacci.append(next_num)
    return fibonacci

def handle_request(request):
    if request == 'GET /numbers/primes HTTP/1.1':
        primes = [num for num in range(1, 24) if is_prime(num)]
        response = {'numbers': primes}
    elif request == 'GET /numbers/odd HTTP/1.1':
        odds = generate_odd_numbers()
        response = {'numbers': odds}
    elif request == 'GET /numbers/fibo HTTP/1.1':
        fibo = generate_fibonacci_numbers(14)  # Generate 14 Fibonacci numbers
        response = {'numbers': fibo}
    else:
        response = {'error': 'Endpoint not found'}

    return "HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + json.dumps(response)

def start_server():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on http://{host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            request_data = client_socket.recv(1024).decode('utf-8')

            # Assuming the first line of the request is the GET request
            request_line = request_data.split('\n')[0]
            response_data = handle_request(request_line)

            client_socket.sendall(response_data.encode('utf-8'))
            client_socket.close()

    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()

if __name__ == "__main__":
    start_server()
