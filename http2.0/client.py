import httpx
import os
import time
import numpy as np

# This function will send the file to the specified IP address and port
def send_file(filename):
    url = "https://192.168.50.187:8443/download"
    start_time = time.time()
    with httpx.Client(http2=True, verify=False) as client: # Set verify to False to ignore SSL certificate
        response = client.get(url)
        with open(filename, 'wb') as file: # Open the file in binary mode and write the content to it
            file.write(response.content)
    end_time = time.time() # Calculate duration and total bytes sent
    duration = end_time - start_time
    bytes_sent = os.path.getsize(filename)
    print(f"Status Code: {response.status_code}")
    return duration, bytes_sent

# This function will receive the file from the specified IP address and port
def receive_file(filename):
    url = "https://192.168.50.187:8443/upload"
    start_time = time.time()
    with open(filename, 'rb') as f: # Open the file in binary mode and send it to the client
        files = {'file': (filename, f)}
        with httpx.Client(http2=True, verify=False) as client: # Set verify to False to ignore SSL certificate
            response = client.post(url, files=files)
    end_time = time.time()
    duration = end_time - start_time
    bytes_received = len(response.content)  # Assuming response.content has meaningful data
    print(f"Status Code: {response.status_code}")
    return duration, bytes_received

# Initialize lists to track durations and bytes transferred
durations_send, bytes_sent = [], []
durations_receive, bytes_received = [], []
iterations = 1
# Sending files
for i in range(iterations):
    duration, bytes_transferred = send_file('A_10MB')
    durations_send.append(duration)
    bytes_sent.append(bytes_transferred)
    print(i)

# Receiving files
for i in range(iterations):
    duration, bytes_transferred = receive_file('../data/B_10MB')
    durations_receive.append(duration)
    bytes_received.append(bytes_transferred)
    print(i)

# Combine durations for total operation times
total_durations = durations_send + durations_receive

# Calculate throughput and standard deviation
file_size_kb = 10000  # Adjust based on your file sizes
average_throughput = np.mean([file_size_kb / duration for duration in total_durations])
std_dev_throughput = np.std([file_size_kb / duration for duration in total_durations])

# Calculate average total bytes transferred
average_total_bytes_sent = np.mean(bytes_sent)
average_total_bytes_received = np.mean(bytes_received)

print(f"Average Throughput: {average_throughput:.2f} KB/s")
print(f"Standard Deviation of Throughput: {std_dev_throughput:.2f} KB/s")
print(f"Average Total Bytes Sent: {average_total_bytes_sent:.2f} Bytes")
print(f"Average Total Bytes Received: {average_total_bytes_received:.2f} Bytes")
