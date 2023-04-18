docker rmi -f $(docker images -q 'z44_zad21*')

docker build --tag z44_zad21_c_server server_c
docker build --tag z44_zad21_py_server server_py 
docker build --tag z44_zad21_py_client client_py
docker build --tag z44_zad21_c_client client_c