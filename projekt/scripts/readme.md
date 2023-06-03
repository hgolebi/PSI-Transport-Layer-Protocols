INSTRUKCJA URUCHAMIANIA

1. Budujemy kontenery (wystarczy raz)
> bash build.sh

2. Odpalamy serwer:
> bash gateway.sh
Logi z serwera są zapisywane w folderze ../projekt/logs

3. Odpalamy co najmniej jeden sensor:
> bash sensor.sh [tag] 
Argument [tag] zostanie dodany do nazwy kontenera dockerowego (domyslnie z44_sensor), na przyklad:
bash sensor.sh 123  utworzy kontener o nazwie z44_sensor123
Argument jest opcjonalny. Jest on po to, aby można było utworzyć kilka kontenerów z sensorem.

4. Odpalamy co najmniej jednego klienta:
> bash client.sh [tag]
Argument [tag] -> (tak jak wyzej)

Skrypty najpierw usuwają podane kontenery (jeśli istnieją), ale należy pamiętać, że kontenery muszą być wyłączone. Jeśli istnieje już uruchomiony kontener o podanej nazwie należy go najpierw zatrzymać poleceniem:
> docker stop nazwa_kontenera

Dockery są uruchamiane w trybie interaktywnym, to znaczy, że nasza konsola będzie podłączona do kontenera. Aby się od niego odłączyć bez wyłączania, należy skorzystać z kombinacji klawiszy ctrl + p a następnie ctrl + q. Aby z powrotem się podłaczyć możemy skorzystać z komendy:
> docker attach nazwa_kontenera

Natomiast aby zobaczyć wszystkie logi wypisywane w konsoli kontenera możemy użyć komendy:
> docker logs nazwa_kontenera
