docker rmi -f $(docker images -q 'z44_zad21*')

docker build --tag z44_zad21_server_c server_c
docker build --tag z44_zad21_server_py server_py 
docker build --tag z44_zad21_client_py client_py
docker build --tag z44_zad21_client_c client_c