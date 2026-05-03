---
title: S04E02 — Aktywna współpraca z AI
space_id: 2476415
status: scheduled
published_at: '2026-03-31T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/0402-1774694238.png'
circle_post_id: 31103394
---
Mówi się, że prosty interfejs czatu był jedną z przyczyn sukcesu ChatGPT. Choć trudno jednoznacznie stwierdzić czy rzeczywiście tak było, to właśnie taka forma interakcji do dziś pozostaje domyślną przy pracy z agentami AI. Jednak coraz rzadziej jest to wyłącznie wymiana wiadomości, ale także zaawansowane funkcjonalności związane z zarządzaniem kontekstem, integracjami, autonomią czy różnymi formami interakcji.

Nawet w przypadku systemów działających w tle, z ograniczonym udziałem człowieka, obecna jest jakaś forma wymiany informacji, podejmowania decyzji lub raportowania. Wyraźnie zauważalny jest trend, w którym na jedną wiadomość użytkownika nie przypada już jedna odpowiedź asystenta AI, ani nawet dziesiątki kroków wykonywanych przez pojedynczego agenta. Dziś jedno zdarzenie może zapoczątkować aktywność całego zespołu agentów, którzy wspólnie dążą do osiągnięcia postawionego celu.

Będziemy więc chcieli zarządzać taką współpracą, co nierzadko będzie wymagało podjęcia decyzji o tym, kiedy sięgnąć po gotowe rozwiązania, a kiedy stworzyć własne. Aby móc odpowiedzieć na to pytanie, przyjrzymy się dostępnym opcjom, uwzględniając przy tym także budowanie własnych rozwiązań.

## Interfejs czatu

Większość z nas pracuje już z agentami do kodowania takimi jak **Cursor / Claude Code / Open Code / Codex / Pi** bądź IDE rozszerzone o funkcjonalności AI, np. narzędzia JetBrains. Poza kontekstem kodu zwykle wybieramy między ChatGPT, Claude, Perplexity czy Grok, bądź dedykowane aplikacje takie jak Jan czy Cherry Studio albo własne rozwiązania. W niektórych przypadkach sprawdzić się mogą także agenci zintegrowani z komunikatorami takimi jak Slack, Telegram czy Discord.

Obecnie wybór pomiędzy wymienionymi rozwiązaniami sprowadza się do **dostępności modeli** oraz **ceny** i niekiedy także samych funkcjonalności. Jednocześnie granice pomiędzy tymi narzędziami częściowo się zacierają, a wartość końcowa jaką otrzymujemy wydaje się być zbliżona. Interesującym przykładem jest **Agent Client Protocol (ACP)** wykorzystywany między innymi przez JetBrains czy Zed dzięki któremu łączą się one z agentami takimi jak Codex czy Cursor.

Świadomość tego, co dzieje się na rynku jest istotna, ponieważ pomoże nam to w podejmowaniu decyzji przy tworzeniu rozwiązań zarówno dla nas, jak i naszych klientów. Bo przykładowo, gdy tworzymy narzędzia integrujące się np. z Linear na potrzeby wyłącznie zespołu programistycznego, zwykle najlepszym rozwiązaniem będzie stworzenie integracji CLI. Agenci do kodowania bez problemu poradzą sobie z jej obsługą, a użytkownicy z instalacją oraz aktualizacjami. Jeśli jednak z narzędzia będą korzystać także osoby nietechniczne, to wówczas lepszym wyborem będzie opracowanie MCP bo pozwoli to na podłączenie także do interfejsów webowych (np. Claude)

Zatem w sytuacji, gdy możemy stworzyć rozszerzenia lub integracje, które połączą się z narzędziami, z których już teraz korzystają nasi klienci, będzie to raczej lepszy pomysł niż budowanie wszystkiego od podstaw. Jednocześnie takie podejście relatywnie szybko zaczyna być bardzo ograniczające, ale musimy też skutecznie określić granicę, kiedy tak się stanie. Spójrzmy więc na poniższe zestawienie dostępnych na rynku narzędzi.

