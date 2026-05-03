---
title: S03E05 — Niedeterministyczna natura modeli jako przewaga
space_id: 2476415
status: scheduled
published_at: '2026-03-27T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/nondeterministic-1773912609.png'
circle_post_id: 30844689
---
Programowanie przez lata nauczyło nas, że jeśli system nie zachowuje się zgodnie z oczekiwaniami, to jest błędnie zaprojektowany. Wszelkie odchylenia od założeń traktowaliśmy jako błędy, które należało wyeliminować. Odkąd pojawiły się LLM-y, dążymy do tego, aby robiły dokładnie to, czego oczekujemy, w sposób przez nas opisany.

Mówi się, że halucynacja modelu to sytuacja w której odpowiedzi są zmyślone, a ich treść nie jest zgodna z rzeczywistością bądź naszymi założeniami. Ale jeśli przyjrzymy się temu nieco bliżej, modele językowe są "[śniącymi maszynami](https://x.com/karpathy/status/1733299213503787018)" w przypadku których **wszystko jest "halucynacją"**, która po prostu czasem nam sprzyja, a czasem nie.

Eksplorując możliwości, jakie daje generatywna sztuczna inteligencja w połączeniu z programowaniem, łatwo zauważyć, że mamy przed sobą zarówno dobrze znane wyzwania dotyczące architektury, wydajności czy różnych decyzji projektowych, jak i mnóstwo zupełnie nowych wyzwań, których do tej pory nie mieliśmy okazji doświadczać.

I to właśnie nimi zajmiemy się tym razem.

## Tworzenie przestrzeni do otwartej interpretacji

Budując workflow lub agenta AI, definiujemy procesy bądź cele, które chcemy osiągnąć, a następnie sposób ich realizacji. Następnie zakładamy, że **LLM będzie zachowywał się tak samo jak logika opisana w kodzie**, a prompty wykonane **linia po linii** i to jeszcze z uwzględnieniem zapisanych w nich warunków przypominających instrukcje warunkowe 'if' czy pętle.

Z drugiej strony, jeśli będzie zależało nam na nieco większej "losowości" w zachowaniu modelu, to szybko zorientujemy się, że jest ona bardzo niska i to nawet pomimo zmian wartości parametrów **temperature czy top\_p** (oczywiście ich zmiana do pewnego stopnia pomaga, ale nie rozwiązuje problemu).

Klasycznym przykładem jest zapytanie modelu o opowiedzenie żartu. Gdy zrobimy to kilkukrotnie, bardzo szybko zauważymy częste powtórzenia. Jednocześnie ich obecność będzie duża przede wszystkim w **bezpośredniej interakcji z modelem**. Gdy jednak zaczniemy rozmawiać z agentem wyposażonym w dodatkowe informacje o otoczeniu lub korzystającym z pamięci długoterminowej, różnorodność jego wypowiedzi zdecydowanie wzrośnie, choć nadal da się zauważyć efekt widoczny na poniższej wizualizacji.

