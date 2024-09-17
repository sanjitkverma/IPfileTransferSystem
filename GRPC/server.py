from concurrent import futures
import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc

class FileTransferService(file_transfer_pb2_grpc.FileTransferServiceServicer):
    """
    Implements the gRPC service for file transfer.
    """

    def UploadFile(self, request_iterator, context):
        """
        Uploads a file to the server.

        Args:
            request_iterator: An iterator of FileRequest objects containing the file data.
            context: The gRPC context.

        Returns:
            A FileResponse object indicating the status of the file upload.
        """
        file_name = None
        print("File received Successfully")
        with open("A_10MB", "wb") as f:  # Adjust the filename/path as needed
            for request in request_iterator:
                if file_name is None:
                    file_name = request.name 
                f.write(request.data)
        return file_transfer_pb2.FileResponse(message=f"File {file_name} received successfully.")

    def DownloadFile(self, request, context):
        """
        Downloads a file from the server.

        Args:
            request: A FileRequest object containing the name of the file to download.
            context: The gRPC context.

        Yields:
            FileResponse objects containing chunks of the file data.
        """
        file_name = "../data/"+request.name
        print("File sent Successfully")
        try:
            with open(file_name, "rb") as f:
                while True:
                    chunk = f.read(1024 * 1024)  
                    if not chunk:
                        break
                    yield file_transfer_pb2.FileResponse(data=chunk)
        except FileNotFoundError:
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")

def serve():
    """
    Starts the gRPC server and listens for requests.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServiceServicer_to_server(FileTransferService(), server)
    server.add_insecure_port('192.168.50.187:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
