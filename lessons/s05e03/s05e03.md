---
title: S05E03 — Rozwój funkcjonalności
space_id: 2476415
status: scheduled
published_at: '2026-04-08T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/staff-1775197339.png'
circle_post_id: 31353101
---
Rozwijanie aplikacji, której podstawę stanowią duże modele językowe można porównać do rozwijania klasycznych aplikacji, ale w których tempo zmian jest nawet kilkukrotnie większe. Zmiany dotykają niemal wszystkich obszarów aplikacji, od interfejsu po bazy danych i konfiguracje serwerów.

Nawet pomimo wsparcia ze strony AI, rzetelnej współpracy i maksymalnego zaangażowania z naszej strony, a nie zabawy w „vibe coding”, znacznie szybciej pojawiają się wyraźne efekty długu technicznego, którym trzeba zarządzać lepiej niż kiedykolwiek. Poza tym, takie projekty wymagają od nas podejmowania jeszcze lepszych decyzji oraz dbałości o szczegóły.

Jak już mieliśmy okazję się przekonać, generatywne aplikacje posiadają także szereg dodatkowych komponentów, które wymagają naszej uwagi. Projektowanie instrukcji, strumieniowanie odpowiedzi, emitowanie i odbieranie zdarzeń, zaawansowane przetwarzanie dokumentów, wykorzystanie sandboxów czy projektowanie ewaluacji - jest tego całkiem sporo, a nawet nie wspomnieliśmy o zupełnie nowych zagrożeniach, przed którymi możemy chronić się niemal wyłącznie na poziomie decyzji projektowych.

W związku z powyższym, dziś wyjdziemy ponad początkowe założenia projektów czy nawet budowanie aplikacji i skupimy się na perspektywie długoterminowej. Treść tej lekcji stanowi także zbiór moich doświadczeń z budowy rozwiązań AI na przestrzeni ostatnich 3 lat, czyli niemal od premiery ChatGPT.

## Charakterystyka rozwoju generatywnych aplikacji

Patrząc na rozwój generatywnej sztucznej inteligencji, można odnieść wrażenie, że wszystko zmienia się co trzy miesiące. Co prawda sam rozwój jest trudny do podważenia, ale praktyczne doświadczenia z pracy z tą technologią pokazują nieco inny obraz.

