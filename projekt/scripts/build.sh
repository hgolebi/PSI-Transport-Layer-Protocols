#!/bin/bash

docker build -t z44_gateway ../gateway
docker build -t z44_sensor ../sensor
docker build -t z44_client ../client