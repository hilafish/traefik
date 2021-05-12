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


