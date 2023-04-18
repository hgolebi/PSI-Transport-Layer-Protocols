docker run -dit --rm --network-alias z43_z11_c_server --network z43_network --name z43_z11_c_server z43_z11_c_server
docker run -it --rm --network-alias z43_z11_c_client --network z43_network --name z43_z11_c_client z43_z11_c_client
docker logs --tail 15 z43_z11_c_server
docker stop z43_z11_c_server
