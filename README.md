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
So far the image does not have a program, so to run it once the image is in docker, you will need:
```sh
$ docker run -it --entrypoint=bin/bash -v /var/run/docker.sock:/var/run/docker.sock idc_orchestrator:<tag>
```
With:
- `<tag>`: as the image version, i.e. `0.2.0`