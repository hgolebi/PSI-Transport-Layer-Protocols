#!/bin/bash

docker build -t z44_gateway ../server
docker build -t z44_sensor ../sensor
docker build -t z44_client ../client