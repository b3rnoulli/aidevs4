---
title: S03E03 — Kontekstowy feedback wspierający skuteczność agentów
space_id: 2476415
status: scheduled
published_at: '2026-03-25T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/support-1773911487.png'
circle_post_id: 30844667
---
## Film do lekcji

![https://vimeo.com/1175525315](https://vimeo.com/1175525315)

Generatywne aplikacje mogą być wysoce spersonalizowane i nie chodzi wyłącznie o dopasowanie do preferencji użytkownika. Zachowanie agentów może dynamicznie dopasowywać się do otoczenia oraz reagować na zdarzenia w sposób, który może przez niektórych być odbierany jako "samoświadomość" lub bardziej jej sprytną iluzję. Nie chodzi w tym jednak tylko o imponujące sztuczki, lecz wysoką użyteczność.

Co ciekawe, mechaniki, które będziemy omawiać są raczej dość proste. Trudność zwykle będzie dotyczyć tylko dostępu do informacji oraz przekazania jej tak, aby zachowanie agenta było możliwie naturalne. Poza tym, nie będzie nam chodziło wyłącznie o bezpośrednie interakcje z użytkownikiem, lecz także działania podejmowane bez jego udziału.

## Stan i informacje zwrotne z otoczenia

W lekcji **S02E01** mówiliśmy o technikach prowadzenia kontekstu konwersacji, gdzie agent samodzielnie **odkrywał** stan otoczenia poprzez posługiwanie się narzędziami, bądź był o nim informowany poprzez metadane programistycznie dodawane do wiadomości użytkownika. W ten sposób agent zyskiwał dostęp do zmieniającego się stanu otoczenia, co wpływało na jego zachowanie i skuteczność działania.

Tam jednak mieliśmy do czynienia z działaniem reaktywnym, bo otoczenie miało wpływ na agenta, ale tylko podczas trwającej interakcji z użytkownikiem. Natomiast teraz będzie nam zależało na mechanikach, które w pełni zintegrują agenta z otoczeniem i nawet w pewnym stopniu uniezależnią go od bezpośrednich działań człowieka. Jednocześnie ich obecność nie będzie wykluczała interakcji z nim.

Autonomiczne działania systemu mogą zostać wywołane na kilka sposobów, wśród których są:

- **Wiadomości:** przesłane przez człowieka, bądź innych agentów
- **Hooki:** czyli zdarzenia wewnątrz aplikacji (np. działania subagentów)
- **Webhooki:** czyli zdarzenia w zewnętrznych usługach (np. zdarzenie w kalendarzu)
- **Cron:** czyli zdarzenia wywołane poprzez czas / daty (np. codzienne raporty)
- **Heartbeat:** czyli regularne wywołania w celu weryfikacji stanu systemu oraz ewentualnego podjęcia akcji jeśli coś wymaga uwagi

![Autonomiczne wyzwalacze w systemach agentowych](https://cloud.overment.com/2026-02-23/ai_devs_4_triggers-a6c3a053-a.png)

Powyższe wyzwalacze powinny wyglądać dość znajomo, ponieważ pojawiły się już w różnych formach w dotychczasowych lekcjach. Jednak tym razem spojrzymy na nie przez pryzmat autonomii, interakcji z otoczeniem oraz współpracy z człowiekiem. Weźmiemy także pod uwagę wszystko, o czym mówiliśmy do tej pory o zarządzaniu kontekstem, budowaniu narzędzi oraz logiki agentów.

Uruchamianie akcji w wyniku wewnętrznych bądź zewnętrznych zdarzeń nie jest niczym nowym w programowaniu. Zwykle jednak mówimy tu o **niezależnych akcjach** wywoływanych z określonymi argumentami. Dlatego w kontekście agentów również możemy myśleć o nich w podobny sposób. Choć po części nie ma w tym nic złego, tak możliwości jakie mamy teraz do dyspozycji są zdecydowanie większe. Główną różnicą stanowi tu fakt, że system agentowy **może posiadać jeden punkt "wejścia"** i dynamicznie dostosować się do zleconego zadania oraz bieżącego stanu otoczenia.

![Jeden punkt wejścia w systemie agentowym](https://cloud.overment.com/2026-02-23/ai_devs_4_single_entry-b393496a-4.png)

Taka konfiguracja umożliwia przesyłanie automatycznych wiadomości zapisanych w języku naturalnym. Ich treść może być budowana poprzez kod, bądź pochodzić z innych systemów agentowych. W obu przypadkach opisane zadania zostają zinterpretowane przez system oraz powiązane z dostępnymi danymi, a następnie wykonane. Mowa więc tu o niesamowitej elastyczności systemu i tym samym użyteczności całego systemu.

Domyślnie jednak **każda taka akcja to nowa sesja**, więc system nie widzi bezpośrednich powiązań między zdarzeniami. Do pewnego stopnia jest to użyteczne, ponieważ bez potrzeby powinniśmy raczej unikać zanieczyszczania kontekstu niepotrzebnymi danymi. Pytanie jednak co stanie się, gdy **główna sesja** systemu będzie posiadać informacje o tym, co dzieje się w tle? Jak w tej sytuacji zdecydować, które zdarzenia mają współdzielić sesję, a które nie?

W tej chwili można powiedzieć "**to zależy**" i pójść dalej. Ale zamiast to robić, spróbujmy przyjrzeć się nieco bliżej sytuacji w której **główna sesja** użytkownika z agentem pozostaje **"nieskończona"** oraz **proaktywna**. Wówczas architektura będzie prezentować się następująco:

![Przykład mechanizmu proaktywnych działań agenta](https://cloud.overment.com/2026-02-23/ai_devs_4_proactivity-127e7b77-7.png)

"Trwałość" sesji zapewniona jest tutaj przez mechaniki kompresji kontekstu (np. omawiane Observational Memory). Natomiast co określony czas system otrzymuje dodatkową wiadomość z prośbą o przeczytanie pliku **tasks.md** oraz wykonanie zawartych w nich poleceń. Jeśli żadne z nich nie wymaga działania, agent może **pominąć** dalsze wykonanie i z perspektywy użytkownika nic się nie wydarzy. W przeciwnym razie zadania zostaną wykonane, więc sesja zostanie wznowiona **przez agenta** w sposób proaktywny.

Plik **tasks.md** musi więc zawierać najważniejsze aktywności z punktu widzenia użytkownika, które jednocześnie będą wymagały **kontekstu** z głównego wątku. Jego treść będzie więc raczej ustalana ręcznie, aczkolwiek agent może mieć do niego dostęp, aby zarządzać nim w imieniu użytkownika. Poszczególne wpisy mogą dotyczyć powtarzalnych akcji, takich jak informowanie o nadchodzących wydarzeniach czy najważniejszych wiadomościach, ale w bardziej spersonalizowany sposób niż klasyczne powiadomienia.

Agent może uzależnić je od bieżącego otoczenia (np. czasu czy lokalizacji) bądź od tego, czym użytkownik w danej chwili się zajmuje (np. statusu jego komputera, otwarte programy czy zakładki w przeglądarce). Nie chodzi też wyłącznie o samą informację, lecz możliwość podjęcia związanych z nią akcji.

Poniżej mamy dwa przykłady sytuacji w których agent proaktywnie kontaktuje się z użytkownikiem, podejmując przy tym działania w oparciu o dostępne zasoby. Pierwszy scenariusz bierze pod uwagę **godzinę** oraz **wzmiankę o priorytecie**. Agent sprawdza więc postęp zadań w Linear oraz termin realizacji projektu. Na tej podstawie sugeruje optymalizację działań w celu zwiększenia szansy na realizację celu. Z kolei drugi scenariusz opiera się o bieżącą lokalizację użytkownika i wzmiankę o spotkaniu, np. z klientem. To kieruje agenta do wczytania profilu na temat tej osoby oraz sprawdzenia dostępności w kalendarzu.

![Przykłady proaktywnych zachowań agenta](https://cloud.overment.com/2026-02-23/aidevs_4_heartbeat_triggers-9540b47c-7.png)

Nawet te dwa przykłady pokazują, jak istotny jest dostęp do metadanych użytkownika. Co prawda nie musimy od razu mówić tu o lokalizacji, ale nawet skanowanie podłączonych usług i aplikacji może obejmować dane przydatne w proaktywnych mechanikach agentów. Zresztą te same zasady można zastosować nie tylko w odniesieniu do ludzi, ale także w interakcjach między agentami.

## Przykłady interakcji z niewystarczającym kontekstem

Zarówno przy bezpośredniej jak i pośredniej interakcji pomiędzy człowiekiem a systemem agentowym będzie dochodziło do sytuacji w których dostępny kontekst będzie **niewystarczający**. Chodzi tu zarówno o pospiesznie pisane czy dyktowane wiadomości użytkownika, ale także dane pochodzące z pamięci długoterminowej czy narzędzi. Aby zaadresować ten problem, będzie zależało nam na stworzeniu przestrzeni agentom do **"połączenia kropek"**.

Poniżej mamy wizualizację logiki agenta z przykładu **03\_03\_calendar**. Dysponuje on narzędziami takimi jak **kalendarz, mapa** oraz **pamięć**, posiada dostęp do Internetu oraz możliwość skontaktowania się z użytkownikiem. Poza tym ma także stały dostęp do lokalizacji oraz pogody.

Choć nie ma przeszkód, aby taki agent działał w interfejsie czatu, tak w obecnej formie sprawdzi się świetnie działając całkowicie w tle. Poza tym, podobnie jak wcześniej, mówimy zarówno o reagowaniu na zdarzenia (np. zamiana zgłoszenia ze strony na wpis w kalendarzu), jak i działaniu proaktywnym (np. reagowanie na zbliżające się wydarzenia). W dostępnych dla niego zasobach jasno widzimy, że specjalizuje się w zarządzaniu kalendarzem, ale bardziej w roli asystenta osoby z działu sprzedaży obejmującej spotkania fizycznie z klientami.

![Przykład interakcji sterowanej kontekstem](https://cloud.overment.com/2026-02-23/ai_devs_4_context_driven-6dae2a3a-a.png)

Po uruchomieniu przykładu **03\_03\_calendar** aktywuje się pierwsza faza **dodawania wydarzeń**. Na potrzeby prezentacji pomiędzy wywołaniami narzędzi dochodzi do symulacji upływu czasu czy zmian lokalizacji. Agent łączy te informacje ze sobą, tworząc wpisy w kalendarzu uzupełnione o dane kontaktowe i konkretne adresy. Dochodzi więc tutaj do **wzbogacenia** oryginalnej wiadomości, co zwiększa jej wartość w kontekście dalszego przetwarzania. Potem następuje druga faza w której ponownie ma miejsce symulacja zmian otoczenia na które agent ma reagować, wysyłając rozbudowane powiadomienia i wskazówki.

> Przykład 03\_03\_calendar nie uwzględnia bezpośredniego połączenia z kalendarzem czy mapą, ale można skorzystać z serwerów MCP [Google Calendar](https://github.com/iceener/google-calendar-streamable-mcp-server/tree/main/src) oraz [Google Maps](https://github.com/iceener/maps-streamable-mcp-server) z mojego publicznego repozytorium.

![Przykład działania kontekstowego agenta](https://cloud.overment.com/2026-02-23/ai_devs_4_context_driven_runtime-4b9fc15f-9.png)

Agenci tacy jak ten mają potencjał działać całkowicie "w tle". Taka forma niesie ze sobą szereg korzyści, ponieważ mówimy tu o wartości dostarczanej użytkownikowi przy minimalnym lub zerowym zaangażowaniu z jego strony. Odpowiednio zaprojektowany system z tej kategorii ma potencjał, by **ustandaryzować i podnieść jakość procesów**, na przykład marketingowych lub sprzedażowych. Po prostu wiązanie ze sobą szczątkowych informacji, które początkowo są rozproszone, stanowi realną wartość dla biznesu.

Jednocześnie w dużym stopniu eliminujemy tu problemy związane z bezpieczeństwem informacji, aczkolwiek w powyższym przykładzie jest jeden wyjątek w postaci **tworzenia wydarzenia**. Na tym etapie może dojść do pomylenia adresów uczestników spotkania, więc jeśli w danym wpisie znajdzie się nazwa bądź opis zawierające poufne informacje, to będzie oznaczało to problemy. Ale jeśli będziemy mieć to na uwadze, to interfejs może w deterministyczny sposób zarządzać kontaktami i wówczas ten etap procesu nie będzie odbywał się po stronie agenta.

Przy projektowaniu agentów, którzy z założenia będą działać bez aktywnego udziału ze strony człowieka, nie eliminuje potrzeby zaprojektowania interfejsu dla sytuacji w których autonomiczna akcja nie będzie możliwa. Konflikty nazw, brakujące dane czy zwykłe błędy integracji będą z pewnością będą miały miejsce i nie możemy zakładać inaczej. Z drugiej strony możemy też nie myśleć o takich rozwiązaniach **defensywnie**, lecz **ofensywnie**. Czyli zamiast zastanawiać się tylko nad tym, gdzie system będzie mieć problemy, możemy pomyśleć także o tym, z jakich opcji możemy skorzystać, aby przenieść go na wyższy poziom. Tutaj dobrym przykładem może być interfejs **głosowy**, który nawet w prostej formie interakcji Speech to Text - Text to Speech może okazać się bardzo użyteczny.

## Rola feedbacku w skuteczności działania agentów

Działanie agentów może uwzględniać informacje zwrotne, które z czasem sprawiają, że z czasem stają się coraz lepsi w wykonywanych zadaniach. Co więcej, nie musimy mówić tu o rozbudowanym systemie pamięci, ale prostych zasadach, którymi będzie kierować się wyspecjalizowany agent. Dobrym przykładem może być system mający na celu **gromadzenie informacji** z wybranych źródeł, na przykład stron Internetowych.

Rola autonomicznych systemów w obszarze poruszania się po Internecie zdecydowanie się zmienia. Jeszcze jakiś czas temu mówiło się o bezwzględnych blokadach agentów (np. [AI Labyrinth](https://blog.cloudflare.com/ai-labyrinth/)) które odgrywają ważną rolę ze względu na różnego rodzaju nadużycia, ale też utrudniają funkcjonowanie w normalnych warunkach. Dziś natomiast narracja zmierza w kierunku traktowania ich "na równi" z użytkownikami, np. w kontekście [Markdown for Agents](https://blog.cloudflare.com/markdown-for-agents/) zaproponowanego przez Cloudflare czy [WebMCP](https://developer.chrome.com/blog/webmcp-epp) zaproponowanego przez Google Chrome.

Nadal jednak powszechne są sytuacje w których agent musi **nawigować po stronach www** bądź obsługiwać systemy nieposiadające API. Przykładem może być platforma Goodreads, która kilka lat temu wyłączyła możliwość rejestrowania nowych kont developerów. Jedyną opcją jest więc utworzenie agenta zdolnego do nawigowania po strukturze serwisu. Tutaj w przypadku powtarzalnych zadań, które mają działać na relatywnie dużej skali, można rozważyć zbudowanie bota **niebędącego pełnoprawnym agentem** i nie zawsze będziemy potrzebowali do tego LLM.

Klasyczne boty nie sprawdzą się jednak w każdym przypadku. W takich sytuacjach możemy sięgnąć po agenta AI posługującego się przeglądarką, z pomocą narzędzi takich jak Playwright bądź Puppeteer. W przypadku gdy będziemy chcieli zrobić to na większej skali, możemy rozważyć platformy takie jak [Browserbase](https://www.browserbase.com/) bądź [kernel.sh](https://kernel.sh/).

W przykładzie **03\_03\_browser** znajduje się agent wyposażony w narzędzia do interakcji z przeglądarką przez Playwright oraz z systemem plików. W katalogu **instructions** możemy umieścić informacje na temat strony, jej struktury czy nawet skrypty playwright do wykonywania konkretnych akcji. Taki dokument znacznie zwiększy skuteczność agenta, ponieważ nie będzie potrzeby odkrywania serwisu za każdym razem od nowa. Następnie

> UWAGA: do uruchomienia przykładu w naszym systemie **musi być zainstalowany** Chromium. Aczkolwiek powinno wydarzyć się to automatycznie przy instalacji zależności przez polecenie **npm install**.

Agent podczas działania będzie popełniał różnego rodzaju błędy, a te automatycznie będą przekładać się na **sugestie** dotyczące możliwości **wykonania zrzutu ekranu** czy **zapisania notatek** na potrzeby przyszłych operacji. Mówimy więc tu o **informacji zwrotnej**, która ma na celu zwiększenie skuteczności nie tylko w obrębie bieżącej sesji, ale w ramach całej domeny, np. goodreads.com.

![Przykład agenta pobierającego informację przez www](https://cloud.overment.com/2026-02-24/ai_devs_4_browser-627d7a9b-0.png)

Taki agent mógłby zostać także rozbudowany o możliwość **wykonywania kodu**. Wówczas nauka może obejmować **tworzenie automatyzacji** dla powtarzalnych aktywności. W podobny sposób możemy rozwijać praktycznie każdego agenta, bo wszędzie tam, gdzie możliwe jest uproszczenie realizacji zadań bądź nawet całkowite pominięcie LLM, powinniśmy to rozważyć.

Agent **03\_03\_browser**, w przeciwieństwie do prostych scraperów, może nawigować po stronach wymagających logowania. W tym celu należy uruchomić polecenie **npm run login** i przejść, na przykład, na wspomniane goodreads.com oraz zalogować się na swoje konto. Po zamknięciu przeglądarki sesja zostanie utrzymana, a agent będzie mógł poruszać się po stronie w naszym imieniu. Wówczas gdy uruchomimy skrypt **npm run start**, możemy przesłać zapytanie: **List books written by Jim Collins and save them in readings.md** a agent wykona dla nas to zadanie.

![Przykład działania agenta do nawigacji po serwisie Goodreads](https://cloud.overment.com/2026-02-24/ai_devs_4_browser_runtime-727cae04-3.png)

Powyższa logika obejmuje także sytuacje, w których zachodzi konieczność pobrania treści strony, co przy dłuższych materiałach szybko przepełnia okno kontekstowe. Dlatego narzędzia mają ustawione limity, po których przekroczeniu **treść strony jest zapisywana w pliku**, a agent może ją przeszukać. Alternatywnie, w takim przypadku moglibyśmy uruchomić **subagenta**.

Mechanizmy feedbacku i uczenia mogą być powiązane z konkretnymi narzędziami, a nawet wyłącznie z wybranymi kategoriami błędów. W przypadku tego agenta nie mówimy jednak tylko o statycznych "wskazówkach", lecz także o podejmowaniu dodatkowych działań, które dostarczają dodatkowego kontekstu. Dodatkowo logika uwzględnia polecenie **zachęcające** agenta do zapisywania wniosków z ostatnich błędów, aby uniknąć ich w przyszłości.

![Mechaniki nauki i feedbacku](https://cloud.overment.com/2026-02-24/ai_devs_4_learning_mechanics-3dde467f-2.png)

## Przestrzeń pomiędzy wywoływaniem narzędzi

Działanie agentów opiera się na pętli, w której uruchamiane są kolejne kroki. Przykład agenta posługującego się przeglądarką pokazuje, że każdy etap może uwzględniać dodatkową logikę, wpływającą albo na dalszy przebieg pracy bądź na zewnętrzne procesy. Zwykle mówimy tutaj o koncepcji generycznych **hooków**, czyli funkcji wywoływanych na poszczególnych etapach, na przykład:

- **onStart:** agent rozpoczyna pracę
- **onStepStart:** agent rozpoczyna kolejny krok
- **onStepFinish:** agent kończy dany krok
- **onToolCallStart:** agent rozpoczyna wywołanie narzędzia
- **onToolCallFinish:** agent kończy wywołanie narzędzia
- **onFinish:** agent kończy pracę

Przykłady powyższych hooków pochodzą z [AI SDK](https://ai-sdk.dev/docs/reference/ai-sdk-core/generate-text#experimental_on-tool-call-finish.on-tool-call-finish-event.output) i jest to raczej podstawowa lista. Patrząc na projekty agentów takich jak [Pi](https://github.com/badlogic/pi-mono) , hooki mogą dotyczyć także **strumieniowania**, **budowania kontekstu**, **modyfikacji sesji** (np. jej kompresji), **aktywności użytkownika** czy **statusów agentów**.

Hooki powinny posiadać dostęp do bieżącego stanu interakcji oraz informacji na temat sesji. Wówczas pozwala nam to na emisję zdarzeń bądź bezpośrednie wywoływanie dodatkowych akcji. Jednym z najprostszych przykładów jest **generowanie nazwy** dla bieżącej sesji, co możemy zaobserwować na przykład w ChatGPT, gdzie już po przesłaniu pierwszej wiadomości, wpis w historii zmienia nazwę z "New Chat" na wariant opisujący kontekst konwersacji.

W przykładzie **03\_03\_language** mamy implementację agenta pełniącego rolę **nauczyciela języka angielskiego** wyposażonego w narzędzia do analizy i generowania nagrań audio. Po jego uruchomieniu możemy poprosić agenta o przesłuchanie nagrania, na przykład "**Please feedback me input/example-day-1.wav**".

Agent w pierwszej kolejności **wczyta profil użytkownika**, a następnie odsłucha nagranie z pomocą Gemini API, które umożliwia nie tylko transkrypcję, ale także wychwycenie różnych aspektów związanych z wymową czy stylem wypowiedzi. Na tej podstawie powstają notatki zapisywane w ramach sesji oraz profilu dotyczące **popełnionych błędów** oraz **transkrypcja**, a także wstępny feedback.

Następnie agent **generuje feedback** w formie audio, korzystając z **Gemini Live** dzięki czemu może przeanalizować zarówno **tekst** jak i **nagranie** użytkownika, generując w odpowiedź w formacie **audio** oraz tekstu. Mamy więc tu do czynienia z interakcją **text + audio input -> text + audio output**.

W związku z tym, że w całej interakcji istotne jest także **zapisanie postępów** oraz **aktualizacja profilu**, agent wykorzystuje serię hooków:

- **beforeToolCall**: w przypadku wywołania narzędzia **listen** automatycznie zapisuje **ścieżkę do pliku audio**, którego dotyczy dana sesja.
- **afterToolResult**: aktualizuje postępy analizy, zmieniając flagi poszczególnych etapów **listen\_done, feedback\_done, session\_saved**. W sytuacji gdy wszystkie flagi zostają zaliczone, stan zostaje zresetowany, co pozwala przejść do kolejnej tury i analizy kolejnych nagrań
- **beforeFinish**: pełni rolę strażnika sprawdzającego czy wszystkie wymagane kroki analizy zostały ukończone i jeśli tak nie jest, to automatycznie prosi agenta o ich wykonanie. Wyjątek stanowi sytuacja w której **liczba dopuszczalnych kroków jest przekroczona** bądź **przy wywołaniu narzędzi wystąpił jakiś błąd**.

Jasne jest więc tutaj, że rola hooków nie ogranicza się jedynie do subtelnych akcji realizowanych w tle, ponieważ mogą one brać czynny udział w podnoszeniu skuteczności agenta oraz pilnowaniu procesu.

Logika agenta wygląda więc następująco:

![Architektura agenta do nauki angielskiego](https://cloud.overment.com/2026-02-24/ai_devs_4_teacher-59bb9c1d-1.png)

W przypadku tego agenta kluczowe jest zapisywanie postępów oraz wykorzystywanie ich podczas kolejnych sesji, ponieważ bezpośrednio wpływa to na proces personalizacji feedbacku. Co prawda sprawia to, że agent zostaje bardzo mocno wyspecjalizowany w tym konkretnym zadaniu, ale raczej nie stanowi to problemu bo nie każdy agent musi być uniwersalny.

Oczywiście w bardziej produkcyjnym kontekście mówilibyśmy tu o zastosowaniu interfejsu, który prawdopodobnie opierałby się całkowicie o interakcję **w czasie rzeczywistym** prowadzoną w **formacie audio**. Aczkolwiek też nic nie stoi na przeszkodzie, aby takie sesje odbywały się asynchronicznie i wówczas użytkownik otrzymywałby jedynie powiadomienia dotyczące **zadań** takich jak nagranie wiadomości opowiadającej o tym jak spędził dzień, albo zrelacjonowaniu swojej pracy.

Na uwagę zasługuje tutaj także fakt, że narzędzia **listen** oraz **feedback** po uruchomieniu wywołują **dodatkowe zapytania API** realizowane z pomocą modeli wyspecjalizowanych w analizie bądź generowaniu audio. Sytuacja w której narzędzia muszą wywołać zapytania API jest dość często spotykana i z tego powodu Model Context Protocol uwzględnia tzw. **[Sampling](https://modelcontextprotocol.io/specification/2025-11-25/client/sampling)** pozwalający Serwerowi MCP na wywołania API realizowane po stronie klienta. Jest to zatem **odwrócona komunikacja**, która niestety jest bardzo rzadko wspierana.

## **Wsparcie ze strony człowieka**

Projektowanie rozwiązań AI zwykle stawia przed nami oczekiwania i wyobrażenia o pełnej autonomii. Na podstawie dzisiejszej lekcji widzimy, że stosując nawet relatywnie proste mechaniki feedbacku, obserwacji, wyzwalaczy czy łączenia z otoczeniem możliwe jest uzyskanie **proaktywnych** działań. Ich odpowiednie wdrożenie będzie miało bezpośredni wpływ na pozytywne **doświadczenia użytkownika (UX)** ale też może przełożyć się na **skuteczność działania agenta**.

To wszystko jeszcze bardziej przesuwa nasze wyobrażenia w stronę systemów zdolnych do odnalezienia się w dowolnej sytuacji. Jednak bardzo szybko przekonamy się, że **złożoność** otaczającego świata, nawet po zawężeniu specjalizacji do całkiem prostych procesów, jest bardzo duża. Warto więc już na wstępnym etapie projektowania założeń oraz wstępnych wersji (np. MVP) uwzględnić rolę człowieka oraz aktywności wymagane po jego stronie. Korzystanie z mechanik takich jak hooki, webhooki czy heartbeat może w tym kontekście bardzo pomóc, ponieważ jest tam miejsce nie tylko na dodatkowe akcje systemu, ale także kontakt z człowiekiem. Przykładowo:

- Hook rozpoczynający sesję bądź wywołanie narzędzia może obejmować weryfikację po stronie człowieka. Taka mechanika powszechnie występuje w kontekście **potwierdzenia niezaufanej akcji**, jednak w praktyce może obejmować także uzupełnienie brakujących informacji czy wymagających rozstrzygnięcia.
- System może samodzielnie przeanalizować podjęte działania przed zakończeniem sesji i, w określonych przypadkach, podjąć decyzję o potrzebie wsparcia ze strony człowieka albo po prostu poinformować go o statusie realizacji.

Działanie systemu może też obejmować konkretne wymagania ze strony człowieka, które muszą zostać podjęte "przed" lub "po". Przykładowo osoba pracująca ze wspomnianym agentem do nauki języków może być poinformowana o roli **jakościowego nagrania** oraz potrzebie **zaangażowania** w jego treść, ponieważ bez tego nawet najlepsze instrukcje i modele nie będą w stanie wygenerować wartościowego feedbacku.

Choć takie przykłady mogą brzmieć banalnie, tak w praktyce problemy z działaniami agentów bardzo często leżą po stronie użytkowników, którzy z różnych powodów pracują z nimi w nieodpowiedni sposób. Zaadresowanie tych kwestii na poziomie komunikacji produktu czy onboardingu może znacząco wpłynąć na odbiór naszych rozwiązań oraz na skuteczność ich działania. Musimy więc potraktować te kwestie na równi z detalami architektury agentów i aspektów technicznych.

## Fabuła

![https://vimeo.com/1175524674](https://vimeo.com/1175524674)

## Transkrypcja filmu z Fabułą

"Dzięki, Numer Piąty, za ogarnięcie problemu z niedziałającym oprogramowaniem. Teraz wszystko działa poprawnie.

Nasi technicy potwierdzili, że testy oprogramowania także przechodzą poprawnie, więc wgraliśmy przygotowany przez Ciebie soft do realnego urządzenia.

Mamy teraz jednak pewien problem, ponieważ urządzenie do sterowania chłodzeniem znajduje się bardzo niebezpiecznie blisko reaktora, a jak wiesz, działał on już przez niemal cały dzień. Nie możemy więc tam wysłać człowieka ze względu na podwyższony poziom radiacji. Aby zainstalować to urządzenie, posłużymy się robotem.

I tutaj potrzebna jest Twoja pomoc, bo kto jak nie Ty mógłby tego robota zaprogramować? Zadanie wydaje się trywialne, bo wystarczy tylko zawieźć moduł sterowania chłodzeniem w pobliże reaktora i umieścić go w specjalnym slocie, ale po drodze znajdują się elementy rdzenia reaktora, które cały czas są w ruchu. Musimy więc tak zaprogramować robota, aby nie dotknął żadnego z tych elementów.

Mamy trochę tych robotów transportujących na stanie, ale proszę Cię, nie nadwyrężaj naszego budżetu i postaraj się to zrobić raz a dobrze. Więcej szczegółów znajdziesz w notatce do tego nagrania."

## Zadanie

Twoim zadaniem jest doprowadzenie robota transportującego urządzenie chłodzące w pobliże reaktora.

Do sterowania robotem służy specjalnie przygotowane API, które przyjmuje polecenia: `start`, `reset`, `left`, `wait` oraz `right`. Możesz wysłać tylko jedno polecenie jednocześnie.

Zadanie uznajemy za zaliczone, jeśli robot przejdzie przez całą mapę, nie będąc przy tym zgniecionym przez elementy reaktora. Bloczki reaktora poruszają się w górę i w dół, a status ich aktualnego kierunku, podobnie jak ich pozycja są zwracane przez API.

Napisz aplikację, która na podstawie aktualnej sytuacji na planszy będzie decydowała, jakie kroki powinien podjąć robot. Aby uprzyjemnić Ci pracę, przygotowaliśmy też graficzny podgląd sytuacji wewnątrz reaktora.

Podgląd sytuacji w reaktorze: https://hub.ag3nts.org/reactor\_preview.html

Zadanie nazywa się: **reactor**

Komendy dla robota wysyłasz do `/verify`:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "reactor",
  "answer": {
    "command": "start"
  }
}
```

### Mechanika zadania

- Plansza ma wymiary 7 na 5 pól.
- Robot porusza się zawsze po najniższej kondygnacji, czyli jego pozycja startowa to pierwsza kolumna i 5 wiersz.
- Miejsce instalacji modułu chłodzenia (Twój punkt docelowy) to 7 kolumna i 5 wiersz (dobrze widać to na podglądzie graficznym podlinkowanym wyżej).
- Każdy blok reaktora zajmuje dokładnie 2 pola i porusza się cyklicznie góra/dół. Gdy dojdzie do pozycji skrajnie wysokiej, zaczyna wracać na dół, a gdy osiągnie pozycję najniższą, wraca do góry.
- Bloki poruszają się tylko, gdy wydajesz polecenia. Oznacza to, że odczekanie np. 10 sekund nie zmieni niczego na planszy. Jeśli chcesz, aby stan planszy zmienił się bez poruszania robotem, wyślij komendę `wait`.

### Oznaczenia na mapie

- P — to pozycja startowa
- G — to pozycja do której masz doprowadzić robota
- B — to bloki reaktora
- . — to puste pola. Nic się na nich nie znajduje (to kropka)

### Jak powinna wyglądać implementacja Twojego algorytmu?

- Na początek zawsze wysyłasz polecenie `start`
- Rozglądasz się, jak wygląda plansza i podejmujesz decyzję, czy możesz wykonać krok do przodu
- Jeśli nie możesz wykonać kroku lub jest to zbyt niebezpieczne (np. zbliża się bloczek), to czekasz
- Jeśli czekanie nie wchodzi w grę (bo w kolumnie, w której stoisz, też zbliża się bloczek), to uciekasz w lewo
- Wykonujesz odpowiednie kroki za każdym razem podglądając mapę, tak długo, aż osiągniesz punkt docelowy
