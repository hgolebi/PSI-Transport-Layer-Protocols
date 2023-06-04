#!/bin/bash

docker rm z44_client$1
docker run -it --network z44_network --name z44_client$1 z44_client:latest z44_gateway 8000