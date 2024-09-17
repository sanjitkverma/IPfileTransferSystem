### README for Experiment with HTTP/2.0

#### Environment Setup

- **Python Version Required**: 3.11.X
- **Required Libraries**: Install these libraries using pip:
  - `httpx`
  - `aiohttp`
  - `numpy`
  
To install the required libraries, use the following command:
```bash
pip install httpx aiohttp numpy
```

#### Generating SSL Certificate and Key for HTTPS

To secure the connection for HTTP/2.0, generate a self-signed SSL certificate and private key with the following commands:

```bash
openssl genrsa -out 172.20.10.12-key.pem 2048
openssl req -new -key 172.20.10.12-key.pem -out 172.20.10.12.csr
openssl req -x509 -sha256 -days 365 -key 172.20.10.12-key.pem -in 172.20.10.12.csr -out 172.20.10.12.pem
```
replace 172.20.10.12 with your IP adress  

### Server Setup (Computer 1)

File: `server.py`

- This server script utilizes `aiohttp` for asynchronous HTTP server capable of HTTP/2.0.
- The server provides two endpoints: `/download` for sending a file to the client, and `/upload` for receiving a file from the client.

To run the server on one computer, use the command:

```bash
python3 server.py
```

be sure to replace the current PEM and key file with the one generated above 
replace the current line:
ssl_context.load_cert_chain('172.20.10.12.pem', '172.20.10.12-key.pem')

with your 

ssl_context.load_cert_chain('XXX.XX.XX.XX.pem', 'XXX.XX.XX.XX-key.pem')

### Client Setup (Computer 2)

File: `client.py`

- The client script uses `httpx` to support HTTP/2.0 for both uploading and downloading files.
- Adjust the filename and iteration variables in the script as needed for your experiment.

To run the client on a second computer, use the command:

```bash
python3 client.py
```

#### Experiment Execution

1. **Server Side**: Run `server.py` on the computer designated as the server. Ensure the SSL certificate and key are correctly placed and referenced in the script.

2. **Client Side**: Execute `client.py` on the client machine. Make sure the URL in the script matches the server's IP and the ports are correctly configured for HTTP/2.0 (default is 8443 for HTTPS).

Note: Be sure to use your own IP adress and replace the current placeholder IP adress. REplace iterations with the iterations value you want, repalce the file names (ex: A_10MB or ../data/B_10MB) with the file you want such as A_10kB or ../data/B_10kB). Replace file_size with the file size of the files for the correct calculation
