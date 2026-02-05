Lab 1 - Hello Web

Build:
  docker build -t hello-web:local hello_web

Run:
  docker run --rm -p 8080:80 hello-web:local

Test:
  curl http://localhost:8080
