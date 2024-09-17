### README for Experiment with HTTP/1.1

### README for Computer 1 (server) Setup

#### Requirements:

*   **Python Version**: 3.11.X

*   **Libraries**: None required beyond standard library.

#### Setup Instructions:

1.  Ensure Python 3.11.X is installed on your computer.

2.  No additional libraries are required for the server script.

#### Running the Server:

*   **Command to Run on Server Computer**:

    ```bash
    python3 server.py
    ```

*   This will start the HTTP server on the specified IP address and port (e.g., `172.20.10.12:8000`). The server will serve files located in the `../data/` directory.

***

### README for Computer 2 (Client) Setup

#### Requirements:

*   **Python Version**: 3.11.X

*   **Libraries**: `requests`, `numpy`

    *   Install using pip:

        ```bash
        pip install requests numpy
        ```

#### Setup Instructions:

1.  Ensure Python 3.11.X is installed on your computer.

2.  Install the required libraries using the pip command provided above.

#### Running the Client:

*   **Sending Files Command**:

    ```bash
    python3 client.py
    ```

*   This script will send and receive files to/from the server. It calculates and prints the average throughput and standard deviation of throughput for the file transfer operations.

Note: Adjust the `url_send`, `url_receive`, `file_path_send`, and `file_path_receive` variables in the client script to match server's IP address and the files you wish to send/receive. Adjust Iterations to run the amount of time you want it to and file_size to the one you want too
