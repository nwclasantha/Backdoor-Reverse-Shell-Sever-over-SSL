import socket
import sys
import logging
from OpenSSL import SSL

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("client.log"),  # Log to a file
        logging.StreamHandler(sys.stdout)   # Log to the console
    ]
)

class SSLClient:
    def __init__(self, host, port, certfile):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.certfile = certfile
        self.ssl_sock = None

    def setup_connection(self):
        """Set up SSL connection to the server."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ctx = SSL.Context(SSL.SSLv23_METHOD)
            ctx.use_certificate_file(self.certfile)
            self.ssl_sock = SSL.Connection(ctx, sock)
            self.ssl_sock.connect(self.address)
            logging.info(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            logging.critical(f"Failed to connect to server at {self.host}:{self.port}. Exception: {e}")
            sys.exit(1)

    def send_command(self, command):
        """Send command to the server and receive the response."""
        try:
            logging.info(f"Sending command: {command}")
            self.ssl_sock.sendall(command.encode())  # Send the command
            data = self.ssl_sock.recv(66384).decode()  # Receive server's response
            logging.info(f"Received response: {data.strip()}")
            return data
        except Exception as e:
            logging.error(f"An error occurred while sending command: {e}")
            return None

    def close_connection(self):
        """Close the SSL connection."""
        if self.ssl_sock:
            self.ssl_sock.close()
            logging.info("Connection closed.")

def main():
    # Server details
    host = '192.168.0.200'
    port = 31337
    certfile = 'server.crt'

    # Create SSLClient instance
    client = SSLClient(host, port, certfile)

    # Setup connection to the server
    client.setup_connection()

    # Command loop
    try:
        while True:
            cmd = input('$ ')
            if cmd.lower() in ['exit', 'quit']:
                logging.info("Exiting client.")
                break
            response = client.send_command(cmd)
            if response:
                print(response)
    except KeyboardInterrupt:
        logging.info("Client exiting on KeyboardInterrupt...")
    finally:
        # Close the connection when done
        client.close_connection()

if __name__ == '__main__':
    main()
