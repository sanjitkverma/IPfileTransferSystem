import requests
import time
import numpy as np

def send_file(url, file_path, iterations):
    """
    Sends a file to the specified URL using HTTP POST request.

    Args:
        url (str): The URL to send the file to.
        file_path (str): The path of the file to send.
        iterations (int): The number of times to send the file.

    Returns:
        tuple: A tuple containing two lists - durations and total_bytes_sent.
            durations (list): The durations of each file transfer in seconds.
            total_bytes_sent (list): The total bytes sent for each file transfer.
    """
    durations = []
    total_bytes_sent = []

    with requests.Session() as session:
        session.headers.update({'Connection': 'keep-alive'})

        for _ in range(iterations):
            with open(file_path, 'rb') as file:
                file_data = file.read()
                start_time = time.time()
                response = session.post(url, files={'file': (file_path, file_data)})
                end_time = time.time()

                if response.status_code == 201:
                    durations.append(end_time - start_time)
                    total_bytes_sent.append(len(file_data))

    return durations, total_bytes_sent

def receive_file(url, save_path, iterations):
    """
    Receives a file from the specified URL using HTTP GET request.

    Args:
        url (str): The URL to receive the file from.
        save_path (str): The path to save the received file.
        iterations (int): The number of times to receive the file.

    Returns:
        tuple: A tuple containing two lists - durations and total_bytes_received.
            durations (list): The durations of each file transfer in seconds.
            total_bytes_received (list): The total bytes received for each file transfer.
    """
    durations = []
    total_bytes_received = []

    for _ in range(iterations):
        start_time = time.time()
        response = requests.get(url, stream=True)
        end_time = time.time()

        total_bytes = 0  # Initialize total bytes for this transfer

        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Ensure chunk is not empty
                        file.write(chunk)
                        total_bytes += len(chunk)  # Add the size of the chunk to total bytes

            durations.append(end_time - start_time)
            total_bytes_received.append(total_bytes)  # Append the total bytes for this transfer

    return durations, total_bytes_received

# set our constants to run the experiments
file_size = '10MB'
url_send = 'http://192.168.50.187:8000/A_' + file_size
url_receive = 'http://192.168.50.187:8000/B_' + file_size
file_path_send = '../data/A_' + file_size
file_path_recieve = "B_" + file_size
iterations = 1
file_size_kb = 10000 

# Sending files
durations_send, total_bytes_sent = send_file(url_send, file_path_send, iterations)

# Receiving files
durations_receive, total_bytes_received = receive_file(url_receive, file_path_recieve, iterations)

total_durations = durations_send + durations_receive

# Calculate throughput and standard deviation for both operatios
average_throughput = np.mean([file_size_kb / duration for duration in total_durations])
std_dev_throughput = np.std([file_size_kb / duration for duration in total_durations])

# Calculate average total bytes transferred
average_total_bytes_sent = np.mean(total_bytes_sent)
average_total_bytes_received = np.mean(total_bytes_received)

print(f"Average Throughput: {average_throughput:.2f} KB/s")
print(f"Standard Deviation of Throughput: {std_dev_throughput:.2f} KB/s")
print(f"Average Total Bytes Transferred: {average_total_bytes_sent:.2f} Bytes")
print("\n")
print(f"Average Total Bytes Transferred (Receive Only): {average_total_bytes_received:.2f} Bytes")
