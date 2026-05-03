---
title: S02E03 — Dokumenty oraz pamięć długoterminowa jako narzędzia
space_id: 2476415
status: scheduled
published_at: '2026-03-18T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/thinking-1773302525.png'
circle_post_id: 30573309
---
![https://vimeo.com/1172919468](https://vimeo.com/1172919468)

Personalizacja zachowań agentów poprzez system pamięci z jednej strony pozostaje nierozwiązanym problemem, a z drugiej już teraz możemy osiągnąć bardzo wysoką skuteczność, zachowując elastyczność i niską złożoność.

Łącznie LLM z bazą wiedzy niemal zawsze utożsamiane jest z podłączaniem **istniejących dokumentów**. Oznacza to, że ich treść raczej była projektowana z myślą o człowieku. Dlatego tym razem odwrócimy ten proces i skupimy się na **tworzeniu bazy wiedzy**. Dzięki temu zyskamy możliwość kontroli nad kształtowaniem i organizacją dokumentów i dopasować te procesy do naszego systemu.

**Plan na dziś:**
...

## Wyzwania procesu przeszukiwania dostępnych zasobów

W poprzednich lekcjach powiedzieliśmy już sporo na temat problemu wyszukiwania informacji dostępnych w bazie wiedzy. Problem ten, w uproszczeniu, można sprowadzić do trudności wygenerowania przez LLM zapytań, które pozwolą skutecznie dotrzeć do potrzebnych informacji. Jednak w rzeczywistości problem ten nie dotyczy wyłącznie ich odnalezienia, ale także **zrozumienia ich w szerszym kontekście**.

Poniżej mamy przykład sytuacji w której w rzeczywistości (lewa strona) dokumenty są ze sobą **powiązane**. Jednak w praktyce (prawa strona), agent dociera tylko do pierwszego z nich, bez pogłębiania wyszukiwania, ponieważ **doc\_B** może wyglądać na kompletny.

![Problem rozumienia dokumentu w szerszym kontekście](https://cloud.overment.com/2026-02-10/ai_devs_4_gap-96e11ee3-4.png)

Można pomyśleć, że wystarczy „zmiana” w prompcie, aby agent dokładniej przeszukiwał dokumenty. Jednak dobre zrozumienie kontekstu może wymagać przeczytania nawet dziesiątek dokumentów, a nawet to może okazać się niewystarczające, by uchwycić pełny obraz.

Problem, o którym tutaj mówimy, jest obecnie **otwarty**, więc nie znamy definitywnego rozwiązania. Jednocześnie jest on na tyle istotny, że już dziś można znaleźć wiele materiałów na jego temat. Jednym z przykładów jest publikacja [LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory](https://arxiv.org/pdf/2410.10813), która dość dokładnie opisuje kluczowe problemy, szczególnie dotyczące budowania pamięci w wymiarze wykraczającym poza pojedyncze sesje.

Ale co gdyby spojrzeć na ten problem inaczej i zamiast dążyć do rozwiązania jego poszczególnych elementów, **po prostu je wyeliminować?**

Jedna z najbardziej skutecznych strategii została przedstawiona ostatnio przez Mastra.ai pod nazwą [Observational Memory](https://mastra.ai/blog/observational-memory). Jej idea jest niezwykle prosta i możemy się z niej wiele nauczyć. Tym bardziej, że całkowicie pomija ona wyszukiwanie semantyczne czy konieczność budowania grafów (aczkolwiek nie wyklucza ich zastosowania).

Główne założenia OM opierają się na uruchomieniu dwóch rodzajów zapytań **Observer** i **Reflector**, których celem jest zapisanie obserwacji w formie **dziennika "logów** oraz opisu bieżącego zadania. Dziennik ten składa się z bardzo precyzyjnych i zwięzłych wpisów stanowiących esencję bieżącej interakcji. Przykład takiej notatki znajduje się poniżej.

![Przykład dziennika logów z Observational Memory](https://cloud.overment.com/2026-02-10/ai_devs_4_observational_memory-aaa1f996-0.png)

Generowanie takiej notatki zostaje uruchomione **po przekroczeniu 30 000 tokenów** w bieżącej rozmowie. Wówczas uruchamiany jest **Observer**, który otrzymuje **bieżący dziennik logów (jeśli istnieje) oraz listę najnowszych wiadomości**. Po wygenerowaniu najnowszej wersji dziennika wiadomości zostają oznaczone jako "zapieczętowane" i usunięte z bieżącej konwersacji, a efekt pracy Observera zostaje dołączony na końcu wiadomości systemowej. Natomiast gdy sam dziennik logów przekroczy **60 000 tokenów**, to jego treść (i tylko ona) zostaje przekazana do **Reflectora**, którego zadaniem jest skompresowanie dziennika.

![Schemat działania Observational Memory](https://cloud.overment.com/2026-02-10/ai_devs_4_observer_reflector-90bac67f-2.png)

Powyższy schemat powtarza się w nieskończoność i wykracza poza pojedynczą sesję, ponieważ „niezapieczętowane” wiadomości wraz z najnowszą wersją dziennika mogą być dołączane do nowej sesji.

W tak prosty sposób osiągamy rezultat, który zalicza **[LongMemEval](https://github.com/xiaowu0162/LongMemEval)** na poziomie **94.87%** z modelem gpt-5-mini (!). Oczywiście trzeba mieć tu na uwadze fakt, że mamy tutaj do czynienia z **kompresją**, więc z czasem część wspomnień naturalnie zostaje zapomniana (poniekąd podobnie jak u ludzi). Natomiast wyniki mówią tu same za siebie i nawet na poziome teoretycznym widać, że ta koncepcja ma mocne fundamenty, aby działać. Poza tym, nikt nie powiedział, że agent nie może posiadać narzędzi do wczytywania wcześniejszych wspomnień.

Niezależnie od tego, czy będziemy korzystać z Observational Memory, czy nie, schemat myślenia którym podążali jego autorzy jest tym, na którym w AI\_devs najbardziej nam zależy. Kod źródłowy projektu można znaleźć [na Githubie](https://github.com/mastra-ai/mastra).

## Kategoryzacja oraz mapa obszarów bazy wiedzy

Nawigowanie po nawet względnie małej bazie wiedzy nie jest oczywiste. Zawarte w niej informacje zwykle są rozproszone w wielu dokumentach, co, nawet po zbudowaniu "mapy", utrudnia dotarcie do całej niezbędnej wiedzy. Wszystko jeszcze bardziej się komplikuje, gdy dane są aktualizowane bądź gdy się dezaktualizują.

Sytuacja odwraca się, gdy baza wiedzy nie zostaje podłączona do agentów, lecz **zbudowana dla nich** oraz przypisanych do nich procesów. Wówczas w ogóle nie dotykamy problemu **odnajdywania** informacji. Każdy agent posiada jedynie dostęp do tego, czego potrzebuje. Nawet jeśli pojawia się potrzeba sięgnięcia po **ogólne dane**, to przy możliwościach obecnych modeli wystarczy jedynie odnośnik do katalogu bądź konkretnego pliku.

W przypadku generowanych baz wiedzy rzadko występują też problemy związane ze zbyt obszernymi dokumentami lub formatami plików. Nawet jeśli agent generuje pliki PDF lub DOCX, to zwykle mają one charakter końcowy, a ich ponowne odczytywanie i modyfikowanie nie są już potrzebne.

Poniżej mamy porównanie połączenia z **istniejącą** bazą wiedzy i **tworzoną** z myślą o agentach. W pierwszym przypadku agent **ma szansę** trafić na właściwe dokumenty. Natomiast w drugiej wprost wie, gdzie się one znajdują. Nie chodzi tu jednak o specyficzną instrukcję np. **"proces zarządzania zadaniami w Linear opisany jest w katalogu (...)**", lecz bardziej generyczną "**instrukcje obsługi Twoich narzędzi znajdziesz w ./workflows**".

![Różnica pomiędzy przeszukiwaniem istniejącej bazy, a tworzeniem bazy dla agenta](https://cloud.overment.com/2026-02-10/ai_devs_4_generated_knowledge-fa68663c-a.png)

Załóżmy teraz, że **agent „Task Manager”**: otrzymuje informację, że instrukcje obsługi narzędzi znajdzie w katalogu **workflows**. Poproszony o dopisanie zadania, wczytuje instrukcję z zasadami przypisywania i opisywania zadań. Wśród jej punktów znajduje wzmiankę, że informacje o projektach znajdzie w katalogu **projects/overview.md**. Po zapoznaniu się z nią dowiaduje się, że jeden z projektów jest powiązany z zadaniem, które ma dodać. Dodaje więc wpis do Linear, przypisany do właściwego projektu.

Taki proces nieco bliżej, prezentuje się następująco:

![Schemat eksploracji informacji według procedur stworzonych z myślą o agentach AI](https://cloud.overment.com/2026-02-10/ai_devs_4_exploration-6e2a83e8-4.png)

Agent przechodzi krok po kroku przez kolejne wskazówki opisane w dokumentach. Nawet jeśli taka ścieżka będzie dość rozbudowana, to nadal agent porusza się jedynie po wybranych fragmentach bazy wiedzy.

Takie podejście ma jeszcze jedną zaletę, dotyczącą kompozycji informacji. Bo jeśli w ramach danego projektu pojawi się na przykład nowa kategoria zadań, to wystarczy zaktualizować tylko jeden wpis, a całą reszta procesu dostosuje się samodzielnie. Oczywiście wymaga to dużej dyscypliny i choć w organizacji może pomagać AI, to na tym etapie nie może jeszcze przejąć tego procesu w całości.

Samo skalowanie tego podejścia oczywiście ma swoje limity. Przełożenie bardzo złożonych procesów oraz uwzględnienie rozbudowanych interakcji z ludźmi, ujawnia różnego rodzaju wyzwania. Jednocześnie nikt nie powiedział, że agenci AI od razu mają przejmować kompletne procesy, a nie ich pojedyncze elementy, gdzie nadal mogą wnosić ogromną wartość.

## Prezentowanie dostępnych zasobów dla modelu

Podejście o którym teraz mówiliśmy występuje naturalnie w przypadku **kodu źródłowego** po którym nawigują agenci do kodowania. Ci, wyposażeni jedynie w wiedzę o ścieżce do katalogu roboczego oraz ewentualnie zmodyfikowanych plikach w git, potrafią bardzo skutecznie (ale nie bezbłędnie) poruszać się po plikach projektu.

Przyjrzyjmy się temu bliżej.

Poniżej znajduje się schemat prezentujący agenta reagującego na prośbę dodania pola "**bio**" do profilu użytkownika. Jeśli projekt jest duży, tak krótka wiadomość może być potencjalnie niewystarczająca. Zwykle jednak wystarczy wykonać nawet kilka losowych
"grepów", aby dotrzeć przynajmniej do jednego pliku powiązanego z "**profilem użytkownika**". Wtedy dotarcie do reszty logiki jest zazwyczaj proste, ponieważ wystarczy podążać za importowanymi plikami lub za nawet najmniejszymi wskazówkami, takimi jak nazwa funkcji czy ścieżki API, aby odkryć wszystkie zależności.

![Przykład agenta nawigującego po kodzie źródłowym](https://cloud.overment.com/2026-02-11/ai_devs_4_imports-85a5e7a9-4.png)

Okazuje się zatem, że **mapą** według której porusza się agent, jest ponownie **zawartość pliku**. Agent nie musi widzieć całej struktury projektu. A jeśli tylko ma taką potrzebę, to w każdej chwili może ją sprawdzić na przykład poleceniem "**ls**". Mówimy więc tutaj o więcej niż **jednym** sposobie nawigowania po treściach, a konkretnie:

- **perspektywie:** czyli spojrzeniu "z lotu ptaka" na dostępne materiały
- **nawigacji**: czyli przeszukiwaniu zarówno nazw plików jak i ich treści
- **powiązaniach:** czyli odnośnikach pomiędzy plikami
- **szczegółach:** czyli opcji czytania oryginalnej treści dokumentu

Jest to więc sytuacja w której **ekspozycja zewnętrznego kontekstu, opiera się o informacje zawarte wewnątrz oryginalnych treści dokumentu**. Zjawisko to występuje naturalnie w kodzie, ale jest dość rzadko spotykane poza nim. Wyjątek stanowią strony Internetowe z bardzo bogatym linkowaniem wewnętrznym (np. Wikipedia) bądź odpowiednio prowadzone projekty typu Second Brain czy Digital Garden, które zwykle oparte są o Obsidian, Roam Research czy Logseq.

Natomiast w większości treści biznesowych, takich jak dokumentacje, maile, transkrypcje spotkań, dokumenty finansowe, marketingowe czy strategiczne, takie powiązania występują zdecydowanie rzadziej albo wcale. Jednak co w sytuacji, gdyby agent zamiast być podłączany do zewnętrznych informacji **uczył się ich** poprzez zapamiętywanie?

Poniżej mamy schemat porównujący **łączenie ze źródłem** (poprzez chunki) z **nauką ze źródła**. W tym pierwszym przypadku model widzi kontekst nie tylko pozbawiony powiązań i to przez pryzmat **chunków**. Natomiast w drugim, dane są zaprezentowane tak, aby agent mógł sprawnie po nich nawigować.

![Porównanie połączenia ze źródłem z nauką ze źródła](https://cloud.overment.com/2026-02-11/ai_devs_4_learning-31a263c3-d.png)

Powyższy przykład **nie oznacza**, że agent może magicznie "nauczyć się" wszystkiego (przynajmniej nie teraz), ponieważ, jak powiedzieliśmy, dynamiczne budowanie pamięci pozostaje jeszcze problemem otwartym. Jednak stworzenie agentów wyspecjalizowanych w organizacji określonych rodzajów dokumentów (na przykład transkrypcji spotkań) jest realne, choć mówimy tu o dedykowanym rozwiązaniu.

Stając przed problemem prezentacji zewnętrznego kontekstu modelowi, możemy wpaść na pomysł wyświetlenia **struktury katalogów** bądź **drzewa kategorii**. Coś takiego może okazać się pomocne, ale tylko w sytuacji, gdy **struktura pozostaje stała** podczas interakcji, a dany agent skupia się wyłącznie na jej interakcji. W przeciwnym razie takie informacje będą albo wprowadzać model w błąd, albo niepotrzebnie zajmować kontekst przez większość czasu.

Podsumowując, sposób prezentowania zewnętrznych treści dla modelu zwykle będzie **dynamiczny**, a ujawnianie kolejnych informacji będzie wynikało z **powiązań pomiędzy dokumentami** zawartymi w ich treści. Ale i tak pojawia się tu wiele wyzwań, które albo wymagają **dopasowania systemu** albo po prostu pozostają jeszcze bez konkretnej odpowiedzi.

## Rola bazy wiedzy w interakcji z otoczeniem

Działania agentów nie zawsze będą obejmować proste interakcje z otoczeniem. Część z nich może być rozłożona w czasie i angażować różne skrypty, agentów, bądź ludzi. Zgromadzone w ten sposób dane, mogą stać się źródłem informacji do kolejnych działań.

Przykładowo:

1. Agent "Researcher" otrzymuje prośbę o przeczytanie instrukcji **news.md** opisującą zasady gromadzenia materiałów na potrzeby newslettera oraz **blogs.md** zawierającą listę blogów wraz z opisem rodzajów treści, które mają zostać zapisane.
2. Agent "Researcher" otrzymuje **drugą** prośbę o podobne działanie, ale z innym źródłem danych, na przykład kanałach YouTube.
3. Agent "Researcher" otrzymuje **trzecią**, tym razem ukierunkowaną na przejrzenie newsletterów z ostatniego dnia.

Ten sam agent zostaje uruchomiony **w trzech oddzielnych sesjach**, lecz fakt przeczytania tej samej instrukcji sprawia, że zebrane dane zostały zapisane w tym samym katalogu, na przykład **newsletter/edition-26/nazwa-pliku.md**.

Po zakończeniu tego etapu, zadanie zostaje przekazane do kolejnych agentów:

1. Agent "Writer" otrzymuje prośbę o zapoznanie się z treścią folderu **newsletter/edition-26** oraz pliku **daily-newsletter.md**, który opisuje zasady tworzenia codziennego newslettera na podstawie zgromadzonych informacji.
2. Agent "Sender" otrzymuje prośbę o przeczytanie pliku **newsletter/edition-26/content.md** oraz przesłanie jej do wskazanej osoby, bądź osób (na przykład zespołu).

Całość prezentuje się następująco:

![Przykład współpracy pomiędzy agentami tworzącymi spersonalizowany newsletter](https://cloud.overment.com/2026-02-11/ai_devs_4_personalized_newsletter-86904b5a-f.png)

**Uwaga:** generowanie newsletterów wysyłanych w ten sposób do list mailingowych powinno być **bezwzględnie weryfikowane przez człowieka**. Agent powinien mieć uprawnienia **jedynie do utworzenia szkicu kampanii**. W przeciwnym razie narażamy się na problemy związane z halucynacją i prompt injection, które mogą prowadzić do fatalnych konsekwencji (na przykład przekierowania odbiorców na zainfekowaną stronę).

Powyższy przykład newslettera, może być z powodzeniem przełożony na **aktualizacje zespołu**, **miesięczne newslettery produktowe** czy **spersonalizowane aktualizacje dla sprzedawców** na temat klientów.

Szczególnym elementem powyższego procesu jest fakt, że jego poszczególne etapy odbywały się w **indywidualnych sesjach** przez co agenci byli skupieni wyłącznie na wybranym zadaniu. Taka dekompozycja pozwala utrzymać wysoką jakość, a jednocześnie jest dość optymalna kosztowo (płacimy wyłącznie za wielokrotne wczytanie tych samych instrukcji na etapie gromadzenia danych).

## Mapowanie treści z wykorzystaniem grafów

Zdolność agentów do eksplorowania rozbudowanych treści coraz lepiej łączy się z koncepcją grafów. Możemy więc zastosować bazę grafową [neo4j](https://neo4j.com/), która pozwoli nam nie tylko na indeksowanie treści, ale także **wyszukiwania pełnotekstowego** oraz **semantycznego**. Mówimy zatem o **hybrydowym RAGu w logice agentów**!

Zacznijmy jednak od krótkiego wprowadzenia. Grafy w Neo4j to tak zwane **grafy właściwości** i stanowią model danych składający się z:

- **wierzchołków (node)**, czyli obiektów posiadających właściwości oraz etykiet,
- **krawędzi (edge)**, czyli połączeń między tymi obiektami i posiadają kierunek, jeden typ i mogą posiadać właściwości. Każde połączenie łączy ze sobą dokładnie **dwa** wierzchołki.

![Przykład prostego grafu](https://cloud.overment.com/2026-02-11/ai_devs_4_graphs-dcb0ecee-9.png)

> **Uwaga:** Dla wielu z Was praca z bazami grafowymi może być czymś nowym. W jej konfiguracji, debugowaniu czy składni Cypher bardzo skutecznie może pomagać LLM.

Dla nas oznacza to, że możemy opracować agenta z dostępem do narzędzi, które pozwalają zarządzać grafem i nawigować po nim. I dokładnie takiego agenta przedstawia przykład **02\_03\_graph\_agents**. Aby go uruchomić, konieczne będzie zainstalowanie Dockera oraz uruchomienie Neo4j zgodnie z instrukcją z pliku README.md. Następnie, po włączeniu agenta poleceniem **npm start**, zobaczymy proces **indeksowania** artykułu z katalogu **workspace**.

Po zaindeksowaniu możemy zadać pytanie dotyczące artykułu, na przykład: "**How does David Shapiro's work relate to prompt engineering?**". Wówczas agent przeszuka graf oraz będzie nawigować po jego strukturze, aby odnaleźć komplet informacji potrzebnych do udzielenia odpowiedzi.

![Przykład działania agenta posługującego się grafem jako pamięcią](https://cloud.overment.com/2026-02-11/ai_devs_agentic_graph_rag-6892e38c-c.png)

Aby lepiej zrozumieć działanie tego agenta, spórzmy na narzędzia, którymi dysponuje. Są one podzielone na trzy kategorie: **przeszukiwanie, indeksowanie** oraz **zarządzanie**. Agent ma także możliwość wykonywania zapytań Cypher, ale ograniczonych wyłącznie do **odczytywania** danych. Wśród narzędzi znajdują się:

- **search**: umożliwia przeszukiwanie fragmentów dokumentów z pomocą BM25 oraz wyszukiwania wektorowego. Zwraca listę fragmentów oraz powiązane z nimi węzły.
- **explore**: umożliwia pobranie sąsiadujących węzłów
- **connect**: umożliwia odnalezienie najkrótszej ścieżki pomiędzy węzłami
- **cypher**: umożliwia wykonywanie zapytań Cypher (read-only)
- **learn**: umożliwia dodanie nowych danych z pliku bądź przekazanej wiadomości
- **forget**: umożliwia usunięcie informacji
- **audit**: ułatwia weryfikowanie poprawności grafu (np. poprzez niepowiązanych węzłów)
- **merge\_entities**: ułatwia weryfikowanie poprawności grafu (np. wykrywanie duplikatów)

![Narzędzia agenta posługującego się grafem](https://cloud.overment.com/2026-02-11/ai_devs_4_agentic_graph_tools-4c483f7d-c.png)

Mamy więc tutaj komplet najważniejszych narzędzi do pracy z grafem. Same bazy grafowe, w takiej konfiguracji, są jednym z najbardziej kompleksowych rozwiązań w kontekście podłączania baz wiedzy do LLM. Jednocześnie złożoność tego podejścia, koszt utrzymania (nie tylko finansowy) oraz czas potrzebny na generowanie odpowiedzi, są na tyle duże, że raczej tylko w uzasadnionych przypadkach będziemy chcieli po nie sięgnąć.

Bazy grafowe sprawdzą się nam w sytuacji, gdy priorytetem będą **wielopoziomowe powiązania** pomiędzy informacjami rozproszonymi w wielu dokumentach, uwzględniając przy tym praktycznie każdy rodzaj wyszukiwania. Bazy grafowe są także dobrym kandydatem do dynamicznego budowania pamięci, czego próby podejmują projekty takie jak [mem0](https://docs.mem0.ai/open-source/features/graph-memory) czy [supermemory](https://supermemory.ai/docs/integrations/supermemory-sdk).

## Generowanie długich form tekstowych, według ustalonych zasad

Agenci AI stają się coraz lepsi w generowaniu rozbudowanych treści, co możemy zaobserwować między innymi w ChatGPT czy Gemini, na przykładzie funkcjonalności **Deep Research**. Jej celem jest opracowanie obszernego dokumentu opartego głównie na treściach znalezionych w Internecie (albo innych, zewnętrznych źródłach). Nie mówimy jednak wyłącznie o wyszukaniu i zapisaniu informacji, lecz także o **pogłębionych wyszukiwaniach**, które umożliwiają dotarcie do treści niewyświetlonych przy wcześniejszych zapytaniach czy **analizach** realizowanych przez **uruchamianie kodu**. Obecnie coraz częściej mówimy tutaj także o zastosowaniu logiki agentów, obejmującej **planowanie**, **syntezę** czy **weryfikację** finalnego dokumentu. Cały proces często trwa nawet **kilkadziesiąt minut** (i jest realizowany "w tle").

Obecnie funkcjonalności Deep Research dostępne są także w API [OpenAI](https://developers.openai.com/api/docs/guides/deep-research), [Gemini](https://ai.google.dev/gemini-api/docs/deep-research) czy na przykład [Firecrawl](https://docs.firecrawl.dev/features/alpha/deep-research#completed). Zwykle rekomenduje się je do przeprowadzania pogłębionych wyjaśnień wybranych tematów, analiz rynkowych czy generowania rozbudowanych raportów. Ze względu na zaawansowany charakter tych operacji, zaleca się, aby oryginalne zapytanie użytkownika było **doprecyzowane** przez pytania pogłębiające i nierzadko **sparafrazowane**.

![Doprecyzowywanie oraz parafraza zapytania użytkownika przed Deep Research](https://cloud.overment.com/2026-02-12/ai_devs_4_rephrasing-e4272053-6.png)

Doprecyzowywanie zapytania może uwzględniać także **wstępne przeszukiwanie** w celu **zawężenia kontekstu zapytania** oraz **wzbogacenia kontekstu modelu**. Takie techniki mogą pojawić się nie tylko przy okazji korzystania z Deep Research, ale także przy każdym zadaniu, które nie wymaga natychmiastowej reakcji i może zyskać na precyzyjnie sformułowanym zapytaniu.

Rozbudowane zapytanie początkowe jest przekazywane do logiki agenta, którego zadaniem jest **dekompozycja zapytania**, **przeszukiwanie**, **analiza**, **identyfikacja brakujących elementów** oraz przeprowadzenie kolejnej iteracji w celu pogłębienia analizy, aż do momentu uzyskania pełnego raportu.

![Mechanika Deep Research](https://cloud.overment.com/2026-02-12/ai_devs_4_deepresearch-0f1da77b-3.png)

Podobny schemat można przełożyć na inne kategorie zadań, w przypadku których wymagane jest opracowanie **dłuższego formatu treści** oraz **eksploracja przez pogłębianie zapytań**. Przykładami mogą być procesy związane z generowaniem kodu czy audytami. W myśleniu o potencjalnych zastosowaniach bardzo pomaga też zmiana nazwy z "deep research" na "deep action".

Implementacją podobnych mechanik zajmowaliśmy się przy okazji jednego z wydarzeń AI\_devs 3. Tam tworzyliśmy spersonalizowanego agenta deep research, zdolnego do pracy wyłącznie na naszych danych. Jego kod źródłowy jest publicznie dostępny pod [tym adresem](https://github.com/iceener/aidevs-deeper), a główna logika agenta znajduje się w [pliku deep.service.ts](https://github.com/iceener/aidevs-deeper/blob/main/src/services/agent/deep.service.ts). Co prawda agent ten nie generuje kilkusetstronicowych raportów, ale jego logika jest na tyle prosta, aby zrozumieć najważniejsze mechaniki stanowiące fundament "deep actions".

## Fabuła

![https://vimeo.com/1171811350](https://vimeo.com/1171811350)

## Transkrypcja filmu z Fabułą

> Technicy powiedzieli, że załadowanie baterii przy takiej mocy elektrowni, jaką udało nam się uzyskać, zajmie przynajmniej 2 tygodnie. Wcześniej i tak nie uda mi się wykonać skoku w czasie.
>
> Mógłbym powiedzieć, że jedyne, czego teraz potrzebujemy, to cierpliwość, ale nie będzie to prawda.
>
> Uruchomiliśmy elektrownię. System wystartował, ale po drodze nie wszystko poszło gładko. Technicy rozpoczęli uruchamianie systemu w okolicach godziny szóstej rano. Elektrownia samoczynnie wyłączyła się tuż przed dwudziestą drugą. Nie mamy pojęcia, co się stało, a też nie chcemy sprawdzać każdego podzespołu z osobna.
>
> Ale mamy logi z całej operacji!
>
> Jednak ilość danych do analizy jest po prostu za duża, aby wrzucić to do naszych systemów analitycznych, którymi dysponujemy. Pamiętasz o rozmiarze okna kontekstowego, prawda? No właśnie. My dysponujemy znacznie lepszym sprzętem, więc okno jest może i o rząd wielkości większe niż ostatnio, ale to i tak za mało, by przeprowadzić analizę.
>
> Wierzę, że jesteś w stanie przygotować dla nas skrócony opis tego, co wydarzyło się w systemie. Musisz wykazać się swoimi zdolnościami kompresji danych. Interesują nas tylko te naprawdę ważne wpisy z logów... wiesz... system jest gadatliwy, ale przecież nie wszystko jest ważne.
>
> Zoptymalizujesz dla nas ten kontekst?
>
> W notatce pod nagraniem znajdziesz więcej informacji na temat tego, czego potrzebujemy.

## Zadanie

Wczoraj w elektrowni doszło do awarii. Masz dostęp do pełnego pliku logów systemowych z tego dnia - ale jest on ogromny. Twoje zadanie to przygotowanie skondensowanej wersji logów, która:

- zawiera wyłącznie zdarzenia istotne dla analizy awarii (zasilanie, chłodzenie, pompy wodne, oprogramowanie i inne podzespoły elektrowni),
- mieści się w **1500 tokenach**,
- zachowuje format wieloliniowy - jedno zdarzenie na linię.

Skondensowane logi wysyłasz do Centrali. Technicy weryfikują, czy na ich podstawie można przeprowadzić analizę przyczyny awarii. Jeśli tak - otrzymujesz flagę.

**Nazwa zadania: `failure`**

#### Skąd wziąć dane?

Pobierz pełny plik logów:

```
https://hub.ag3nts.org/data/tutaj-twój-klucz/failure.log
```

#### Jak wysłać odpowiedź?

Metodą POST na `https://hub.ag3nts.org/verify`:

```json
{
  "apikey": "tutaj-twój-klucz",
  "task": "failure",
  "answer": {
    "logs": "[2026-02-26 06:04] [CRIT] ECCS8 runaway outlet temp. Protection interlock initiated reactor trip.\\n[2026-02-26 06:11] [WARN] PWR01 input ripple crossed warning limits.\\n[2026-02-26 10:15] [CRIT] WTANK07 coolant below critical threshold. Hard trip initiated."
  }
}
```

Pole `logs` to string - wiersze oddzielone znakiem `\n`. Każdy wiersz to jedno zdarzenie.

#### Wymagania formatowe

- **Jeden wiersz = jedno zdarzenie** - nie łącz wielu zdarzeń w jednej linii
- **Data w formacie YYYY-MM-DD** - technicy muszą wiedzieć, którego dnia zdarzenie miało miejsce
- **Godzina w formacie HH:MM lub H:MM** - żeby umieścić zdarzenie w czasie
- **Możesz skracać i parafrazować** - ważne żeby zachować: znacznik czasu, poziom ważności i identyfikator podzespołu
- **Nie przekraczaj 1500 tokenów** - to twarde ograniczenie systemu Centrali. Możesz sprawdzić liczbę tokenów na <https://platform.openai.com/tokenizer>

### Co należy zrobić w zadaniu?

1. **Pobierz plik logów** - sprawdź jego rozmiar. Ile ma linii? Ile tokenów zajmuje cały plik?
2. **Wyfiltruj istotne zdarzenia** - z tysięcy wpisów wybierz tylko te dotyczące podzespołów elektrowni i awarii. Jak można stwierdzić które zdarzenia istotnie przyczyniły się do awarii? Które są najważniejsze?
3. **Skompresuj do limitu** - upewnij się, że wynikowy plik mieści się w 1500 tokenach. Możesz skracać opisy zdarzeń, byleby zachować kluczowe informacje.
4. **Wyślij i przeczytaj odpowiedź** - Centrala zwraca szczegółową informację zwrotną od techników: czego brakuje, które podzespoły są niejasne lub niewystarczająco opisane. Wykorzystaj tę informację do poprawienia logów.
5. **Popraw i wyślij ponownie** - iteruj na podstawie feedbacku, aż technicy potwierdzą kompletność i otrzymasz flagę `{FLG:...}`.

### Wskazówki

- **Plik z logami jest duży** - jak możesz go sensownie przeszukiwać? Jaki model może pomóc? Drogie modele wygenerują wysokie koszty jeśli będziesz wielokrotnie pracował na dużych zbiorach danych.
- **Feedback od techników jest bardzo precyzyjny** - Centrala podaje dokładnie, których podzespołów nie dało się przeanalizować. To cenna wskazówka, czego w logach brakuje - warto ją wykorzystać do uzupełnienia wynikowego pliku.
- **Czy warto na początku wysłać wszystko co istotne?** - Ile tokenów zajmują same zdarzenia WARN/ERRO/CRIT? Czy na pewno zmieszczą się w limicie bez dalszej kompresji? A może lepiej zacząć od mniejszego zestawu i uzupełniać w oparciu o feedback? Przemyśl, które podejście da szybszy wynik.
- **Zliczaj tokeny przed wysłaniem** - wysyłanie logów przekraczających limit skończy się odrzuceniem. Wbuduj zliczanie tokenów jako osobny krok przed weryfikacją. Przyjmij konserwatywny przelicznik.
- **Podejście agentowe** - to zadanie dobrze nadaje się do automatyzacji przez agenta z Function Calling, który może: przeszukiwać plik, budować wynikowy log, zliczać tokeny i iteracyjnie wysyłać do weryfikacji na podstawie feedbacku. Warto mieć narzędzie do przeszukiwania logów, zamiast trzymać je w całości w pamięci głównego agenta. Przeszukiwaniem może zająć się subagent.
