server {
        listen       9090  deferred backlog=65535;
        server_name  localhost 127.0.0.1;
        location / {
            uwsgi_pass  unix:/tmp/uwsgi.sock;
            include     uwsgi_params;
        }
 
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
}



