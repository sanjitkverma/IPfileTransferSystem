import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
import numpy as np
import time

# Initialize lists to track durations and bytes transferred
durations_send = []
durations_receive = []
bytes_sent = []
bytes_received = []

def generate_chunks(file_name, chunk_size=1024*1024):
    # Track total bytes for each file
    total_bytes = 0  
    with open(file_name, "rb") as f:
        while True: # read until empty chunk
            chunk = f.read(chunk_size)
            if not chunk:
                break
            total_bytes += len(chunk)
            yield file_transfer_pb2.FileRequest(name=file_name, data=chunk)
    # Append total bytes after file is fully read
    bytes_sent.append(total_bytes)  

def download_file(file_name):
     # Start timing
    start_time = time.time() 
    total_bytes = 0  # Track total bytes received
    with grpc.insecure_channel('192.168.50.187:50051') as channel: # replace IP address with own
        stub = file_transfer_pb2_grpc.FileTransferServiceStub(channel)
        response_iterator = stub.DownloadFile(file_transfer_pb2.FileDownloadRequest(name=file_name))
        with open(file_name, "wb") as f:
            for response in response_iterator:
                f.write(response.data)
                total_bytes += len(response.data)
    duration = time.time() - start_time  # Calculate duration
    durations_receive.append(duration)  # Track duration
    bytes_received.append(total_bytes)  # Track total bytes received

def upload():
    start_time = time.time()  # Start timing
    with grpc.insecure_channel('192.168.50.187:50051') as channel: # replace IP address with own
        stub = file_transfer_pb2_grpc.FileTransferServiceStub(channel)
        response = stub.UploadFile(generate_chunks("../data/A_10MB"))  # Specify the fil to send
        print(response.message)
    duration = time.time() - start_time  # Calculate duration
    durations_send.append(duration)  # Track duration
    # Note: bytes_sent is updated within generate_chunks

iterations = 1
if __name__ == '__main__':
    # conduct the experiments
    for i in range(iterations):
        upload()
        print(i)

    for i in range(iterations):
        download_file(f"B_10MB")
        print(i)

    # Combine durations for total operation times
    total_durations = durations_send + durations_receive

    # Calculate throughput and standard deviation
    file_size_kb = 10000 # CHANGE THIS FOR FILE SIZE
    average_throughput = np.mean([file_size_kb / duration for duration in total_durations])
    std_dev_throughput = np.std([file_size_kb / duration for duration in total_durations])

    # Calculate average total bytes transferred
    average_total_bytes_sent = np.mean(bytes_sent)
    average_total_bytes_received = np.mean(bytes_received)

    # Print results
    print(f"Average Throughput: {average_throughput:.2f} KB/s")
    print(f"Standard Deviation of Throughput: {std_dev_throughput:.2f} KB/s")
    print(f"Average Total Bytes Sent: {average_total_bytes_sent:.2f} Bytes")
    print(f"Average Total Bytes Received: {average_total_bytes_received:.2f} Bytes")
