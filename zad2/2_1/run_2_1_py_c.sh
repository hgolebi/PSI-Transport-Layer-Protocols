docker run -dit --rm --network-alias z44_z21_py_server --network z44_network --name z44_z21_py_server z44_z21_py_server:latest
docker run -it --rm --network-alias z44_z21_c_client --network z44_network --name z44_z21_c_client z44_z21_c_client:latest z44_z21_py_server 8000
docker logs --tail 15 z44_z21_py_server
docker kill z44_z21_py_server
