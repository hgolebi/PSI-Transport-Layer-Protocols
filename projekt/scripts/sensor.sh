#!/bin/bash

docker rm z44_sensor$1
docker run -it --network z44_network --name z44_sensor$1 z44_sensor:latest z44_gateway 8001