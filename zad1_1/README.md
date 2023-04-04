# Zadanie 1_1

Po pierwszym pobraniu lub zmianie plików źródłowych należy utworzyć nowy obraz dla dockera. W odpowiednim folderze wpisujemy komendę: 

docker build --tag *nazwa* .

Z gotowego obrazu możemy uruchomić kontener korzystając z komendy:

docker run -it --network z44_network --name *nazwa* *nazwa_obrazu*

Dodatkowo dla klienta należy podać jako kolejne argumenty ww. komendy *nazwę_serwera* oraz *port_serwera*
