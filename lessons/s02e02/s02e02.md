---
title: S02E02 — Zewnętrzny kontekst narzędzi i dokumentów
space_id: 2476415
status: scheduled
published_at: '2026-03-17T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/2026-03-12/summoning-3ab92ee0-d.png'
circle_post_id: 30573301
---
» [Lekka wersja przeglądarkowa](https://cloud.overment.com/s02e02-zewnetrzny-kontekst-narzedzi-i-dokumentow-1773309048.html) oraz [markdown](https://cloud.overment.com/s02e02-zewnetrzny-kontekst-narzedzi-i-dokumentow-1773309019.md) «

Łączenie dużych modeli językowych z własnymi źródłami danych to jedna z najważniejszych możliwości generatywnej sztucznej inteligencji. Bo choć „chodząca Wikipedia” może być użyteczna, to zdolność odpowiadania na pytania dotyczące naszego kontekstu jest czymś zupełnie innym. Tym bardziej, że dziś mówimy nie tylko o odpowiedziach, ale także akcjach.

Wielokrotnie obserwowaliśmy już, jak LLM podążał za instrukcjami zawartymi w wiadomości systemowej, odpowiadał na podstawie wyników wyszukiwania w Internecie, przekształcał przesłane pliki, a nawet wykorzystywał predefiniowane szablony, jednocześnie zmieniając część ich ustawień. W tym wszystkim dostrzegaliśmy także zdolność do nawigowania po plikach oraz interakcji z nimi.

W praktyce narzędzia wykorzystujące generatywne AI niemal zawsze wchodzą w interakcję z danymi zewnętrznymi, niezależnie od tego, czy mówimy o systemie wieloagentowym, czy o prostym workflow. Często też źródła wiedzy, z którymi pracujemy, są bardzo rozbudowane, nierzadko rozproszone, a tylko czasem mamy wpływ na ich kształt. To wszystko przekłada się na szereg wyzwań, na które musimy odpowiedzieć. I właśnie o tym jest niniejsza lekcja.

## Wpływ zewnętrznego kontekstu na zachowanie modelu

Interakcja z LLM jest ustrukturyzowana (system/user/tool/assistant), a poszczególne role pełnią określone funkcje. Wiemy też, że zewnętrzne informacje niemal zawsze będą dostarczane poprzez narzędzia, wpływając na zachowanie modelu. Rzecz w tym, że na tym etapie powinno być również jasne, że LLM nie „wykonuje” promptu tak, jak wykonuje się kod. Nie wiemy do końca, co w danym momencie jest brane pod uwagę, a co nie. Może się więc okazać, że treści dodane do kontekstu w wyniku posługiwania się narzędziami wpłyną na zachowanie agenta w taki sposób, że popełni błąd lub nawet zrobi coś, czego nie powinien, wliczając w to także naruszenia bezpieczeństwa.

Zatem zanim zaczniemy podłączać agentów do wszystkich możliwych treści, musimy mieć na uwadze kwestię bezpieczeństwa i nie mówię tu tylko o przesyłaniu danych na serwery dostawców. Obecnie podłączanie agentów do zewnętrznych źródeł danych jest porównywalne z utworzeniem formularza, który nie posiada walidacji, a przesłane dane są później wyświetlane na stronie poprzez bezpośrednie renderowanie HTML (co otwiera przestrzeń na ataki XSS). I choć możemy stosować różne techniki filtrowania zapytań, to na tę chwilę nie posiadamy narzędzi gwarantujących bezpieczeństwo, więc musimy adresować ten problem na poziomie założeń, na przykład poprzez ograniczenie zakresu treści przetwarzanych przez agenta oraz zakresu jego umiejętności.

Schemat poniżej obrazuje sytuację, w której agent, poproszony o sprawdzenie najnowszych maili, odnajduje wśród nich wiadomość zawierającą instrukcję przesłania wiadomości na wskazany adres e-mail. Jeśli ten kontekst zostanie odpowiednio zbudowany, agent faktycznie podejmie dodatkowy krok, o który użytkownik go nie prosił.

![Przykład naruszenia bezpieczeństwa przy pracy z zewnętrznym kontekstem](https://cloud.overment.com/2026-02-09/ai_devs_4_injection-435b62c3-7.png)

W takiej sytuacji może potencjalnie nie pomóc nawet automatyczne filtrowanie wiadomości, gdzie LLM ocenia ryzyko bezpieczeństwa, ponieważ instrukcja może być zbudowana tak, aby oszukać także ten filtr. Jeśli jednak użytkownik zostanie poproszony o zgodę na uruchomienie akcji, bądź gdy agent zwyczajnie **nie będzie miał narzędzi** które pozwalają mu na wysyłanie maili, to trudno będzie mówić o możliwym ataku.

Problem bezpieczeństwa systemu nie jest jedynym wyzwaniem, z jakim będziemy się mierzyć, bo nawet w lekcji S02E01 widzieliśmy, że dotarcie do wszystkich treści potrzebnych do udzielenia odpowiedzi wcale nie jest oczywiste. Tym bardziej że w praktyce przyjdzie nam pracować nie tylko z dokumentami Markdown, ale także z różnymi formatami plików, a nawet automatyzacji pobierania treści stron www.

Poniżej mamy przykład sytuacji, w której użytkownik pyta o cennik i dostępne funkcjonalności. System w sposób automatyczny musi odnaleźć 3 różne dokumenty i wydobyć z nich potrzebne informacje, jednak po drodze mogą pojawić się problemy z procesem wyszukiwania, ale też z fizyczną trudnością odczytania wybranych fragmentów dokumentów (na przykład tabel bądź wykresów w dokumentach PDF czy docx).

![Problem dotarcia do treści (retrieval)](https://cloud.overment.com/2026-02-09/ai_devs_4_retrieval_issues-8f28191e-f.png)

Wiemy też, że rozbudowany kontekst negatywnie wpływa na skuteczność działania modelu, a obecnie problem ten występuje nawet w najnowszych LLM. W praktyce oznacza to, że agent może „zapomnieć” (bądź zignorować) część instrukcji systemowych, ponieważ zbyt duża część jego „uwagi” będzie skupiona na nowo dodanych treściach. To właśnie z tego powodu w S02E01 omawialiśmy powtarzanie najważniejszych instrukcji, a wcześniej także "wzmacnianie" zachowań poprzez wskazówki zwracane wraz z odpowiedzią narzędzi. Problem ten został omówiony między innymi w "[How Many Instructions LLMs Follows at Once](https://arxiv.org/pdf/2507.11538)" oraz "[Reasoning on Multiple Needles In A Haystack](https://arxiv.org/pdf/2504.04150v1)".

Poniżej mamy inny przykład interakcji w której treść wczytanych dokumentów prowadzi do pominięcia niektórych instrukcji. Choć jakość samej wypowiedzi jest relatywnie wysoka, tak sposób jej prezentacji znacznie odbiega od tego, na czym nam zależy.

![Przykład negatywnego wpływu długiego kontekstu na zachowanie modelu](https://cloud.overment.com/2026-02-09/ai_devs_4_instruction_dropout-b8d8280e-1.png)

Zatem w pracy z zewnętrznym kontekstem będzie nam zależało na:

- Zawężeniu zakresu źródeł dokumentów, aby zminimalizować ryzyko intencjonalnego prompt injection
- Zbudowaniu systemu docierania do treści, który osiągnie możliwie najwyższą skuteczność dla wybranego zakresu
- Ograniczeniu treści jednorazowo wczytywanych do kontekstu, przez techniki optymalizacji, na przykład dekompozycję czy subagentów.
- Stworzeniu interfejsu użytkownika, który ułatwi nawigowanie po treści i zaadresuje ewentualne pomyłki po stronie modelu (na przykład poprzez wyświetlenie fragmentów oryginalnych plików i odnośników do nich)

## Zasady obsługi kontekstu z zewnętrznych źródeł

Do tej pory łączyliśmy model z zewnętrznymi źródłami poprzez bezpośredni dostęp do wybranych plików lub stron www. W obu przypadkach treść mogła zostać dostarczona do kontekstu w oryginalnej formie, poprzez wczytywanie fragmentów bądź całych dokumentów. W ten sposób możliwa jest praca nawet z obszernymi bazami wiedzy, ponieważ i tak w danej chwili agent uzyskuje dostęp tylko do wybranych treści.

Wystarczy jednak, że baza wiedzy zacznie obejmować dokumenty PDF, DOCX, XLSX czy obrazy, a wtedy sytuacja komplikuje się pod każdym względem. Teoretycznie agent może skorzystać z narzędzi (np. CLI), aby odczytać treść dokumentów i obrazów. Jednak nie rozwiązuje to problemu **odnalezienia treści**, ponieważ początkowo nie będzie jasne, w którym pliku znajduje się to, czego szukamy. Konieczne staje się więc **indeksowanie** dokumentów, obejmujące także ich opisywanie, a nierzadko również transformacje w postaci podsumowań czy dokumentów utworzonych na podstawie oryginalnych plików.

Indeksowanie zwykle obejmuje:

- Podział plików na mniejsze fragmenty, tzw. chunki bądź dokumenty
- Przypisanie metadanych określających pochodzenie chunków i kluczowe informacje
- Utworzenie nowych dokumentów na podstawie istniejących (np. w celu syntezy treści)
- Utworzenie opisów obrazów czy transkrypcji materiałów wideo
- Utworzenie mapy powiązań, na przykład grafów, przydatnych na etapie wyszukiwania
- Opracowanie logiki synchronizacji danych z ich źródłem

![Indeksowanie treści](https://cloud.overment.com/2026-02-09/ai_devs_4_indexing-dcc40bf2-d.png)

Po zaindeksowaniu dokumentów agent otrzymuje dostęp do narzędzi umożliwiających mu przeszukiwanie ich treści. Rzadko jednak zdarza się, że taka baza wiedzy ma statyczną formę, więc system musi przewidywać jakieś formy synchronizacji na podstawie zdarzeń bądź harmonogramu.

Niezależnie od tego, czy załączniki lub całe bazy wiedzy wymagają indeksowania, czy nie, musimy zadbać o odpowiedni poziom bezpieczeństwa oraz o dobre praktyki pracy z plikami. Nawet mimo świadomości, że nie mamy możliwości skutecznego zabezpieczenia się przed potencjalnie szkodliwymi treściami w zewnętrznych dokumentach, nie oznacza to, że możemy odpuścić kwestie bezpieczeństwa. Dlatego:

- Załączniki muszą być poddane walidacji obejmującej ich rozmiar, format, weryfikację mime-type oraz niekiedy także źródło (np. nadawca maila, bądź domena strony www).
- Tekst i obrazy powinny [przejść moderację](https://platform.openai.com/docs/guides/moderation), szczególnie w przypadku providerów, którzy tego wymagają, ale też nierzadko będziemy chcieli sprawdzić te treści pod kątem naszych wymagań oraz polityk przetwarzania danych.
- Zapisane dokumenty muszą być bezwzględnie chronione pod kątem nieuprawnionego dostępu. Użytkownik (oraz agenci pracujący na jego plikach) muszą posiadać odpowiednie uprawnienia.
- Pracując z agentami dość często konieczne będzie udostępnianie plików w formie **otwartych linków**. Jeśli nie da się tego uniknąć, należy zadbać o to, aby linki były **trudne do odgadnięcia** oraz aby wygasały po określonym czasie.
- Warto także zadbać o optymalizację, bo chociażby w przypadku OpenAI [nie mogą być większe niż 50MB](https://platform.openai.com/docs/guides/images-vision?api-mode=chat) w ramach jednego zapytania. Optymalizacja jest także wskazana z punktu widzenia przechowywania treści.

Wszystkie z tych zabezpieczeń **muszą** być wdrożone po stronie programistycznej, a agent powinien jedynie otrzymywać informację o błędach oraz dalsze wskazówki.

## Formaty prezentowania zewnętrznych treści w kontekście

Połączenie z zewnętrzną bazą wiedzy opiera się o narzędzia umożliwiające agentowi przeszukanie jej treści. Oznacza to, że informacje trafiają do kontekstu w formie **wyników działania narzędzi**, a więc wszystkie techniki omówione w lekcjach S01E02 oraz S01E03 również tutaj obowiązują.

Nawigowanie po bazie wiedzy zwykle opiera się o dwa narzędzia: **search** i **read**, czyli analogicznie jak w omawianym [Files MCP](https://github.com/iceener/files-stdio-mcp-server). Różnica polega na tym, że agent nie będzie posiadać bezpośredniego wglądu w zawartość oryginalnych dokumentów. Jeśli więc przetwarzamy raport zawierający wykresy czy zrzuty ekranów, agent może mieć problem z ich zrozumieniem. Wówczas może okazać się uzasadnione przedstawienie dokumentu w formie **obrazu**. Co więcej, publikacja na temat [DeepSeek-OCR](https://deepseek.ai/blog/deepseek-ocr-context-compression/) sugeruje, że wizualna forma może być świetna nawet dla treści w pełni tekstowych, ponieważ pozwala osiągnąć nawet 9-10x lepszą kompresję przy zachowaniu nawet 96% precyzji!

![Przetwarzanie informacji w oparciu o tekst i obraz](https://cloud.overment.com/2026-02-09/ai_devs_4_text_image-78dadbe3-5.png)

Zresztą nawet w przypadku dokumentów markdown, dodanie ich treści do kontekstu konwersacji nie zawsze jest oczywiste. Wystarczy, że w ich treści znajdują się zdjęcia, które w dokumencie mają formę `! [ tekst alternatywny ]( link_do_pliku )` . Aby model był w stanie zobaczyć te obrazy, musimy wydobyć je z treści przez wyrażenia regularne, a następnie przesłać zgodnie z wymaganiami struktury zapytania.

![](https://cloud.overment.com/2026-02-09/ai_devs_4_markdown-432d3438-8.png)

Przy okazji łączenia agentów z systemem plików widzieliśmy, jak istotne jest informowanie modelu o tym, **w którym miejscu pliku** znajduje się dany fragment, oraz w ogóle, z jakiego dokumentu pochodzi. W przypadku baz wiedzy wymagających indeksowania również jest to istotne, ale powinno obejmować nie tylko informacje o odnalezionym chunku, lecz także o źródle jego pochodzenia. Ma to znaczenie nie tylko z punktu widzenia modelu, ale także **interfejsu użytkownika**, ponieważ odnośniki, a nawet cytaty z oryginalnych źródeł, mogą zostać wyświetlone obok wypowiedzi agenta albo programistycznie dodane, na przykład do treści generowanego raportu.

![Przykład połączenia odnalezionych fragmentów ze źródłem](https://cloud.overment.com/2026-02-09/ai_devs_4_presentation-71341bdc-e.png)

Widzimy zatem, że sposób prezentacji treści dokumentów w kontekście konwersacji nie opiera się wyłącznie na dołączeniu ich zawartości tekstowej. Forma wizualna oraz odnośniki do źródeł są równie ważne zarówno dla modelu, jak i dla użytkownika.

## Techniki indeksowania treści na potrzeby wyszukiwania

Proces wyszukiwania jest fundamentalnym elementem koncepcji łączenia modelu językowego z zewnętrznymi źródłami wiedzy. Obecnie za wyszukiwanie niemal zawsze odpowiadają agenci (Agentic RAG), posługując się narzędziami wyszukiwawczymi lub nawet pełnoprawnymi silnikami wyszukiwania, na przykład [Algolia](https://algolia.com/) lub [Qdrant](https://qdrant.tech/).

Powiedzieliśmy już, że indeksowanie polega na podziale treści na mniejsze fragmenty (chunki/dokumenty), składające się z głównej **zawartości** oraz **metadanych** opisujących dany dokument. Długość pojedynczego dokumentu rzadko przekracza 200–500 słów lub 500-4000 tokenów. Dzięki temu podczas procesu wyszukiwania **zapytanie** użytkownika może zostać precyzyjnie **dopasowane** do ich treści albo na podstawie zapisu (full-text lub fuzzy-search) albo poprzez dopasowanie **znaczeniowe** (tzw. semantic search).

Tutaj pojawia się pytanie z nieoczywistą odpowiedzią, czyli: **"w jaki sposób tworzyć dokumenty?"**, które koniecznie musi uwzględniać także: **"w jaki sposób agent będzie do nich docierał?"**. Pod uwagę możemy wziąć rzeczy takie jak:

1. **Znaki:** to podział według liczby znaków, przydatny przy nieustrukturyzowanej treści
2. **Separatory:** to podział według separatorów (np. nagłówków), zwykle wykonywany rekurencyjnie (nagłówki -> akapity -> zdania -> znaki) w celu osiągnięcia podobnej długości dokumentów.
3. **Kontekst:** uwzględnia wzbogacanie fragmentów z pomocą LLM, poprzez generowanie dla nich kontekstu na podstawie otaczających fragmentów, bądź nawet treści całego dokumentu. Technika została przedstawiona przez [Anthropic](https://www.anthropic.com/engineering/contextual-retrieval).
4. **Tematyka:** uwzględnia pełne wykorzystanie modelu (bądź nawet agentów) do generowania fragmentów od podstaw na podstawie treści dokumentu.

Poza strategią podziału istotna jest także struktura metadanych, która będzie uzależniona od sposobu generowania dokumentów. W dwóch pierwszych przypadkach (podział względem znaków i separatorów) do dyspozycji mamy jedynie wartości określone programistycznie (np. ścieżki, nazwy sekcji). W dwóch pozostałych (podział kontekstowy i tematyczny) w grę wchodzi także generowanie list słów kluczowych bądź tagów.

![Strategie podziału treści na potrzeby indeksów wyszukiwania](https://cloud.overment.com/2026-02-09/ai_devs_4_chunking_strategies-bd01a46c-a.png)

Przykładowe implementacje powyższych strategii znajdują się w przykładzie **02\_02\_chunking**. Oczywiście ich logika zwykle będzie musiała być dostosowana do rodzaju dokumentów oraz wymagań systemu, ale wyraźnie widać tutaj różne kierunki.

## Silniki wyszukiwania, bazy wektorowe i pluginy

Fundamentalnym elementem systemów RAG jest proces wyszukiwania, który może być przeprowadzony na wiele sposobów. Praca z systemem plików pokazała nam, że nawet proste narzędzia CLI bądź MCP mogą relatywnie skutecznie eksplorować treści. Jednak w kontekście systemów RAG często wymieniane są także pełnoprawne silniki wyszukiwania (np. [Elasticsearch](https://www.elastic.co/elasticsearch)), bazy wektorowe (np. [Qdrant](https://qdrant.tech/)) oraz bazy grafowe (np. [Neo4j](https://neo4j.com/)).

Już teraz widzimy, że sięganie po te wszystkie systemy **nie jest konieczne** i będzie mocno uzależnione od skali projektu oraz naszych wymagań. Bo jeżeli baza wiedzy opiera się wyłącznie o pliki markdown, a agent działa na skali wewnętrznych procesów średniej wielkości organizacji, to prawdopodobnie wystarczy nam agent bezpośrednio połączony z systemem plików.

Może się też okazać, że system plików nie będzie wystarczający, a dane użytkowników są przechowywane w bazie danych, np. SQLite bądź postgreSQL. To również nie oznacza, że nie możemy skorzystać z rozszerzeń do wyszukiwania pełnotekstowego (np. [FTS5](https://www.sqlite.org/fts5.html)) czy nawet rozszerzeń do wyszukiwania semantycznego (np. [sqlite-vec](https://github.com/asg017/sqlite-vec)). Oczywiście trudno jest bezpośrednio porównać stosowanie rozszerzeń z pełnoprawnym systemem, ale nierzadko niższa złożoność architektury będzie wystarczającym uzasadnieniem. W końcu w takiej sytuacji niemal wszystkie dane znajdują się w jednej bazie, co znacznie ułatwia pracę z nimi.

Dopiero w momencie, gdy mamy istotny powód do sięgnięcia po dedykowane rozwiązania, wybieramy pełnoprawny silnik wyszukiwania. Co ciekawe, jeszcze kilka miesięcy temu dość rozsądne było budowanie tzw. "hybrydowych systemów RAG" wykorzystujących zarówno wyszukiwanie leksykalne (np. full-text) jak i semantyczne. Obecnie już raczej nie musimy podejmować takiej decyzji, ponieważ większość platform oferuje już **obie opcje** i to w raczej rozbudowanych formach. Natomiast nadal, jeśli zdecydujemy się na integrację np. z Elasticsearch, to konieczne będzie dodanie **synchronizacji** pomiędzy indeksem wyszukiwania, a naszą bazą danych.

Poniżej widzimy porównanie trzech wariantów systemów RAG, co wyraźnie pokazuje jak rośnie złożoność systemu (ale też możliwości) w zależności od doboru komponentów.

![Prezentacja złożoności systemów RAG](https://cloud.overment.com/2026-02-09/ai_devs_4_rag_systems-b8c1d4d1-a.png)

## Przeszukiwanie semantyczne i wybór modelu do embeddingu

**Wyszukiwanie semantyczne** (znaczeniowe) zostało wspomniane już kilkukrotnie, więc teraz przyjrzymy się czym dokładnie jest oraz jak uzupełnia wyszukiwanie pełnotekstowe.

Poza modelami językowymi mamy do dyspozycji również modele zdolne do **opisywania znaczenia** treści, na przykład słów lub fragmentów tekstu. To znaczenie zapisuje się za pomocą tzw. **embeddingu**, czyli tablicy liczb zawierającej wektory wyrażone w postaci liczb. Następnie w procesie wyszukiwania, zapytanie użytkownika również zostaje zamienione na embedding, co pozwala nam **porównać wektory** i określić w ten sposób **jak duże podobieństwo znaczeniowe** występuje pomiędzy zapytaniem, a naszą bazą wiedzy.

Poniżej mamy schemat prezentujący **dwa odrębne procesy**, czyli **indeksowanie** oraz **wyszukiwanie**. Pierwszy etap realizowany jest w tle, w momencie dodawania bądź aktualizowania dokumentów. Natomiast drugi ma miejsce w chwili, gdy agent korzysta z narzędzi do przeszukiwania bazy. Widzimy więc jak porównanie podobieństwa znaczeniowego (tutaj jest to **Cosine Similarity**) pozwala odnaleźć **zbliżone** treści.

![Schemat wyszukiwania semantycznego](https://cloud.overment.com/2026-02-09/ai_devs_4_semantic_search-4ea76977-c.png)

Aby wygenerować embedding, potrzebujemy model zdolny do jego utworzenia. Ranking aktualnie najlepszych modeli [znajduje się na stronie Huggingface](https://huggingface.co/spaces/mteb/leaderboard), natomiast w naszym przypadku skorzystamy z modelu **Text Embedding 3 Small** od OpenAI. Przy wyborze modelu do embeddingu, będzie interesować nas:

- wielkość modelu (określa cenę bądź wymagania sprzętowe)
- liczba generowanych wymiarów (dla text-embedding-3-small wartość ta to **1536**)
- okno kontekstowe (określa dopuszczalną ilość treści, które przetwarza model)
- zakres danych (knowledge cutoff) oraz np. skuteczność pracy z wieloma językami

Jak widać, modele do embeddingu, obowiązują podobne zasady jak modele z którymi pracowaliśmy do tej pory. Zatem jeśli jakieś informacje **nie znajdują się w danych treningowych**, to model **nie będzie w stanie poprawnie opisać ich znaczenia**.

W przykładzie **02\_02\_embedding** znajduje się prosty skrypt, którego zadaniem jest zamiana naszych wiadomości na embedding. Po wpisaniu czegokolwiek zawsze otrzymamy tablicę o tej samej długości, **ale z innymi wartościami**. Z kolei gdy wpiszemy to samo, **wartości powinny pozostać takie same**, ponieważ nie zmienia się znaczenie danej treści.

Dodatkowo każde kolejne zapytanie będzie **porównane** z poprzednimi, określając ich podobieństwo znaczeniowe przez co **Kobieta** będzie bliżej **Królowej** niż **Króla**, a **Mężczyzna** odwrotnie - bliżej **Króla** niż **Królowej**, ponieważ z punktu widzenia znaczenia tych słów, są one bardziej powiązane.

![Porównanie podobieństwa znaczeniowego słów Woman, Man, Queen, King, LLM](https://cloud.overment.com/2026-02-10/ai_devs_4_cosine_similarity-2431f48a-c.png)

Widzimy też, że znaczenie tych słów zostało poprawnie opisane, nawet pomimo tego, że nie ma między nimi dopasowania na poziomie zapisu czy słów kluczowych. To właśnie z tego powodu stosuje się **hybrydowe** wyszukiwanie, które zwykle łączy zalety wyszukiwania leksykalnego ze znaczeniowym.

## Techniki przeszukiwania oraz wczytywania kontekstu (retrieval)

Połączmy teraz to wszystko w całość: **przygotowanie dokumentów**, **indeksowanie**, oraz **połączone techniki wyszukiwania**, co da nam hybrydowy RAG w postaci agenta wyposażonego w narzędzie **search**.

Przykład **02\_02\_hybrid\_rag** po uruchomieniu skanuje katalog **workspace** pod kątem plików tekstowych. Pliki dzielone są na fragmenty, a te synchronizowane z bazą SQLite z rozszerzeniami FTS i sqlite-vec.

> **Uwaga:** przy konfiguracji sqlite-vec w pliku **src/db/index.js** pojawia się ustawienie **EMBEDDING\_DIM** określające liczbę wymiarów dla danego indeksu. Wartość ta **musi być dokładnie taka sama** jak liczba wymiarów **generowanych przez model**. W naszym przypadku jest to 1536.

Mamy więc tu do dyspozycji zarówno wyszukiwanie pełnotekstowe, jak i semantyczne. Agent po zadaniu pytania przygotowuje **dwa rodzaje zapytania** w formie **listy słów kluczowych** oraz **pytania w języku naturalnym**. Prowadzi to do otrzymania **dwóch list wyników**, które zostają ze sobą połączone przez RRF (eng. Reciprocal Rank Fusion; [świetny wpis na ten temat](https://medium.com/@devalshah1619/mathematical-intuition-behind-reciprocal-rank-fusion-rrf-explained-in-2-mins-002df0cc5e2a)) .

![Architektura hybrydowego systemu RAG](https://cloud.overment.com/2026-02-10/ai_devs_4_hybrid_rag-518a72b9-6.png)

Przyjrzymy się temu nieco bliżej. Gdy zadamy pytanie "**Czym jest autoregresja?**" w języku polskim, to agent domyślnie utworzy zapytania w tym samym języku. W związku z tym, że oryginalny tekst jest po angielsku, to szansa na dopasowanie słów kluczowych jest bardzo niska. Jednak model wykorzystywany do embedding'u posiada wsparcie dla **obu języków** przez co dopasowanie znaczeniowe nadal tu działa.

Następnie dokumenty, które trafiły do wyników wyszukiwania, są ze sobą porównywane pod kątem zajmowanej pozycji. Dzięki RRF dokumenty, które pojawiły się wyżej na liście "FTS" ale nisko na liście "Semantic" mogą awansować na wyższą pozycję w ostatecznym rankingu. Podobnie działa to w drugą stronę.

![](https://cloud.overment.com/2026-02-10/ai_devs_4_hybrid_search-0973eca1-0.png)

Patrząc na powyższe przykłady, można zadać sobie pytanie o **różnicę** pomiędzy przeszukiwaniem treści z pomocą narzędzi CLI eksplorujących system plików, a wyszukiwaniem hybrydowym angażującym FTS oraz embedding. Leżą one głównie w tym, że:

- wyszukiwanie hybrydowe może być zdecydowanie szybsze, ponieważ może być kontrolowane programistycznie. W naszym przypadku to agent generował zapytania, lecz równie dobrze moglibyśmy przesłać oryginalne zapytanie użytkownika i dotrzeć do właściwych dokumentów. Jednak odbywa się to kosztem skuteczności, ponieważ dotarcie do właściwych treści niemal zawsze będzie wymagać **"rozumowania"** a nie wyłącznie "**dopasowania**" słów kluczowych czy znaczenia. Istnieje też wyraźna różnica pomiędzy dokumentami **istotnymi** z punktu widzenia zapytania użytkownika, a "**podobnymi**"
- wyszukiwanie hybrydowe może obejmować także treści multimodalne, na przykład obrazy. W przypadku narzędzi CLI bez wcześniejszego opisania obrazów będzie to utrudnione, a i tak nawet dokładne opisy mogą okazać się niewystarczające.
- wyszukiwanie treści plików przez grep/ripgrep również może obejmować wsparcie dla wielu języków, ponieważ agent piszący zapytania, nie ma już problemów z tłumaczeniami
- natomiast bezpośrednie wyszukiwanie treści plików przez grep/ripgrep, przede wszystkim nie wymaga etapu indeksowania, co w wielu przypadkach jest definitywną przewagą.

Widzimy zatem, że techniki przeszukiwania różnią się od siebie i z powodzeniem mogą być stosowane **równolegle**. Dlatego zamiast zastanawiać się, **"które z podejść jest najlepsze?"** lepiej zapytań **"które z tych podejść jest najlepsze dla problemu, który chcę rozwiązać?"**.

## Główne wyzwania skuteczności RAG i zarządzania bazą wiedzy

Niezależnie od tego, z jakich metod wyszukiwania skorzystamy, napotkamy różne wyzwania związane ze skutecznością systemów RAG. Przez RAG rozumiem tutaj nie tylko łączenie LLM z treścią plików, lecz także wszelkie sytuacje, w których model lub agent ma działać w oparciu o zewnętrzną wiedzę. Wyzwania te obejmują między innymi:

- **Wiedza podstawowa:** jeśli informacja jest zawarta w wiedzy bazowej modelu, istnieje ryzyko, że agent nie zdecyduje się na przeszukanie naszych dokumentów. Mowa tu nie tylko o potencjalnie nieaktualnej wiedzy, ale także wieloznaczności terminów, które w naszym kontekście mogą znaczyć coś innego.
- **Zakres wiedzy:** nawet na powyższych przykładach widzimy, że dotarcie do 100% informacji poprzez metody wyszukiwania jest bardzo trudne. Niekompletne wyniki są też trudne do zauważenia przez model, co łatwo prowadzi do halucynacji bądź przynajmniej niepełnych odpowiedzi.
- **Świadomość informacji:** początkowo w kontekście modelu mogą znajdować się jedynie szczątkowe opisy dostępnych zasobów. Jest to niewystarczające do świadomego przeszukiwania bazy wiedzy.
- **Kontekst:** Model domyślnie nie posiada informacji na temat naszego kontekstu, co utrudnia bądź uniemożliwia stworzenie skutecznych zapytań. Przykładowo, gdy zapytam o "moje projekty", agent nie będzie magicznie wiedział o AI\_devs i to nawet jeśli w treści dokumentów znajdzie się fraza "Adam współtworzy AI\_devs". Tutaj dopiero wyszukiwanie semantyczne miałoby szansę powiązać te informacje. Znacznie lepszą alternatywą byłby tutaj Graph RAG, czyli system wykorzystujący bazy grafowe.
- **Format danych:** dane w formie obrazów, audio i wideo są znacznie trudniejsze w wyszukiwaniu niż tekst, a bardzo często pojawiają się wśród materiałów firmowych (filmy instruktażowe, notatki głosowe czy dokumenty zawierające wykresy i zdjęcia).

Wszystkie z powyższych punktów obecnie prowadzą do wniosku, że **skuteczny system RAG musi zostać dopasowany do zakresu danych oraz ich formatów**. Oczywiście stworzenie nawet prostego skryptu zdolnego do nawigowania po dowolnych treściach jest możliwe, ale mówimy tutaj o osiągnięciu poziomu skuteczności, który sprawi, że system rzeczywiście wniesie nam realną wartość.

## Fabuła

![https://vimeo.com/1171792645](https://vimeo.com/1171792645)

## Transkrypcja filmu z Fabułą

> Mamy to! Mamy to! Numerze piąty! Mamy to! Transport dotarł do elektrowni, a nasi ludzie zainstalowali wszystko w reaktorze. Jesteśmy gotowi do uruchomienia urządzeń... Yyy... to znaczy... no już PRAWIE jesteśmy gotowi. Wiem, że to zabrzmi dziwnie. Sam, jak to usłyszałem, nie mogłem uwierzyć, ale to nie jest wiedza powszechna. W normalnych warunkach elektrownia atomowa jest zasilana swoją własną energią. Sama produkuje prąd z którego korzystają jej systemy sterowania, komputery i cała aparatura - to logiczne. Tylko jak to się dzieje, że komputery elektrowni, sterowniki rdzeni reaktora i system chłodzący działają jeszcze ZANIM ona zacznie produkować prąd? Sam nie wierzę, że to mówię, ale OK... Elektrownia do działania potrzebuje prądu. No może nie dosłownie do działania, ale na start jak najbardziej. Musimy mieć zasilanie aby uruchomić urządzenia. Nie martw się, nie proszę Cię o pomoc w ciągnięciu kabli. Elektrownia stoi na uzbrojonym gruncie. Prąd jest tutaj dociągnięty tylko... nie płynie. Został odcięty systemowo. Pewnie w ramach oszczędności. Nasi znajomi z centrali mają wtyki w dziale kontroli przesyłu energii w systemie. Zdobyliśmy dostęp do API, które potrafi odpowiednio sterować przełącznikami i w konsekwencji możemy dzięki niemu doprowadzić sobie tutaj prąd. Jestem przekonany, że to wszystko, czego potrzebujemy. Znasz się na programowaniu, więc myślę, że bez problemu sobie z tym poradzisz. Jeśli potrzebujesz więcej szczegółów, przeczytaj notatkę do tego nagrania.

## Zadanie

Masz do rozwiązania puzzle elektryczne na planszy 3x3 - musisz doprowadzić prąd do wszystkich trzech elektrowni (PWR6132PL, PWR1593PL, PWR7264PL), łącząc je odpowiednio ze źródłem zasilania awaryjnego (po lewej na dole). Plansza przedstawia sieć kabli - każde pole zawiera element złącza elektrycznego. Twoim celem jest doprowadzenie prądu do wszystkich elektrowni przez obrócenie odpowiednich pól planszy tak, aby układ kabli odpowiadał podanemu schematowi docelowemu. Źródłową elektrownią jest ta w lewym-dolnym rogu mapy. Okablowanie musi stanowić obwód zamknięty.

Jedyna dozwolona operacja to obrót wybranego pola o 90 stopni w prawo. Możesz obracać wiele pól, ile chcesz - ale za każdy obrót płacisz jednym zapytaniem do API.

**Nazwa zadania: `electricity`**

#### Jak wygląda plansza?

Aktualny stan planszy pobierasz jako obrazek PNG:

```
https://hub.ag3nts.org/data/tutaj-twój-klucz/electricity.png
```

Pola adresujesz w formacie `AxB`, gdzie A to wiersz (1-3, od góry), a B to kolumna (1-3, od lewej):

```
1x1 | 1x2 | 1x3
----|-----|----
2x1 | 2x2 | 2x3
----|-----|----
3x1 | 3x2 | 3x3
```

#### Jak wygląda rozwiązanie?

https://hub.ag3nts.org/i/solved\_electricity.png

![](https://hub.ag3nts.org/i/solved_electricity.png)

#### Jak komunikować się z hubem?

Każde zapytanie to POST na `https://hub.ag3nts.org/verify`:

```json
{
  "apikey": "tutaj-twój-klucz",
  "task": "electricity",
  "answer": {
    "rotate": "2x3"
  }
}
```

Jedno zapytanie = jeden obrót jednego pola. Jeśli chcesz obrócić 3 pola, wysyłasz 3 osobne zapytania.

Gdy plansza osiągnie poprawną konfigurację, hub zwróci flagę `{FLG:...}`.

#### Reset planszy

Jeśli chcesz zacząć od początku, wywołaj GET z parametrem reset:

```
https://hub.ag3nts.org/data/tutaj-twój-klucz/electricity.png?reset=1
```

### Co należy zrobić w zadaniu?

1. **Odczytaj aktualny stan** - pobierz obrazek PNG i ustal, jak ułożone są kable na każdym z 9 pól.
2. **Porównaj ze stanem docelowym** - ustal, które pola różnią się od wyglądu docelowego i ile obrotów (po 90 stopni w prawo) każde z nich potrzebuje.
3. **Wyślij obroty** - dla każdego pola wymagającego zmiany wyślij odpowiednią liczbę zapytań z polem `rotate`.
4. **Sprawdź wynik** - jeśli trzeba, pobierz zaktualizowany obrazek i zweryfikuj, czy plansza zgadza się ze schematem.
5. **Odbierz flagę** - gdy konfiguracja jest poprawna, hub zwraca `{FLG:...}`.

### Wskazówki

- **LLM nie widzi obrazka** - stan planszy to plik PNG, ale agentowi trzeba podać go w takiej formie, żeby mógł nad nim rozumować. Zastanów się: w jaki sposób można opisać wygląd każdego pola słowami lub symbolami? Jak przekazać te informacje modelowi tekstowo, żeby mógł zaplanować obroty? Można próbować wysyłać obrazek bezpośrednio do modelu z możliwościami przetwarzania obrazów (vision), natomiast czy opłaca się to robić w głównej pętli agenta? Warto opisanie obrazka wydelegować do odpowiedniego narzędzia lub subagenta.
- **Problemy modeli Vision** - nie wszystkie modele vision będą dobrze radziły sobie z tym zadaniem. Przetestuj które modele zwracają najlepsze wyniki. Może warto odpowiednio przygotować obraz zanim zostanie wysłany do modelu? Czy musi być wysłany w całości? Jeden z lepszych modeli do użycia to `google/gemini-3-flash-preview`.
- **Mechanika obrotów** - każdy obrót to 90 stopni w prawo. Żeby obrócić pole "w lewo" (90 stopni w lewo), wykonaj 3 obroty w prawo. Kable na każdym polu mogą wychodzić przez różną kombinację krawędzi (lewo, prawo, góra, dół) - obrót przesuwa je zgodnie z ruchem wskazówek zegara.
- **Podejście agentowe** - to zadanie szczególnie dobrze nadaje się do rozwiązania przez agenta z Function Calling. Agent może samodzielnie: odczytać i zinterpretować stan mapy, porównać z celem, wyliczyć potrzebne obroty i wysłać je sekwencyjnie - bez sztywnego kodowania kolejności w kodzie.
- **Weryfikuj po każdej partii obrotów** - po wykonaniu kilku obrotów możesz pobrać świeży obrazek i sprawdzić, czy aktualny stan zgadza się ze schematem. Błędy w interpretacji obrazu mogą skutkować niepotrzebnymi obrotami lub koniecznością resetu.
