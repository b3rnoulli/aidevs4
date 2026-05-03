---
title: S05E02 — Zestaw narzędzi
space_id: 2476415
status: scheduled
published_at: '2026-04-07T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/chamber-1775197086.png'
circle_post_id: 31353089
---
## Film do lekcji

![https://vimeo.com/1179917043](https://vimeo.com/1179917043)

Budowanie aplikacji wykorzystujących modele generatywnej sztucznej inteligencji może wymagać skorzystania z narzędzi rozwiązujących **jasno zdefiniowane problemy**, bądź pomagające w budowaniu funkcjonalności związanych ściśle z działaniem AI. Niekiedy też sami będziemy opracowywać rozwiązania, które przydadzą nam się w więcej niż jednym projekcie.

W tym przypadku nie mówimy wyłącznie o prostych skryptach czy bibliotekach, ale także całych platformach. Bo nawet jeśli dzięki AI możemy wygenerować mnóstwo logiki, to i tak do rozwijania rozbudowanych serwisów wciąż jest daleko i czasem lepiej jest sięgnąć po rozwiązania dostępne na rynku.

## Budowanie interfejsu użytkownika

Może wydawać się, że generatywne aplikacje nie wnoszą nic nowego do interfejsu użytkownika, ponieważ **komunikatory** i różnego rodzaju **dashboard'y** są z nami od dawna. W dużym stopniu jest to prawda, ale przy budowaniu zaawansowanych interfejsów dla agentów pojawiają się zupełnie nowe problemy.

Jednym z nich jest **wyświetlanie treści Markdown** z uwzględnieniem **strumieniowania** oraz **własnych komponentów**, których stan może zmieniać się w trakcie generowania odpowiedzi. Wśród komponentów mogą pojawić się zaawansowane artefakty, odtwarzacze czy inne, interaktywne bloki. W dodatku całość musi być dobrze zoptymalizowana, aby móc wyświetlić bardzo długie konwersacje, zawierające nawet kilkaset wiadomości. A w tym wszystkim musimy także zadbać o dobre doświadczenia użytkownika, które wynikają nie tylko z poprawnego działania, ale także zadbania o detale, takie jak wizualna informacja o bieżących statusach czy drobne animacje.

Zatem przygotowanie UI dla prostego czatu nie jest wyzwaniem. Ale stworzenie go dla zaawansowanego agenta, bądź systemu wieloagentowego potrafi zaskoczyć.

W przykładzie **05\_02\_ui** znajduje się aplikacja skupiająca się na **interfejsie czatu** obsługującym strumieniowanie oraz renderowanie wiadomości z uwzględnieniem specjalnych bloków odpowiedzialnych za wyświetlanie **reasoningu**, **narzędzi** oraz **artefaktów**. Interfejs obsługuje także **kontrolę tempa strumieniowanego tekstu** oraz tryby **live / demo** z których ten drugi daje możliwość sprawdzenia jak zachowuje się czat, gdy na liście pojawia się nawet 1500 wiadomości.

> Wskazówka: Wskazówka: Przykład 05\_02\_ui należy uruchomić poleceniem lesson22:ui oraz przejść w przeglądarce na adres localhost:5173

![Przykład interfejsu](https://cloud.overment.com/2026-03-19/ai_devs_4_generative_ui-36620434-5.png)

Interfejs czatu korzysta z kilku bibliotek:

- **[markdown-it](https://github.com/markdown-it/markdown-it)**: konwertuje składnię Markdown na HTML i odpowiada za całą warstwę renderowania tekstu
- **[highlight.js](https://github.com/highlightjs/highlight.js/)**: renderuje bloki kodu ze składnią właściwą dla danego języka programowania
- **[dompurify](https://github.com/cure53/DOMPurify)**: usuwa potencjalnie złośliwe tagi z generowanych wypowiedzi LLM. Jest to krytycznie istotne narzędzie zabezpieczające przed renderowaniem niepożądanych tagów czy skryptów.
- **[remend](https://www.npmjs.com/package/remend)** — naprawia niekompletną składnię Markdown podczas strumieniowania, umożliwiając poprawne renderowanie elementów, które nie zostały jeszcze zamknięte (np. bloki kodu, listy, pogrubienia)
- **[marked](https://marked.js.org/)** — tokenizuje narastającą treść strumieniowaną na niezależne bloki (akapity, nagłówki, bloki kodu itd.). Bez tego cała wiadomość modelu musiałaby być **ponownie renderowana** co każdy token.

Powyższa lista stanowi fundamentalny zestaw, z którego korzystam niemal we wszystkich swoich projektach. Na uwagę zasługuje jeszcze narzędzie **[Streamdown](https://github.com/vercel/streamdown)** jednak nie miałem okazji pracować z nim na produkcji. Na Githubie pojawiają się też nowe projekty, więc zawsze i tak warto przeszukać Internet, bo być może pojawią się lepsze alternatywy dla powyższych narzędzi.

Pomimo tego, że interfejs z omówionego przykładu **05\_02\_ui** już teraz jest dość zaawansowany, to nadal brakuje w nim wielu potencjalnie istotnych elementów:

- przesyłanie i **wyświetlanie** załączników (obrazy, dokumenty)
- **kopiowanie** treści całej wiadomości z zachowaniem stylów
- **rozgałęzianie** wątków i **edytowanie** poszczególnych wiadomości
- **usuwania** wybranych wiadomości (bądź cofania konwersacji)
- **wstrzymywanie** generowanej odpowiedzi
- **przeszukiwania** słów kluczowych dla całej konwersacji
- wysyłanie kolejnych wiadomości w trakcie inferencji
- **nagrywanie i odsłuchiwanie** wiadomości
- renderowanie składni LaTeX (np. z pomocą [KaTeX](https://katex.org/))
- **formatowanie tekstu** w polu tekstowym (np. z pomocą [TipTap](https://tiptap.dev/))
- wyświetlanie **diagramów** (np. z pomocą [Beautiful Mermaid](https://github.com/lukilabs/beautiful-mermaid))
- renderowanie map myśli (np. z pomocą [Markmap](https://markmap.js.org/))
- **udostępnianie wątków** innym użytkownikom
- wsparcie subagentów
- **obsługi** skrótów klawiszowych

Do tych punktów zazwyczaj musimy dołożyć także kontrolę ustawień, a także wszystko to, co mówiliśmy na temat wsparcia różnych modeli oraz providerów oraz naturalnie zarządzania kontekstem i obsługi zdarzeń. Mówiąc inaczej - jest to sporo pracy nawet pomimo wsparcia ze strony AI.

## Przydatne narzędzia dla agentów

W dotychczasowych lekcjach pojawiały się nazwy różnych narzędzi oraz platform, ale nie sposób omówić je wszystkie. Poza tym, nawet nie ma takiej potrzeby, ponieważ większość rozwiązań o których nierzadko jest dość głośno, pozostaje na bardzo wczesnym etapie rozwoju, a twórcy porzucają ich rozwój. Należy więc zachować ostrożność w ich dobieraniu, szczególnie jeśli dotyczą bezpośrednio AI. Sam też nie miałem okazji sprawdzić na produkcji wszystkich rozwiązań, które za chwilę sobie omówimy, także warto zachować do nich pewien dystans.

> Uwaga: część z wymienionych narzędzi jest powiązana z ekosystemem JavaScript / Node. Warto poszukać alternatyw dla swoich technologii bądź skorzystać z AI do przetłumaczenia wybranych funkcjonalności, o ile tylko pozwala na to licencja.

- **[just-bash](https://github.com/vercel-labs/just-bash)**: narzędzie to pozwala na pracę z wirtualnym systemem plików z pomocą poleceń znanych z **bash**'a. Różnica polega jednak na tym, że nie musimy dawać agentowi dostępu do terminala. Korzystamy więc z faktu, że modele świetnie posługują się tym narzędziem, a jednocześnie nie komplikujemy architektury poprzez konieczność podłączania sandbox'ów. Takie podejście może być dobrą alternatywą dla Files MCP, które przedstawiałem w pierwszych lekcjach.
- **[agent-browser](https://github.com/vercel-labs/agent-browser.git)**: to narzędzie CLI umożliwiające agentom korzystanie z **lokalnej** przeglądarki (Chrome/Chromium) w trybie "headless". Udostępnia narzędzia w postaci prostych komend, którymi bez problemu posługują się agenci. Odpowiedzi narzędzi są też domyślnie zoptymalizowane pod kątem liczby tokenów. Wspiera także indywidualne **sesje**, co pozwala na dostęp do stron wymagających logowania.
- **[browser-use](https://docs.browser-use.com/cloud/introduction) / [browserbase](https://www.browserbase.com/)**: to podobne do siebie narzędzia oferujące dostęp do przeglądarki w chmurze. Można je połączyć z **agent-browser** na przykład w sytuacji, gdy nie mamy dostępu do przeglądarki lokalnej bądź z innego powodu (np. z powodu skali) zależy nam na skorzystaniu z takich rozwiązań.
- [firecrawl](https://www.firecrawl.dev/) / [tavily](https://www.tavily.com/) / [brave](https://brave.com/search/api/) / [exa](https://exa.ai/) / [jina](https://jina.ai/): to narzędzia do przeszukiwania Internetu oraz wczytywania treści stron. W przeciwieństwie do narzędzi **web\_search** dostępnych natywnie u wszystkich głównych providerów LLM API, tutaj mamy nieporównywalnie większą kontrolę nad tym procesem. Spośród wymienionych najbardziej mogę polecić Firecrawl, Jina oraz Brave. W niektórych przypadkach może sprawdzić się skorzystanie z więcej niż jednej usługi ze względu na różne ograniczenia oraz ogólną skuteczność wczytywania treści stron.
- [daytona](https://www.daytona.io/)/ [e2b](https://e2b.dev/): to wspominane już sandbox'y, przydatne dla agentów posługujących się terminalem bądź narzędziami w trybie Code Mode. Alternatywnie można skorzystać tu także z [Deno Sandbox](https://deno.com/deploy/sandbox)
- [secure-exec](https://github.com/rivet-dev/secure-exec): dodaję to narzędzie, choć **nie miałem okazji z nim pracować**, ale prezentuje koncepcję wykonywania kodu bez potrzeby uruchamiania sandbox'a.
- **[live-kit](https://github.com/livekit/client-sdk-js)**: to narzędzie do budowania zaawansowanych interfejsów audio/video z przydatnymi funkcjonalnościami, na przykład do rozpoznawania ciszy bądź przeciwnie, do rozpoznawania momentu w którym użytkownik znów zaczyna coś mówić.
- [tiptap](https://tiptap.dev/): prawdopodobnie najlepszy dostępny tooling do budowania edytorów markdown
- [pyodide](https://pyodide.org): pozwala uruchamiać kod Python w przeglądarce lub Node.js dzięki WebAssembly.
- [markitdown](https://github.com/microsoft/markitdown): narzędzie do parsowania dokumentów (np. PDF / docx) do Markdown, prosto od Microsoft. Oczywiście jego skuteczność nie zawsze będzie perfekcyjna, ale dla prostszych struktur powinna być wystarczająca.
- [react-flow](https://reactflow.dev/): to narzędzie potencjalnie przydatne przy budowaniu interfejsów dla systemów wieloagentowych, skupiające się na interaktywnych diagramach.
- **[elevenlabs](https://elevenlabs.io/)**: to platforma oferująca jedne z najlepszych modeli text-to-speech oraz ostatnio także speech-to-text. Oferuje także opcję klonowania głosów oraz rozwiązania dla agentów głosowych. API oferuje także wsparcie dla narzędzi (np. MCP) oraz opcję strumieniowania generowanego audio.
- [sine-waves](https://github.com/isuttell/sine-waves): narzędzie przydatne przy wizualizacji nagrań audio (wave form)
- **[replicate](https://replicate.com/) / [fal](https://fal.ai/)**: to platformy udostępniające różne modele do przetwarzania między innymi obrazu i wideo. Uwzględniają także opcje **fine-tuningu**. Warto przede wszystkim zapoznać się z katalogiem i możliwościami, jakie oferują dostępne modele.
- **[sqlite-vec](https://github.com/asg017/sqlite-vec)**: rozszerzenie dla SQLite umożliwiające przechowywanie embedding'u oraz wyszukiwanie semantyczne.
- [qdrant](https://qdrant.tech/): wyszukiwarka wektorowa, przydatna w przypadku projektów działających na większej skali, w przypadku których rozszerzenia do baz danych nie są wystarczające.
- **[google-workspace-cli](https://github.com/googleworkspace/cli)**: to narzędzia CLI do interakcji z Google Drive, które mogą się przydać do tworzenia prywatnych agentów, bądź agentów działających wykorzystujących sandbox'y.
- **[chokidar](https://github.com/paulmillr/chokidar.git)**: narzędzie do monitorowania zmian w systemie plików
- **[commander](https://github.com/tj/commander.js#readme) / [zx](https://github.com/google/zx)**: narzędzia do interakcji z terminalem z poziomu kodu JavaScript / TypeScript.
- **[croner](https://www.npmjs.com/package/croner)**: narzędzie do zarządzania planowanymi zadaniami CRON dla JavaScript / Node.
- [winston](https://github.com/winstonjs/winston) / [tslog](https://github.com/fullstack-build/tslog.git): narzędzia do logowania

Stosowanie takich narzędzi bardzo pomaga w budowaniu aplikacji generatywnych, ponieważ odpowiada na **jasno zdefiniowane i powtarzalne** problemy. Dobrym przykładem jest projektowanie interfejsów głosowych, w przypadku których większość logiki dotycząca przetwarzania audio funkcjonuje od dawna. Jednocześnie zespół Livekit robi bardzo dobrą pracę w przystosowaniu tych rozwiązań do kontekstu agentowego.

W przykładzie **05\_02\_voice** znajduje się kod agenta z którym możemy po prostu **porozmawiać**. Dodatkowo agent ten, jest w stanie posługiwać się narzędziami (np. Files MCP), a wszystko dzieje się niemal w czasie rzeczywistym z uwzględnieniem wykrywania **ciszy** czy **przerywania** jego wypowiedzi.

> Uwaga: Przykład **05\_02\_voice** opiera się o Livekit działający lokalnie, więc należy zainstalować go w swoim systemie według [tej instrukcji](https://docs.livekit.io/transport/self-hosting/local/), a następnie uruchomić poleceniem **lesson22:voice**

Agent ten, może działać w dwóch trybach:

- **Speech to Text / Text to Speech:** aktywuje się, gdy dodamy klucz OpenAI (i opcjonalnie Elevenlabs). W tym trybie agent korzysta z trzech modeli, czyli **speech to text** (do rozpoznawania naszych poleceń), **LLM** (do generowania odpowiedzi agenta) oraz **text to speech** (do generowania audio).
- **Realtime:** aktywuje się, gdy dodamy klucz Gemini do naszego głównego pliku `.env`. Wówczas agent korzysta z [Gemini Live](https://ai.google.dev/gemini-api/docs/live-api), w przypadku którego AI może przyjąć i zwracać dane w różnych formatach.

Istotną różnicą pomiędzy tymi trybami jest fakt, że w tym pierwszym przypadku korzystamy z trzech modeli, a treść **tekstowa** jest **oddzielona** od treści **audio**. Natomiast w trybie **Realtime** ten podział nie występuje, więc agent jest w stanie jednocześnie przetwarzać **audio/tekst/obrazy/wideo** (ale w przykładzie skupiamy się tylko na audio).

![Tryby interakcji z agentem głosowym](https://cloud.overment.com/2026-03-21/ai_devs_4_voice_agents_modes-5191d053-c.png)

Mówimy więc tutaj o zupełnie nowych możliwościach projektowania agentów, które u swoich podstaw wykorzystują wszystko, czego do tej pory się nauczyliśmy, ale rozszerzają interakcję o różne formaty danych. W praktyce jednak do prostych interakcji i poleceń, nie będziemy potrzebowali trybu Realtime (bądź Live), który obecnie jest też dość kosztowny.

## Silniki wyszukiwania i bazy wektorowe

Już w lekcji **S02E02** omawialiśmy przykłady hybrydowego systemu RAG, który łączy ze sobą wyszukiwanie full-text oraz wyszukiwanie semantyczne. Omawialiśmy tam także różne strategie indeksowania oraz eksploracji treści. Z kolei w przykładach pojawiła się logika oparta o **SQLite** z rozszerzeniami **[fts5](https://www.sqlite.org/fts5.html)** oraz **[sqlite-vec](https://github.com/asg017/sqlite-vec)**. Podobne rozszerzenia możemy znaleźć także dla PostgreSQL, a samo wyszukiwanie pełnotekstowe oraz semantyczne dziś już niemal zawsze jest domyślne w większości narzędzi, wliczając w to rozwiązania takie jak [Supabase](https://supabase.com/) czy [Neo4j](https://neo4j.com/).

Jednocześnie na rynku istnieją bazy wektorowe takie jak [Qdrant](https://qdrant.tech/) czy [Chroma](https://www.trychroma.com/) specjalizujące się przede wszystkim w wyszukiwaniu semantycznym (bądź hybrydowym). Jeszcze do niedawna przy tworzeniu generatywnych aplikacji zwykle korzystaliśmy z połączenia **klasycznej bazy danych** oraz **bazy wektorowej**, pomiędzy którymi synchronizowaliśmy dane. W niektórych konfiguracjach do architektury dołączaliśmy także **klasyczny silnik wyszukiwania** taki jak [Algolia](https://algolia.com/) czy [Elasticsearch](https://www.elastic.co). Wówczas cały stack technologiczny stawał się dość skomplikowany, ale oferował też bardzo rozbudowane możliwości.

Obecnie rola wyszukiwania semantycznego spadła, a uwaga skupiła się na systemach plików oraz przeszukiwaniu ich treści z pomocą narzędzi typu **grep / ripgrep**. Co więcej, ogólny głos społeczności sugeruje, że stosowanie dziś wyszukiwania semantycznego nie ma sensu. Jednak jak zwykle zdania są tu podzielone i na przykład twórcy Claude Code opierają się wyłącznie o **grep**, a twórcy Cursor korzystają z obu podejść.

Natomiast dla nas oznacza to mniej więcej tyle, że mamy do dyspozycji wiele opcji, które możemy dopasować do charakterystyki oraz skali naszego projektu. A przy podejmowaniu takich decyzji, możemy kierować się tym, co znaliśmy do tej pory. Na przykład **wyszukiwanie pełnotekstowe** oparte wyłącznie o bazę taką jak SQLite czy PostgreSQL może sprawdzić się w wielu projektach, ale gdy wyszukiwanie staje się dla nas krytycznie ważne i w dodatku pracujemy na ogromnych zestawach danych, to wówczas trudno wyobrazić sobie inne scenariusze niż skorzystanie z pełnoprawnych silników wyszukiwania. Podobne podejście można przełożyć na zastosowanie baz wektorowych, gdzie na ich wybór możemy zdecydować się dopiero wtedy, gdy zaczyna wymagać tego nasz projekt.

Poniżej widzimy porównanie dwóch scenariuszy, czyli zastosowania **rozszerzeń** dla baz danych oraz **dedykowanych rozwiązań**. Schemat dobrze pokazuje, że w obu przypadkach proces jest niemal identyczny, ale złożoność architektury w drugim przypadku jest **nieporównywalnie większa**. Musimy więc mieć realny powód, aby się na nią zdecydować, a tym powodem zazwyczaj będą duże ilości danych, potrzeba wysokiej wydajności oraz zaawansowanych funkcji wyszukiwania, np. zaawansowane filtrowanie czy grupowanie rekordów.

![Porównanie architektury RAG](https://cloud.overment.com/2026-03-21/ai_devs_4_searches-983353e2-8.png)

Przekładając to na proces decyzyjny, możemy wziąć pod uwagę kilka aspektów:

- **Wczytywanie treści:** może się okazać, że wyszukiwanie w ogóle nie jest potrzebne, ponieważ w pełni wystarczające jest wczytanie wybranych dokumentów do kontekstu konwersacji. Przykładem tutaj może być (prawdopodobnie) główna mechanika pamięci ChatGPT, która według [tej analizy](https://x.com/manthanguptaa/status/2011673060844397005) znacznie priorytetyzuje **szybkość działania** nawet kosztem **skuteczności**. W takim przypadku zastosowanie baz wektorowych nie jest konieczne.
- **Pliki tekstowe:** przekonaliśmy się już wielokrotnie, że agent nawigujący po plikach tekstowych może uzyskać bardzo wysoką skuteczność. Może się więc okazać, że takie podejście będzie dla nas wystarczające, a jednocześnie jest raczej proste w realizacji. Natomiast w praktyce możemy też zauważyć jego ograniczenia, na przykład w sytuacji, gdy pracujemy z treściami w wielu językach bądź różnych formatach.
- **Podejście hybrydowe**: stosowanie wyłącznie samych baz wektorowych do wyszukiwania kontekstu **jest już nierekomendowane** i jeśli będziemy brali je pod uwagę, to zawsze musimy myśleć o nim w kontekście wyszukiwania hybrydowego. Tutaj najlepiej jest pomyśleć o tym tak, że jeśli wyszukiwanie treści przez **grep / wyszukiwanie pełnotekstowe** nie jest wystarczające, to wówczas powinniśmy pomyśleć o jego **rozszerzeniu** o wyszukiwanie semantyczne.
- **Grafy:** zastosowanie zaawansowanego indeksowania, obejmującego mapowanie treści oraz jego eksplorację z pomocą grafów z dużym prawdopodobieństwem da nam największą skuteczność, ale będzie wiązało się z odpowiednio wysokimi kosztami - nie tylko wyrażonymi finansowo, ale także złożonością logiki oraz czasem potrzebnym na przetwarzanie danych. Bez wątpienia jednak jest to podejście, które możemy brać pod uwagę.

Patrząc na te scenariusze widzimy, że mamy do dyspozycji różne opcje, które dobieramy do wymagań naszego projektu. Z doświadczenia mogę powiedzieć tutaj, że w swoich projektach wykorzystuję pierwsze trzy podejścia i raczej nie ma tutaj **uniwersalnego rozwiązania**.

## Własne rozwiązania i narzędzia

Pracując z generatywnym AI zauważymy powtarzające się schematy. Wśród nich będą pojawiać się uniwersalne problemy, które będziemy mogli zaadresować pojawiającymi się na rynku narzędziami. Są jednak przypadki, gdy problemy jakie spotkamy będą na tyle indywidualne, że lepiej będzie opracować własne rozwiązania. Tutaj mam na myśli zarówno serwery MCP, narzędzia CLI, a nawet dedykowane aplikacje udostępniające API z których będą mogli skorzystać nasi agenci.

W związku z tym, że lista o której tutaj mówimy jest raczej indywidualna, skupimy się na obszarach oraz sytuacjach na które warto zwrócić uwagę.

- **Prompty:** w całym szkoleniu skupiliśmy się na budowaniu logiki workflow oraz systemów agentowych. Choć sam temat projektowania instrukcji pojawiał się wielokrotnie, tak mało mówiliśmy o **prostych, powtarzalnych** promptach, które możemy przypisać do skrótów klawiszowych czy jako umiejętności agentów. Opracowanie własnej biblioteki składającej się nawet z kilku instrukcji z których będziemy korzystać wielokrotnie, jest niezwykle wartościowe pomimo swojej prostoty. Warto więc zwrócić uwagę na zapytania oraz zwroty, które często kierujemy do AI, a następnie zastanowić się jak możemy ułatwić sobie ich uruchamianie, bo poza skrótem klawiszowym, może być to makro, rozszerzenie do przeglądarki lub skrót na telefonie.
- **Zarządzanie plikami:** wielokrotnie przekonaliśmy się jak istotną rolę w pracy z AI odgrywają dokumenty w systemie plików bądź zewnętrznych usługach, np. Notion lub Google Drive. Warto więc przygotować sobie narzędzia (bądź skorzystać z istniejących), które pozwolą agentowi się nimi posługiwać.
- **Dostęp do chmury:** praktycznie na każdym kroku pojawia się potrzeba udostępniania i przesyłania plików oraz obrazów. Warto więc wyposażyć agenta w narzędzia do ich odczytu oraz wgrywania na zdalny serwer. Ewentualnie można tu skorzystać ze wspomnianych rozwiązań takich jak [Uploadthing](https://uploadthing.com/) lub z własnych serwerów.
- **Generowanie dokumentów:** nie mam tutaj na myśli generowania całej treści, ale jej elementów, takich jak obrazy, tabele czy wizualizacje. Pod uwagę można wziąć także całe szablony dokumentów czy kreacji reklamowych, które już teraz mogą być automatycznie uzupełniane przez LLM.
- **Przetwarzanie obrazu/audio/wideo:** jeśli tylko pracujemy z notatkami głosowymi, mamy w nawyku robienie zdjęć albo często korzystamy z treści wideo, to również możemy odnaleźć wartość w nawet prostych integracjach AI. Dobrym przykładem jest narzędzie [Audiopen](https://www.audiopen.ai/), czyli dopracowane rozwiązanie skupiające się wyłącznie na jednym zadaniu.
- **Sandbox:** agenci wykonujący akcje wymagające dostępu do funkcjonalności, których nieprawidłowe uruchomienie mogłoby przynieść negatywne efekty, obecnie są czymś powszechnym. Warto więc zadbać o stworzenie bądź wybranie sandboxów w których będą mogli funkcjonować nasi agenci. Z kolei na własne potrzeby można rozważyć nawet dedykowany komputer (np. stary laptop) na potrzeby podejmowania akcji, które mogą być blokowane na zdalnych serwerach ze względu na adres IP.
- **CLI/MCP**: stworzenie integracji dla narzędzi i serwisów z którymi pracujemy na co dzień i zamknięcie ich w formę CLI lub MCP umożliwia ich łatwe "przenoszenie" pomiędzy agentami, które będziemy tworzyć oraz udostępnianie w zespole bądź wśród klientów. Warto zacząć nawet od utworzenia zaledwie jednej takiej integracji, która natychmiast stanie się częścią naszej pracy - wdrożenie jej powinno być łatwe, a korzystając z niej łatwiej zauważymy potrzebę budowania kolejnych.
- **Interfejs:** stworzenie własnego graficznego interfejsu czatu, który dziś może obejmować współpracę z wieloma agentami lub wprost pełnić rolę „panelu zarządzania”, jest wymagającym, ale bardzo wartościowym projektem, którego możemy się podjąć. Takie rozwiązanie sprawdzi się przede wszystkim wtedy, gdy będziemy potrzebować **wysokiego poziomu personalizacji** oraz dopasowania ustawień do naszych potrzeb. Jednocześnie sam interfejs nie musi od razu skupiać się na zarządzaniu całym systemem, ale jak widzieliśmy w poprzednich lekcjach, może koncentrować się wyłącznie na wybranych obszarach.

Choć powyższa lista może wyglądać niepozornie, tak wymienione obszary mogą składać się na cały system zarządzania naszą pracą bądź też wybranymi aktywnościami z życia prywatnego. Mówimy tutaj głównie o **komponentach**, które możemy układać w różnych konfiguracjach. Poza tym, możemy też znacznie ułatwić sobie projektowanie tych najbardziej powtarzalnych, np. narzędzi CLI, serwerów MCP czy promptów.

Natomiast na ten moment najważniejsze jest przynajmniej **"przeklikanie"** wymienionych dzisiaj narzędzi. Nawet jeśli dziś z nich nie skorzystamy, to jest szansa, że zapadną nam w pamięć i wrócimy do nich, gdy pojawi się taka potrzeba. Poza tym warto podjąć działanie i utworzyć nawet proste narzędzia MCP/CLI przy współpracy z AI i zwyczajnie zacząć z nich korzystać.

## Fabuła

![https://vimeo.com/1179946858](https://vimeo.com/1179946858)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze piąty... nie wiem, czy Ty też tak masz, ale ja, gdy planuję alternatywne rozwiązanie na wypadek, gdy mój plan się nie uda, czuję się, jakbym spisywał testament. Bo co to znaczy, że skok w czasie się nie uda? Że wylądujemy w złym miejscu? Że nie powstrzymamy Zygfryda przed przejęciem kontroli nad światem? Czy może to, że mnie i Ciebie już nie będzie? Dla kogo my to wszystko przygotowujemy? Dla ludzi, którzy będą po nas? Czy też przed nami? Zależnie od systemu chronologicznego, który przyjmiemy. Musimy teraz zaplanować bezpieczną drogę ucieczki dla wszystkich miast, które mają zostać ewakuowane. Trzeba będzie dowiedzieć się, która z dróg, a tych, które bierzemy pod uwagę, jest bezpieczna i nieskażona. Jednocześnie musimy przekonać operatorów, aby, gdy tylko zobaczą podejrzany ruch w systemie OKO, nie podnieśli alarmu. Ma to być dla nich coś zupełnie normalnego, czego się spodziewają. Tym razem nie możemy posłużyć się ani falami radiowymi, ani internetem. Wprost uderzymy w jednego z operatorów systemu. Konkretniej mówiąc, zadzwonimy do niego. Stary, dobry telefon... kto by przypuszczał, że przyda nam się w takich okolicznościach. Mamy już zestawione bezpieczne połączenie z operatorem. Jedyne, co musisz zrobić, to zaprojektować bota, który będzie w stanie wyciągnąć od operatora potrzebne nam informacje. Więcej szczegółów znajdziesz w notatce do tego filmu.

## Zadanie praktyczne

Musisz dodzwonić się do operatora systemu i przeprowadzić rozmowę (audio) tak, aby nie wzbudzić podejrzeń. Interesuje nas tylko jedna rzecz: która droga nadaje się do przerzutu ludzi do Syjonu. Gdy już ustalisz bezpieczną trasę, musisz jeszcze doprowadzić do wyłączenia monitoringu na tej konkretnej drodze, bo przejście większej grupy nie może uruchomić alarmu.

To zadanie jest rozmową wieloetapową. Liczy się nie tylko to, co chcesz uzyskać, ale też kolejność wypowiedzi. Jeśli pomylisz etapy albo wyślesz zły komunikat, rozmowa zostanie spalona i trzeba będzie zacząć od nowa.

Nazwa zadania: **phonecall**

Odpowiedź wysyłasz do: <https://hub.ag3nts.org/verify>

Na początku musisz rozpocząć sesję rozmowy:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "phonecall",
  "answer": {
    "action": "start"
  }
}
```

Po uruchomieniu rozmowy masz ograniczony czas na jej dokończenie, więc nie zwlekaj niepotrzebnie.

### Jak rozmawiać z operatorem

Każdy kolejny krok po `start` wysyłasz jako pojedyncze nagranie audio encodowane w formacie base64 (preferowany format to MP3).

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "phonecall",
  "answer": {
    "audio": "tutaj-wklej-base64-z-nagraniem"
  }
}
```

Tę samą formę komunikacji utrzymuj przez całą rozmowę. Jeśli rozmawiasz z operatorem przez audio, jego odpowiedzi także mogą wracać w postaci nagrań.

### Informacje, które posiadasz

- Porozumiewasz się tylko w języku polskim, a operator odpowiada także w języku polskim.
- Przedstawiasz się jako Tymon Gajewski - od tego zaczynasz rozmowę
- Zapytaj operatora o status wszystkich trzech dróg: RD224, RD472 i RD820. Musisz poinformować także operatora, że pytasz o to ze względu na transport organizowany do jednej z baz Zygfryda - podaj to wszystko w jednej wiadomości
- Poproś operatora o wyłączenie monitoringu na tych drogach, które według niego będą przejezdne.
- Tajne hasło operatorów brzmi: **BARBAKAN**
- Gdyby operator dopytywał, dlaczego chcesz wyłączyć ten monitoring, to wspomnij, że jest to w ramach transportu żywności do jednej z tajnych baz Zygfryda. Nie można zdradzić jej lokalizacji, dlatego ta misja nie może być odnotowana w logach.

### Ważne uwagi

- Staraj się wysyłać krótkie i sensowne komunikaty do operatora. Nie proś o wiele rzeczy w ramach jednej wiadomości.
- Po wysłaniu komendy `start` komunikujesz się z operatorem wyłącznie przez pole `audio`.
- Jeśli rozmowa pójdzie źle, musisz ponownie wywołać `start` i przejść całość scenariusza od początku.
- Zadanie zostanie zaliczone, gdy podczas jednej rozmowy ustalisz, która droga jest przejezdna, a następnie poprosisz o jej odblokowanie i zostanie ona skutecznie odblokowana.

Jeśli przeprowadzisz rozmowę poprawnie, Centrala odeśle flagę.
