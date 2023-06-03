#!/bin/bash

docker kill z44_gateway
docker remove z44_gateway
docker run -it --network z44_network --name z44_gateway z44_gateway:latest