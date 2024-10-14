### **1. Server:**

In networking, a **server** is a system that listens for incoming connections from clients. It can be a physical machine or a virtual service that waits for clients to send requests. The server responds to these requests, providing the necessary resources or data.

#### **Objectives of the Server**:
- **Listen for Connections**: The server waits on a specific IP address and port for incoming client requests.
- **Authenticate Clients (if needed)**: The server can verify clients before accepting the connection, especially when using SSL/TLS, to ensure a secure communication channel.
- **Process Requests**: Once a client connects, the server processes the request, which can involve running commands, providing data, or performing operations.
- **Send Responses**: The server sends back the results or data to the client based on the request.
- **Maintain Secure Communication**: Using SSL/TLS, the server ensures that all communication between it and the client is encrypted and secure.

#### **Key Components**:
- **SSL/TLS Security**: The server loads its SSL certificate and private key, enabling it to provide secure communication through encryption.
- **Listening on a Port**: The server waits on a specific port (e.g., port 31337) for incoming client connections.
- **Handling Requests**: When the client sends a request (like a command), the server executes the necessary tasks and responds securely.
  
### **2. Client:**

A **client** in networking is any system or software that connects to a server to send requests or receive services. The client initiates the connection to the server and communicates securely in an SSL/TLS scenario.

#### **Objectives of the Client**:
- **Initiate Connection**: The client creates a connection to the server by specifying its IP address and port. In this case, it's `192.168.0.200:31337`.
- **Send Requests**: The client sends commands or requests to the server over the established connection. For example, it might send a shell command that the server is supposed to execute.
- **Receive Responses**: The client waits for the server’s response after sending a command. It then displays or processes the data it gets back.
- **Handle Secure Communication**: Just like the server, the client uses SSL/TLS to ensure that the data sent between it and the server is encrypted and cannot be easily intercepted or altered.

#### **Key Components**:
- **SSL/TLS Security**: The client uses the server's SSL certificate to ensure secure communication with encryption.
- **Sending Commands**: The client takes user input (e.g., a shell command like `ls -la`), encodes it, and sends it to the server.
- **Receiving Responses**: After sending the command, the client waits for the server's response and then displays it.

### **How They Work Together**:

In a typical client-server architecture with SSL/TLS security:
1. **Server Setup**: The server is set up with an IP address, port, and an SSL certificate for secure communication. It starts listening for incoming connections.
2. **Client Connection**: The client initiates a connection to the server using its IP and port, starting a secure SSL/TLS handshake to ensure encryption.
3. **Command Execution**: The client sends a command or request to the server. The server receives this, processes the command, and executes the requested task.
4. **Response**: The server sends back the result of the task to the client. The client displays the response or acts on the data received.
5. **Closing Connection**: Once the interaction is complete, the client or server can close the connection.

### **Objectives of the Combined System (Client-Server Communication)**:
- **Secure Data Transmission**: Using SSL/TLS, both the server and client ensure that all communication is encrypted and secure from potential attackers.
- **Separation of Concerns**: The server is responsible for handling tasks or commands, while the client only sends requests and receives results.
- **Ease of Use**: Clients interact with servers via simple commands. For example, the client can issue a shell command to the server, and the server will execute it and return the result.
- **Scalability**: The server can handle multiple clients by listening on the same IP and port. Each client can issue requests, and the server responds to them independently.

### **Real-World Example**:
In a secure web application:
- The **client** is your web browser (like Chrome or Firefox). When you visit a website, the browser initiates a connection to the web server using SSL (HTTPS).
- The **server** is the web server hosting the website. It listens for incoming connections from clients, processes requests (such as loading a webpage), and sends back the appropriate response (e.g., HTML content).

Similarly, in this case:
- The **client** is a script that sends commands to a server.
- The **server** executes the commands and returns the results over a secure, encrypted channel.

### Benefits of SSL/TLS in Client-Server Communication:
- **Encryption**: Data is encrypted, ensuring that no third party can read or tamper with it.
- **Authentication**: The server proves its identity to the client using an SSL certificate, helping prevent man-in-the-middle attacks.
- **Integrity**: Data integrity is maintained, ensuring that data sent between the client and server is not altered during transmission.

### Conclusion:
- **The server's role**: Listen for client connections, process commands securely, and respond with results.
- **The client’s role**: Initiate the connection, send requests, and handle responses while ensuring secure communication.
- **SSL/TLS**: Ensures that all data transmitted between the client and server is encrypted, authenticated, and safe from tampering.

This client-server architecture is widely used in secure communication systems, from websites (HTTPS) to remote command execution (as in this case).

### Create a Certificate Authority Root:
```
openssl genrsa -des3 -out ca.key 4096  
openssl req -new -x509 -days 365 -key ca.key -out ca.crt
```

### Create the Client Key and CSR:
```
openssl genrsa -des3 -out client.key 4096  
openssl req -new -key client.key -out client.csr  
# self-signed
openssl x509 -req -days 365 -in client.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out client.crt
```

### Convert Client Key to PKCS (It may be installed in most browsers):
```
openssl pkcs12 -export -clcerts -in client.crt -inkey client.key -out client.p12
```

### Convert Client Key to (combined) PEM:
Combines `client.crt` and `client.key` into a single PEM file for programs using OpenSSL.

```
openssl pkcs12 -in client.p12 -out client.pem -clcerts
```

### Command Output:

```
$ uname -a
Linux 4.2.3.3

$ whoami
root
```

### TCPDUMP showing encrypted communication:

```
[root@cl]# tcpdump -i ens192 dst 192.168.200.107 and -s 1024 -A tcp port 31337
```

**TCPDUMP Output:**
```
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode  
listening on ens192, link-type EN10MB (Ethernet), capture size 1024 bytes  

23:54:53.024601 IP SOURCE_IP.52689 > nexus.example.com.31337: Flags [S],  
seq 2690615083, win 64240, options [mss 1260,nop,wscale 0,nop,nop,sackOK], length 0  
E..4*.@.....>.~....k..zi._.+........................  

23:54:53.042655 IP SOURCE_IP.52689 > nexus.example.com.31337: Flags [.],  
ack 3152217485, win 64240, length 0  
E..(*.@.....>.~....k..zi._.,....P...<.........  

23:55:10.331534 IP SOURCE_IP.52689 > nexus.example.com.31337: Flags [P.],  
seq 0:247, ack 1, win 64240, length 247  
E...+.@.....>.~....k..zi._.,....P....J  
............V....@b...i....W.t&R..Z...ya  
..Z@....0.,.(.$........<./...A.....2...*  
.&.......=5....+.'.#........g.@.3.2.....
```
