---
title: S03E04 — Budowanie narzędzi na podstawie danych testowych
space_id: 2476415
status: scheduled
published_at: '2026-03-26T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/tools-1773912026.png'
circle_post_id: 30844677
---
Budowanie lub generowanie narzędzi dla agentów AI nie musi dotyczyć wyłącznie samego **łączenia** systemu z zewnętrzną aplikacją lub serwisem. Nawet jeśli na rynku zaczynają pojawiać się oficjalne serwery MCP, CLI czy skille, nadal możemy potrzebować tworzyć własne, aby **spersonalizować** zachowanie agentów. Poza tym narzędzia wcale nie muszą dotyczyć zewnętrznych połączeń, lecz interakcji **wewnątrz naszego systemu**.

Rozszerzanie możliwości agentów jest więc ważną umiejętnością, dlatego poświęciliśmy jej tak dużo uwagi w dotychczasowych lekcjach. Jednocześnie coraz częściej obserwujemy sytuacje, w których agenci **samodzielnie budują narzędzia**. Nierzadko wykracza to poza proste zapytania API, ale wciąż nie mówimy jeszcze o kompleksowych integracjach. Dodatkowo autonomiczny proces generowania narzędzi jest bardzo trudny do kontrolowania, co na ten moment wyklucza jego zastosowania produkcyjne. Ale nic nie stoi na przeszkodzie, abyśmy skorzystali z aktualnych możliwości modeli w procesie kształtowania narzędzi począwszy od koncepcji, przez ich strukturę, implementację po testowanie oraz optymalizację.

## Koncepcja stosowania LLM przy tworzeniu narzędzi

