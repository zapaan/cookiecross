from http.server import HTTPServer,SimpleHTTPRequestHandler
import ssl

httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
sslctx = ssl.SSLContext()
sslctx.check_hostname = False # If set to True, only the hostname that matches the certificate will be accepted
sslctx.load_cert_chain(certfile='/code/localho.st.pem', keyfile="/code/localho.st-key.pem")
httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()