![Porównanie interfejsów AI](https://cloud.overment.com/2026-03-04/ai_devs_4_agents_map-65da49cd-5.png)

Można uznać, że każde z narzędzi posiada zbliżone możliwości bazowe. Różnice są jednak bardzo wyraźne w kontekście **personalizacji i rozszerzeń**. W tym przypadku najwięcej do zaoferowania mają narzędzia CLI, ale wiemy też, że nie są one przyjaznym środowiskiem dla wszystkich, więc nie możemy ignorować pozostałych opcji.

Przed decyzją o tworzeniu całkowicie dedykowanych rozwiązań należy wziąć pod uwagę także aspekt ekonomiczny. Narzędzia takie jak Claude Code, Codex czy ChatGPT oferują plany subskrypcyjne, które ze względu na działanie na dużej skali, są nieporównywalnie bardziej atrakcyjne cenowo niż korzystanie z API ([przykład estymacji](https://she-llac.com/claude-limits)). Co więcej część klientów posiada już umowy oraz plany dla pracowników, co również ułatwia wdrożenie.

Zatem wybór interfejsu wcale nie jest oczywisty, a jednocześnie w bardzo dużym stopniu będzie determinował pozostałe obszary projektu. Sama decyzja nie jest ograniczona jedynie do gotowych i dedykowanych narzędzi, bo możliwych scenariuszy jest sporo.

- **Narzędzia CLI:** powiedzieliśmy, że narzędzia CLI sprawdzą się w indywidualnym kontekście użytkownika pracującego na swojej maszynie. Jednocześnie rolę tej maszyny może pełnić sandbox i choć komplikuje to architekturę, tak otwiera przestrzeń do stosowania narzędzi CLI w różnych scenariuszach.
- **Serwery MCP:** niemal każdy ze wspomnianych interfejsów posiada wsparcie MCP. Fakt, że narzędzia MCP nie muszą być pojedynczymi akcjami sprawia, że mogą obejmować także komunikację z systemem wieloagentowym. Połączenie tego z interfejsem MCP Apps pozwoli także na monitorowanie postępów czy dostarczanie dodatkowych informacji.
- **Komunikatory:** narzędzia takie jak Slack nie zostały stworzone z myślą o AI, ale ich API obejmuje koncepcje botów, a nawet interaktywnych wiadomości wyświetlających proste elementy interfejsu. Profile botów, dedykowane kanały czy komendy pozwalają na relatywnie duży poziom dopasowania. Natomiast przede wszystkim użytkownicy pozostają w znanym im kontekście komunikatora.
- **Dedykowane rozwiązanie:** tutaj mówimy już o budowaniu narzędzi od podstaw, co wbrew pozorom dziś nie jest już tak skomplikowane jak kiedyś. Tym bardziej, że nie musimy od razu mówić o klonowaniu wszystkich funkcjonalności ChatGPT czy Slack'a, ale nawet relatywnie prostych interfejsach skupiających się na konkretnych interakcjach z agentem.

Przekładając to na wizualizację, widzimy, że nie ma jednego, uniwersalnego rozwiązania. Tym bardziej że w praktyce nie mówimy tu o „opcjach”, spośród których musimy coś wybrać, lecz o ich połączeniu w sposób, który będzie działał dla nas najlepiej.

![Wybór interfejsu według scenariuszy](https://cloud.overment.com/2026-03-05/ai_devs_4_fit-e01dadf3-f.png)

Jeśli spojrzymy na te opcje z myślą o własnych potrzebach (np. prywatnych bądź wewnątrzfirmowych), to:

- Kontekst CLI może być domyślnym wyborem. Tym bardziej, że istnieje możliwość uruchamiana agentów do kodowania na zdalnych serwerach. Tutaj największą wartością będzie optymalizacja swojej pracy oraz obserwowanie skuteczności modeli w różnych sytuacjach.
- Budowanie wszystkich mechanik od podstaw lub częściowo w oparciu o istniejące narzędzia da nam także wartość edukacyjną oraz doświadczenia, które będziemy mogli wykorzystać w pracy.
- Tworzenie własnych interfejsów również daje ogromną wartość, nawet w zakresie świadomości ich przewag czy wysiłku wymaganego przy ich budowie, który nadal jest znaczący pomimo dużego wsparcia ze strony AI i generowania kodu.

Analogicznie będziemy budować scenariusze z myślą o klientach czy potrzebach wewnątrzfirmowych. Aby jednak lepiej to zrozumieć, przyjrzyjmy się teraz dokładniej różnicy pomiędzy **Serwerem MCP w Claude**, a **dedykowanym interfejsem**.

Załóżmy, że posiadamy system agentowy, który pozwala monitorować skuteczność kampanii marketingowych realizowanych na potrzeby naszego produktu. Funkcjonalności obejmują **przeglądanie statystyk**, **monitorowanie** sytuacji wymagających uwagi oraz **generowanie raportów**. Każda z tych akcji obejmuje zaangażowanie AI w kontekście formy prezentacji danych oraz wskazówek i sugestii dotyczących potencjalnych działań.

![Agent wspierający monitorowanie działań marketingowych](https://cloud.overment.com/2026-03-05/ai_devs_4_marketing_agent-0c151848-b.png)

W tej sytuacji możemy skorzystać z MCP Tools i MCP Apps, aby bez większych problemów zintegrować się np. z Claude. Wiąże się to jednak z konkretnymi ograniczeniami:

- Claude.ai nie wspiera **samplingu** w MCP. Oznacza to, że poza opłatą subskrypcji, ponosimy także koszty API związane z działaniem agenta.
- Personalizacja instrukcji w Claude jest możliwa, lecz na różne sposoby ograniczona. Nasz system raczej będzie musiał opierać się wyłącznie o opisy narzędzi i zwracane przez nich treści.
- Sam interfejs wywołań narzędzi MCP jest poza naszą kontrolą. Zakładając więc, że nasz system podczas gromadzenia statystyk będzie potrzebował dodatkowych informacji lub potwierdzeń, technicznie mamy bardzo ograniczone możliwości skontaktowania się z użytkownikiem.
- W przypadku rozbudowanych reguł dotyczących uprawnień również pojawiają się komplikacje. Przykładem może być potrzeba wczytania danych dla z różnych kampanii czy przeglądu statystyk dla wszystkich klientów.
- Jeśli system będzie uwzględniał podejmowanie działań w tle, to mamy bardzo małe możliwości poinformowania użytkownika o ich statusie, nie mówiąc już o ewentualnych interwencjach.

Przynajmniej część z tych ograniczeń adresuje MCP Apps, ale i tak nie da się tego porównać do dedykowanego interfejsu i całościowej kontroli doświadczeń użytkownika.

Myślę, że powyższy przykład, pomimo widocznych ograniczeń pokazuje, że podłączanie się do istniejących narzędzi i ekosystemów może mieć mnóstwo sensu. Niezbędna jest tu jednak świadomość możliwości oferowanych przez narzędzia takie jak Claude, ChatGPT czy nawet komunikatorów takich jak Telegram (który niedawno wprowadził możliwość strumieniowania wiadomości). Tym bardziej, że funkcjonalności oferowane przez stojące za nimi firmy nieustannie się zmieniają.

Na tym etapie dobrze jest też wybrać bądź stworzyć przynajmniej jeden serwer MCP i przejść przez proces podłączenia go np. z Claude Code bądź Claude.ai. Takie doświadczenie pozwoli lepiej zrozumieć to, o czym właśnie sobie powiedzieliśmy.

Tymczasem, gdy spojrzymy na **[listę popularnych klientów MCP](https://modelcontextprotocol.io/clients)** zobaczymy, że zaledwie pojedyncze wpisy deklarują pełne wsparcie tego protokołu. Nawet w ostatnim przykładzie mieliśmy okazję zobaczyć jak dużym ograniczeniem może być brak **samplingu**, czyli możliwości odwrotnej komunikacji Client - Server. Zauważyliśmy również, że potencjalnym problemem jest także ustawienie instrukcji systemowej. To zaledwie pojedyncze przykłady funkcjonalności, których może nam brakować, ponieważ w praktyce istotne stają się:

- Dostęp do historii wiadomości przez różnych użytkowników (np. kanały na Slacku)
- Tworzenie profili asystentów dla wybranych obszarów (np. projekty w Claude)
- Automatyczna konfiguracja ustawień (np. współdzielenie umiejętności w Claude Code)
- Elastyczny interfejs aplikacji (np. wyświetlanie Artifacts w ChatGPT)
- Opcja korzystania z różnych modeli (np. Raycast)
- Możliwość przetwarzania różnych formatów treści (np. źródła w NotebookLM)
- Wsparcie interakcji audio & wideo (np. tryb live w Google AI Studio)
- Dostęp do funkcji systemowych (np. w przypadku aplikacji desktopowych)
- Możliwość zachowania pełnej prywatności (np. LM Studio)

Powyższa lista sugeruje, że pomimo podobieństw pomiędzy dostępnymi na rynku aplikacjami, istnieje także mnóstwo szczegółów które będą decydować o wyborze, bądź konieczności stworzenia własnych narzędzi. Patrząc jednak na obecną sytuację na rynku, możemy powiedzieć, że:

- **Claude Code / Open Code** sprawdzą się najlepiej w osobistym kontekście
- **Pi** będzie alternatywą dla powyższych, ale bardziej zaawansowaną
- **Claude.ai** to bardzo dobra opcja dla osób o profilu nietechnicznym
- **Slack** (bądź inny komunikator) sprawdzi się w kontekście zespołowym

Oczywiście powyższa rekomendacja stanowi duże uogólnienie, ale dość dobrze opisuje rzeczywistość i rozwiązania na które decydują się firmy. Jednocześnie wyraźnie widać również to, że wzrost poziomu wykorzystania AI naturalnie odsuwa nas od generycznych interfejsów w stronę dedykowanych rozwiązań.

## Personalizacja interakcji z modelami językowymi

Do tej pory omawialiśmy przede wszystkim **narzędzia** oraz możliwość połączenia agentów do **dokumentów**. Pojawiał się także wątek kształtowania instrukcji agentów, ale raczej w logice back-endu. Jednak potrzeba personalizacji może być potrzebna także po stronie interfejsu użytkownika. Przekłada się to na:

- **Profile**: użytkownik może pracować w więcej niż jednym kontekście, dlatego podział na profile wyspecjalizowanych agentów ma duży sens. Każdy z nich może posiadać własne ustawienia i zasoby wiedzy, a sama aplikacja może obejmować ich autonomiczną współpracę. Mówimy więc tu o koncepcji **subagentów** znanych na przykład z Claude Code.
- **Umiejętności**: predefiniowane instrukcje wstrzykiwane do konwersacji albo intencjonalnie w wyniku akcji użytkownika, albo poprzez decyzję modelu, to bardzo wygodny sposób na personalizację zachowań modelu. Jest to jedna z najważniejszych funkcjonalności każdego interfejsu AI.
- **Narzędzia**: wsparcie MCP czy natywnych integracji musi uwzględniać łatwą kontrolę nad tym, jakie narzędzia są w danej chwili uruchomione, a także ich możliwości personalizacji (omawialiśmy to w kontekście "Augmented Function Calling")
- **Workflow**: obecnie tylko pojedyncze interfejsy posiadają funkcjonalności umożliwiające wykonywanie serii powtarzalnych akcji. W tym kontekście pomocne są także mechaniki takie jak hooki czy zaplanowane zadania.

Mówimy tu o relatywnie prostych i użytecznych mechanikach, których wciąż trudno szukać w popularnych interfejsach, szczególnie gdy zależy nam na ich rozbudowanych wersjach, a nie na podstawowych ustawieniach.

![Główne elementy interfejsu agentów](https://cloud.overment.com/2026-03-05/ai_devs_4_components-1091651e-c.png)

Sama implementacja takich funkcjonalności nie decyduje o ich użyteczności, ponieważ:

- Konfiguracja subagentów powinna obejmować możliwość ich **generowania** zgodnie z dobrymi praktykami, a ich ustawienia powinny uwzględniać na przykład wybór modelu oraz aktywnych trybów aplikacji (np. przeszukiwanie sieci). Przykładem aplikacji, która robi to w ten sposób jest Claude Code. Następnie przełączanie się pomiędzy nimi powinno odbywać się przez wygodne menu, skróty klawiszowe, ich wywołanie przez znak '@' (mention) czy automatyczne wywołanie przez AI.
- Analogicznie też łatwe powinno być generowanie i wywoływanie umiejętności. Tutaj ze względu na ich potencjalną liczbę, dobrze też zadbać o wyszukiwanie czy grupowanie (np. poprzez przypisanie do agentów)
- Samo wywoływanie narzędzi to nie wszystko, ponieważ liczy się także sposób w jaki prezentujemy dane do uruchomienia akcji, potwierdzenia, postęp, informacje o błędach oraz wyniki. Istotne są także możliwość wstrzymania / anulowania akcji.
- W przypadku akcji odbywających się w tle, albo w wyniku automatyzacji albo po prostu prowadzenia więcej niż jednego wątku jednocześnie, użytkownik powinien być w jasny sposób informowany o bieżącym statusie czy potrzebie interwencji. Złe praktyki można zaobserwować na co dzień niemal we wszystkich dostępnych na rynku narzędziach. Nacisk na doświadczenia użytkownika i świetny interfejs nadal ma tutaj znaczenie i nie chodzi wyłącznie o wygląd ale także jakość implementacji.

Patrząc na liczbę funkcjonalności, ilość detali oraz mechanik, które bierzemy tutaj pod uwagę, można powiedzieć, że jest to niemal zupełnie nowa klasa interfejsów i wyzwań z perspektywy ich projektowania.

![Jakość interfejsu i szczegóły wpływające na doświadczenia użytkownika](https://cloud.overment.com/2026-03-05/ai_devs_4_uiux-00adee0c-8.png)

Powyższa wizualizacja stanowi także dobry dowód na to, że budowanie własnych interfejsów zdecydowanie nie polega wyłącznie na klonowaniu istniejących funkcjonalności i jest to przestrzeń na nowe pomysły.

## Jednorazowe zadania i pojedyncze akcje

Rozmowy na temat agentów bardzo szybko przechodzą w obszary skomplikowanych systemów. Nawet teraz znacznie łatwiej jest mówić o zaawansowanych interfejsach, integracjach i autonomii, niż o prostych rozwiązaniach, które możemy wdrożyć w ciągu zaledwie kilku minut. Problem w tym, że zauważenie przestrzeni na wdrożenie pojedynczych akcji i szybkich zadań, nie jest takie łatwe.

Dobrym punktem startowym procesu myślowego na temat takich mikro-narzędzi jest spojrzenie na nie przez pryzmat akcji przypisywanych do skrótów klawiszowych, gestów (np. na ekranie dotykowym) czy prostych wyzwalaczach znanych z aplikacji Keyboard Maestro czy BetterTouchTool. Kilka przykładów:

- **Czytanie zaznaczenia:** modele do generowania audio są już bardzo szybkie i skuteczne, nawet jeśli działają lokalnie (zakładając, że mamy odpowiedni sprzęt). Przeczytanie zaznaczonego tekstu bardzo pomaga w jego zrozumieniu, szczególnie jeśli mamy łatwą możliwość kontroli tempa odtwarzania.
- **Wyjaśnienie zaznaczenia:** analogicznie do wcześniejszej akcji, zaznaczony tekst (np. słowo kluczowe bądź definicja) może zostać zwięźle wyjaśniona korzystając z wiedzy modelu bądź wyników wyszukiwania
- **Transformacja zaznaczenia:** korekty, tłumaczenia, parafrazy, zwiększenie czytelności, zmiana na listę zadań, ekstrakcja informacji z danej kategorii - takie transformacje tekstu przypisane do skrótów klawiszowych są potencjalnie najbardziej użytecznym zastosowaniem AI w codziennej pracy.
- **Transformacje kontekstowe:** transformacje tekstu mogą dopasowywać się w zależności od kontekstu. np. w przeglądarce, gdy aktywna karta jest w domenie github.com, transformacje tekstu automatycznie dopasowują się do naszego stylu tworzenia dokumentacji / opisów issues.
- **Wizualizacja zaznaczenia:** zmiana tekstu na wizualizację i to bardzo precyzyjną, a nawet w wybranym stylu jest już dziś możliwa, szczególnie z tak precyzyjnymi modelami jak Nano Banana 2, bądź poprzez konwertowanie HTML do obrazu PNG.
- **Odnalezienie powiązań:** zakładając, że budujemy własną bazę wiedzy, zaznaczony tekst może być zamieniony na zapytanie do wyszukiwarki, która natychmiast otworzy powiązane notatki (np. poprzez deep-link / x-scheme-url)
- **Opisanie zaznaczenia:** przy pracy z generowaniem obrazu przydatne jest opisywanie stylu, który może być generowany automatycznie na podstawie zdjęć znajdujących się w schowku systemowym.
- **Lokalizacja zdjęcia:** zdjęcie zrobione w telefonie może być przesłane wraz z metadanymi, na przykład lokalizacją. Na podstawie treści zdjęcia może zostać podjęta określona akcja, np. dopisanie przedmiotu do listy zakupów.

![Przykłady mikro-akcji](https://cloud.overment.com/2026-03-05/ai_devs_4_microactions-fa8c17e9-a.png)

Tworzenie takich akcji zwykle będzie sprowadzało się do utworzenia prostego skryptu i przypisania go do skrótu klawiszowego czy połączenia z aplikacjami do automatyzacji w telefonie, np. Siri Shortcuts. Automatyzacje mogą być też powiązane z konkretnymi katalogami czy przestrzeniami w zdalnych dyskach. Obecnie też bez problemu możemy też wygenerować aplikację desktopową bądź mobilną w Swift / Electron / Tauri / React Native i zyskać dostęp do natywnych funkcjonalności urządzeń. Takie aplikacje nie muszą być udostępniane publicznie, ale być wykorzystywane w naszym prywatnym kontekście.

## Projektowanie własnych meta-promptów

Bezpośrednia współpraca z AI różni się od projektowania systemów agentowych tym, że raczej nie poświęcamy zbyt dużo czasu na pisanie promptów. Niekiedy można spotkać się z opiniami, że projektowanie promptów nie ma już znaczenia z punktu widzenia użytkownika końcowego, ponieważ model i tak zrozumie to, o co nam chodzi. W zamian przeszliśmy do koncepcji generowania planów i specyfikacji, co też jest mocno sugerowane przez narzędzia takie jak Claude Code oraz Cursor w przypadku których tryb ten może włączyć się automatycznie i przeprowadzić nas przez proces opracowania rozbudowanego dokumentu opisującego zadania, które ma wykonać dla nas agent.

Projektowanie agentów pokazało nam, że napisanie instrukcji dzięki której model będzie realizował nie **jedno zadanie**, lecz całą **kategorię zadań** jest dość wymagające, szczególnie jeśli chcemy aby zrobił to za pierwszym razem, bez naszej interwencji. Tym bardziej, że nie chodzi tu wyłącznie o poziom inteligencji modelu, lecz także przekazanie niezbędnej wiedzy, zarysowanie kontekstu czy nadanie reguł, których model zwyczajnie nie posiada. Po zgromadzeniu tych informacji musimy także zadbać np. o ich syntezę czy parafrazę, aby uniknąć powtórzeń czy zwiększyć nacisk na wybrane zachowania. To również bywa czasochłonne i niekiedy również trudne.

Powyższy proces można sprowadzić do serii pytań oraz odpowiedzi, które pozwolą zgromadzić wymagane informacje, a potem ukształtować z nich instrukcję według praktyk, które uznamy za słuszne. Poniżej mamy koncepcyjny schemat meta-promptu którego celem jest **generowanie instrukcji dla agentów** na podstawie **rozmowy z użytkownikiem**. Także nie jest to autonomiczny proces i rola człowieka jest tu fundamentalna. Meta-prompt składa się więc z:

- **Danych:** opisujących kategorie informacji, które powinny zostać zgromadzone od użytkownika. Chodzi tu o rzeczy takie jak **cel, zakres, styl, narzędzia, wzorce, modele mentalne, ograniczenia, format, wyjątki**. Inaczej mówiąc, jest to wszystko to, czego model nie posiada oraz to, na czym powinien się skupić.
- **Generatora:** obejmuje domyślne struktury, zasady specjalizacji oraz generalizacji, przydatne wyrażenia czy obszary na których powinna skupiać się końcowa instrukcja. Znajdziemy więc tutaj wskazówki kształtowania stylu, zachowań czy schematów "myślowych", które normalnie staramy się stosować samodzielnie przy budowie instrukcji agentów. Można o tym myśleć, jak o **wiedzy na temat dobrych praktyk tworzenia promptów** z których tym razem nie korzystamy my, lecz model / agent generujący nowy prompt.
- **Rezultatu:** tutaj zwykle chodzi o rodzaj szablonu bądź komponentów na podstawie których ma powstać końcowa instrukcja. W tym przypadku są to raczej stałe sekcje takie jak **tożsamość, opis procesu myślowego, zasady i ograniczenia, zewnętrzna wiedza oraz styl wypowiedzi**.

![Koncepcja meta-promptu](https://cloud.overment.com/2026-03-05/ai_devs_4_metaprompt-6061f547-a.png)

Przykładową treść jednego z meta-promptów który wykorzystuję jako punkt startowy dla instrukcji agentów można znaleźć [tutaj](https://cloud.overment.com/metaprompt-1772797061.txt) (to plik tekstowy, który powinien zostać pobrany na komputer). Nietrudno zauważyć, że to bardzo rozbudowana instrukcja, głównie ze względu na dużą liczbę przykładów, wyrażeń oraz definicji obszarów, które model powinien rozważyć oraz zasad **dopasowania się** do bieżącego kontekstu.

Ze względu na tak dużą złożoność dość uzasadnione bywa także **rozbicie procesu generowania promptów na oddzielne fazy**. Bo jeśli spojrzymy sobie na strukturę promptu widoczną poniżej, to wyraźnie widać w niej poszczególne etapy, które mogą zostać pogrupowane. Jednocześnie schemat ten pokazuje najważniejsze obszary meta-promptu, takie jak:

- **Proces:** model zostaje na początku poinformowany o tym, że jego celem jest przeprowadzenie użytkownika przez serię pytań w celu ukształtowania instrukcji dla modelu językowego, zgodnie z opisanymi zasadami i szablonem.
- **Strategia:** następnie mamy kilka punktów opisujących strategię realizacji celu, uwzględniając przy tym konieczność dopasowania się do bieżącej sytuacji.
- **Dopasowanie:** ze względu na znaczenie dopasowania, oddzielna sekcja zawiera zasady, które powinny być uwzględnione przy generowaniu promptów agentów specjalizujących się w różnych dziedzinach. Poza tym, należy też uwzględnić specjalne wymagania użytkownika, które niekiedy mogą wykraczać poza domyślną strukturę.
- **Format:** w tej sekcji znajduje się szablon oraz komponenty instrukcji końcowej, a także sposób jej zaprezentowania. Akurat w tym przypadku mówimy o wyświetleniu jej wewnątrz specjalnego bloku markdown, który będzie umożliwiał "instalację" promptu.
- **Zasady:** w związku z tym, że proces generowania promptu opiera się o zadawanie pytań, model musi być poinformowany o tym, jak przeprowadzić przez niego użytkownika. Są tu uwzględnione elementy takie jak **oczekiwanie na odpowiedź** bądź **pogłębianie niejasnych instrukcji**, ponieważ model nie powinien zgadywać czegoś, co powinien otrzymać od użytkownika.
- **Natywne funkcjonalności:** jest to sekcja dodatkowa, występująca akurat w tym meta-prompcie. Dotyczy natywnych funkcjonalności aplikacji, które muszą być wzięte pod uwagę, ponieważ poza wygenerowaniem instrukcji, model musi wygenerować także **ustawienia agenta**, które zostaną potraktowane jako domyślne. Sama koncepcja jest bardzo użyteczna, ponieważ generowanie promptów nie musi sprowadzać się wyłącznie do utworzenia samej instrukcji.
- **Proces generowania:** meta-prompt zawiera wiele instrukcji, przykładów oraz możliwych komponentów końcowej instrukcji. Dlatego w końcowej sekcji znajdują się zasady, które zwracają uwagę na to, że pod uwagę należy brać wyłącznie elementy istotne z punktu widzenia bieżącego kontekstu konwersacji oraz celu użytkownika, a także wskazują, jak powinien wyglądać proces selekcji.
- **Krytyczne zasady:** tak jak już mówiliśmy, na sam koniec instrukcji warto jest podkreślić najważniejsze zasady oraz rzeczy, których chcemy uniknąć. Jeśli możliwe, to część z tych reguł powinna pojawiać się także w metadanych wiadomości użytkownika.

![Przykładowa struktura metapromptu](https://cloud.overment.com/2026-03-06/ai_devs_4_metaprompt_structure-5f0b61c4-c.png)

Koncepcja meta-promptu może na pierwszy rzut oka wyglądać jak coś, co ma bardzo wąskie zastosowanie. Szczególnie jeśli pracujemy z agentami do kodowania, gdzie poza trybem planowania i ewentualnie ustawienia głównych instrukcji AGENTS.md raczej nie zastanawiamy się zbyt dużo nad sposobem prowadzenia konwersacji (co swoją drogą jest błędem, ale też nie chodzi tu o projektowanie rozbudowanych promptów w każdej wiadomości). Natomiast w praktyce, koncepcja meta-promptów będzie pojawiać się bardzo często. Na przykład:

- **Onboarding:** nowi użytkownicy często przechodzą przez proces początkowej konfiguracji aplikacji i na tej podstawie możemy mieć potrzebę stworzenia instrukcji dopasowanych do ich kontekstu, a nie zawsze będzie to możliwe przez logikę kodu. Przykładowo jeśli prowadzimy platformę typu marketplace, gdzie użytkownik może dodać swoje produkty, to najwięcej informacji uzyskamy z ich opisów, strony produktu czy dołączonych zdjęć. Dane te pozwolą na lepszą personalizację np. funkcjonalności generowania opisów czy kreacji reklamowych.
- **Generowanie obrazów:** w narzędziach marketingowych czy sprzedażowych, często będzie pojawiać się potrzeba generowania bądź edycji obrazu w sposób dopasowany do danego produktu oraz tonu marki. Tutaj także generowanie instrukcji będzie bardzo pomocne.
- **Czatboty i agenci:** narzędzia takie jak Claude czy Claude Code już teraz mają meta-prompty do generowania instrukcji dla subagentów lub skilli. Dlatego, niezależnie od tego, czy mówimy o kontekście programistycznym, czy biznesowym, usprawnienie procesu tworzenia promptów jest mile widziane przez użytkowników. Co więcej, może to również wpłynąć na odbiór naszego produktu, ponieważ sama personalizacja może bezpośrednio przełożyć się na jego użyteczność i skuteczność.
- **Optymalizacja:** nawet w przypadku relatywnie prostych mechanik czy agentów wyspecjalizowanych w wybranych obszarach (np. klasyfikacji danych) możemy mówić o strategiach automatycznych optymalizacji. Tutaj także chodzi o zastosowanie koncepcji meta-promptów.

Podsumowując, po raz kolejny przekonujemy się, że pomimo wzrostu możliwości modeli językowych w zakresie rozumienia nawet bardzo ogólnych instrukcji, w praktyce nadal istnieje potrzeba włożenia dużej ilości pracy w ich optymalizację. Tym bardziej że od jakości tych promptów zależy skuteczność modeli, a w rezultacie także wartość, jaką daje nam AI w codziennej pracy oraz w produktach, które będziemy tworzyć.

## Fabuła

![https://vimeo.com/1177414973](https://vimeo.com/1177414973)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze piąty!

Mamy już turbinę. Jest gotowa do produkcji prądu, ale jak to zwykle bywa, jest pewien haczyk. Nie udało nam się zdobyć do niej nowego akumulatora zasilającego, więc ten, który mamy działa już na rezerwie. Nie mamy też odpowiedniej ładowarki, a z częściami, którymi dysponujemy, raczej niczego nie wykombinujemy. W zespole brakuje nam MacGyvera, więc pomysł z budową ładowarki ze spiczaczy biurowych także odpada.

Musimy więc ustalić konkretny dzień i konkretną godzinę, kiedy uruchomimy naszą turbinę i zaczniemy produkcję prądu niezbędnego do rozruchu komputerów sterujących. Elektrownia raportuje przez API, jakie ma obecnie niedobory prądu - jest to zmienne w czasie, więc zwróć na to uwagę! Musimy wyliczyć, na podstawie prognozy pogody, kiedy warunki atmosferyczne będą optymalne do wyprodukowania wymaganej mocy.

Musisz znaleźć pierwsze możliwe okno pogodowe, ponieważ zależy nam na czasie. Z tego, co widziałem w prognozie, czekają nas jeszcze spore zawieruchy i jest szansa, że połamią one nasz nowy nabytek.

Istnieje jednak sposób na przetrwanie takich wichur. Wystarczy ustawić łopaty wirnika w taki sposób, aby nie stawiały oporu wiatrowi. To je ocali.

Przeanalizuj proszę prognozę pogody i określ, kiedy konkretnie czekają nas ogromne wichury. Ustaw łopaty wirnika w taki sposób, aby je przetrwały. Następnie znajdź pierwszy moment, kiedy jesteśmy w stanie wyprodukować potrzebną nam moc. Wyślij taką konfigurację do API centrali.

Musisz wiedzieć, że wirnik mniej więcej godzinę po każdej większej wichurze wraca do standardowego ustawienia, więc czasami będzie wymagał on kilkukrotnego włączenia trybu ochronnego.

Mamy też pewien problem, który nazwałbym "walką z czasem". Pamiętasz o umierającej baterii systemu sterowania turbiną? Przez tą baterię jesteśmy w stanie włączyć Ci okno serwisowe do konfiguracji tego urządzenia tylko na kilkadziesiąt sekund, a Ty przez ten czas musisz pobrać wszystkie niezbędne informacje przez nasze API, a następnie zaprogramować harmonogram pracy urządzenia i zgłosić do Centrali, że konfiguracja jest już gotowa.

Jeśli wszystko pójdzie zgodnie z planem, to znaczy, że już w tym tygodniu będziemy gotowi na rozpoczęcie produkcji prądu. Więcej informacji, jak zawsze, znajdziesz w notatce do tego filmu.

## Zadanie praktyczne

Twoim zadaniem jest zaprogramowanie harmonogramu pracy turbiny wiatrowej w taki sposób, aby uzyskać moc niezbędną do uruchomienia elektrowni.

Elektrownia nie może pracować przez cały czas, ponieważ jej bateria na to nie pozwoli. Musisz więc uruchomić jej system tylko wtedy, gdy naprawdę będzie wymagany. Jesteś w stanie znaleźć idealny czas poprzez analizę wyników prognozy pogody.

Dostarczone przez nas API dają Ci też informacje na temat stanu samej turbiny oraz na temat wymagań elektrowni. Przygotowanie raportu do każdej z funkcji wymaga czasu. Nie jesteśmy w stanie powiedzieć, ile konkretnie czasu zajmie wykonanie danej funkcji, ale wywołania te są kolejkowane. Później musisz tylko wywołać funkcję do pobierania wygenerowanych raportów.

Każdy wygenerowany raport da się pobrać tylko jednokrotnie. Jeśli uda Ci się wszystko skonfigurować w czasie **40 sekund**, to jesteśmy uratowani i możemy przejść do fazy produkcji prądu.

Nazwa zadania: **windpower**

Odpowiedź wysyłasz do /verify

> **UWAGA**: to zadanie posiada limit czasu (40 sekund), w którym musisz się zmieścić. Liniowe wykonywanie wszystkich akcji nie umożliwi Ci ukończenia zadania.

Z API porozumiewasz się w ten sposób:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "windpower",
  "answer": {
    "action": "..."
  }
}
```

Sugerujemy od rozpoczęcia:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "windpower",
  "answer": {
    "action": "help"
  }
}
```

Zanim przystąpisz do konfiguracji turbiny wiatrowej, musisz uruchomić okno serwisowe poprzez wydanie polecenia:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "windpower",
  "answer": {
    "action": "start"
  }
}
```

Przykładowe wysłanie konfiguracji może wyglądać tak - **w godzinie zawsze ustawiaj minuty i sekundy na zera**.

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "windpower",
  "answer": {
    "action": "config",
    "startDate": "2238-12-31",
    "startHour": "12:00:00",
    "pitchAngle": 0,
    "turbineMode": "idle",
    "unlockCode": "tutaj-podpis-md5-z-unlockCodeGenerator"
  }
}
```

Możesz także wysłać wiele konfiguracji za jednym razem - inny format danych.

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "windpower",
  "answer": {
    "action": "config",
    "configs": {
      "2026-03-24 20:00:00": {
        "pitchAngle": 45,
        "turbineMode": "production",
        "unlockCode": "tutaj-podpis-1"
      },
      "2026-03-24 18:00:00": {
        "pitchAngle": 90,
        "turbineMode": "idle",
        "unlockCode": "tutaj-podpis-2"
      }
    }
  }
}
```

### Co musisz zrobić

- Odczytaj z prognozy pogody wszystkie momenty, w których wiatr jest bardzo silny i może zniszczyć łopaty wiatraka. Zabezpiecz wtedy turbinę (odpowiednie nachylenie łopat i odpowiedni tryb pracy).
- Wyznacz punkt, w którym możliwe jest wygenerowanie brakującej energii i ustaw tam optymalne nachylenie łopat wirnika i poprawny tryb pracy umożliwiający produkcję prądu.
- Każda przesłana do API konfiguracja musi być cyfrowo podpisana. Mamy jednak generator kodów, który takie kody dla Ciebie wygeneruje - unlockCodeGenerator, a wygenerowane kody wyślij razem z konfiguracją.
- Zapisz konfigurację przez "config".
- Na końcu wyślij akcję o nazwie "done", która sprawdzi, czy Twoja konfiguracja jest poprawna.

### Dodatkowe uwagi

- Większość funkcji działa asynchronicznie. Najpierw dodajesz zadanie do kolejki, potem odbierasz wynik przez action "getResult". Odpowiedzi przychodzą w losowej kolejności.
- Za wichurę uznajesz wiatr powyżej wytrzymałości wiatraka.
- Przy wichurze turbina nie powinna stawiać oporu i nie może produkować prądu.
- Przed finalnym "done" musisz wykonać test turbiny przez "turbinecheck".
- Każdy punkt konfiguracji musi mieć poprawny unlockCode z funkcji "unlockCodeGenerator".

Jeśli konfiguracja będzie poprawna i zmieścisz się w czasie, Centrala odeśle flagę.
