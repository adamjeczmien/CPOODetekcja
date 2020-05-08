# Repo CPOODetekcja
#### Projekt CPOO sem letni 2020

**Algorytm** - Rzeczy do zrobienia:
1. **Usuniecie Menu**
   - najprościej usunąć ten pasek nawigacji, po prostu nie brać go do algorytmów
   - jako, że guziki wchodzą w obraz = trzeba je usunąć, ale są one stałe w swojej lokalizacji i kolorze, więc 
     - za pomocą maski koloru
     - patrzac po histogramie\
     usuniemy w tym miejscu wszysctko co nie jest pomarańczowe/czarne guziki(itp itd) i 
     zamienimy na kolor tła(znaleziony za pomocą histogramu również jako najczęstszy kolor w obrazie) albo na czarny
   - Kolejnym pomysłem jest sprawdzanie pomiędzy klatkami co jest stałe w tym rejonie obrazka i usuwanie tego(zamiana na czarny)
2. **Filtracja Obrazu** (może być inna dla różnych zadań)
3. **Znalezienie Dna** 
  - Tutaj można by zaznaczyć ogólną linię dna(obwiednią albo punkty  co 100 px, pomiędzy,którymi narysować prostą )
4. **Znalezienie regionów zainteresowania**
5. **Wyznaczenie maksimum/średniej głebokości dna**
   - na wyznaczonej już linii dna znaleźć maksimum głębokości i minimum (punkt najgłębszy i najpłytszy)
   - zazaczyć np. kropką albo linią od 0 do dna
   - napisać jaka to głębokość

 **Klasyfikacja** - Rzeczy do zrobienia | przykład w images:
1. Sprawdzenie zadanych plików wideo i wyznaczenie:
   - w jakich sekundach wideo pojawia się np.ryba i zapis
2. Przejechać po wszystkich wideo i zaznaczyć w paincie parę linii dna.
3. Zazaczyć na paru klatkach wideo w paincie głębokość dna ( i bardzo prosto wyznaczyć, nwm linijką nawet xd)

Przykładowo sklasyfikowana klatka:
![alt text](./images/Example_classification.png "Klatka ze sklasyfikowanymi rzeczami (ale mega prosto, można inaczej)")