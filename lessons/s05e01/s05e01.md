---
title: S05E01 — Architektura
space_id: 2476415
status: scheduled
published_at: '2026-04-06T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/the-architect-1775194817.png'
circle_post_id: 31353053
---
## Film do lekcji

![https://vimeo.com/1179919808](https://vimeo.com/1179919808)

Dotychczasowe lekcje pokazały nam, że generatywne aplikacje to faktycznie w 80% kod, który pojawia się w klasycznych aplikacjach. Jest jednak tu kilka zmiennych, których nie wzięliśmy pod uwagę. Po pierwsze, LLM potrafi zrealizować dużą część logiki, której już nie musimy pisać. Po drugie, architektura aplikacji musi uwzględniać obecność AI bardziej, niż z początku się wydaje. Wyraźne zmiany są obecne niemal wszędzie - od interfejsu użytkownika, przez API, po struktury bazy danych czy konfigurację serwerów. Pojawia się także potrzeba skorzystania z szeregu dodatkowych narzędzi czy bibliotek, których normalnie by nie było.

Dlatego dziś odpowiemy sobie na pytanie, jak może wyglądać architektura aplikacji w której pojawiają się LLMy, bądź w przypadku której stanowią one absolutną podstawę.

### Cechy aplikacji wykorzystującej generatywne AI

Modele oraz agenci AI mogą pojawiać się w logice aplikacji w różnym zakresie. Czasem będą stanowić fundament całego produktu i wówczas architektura będzie pod to ułożona. Innym razem będą pojawiać się jako jeden z modułów, który musi dopasować się do reszty. Okazuje się jednak, że w obu przypadkach decyzje, które musimy podjąć będą podobne i będą obejmować:

- **Gateway:** czyli scentralizowaną logikę odpowiadającą za komunikację z AI. Uwzględnia ona zarządzanie połączeniem, ustawieniami zapytań czy monitorowaniem. Całość powinna być zaprojektowana w taki sposób, aby umożliwić nam **swobodne przełączanie się** pomiędzy różnymi modelami, **a nawet dostawcami.** Można to osiągnąć poprzez skorzystanie z **AI SDK** bądź **LiteLLM** albo własnego formatu API mapowanego do formatów poszczególnych providerów.
- **API:** czyli struktura endpointów oraz ich ustawienia. Klient (np. aplikacja webowa) nie powinien mieć bezpośredniego dostępu do modelu, np. przez endpoint `/api/chat`, o ile nie jest to konieczne. Zamiast tego powinniśmy przygotować wyspecjalizowane endpointy, np. `/product/review`, które przyjmują i zwracają dane o ustalonym kształcie. Inaczej mówiąc - kontakt z modelem powinien być ograniczony już na poziomie API.
- **System plików:** czyli konfiguracje dostępu do katalogów i plików dla agentów działających w imieniu użytkowników. Musimy tu zadbać przede wszystkim o zakresy uprawnień oraz zasady interakcji z dokumentami. Jest to trudniejsze niż w przypadku klasycznych aplikacji, ponieważ agent AI może nawet przypadkiem podjąć akcje, których się nie spodziewamy (jak np. usunięcie całego katalogu(!)).
- **Baza danych:** czyli dodatkowe struktury powiązane bezpośrednio z agentami, ich aktywnością oraz wiedzą. Konieczne będzie tu zapisywanie interakcji, zaplanowanych zadań, a nierzadko także definicji oraz ustawień samych agentów i ich narzędzi.
- **Zależności:** czyli biblioteki i narzędzia związane np. z ewaluacją, obserwowaniem, transformacją dokumentów (np. markdown), wyszukiwaniem semantycznym, renderowaniem strumieniowanych treści markdown do HTML czy frameworkami AI (o ile zdecydujemy się na skorzystanie z nich).

![Generatywne aplikacje - architektura](https://cloud.overment.com/2026-03-16/ai_devs_4_architecture-1f6d8c0d-e.png)

Podejmowanie decyzji o kształcie architektury w kontekście logiki agentów oraz zasobów na których pracują, można porównać z integracją zewnętrznego systemu, np. **systemu płatności**. Tam również musimy podjąć decyzję o jego roli w systemie czy zorganizować struktury danych tak, aby możliwe było zrealizowanie całego procesu oraz połączenie go z istniejącymi modułami (np. powiadomieniami). Zazwyczaj konieczne będzie też zadbanie o przygotowanie logiki w taki sposób, aby możliwe było **połączenie z wieloma operatorami płatności** i wygodne przełączanie się między nimi.

Wśród decyzji, które będziemy podejmować, można uwzględnić kilka, które niemal zawsze będą "pewnikami", np.:

- Centralizacja interakcji z AI niemal zawsze będzie priorytetem. Budowanie i wysyłanie zapytań z wielu miejsc aplikacji bardzo utrudnia zarządzanie globalnymi ustawieniami czy nawet przełączanie między modelami.
- Otwartość na więcej niż jednego providera, powinna być przynajmniej mocno wzięta pod uwagę, ponieważ nie będziemy chcieli blokować możliwości skorzystania ze znacznie lepszych modeli innych dostawców.
- Wsparcie dla strumieniowania zdarzeń, w celu informowania użytkownika o postępach oraz zmniejszenia czasu reakcji.
- Wsparcie multimodalności, nawet jeśli początkowo będziemy przetwarzać wyłącznie tekst. Wystarczy otworzyć sobie "furtkę" w postaci zbudowania struktur baz danych tak, aby przetwarzanie obrazu bądź formatu audio było łatwe do dodania.
- Wsparcie logiki agentów, nawet jeśli początkowo budujemy prostego czatbota. Przykładowo zamiast tworzyć tabelę `messages` zawierającą tekst, można skorzystać ze struktury tabeli `items` wspomnianej chociażby w **S01E01**, aby ułatwić sobie monitorowanie poszczególnych akcji występujących **pomiędzy** wiadomościami.
- Obsługa zdarzeń realizowanych w dużym horyzoncie czasowym. Na produkcji szybko okaże się, że użytkownik zamknie kartę przeglądarki albo po prostu czas realizacji zadania przekroczy dopuszczalne limity czasu połączenia.

Powyższe punkty występują w każdym z moich projektów, niezależnie od tego czy mówimy jedynie o wybranych funkcjonalnościach czy całym systemie ukierunkowanym na logikę agentów.

### Fundamentalna cecha produktów w dobie AI

Przy obecnym tempie rozwoju modeli oraz ekosystemu narzędzi, każdy tworzony przez nas system **powinien** (jeśli to możliwe) być zaprojektowany tak, aby **dalszy rozwój modeli wzmacniał jego możliwości**. Warto odnieść się do tego zarówno w kontekście biznesowym, produktowym, jak i technologicznym.

Obszar biznesowy leży zwykle poza naszą kontrolą. Jednak budowanie rozwiązań adresujących obszary z którymi obecnie LLM radzą sobie przeciętnie, raczej nie jest dobrym pomysłem. Szczególnie gdy widzimy wyraźny postęp w skuteczności najnowszych modeli, powinno dać nam to domyślenia. W przeciwnym razie może się okazać, że premiera kolejnych wersji modeli sprawi, że nasz produkt stanie się niepotrzebny, albo wysiłek który włożyliśmy w opracowanie funkcjonalności nigdy się nie zwróci. Oczywiście są tutaj wyjątki, ale mówimy tu raczej o realnym ryzyku, które należy brać pod uwagę.

Ta sama sytuacja ma też przełożenie na obszar technologiczny, ponieważ systemy które tworzymy powinny być podatne na modyfikacje bardziej niż kiedykolwiek. A to oznacza, że nasze umiejętności budowania architektury mają jeszcze większe znaczenie. Istotną rolę odgrywają tutaj **detale** implementacji, które mogą nam znacznie utrudnić bądź zablokować rozwój. Co prawda dziś z pomocą agentów AI jesteśmy w stanie dość łatwo wprowadzić nawet rozległe modyfikacje w rozbudowanych systemach, ale nadal są scenariusze w których będzie to trudne. To właśnie z tego powodu tak dużą rozwagę zalecam przy decyzji o wyborze **frameworków AI**. Choć tu decyzja należy wyłącznie od nas, tak łatwo się przekonać jak duży problem może stanowić oparcie całej aplikacji o rozwiązanie budowane na fundamentach, które wciąż się zmieniają.

Tylko co to oznacza w praktyce?

Programowanie jakie znaliśmy do tej pory uczyło nas projektowania architektury, która nie tylko zrealizuje założenia biznesowe, ale też nie będzie utrudniać dalszego rozwoju niezależnie od tego, w jaki sposób będzie rozwijał się produkt. Zazwyczaj jednak i tak większość komponentów nigdy się nie zmienia i z czasem okazuje się, że nawet gdy zachodzi potrzeba ich wymiany na inne, staje się to zbyt trudne ze względu na liczbę zależności czy po prostu ilość dedykowanej logiki.

W przypadku generatywnych aplikacji obowiązują nas podobne zasady, ale dynamika rozwoju samej aplikacji oraz zmiany otoczenia są tak duże, że coraz trudniej jest mówić o podejmowaniu decyzji na lata. Jednak z drugiej strony mówimy o potrzebie **bardzo szybkich iteracji**, których zakres nierzadko będzie obejmował to, co normalnie robiliśmy w ciągu kwartału bądź półrocza.

Choć nie mam bezpośredniej odpowiedzi na pytanie, **"jak należy projektować"** aplikacje zachowujące ogromną elastyczność i pozwalające na tak szybkie iterowanie nawet jeśli po drodze wymienimy dużą część logiki, tak wiele wskazuje na to, że nasza uwaga powinna skupić się na **"prymitywach"** (w kontekście architektury), a nie "funkcjonalnościach".

**Prymitywy:** to podstawowe, możliwie najprostsze elementy z których można zbudować bardziej złożone struktury.

Zatem przykładowo: podczas implementacji logiki dla funkcjonalności **czatu**, zwykle myślimy o niej jako o wymianie **wiadomości** pomiędzy **użytkownikiem**, a **asystentem**. Jest to więc wyspecjalizowana i raczej mało elastyczna struktura, która może znacznie utrudniać wprowadzenie interakcji pomiędzy agentami.

Jeśli jednak pomyślimy o tym w kategorii **zdarzeń** związanych z interakcją pomiędzy **aktorami**, to sama struktura przestaje nas tak bardzo ograniczać, ponieważ zdarzenia nie muszą dotyczyć wyłącznie wiadomości, a aktorem nie musi być użytkownik, ale także inny agent bądź sam system.

![Elastyczne schematy danych](https://cloud.overment.com/2026-03-16/ai_devs_4_primitives-50efe16a-f.png)

W takiej strukturze zdarzenia mogą obejmować również obsługę narzędzi, reasoning modelu czy nawet akcje, które nie są bezpośrednio powiązane z LLM API, ale są istotne z punktu widzenia samej interakcji, np. kompresja kontekstu bądź prośba o potwierdzenie akcji subagenta.

Innym przykładem mogą być **artefakty**, które widzieliśmy w lekcji **S03E05**. Natomiast w tym kontekście artefaktami nazywamy **metadane** reprezentujące różne formy treści generowane przez agentów. Mogą więc to być obrazy, pliki tekstowe czy binarne, ale również interaktywne interfejsy posiadające swój własny stan. Artefakt może być przypisany do użytkownika lub agenta oraz może być udostępniany między nimi. Także zamiast projektować oddzielne struktury danych dla obrazów czy dokumentów tekstowych, mamy po prostu artefakty różnych typów.

Analogiczny sposób myślenia możemy przenieść na pozostałe obszary aplikacji: front-end, back-end czy nawet samo planowanie interfejsu i same założenia biznesowe. Oczywiście **nie oznacza to, że w ten sposób zawsze musimy podchodzić do architektury** i warto zachować rozsądek w zbyt mocnym wybieganiu w przyszłość, która może nigdy nie nadejść. Ale w praktyce zdarza się, że "prosty czatbot" szybko zmienia się przynajmniej w agenta, a niekiedy też system wieloagentowy.

Podsumowując - obecnie projektowanie aplikacji stawia przed nami jeszcze więcej wyzwań ze względu na dynamiczny rozwój ekosystemu gen-AI. Możemy adresować je przede wszystkim przez podejmowanie mądrych decyzji projektowych, a tu bardzo pomocne bywają rozmowy z AI.

### Architektura dla czatbotów i agentów

Wspomniałem, że przy projektowaniu czatbotów wystarczy przechowywanie **konwersacji** oraz **listy wiadomości**. W kontekście bazy danych są to więc dwie, raczej proste tabele. Obecnie jednak niemal każdy czatbot jest agentem i widać to nawet po ChatGPT czy Claude, czyli najpopularniejszych obecnie aplikacjach do pracy z AI. Podobnie wygląda to z narzędziami do kodowania, gdzie mówimy już wyłącznie o agentach.

W lekcji **S02E04** omawialiśmy techniki projektowania kontekstu oraz przykłady architektury systemów wieloagentowych, takie jak Orchestrator, Mesh czy Blackboard. W praktyce raczej nie będziemy stosować ich w pełnej formie, lecz wykorzystamy różne ich elementy. Przykładem, który to obrazuje jest **05\_01\_agent\_graph**, który łączy w sobie koncepcje:

- **Orchestrator:** jest to po prostu agent wyposażony w narzędzia takie jak `delegate_task` czy `create_actor` z pomocą których zarządza zadaniami oraz pozostałymi agentami.
- **Blackboard:** to warstwa współdzielonego stanu zawierającego sesję, zdarzenia, zadania, relacje oraz artefakty, którymi agenci mogą zarządzać przez narzędzia którymi dysponują (np. write\_artifact)
- **Grafów (konkretnie DAG-ów):** relacje między zadaniami tworzą graf, a "scheduler" w postaci deterministycznej logiki rozwiązuje zależności między nimi, np. promuje zadania, których zależności zostały spełnione, oraz wstrzymuje te, które wciąż czekają na wykonanie pozostałych.
- **Zdarzeń:** każda zmiana stanu, np. utworzenie zadania, modyfikacja artefaktu czy wywołanie narzędzia, wysyła zdarzenie przez SSE (Server Side Events). W przykładzie są one wykorzystywane przez panel wizualizujący aktywności agentów, ale w praktyce będą przydatne na potrzeby obserwacji, ewaluacji czy wprowadzania guardrails.

UWAGA: Przykład 05\_01\_agent\_graph jest zaawansowany, a jego zrozumienie **nie jest wymagane** przy zaliczeniu zadań. Jednocześnie może okazać się bardzo interesujący i warto go przynajmniej uruchomić (wówczas pojawi się okno przeglądarki oraz przykładowe zadanie realizowane przez system).

Poniżej widzimy główne komponenty architektury tego agenta. Każdy z nich jest już nam znany, ponieważ widzieliśmy już agentów "zarządzających", współdzielony stan, subagentów czy pamięć. Tutaj największą różnicę stanowi **scheduler**, który pojawił się w przykładzie **03\_02\_events** pod nazwą "heartbeat", ale tam cały plan zadań i zależności był określany z góry. Natomiast plan jest **kształtowany dynamicznie** przez agenta zarządzającego. Mówimy więc tutaj o zdecydowanie bardziej elastycznej (ale mniej przewidywalnej) strukturze.

![Przykładowa architektura systemu agentowego opartego o grafy](https://cloud.overment.com/2026-03-18/ai_devs_4_agent_graph-91448bfb-c.png)

Zatem to agent zarządzający **tworzy** oraz **przydziela** zadania, ale to **scheduler** zarządza dalszym cyklem ich życia, dbając o rozwiązanie zależności, kolejność wykonania oraz wznowienie agentów po zakończeniu zadań.

Poniżej mamy wizualizację logiki **scheduler'a**. Widzimy na niej, że:

- pod uwagę zostają wzięte zadania, które albo **nie posiadają zależności**, albo **oczekują na wykonanie**, ponieważ ich zależności zostały spełnione.
- w danej rundzie, status tych zadań zmienia się na `in_progress` i są przekazywane do pętli przypisanego do nich aktora, który po wykonanej pracy zmienia ich status na `done` lub `blocked`. Natomiast status `waiting` zostaje ustalony automatycznie, gdy dany aktor **kończy pracę**, ale scheduler zauważa aktywność subagentów.
- po zakończeniu pętli aktorów uruchamiana jest kolejna runda.

![Scheduler oparty o graf](https://cloud.overment.com/2026-03-18/ai_devs_4_agent_dag-97db9952-6.png)

Po uruchomieniu przykładu uruchamia się testowe zapytanie o utworzenie wpisu na bloga na temat TypeScript. Schemat wykonania widoczny jest na wizualizacji poniżej, ale obejmuje:

- Utworzenie głównego aktora **Orchestrator** oraz głównego zadania.
- Pierwsza runda bierze pod uwagę główne zadanie oraz głównego aktora, który tworzy podrzędnego aktora **Researcher** oraz **deleguje** mu zadanie polegające na zebraniu materiałów. **Orchestrator** kończy swoją pracę, a **Scheduler** zmienia status głównego zadania na `waiting`.
- W drugiej rundzie **Researcher** przeszukuje Internet i tworzy **artefakt** "research-notes". Jego zadanie zmienia status na `done`.
- W trzeciej rundzie **Orchestrator** widząc zgromadzone informacje decyduje, że mamy komplet informacji, aby rozpocząć pisanie artykułu. Tworzy więc aktora **Writer** i **deleguje** mu przygotowanie artykułu, co zostaje wykonane **w tej samej rundzie**.
- W czwartej rundzie **Orchestrator** znowu zostanie wznowiony i widząc wszystkie wykonane pod-zadania uznaje, że główne zadanie zostało zrealizowane, więc zamyka je i kontaktuje się z użytkownikiem.

![Przykład działania logiki systemu agentowego wykorzystującego grafy](https://cloud.overment.com/2026-03-18/ai_devs_4_agent_graph_trace-16dd7be5-5.png)

Ten przykład pokazuje nam na jak różne sposoby możemy podejść do architektury agentów, balansując pomiędzy deterministyczną logiką kodu, a nieprzewidywalnym lecz elastycznym działaniem modeli językowych. Jednocześnie architektura którą tutaj mamy jest wyjątkowo elastyczna, ponieważ sprawdzi się zarówno do zwykłych rozmów z AI, jak i obsługi narzędzi oraz realizowania zadań nawet w nieco dłuższych horyzontach czasowych.

Natomiast przede wszystkim architektura, którą tutaj mamy, jest bardzo podatna na rozbudowę, a nawet na wymianę jej fundamentalnych elementów, wliczając w to providera AI oraz różne ustawienia narzędzi i aktorów (np. agentów). Dodawanie mechanik umożliwiających wykonywanie zadań w tle również wchodzi w grę, zarówno z zaangażowaniem człowieka, jak i przy jego ograniczeniu. W obu tych przypadkach pomocne będą zdarzenia emitowane przez system.

### Integracje z różnymi providerami

Budowanie generatywnych aplikacji zwykle będzie wiązało się z integrowaniem więcej niż jednego providera. Zazwyczaj wynika to z chęci skorzystania z unikatowych funkcjonalności. Przykładem mogą być najlepsze modele do edycji grafiki oferowane przez Gemini, bądź świetne modele do kodowania oferowane przez Anthropic. Jednak w takiej sytuacji skorzystanie z tych dwóch providerów od strony technicznej **nie stanowi dużego wyzwania**, ponieważ mówimy o zupełnie odrębnej logice.

Problem zaczyna się wtedy, gdy więcej niż jeden provider pojawia się **w tej samej logice**. Przykładowo jeden agent pracujący z modelem OpenAI, a drugi z modelem Anthropic. Wówczas musimy zadbać o warstwę **tłumaczeń**, która będzie odpowiednio **mapować zapytania**, a nie zawsze jest to takie oczywiste ponieważ:

- API różnią się strukturą, więc musimy zadbać o mapowanie. Na przykład wiadomość systemowa w OpenAI może być przekazana razem z pozostałymi wiadomościami, a w Anthropic musi to być oddzielne pole `system`. Natomiast w Gemini prompt systemowy musi trafić do `system_instruction`.
- Ustawienia modeli potrafią znacznie się różnić. Np. Anthropic i Gemini opierają **reasoning** modeli o tzw. `budget_tokens`, a OpenAI o tzw. `reasoning_effort`.
- API zwykle wymagają tzw. [Thought Signatures](https://ai.google.dev/gemini-api/docs/thought-signatures) w celu zachowania tokenów "reasoning". Sygnatura ta jest **wymagana** w Interactions API, ale tylko od Gemini w wersji 3 lub nowszej oraz tylko przy wywołaniu narzędzi i to tylko w bieżącej turze (!!!). API Anthropic również posiada swoje [Sygnatury](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#how-to-use-extended-thinking), które działają podobnie.

Lista różnic pomiędzy API jest bardzo duża i nie ma potrzeby wymieniać ich wszystkich, ponieważ wciąż obserwujemy zmiany w API. Na przykład jeszcze niedawno API Gemini nie pozwalało na stosowanie narzędzi z natywną funkcją Web Search, ale teraz jest to już możliwe. Natomiast nadal nie możemy przesłać wiadomości asystenta jako pierwszej do API Anthropic - takie ograniczenia sprawiają, że mapowanie API różnych dostawców potrafi sprawić mnóstwo problemów.

W tym miejscu można pomyśleć o trzech rozwiązaniach:

1. Dobrze znanym nam OpenRouter, którego ograniczenia już znamy
2. Bibliotekach lub frameworkach, np. [LiteLLM](https://www.litellm.ai/) czy [AI SDK](https://ai-sdk.dev/)
3. Własnej logice, dopasowanej do naszych potrzeb (oczywiście przygotowanej z pomocą AI)

Z doświadczenia mogę powiedzieć, że każde z tych podejść ma swoje zalety i wady:

- OpenRouter jest bardzo wygodny, ale wspiera tylko podstawowe funkcjonalności API. Poza tym w przypadku mapowania API oraz sygnatur wciąż zdarzają się tu rzadkie błędy.
- Biblioteki/Frameworki potrafią nas zablokować z dostępem do najnowszych funkcjonalności. Zdarzają się w nich także istotne błędy, które mogą ujawniać się tylko przy zaawansowanej logice przez co priorytet ich naprawienia jest niski.
- Własna logika daje najwięcej kontroli, ale też przekłada na nas cały ciężar. W tym przypadku warto określić **domyślny** format danych dla naszego systemu i tutaj obecnie najlepszą decyzją będzie Responses API ze względu na jego popularność.

Ostatecznie decyzję należy uzależnić od projektu i naszych potrzeb:

- Jeśli pracujemy wyłącznie z LLM i nie interesują nas inne funkcjonalności, OpenRouter jest dobrym wyborem.
- Biblioteki (np. AI SDK) mogą być dobrym wyborem i z czasem może się okazać, że będą najlepszą opcją o ile tylko nasz provider jest wspierany bądź mamy możliwość dodania własnego "adaptera" — tutaj jednak moje doświadczenie sugeruje, że należy zachować ostrożność.
- Dziś własna logika, szczególnie przy wsparciu AI oraz ewentualnie w połączeniu z oficjalnymi SDK wydaje się najlepszym rozwiązaniem — z tego podejścia korzystam w większości projektów.

Powyższe sugestie opierają się przede wszystkim o moje praktyczne doświadczenie z produkcji. Nie oznacza to, że są to jedyne słuszne opcje oraz, że za jakiś czas mogą przestać być aktualne.

Warto dodać, że o budowaniu własnej logiki nigdy bym nie wspomniał, gdyby nie fakt, że mamy do dyspozycji agentów do kodowania. Tworzenie jej od podstaw zwyczajnie kosztowałoby nas więcej, niż potencjalne korzyści. Natomiast teraz wystarczy umieścić pliki oficjalnych SDK providerów, których chcemy podłączyć oraz porozmawiać z agentem o głównych założeniach takich jak:

- jaka struktura API będzie dla nas domyślna. Tutaj musimy określić kształt zapytania oraz odpowiedzi, a także formatu strumieniowanych danych
- w jaki sposób będziemy określać, który provider powinien zostać aktywowany oraz jak będziemy mapować ustawienia (np. `reasoning_effort`)
- które z ustawień chcemy obsługiwać, ponieważ z dużym prawdopodobieństwem będzie nam zależało tylko na niektórych

Poniżej widzimy **koncepcyjną wizualizację** (czyli detale są bardzo ogólne) takiej logiki.

![Wsparcie dla wielu providerów](https://cloud.overment.com/2026-03-18/ai_devs_4_multi_provider-bcf2efbc-9.png)

Sam przykład takiej **spersonalizowanej** logiki, którą potencjalnie moglibyśmy uzyskać korzystając z frameworków można też przełożyć na inne obszary i wyciągnąć z tego wartościowe lekcje. No bo przed popularyzacją AI po prostu wybieraliśmy zestaw narzędzi z których chcemy skorzystać i kierowaliśmy się tam głównie kluczowymi funkcjonalnościami, które nam oferują. W zamian przyjmowaliśmy także pozostałe rozwiązania oferowane przez twórców.

Dziś jednak możemy pozwolić sobie na to, aby w przypadku narzędzi, które **nie mają stabilnych fundamentów** bądź **są jeszcze na etapie kształtowania**, podjąć decyzję o tym czy chcemy z nich korzystać czy zastąpimy je własną logiką. Oczywiście w tym miejscu możemy zastanowić się nad tym aspektami związanymi chociażby ze **wsparciem** tych projektów. Poza tym samodzielne budowanie i utrzymywanie logiki wydaje się mieć mały sens, ale takie podejście zwyczajnie **przestaje być aktualne w erze AI**. Tym bardziej, że nikt nie mówi tutaj o budowaniu od podstaw narzędzi i frameworków, które są z nami od lat.

Ostatecznie może się okazać, że wkrótce wśród narzędzi i frameworków AI wyłonią się kandydaci porównywalni chociażby z React / Vue / Angular czy Svelte. Jednak nawet w takiej sytuacji dobrze jest pozostać otwartym na **nowe możliwości, jakie daje nam generatywne AI** w kontekście programowania.

## Fabuła

![https://vimeo.com/1179947065](https://vimeo.com/1179947065)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze piąty!

Udało się dostarczyć jedzenie do wszystkich potrzebujących, a wszystko to dzięki Twojej pomocy. Gratuluję.

Rozmawiałem z Natanem na temat naszych dalszych planów. Przedstawiłem mu koncepcję naszego skoku w czasie i odwrócenia rzeczywistości, ale... chyba nie muszę mówić, że nie za bardzo uwierzył w te - jak to nazwał - 'brednie'. W tych czasach ludzie nie znają jeszcze zagadnień dyslokacji czasu i przyczynowości wstecznej. Ech ten XXI wiek.

Opracowaliśmy jednak plan, który pozwoli ocalić ludzkość na wypadek, gdyby skok jednak się nie udał. Natan wspomniał mi o mieście, które ma całkiem dobrą lokalizację i dostęp do wody pitnej. Uprawiają tam bydło, dostępne są pola uprawne, a jednocześnie, ktoś z Ruchu Oporu przy włamaniu do Systemu, wymazał to miejsce z mapy kraju. Jak się więc domyślasz, nie znajdziemy go tak łatwo.

Natan posiadał notatki dotyczące lokalizacji miasta ocalałych. Niestety wszystko to spłonęło razem z mieszkaniem Natana, jego sprzętem i całym miastem. Nie wszystko jednak stracone.

Dzięki Natanowi uzyskaliśmy dostęp do nadajnika nasłuchowego używanego przez Domatowo - miasto, w którym mieszka Natan... znaczy... mieszkał.

Nadajnik położony był poza granicami miasta, więc nadal jest funkcjonalny, a niszczycielom nie udało się go zniszczyć. Wyłapuje on cały sygnał radiowy w promieniu 200, a no może i nawet 250 kilometrów. Jest tam sporo szumu i zbytecznych informacji, ale niekiedy można tam natrafić na fragmenty rozmów i dokumenty członków ruchu oporu. Od czasu do czasu wpadnie tam także coś od operatorów Systemu, ale oni już niemal zrezygnowali komunikacji radiowej.

Wierzę, że jeśli odfiltrujesz z tego potoku to, co zbyteczne, a bliżej przyjrzysz się temu, co ma sens, pomożesz nam namierzyć lokalizację miasta ocalałych.

Plan awaryjny, który opracowaliśmy, zakłada, że po namierzeniu tego miejsca przetransportujemy tam wszystkich ludzi z pozostałych miast.

To miejsce stanie się nową stolicą naszego kraju i tam wybuchnie pierwsze powstanie przeciwko Zygfrydowi. Wszystko to będzie się działo równolegle z naszą misją.

Wierzę, że ryzyko, które podejmujemy, okaże się zbyteczne i skok, który planujemy od tygodni, rozwiąże wszelkie problemy, i już nigdy więcej nie usłyszymy imienia Zygfryd.

## Zadanie praktyczne

Twoim zadaniem jest przechwycić i przeanalizować materiały z radiowego nasłuchu, a następnie przesłać do Centrali końcowy raport na temat odnalezionego miasta. W eterze panuje chaos: część komunikatów to zwykły szum, część to tekstowe transkrypcje, a czasem trafisz też na pliki binarne przekazane jako dane encodowane w Base64.

Nazwa zadania: **radiomonitoring**

Odpowiedź wysyłasz do: <https://hub.ag3nts.org/verify>

Cała komunikacja odbywa się przez **POST** na `/verify` w standardowym formacie:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "radiomonitoring",
  "answer": {
    "action": "..."
  }
}
```

### Jak działa zadanie

Najpierw uruchamiasz sesję nasłuchu, potem wielokrotnie pobierasz kolejne przechwycone materiały, a na końcu wysyłasz raport końcowy.

#### 1. Start sesji

Na początku wywołaj:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "radiomonitoring",
  "answer": {
    "action": "start"
  }
}
```

To przygotowuje sesję nasłuchu i ustawia pulę materiałów do odebrania.

#### 2. Nasłuchiwanie

Kolejne porcje materiału pobierasz przez:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "radiomonitoring",
  "answer": {
    "action": "listen"
  }
}
```

W odpowiedzi możesz dostać jeden z dwóch głównych typów danych:

- tekstową transkrypcję komunikatu głosowego w polu `transcription`
- plik binarny opisany metadanymi i przekazany jako `attachment` w Base64

Przykład odpowiedzi tekstowej:

```json
{
  "code": 100,
  "message": "Signal captured.",
  "transcription": "fragment przechwyconej rozmowy radiowej"
}
```

Przykład odpowiedzi z plikiem:

```json
{
  "code": 100,
  "message": "Signal captured.",
  "meta": "application/json",
  "attachment": "BASE64...",
  "filesize": 12345
}
```

Zwróć uwagę na kilka rzeczy:

- nie każda odpowiedź będzie przydatna, bo część materiału to zwykły radiowy szum
- pliki binarne mogą mieć sensowną zawartość, ale mogą też być kosztowne w analizie
- zakodowanie binarki w Base64 dodatkowo zwiększa rozmiar danych, więc bezpośrednie przekazanie całości do LLM-a może być bardzo drogie!
- rozsądne rozwiązanie zwykle zaczyna się od decyzji programistycznej: co da się odsiać, co zdekodować i przeanalizować lokalnie, a co rzeczywiście wymaga modelu

Gdy materiał się skończy, system poinformuje Cię, że masz już wystarczająco dużo danych do analizy.

### Co musisz ustalić

Na podstawie zebranych materiałów przygotuj końcowy raport zawierający:

- `cityName` - jak nazywa się miasto, na które mówią "Syjon"?
- `cityArea` - powierzchnię miasta zaokrągloną do dwóch miejsc po przecinku
- `warehousesCount` - liczbę magazynów jaka jest na Syjonie
- `phoneNumber` - numer telefonu osoby kontaktowej z miasta Syjon

Ważna uwaga dotycząca `cityArea`:

- wynik musi mieć dokładnie dwa miejsca po przecinku
- chodzi o prawdziwe matematyczne zaokrąglenie, a nie o obcięcie wartości
- format końcowy ma wyglądać jak `12.34`

#### 3. Wysłanie raportu końcowego

Gdy ustalisz wszystkie dane, wyślij:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "radiomonitoring",
  "answer": {
    "action": "transmit",
    "cityName": "NazwaMiasta",
    "cityArea": "12.34",
    "warehousesCount": 321,
    "phoneNumber": "123456789"
  }
}
```

### Praktyczna wskazówka

To zadanie jest przede wszystkim ćwiczeniem z mądrego routingu danych. Podczas nasłuchiwania możesz otrzymywać DUŻE porcje danych binarnych. Wrzucenie takich danych bezpośrednio do modelu językowego może wygenerować bardzo duże koszty. W praktyce przyda Ci się programistyczny router, który najpierw oceni, z jakim materiałem ma do czynienia, a dopiero potem zdecyduje, czy coś analizować kodem, zdekodować lokalnie, odfiltrować jako mało istotne, czy dopiero skierować do odpowiednio dobranego modelu. Być może warto też użyć różnych modeli do różnych typów danych.

Najbardziej opłacalne podejście do tego zadania to nie "jeden wielki prompt", tylko sensowny pipeline:

- odbierasz materiał
- rozpoznajesz, czy to tekst, szum czy binarka
- dla binarki podejmujesz decyzję, czy analizować ją kodem, zdekodować lokalnie, czy dopiero potem przekazać dalej
- wybrane, wartościowe dane kierujesz do odpowiednio dobranego modelu

Jeśli dobrze rozplanujesz taki router, ograniczysz liczbę tokenów i koszt całej operacji, a właśnie to jest tutaj jednym z najważniejszych celów.

## Linki

- [LiteLLM](https://www.litellm.ai/)
- [AI SDK](https://ai-sdk.dev/)
- [Thought Signatures (Gemini)](https://ai.google.dev/gemini-api/docs/thought-signatures)
- [Extended Thinking Signatures (Anthropic)](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#how-to-use-extended-thinking)
