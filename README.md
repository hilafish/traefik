# traefik_exercise
Traefik demo with an in-house solution for POST requests distribution

In order to bootstrap the containers, run - "docker-compose up -d"
This will bootstrap-
* 10 "whoami" containers - dummy application to demonstrate Traefik requests distribution, but in order for the POST requests to pass ok and not go to retry 
  phase, set an app that can report back with status code 201, or alternatively edit the web_service.py retry mechanism to check status code 200 rather than 201.
* traefik container - The actual LB
* traefik_post_app - Web service that catches POST requests from Traefik and distribute them to all backend containers (a.k.a, the 10 whoami containers), a  
  workaround for builtin round-robin LB mechanism. 
* prometheus container - For metrics exposure

**Flow:**
* Client posts a GET request that is catched by LB and passed to whoami container in a round-robin manner
* CLient posts a POST request that is catched by LB, and passed to a web service (traefik_post_app container) which then distributes the request to all backend services (10 "whoami" containers).

```
hfish:~$ curl -X POST -F 'name=hila' -F 'email=hf@test.com' -H Host:whoami.docker.localhost http://127.0.0.1/register
POST request for /register
```

traefik_post_app logs:
```
INFO:root:POST request,
Path: /register
Headers:
Host: whoami.docker.localhost
User-Agent: curl/7.64.1
Content-Length: 249
Accept: */*
Content-Type: multipart/form-data; boundary=------------------------d337d3bb05c2229e
X-Forwarded-For: 192.168.16.1
X-Forwarded-Host: whoami.docker.localhost
X-Forwarded-Port: 80
X-Forwarded-Proto: http
X-Forwarded-Server: 2b05c3834c8d
X-Real-Ip: 192.168.16.1
Accept-Encoding: gzip



Body:
--------------------------d337d3bb05c2229e
Content-Disposition: form-data; name="name"

hila
--------------------------d337d3bb05c2229e
Content-Disposition: form-data; name="email"

hfe@test.com
--------------------------d337d3bb05c2229e--


192.168.16.3 - - [12/May/2021 16:45:51] "POST /register HTTP/1.1" 200 -
INFO:root:POST request forwarded to traefik_whoami_1, status code: 200
INFO:root:POST request forwarded to traefik_whoami_2, status code: 200
INFO:root:POST request forwarded to traefik_whoami_3, status code: 200
INFO:root:POST request forwarded to traefik_whoami_4, status code: 200
INFO:root:POST request forwarded to traefik_whoami_5, status code: 200
INFO:root:POST request forwarded to traefik_whoami_6, status code: 200
INFO:root:POST request forwarded to traefik_whoami_7, status code: 200
INFO:root:POST request forwarded to traefik_whoami_8, status code: 200
INFO:root:POST request forwarded to traefik_whoami_9, status code: 200
INFO:root:POST request forwarded to traefik_whoami_10, status code: 200
```