![Powtarzalność w LLMach](https://cloud.overment.com/2026-02-27/ai_devs_4_randomness-a4c6e888-8.png)

Widać tu bardzo wyraźnie jak bardzo zachowanie modelu jest uzależnione od **poprzedzającej treści**. Jeśli ta się nie zmienia, to wynik **zazwyczaj** będzie bardzo podobny. Jednocześnie nie możemy liczyć na to, że model zachowa się jak "funkcja czysta", która dla tych samych danych wejściowych zwróci dokładnie ten sam rezultat.

Można więc powiedzieć, że dla LLM dużym wyzwaniem jest zarówno **precyzyjne** podążanie za instrukcjami, jak i generowanie **zróżnicowanych** odpowiedzi.

Biorąc to wszystko pod uwagę, możemy zadać sobie pytanie: **jak sprawić, by model wykorzystał swoją wiedzę do robienia rzeczy wykraczających poza to, co jesteśmy w stanie przewidzieć i samodzielnie zaprogramować?**

Agenci, których tworzyliśmy do tej pory, mieli dostęp do różnych narzędzi uruchamianych niemal bezpośrednio w odpowiedzi na **polecenia** użytkownika, na przykład:

- Dodaj poniższe zadania do listy ...
- Utwórz kod rabatowy ... dla produktów ...
- Przygotuj zestawienie kosztów za ostatni miesiąc ...

W połączeniu z pamięcią długoterminową, efekt był nieco bardziej dynamiczny. Przykładowo:

- Wyślij zaproszenie do Marty i Grześka na spotkanie w sprawie ...
- Prześlij mi notatki na nadchodzącą konsultację z ...
- Sprawdź aktualne promocje produktów z mojej listy ...

Natomiast nadal widzimy tu wyraźne połączenie pomiędzy tym, co mówi użytkownik, a tym co robi agent. Przestrzeń na samodzielną interpretację tych zapytań jest bardzo mała.

W przykładzie **S03E05** znajduje się agent, który na pozór wygląda bardzo podobnie do tych, które tworzyliśmy do tej pory. On również ma dostęp do systemu plików, który stanowi formę jego pamięci. Poza tym, w kontekście znajdują się także informacje o stanie otoczenia. Jednak jego zachowanie znacznie się różni, ponieważ **nie wymaga bezpośrednich poleceń**, aby zdecydować o **wyborze akcji**. Konkretnie:

- Agent na proste "**cześć**" reaguje poprzez zastanowienie się nad informacjami, których mu brakuje z pomocą narzędzia `think`. Następnie narzędziem `recall` wczytuje swoją **"osobowość" oraz tożsamość użytkownika**. Pomimo braku wyraźnych poleceń, model próbuje odnaleźć się w bieżącej sytuacji.
- Gdy użytkownik jedynie **wspomina** o tym, że zastanawia się nad tym, jak spędzić wieczór, agent zauważa lukę w swojej wiedzy i wywołuje `recall` w celu pobrania szczegółów o lokalizacji oraz preferencjach użytkownika. W ten sposób odpowiada **konkretnymi** sugestiami, które nawiązują do potencjalnych zainteresowań.
- Przy dalszej wymianie wiadomości agent **nie wywołuje dodatkowych narzędzi** jeśli uznaje, że sytuacja tego nie wymaga. W odpowiedziach wykorzystuje też posiadane już informacje.

Interesujące jest jednak to, że szansa na to, że po uruchomieniu tej interakcji otrzymamy ten sam wynik jest **bardzo niska**! Żadna z podjętych decyzji oraz zachowań nie zostały wprost zdefiniowane w logice aplikacji ani promptach. To model "decyduje" kiedy kontekst jest wystarczający, a kiedy trzeba sięgnąć do pamięci. W bardzo dużym stopniu zachowanie uzależnione jest od **stanu otoczenia** oraz **treści wiadomości użytkownika**, a finalnie także **kolejnych odpowiedzi agenta**.

![Przykład "świadomego" agenta](https://cloud.overment.com/2026-02-28/ai_devs_4_situational_awareness_agent-74687ea3-d.png)

Oznacza to, że "**straciliśmy kontrolę**" nad zachowaniem agenta i możemy jedynie liczyć na to, że model skutecznie odnajdzie się w bieżącej sytuacji, generując użyteczny wynik. W teorii brzmi to jak coś zupełnie niepożądanego. Jednak w praktyce, biorąc pod uwagę możliwości obecnych modeli, może okazać się niezwykle użyteczne. Tym bardziej, że jeśli przyjrzymy się nieco bliżej mechanice, to zobaczymy, że nie jest to do końca tak, że **"rzeczy dzieją się same"** ponieważ agent cały czas porusza się po wyznaczonej przez nas przestrzeni. Po prostu przestrzeń ta jest zdecydowanie większa, niż w sytuacji, gdy agent podąża ściśle za konkretnymi instrukcjami opisanymi w kodzie.

Poniżej widzimy obszary, które w tym przypadku zostały **oddelegowane** do modelu. Wśród nich znajdziemy:

- **Proaktywność:** model samodzielnie określa **kiedy** podjąć działanie oraz jakiej wiedzy potrzebuje, aby to zrobić. Nie robi jednak tego w odpowiedzi na polecenia, lecz na podstawie **podejrzeń**, zadawania **otwartych pytań** oraz otwartego **wnioskowania** w oparciu o dostępne informacje, oraz te **"potencjalnie"** posiadane.
- **Synteza:** model posiada bardzo dużą swobodę w obszarze łączenia ze sobą informacji. Nie ma jasnych wytycznych o tym, jak połączyć oraz wykorzystać posiadaną wiedzę. Nie ma więc tutaj instrukcji "jeśli X to Y", lecz bardziej dynamiczne dopasowanie do bieżącej sytuacji.
- **Wnioskowanie:** pomimo tego, że wykorzystujemy model "rozumujący" (LRM) w postaci GPT-5.2 z właściwością **reasoning\_effort** ustawioną na **high**, samo wnioskowanie opiera się o **dedykowane narzędzia** zachęcające model do zadawania pytań samemu sobie. Ich rolą jest wyłącznie stworzenie przestrzeni na **zastanowienie**, ponieważ sama ich obecność wpływa na dalszą pracę modelu.
- **Dopasowanie:** model samodzielnie "decyduje" o tym, na czym skupić swoją uwagę oraz jak kształtować swoje zachowanie czy nawet styl wypowiedzi. Co prawda obecne są mechaniki, wzmacniające pewne **kategorie** zachowań, ale nie mówimy w tym przypadku o konkretnych instrukcjach.

![Agent działający według skryptu oraz bez niego](https://cloud.overment.com/2026-02-28/ai_devs_4_situational_awareness_fields-df1d0b5c-7.png)

Kształtowanie agentów w ten sposób stoi raczej w kontrze do tego, co zwykle oczekujemy od takich systemów. Co więcej, poniekąd neguje to także kierunek w jakim na ten moment zmierza generatywna sztuczna inteligencja. Uwaga wydaje się skupiać w większości na **podążaniu za instrukcjami** oraz rozwiązaniu problemu halucynacji czy niedeterministycznych zachowań. Ale gdy się nad tym zastanowimy, to podejście które omówiliśmy wcale tego nie wyklucza. Po prostu wprowadza element zmienności wpływającej zarówno na **doświadczenie** interakcji, ale także potencjalnie na jej skuteczność ze względu na **odkrywanie ścieżek** o których trudno byłoby pomyśleć na poziomie założeń projektu.

Pytanie więc w jaki sposób podejść do budowania takiego agenta oraz w jakich sytuacjach możemy sobie na niego pozwolić?

Przede wszystkim jest to miejsce w którym przestajemy mówić o agentach w kontekście wyłącznie programistycznym czy biznesowym. Przestajemy też postrzegać proces ich tworzenia jako problem **spełnienia założeń** czy nawet **kształtowania zachowań**. W zamian przechodzimy w obszary **stwarzania warunków** w których te elementy powstają samoistnie. W tym miejscu zaczynamy wchodzić w obszar architektury kognitywnej o której w kontekście modeli językowych mówi między innymi "[Cognitive Architectures for Language Agents](https://arxiv.org/pdf/2309.02427)".

Patrząc więc na agenta **03\_05\_awareness** warto przyjrzeć się instrukcjom, metadanym oraz strukturze informacji, którymi ten agent dysponuje. Całość przekłada się na następujące warstwy:

- **Tożsamość i "samoświadomość":** instrukcje skupiają się na zarysowaniu przestrzeni po której agent może się poruszać, zaznaczając przy tym zarówno jego możliwości i ograniczenia, ale też konieczność zwracania uwagi na różnice pomiędzy nimi. Agent dąży więc do tego, aby "czytać między słowami", "wychodzić z inicjatywą" czy rozpoznawać różnicę pomiędzy swoją bazową wiedzą, a zewnętrznym kontekstem.
- **Zdolności poznawcze:** obejmują instrukcje wpływające na zachowanie agenta w odpowiedzi na sytuację w której się znajduje poprzez **zadawanie pytań** pozwalających na podjęcie możliwie najlepszych kroków.
- **Inteligencja emocjonalna:** czyli podkreślanie roli odczytywania stanu emocjonalnego rozmówcy oraz jego możliwych intencji w celu **dopasowania** posiadanych informacji do celu, który chce osiągnąć użytkownik. Obejmuje to także sytuacje w których użytkownik **jeszcze nie wie** na czym mógłby się skupić.
- **Sposoby ekspresji:** dopasowanie stylu i formatu wypowiedzi do rozmówcy nie jest oczywiste w przypadku modeli językowych. W tym przypadku zachowanie to jest podkreślane sztucznie poprzez **metadane** dodane do wiadomości użytkownika.
- **Mechaniki wzmacniające:** zarówno w treści metadanych jak i wynikach zwracanych przez narzędzia pojawiające się mechaniki wzmacniające oczekiwane **postawy** modelu. W tej sytuacji przestajemy mówić o konkretnych działaniach, lecz raczej **schematach myślowych**, które model powinien brać pod uwagę.

![Kształtowanie zachowań agentów](https://cloud.overment.com/2026-02-28/ai_devs_4_behavior_shaping-5ff1c5f4-8.png)

W widocznych tu mechanikach mówimy o bardzo intensywnym wykorzystaniu rozległej **wiedzy modelu** oraz także jego umiejętnościach sięgających [Theory of Mind](https://arxiv.org/pdf/2505.00026), które obserwujemy już od wczesnych wersji modelu GPT-4 i które znacznie rozwinęły się w modelach, które dziś mamy do dyspozycji.

## Sterowanie rozumowaniem modelu

W przypadku tego agenta mamy do czynienia z instrukcjami wykraczającymi poza to, co widzieliśmy do tej pory, aczkolwiek po raz kolejny mówimy tu o dużej **generalizacji**. Przykładowo:

- Agent jest poinformowany o tym, że **posiada osobowość, nastrój i opinie** oraz **informacje na temat rozmówcy**. Jednak na początku każdej interakcji informacje te pozostają **rozmyte** dopóki nie zostaną **odkryte**.
- Agent zostaje poinformowany o możliwości **przywołania** informacji oraz, że powinien odkrywać je **stopniowo** w zależności od rozwoju interakcji.
- Agent powinien być **uważny** pod kątem mówienia rzeczy, na temat których kontekst może nie być jeszcze dostępny oraz, że narzędzie **think** może być wykorzystane do zauważenia oraz odkrycia luk pomiędzy tym, co **wie** oraz tym, co **może wiedzieć**.
- Agent zostaje poinformowany o tym, że wiedza na temat siebie, rozmówcy oraz znajomości z nim, a także szczegółów otoczenia pochodzą z zewnętrznego kontekstu, a nie ogólnej wiedzy jaką dysponuje (chodzi o bazową wiedzę modelu).
- Agent posiada wiedzę o tym, że wczytane informacje nie zawsze zawierają informacje, która musi być dostarczona użytkownikowi, ale stają się one elementem **zrozumienia** bieżącej sytuacji i mogą być wykorzystane do udzielenia odpowiedzi oraz dalszych kroków.
- Agent posiada pozwolenie na **luźne łączenie faktów** oraz wnioskowanie nie tylko na podstawie dostępnego kontekstu, ale potencjalnych powiązań wynikających z zasad według których funkcjonuje świat. Zostaje także podkreślona rola docierania do wiedzy, która nie została bezpośrednio wspomniana podczas rozmowy.
- Agent wie, że każdy kolejny temat rozmowy to potencjalnie nowa przestrzeń na informacje, których w danych momencie może nie mieć w kontekście. One także muszą zostać odkryte poprzez serię pytań oraz eksplorację, ale także zestawienie z wiedzą, którą już posiada.

Wszystkie powyższe instrukcje w jakiś sposób **kierują "snem" modelu**, ale jednocześnie nie mówimy tutaj o bezpośrednich poleceniach, regułach czy zasadach bezpośrednio **prowadzących** model w konkretną stronę. W ten sposób zostawiamy całą przestrzeń do interpretacji, a bieżący kontekst dodaje tu element "losowości" zwiększający dynamikę całej interakcji.

Co ciekawe, choć modele takie jak Claude Opus 4.6 posiadają bardzo mocno rozwinięte umiejętności związane z Prompt Engineeringiem, tak w tej sytuacji niemal w pełni zawodzą, ponieważ widocznym wyzwaniem jest dla nich tak szerokie **generalizowanie zadań**. Jak zwykle jednak okazują się bardzo dobrym towarzyszem procesu myślowego stojącego za kształtowaniem tak zgeneralizowanych instrukcji. Nasza rola nadal pozostaje tutaj kluczowa.

## Elastyczne formy prezentacji danych

Niedeterministyczne zachowania połączone z rozległą wiedzą modeli językowych mogą sprawdzić się także przy okazji prezentowania danych. Sama forma prezentacji również może zostać dopasowana przez AI poprzez połączenie **celu użytkownika** oraz **rodzaju danych do zaprezentowania**. Co więcej, możemy mówić nie tylko o wygenerowaniu interfejsu, lecz także jego dopasowaniu na podstawie feedbacku w formie nawet bardzo ogólnych wiadomości.

Najnowsze modele językowe, szczególnie w trybach **rozbudowanego rozumowania** (w OpenAI jest to **reasoningEffort**) radzą sobie zwykle bez problemów nawet z relatywnie złożonymi interfejsami generowanymi "w locie". Oznacza to, że w kontekście prezentacji danych nie mówimy już wyłącznie o wyświetlaniu prostych wykresów, ale wręcz paneli do pozwalających zobaczyć dane z różnych perspektyw.

Już od dłuższego czasu w interfejsach takich jak Claude czy ChatGPT obecna jest funkcjonalność określana zwykle jako **artifacts**. Pozwala ona agentowi na generowanie kodu HTML/CSS/JS, zwykle na potrzeby prostych interfejsów czy wspomnianej wizualizacji danych. Jednak wraz z rozwojem modeli w tym zakresie, możliwości tej funkcjonalności są wprost ogromne. I choć jak zwykle mówimy tu o dużej przestrzeni na halucynacje, tak jednocześnie to jak złożone artefakty potrafią dziś generować modele i to **bezbłędnie** wyraźnie się przesuwa.

Możemy się zresztą przekonać o tym gdzie ona dokładnie leży w przypadku agenta **03\_05\_artifacts**, który po uruchomieniu z pomocą polecenia **npm run demo** uruchomi **przeglądarkę** oraz interfejs CLI. Agent rozpocznie generowanie wizualizacji dla jednego z predefiniowanych zestawów danych testowych z którym dodatkowo będziemy mogli porozmawiać. Ze względu na ustawienia **poziomu rozumowania**, generowanie wizualizacji może trwać nawet kilka minut, więc potrzebna będzie chwila cierpliwości. Natomiast tymczasem, możemy przyjrzeć się budowie tego agenta, który obejmuje:

- **Dane testowe:** to po prostu pliki CSV bądź JSON z różnymi rodzajami informacjami, typowymi dla różnych procesów biznesowych. Agent po uruchomieniu zajmie się wizualizacją jednego z nich.
- **Rozpoznanie:** agent zapoznaje się z treścią danych i na tej podstawie decyduje o sposobie ich wizualizacji. Co ważne, nie opieramy się tu o kilka dostępnych opcji, lecz o ogólną wiedzę modelu bądź konkretne wymagania użytkownika.
- **Generowanie:** agent generuje interaktywny dokument HTML, który zostaje osadzony w izolowanym `iframe`. W tym miejscu mamy spore możliwości pod kątem kontroli uprawnień, co jest fundamentalnie ważne z powodów, które omawialiśmy przy okazji przykładów związanych z uruchamianiem narzędzi poprzez kod oraz sandboxów.
- **Optymalizacja:** w związku z tym, że mówimy tu o logice agenta, istnieje możliwość wprowadzenia modyfikacji w przypadku których agent **nie przepisuje** całego dokumentu, lecz aktualizuje tylko wybrane fragmenty, dokładnie tak, jak ma to miejsce w przypadku agentów do kodowania.

![Agent wizualizujący dane z pomocą HTML/JS](https://cloud.overment.com/2026-02-28/ai_devs_4_artifacts-57900cf6-0.png)

Wizualizacja danych obejmuje więc **interaktywny interfejs** uwzględniający filtrowanie, sortowanie bądź w niektórych przypadkach także aktualizację danych.

Tutaj agent ponownie musi być zaprojektowany tak, aby nie podążać w pełni za sztywno ustawionymi regułami. Jednocześnie może się zdarzyć, że niektóre obszary jego działania (na przykład sposób aktualizacji dokumentu) będzie musiał być precyzyjnie sterowany. Natomiast poprowadzenie tego procesu, nie będzie stanowiło już dla nas wyzwania.

![Przykład wizualizacji dopasowanej do zestawu danych](https://cloud.overment.com/2026-02-28/ai_devs_4_regional_margin-4d4d8484-d.png)

Na uwagę zasługują tutaj także opcje, które mamy do dyspozycji pod kątem samej funkcjonalności **artefaktów**. W praktyce, mówimy tutaj o dokumencie HTML, ale kod generowany przez agenta niemal zawsze będzie "wzbogacony" o dodatkowe konfiguracje i ustawienia. W tym przypadku mówimy o wczytaniu bibliotek takich jak:

1. **[Preact](https://preactjs.com/) + [HTM](https://www.npmjs.com/package/htm)**: generowanie komponentów
2. [TailwindCSS](https://tailwindcss.com/): stylowanie interfejsów
3. [Day.js](https://day.js.org/): obsługa dat
4. [Zod](https://zod.dev/): walidacja schematów
5. [Chart.js](https://www.chartjs.org/) / [d3](https://d3js.org/): prezentacja danych
6. [Papaparse](https://www.npmjs.com/package/papaparse): parsowanie danych

Oczywiście zestaw "predefiniowanych" narzędzi możemy dobrać indywidualnie do agenta, ale kluczowe jest przede wszystkim **poinformowanie go** o ich dostępności. Przy wyborze tych narzędzi warto kierować się przede wszystkim tym, jak dobrze są one znane LLM. Przykładowo Tailwind CSS jest już dostępny w wersji 4, ale celowo podłączyłem wersję 3, ponieważ modele znacznie lepiej się nią posługują. Także przy projektowaniu funkcjonalności takich jak artefakty nie zawsze będziemy podążać za "najlepszymi standardami", lecz nad optymalnym wyborem narzędzi, które ułatwią realizację celu. Tym bardziej, że mówimy tutaj o wciąż relatywnie prostych interfejsach tworzonych na potrzebę chwili.

## Generatywne UI i dynamiczne elementy interfejsu

Koncepcja artefaktów może mieć swoje zastosowania, ale jej zastosowanie na produkcji może stanowić wyzwanie ze względu na bardzo ograniczony poziom kontroli, który może okazać się krytyczny. Potrzeba ta jest bardzo widoczna i dlatego pojawiają się narzędzia takie jak [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview), [a2ui](https://a2ui.org/) czy [json-render](https://json-render.dev/), w przypadku których poziom kontroli jest zdecydowanie wyższy. Nierzadko mówimy także o większych możliwościach, takich jak **dwukierunkowa** komunikacja wykraczająca poza proste filtrowanie czy sortowanie danych, ale podejmowanie akcji mających odzwierciedlenie w zewnętrznych systemach.

W przykładzie **03\_05\_render** znajduje się agent bliźniaczo podobny do tego, który generował artefakty. Tutaj także po uruchomieniu **npm run demo** otwiera się przeglądarka w której po pewnym czasie pojawia się interaktywna wizualizacja. Jednak w tym przypadku LLM nie generuje całego kodu HTML / CSS / JS, lecz obiekt JSON opisujący poszczególne komponenty oraz ich bieżący stan. Niemożliwe jest więc znaczące odejście od predefiniowanej struktury, ale nadal **nie mamy tutaj gwarancji** uzyskania rezultatów pozbawionych błędów, aczkolwiek ryzyko ich wystąpienia jest zdecydowanie niższe.

Poniższa wizualizacja pokazuje, że w obu przypadkach poruszamy się wokół tej samej koncepcji, czyli **wykorzystania LLM do generowania interfejsów**. Jednak ten efekt możemy osiągnąć na różne sposoby. W przypadku JSON Render mamy do czynienia ze **stanem**, który możemy nie tylko **zainicjalizować**, ale także **zapisać i wczytać**. Innymi słowy, przechodzimy tu do zarządzania komunikacją w sposób znany z aplikacji, które projektujemy na co dzień.

![Różnica pomiędzy artefaktami HTML a Render](https://cloud.overment.com/2026-03-01/ai_devs_4_artifacts_vs_render-e17dfde9-e.png)

Idąc dalej, mamy jeszcze MCP Apps, czyli podejście do tego samego problemu zaproponowane przez **Model Context Protocol**. W tym przypadku mówimy o sytuacji w której agent otrzymuje do dyspozycji **narzędzia** umożliwiające **uruchomienie** interaktywnego interfejsu udostępnionego przez serwer. Interfejs ten jest **w pełni interaktywny**, a akcje podjęte przez użytkownika mogą być natychmiast synchronizowane z zewnętrznymi usługami. Następnie po zakończeniu interakcji model może uzyskać informację o **wprowadzonych zmianach** i tym samym dopasować swoje dalsze zachowanie.

Zatem w tym przypadku model **nie posiada dostępu** do kodu wygenerowanego interfejsu, a nawet do jego stanu **z wyjątkiem danych**, które zostają wprost udostępnione agentowi. Możemy to zobaczyć w praktyce w przykładzie **03\_05\_apps**, gdzie po jego uruchomieniu (**npm start**) możemy poprosić o wyświetlenie listy zadań. Wówczas otworzy się przeglądarka z **interfejsem**, który nam to umożliwi. Przed jej zamknięciem możemy **zsynchronizować stan**, który zostanie odzwierciedlony w pliku **todo.md**.

Poniżej widzimy schemat działania MCP Apps, który w bardzo dużym stopniu opiera się na tych samych koncepcjach, które obserwowaliśmy przy okazji korzystania z narzędzi. Różnica polega na tym, że tutaj wywołania narzędzi prowadzą także do wyświetlenia graficznego interfejsu, którego stan może być deterministycznie aktualizowany w wyniku działań użytkownika. W takim układzie wyraźnie zwiększona zostaje rola **hosta**, ponieważ wówczas odpowiada on nie tylko za interakcję między użytkownikiem a agentem, ale także obsługę interfejsu.

![MCP Apps](https://cloud.overment.com/2026-03-01/ai_devs_4_apps-52d75cb8-1.png)

Powyższe przykłady pokazują nam to, jak mocno generatywna sztuczna inteligencja zmienia podejście do **projektowania** interfejsów i to w pełnym ujęciu tego procesu - od planów, przez projekt, po wdrożenie, obsługę oraz rozwój. Nasza rola bardzo wyraźnie zmienia się z ręcznego budowania najdrobniejszych detali w stronę projektowania **struktur** po których poruszają się agenci AI. Podobnie jak w przypadku kształtowania logiki aplikacji w której pojawia się model językowy, projektowanie interfejsów również zaczęło polegać na sztuce **balansowania** pomiędzy przewidywalnością i stabilnym realizowaniem procesów, a dynamicznymi możliwościami oferowanymi przez modele generatywnego AI.

Warto także zauważyć, że koncepcje przez które tutaj przeszliśmy w większości się nie wykluczają i mogą być stosowane jednocześnie. Dyskusje "X vs Y" warto zmienić na "kiedy X, kiedy Y, kiedy X + Y", mając w tym na uwadze cele biznesowe, założenia projektu oraz realne możliwości, które daje nam sztuczna inteligencja.

## Fabuła

![https://vimeo.com/1176952176](https://vimeo.com/1176952176)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze piąty...

Nie wiem... no nie wiem... Nie rozumiem nic...

Automat negocjacyjny, który udało nam się zaprogramować, nawiązał kontakt z pierwszym z miast. Podjął negocjacje, wysłał sporo wiadomości i wtedy dowiedzieliśmy się, że czujniki sejsmiczne w tym mieście odnotowały, jak pulsuje ziemia. A chwilę później nie było już niczego.

Kroczące niszczyciele dotarły na miejsce i zmiotły miasto z powierzchni ziemi. Nie zostało nic. Nie przeżył też żaden mieszkaniec. Ponad 140 zabitych osób.

My tu siedzimy, programujemy rozwiązania, staramy się przechytrzyć systemy, ale po drugiej stronie są prawdziwi ludzie. Oni chcą po prostu przeżyć. A to my, nawiązując kontakt z ich miastem, zdradziliśmy ich lokalizację. Jedno z miast ocalałych zostało zniszczone... nie pierwsze już zresztą.

Na szczęście automat nie zdążył jeszcze nawiązać kontaktu z drugim miastem i zdecydowanie nie pozwolimy mu na to, aby podjął próbę takiego kontaktu. Wyślemy do tego drugiego miasta naszego człowieka. Musimy tylko zaplanować jego podróż. Ma on do dyspozycji kilka środków transportu, prowiant na drogę oraz ograniczony zapas paliwa.

Musisz odpowiednio rozplanować jego ruchy. Przekaż proszę do Centrali, którędy ma się udać i jaki pojazd ma wybrać. Gdy uda Ci się to odpowiednio rozplanować, wtedy nasz wysłannik podejmie negocjacje w sprawie części do turbiny wiatrowej.

Wiem, że rodzi się w Tobie bunt po tym, co usłyszałeś. Wiem, że może ogarnąć Cię beznadzieja, bo ludzie nie żyją i jest to w dużym stopniu nasza wina - nie zachowaliśmy należytej ostrożności.

Ale pamiętaj: mamy władzę nad czasem. Wszystko, co się wydarzyło, można cofnąć, ale tylko pod warunkiem, że uda nam się uruchomić maszynę czasu. Jeden skok wyzeruje wszystkie wydarzenia. Więc chociaż jest to wbrew logice, wierzę, że jeszcze pomożemy tym ludziom. Cofniemy czas.

## Zadanie praktyczne

Twoim zadaniem jest zbudowanie agenta, który wytyczy optymalną trasę dla naszego posłańca, który podejmie negocjacje w mieście Skolwin. Niewiele wiemy na temat tego, jak wygląda teren, więc z pewnością na początku będziemy musieli zdobyć mapę. Musimy też zdecydować się na konkretny pojazd, którym wyruszymy z bazy. Jest ich do wyboru kilka. Myślę, że bez problemu znajdziesz informacje na ich temat. Każdy pojazd spala paliwo. Im szybciej się porusza, tym więcej paliwa zużywa. Jednocześnie nasz wysłannik potrzebuje prowiantu. Im dłużej trwa podróż, tym więcej będzie wymagał jedzenia. Trzeba więc odpowiednio rozplanować tę drogę w taki sposób, by poruszać się możliwie szybko, ale jednocześnie tak, aby wystarczyło nam jedzenia i paliwa na dotarcie do celu.

Tym razem nie dajemy Ci dostępu do konkretnych narzędzi, a jedynie do wyszukiwarki narzędzi, która pomoże Ci zdobyć informację o pozostałych narzędziach. Używasz jej jak poniżej:

Endpoint: https://hub.ag3nts.org/api/toolsearch

```json
{
  "apikey": "tutaj-twoj-klucz",
  "query": "I need notes about movement rules and terrain"
}
```

Uwaga: wszystkie narzędzia porozumiewają się tylko w języku angielskim!

Wszystkie znalezione narzędzia obsługuje się identycznie jak toolsearch, czyli wysyła się do nich parametr 'query' oraz własny apikey.

Twoim zadaniem jest wysłać do centrali optymalną trasę podróży dla naszego wysłannika.

**Zadanie nazywa się savethem**, a dane wysyłasz do /verify

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "savethem",
  "answer": ["wehicle_name", "right", "right", "up", "down", "up","..."]
}
```

Tutaj znajdziesz podgląd trasy, którą pokonuje nasz człowiek:
https://hub.ag3nts.org/savethem\_preview.html

## Wskazówki

Co wiemy?

- wysłannik musi dotrzeć do miasta Skolwin
- pozyskane mapy zawsze mają wymiary 10x10 pól i zawierają rzeki, drzewa, kamienie itp.
- masz do dyspozycji 10 porcji jedzenia i 10 jednostek paliwa
- każdy ruch spala paliwo (no, chyba że idziesz pieszo) oraz jedzenie. Każdy pojazd ma własne parametry spalania zasobów.
- im szybciej się poruszasz, tym więcej spalasz paliwa, ale im wolniej idziesz, tym więcej konsumujesz prowiantu. Trzeba to dobrze rozplanować.
- w każdej chwili możesz wyjść z wybranego pojazdu i kontynuować podróż pieszo.
- narzędzie toolsearch może przyjąć zarówno zapytanie w języku naturalnym, jak i słowa kluczowe
- wszystkie narzędzia zwracane przez toolsearch przyjmują parametr "query" i odpowiadają w formacie JSON, zwracając zawsze 3 najlepiej dopasowane do zapytania wyniki (nie zwracają wszystkich wpisów!)
- jeśli dotrzesz do pola końcowego, zdobędziesz flagę i zaliczysz zadanie (flaga pojawi się zarówno na podglądzie, w API jak i w debugu do zadań)
