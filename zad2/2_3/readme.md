Aby zaprezentowac zadanie 2.3 potrzebujemy 3 konsol z odpalonym serwerem biguwu.

1. Budujemy obrazy kontenerowe za pomoca komendy:
sh build.sh

2. W pierwszej konsoli odpalamy serwer:
sh server.sh

UWAGA: Jeśli serwer przez 5 sekund nie otrzyma zadnego polaczenia to sie wylaczy. Nalezy wtedy jeszcze raz go odpalic ta sama komenda.

3. W drugiej konsoli odpalamy blokujacego klienta:
sh block_client.sh

UWAGA: Client poprosi o wpisanie wiadomosci do przeslania. Nie wpisujemy jej od razu, aby serwer sie zablokowal na recv().

4. W trzeciej konsoli odpalamy nieblokujacego klienta. Klient przesle wiadomosc i przez 5 sekund bedzie oczekiwal na odpowiedz serwera. Jako, ze serwer jest zablokowany, klient nie otrzyma odpowiedzi i sie wylaczy.

5. Mozemy wpisac wiadomosc blokujacego klienta. Po jej wpisaniu na serwerze powinny sie pojawic wiadomosci od obu klientow.