terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_network" "mlops_net" {
  name = "mlops_net"
}

resource "docker_image" "web" {
  name         = "nginx:alpine"
  keep_locally = true
}

resource "docker_container" "nginx" {
  name  = "mlops-nginx-demo"
  image = docker_image.web.image_id

  networks_advanced {
    name = docker_network.mlops_net.name
  }

  ports {
    internal = 80
    external = 8088
  }
}
