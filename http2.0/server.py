from aiohttp import web
import ssl

async def handle(request):
    """
    Handle the download request by reading a file and returning its content as a response.

    Args:
        request: The HTTP request object.

    Returns:
        A web.Response object with the file content as the response body.
    """
    file_path = '../data/A_10kB'  # Adjust the file path/name as necessary
    with open(file_path, 'rb') as file:
        content = file.read()
    return web.Response(body=content, content_type='application/octet-stream')

async def upload_file(request):
    """
    Handle the file upload request by saving the uploaded file.

    Args:
        request: The HTTP request object.

    Returns:
        A web.Response object with a success message.
    """
    reader = await request.multipart()
    # Assuming 'file' is the name of the field in the form
    field = await reader.next()
    filename = '../data/B_10kB'
    with open(filename, 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            f.write(chunk)
    return web.Response(text=f'{filename} uploaded successfully.')

# start the server and create endpoints with handlers
app = web.Application()
app.add_routes([web.get('/download', handle)])
app.add_routes([web.post('/upload', upload_file)])

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('172.20.10.12.pem', '172.20.10.12-key.pem') # replace with your own certificate and key

web.run_app(app, port=8443, ssl_context=ssl_context)