#!/bin/bash

# docker kill z44_gateway
docker rm z44_gateway
docker run -it --network z44_network --name z44_gateway -v $(dirname $PWD)/logs:/gateway_server/logs z44_gateway:latest