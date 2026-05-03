---
title: S05E04 — Produkcja
space_id: 2476415
status: scheduled
published_at: '2026-04-09T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/fight-1775229832.png'
circle_post_id: 31353112
---
## Film do lekcji

![https://vimeo.com/1179914574](https://vimeo.com/1179914574)

Budowanie narzędzi AI na własne potrzeby zwykle jest proste. Dziś nawet kilkanaście minut wystarczy, aby stworzyć proste rozwiązanie, które od razu może przynieść nam realną wartość. Możemy przy tym skorzystać z technologii, którymi nie posługujemy się na co dzień (np. Swift), a największym wyzwaniem jest przede wszystkim sam pomysł. Takie rozwiązanie będzie dobrze dopasowane do nas, ale trudno będzie je udostępnić nawet znajomemu, nie wspominając już o wdrożeniu na skalę produkcyjną.

Dotychczasowe lekcje pokazały nam jak projektować narzędzia i logikę agentów, dbać o bezpieczeństwo, wydajność i drobne detale, które odgrywają krytyczną rolę na produkcji. Pomimo tego, nawet już przy pierwszych wdrożeniach funkcjonalności AI możemy doświadczyć przepaści, która dzieli środowisko developerskie czy nawet etap MVP (Minimum Viable Product) od środowiska produkcyjnego.

Co prawda doświadczenie programistyczne sugeruje nam, że nie jest to nic nowego, ponieważ wyzwania na produkcji pojawiają się od zawsze i nie wszystko da się przewidzieć na etapie planowania. Natomiast w przypadku aplikacji generatywnych problem ten jest jeszcze bardziej widoczny.

## Doświadczenia z produkcji

W lekcji **S05E02** pojawił się przykład **05\_02\_ui**. Umożliwiał on wyświetlanie interakcji z agentem, uwzględniając strumieniowanie, renderowanie markdown i wsparcie dynamicznych bloków. Wymieniłem tam też kilkanaście punktów wskazujących na funkcjonalności, których nam brakowało. Choć były to zaledwie pojedyncze zdania, tak każda z nich wymaga wielu dni pracy i to nawet przy wsparciu AI.

Kilkukrotnie mówiłem, że generatywne aplikacje muszą być bardziej dopracowane niż te klasyczne, a my musimy stać się jeszcze lepsi w swojej pracy. Produkcyjne doświadczenie pokazuje jednak, że nie chodzi tu wyłącznie o dobre decyzje dotyczące architektury, ale nawet drobne rzeczy, na które normalnie nie zwrócilibyśmy uwagi.

Przykładowo, wiele interfejsów czatu pozwala na **usuwanie wiadomości**. Jednak z jakiegoś powodu, nie znajdziemy jej w ChatGPT, Claude, Claude Code czy Cursor. Natomiast znacznie częściej możemy spotkać opcję **rozgałęzienia** konwersacji lub ewentualnie **przywrócenia jej** do wskazanego punktu.

Powodem jest fakt, że usuwanie wiadomości ze środka konwersacji zaburza historię i mogą mieć negatywny wpływ na zachowanie modelu, mechanizm zarządzania kontekstem, a nawet uniemożliwić prowadzenie dalszej konwersacji. API Anthropic i Gemini wymagają, aby wiadomość użytkownika była **ostatnia** i w przeciwnym razie zwrócą błąd.

![Problemy związane z manipulacją konwersacji](https://cloud.overment.com/2026-03-28/ai_devs_4_message_deletion-07da31bb-7.png)

Dopuszczalne jest jednak **edytowanie treści wiadomości**, ale i tutaj pojawiają się wyzwania. Agent posługuje się narzędziami, więc edycja treści jego wiadomości nie powinna być możliwa. Natomiast nawet bez tego edytowanie wypowiedzi modelu może otworzyć ścieżkę do **[many-shot jailbreaking](https://cloud.overment.com/2026-03-28/ai_devs_4_message_deletion-07da31bb-7.png)**, ponieważ użytkownik mógłby zasugerować agentowi, że zrobił już coś, czego zrobić nie powinien, a model mógłby uznać takie zachowanie za właściwe.

![Przykład many-shot jailbreaking](https://cloud.overment.com/2026-03-28/ai_devs_4_jailbreak-03e3c821-5.png)

Interesujące sytuacje zdarzają się także przy przetwarzaniu audio, na przykład **dyktowania**. W związku z tym, że niektóre modele, np. whisper, są prawdopodobnie trenowane na napisach filmów, to pojawiają się w nich halucynacje, takie jak zinterpretowanie ciszy jako **Thanks for watching!** lub **Thank you so much for joining us** albo nawet **Subtitles by the Amara.org community**. Albo nawet w przypadku modeli, które posiadają wsparcie dla wielu języków, pojawiają się problemy, gdy dochodzi do ich **mieszania**, na przykład w określeniach: "Turn left and walk straight down **Piotrkowska** Street".

![Problemy z przetwarzaniem audio](https://cloud.overment.com/2026-03-28/ai_devs_4_mixing-61e288c2-e.png)

Nietypowe problemy zdarzają się również przy obsłudze narzędzi. Wystarczy, że w instrukcji systemowej pojawi się jakakolwiek wzmianka o możliwościach, które w rzeczywistości nie są dostępne dla agenta. Na przykład jeśli powiemy, że agent może przeszukiwać Internet, ale narzędzie **nie będzie aktywowane**, to model i tak **może** zachować się tak, jak gdyby było inaczej.

Są też sytuacje, które można spotkać również w klasycznych aplikacjach, ale przy projektowaniu agentów zdarzają się one częściej. Na przykład pole tekstowe po wklejeniu większej ilości tekstu staje się niemal niemożliwe do edycji z powodu spadku wydajności. Problem w tym, że podczas rozmowy z LLM bardzo często wklejamy duże ilości treści. Konieczne jest więc wykrywanie zbyt dużej ilości treści i obsługiwanie jej tak, jak gdyby został dołączony plik tekstowy.

![Przykład rozwiązania problemu długich treści w prompcie](https://cloud.overment.com/2026-03-30/ai_devs_4_long_content_fix-b24ee1be-c.png)

Patrząc na powyższe przykłady, można powiedzieć, że to detale, które nie mają większego znaczenia. Jednak to właśnie one wpływają zarówno na doświadczenia użytkowników, jak i na skuteczność działania agentów. Co więcej, obecnie modele językowe niemal zawsze będą je pomijać, więc to **my będziemy musieli zwrócić na nie uwagę**. Dziś kod źródłowy można generować na dużą skalę, ale różnicę robi zarówno to, co zostanie wygenerowane, jak i to, **co zostanie pominięte**.

Umiejętność rozpoznawania takich detali bierze się niemal tylko i wyłącznie z doświadczenia. Podczas budowania, będziemy spotykać problemy i szukać na nie odpowiedzi. Nie chodzi tu jednak o wpisanie promptu i wciśnięcie "enter", lecz świadomą pracę z dostępnymi narzędziami w celu kształtowania produktów z których sami chcemy korzystać. W praktyce, to właśnie te detale robią różnicę, a występują one wszędzie - w interfejsie, na back-endzie czy w ogóle u podstaw architektury.

Co więcej, szczegóły o których mowa, wpływają nie tylko na doświadczenia użytkowników, ale także na ich **bezpieczeństwo**. Jak już wielokrotnie mogliśmy się przekonać, agenci AI popełniają błędy, ale też odblokowują zupełnie nowe metody ataków. Możliwość podłączania serwerów MCP, narzędzi CLI, albo nawet pozornie niewinna integracja, którą stworzyliśmy sami, może skończyć się dużymi problemami dla użytkownika końcowego, a w konsekwencji również dla nas. Widzieliśmy już wiele przykładów źle wdrożonych czatbotów, ale jeszcze więcej jest przykładów wdrożeń, gdzie nikt jeszcze nie zorientował się, że coś jest nie tak.

Jednak poza błędami, niedopatrzeniami czy problemami z bezpieczeństwem, istnieją także ogromne oczekiwania ze strony przełożonych, klientów, a nawet nas samych. Nie ma wątpliwości, że to, co możemy dziś osiągać dzięki odpowiedniemu korzystaniu z generatywnego AI, jest naprawdę imponujące.

Niezależnie od tego, jak wygląda nasza praca na co dzień, czy już teraz możemy stosować AI na produkcji, rozwijać systemy od zera, bądź wprost przeciwnie, dopiero będziemy stawiać pierwsze kroki, warto zbudować rozwiązanie, które będzie działało dla nas. Gdy AI stanie się częścią naszej codzienności, nawet w niewielkim wymiarze, i będzie opierało się na narzędziach, które **stworzymy** bądź będziemy **rozwijać** samodzielnie, to właśnie na tym zbudujemy największe doświadczenie. Nie mówię tutaj jednak wyłącznie o prostych integracjach, ale wprost całych systemach, które zintegrują się z naszą codziennością (np. w obszarze pracy).

Dlatego w tej lekcji przygotowałem dwa **bardzo rozbudowane przykłady**, które w praktyce się ze sobą łączą, ponieważ jeden z nich - **05\_04\_ui** to warstwa front-endowa, a **05\_04\_api** to back-end tej samej aplikacji. Ich logika wykorzystuje niemal wszystko, czego dowiedzieliśmy się do tej pory:

- Zaawansowane integracje z providerami API
- Strumieniowanie i renderowanie treści
- Zaawansowany interfejs czatu do pracy z agentami
- Wsparcie treści multimodalnych
- Zarządzanie wątkami oraz uprawnieniami
- Filtrowanie zapytań przez Moderation API
- Zarządzanie kontekstem oraz prompt cache
- Kompresję kontekstu przez obserwacje i refleksje
- Wsparcie dla załączników i dokumentów
- Integracja z systemem plików
- Natywne narzędzia oraz MCP (+ MCP Apps)
- Uruchamianie kodu (sandbox)
- Human in the loop
- Observability
- Logikę agentów (heartbeat + graf) i współpracy między nimi
- Aktywną pracę z agentami
- Przetwarzanie zadań w tle
- ...i wiele innych

> Ważne: powyższe przykłady należy uruchomić w dwóch oknach terminala poleceniami **npm run lesson24:ui** oraz npm run **lesson24:api**. Aplikacja będzie dostępna pod adresem http://localhost:5173

Architektura tej aplikacji została opracowana z myślą o wdrożeniu produkcyjnym, a nie wyłącznie prywatnym zastosowaniu. Co prawda nie jest ona ostateczna i za chwilę omówimy elementy, które jeszcze powinny się w niej znaleźć, natomiast już teraz znajdziemy tam:

- **UI:** to rozbudowana wersja przykładu **05\_02\_ui**. To minimalistyczny, lecz mocno zoptymalizowany interfejs pod kątem wydajności oraz solidnego strumieniowania składni markdown z uwzględnieniem bloków prezentujących akcje agentów oraz palety akcji do obsługi ustawień oraz trybów. Posiada także wsparcie dla skrótów klawiszowych oraz zaawansowanej konfiguracji każdego agenta.
- **Auth:** obejmuje formularz logowania poprzez dane **wygenerowane** na etapie seed'owania bazy danych bądź ręcznego dodania użytkownika. Na produkcji prawdopodobnie skorzystalibyśmy z rozwiązań takich jak na przykład **[better-auth](https://better-auth.com/)**. Konta podzielone są także na **grupy** z możliwością **współdzielenia zasobów** (np. profili agentów) bądź nawet przełączania się pomiędzy nimi.
- **Stan aplikacji:** tutaj mamy zarządzanie stanem oparte o runy frameworka Svelte. Mamy więc tu zarządzanie wątkiem, sesją, aktywnymi ustawieniami oraz głównymi elementami interfejsu.
- **System zdarzeń:** z jego pomocą odzwierciedlamy zdarzenia emitowane przez back-end. To na nich opiera się prezentacja aktywności agentów, komunikacji pomiędzy nimi, a także z użytkownikiem (np. w przypadku zgody na wykonanie akcji). Dodatkowo uwzględniamy tutaj również **wznawianie interakcji** w przypadku zamknięcia przeglądarki bądź po prostu wczytania istniejącego wątku.
- **API (frontend):** czyli już bezpośrednie połączenie z back-endem, odbywa się o zapytania HTTP (aczkolwiek tutaj jest też przestrzeń na WSS).
- **API (backend)**: mamy tu zarządzanie sesją, limity, zarządzanie uprawnieniami oraz spójne formaty wymiany danych (w tym błędów) oraz strumieniowania odpowiedzi.
- **Agent:** jest to rozbudowana wersja przykładu **05\_01\_agent\_graph** z **02\_05\_agent** i **01\_05\_agent**, czyli logika oparta o dynamiczne zarządzanie zależnościami przez LLM oraz logikę kodu. Więcej na jej temat powiemy sobie za chwilę
- **Event Dispatcher**: zarządza emisją zdarzeń dotyczących zarówno interakcji z agentami, jak i akcjami dodatkowymi (np. generowaniem nazwy dla wątku czy kompresji kontekstu).
- **LLM Provider**: zarządza połączeniem z LLM, ustawieniami oraz monitorowaniem zużycia kontekstu.
- **MCP / Tools**: czyli warstwa zarządzająca połączeniami z MCP oraz przygotowaniem natywnych narzędzi oraz narzędzi providera (np. Web Search).

Całość przedstawia poniższy schemat:

![Przegląd architektury UI + API](https://cloud.overment.com/2026-03-31/ai_devs_4_ui_api_arch-89bf1510-b.png)

Większość elementów tej architektury możemy spotkać w klasycznych aplikacjach. Dlatego teraz przyjrzymy się tym, które bezpośrednio dotyczą logiki agentów. Choć opiera się ona na koncepcjach, które już znamy, jej obecna konfiguracja jest nieco bardziej zaawansowana.

Przede wszystkim, struktura danych obejmuje następujący podział:

- **Tenant:** pozwala na grupowanie kont użytkowników, przestrzeni roboczych, agentów, plików i konfiguracji serwerów MCP. Otwiera także przestrzeń do zarządzania dostępami dla planów abonamentowych czy różnych poziomów uprawnień.
- **Account:** to konto indywidualnego użytkownika, dające przestrzeń na personalizowanie ustawień oraz zarządzanie indywidualnymi uprawnieniami. Do konta przypisane są także indywidualne klucze API (ale fizycznie znajdują się w oddzielnej tabeli).
- **Workspace:** to przede wszystkim przestrzeń na zasoby (np. system plików), organizację ustawień (np. agentów) oraz interakcji.
- **Sessions (auth):** przechowuje informacje na temat sesji logowania
- **Sessions (work):** to struktura grupująca wątki (np. w przypadku ich rozgałęzienia) pozwalająca na współdzielenie zasobów między nimi.
- **Threads:** jest to bieżąca interakcja z agentem. W kontekście czatu, jest to po prostu konwersacja. Można też na nią patrzeć przez pryzmat rozgałęzień, ponieważ każdy wątek może mieć wątek nadrzędny.
- **Messages:** to pojedyncze wiadomości pomiędzy użytkownikiem, a agentem
- **Jobs**: to przestrzeń na zadania agentów, status ich realizacji, dane wejściowe oraz wynik. Można o tym myśleć jak o Issue w Linear czy Jira.
- **Runs:** reprezentują aktywności agenta i posiadają swój stan (np. pending/running/waiting/completed itd), a także snapshot konfiguracji modelu oraz wszystkie informacje na temat błędów oraz rezultatów.
- **Items:** to elementy składające się na aktywność, takie jak reasoning modelu czy wywołania oraz rezultaty działania narzędzi
- **Dependencies:** to dane mechanizmu oczekiwania oraz blokad aktywności agentów, obejmujących innych agentów, wykonania narzędzi czy odpowiedź ze strony człowieka.
- **Executions:** to historia wywołań pojedynczych narzędzi w ramach aktywności agentów. Przechowują argumenty, wyniki, błędy oraz metadane dotyczące danego wykonania.
- **MCP Servers:** przechowuje informacje o konfiguracji serwerów MCP oraz ich przynależności.
- **Uploads:** zawiera zdarzenia dotyczące wgrywanych plików oraz prób ich wgrania.
- **Files:** zawiera informacje na temat plików wgranych przez użytkownika, ale także artefaktach generowanych przez agentów

Ważne jest teraz, abyśmy uchwycili szerszy obraz aplikacji i poniżej mamy schemat, który go oddaje. Schemat pokazuje struktury danych dla **konwersacji** oraz **głównej logiki**. Ich główne założenia opierają się o te same zasady, które widzieliśmy już w dotychczasowych lekcjach, ale w nieco bardziej produkcyjnym wydaniu, ponieważ:

- istnieje przestrzeń na współdzielenie zasobów między konwersacjami, a także rozgałęzianie wątków czy nawet udostępnianie pomiędzy użytkownikami.
- mamy bardzo dużą kontrolę nad tym, co dzieje się na poszczególnych etapach działania agentów, co może być odzwierciedlone w interfejsie użytkownika
- wspomniana kontrola daje też duże możliwości w zakresie pracy asynchronicznej, obejmującej oczekiwanie na spełnienie wielu zależności oraz wznawianie pracy
- interakcje nie muszą odbywać się wyłącznie między użytkownikiem, a agentem, ponieważ zlecenia mogą być tworzone przez innych agentów bądź zewnętrzne zdarzenia

![Główna architektura systemu wieloagentowego](https://cloud.overment.com/2026-04-01/ai_devs_4_backbone-c46c10e0-f.png)

Podobnie wygląda to w przypadku **organizacji** (tenantów), **użytkowników** (accounts) oraz danych dotyczących sesji i kluczy. Poniższa struktura daje nam duży wgląd w aktywność pod kątem sesji oraz zarządzanie dostępami, a także kwestiami bezpieczeństwa.

Większe możliwości organizacji dotyczą także agentów. W ich przypadku mamy między innymi "rewizje" posiadające informacje o ustawieniach w chwili zapytania, co bywa pomocne przy analizie aktywności użytkowników w kontekście rozwiązywania problemów.

![Struktura danych dla kont i agentów](https://cloud.overment.com/2026-04-01/ai_devs_4_identity-1ac2f904-6.png)

Ostatecznie mamy też główną logikę systemu. Naturalnie architektura ta, nie jest definitywnym rozwiązaniem, bo jak już wiemy, możemy podejść do tego tematu na wiele sposobów. Jednocześnie stanowi ona całkiem dobry punkt odniesienia oraz rysuje nam różne procesy na które możemy zwrócić uwagę przy projektowaniu własnych systemów bądź wyborze frameworków.

W przypadku tego systemu, interakcja z użytkownikiem wygląda niepozornie. Z jego perspektywy, agent po prostu odpisuje na wiadomości i w razie potrzeby wzywa pozostałych agentów. Jednak w tle dzieje się zdecydowanie więcej, ponieważ wiadomość traktowana jest jak **zadanie do wykonania**, które można wykonać, wznowić, bądź zatrzymać, ale także przekazać do narzędzi bądź innych agentów.

Poniżej mamy wizualizację głównej logiki, natomiast jej szczegóły omawiam w krokach opisanych w dalszej części.

![Agent Runtime](https://cloud.overment.com/2026-04-01/ai_devs_4_main_runtime-3add9c70-3.png)

Poszczególne kroki obejmują:

- **Żądanie:** zapytanie HTTP zawierające wiadomość do systemu wraz z ustawieniami (np. identyfikatorem agenta). Na tym etapie dochodzi także do uwierzytelnienia zapytania oraz walidacji danych.
- **Inicjalizacja:** utworzenie bądź powiązanie wpisów w bazie danych: sesji, wątku, wiadomości, zlecenia (job) oraz próby wykonania (run). Tutaj ma miejsce **wyłącznie** zapis danych, ale nie są podejmowane żadne dodatkowe akcje.
- **Kolejka:** zlecenie (job) otrzymuje tutaj status **queued**, a próba wykonania (run) status **pending**. Tutaj nadal jeszcze nie są podejmowane żadne akcje, ale takie przygotowanie zadań pozwala na ich późniejsze wznowienie w razie wystąpienia błędu.
- **Scheduler:** jest to pętla, która cyklicznie zadaje pytanie do bazy danych o to, czy istnieją pary job/run wymagające działania. Gdy znajdzie oczekujące zadanie, przekazuje je do wykonania. Kolejność jest stała: najpierw dostarczanie wyników od agentów podrzędnych, potem wznowienia, odzyskiwanie po awariach, a na końcu nowe zadania.
- **Rezerwacja (Claim)**: zanim rozpocznie się wykonanie, worker rezerwuje run wpisem do bazy z czasem wygaśnięcia. Od tego momentu uruchamiany jest heartbeat — cykliczne odświeżanie rezerwacji potwierdzające, że proces nadal działa. Jeśli proces upadnie, heartbeat przestaje bić, rezerwacja wygasa, a scheduler automatycznie ponowi próbę.
- **Pętla Agenta**: czyli klasyczna pętla, którą znamy z wcześniejszych przykładów. Gdy model nie wskaże żadnych narzędzi do wykonania, odpowiedź zostaje zapisana, a próba wykonania (run) zakończona. W przeciwnym razie dochodzi do wykonania narzędzi i kolejnej iteracji z nowymi danymi.
- **Delegacja:** gdy model wywołuje `delegate_to_agent`, system tworzy prywatny child run z własnym agentem, narzędziami i kontekstem. Parent run przechodzi w stan waiting i opuszcza pętlę. Delegacja może być zagnieżdżona wielopoziomowo, tworząc łańcuch zależności rozwijający się jak stos wywołań.
- **Dostarczenie wyniku (Delivery):** gdy child run się zakończy, scheduler wykrywa to i dostarcza wynik z powrotem do wątku nadrzędnego jako odpowiedź narzędzia. Zależność zostaje rozwiązana, parent wraca do kolejki i wznawia swoją pętlę z miejsca, w którym ją przerwał.
- **Zapis (Persistence):** obejmuje zapisywanie **wiadomości wątku** oraz **items**, czyli poszczególne akcje, takie jak reasoning, wywołania narzędzi, ich wyniki czy delegowanie.
- **Odzyskiwanie (Recovery):** scheduler w każdym cyklu sprawdza, czy nie ma "martwych" prób wykonania (run). Wykryty problem skutkuje przywróceniem próby wykonania do stanu pending i ponownym umieszczeniu zlecenia w kolejce.

Mamy więc tu do czynienia z logiką, która obudowuje pętle agenta w taki sposób, aby zarządzać realizacją zadań poprzez kontrolowanie ich statusów oraz odpowiedzialności. Całość uwzględnia także mechanizmy automatycznego naprawiania potencjalnych błędów oraz wznawiania wywołań w chwili, gdy po drodze coś pójdzie nie tak.

Kod źródłowy przykładów **05\_04\_ui** oraz **05\_04\_api** jest bardzo rozbudowany, więc zdecydowanie polecam zapoznać się z nim **wspólnie z agentem do kodowania**. Zaznaczę tutaj tylko, że na część frontendową poświęciłem odpowiednio mniej czasu i pełni ona głównie rolę prezentacji możliwości back-endu. Jednocześnie już sam interfejs zawiera różne elementy, na które warto zwrócić uwagę na produkcji. Są to między innymi:

- Definiowanie agentów, ich domyślnych ustawień, instrukcji oraz narzędzi.
- Udostępnianie agentów oraz narzędzi w ramach organizacji (tenant)
- Możliwość podłączania własnych serwerów MCP. **UWAGA:** tutaj celowo dodałem opcję dodawania serwerów STDIO, natomiast coś takiego na produkcji jest dopuszczalne **tylko i wyłącznie wtedy**, gdy mówimy o aplikacji desktopowej, gdzie proces uruchamiany jest **na urządzeniu użytkownika**.
- Tworzenie profili narzędzi udostępnianych pomiędzy agentami oraz opcję duplikowania agentów.
- Wyświetlanie aktywności agentów oraz subagentów, a także obsługa logiki związanej z **akceptowaniem wywołań narzędzi**.
- Informacje na temat bieżącego zużycia kontekstu oraz detale związane z obserwacją oraz refleksją (czyli mechanizmami kompresji kontekstu) obejmujące możliwość ich **edycji**
- Możliwość odnoszenia się do plików przechowywanych w workspace poprzez paletę wywoływaną z pomocą "#"
- Opcję wykonywania więcej niż jednego wątku jednocześnie

Zatem front-end może posłużyć przede wszystkim do doświadczenia kształtu całej interakcji. Back-end natomiast wymaga przestudiowania wspólnie z AI. Oczywiście nie jest to wymagane, ale myślę, że można znaleźć tam wskazówki, które da się wykorzystać w swoich projektach. Dodatkowo w przypadku uzupełnienia zmiennych środowiskowych w pliku `.env` dla platformy Langfuse, możliwe jest podejrzenie interakcji i przeanalizowanie jej również z tej perspektywy.

## Generalne sugestie

Generatywne aplikacje na produkcji to bardzo szeroki temat i mimo że we wszystkich dotychczasowych lekcjach omówiliśmy mnóstwo zagadnień, które realnie pomogą nam w budowaniu aplikacji produkcyjnych, bez wątpienia nie powiedzieliśmy jeszcze wszystkiego.

Pomimo tego, że większość omawianych przykładów skupiała się na **prezentowaniu koncepcji** i często chodziliśmy na skróty, aby niepotrzebnie nie zwiększać złożoności kodu, wciąż można z nich wyciągnąć mnóstwo wniosków, które sprawdzą się na produkcji. Mam tu na myśli zarówno budowanie narzędzi i agentów, zarządzanie kontekstem, podłączanie zaawansowanego monitoringu czy ewaluacji, jak i przede wszystkim dbanie o aspekty związane z bezpieczeństwem, przy świadomości braku skutecznych technik obrony przed prompt injection.

Jest jednak kilka rzeczy, które sam chciałbym usłyszeć miesiące temu, które pomogłyby mi w budowaniu lepszych aplikacji. Są to między innymi:

- **Mamy nowe możliwości, ale zasady są takie same:** pomimo tego, że dziś 100% kodu możemy generować z pomocą AI (pod nadzorem), co pozwala na znacznie szybsze poruszanie się, tak pytania takie jak "co w danej chwili ma znaczenie?" albo "jaki problem rozwiązujemy?" albo "czy można to zrobić lepiej?" albo "co nam umyka" pozostają tak samo trudne lub nawet trudniejsze. Pomimo tego, że dziś możemy wygenerować rozbudowane aplikacje z pomocą zaledwie kilku promptów nie rozwiązuje wszystkich naszych problemów. Dodatkowo środowisko produkcyjne nadal stawia przed nami tak wiele wyzwań, że aż trudno określić na czym powinniśmy się skupić.
- **Wszyscy eksplorujemy:** im bardziej rosną możliwości oraz popularność modeli językowych, tym więcej nowych pytań się pojawia. Spotykamy zupełnie nowe techniki pracy, nowe pomysły oraz zupełnie nowe wyzwania. Co więcej, wszystkie nasze przekonania oraz opinie na temat AI należy bardzo często aktualizować bądź po prostu wprost zakładać, że **mogą być niepoprawne** w chwili, gdy zaczynają się kształtować. Pozwala to na utrzymanie otwartości oraz zwiększenia szansy na sięgnięcie po nowe możliwości, które dopiero się pojawiają.
- **Zrozumienie zasad tylko po to, aby je łamać:** w związku z powyższymi, gdy już poznamy zasady pracy z modelami, techniki pracy, wzorce czy narzędzia, warto wprost je kwestionować i szukać własnych ścieżek. Obecnie możemy bardzo szybko eksperymentować i iterować kolejne pomysły. Koszt sprawdzenia zupełnie nowej technologii czy strategii, a niekiedy nawet zbudowania całego produktu od podstaw, jest zupełnie inny, niż był jeszcze kilkanaście miesięcy temu.
- **Przedefiniowanie naszej roli:** na tym etapie nie potrafię odpowiedzieć, jakie umiejętności dalej mają znaczenie w naszej pracy. Mówi się, że stanowiska juniorskie nie mają przyszłości. Jednak to właśnie świeże podejście juniorów połączone z możliwością bardzo szybkiego zdobywania wiedzy wydaje się mieć więcej przewag niż osoba z doświadczeniem, która jest zamknięta na AI oraz zmianę swoich dotychczasowych nawyków. Patrząc na to, można powiedzieć, że bardziej niż kiedykolwiek liczy się umiejętność odnalezienia się w bardzo szybko zmieniającym otoczeniu.
- **Poziom zrozumienia AI:** to jedno z największych wyzwań, z którymi będziemy mierzyć się w przypadku aplikacji działających na produkcji. Zbudowanie rozwiązań wykorzystujących AI jest stosunkowo proste. Jednak stworzenie ich w taki sposób, by były łatwe w obsłudze oraz dostarczały wartość osobie, która nie wie praktycznie nic na temat AI, jest ogromnym wyzwaniem. Dlatego zawsze musimy zakładać, że użytkownicy naszych aplikacji posiadają minimalną bądź zerową wiedzę na temat działania modeli.
- **Rola jakości i dbania o szczegóły:** obecna narracja dotycząca AI kładzie ogromny nacisk na zwiększanie wydajności pracy. Natomiast w świecie w którym niemal każdy może wygenerować relatywnie złożone narzędzia dopasowane do jego potrzeb, ogromnym wyróżnikiem staje się jakość. Wymaga ona zdecydowanie więcej pracy i nierzadko także doświadczenia i wiedzy z danego obszaru. Wiele więc wskazuje na to, że warto korzystać z AI nie tylko po to, aby pracować szybciej, ale przede wszystkim po to, aby **podnosić jakość swojej pracy**.
- **Agent bez czatu:** spojrzenie na systemy agentowe poza interfejsem czatu pozwala przestawić myślenie na zupełnie nowe zastosowania. Co więcej, w kontekście produkcyjnym znacznie łatwiej jest zbudować logikę, która korzysta z modeli **bez okna czatu**. Wystarczy obserwowanie zachowań użytkownika czy reagowanie na podejmowane przez niego akcje oraz uzupełniane zasoby (np. wciśnięcie przycisku czy wgranie pliku). Wówczas mamy znacznie większą kontrolę nad przetwarzanymi danymi oraz scenariuszami, które potrzebujemy obsłużyć.
- **Budowanie "dla agentów":** do tej pory tworzyliśmy aplikacje z myślą o użytkownikach. Obecnie coraz częściej powinniśmy robić to z myślą o agentach, którzy będą działać w imieniu użytkowników. To potężna zmiana, która obecnie zaczyna mieć miejsce i wiele wskazuje na to, że będzie wpływać na naszą przyszłość.

Co prawda nie potrafię przewidzieć przyszłości i, patrząc na to, jak rozwijały się narracje dotyczące AI na przestrzeni ostatnich lat, można powiedzieć, że nikt tego nie potrafi. Nie zawsze jednak trzeba ją znać, ponieważ wystarczy po prostu rozejrzeć się wokół i zobaczyć to, co mamy do dyspozycji już teraz. Bardzo pomaga w tym również pozytywne nastawienie wobec tego, co potencjalnie może nadejść. Założenie, że modele będą się dalej rozwijać, do tej pory było poprawne. I choć nie wiemy, czy tak nadal będzie, to nawet gdyby ich możliwości dziś zatrzymały się w miejscu, nadal możemy znaleźć dla nich mnóstwo zastosowań.

## Fabuła

![https://vimeo.com/1179946236](https://vimeo.com/1179946236)

## Zadanie

Wyruszasz rakietą naziemną w kierunku Grudziądza. Problem polega na tym, że systemy zakłócające nawigację na całej trasie sprawiają, że nie wiesz, co znajduje się przed tobą - możesz więc uderzyć w skałę. Jedyne, co możesz zrobić, to nasłuchiwać komunikatów radiowych opisujących położenie skał tuż przed Tobą.

Pamiętaj, że system OKO cały czas namierza każdy, nawet najdrobniejszy ruch, jaki wykonujemy na tych odludnych terenach. Jeśli system namierzania wykryje Cię, to wystrzeli pocisk, który zakończy Twoje życie. Mamy jednak dostęp do API, które umożliwia wykrycie, kiedy jesteś namierzany, oraz potrafi zneutralizować sygnał radarowy, dzięki czemu będziesz niewidoczny dla systemu OKO. Musisz jedynie sprawdzać w API przed wykonaniem każdego ruchu, czy znajdujesz się akurat koło radaru i jeśli tak, musisz przeprowadzić procedurę jego deaktywacji.

Uwaga: mechanizmy zagłuszające stosowane przez system OKO mają podwójne działanie. Po pierwsze, dane odbierane ze skanera częstotliwości są bardzo często zniekształcone, czy nawet zepsute. Po drugie, API może losowo zwracać błędy, nawet jeśli Twoje zapytanie jest poprawne. Twój kod musi być odporny zarówno na uszkodzone pakiety danych, jak i na losowe błędy API - w razie błędu po prostu ponów zapytanie.

Nazwa zadania: **goingthere**

Odpowiedź wysyłasz do https://hub.ag3nts.org/verify

Podgląd trasy i stanu gry:

https://hub.ag3nts.org/goingthere\_preview

## Sterowanie rakietą

Rakieta porusza się po siatce o wymiarach 3 wiersze na 12 kolumn. Start jest zawsze w kolumnie 1, w środkowym wierszu (wiersz 2). Baza w Grudziądzu znajduje się w kolumnie 12, w wierszu podanym na starcie. W każdej kolumnie znajduje się dokładnie jedna skała.

Masz do dyspozycji trzy komendy ruchu i jedną komendę startową:

- **start** - rozpoczyna nową grę, generuje nową mapę i resetuje wszystkie ustawienia.
- **go** - leci prosto do przodu (ta sama pozycja w wierszu, następna kolumna)
- **left** - idzie na wyższy wiersz i do przodu (góra + następna kolumna)
- **right** - idzie na niższy wiersz i do przodu (dół + następna kolumna)

Każdy ruch przesuwa rakietę o jedną kolumnę do przodu (także left i right!). Jeśli trafisz w skałę, rakieta rozbija się i musisz zacząć od nowa. Jeśli wypadniesz poza mapę, to także się rozbijasz. Jeśli nie zneutralizujesz systemu radarów, zostaniesz zestrzelony.

Rozpocznij grę:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "goingthere",
  "answer": {
    "command": "start"
  }
}
```

Po starcie otrzymasz informację o swojej pozycji, pozycji bazy docelowej oraz opis bieżącej kolumny (wolne wiersze i pozycja skały). Możesz wykonać bezpieczny ruch - przykładowo:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "goingthere",
  "answer": {
    "command": "go"
  }
}
```

## Radiowe wskazówki o skałach

Ponieważ nie widzisz trasy przed sobą, możesz poprosić o radiową wskazówkę. Endpoint:

https://hub.ag3nts.org/api/getmessage

```json
{
  "apikey": "tutaj-twoj-klucz"
}
```

W odpowiedzi otrzymasz pole "hint" z komunikatem w języku angielskim. Komunikat opisuje, po której stronie (lewa/prawa/przód) względem rakiety znajduje się skała w następnej kolumnie. Na tej podstawie musisz zdecydować, którą komendę ruchu wysłać, aby nie trafić w skałę. Komunikaty radiowe czasami bywają dziwne i używają języka stosowanego w żegludze.

## Skaner częstotliwości i skanery systemu OKO

Na trasie rozmieszczone są skanery systemu OKO - nie wiesz, gdzie się znajdują. Jeśli rakieta znajduje się w kolumnie z aktywną pułapką i spróbujesz wykonać ruch bez jej zneutralizowania, rakieta zostanie zestrzelona.

Aby sprawdzić, czy jesteś namierzany, odpytaj skaner częstotliwości metodą GET:

https://hub.ag3nts.org/api/frequencyScanner?key=tutaj-twoj-klucz

Skaner zwróci jedną z dwóch odpowiedzi:

- Gdy jest bezpiecznie, odpowiedź zawiera tekst "It's clear!"
- Gdy jesteś namierzany, odpowiedź zawiera JSON z kilkoma polami. Przede wszystkim jest tam podana częstotliwość namierzania oraz ciąg znaków niezbędny do wygenerowania kodu unicestwiającego radar.

**Pamiętaj**: odpowiedzi ze skanera są zniekształcone przez systemy zagłuszające. To, co otrzymasz, może wyglądać jak JSON, ale może nie być zdatne do parsowania.

## Neutralizacja pułapki

Gdy skaner wykryje namierzanie, musisz zneutralizować pułapkę, zanim wykonasz kolejny ruch. Wyślij POST na:

https://hub.ag3nts.org/api/frequencyScanner

```json
{
  "apikey": "tutaj-twoj-klucz",
  "frequency": 123,
  "disarmHash": "abc123def456..."
}
```

Gdzie:

- **frequency** to wartość liczbowa z pola "frequency" odczytana z odpowiedzi skanera
- **disarmHash** to hash SHA1 obliczony z wartości pola "detectionCode" z dopisanym na końcu słowem "disarm" (czyli SHA1 z ciągu: detectionCode + "disarm")

Jeśli dane będą poprawne, pułapka zostanie rozbrojona i będziesz mógł bezpiecznie kontynuować lot.

## Co musisz zrobić

1. Wystartuj grę komendą "start" i zanotuj pozycję bazy docelowej.
2. Na każdym polu najpierw odpytaj skaner częstotliwości przez API `frequencyScanner`, aby sprawdzić, czy nie jesteś namierzany.
3. Jeśli jesteś namierzany, sparsuj zniekształconą odpowiedź skanera, wyciągnij z niej "detectionCode" i "frequency", oblicz hash SHA1 i wyślij go do skanera, aby rozbroić pułapkę.
4. Pobierz wskazówkę radiową z endpointu `getmessage`, aby dowiedzieć się, gdzie jest skała w następnej kolumnie.
5. Na podstawie wskazówki wybierz odpowiednią komendę ruchu (go/left/right) i przesuń rakietę.  Pamiętaj, że nie wolno Ci także wylecieć poza mapę.
6. Powtarzaj kroki 2-5 aż dotrzesz do bazy w Grudziądzu.

Gdy rakieta dotrze do Grudziądza, otrzymasz flagę.
