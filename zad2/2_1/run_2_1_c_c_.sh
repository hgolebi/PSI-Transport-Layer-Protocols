docker run -dit --rm --network-alias z44_z21_c_server --network z44_network --name z44_z21_c_server z44_z21_c_server:latest
docker run -it --rm --network-alias z44_z21_c_client --network z44_network --name z44_z21_c_client z44_z21_c_client:latest
docker logs --tail 15 z44_z21_c_server
docker stop z44_z21_c_server
