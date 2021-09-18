RESP = {
    200: '200 OK\r\nConnection: close\r\n',
    301: '301 Moved Permanently\r\nLocation: %s\r\nConnection: close\r\n',
    302: '302 Found\r\nConnection: close\r\n',
    404: '404 Not Found\r\nConnection: close\r\n',
    405: '405 Method Not Allowed\r\nAllow: GET\r\nConnection: close\r\n',
}
