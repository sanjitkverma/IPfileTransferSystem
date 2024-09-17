### README for gRPC File Transfer Experiment

#### Environment Setup

- **Python Version Required**: 3.11.X
- **Required Libraries and Tools**: Install these using pip:
  - `grpcio`
  - `grpcio-tools`
  - `numpy`
  
To install the required libraries, use the following command:
```bash
pip install grpcio grpcio-tools numpy
```

#### Generating gRPC Code from Proto File

To generate the Python gRPC code from your `.proto` file, run the following command in the directory where your `file_transfer.proto` file is located:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. file_transfer.proto
```

This will generate `file_transfer_pb2.py` and `file_transfer_pb2_grpc.py`, which contain the code for your protocol buffers and gRPC client and server.

### Server Setup (Computer 1)

File: `server.py`

- Implements the `FileTransferService` defined in the `.proto` file.
- Listens for file upload and download requests from clients.

To run the server, use the command:

```bash
python3 server.py
```

### Client Setup (Computer 2)

File: `client.py`

- Implements functionality to upload and download files using the gRPC protocol.
- Modify the file paths and server address as necessary for your setup.

To run the client, use the command:

```bash
python3 client.py
```

#### Experiment Execution

1. **Server Side**: Start the server using the command above. The server will listen on the specified port for incoming file transfer requests.

2. **Client Side**: Run the client script to either upload or download files from the server. The client will connect to the server using the gRPC protocol.

Note: Be sure to use your own IP adress and replace the current placeholder IP adress. REplace iterations with the iterations value you want, repalce the file names (ex: A_10MB or ../data/B_10MB) with the file you want such as A_10kB or ../data/B_10kB) and file_size witht the size of the file.