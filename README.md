# Service Manager

This repository contains an application to control the internal configurations of other docker containers inside the same compose.

## Dependencies
This repository is a docker image. To use it one will need:
```sh
$ sudo apt install docker docker.io
```
Also some configurations regarding the addition of your user to the docker group may be needed.
```sh
$ sudo usermod -aG docker $USER
```
After the execution of the past command a Logout and Login is needed.

## Building the image
```sh
$ docker build -t orchestrator:<tag> .
```
With:
- `<tag>`: as the image version, i.e. `0.2.0`

## Configurations
- Volumes:
    - `/var/run/docker.sock`: Docker socket connection

## Running the image
```sh
$ docker run -v /var/run/docker.sock:/var/run/docker.sock -v $PWD/config:/home/config --name orchestrator orchestrator:<tag>
```
With:
- `<tag>`: as the image version, i.e. `0.2.0`