Projektowanie narzędzi dla **agentów przez agentów** omawialiśmy już w lekcji **S01E03**. Opieraliśmy się tam na [szablonie serwera MCP](https://github.com/iceener/streamable-mcp-server-template) oraz **dokumentacji API**, które agenci kodujący szybko zamieniają w funkcjonalną integrację, ale jej ogólna jakość bywa dość niska. Dlatego teraz, wyposażeni w całą dotychczasową wiedzę, przejdziemy przez proces tworzenia wysokiej jakości narzędzi realizowany **wspólnie** z LLM.

Aby dobrze zrozumieć możliwości związane ze stosowaniem LLM przy kształtowaniu integracji, omówimy kilka przykładów powszechnie znanych serwisów, które być może już teraz są częścią naszej codzienności. Mam tutaj na myśli integracje z Google Calendar, Gmail czy Resend (jako przykład platformy dla maili transakcyjnych i newsletterów). Problem w tym, że jeśli przeszukamy Internet to z łatwością znajdziemy gotowe serwery MCP czy narzędzia CLI z których będziemy mogli natychmiast skorzystać. Nam jednak chodzi o **dopasowanie integracji do naszych potrzeb**.

Bo przykładowo sam pomysł **pełnego połączenia** agenta z firmową skrzynką e-mail, którego zadaniem jest jedynie obsługa wybranych kategorii wiadomości, to proszenie się o kłopoty. Ale już wtedy, gdy agent nie otrzyma narzędzia **gmail\_\_search**, lecz **gmail\_\_search\_support**, które będzie domyślnie zawężone i nie da mu przestrzeni na dotarcie do pozostałych wiadomości. Innym przykładem może być integracja z API do generowania grafik, np. z platformą **[Replicate](https://replicate.com/)**. Podłączenie agenta do ich oficjalnego serwera MCP to zły pomysł, jeśli nasza aplikacja wymaga tworzenia spersonalizowanych grafik ze ściśle określonymi ustawieniami.

Na potrzeby dzisiejszej lekcji **zrezygnujemy** z Model Context Protocol czy projektowania CLI. Naszym priorytetem będzie przećwiczenie procesu budowania **skutecznych narzędzi**. Później będziemy mogli zdecydować czy chcemy wykorzystać je przez MCP, CLI czy w dowolnej innej formie.

Zacznijmy więc od integracji z **Gmail** obejmującej typowe akcje, które powinny być dostępne dla agenta wspierającego nasze codzienne aktywności. Pierwszym krokiem będzie **"rozejrzenie się"** w celu zrozumienia, jakie opcje w ogóle mamy do dyspozycji. W tym celu powinniśmy:

- Zapisać treść dokumentacji [API Gmail](https://developers.google.com/workspace/gmail/api/guides) jako pliki Markdown - tutaj **możemy pominąć** obszary, których z góry wiemy, że nie chcemy adresować, np. "zarządzanie ustawieniami Gmail"
- Pobrać kod [oficjalnego SDK](https://github.com/googleapis/googleapis) (np. dla [Node.js](https://github.com/googleapis/google-api-nodejs-client#google-apis-nodejs-client))
- Uruchomić wybranego agenta do kodowania (może być dowolny)

API Gmail jest raczej dobrze znane LLM, więc na większość pytań będą w stanie odpowiedzieć "z pamięci". Natomiast odpowiadanie na podstawie plików i kodu źródłowego daje nam także możliwość samodzielnego przeczytania wybranych fragmentów.

Zanim przejdziemy dalej dodam, że omawiany przykład dostępny jest w folderze **03\_04\_gmail** i znajdziemy w nim nie tylko definicje narzędzi, ale także przykładowe dane testowe, ustawienia Promptfoo, przykładowe dane z API Gmail oraz wyniki testów. Natomiast samo działanie agenta można przetestować dopiero po utworzeniu projektu na stronie https://console.developers.google.com, co pozwoli nam na **lokalne** zintegrowanie z naszą skrzynką e-mail. AI jest w stanie skutecznie poprowadzić przez proces konfiguracji projektu oraz uzyskania danych autoryzacji, które należy umieścić w pliku **credentials.json**.

Tymczasem, mając zgromadzony kontekst możemy zadać pytanie o **zwięzłą listę dostępnych akcji, skupiających się na interakcji z wiadomościami**. W odpowiedz otrzymamy strukturę, która da nam szerokie spojrzenie na dostępne możliwości i pozwoli zastanowić się nad kształtem narzędzi agenta tak, aby odpowiadały naszym potrzebom.

![Skanowanie dostępnych akcji w API](https://cloud.overment.com/2026-02-25/ai_devs_4_gmail_api-f8b81038-d.png)

Już na podstawie powyższej listy możemy odpowiedzieć na pierwsze pytania, takie jak:

- Które z akcji są nam potrzebne, a które nie?
- Które akcje powinny zostać połączone **w jedno narzędzie?**
- Które akcje powinny zostać **zablokowane?**

Nie musimy jednak robić tego sami, bo sam proces może być interaktywny. Wystarczy zadać pytanie o **zaprojektowanie schematu input/output dla narzędzia do przeszukiwania wiadomości**. Poniżej widzimy przykładową odpowiedź AI, która jest pomocna, ale jej jakość jest bardzo niska. Od razu widzimy w niej wyraźne naruszenia dobrych praktyk projektowania narzędzi dla agentów.

![Przykład schematu narzędzia search\_messages](https://cloud.overment.com/2026-02-25/ai_devs_4_gmail_search-726795ae-a.png)

Przede wszystkim struktura **input** nie daje informacji o tym, jak stronicować zwrócone wyniki. Następnie samo pole "**to**" jest niewystarczające, ponieważ wiadomość może mieć więcej niż jednego odbiorcę. Nazwa pola "**date**" również mogłaby wyraźniej sugerować znaczenie tego pola. "**Snippet**" stanowi tutaj szum, bo jego treść jest za krótka, aby agent skutecznie mógł określić o czym jest wiadomość. Brakuje także załączników oraz metadanych określających czy e-mail został odczytany bądź czy w wątku znajduje się więcej wiadomości.

Inaczej mówiąc - otrzymana struktura daje nam jedynie **iluzję** poprawności. Budując narzędzia w ten sposób, nie możemy oczekiwać, że agent skutecznie będzie się nimi posługiwał.

Wystarczy jednak, że w odpowiedzi zapiszemy listę **dobrych praktyk**, które chcemy zastosować, a wówczas kolejna iteracja będzie zdecydowanie lepsza, co widać poniżej. Agent natychmiast zyskuje informację o etykietach i załącznikach, a także o statusach wiadomości. Tutaj moglibyśmy się zastanowić, czy **input** nie powinien umożliwiać agentowi decydowania o tym, jak szczegółowa ma być lista wyników.

![Poprawiona struktura interfejsu wyszukiwania wiadomości](https://cloud.overment.com/2026-02-25/ai_devs_4_gmail_search_improved-e459ddbb-9.png)

Podobną dyskusję możemy przeprowadzić na temat pozostałych narzędzi oraz ich kształtu. W jej trakcie zobaczymy wiele sugestii, spośród których będziemy musieli wybrać te, które według nas mają największą szansę sprawdzić się w praktyce. Chodzi nie tylko o ich wybór, ale także nadanie kształtu dla schematów input/output. Niestety początkowe sugestie modelu są dość kiepskie.

Poniżej mamy listę narzędzi: **search, read, send, modify, attachment**, która sama w sobie wygląda w porządku. Jeśli jednak przyjrzymy się schematom, to brakuje w nich **opisów właściwości** oraz **wskazówek dla agenta**, a do tego pojawiają się fundamentalne błędy, jak na przykład zwracanie załącznika w formie base64 (!!!!!), co dosłownie zabija kontekst modelu.

![Początkowa struktura narzędzi dla Gmail](https://cloud.overment.com/2026-02-26/ai_devs_4_initial_gmail_schema-97c36a14-2.png)

Pomimo swoich wad takie schematy stanowią bardzo dobry punkt startowy, ponieważ 60-70% pracy jest już wykonane. Naszym zadaniem jest więc **pokierowanie** agenta we właściwą stronę. Można to zrobić na przykład poprzez przesłanie **zestawu pytań bądź poleceń** oraz prośbę o **wypisanie obecnych w nich zasad**, które mogą zostać przełożone na kontekst całej integracji.

Mówiąc inaczej: **przesyłamy kilka wskazówek, które model rozszerza i przenosi na kontekst całej integracji**.

Wskazówki w moim przypadku wyglądały następująco:

```
- W przypadku braku wyników dla podanego zapytania, powinniśmy zwracać wskazówkę sugerującą zmianę jego treści bądź filtrów. 
- W przypadku błędów zapytania bądź problemów z API powinniśmy jasno wyjaśnić co się wydarzyło i co można z tym zrobić.
- Musimy zadbać także o problemy globalne, np. związane z autoryzacją
- Powinniśmy dołączać wskazówki dotyczące **łączenia akcji**, na przykład pobierania szczegółów wpisu bądź przechodzenia na kolejne strony.
- Dla akcji "read" agent nie powinien decydować o typie zasobu (wiadomość/wątek), a rozwiązanie identyfikatora powinno odbyć się programistycznie
- Dla akcji **modify** w odopowiedzi powinniśmy wprost zwracać pola, które zostały zmienione, aby agent miał natychmiastową wiedzę o tym, czy jego działania przyniosły efekt.
- Załącznik w gmailu **nie może** być prezentowany jako base64, lecz link kierujący do konkretnego zasobu, który może odczytać użytkownik bądź inny agent.
```

AI bez większych problemów naniesie poprawki, przez które będziemy musieli iterować kilka razy, stopniowo dochodząc do kształtu który uznamy za właściwy.

W przypadku narzędzia Gmail doszedłem do struktury, która po części jest **eksperymentalna** ponieważ zawiera kilka nowych pomysłów których skuteczność będzie trzeba sprawdzić w praktyce. Natomiast na poniższym schemacie widzimy już:

- Wspólną strukturę odpowiedzi dla **wszystkich narzędzi**. Jest to dobra praktyka każdego API, lecz tutaj obejmuje właściwości takie jak **next\_action, recovery oraz diagnostics**.
- Narzędzia **read/search** pozwalają agentowi kontrolować szczegółowość wyników.
- Narzędzia **modify** zwracają treść zmienionych właściwości, więc agent natychmiast widzi wynik swoich działań
- i naprawiliśmy błędy z wcześniejszego schematu, np. związane z formą zwracania załącznika (na potrzeby tego przykładu jest to placeholder)

Nowa struktura prezentuje się następująco:

![Finalna struktura narzędzi dla Gmail](https://cloud.overment.com/2026-02-26/ai_devs_4_final_gmail_schema-b6ac9251-f.png)

Taka dyskusja z AI na temat struktury narzędzi pozwala na bardzo szybkie iterowanie pomysłów, co pozwala na ich staranne dopracowanie. Może się jednak zdarzyć, że zacznie brakować nam pomysłów lub jedynie będzie nam się wydawać, że uzyskaliśmy efekt na którym nam zależy. Wówczas możemy zmienić taktykę i zamiast zadawać pytania, możemy poprosić o **wygenerowanie przykładowych interakcji**.

## Gromadzenie i generowanie zestawów danych testowych

Modele językowe świetnie sprawdzają się w generowaniu syntetycznych danych na potrzeby ewaluacji, o ile tylko nadamy im właściwy kontekst oraz zasady. Nawet jeśli mamy zaledwie wstępną strukturę narzędzi bądź agenta, możemy wykorzystać kod źródłowy jako punkt startowy. Agent po jego przeczytaniu może wygenerować kilka-kilkanaście przykładów interakcji z których możemy wybrać część, a następnie poprosić o generowanie kolejnych na ich podstawie.

Sami musimy zadbać o aspekty takie jak **różnorodność** czy **sens**, ponieważ AI ma raczej małą szansę na idealne dopasowanie odpowiedzi do naszych potrzeb, ponieważ pełen kontekst narzędzi nad którymi pracujemy może być albo trudny do przekazania, albo w ogóle może być jeszcze na etapie kształtowania.

Zestawy danych testowych mogą obejmować zarówno **pojedyncze interakcje** z poszczególnymi akcjami narzędzi, ale też sięgać dalej w interakcje **wieloetapowe**, charakterystyczne dla czatbotów bądź systemów agentowych. Dobrym pomysłem jest zdefiniowanie **kategorii** w ramach których chcemy się poruszać, a potem stopniowe rozbudowywanie każdej z nich.

Na tym etapie nie warto poświęcać zbyt dużo czasu na dopracowanie każdego wpisu, ponieważ ich użyteczność zacznie ujawniać się na etapie testowania.

> Treść poniższych pytań znajduje się w przykładzie **03\_04\_gmail** w katalogu **spec**.

![Przykładowe interakcje z agentem na temat gmail](https://cloud.overment.com/2026-02-25/ai_devs_4_gmail_examples-5fa1c6ae-7.png)

No bo tak wygenerowane scenariusze/przykłady, możemy wykorzystać nie tylko na etapie kreatywnym, ale także na etapie kształtowania ewaluacji czy nawet analizy ich wyników. Model na podstawie ich treści może ocenić nie tylko wyniki poszczególnych testów, ale także same testy! Jednak jak zawsze musimy pozostać zaangażowani w ten proces ponieważ agenci sami z siebie raczej nie poprowadzą tego procesu.

Jest to więc dobry moment, aby poprosić agenta o **zaimplementowanie** struktury narzędzi, którą mamy w tej chwili. Pozwoli nam to przejść do **ewaluacji**, które szybko zaczną ujawniać potencjalne problemy, albo bezpośrednio, albo poprzez podsuwanie nam pomysłów na możliwe usprawnienia.

Tym razem do ewaluacji nie wykorzystamy Langfuse, lecz [Promptfoo](https://www.promptfoo.dev/), czyli jedno z najlepszych narzędzi do ewaluacji "offline", czyli tych, które mają miejsce na etapie developmentu czy w trakcie publikowania aplikacji. Tutaj co prawda istnieją możliwości zintegrowania Promptfoo z Langfuse, ale to czy się na to zdecydujemy, zależy już od indywidualnych potrzeb projektu. Poza tym nic nie stoi na przeszkodzie, aby Langfuse pełnił głównie rolę obserwatora i ewaluacji online, a Promptfoo był narzędziem developerskim.

Aby szybko poznać możliwości Promptfoo, warto pobrać ich oficjalne repozytorium do zasobów naszego projektu i zapytać model o listę dostępnych asercji oraz o zrozumienie dostępnych interfejsów. Choć dziś LLM-y posiadają już ogólną wiedzę na temat tego narzędzia, posługiwanie się kontekstem zbudowanym na podstawie repozytorium zapewni nam dostęp do najnowszych funkcjonalności, co znacząco podniesie jakość wypowiedzi modelu.

Poniżej mamy przykład interakcji w której model wymienia dostępne typy asercji. Jeśli taki kontekst **połączymy** z zestawem danych testowych, o którym mówiliśmy przed chwilą, agent będzie w stanie wygenerować nam wstępne testy dla każdego z narzędzi. W tym miejscu warto jest zacząć od zaledwie kilku podstawowych, aby w ogóle je uruchomić i sprawdzić poprawność konfiguracji.

![Budowanie kontekstu na podstawie repozytorium Promptfoo](https://cloud.overment.com/2026-02-26/ai_devs_4_discovery-12e5fbee-5.png)

Tutaj ponownie **nic nie wydarzy się "samo"** i musimy pokierować model w stronę opracowania syntetycznych danych oraz ewaluacji dla poszczególnych narzędzi oraz scenariuszy. AI domyślnie będzie sugerować raczej proste, płytkie testy, które niewiele nam powiedzą. Co gorsza, nie będą podzielone na kategorie, co znacznie utrudni ich dalszą rozbudowę oraz modyfikacje.

Powinniśmy więc zadbać przede wszystkim o testy **poszczególnych narzędzi**, aby wiedzieć, jak dobrze model radzi sobie z ich indywidualną obsługą, oraz o testy **scenariuszy**, aby zrozumieć, jak skutecznie agent będzie **łączył dostępne narzędzia**. Istotne jest tutaj także, jak agent poradzi sobie w przypadku **wystąpienia błędów** oraz w sytuacjach, gdy podjęte akcje okażą się nieskuteczne.

![Przykładowa lista ewaluacji i zestawów danych testowych](https://cloud.overment.com/2026-02-26/ai-devs_4_evals_datasets-597cce6c-a.png)

Implementacją ewaluacji po stronie narzędzia Promptfoo może w pełni zająć się AI. Natomiast my musimy rozumieć ją na tyle dobrze, aby być w stanie zauważyć błędy logiczne w testach, które zbyt mocno odbiegają od rzeczywistości albo zostały zaprojektowane w taki sposób, że nie da się ich nie zaliczyć.

Poniżej widzimy scenariusze dla interakcji **wieloetapowych** występujących w przypadku pracy z agentem. Ewaluacje te przeprowadzane są niemal **bez wiadomości systemowej**, aby sprawdzić jak model domyślnie poradzi sobie z ich realizacją. Opieramy się więc tutaj przede wszystkim na **opisach narzędzi** oraz ich **schematach**, więc przynajmniej w teorii, jeśli agent bez dodatkowych instrukcji poradzi sobie z ich obsługą, to możemy założyć, że po wyspecjalizowaniu poradzi sobie z nimi jeszcze lepiej.

![Szczegóły ewaluacji scenariuszy](https://cloud.overment.com/2026-02-26/ai_devs_4_evals_detailed-aa1655dd-a.png)

Mając gotowe zestawy danych i ewaluacje, możemy sprawdzić nie tylko jak dobrze poradzi sobie z nimi wybrany przez nas model. Dobrym pomysłem jest przetestowanie **kilku modeli**, dzięki czemu dowiemy się, czy możliwe jest skorzystanie z tańszych i szybszych alternatyw. W tym przypadku wziąłem pod uwagę **gpt-5.2, gpt-5-mini** oraz **gpt-4.1** (to model non-reasoning) jako przykłady modeli o różnych możliwościach i charakterystyce.

Po wykonaniu testów i wstępnej weryfikacji, przekazałem wyniki do LLM z prośbą o interpretację. Agent może nam ułatwić analizę dużych zestawów danych poprzez przedstawianie ich na różne sposoby. Dzięki temu dowiedzieliśmy się, że **wszystkie modele zaliczyły testy**, ale każdy z nich zrobił to nieco inaczej i przykładowo:

- GPT-4.1 potrzebował najmniej kroków, a jego wypowiedzi były bardzo profesjonalne, ale zdarzały mu się błędy prowadzące do **niepełnych** odpowiedzi.
- GPT-5.2 potrzebował najwięcej czasu, a jego wypowiedzi były bardzo techniczne, korzystał nawet z identyfikatorów, co jest dość mało przyjazne z punktu widzenia użytkownika. W zamian, jego skuteczność była perfekcyjna.
- GPT-5-mini zaliczył testy gdzieś pomiędzy pozostałymi modelami.

![Wyniki ewaluacji dla modeli gpt5.2 gpt-5-mini oraz gpt-4.1](https://cloud.overment.com/2026-02-26/ai_devs_4_evals_results-d77391e0-1.png)

## Wybór zestawu modeli w celu zwiększania efektywności

Biorąc pod uwagę wyniki powyższych ewaluacji, można uznać, że pod uwagę możemy brać wyłącznie GPT-5.2 i GPT-5-mini. Model GPT-4.1 co prawda zaliczył wszystkie testy i zrobił to najbardziej efektywnie, ale ogólna stabilność jego działania już teraz ujawniła problemy, które z całą pewnością będą pogłębiać się na produkcji.

Wybór modeli musi brać też pod uwagę szerszy kontekst, który wykracza poza jedno narzędzie. Bo jeśli zakres odpowiedzialności agenta będzie wykraczać poza integrację z Gmail bądź złożoność zadań będzie wiązała się z koniecznością przetwarzania rozbudowanego kontekstu, to patrzenie w stronę mniejszych modeli nie ma sensu. W tym miejscu w ogóle możemy rozważyć utworzenie ewaluacji sprawdzających modele dokładnie pod tym kątem.

Ale jeśli mówimy o integracji mającej na celu podejmowanie prostych akcji, to być może będziemy mogli skorzystać z jeszcze mniejszych, szybszych i tańszych modeli. Fakt, że posiadamy ewaluacje sprawia, że z łatwością będziemy mogli sprawdzić ich skuteczność i szybko odpowiedzieć sobie, czy optymalizacja w zakresie wyboru modelu w ogóle ma sens.

W omawianym przykładzie mamy integrację bezpośrednio z API OpenAI, ale możemy rozważyć także podłączenie platform takich jak OpenRouter czy wprost odwrotnie - własnych serwerów do lokalnej inferencji. W końcu może się okazać, że zastosowanie modeli typu Qwen 3.5 będzie wystarczające. Ostatecznie nawet jeśli okaże się, że zdecydujemy się na pracę wyłącznie z "najmocniejszym" dostępnym modelem to i tak możemy poświęcić czas na optymalizację interfejsu narzędzi dla mniejszych modeli. Jest to forma narzucania ograniczeń, które pozwolą uzyskać jeszcze większą skuteczność w połączeniu z lepszymi modelami.

## Automatyczna optymalizacja schematu oraz odpowiedzi

Planowanie interfejsów narzędzi, zestawów danych testowych i ich późniejsza ewaluacja to wymagająca i często żmudna praca. Jednak jak widzieliśmy już na przykładzie tworzenia narzędzi do interakcji z Gmail, na każdym kroku możemy liczyć na istotne wsparcie ze strony agentów do kodowania.

Choć zaangażowanie z naszej strony, przynajmniej na ten moment, musi być bardzo duże, tak sam proces optymalizacji może być w dużym stopniu zautomatyzowany. W końcu na każdym etapie możemy opracować dokumenty opisujące **dobre praktyki** i **checklisty**, które powinny być przestrzegane. W związku z tym, że agenci do kodowania mają możliwość swobodnego czytania plików i posługiwania się terminalem, możemy poprosić je o **zapoznanie się z interfejsem narzędzi oraz testami**, a następnie o przeprowadzenie ewaluacji oraz jej interpretację, a nawet sugestie dotyczące usprawnień.

Dopiero na etapie względnego **ustabilizowania** całego procesu, możemy sprawdzić możliwość niemal pełnej automatyzacji procesu **weryfikowania najnowszych modeli**. Mówimy tu zarówno o ewentualnym przełączeniu się na **mocniejsze** modele, jak i te **słabsze**. Na rynku wciąż pojawiają się modele Open Source, na przykład Minimax, GLM czy Qwen, których skuteczność stopniowo staje się na tyle wystarczająca, że przynajmniej część agentów bądź workflow śmiało może być na nie przełączona, znacznie redukując koszty, a niekiedy nawet podnosząc ogólną jakość (np. ze względu na lepszy styl wypowiedzi).

## Fabuła

![https://vimeo.com/1175524206](https://vimeo.com/1175524206)

## Transkrypcja filmu z Fabułą

"Numerze piąty! Idzie nam naprawdę świetnie. Moduł został zainstalowany. Czas zająć się kolejnym wyzwaniem.

Pamiętasz, że mieliśmy informację o niestabilnym napięciu w logach? Niestety nie uda nam się tutaj legalnie doprowadzić więcej energii. Myślałem, że odblokowana linia energetyczna w zupełności nam wystarczy, ale po pierwsze zasilanie w niej jest niestabilne, a po drugie potrzebujemy więcej mocy na uruchomienie systemów podtrzymywania pracy elektrowni.

Nasi technicy wpadli na pomysł, że można by wykorzystać energię słońca lub energię wiatru. Energia słońca odpada ze względu na ilość pyłu utrzymującego się w powietrzu. Wiatru mamy za to pod dostatkiem, ale nie mamy turbiny. Istnieje jednak ogromna szansa na to, że uda nam się namierzyć handlarzy, którzy sprzedadzą nam turbinę i wszelkie podzespoły niezbędne do jej uruchomienia.

Po wielkiej korekcie zostało jeszcze w naszym kraju kilka miast, w których mieszkają ocalali. Wbrew pozorom nie wszyscy, którzy przetrwali to wydarzenie, to ci, których wybrał system. Są też tacy, którzy mieli trochę więcej szczęścia. To oni tworzą ruch oporu i to oni zamieszkują miasta ocalałych.

Mamy przygotowany automatyczny system do nawiązywania kontaktu ze wspomnianymi miastami. System sam, za pomocą szyfrowanego kanału, nawiąże kontakt z przywódcami miast i sam podejmie też kwestię negocjacji.

Czego w takim razie potrzebuję od Ciebie? Na podstawie danych, które zgromadziliśmy, przygotuj proszę narzędzia dla systemu, o którym wspomniałem, tak aby agent, który tam działa, był w stanie z nich korzystać. Agent zawsze wysyła do podanego przez Ciebie endpointa tylko parametry w formacie JSON, jakie chciałby przekazać do wybranego narzędzia. Niestety, nie wysyła tych danych w ustrukturyzowanej formie, więc spodziewaj się, że parametr ten będzie w języku naturalnym.

Mamy tu także pewne ograniczenia techniczne, ponieważ możesz zdefiniować maksymalnie dwa narzędzia dla naszego agenta. Nie umie on obsłużyć ich więcej, ale myślę, że przy odrobinie optymalizacji, to powinno wystarczyć.

Więcej szczegółów, jak zawsze, znajdziesz w notatce do tego nagrania.

Powodzenia!"

## Zadanie

Twoim celem jest przygotowanie jednego lub dwóch narzędzi, które nasz automat wykorzysta do namierzenia miast oferujących wszystkie potrzebne mu przedmioty. Wtedy będzie mógł podjąć negocjacje cen ze znalezionymi miastami.

Automat sam wie najlepiej, co jest nam potrzebne do uruchomienia turbiny wiatrowej, aby zapewnić nam dodatkowe źródło zasilania.

Agent podaje parametry do Twoich narzędzi w języku naturalnym. Pamiętaj też, że musisz tak opisać te narzędzia, aby automat wiedział, jakie parametry i do którego narzędzia powinien przekazać.

Celem naszego agenta jest uzyskanie informacji, gdzie może kupić (nazwy miast) wszystkie potrzebne mu przedmioty. Potrzebne nam są miasta, które oferują WSZYSTKIE potrzebne przedmioty jednocześnie. Nasz agent musi pozyskać te informacje, korzystając z Twoich narzędzi.

Oto pliki będące podstawą wiedzy Twojego agenta:
https://hub.ag3nts.org/dane/s03e04\_csv/

W razie problemów użyj też naszego narzędzia do debugowania, abyś dokładnie wiedział, co dzieje się w backendzie.

**Nazwa zadania:** negotiations

Swoją odpowiedź jak zawsze do /verify

Przykład odpowiedzi:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "negotiations",
  "answer": {
    "tools": [
      {
        "URL": "https://twoja-domena.pl/api/narzedzie1",
        "description": "Opis pierwszego narzędzia - co robi i jakie parametry przyjmuje w polu params"
      },
      {
        "URL": "https://twoja-domena.pl/api/narzedzie2",
        "description": "Opis drugiego narzędzia - co robi i jakie parametry przyjmuje w polu params"
      }
    ]
  }
}
```

Agent wysyła zapytania POST do Twojego URL w formacie:

```json
{
  "params": "wartość przekazana przez agenta"
}
```

Oczekiwany format odpowiedzi:

```json
{
  "output": "odpowiedź dla agenta"
}
```

#### Ważne ograniczenia

- Odpowiedź narzędzia nie może przekraczać 500 bajtów i nie może być krótsza niż 4 bajty
- Agent ma do dyspozycji maksymalnie 10 kroków, aby dojść do odpowiedzi
- Agent będzie starał się namierzyć miasta dla 3 przedmiotów
- Możesz zarejestrować najwyżej 2 narzędzia (ale równie dobrze możesz ogarnąć wszystko jednym)
- Jeśli agent nie otrzymał żadnej odpowiedzi od narzędzia, to przerywa pracę

#### Jak udostępnić swoje API?

Zrób to podobnie jak w zadaniu S01E03. Możesz postawić endpointy na dowolnym serwerze, który jest publicznie dostępny, albo wykorzystać rozwiązania takie jak np. ngrok.

#### Weryfikacja

Weryfikacja jest asynchroniczna — po wysłaniu narzędzi musisz poczekać kilka sekund, a następnie odpytać o wynik. Zrobisz to wysyłając na ten sam adres /verify zapytanie z polem "action" ustawionym na "check":

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "negotiations",
  "answer": {
    "action": "check"
  }
}
```

Możesz też sprawdzić wynik na panelu do debugowania w Centrali: https://hub.ag3nts.org/debug

### Krok po kroku

1. Pobierz pliki z wiedzą z lokalizacji https://hub.ag3nts.org/dane/s03e04\_csv/
2. Zastanów się, ile i jakich narzędzi potrzebujesz do przeszukiwania informacji o tym, jakie miasto oferuje na sprzedaż konkretny przedmiot
3. Przygotuj swoje 1-2 narzędzia, które umożliwią sprawdzenie, które miasto posiada poszukiwane przedmioty. Bądź gotowy, że agent wyśle zapytanie np. jako naturalne zapytanie "potrzebuję kabla długości 10 metrów" zamiast "kabel 10m"
4. Zgłoś adresy URL do centrali w ramach zadania i koniecznie dobrze opisz je, aby agent wiedział, kiedy ma ich używać i jakie dane ma im przekazać
5. Agent będzie używał Twoich narzędzi tak długo, aż zgromadzi wszystkie potrzebne informacje niezbędne do stwierdzenia, które miasta posiadają jednocześnie wszystkie potrzebne mu przedmioty
6. Agent sam zgłosi do centrali, które miasta znalazł i jeśli będą one poprawne, to otrzymasz flagę
7. Odbierz flagę za pomocą funkcji "check" opisanej wyżej lub odczytaj ją przez narzędzie do debugowania zadań. Pamiętaj, że agent potrzebuje trochę czasu (minimum 30-60 sekund), aby przygotować dla Ciebie odpowiedź
