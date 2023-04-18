docker run -dit --rm --network-alias z44_z21_c_server --network z44_network --name z44_z21_c_server z44_z21_c_server:latest
echo ""
echo "###### client ######"
echo ""
docker run -it --rm --network-alias z44_z21_py_client --network z44_network --name z44_z21_py_client z44_z21_py_client:latest z44_z21_c_server 2000
echo ""
echo "###### server ######"
echo ""
docker logs --tail 15 z44_z21_c_server
docker kill z44_z21_c_server