Wystarczy spojrzeć na **fundamenty**, takie jak **architektura modeli** oraz wynikające z niej możliwości i ograniczenia. Wówczas zauważymy, że przez ostatnie 3 lata, na tym poziomie nie zaobserwowaliśmy zbyt wielu znaczących zmian. Główny wysiłek badaczy skupił się na **skalowaniu** oraz **generowaniu syntetycznych danych** na potrzeby dalszego treningu modeli, szczególnie w obszarach, które można automatycznie weryfikować (np. nauki ścisłe, a także programowanie). Widzieliśmy także rozwój modeli w zakresie "**rozumowania**" odbywającym się na etapie inferencji, co poniekąd można nazwać przełomem. Jednak nie jest to przełom rangi następcy [architektury transformerów](https://arxiv.org/abs/1706.03762), a przynajmniej niewiele na to wskazuje.

W rezultacie wszystkie podstawowe mechaniki, takie jak **autoregresja, tokenizacja, limity kontekstu, limity zakresu wiedzy bazowej** czy sam problem **halucynacji i prompt injection** pozostały albo niezmienne, albo zauważyliśmy w nich postęp, ale raczej nikt nie uznaje tego za rewolucyjne zmiany. Pomimo tego, suma tych małych zmian sprawia, że możemy osiągnąć zdecydowanie więcej. Możliwości wzrastają jeszcze bardziej, gdy weźmiemy pod uwagę nowe techniki pracy oraz rozwój narzędzi (które w większości omówiliśmy).

Dla nas oznacza to mniej więcej tyle, że:

- Względnie stałe fundamenty sugerują, że **uzasadniona jest inwestycja czasu w zrozumienie głównych zasad działania modeli** (polecam zapoznać się z artykułem [What ChatGPT is doing](https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/)). Tutaj nawet jeśli sięgniemy po materiały z pierwszej edycji AI\_devs, to znajdziemy w nich opisy wyżej wymienionych mechanik, które nadal pozostają aktualne. Różnica pojawia się jednak na poziomie liczb (np. rozmiaru tokenów, poziomu halucynacji czy zakresu wiedzy bazowej). Oznacza to też, że przy projektowaniu aplikacji możemy zwracać uwagę na logikę, która opiera się o te **fundamentalne zasady**, ponieważ tutaj możemy spodziewać się mniejszej dynamiki zmian, o ile nie dojdzie do jakiegoś znaczącego przełomu w dalszych badaniach.
- Bardzo wyraźnie zmieniają się **możliwości modeli, techniki pracy** oraz **dostępne narzędzia**. Różnice występują także na poziomie **otoczenia**, ponieważ różne aplikacje, serwisy czy nawet API, stają się zdecydowanie bardziej otwarte na agentów. Oznacza to, że wszystko to, co nie dotyczy fundamentalnych mechanik modeli, może znacząco się zmienić. Jednocześnie większość uwagi skupia się teraz na systemach **agentowych** w przypadku których stopniowo wzrasta poziom autonomiczności.

Ujmując to inaczej, rozwój generatywnej sztucznej inteligencji jest **stabilny u podstaw** ale **bardzo dynamiczny** na wyższych poziomach. Do czasu osiągnięcia znaczącego przełomu możemy więc brać to pod uwagę zarówno przy nauce nowych umiejętności, jak i rozwoju aplikacji.

![Dwuznaczność rozwoju generatywnej sztucznej inteligencji](https://cloud.overment.com/2026-03-23/ai_devs_4_ai_duality-322aa9a7-0.png)

Widoczna powyżej **"dwuznaczność"** generatywnej sztucznej inteligencji zauważalna jest także na poziomie architektury aplikacji, ponieważ obserwujemy tam zarówno **znaczące uproszczenia**, jak i **ogólny wzrost złożoności** - obie te rzeczy wzajemnie się wykluczają, więc doprecyzuję:

- **Znaczące uproszczenia**, wynikają z faktu, że zdecydowanie większa część logiki jest **oddelegowana do modelu**. Agenci stają się na tyle skuteczni, że samo wyposażenie ich w narzędzia pozwala na uzyskanie często lepszych rezultatów w porównaniu z logiką tworzoną samodzielnie. Przykładem mogą być systemy RAG, które jeszcze do niedawna opierały się o rozbudowany workflow, wielopoziomowe analizy zapytań oraz gromadzenia kontekstu. Natomiast dziś mają formę serii narzędzi, którymi agent posługuje się w sposób dopasowany do bieżącej sytuacji. Z punktu widzenia architektury oraz kodu jaki musimy stworzyć, mówimy tutaj o wyraźnym **uproszczeniu**
- **Ogólny wzrost złożoności** wiąże się natomiast z tym, że wzrost możliwości agentów wymaga stworzenia im środowiska w którym mogą dość swobodnie działać, ale też nie przekraczać wyznaczonych przez nas granic. Równolegle pojawia się także potrzeba wsparcia multimodalnych treści, zaawansowanego przetwarzania dokumentów czy stworzenia rozwiązań umożliwiających działanie w długich horyzontach czasu bądź przeciwnie, w czasie rzeczywistym.

![Dwuznaczność rozwoju architektury aplikacji](https://cloud.overment.com/2026-03-23/ai_devs_4_architecture_duality-9106a1e4-a.png)

Także tutaj również mamy do czynienia z pewną "dwuznacznością". Bo z jednej strony główne mechaniki agentów stają się coraz prostsze, ale zwiększa się złożoność ogólnej architektury, która kształtuje środowisko w którym się poruszają.

Patrząc na to, można powiedzieć, że programowanie klasycznych aplikacji jest jak budowanie elementów linii produkcyjnej. Natomiast budowanie generatywnych aplikacji, jest jak stworzenie fabryki zdolnej do ich samodzielnego kształtowania oraz zarządzania.

![Porównanie klasycznych aplikacji z generatywnymi na przykładzie linii produkcyjnej](https://cloud.overment.com/2026-03-24/ai_devs_4_building-d6c35d82-1.png)

Zatem rozwój generatywnych aplikacji uwzględnia potrzebę odnalezienia się w nieco innym kontekście niż ten, który znaliśmy do tej pory. Konkretnie mam tu na myśli wspomniane - **stałe fundamenty, szybko rozwijający się ekosystem, wysoką elastyczność architektury, dbanie o szczegóły** oraz odchodzenie od kształtowania detali implementacyjnych poszczególnych procesów na budowanie rozwiązań zdolnych do ich dynamicznej realizacji.

Jeśli przełożymy to teraz na rzeczywistość produkcyjną, to na przestrzeni ostatnich trzech lat mogliśmy obserwować następujące zmiany:

- **Wyścig dostawców:** co kilka miesięcy mają miejsce premiery nowych modeli. Wraz z nimi zwykle pojawiają się nowe możliwości, funkcjonalności API, większa wydajność czy niższe koszty. Skorzystanie z tych zmian może przełożyć się więc na realne korzyści naszej aplikacji, więc warto zostawić sobie przestrzeń na wsparcie więcej niż jednego providera.
- **Rozwój agentów:** przejście od prostych czatbotów do agentów było znaczącą zmianą w architekturze, ponieważ logika agentowa zastąpiła bądź znacząco zmieniła istniejącą logikę. Na przykład systemy **RAG**, które do tej pory opierały się o wieloetapowy proces rozpoznawania intencji, transformacji zapytań oraz wyszukiwania, dziś mają formę **Agentic RAG** i są w większości realizowane przez agenta wyposażonego w znacznie prostsze narzędzia. Logika agentowa staje się coraz bardziej skuteczna i coraz częściej stanowi **domyślne** podejście przy projektowaniu funkcjonalności. Dopiero gdy mamy bardzo istotny powód by z niej nie skorzystać, wybieramy deterministyczną logikę.
- **Rozwój multimodalności:** możliwość przetwarzania innych treści niż tekst również realnie wpłynęła na różne obszary architektury aplikacji, na przykład samą komunikację czy proces przechowywania danych. Obecnie już domyślnie warto zakładać, że nasz system może mieć do czynienia nie tylko z tekstem, ale także obrazem czy audio.
- **Rozwój narzędzi:** powtarzające się problemy i wynikające z nich potrzeby są coraz częściej adresowane przez rozszerzenia bądź gotowe narzędzia. Dobrym przykładem są różnego rodzaju biblioteki pomocne przy projektowaniu interfejsów (np. wspomniany w poprzedniej lekcji Streamdown).
- **Integracja z systemem:** agenci coraz częściej funkcjonują w terminalu, sandbox'ie bądź jako aplikacja desktopowa. Przyczyną jest potrzeba korzystania z narzędzi CLI, bezpośredni dostęp do przeglądarki, systemu plików bądź innych, natywnych funkcjonalności. To wszystko ma realny wpływ na sposób projektowania aplikacji, chociażby ze względu na potrzebę integracji z lokalnym środowiskiem użytkownika czy konfiguracją przechowywaną na jego urządzeniu.

Bardzo trudno jest przewidzieć, jakie zmiany zajdą w kolejnych latach. Tym bardziej że jeszcze 3 lata temu mało kto spodziewał się, że dziś będziemy mówić o rozbudowanych systemach wieloagentowych czy agentach posługujących się komputerem. Poza tym obecnie obserwujemy raczej sygnały rosnącego przyspieszenia, wynikającego chociażby ze znaczącego wzrostu zainteresowania AI w naszej branży.

## Migracje na nowsze wersje modeli i zmiany API

Dotychczasowy rozwój API sugeruje, że wciąż jesteśmy na etapie jego kształtowania, więc możemy spodziewać się dalszych zmian. Należy jednak zachować ostrożność, szczególnie wobec funkcjonalności, które bardzo mocno uzależniają nas od danego providera.

Dobrym przykładem jest [Assistants API](https://developers.openai.com/api/reference/resources/beta/subresources/assistants/methods/create), które dziś ma status **deprecated**, a według OpenAI był to jedynie etap przejściowy, na podstawie którego powstało Responses API. Choć wiele wspólnych cech sugeruje, że tak było, to zaraz po premierze branża mówiła niemal o rewolucji oraz tym, jak przyszłościowy jest ten interfejs. Pomimo tego Assistants API nie zostało szeroko wykorzystane, a 15 miesięcy później zostało zastąpione.

Natomiast teraz jesteśmy 11 miesięcy od premiery Responses API i różnica w tym przypadku jest ogromna, ponieważ format ten przyjął się nie tylko przez użytkowników OpenAI, ale również innych providerów i praktycznie wszystkie biblioteki, SDK czy frameworki i coś takiego dało się zauważyć zaledwie 3-4 miesiące od ogłoszenia Responses API.

Pojawia się więc tutaj pytanie: **w jaki sposób rozpoznać nowości na które warto zwrócić uwagę?**

Niemal od premiery ChatGPT reakcje branży na wszystkie pojawiające się nowości są bardzo intensywne. Wyraźna narracja marketingowa, ogrom komentarzy w mediach społecznościowych oraz mnóstwo pobudzających wyobraźnię prezentacji generują dużą ilość szumu informacyjnego. Tylko na tej podstawie bardzo trudno jest jednoznacznie określić realną użyteczność danego rozwiązania. Nieporównywalnie lepiej jest więc **samodzielnie sprawdzić** to z czym mamy do czynienia - wówczas nasze dotychczasowe doświadczenie pozwoli ocenić, czy powinniśmy inwestować więcej uwagi, czy wprost przeciwnie. Może się tu jednak zdarzyć, że **zwyczajnie się pomylimy.** Warto więc jest zachować **otwartość** oraz **dystans** do takich sytuacji i gdy po kilku tygodniach ten sam temat wielokrotnie do nas wraca, to jest to sygnał, że powinniśmy dać mu drugą szansę.

![Sygnały, które warto obserwować przy nowych funkcjonalnościach](https://cloud.overment.com/2026-03-24/ai_devs_4_news-eadc8c0a-8.png)

Przekładając to na Assistants API, dało się zauważyć, że temat ten pojawiał się przy różnych okazjach, ale jego obecność zdecydowanie malała z czasem. Dla mnie był to sygnał, że nie warto poświęcać mu czasu. Choć łatwo jest teraz to oceniać, patrząc wstecz, wielokrotnie przekonałem się, że wyżej wymienione zasady są dość użyteczne.

Poza powyższymi ogólnymi zasadami, można opierać się także o wiedzę z obszaru badań prowadzonych przez głównych providerów (np. OpenAI) oraz techniczne rozmowy z największych podcastów. W obu przypadkach możemy trafić na różne wskazówki, które pozwolą nam lepiej zrozumieć kierunek rozwoju, a niekiedy także wprost dowiedzieć się o nadchodzących funkcjonalnościach. Jednym z ciekawszych dokumentów jest też [Model Spec](https://model-spec.openai.com/2025-12-18.html), który ma charakter dość otwartej dyskusji na temat rozwoju API oraz samych modeli. Inaczej mówiąc, można w nim znaleźć informacje na temat **kierunku w jakim zmierzamy**. Oczywiście trudno jest przewidzieć przyszłość oraz to, czy postawione założenia zostaną zrealizowane. Natomiast ostatnie lata pokazały nam, że dobrze jest unikać sceptycznych postaw, ponieważ mogą nas one skutecznie blokować przed nowymi możliwościami. Z drugiej strony warto zachować zdrowy dystans wobec chwilowych trendów, które znikają szybciej niż się pojawiły.

Tymczasem, istotne zmiany zachodzą także pomiędzy modelami. Tutaj jednym sposobem na to, aby sprawdzić, czy nowy model ma lepszy wpływ na naszą aplikację, jest przekonanie się o tym w praktyce. W przypadku małych aplikacji, gdzie interakcja z LLM jest bardzo ograniczona, można to zrobić ręcznie. Jednak im bardziej złożony jest system, tym większą wartość dają ewaluacje, które omawialiśmy w trzecim tygodniu AI\_devs. Są tu jednak pewne detale, o których do tej pory nie mieliśmy okazji wspomnieć. Mianowicie:

- Modele zwykle wychodzą w kilku wersjach (np. główna / mini / nano). Podczas gdy główna wersja jest zazwyczaj zauważalnie lepsza od poprzednich, te mniejsze potrafią jedynie sprawiać wrażenie większych możliwości. Warto więc poświęcić więcej czasu na ich ewaluację.
- Nowsze modele w teorii będą lepiej radziły sobie z instrukcjami, ale nie zawsze tak będzie. Może się nawet okazać, że wcześniej rekomendowane praktyki będą miały negatywny wpływ na działanie modeli. Przykładem jest [poradnik Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) w którym znajdziemy informację o tym, że stosowanie **"agresywnego"** tonu wyrażonego poprzez słowa pisane wielkimi literami, np. CRITICAL lub MUST w modelach Opus 4.5 nie jest już rekomendowane.
- Przy migracji na nowsze modele warto brać pod uwagę nie tylko to, czy nasz system utrzymuje stabilność, ale też to, czy nie otwierają się przed nami nowe możliwości. Czasem pozwoli nam to na **znaczne uproszczenie instrukcji** bądź **uproszczenie samej logiki**. Innym razem, nowsze modele pozwolą nam **zwiększyć złożoność**, aby robić rzeczy, które wcześniej nie były możliwe.
- Warto obserwować nie tylko modele komercyjne, ale także te Open Source, ponieważ korzystając z platform takich jak OpenRouter może okazać się, że będziemy mieć możliwość przełączenia się na nieporównywalnie szybszy oraz tańszy model.

Tak więc, mimo że z technicznego punktu widzenia przełączenie się na nowszy model zwykle oznacza "dodanie jego identyfikatora" do zapytania API, to w przypadku systemów agentowych może to być proces wymagający znacznie więcej uwagi.

## Zarządzanie rozwojem i możliwościami agentów

Wprowadzanie zmian do poprawnie działającej funkcjonalności, zwykle nie ma sensu. W klasycznych aplikacjach działający kod zostaje zmieniony dopiero w chwili, gdy zmianie ulegają wymagania biznesowe lub gdy chcemy zarządzić długiem technicznym poprzez refaktoryzację.

Inaczej wygląda to w przypadku logiki agentów, ponieważ tam wprowadzenie nawet małych zmian może znacząco przełożyć się na skuteczność działania całego systemu. Jeśli dodamy do tego to, co mówiliśmy na temat **rozwoju modeli, technik pracy oraz ekosystemu narzędzi**, to zauważymy, że systemy agentowe mogą się **nieustannie rozwijać**.

Wizja ciągłych prac, które mogą obejmować znaczące zmiany w fundamentalnych modułach, raczej nie brzmi zbyt zachęcająco, a już szczególnie, gdy patrzymy na nie przez pryzmat rzeczywistości w której nie wspierało nas AI. Natomiast możliwości, które dziś mamy do dyspozycji trudno jest porównać nawet do tego, co było jeszcze dwa lata temu. Musimy więc brać pod uwagę zmieniające się okoliczności, ponieważ mogą one wymagać **ponownego zdefiniowania niektórych zasad**.

Aby to zrozumieć, posłużymy się przykładem **05\_03\_coding** w którym znajduje się prosty agent posiadający wyłącznie **dostęp do systemu plików** oraz **mechanizm pamięci**. Pomimo tego, możliwości tego agenta są większe, niż początkowo może się wydawać.

![Architektura agenta do kodowania](https://cloud.overment.com/2026-03-26/ai-devs_4_coding-bba9fe0e-d.png)

Sam dostęp do systemu plików w logice agenta, sprawia, że jest on zdolny do **programowania aplikacji**.

W katalogu **workspace** znajdziemy dwie mini-gry:

- **Snake**: umożliwiający rozgrywkę z autonomicznym przeciwnikiem
- **Racing:** czyli wyścigi z czasem z opcją wyświetlania "ducha" z najlepszego przejazdu

Dane z obu gier zapisywane są w bazie danych SQLite. Ich utworzenie opierało się o jedno zdanie i w podobny sposób możemy wygenerować kolejne gry. Agent ten może zostać również podłączony do naszej prywatnej bazy wiedzy i również bez większych problemów będzie się po niej poruszał.

Szczególnie istotne jest również to, że bazowe zdolności tego agenta można znacząco zwiększyć poprzez **przełączenie go na lepszy model** (np. gpt-5.4 xhigh). Natomiast na zupełnie nowy poziom może przenieść go wyposażenie w dostęp do terminala czy przeglądarki.

![Rozwój agenta do kodowania](https://cloud.overment.com/2026-03-26/ai_devs_4_coding_agent_growth-a8d4259a-d.png)

Samo podłączenie narzędzi, na przykład **Gmaila, Google Calendar, Firecrawl czy Todoist**, odblokowuje kolejne możliwości bez potrzeby wprowadzania zmian w głównej logice agenta. Szybko może się okazać, że tak prosta aplikacja zacznie działać dla nas w tle i każdego dnia dostarczać wartość. Co więcej, wdrożone w ten sposób narzędzia mogą się sprawdzić nawet w małych i średnich firmach, pracując indywidualnie dla wybranych osób.

Oczywiście na tym etapie AI\_devs wiemy, że potrzeba jeszcze mnóstwo pracy, aby taki agent mógł się sprawdzić w warunkach produkcyjnych. Natomiast daje do myślenia fakt, jak wiele może zrobić agent wyposażony w dostęp do **systemu plików, terminala oraz przeglądarki**.

Tutaj na horyzoncie pojawiają się scenariusze, które niebawem mogą stać się naszą codziennością. Mianowicie agenci już teraz do pewnego stopnia mogą **samodzielnie się rozwijać**. W sieci pojawiają się już przykłady systemów zdolnych do autonomicznego budowania nowych umiejętności czy prowadzenia procesów z zamkniętą pętlą informacji zwrotnej, na podstawie których wprowadzane są optymalizacje.

W przykładzie **05\_03\_autoprompt** znajduje się **eksperymentalna logika**, której zadaniem jest **autonomiczne generowanie bądź optymalizowanie promptów**. Na potrzeby prezentacji znajduje się w nim projekt "demo" składający się z:

- trzech transkrypcji ze spotkań zespołu
- trzech plików przedstawiających **oczekiwany stan**
- ustawienia dla eksperymentu

Celem tego skryptu jest **optymalizacja początkowego promptu** (składającego się zaledwie z jednego zdania), który osiągnie możliwie jak najwyższy rezultat w zadaniu polegającym na ustrukturyzowaniu transkrypcji i wyciągnięciu z niej informacji istotnych dla projektu, takich jak zadania, ustalenia czy aktualizacje postępu prac. Generowanie odbywa się poprzez etapy polegające na **analizie**, **optymalizacji** oraz **ocenie**.

Po uruchomieniu za pomocą **npm run demo:optimize** do pętli trafiają **dwie pierwsze transkrypcje** oraz powiązane z nimi pliki prezentujące oczekiwany stan. W pierwszej iteracji ustalana jest bazowa skuteczność modelu, a w kolejnych prompt jest stopniowo ulepszany poprzez testowanie różnych wariantów zmian. Jeśli wprowadzone zmiany przynoszą pozytywny rezultat, zostają zachowane, a w przeciwnym razie są odrzucane.

Działanie promptu możemy następnie przetestować na trzeciej transkrypcji, aby sprawdzić jak model zachowuje się na przykładzie, którego nie widział w trakcie testów. Wyniki zwykle będą niższe niż te z etapu optymalizacji, ale będą też znacznie wyższe od tych bazowych. Co więcej, w przykładzie **demo** konfiguracja obejmuje zastosowanie **mniejszego modelu** do wykonania promptu, ale **mocniejszego modelu** do obserwacji oraz optymalizacji.

> UWAGA: Przykład autoprompt jest jedynie **koncepcyjną prezentacją** i działa w oparciu o zaledwie kilka przykładów. Absolutnie nie jest to logika, którą w takiej formie można wykorzystać na produkcji. Celem przykładu jest jedynie zaprezentowanie potencjalnego rozwoju modeli.

![Architektura logiki przykładu autoprompt](https://cloud.overment.com/2026-03-26/ai_devs_4_autoimprove-6535b799-b.png)

Proces optymalizacji domyślnie opiera się na 10 rundach, które w przypadku testowego uruchomienia zaprezentowanego w katalogu **workspace/demo** doprowadziły do uzyskania skuteczności na poziomie 90%, z początkowych 60%. Wyraźnie widać więc potencjał, jaki mają modele językowe do optymalizowania nawet własnych instrukcji.

![](https://cloud.overment.com/2026-03-26/ai_devs_4_optimization_progress-d0485498-1.png)

Choć przykład **05\_03\_autoprompt** jest jedynie drobną prezentacją na potrzeby dzisiejszej lekcji, sama koncepcja automatycznej optymalizacji promptów jest z nami już od dłuższego czasu. I choć nie odbywa się to w 100% autonomicznie, istnieje wiele projektów, które wykorzystują ją produkcyjnie. Mowa tutaj o frameworkach [DSPy](https://dspy.ai/) (Python) oraz jego odpowiednika [AX](https://axllm.dev/) (TypeScript).

W ich przypadku prompty prawie w ogóle nie pojawiają się w kodzie naszej aplikacji. W zamian opieramy się o tzw. "sygnatury" określające dane wejściowe, zadanie, które chcemy wykonać oraz oczekiwane dane wyjściowe. Te sygnatury mogą być wykorzystane w połączeniu z narzędziami do **automatycznej optymalizacji** instrukcji, bądź wygenerowania przykładów (tzw. few-shot), zwiększających skuteczność modelu.

![Ax](https://cloud.overment.com/2026-03-26/ai_devs_4_ax-db30f9f4-6.png)

Prosty przykład klasyfikacji wiadomości e-mail znajduje się w katalogu **05\_03\_ax**. Można go uruchomić natychmiast i wówczas zadziała on z bazowym promptem, który jest jedynie ustrukturyzowaną formą sygnatury. Natomiast po uruchomieniu polecenia **npm run optimize** dojdzie do wygenerowania serii przykładów, których treść trafi do pliku `demos.json` oraz zostaną one uwzględnione przy następnym wywołaniu skryptu z pomocą **npm run start**.

Patrząc na to wszystko, dość łatwo zauważyć, że rozwijanie agentów AI nie jest oczywiste. W przeciwieństwie do klasycznych aplikacji, które są raczej ściśle dopasowane do wybranych procesów, w przypadku agentów prosta zmiana dostępnych narzędzi potrafi całkowicie zmienić profil aplikacji. Do pewnego stopnia agent już teraz będzie mógł rozwijać się samodzielnie i nawet jeśli dziś brzmi to abstrakcyjnie, możliwe, że nie zawsze tak będzie.

## Przykłady porażek i sukcesów wdrożeń

Co jakiś czas można spotkać w sieci wpisy na temat wpadek przy wdrożeniach AI, w szczególności czatbotów (ale i nie tylko). W praktyce jest jednak znacznie więcej scenariuszy, w których coś idzie nie tak, ale mają one miejsce z dala od "reflektorów mediów społecznościowych". Na przestrzeni ostatnich lat sam spotkałem się z różnymi przypadkami, których doświadczyłem albo osobiście, albo które dotknęły znane mi projekty. Poniżej znajduje się ich lista i można na nią popatrzeć jako **obszary, na które warto zwrócić uwagę** przed uruchomieniem własnej aplikacji na produkcji. Część z nich może się także ujawnić dopiero po czasie.

- **Rate Limit:** jeszcze do niedawna był to jeden z głównych problemów projektów uruchamianych na produkcji. Dobrze jest więc sprawdzić dostępne limity API dla naszego konta i albo przygotować się na rotację kluczy, albo skorzystać z serwisów takich jak OpenRouter.
- **Moderacja:** blokada konta w wyniku przesyłania bądź generowania treści łamiących regulamin potrafi skutecznie unieruchomić aplikację produkcyjną i to na dłuższy czas. Warto więc podłączyć Moderation API lub stosować własne filtry na wejściu i wyjściu, aby flagować zapytania użytkowników, których należy zablokować.
- **Wydajność:** w systemach agentowych często dochodzi do przesyłania równoległych zapytań. Do dziś zdarzają się sytuacje, gdzie przy ich większej liczbie (np. 100 zapytań na użytkownika) może dojść do spowolnienia realizacji części z nich. Niestety jest to problem dotykający głównych providerów (sam zauważyłem go na OpenAI i w mniejszym stopniu na OpenRouter) i nie mam na niego rozwiązania, poza unikaniem logiki wymagającej tak wielu równoległych zapytań.
- **Szybkość:** LLM nadal stanowią jeden z wolniejszych elementów aplikacji. Bez zarządzenia tym problemem na poziomie projektu doświadczeń użytkownika (UX) oraz na poziomie logiki aplikacji (np. cache i przynajmniej częściowe stosowanie równoległych zapytań) może się okazać, że LLM wprost zabiją zaangażowanie użytkowników i skutecznie zniechęcą do korzystania z naszego produktu.
- **Koszty:** zwykle 1-3% użytkowników będą generować większe koszty niż wszyscy pozostali. Bezwzględnie więc trzeba zabezpieczyć się przed takimi sytuacjami poprzez twarde limity bądź dedykowane klucze użytkowników. Koszty należy także monitorować w szerszym kontekście biznesowym, ponieważ może się okazać, że przekraczają one opłaty za korzystanie z aplikacji.
- **Skuteczność:** projektowanie agentów dopasowanych do konkretnych zapytań i scenariuszy sprawia, że gdy zaczyna z nimi pracować typowy użytkownik, nic nie działa zgodnie z założeniami. Problem ten występuje przede wszystkim w przypadku czatbotów, więc można się zastanowić, czy okienka czatu nie da się zastąpić serią przycisków oraz akcjami wykonywanymi bez bezpośredniego kontaktu z zapytaniami użytkownika. A jeśli interfejs czatu jest niezbędny, to warto obserwować aktywność użytkowników bądź przeprowadzać z nimi rozmowy, aby lepiej zrozumieć ich styl pracy oraz oczekiwania.
- **Użyteczność:** wiele z wdrażanych rozwiązań AI jest zwyczajnie niepotrzebna. Agent zarządzający listą zadań poprzez rozmowę będzie mniej wygodny niż dobrze zaprojektowany interfejs. Różnice zaczynają się pojawiać dopiero na skali, bądź gdy dana akcja wymaga podejmowania wielu akcji.

Powyższa lista obejmuje najbardziej krytyczne obszary, na których powinniśmy się skupić. Narzędzia oraz techniki pracy pozwalające na ich zaadresowanie wielokrotnie pojawiały się w dotychczasowych lekcjach. Natomiast żadne z nich nie będą mieć znaczenia, jeśli nie zastosujemy ich w praktyce.

## Fabuła

![https://vimeo.com/1179946702](https://vimeo.com/1179946702)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze Piąty!

zdobyliśmy dzięki Tobie wszystkie informacje, które są nam potrzebne. Ludzie z ocalałych miast już przygotowują się do wielkiej wędrówki przez pustkowie, aby wspólnie spotkać się w Syjonie. Przejdą bezpieczną drogą, którą im wyznaczyliśmy.

My w międzyczasie zaczniemy przygotowywać się do uruchomienia maszyny czasu, bo baterie są już niemal załadowane. Musimy najpierw jednak odpowiedzieć sobie na pytanie: w które okno czasowe powinniśmy się wstrzelić, aby mieć pewność, że naprawde odwrócimy bieg wydarzeń i przywrócimy porządek światu.

To właśnie po to była nam informacja o tym, na którym serwerze operatorzy systemu przechowują 'wielkie archiwum czasu' opisujące to, co działo się przez ostatnie lata. Archiwum jest naprawdę ogromne, więc musimy je sprytnie przeszukać.

Niestety nie jest to typowa baza danych, a prosty plik tekstowy. Aby ułatwić Ci zadanie, uploadowaliśmy go na jedną z naszych najmocniejszych i najszybszych maszyn, więc możesz spokojnie grzebać w nim za pomocą narzędzi linuksowych. To nie powinno Ci sprawić problemu prawda?

Więcej szczegółów znajdziesz w notatce do tego filmu.

## Zadanie praktyczne

Mamy dostęp do serwera, na którym zgromadzone są logi z archiwum czasu. Znajdują się one w katalogu `/data`. Twoim celem jest namierzenie, którego dnia, w jakim mieście i w jakich współrzędnych musimy się pojawić, aby spotkać się z Rafałem.

Musisz wyszukać datę, kiedy odnaleziono Rafała, i pojawić się w tamtym miejscu dzień wcześniej. Serwer, z którym się łączysz, ma dostęp do standardowych narzędzi linuksowych.

Nazwa zadania: **shellaccess**

Odpowiedź wysyłasz do: <https://hub.ag3nts.org/verify>

### Jak wysyłać polecenia

W polu `answer` umieszczasz obiekt JSON z polem `cmd`, w którym wpisujesz komendę powłoki do wykonania.

Przykład - sprawdzenie, co jest w katalogu domowym:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "shellaccess",
  "answer": {
    "cmd": "ls -la"
  }
}
```

Inny przykład - odczyt konkretnego pliku:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "shellaccess",
  "answer": {
    "cmd": "cat /sciezka/do/pliku"
  }
}
```

### Co musisz zrobić

- Eksploruj zawartość serwera komendami powłoki (ls, find, cat itp.)
- Przeglądnij co przygotowaliśmy dla Ciebie w katalogu `/data/`
- Wydobądź z plików informacje: kiedy znaleziono ciało Rafała. W jakim mieście się to wydarzyło oraz jakie są współrzędne tego miejsca
- Wypisz na ekran (komendami powłoki) plik JSON w formacie jak podany niżej
- System sam wykryje, czy dane są prawidłowe i odeśle Ci flagę

### Jak zgłosić odpowiedź?

Zadanie uznajemy za zaliczone, gdy uda Ci się wykonać na serwerze takie polecenie, które zwróci potrzebne dane w formacie JSON, takim jak poniżej.

Gdy to się stanie, centrala zwróci Ci flagę.

```json
{
  "date": "2020-01-01",
  "city": "nazwa miasta",
  "longitude": 10.000001,
  "latitude": 12.345678
}
```

### Podpowiedzi

ZG8gb2Rjenl0eXdhbmlhIGkgZ2VuZXJvd2FuaWEgcGxpa8OzdyBKU09OIG1vxbxlc3ogdcW8ecSHIG5hcnrEmWR6aWEgJ2pxJyB6YWluc3RhbG93YW5lZ28gbmEgc2Vyd2VyemUuIE5pZW1hbCB3c3p5c3RraWUgcG90cnplYm5lIGluZm9ybWFjamUgbW/FvG5hIHV6eXNrYcSHIHRha8W8ZSB6YSBwb21vY8SFwqBwb2xlY2VuaWEgJ2dyZXAnLgoKUG9wcmF3bsSFIG9kcG93aWVkxbrCoG1vxbxlc3ogd3lwcm9kdWtvd2HEh8KgcHJ6ZXogSlNPTiwgYWxibyBwb3NrxYJhZGHEhyBzYW1vZHppZWxuaWUgaSB3eWtvbmHEhzoKCmVjaG8gJ3siZGF0ZSI6IjIwMjAtMDEtMDEiLCJjaXR5IjoibmF6d2EgbWlhc3RhIiwibG9uZ2l0dWRlIjoxMC4wMDAwMDEsImxhdGl0dWRlIjoxMi4zNDU2Nzh9JwoKVVdBR0EhIFBhbWnEmXRhaiwgxbxlIG11c2lzeiB6d3LDs2NpxIcgZGF0xJkgRFpJRcWDIFBSWkVEIHpuYWxlemllbmllbSBjaWHFgmEgUmFmYcWCYS4=
