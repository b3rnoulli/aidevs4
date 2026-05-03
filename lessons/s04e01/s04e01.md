---
title: S04E01 — Wdrożenia rozwiązań AI
space_id: 2476415
status: scheduled
published_at: '2026-03-30T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/0401-1774694233.png'
circle_post_id: c''
---
## Film do lekcji

![https://vimeo.com/1177421190](https://vimeo.com/1177421190)

AI w swojej obecnej formie wciąż jest nowe i trudno jednoznacznie mówić o **najlepszych praktykach** wdrożeń. Tym bardziej, że o konsekwencjach długoterminowych będziemy się dopiero przekonywać. Historie firm takich jak [Klarna](https://fortune.com/2025/05/09/klarna-ai-humans-return-on-investment/), czy ostatnia [Block](https://x.com/jack/status/2027129697092731343) sugerują, że wpływ na rynek pracy jest realny, ale też nieoczywisty. Rozwijające się modele, narzędzia i techniki pracy sprawiają, że to, co było niemożliwe jeszcze kilka miesięcy temu, dziś może być w zasięgu. Jednak w praktyce, dodatkowo utrudnia to określenie co w danej chwili ma znaczenie dla nas.

Powiedzieliśmy już, że wdrożenia rozwiązań AI w dużym stopniu przypominają wdrożenia systemów niewykorzystujących AI. Do pewnego stopnia możemy więc **łączyć to**, co już wiemy, z tym, czego aktualnie się uczymy.

Aby odnaleźć się w nowym obszarze, warto jest **dopasować swoje otoczenie** tak, aby jak najlepiej sprzyjało nam w eksploracji, doświadczaniu oraz wyrabianiu intuicji o tym, co ma szansę zadziałać, a co nie. Dobrym pomysłem jest więc zbudowanie rozwiązań z których **sami będziemy korzystać**, ponieważ w ten sposób doświadczymy problemów i zrozumiemy możliwości, które przygotują nas do tworzenia rozwiązań na większą skalę.

W tej lekcji przyjrzymy się projektowi "**Cyfrowego Ogrodu**", czyli koncepcji osobistej bazy wiedzy, która zwykle ma charakter publiczny. Niekiedy występuje także jako **Digital/Second Brain**. W przeciwieństwie do zwykłego bloga, treści nie ograniczają się wyłącznie do artykułów i mogą przybierać dowolną formę. Taki projekt może potencjalnie stać się częścią codzienności każdego z nas, a elementy tej koncepcji funkcjonują także w kontekście firmowych baz wiedzy. Istotną zmienną będzie tu jednak połączenie z AI, bądź wprost sprawienie, aby nasze notatki stały się jednocześnie **pamięcią** agenta, co po części nawiązuje do lekcji **S02E03**.

## Oczekiwania vs rzeczywistość wdrożeń AI

Słysząc określenie **Second Brain**, zwłaszcza w połączeniu ze **Sztuczną Inteligencją**, natychmiast nasuwają się skojarzenia rodem z komiksów Marvela bądź filmów sci-fi. Jeśli dodamy do tego logikę agentów posługujących się narzędziami w naszym imieniu, to nagle wszystko wydaje się możliwe. Oczywiście wiemy, że tak nie jest. Ale wiemy także, że wiedza, którą posiadamy, pozwoli nam stworzyć system i narzędzia, które nie muszą od razu być odpowiednikiem [J.A.R.V.I.S.](https://en.wikipedia.org/wiki/J.A.R.V.I.S.), ale wciąż mogą być bardzo użyteczne.

Załóżmy więc, że naszym zadaniem jest wdrożenie systemu Second Brain / Digital Garden. Definicje tych nazw są bardzo płynne i mogą być różnie interpretowane, więc załóżmy, że chodzi nam o:

- system wiedzy w formie dokumentów tekstowych (Markdown)
- statyczną stronę www generowaną na podstawie treści tych plików
- agenta, dla którego ten system wiedzy będzie pełnił rolę pamięci oraz przestrzeni roboczej
- agent będzie mógł swobodnie manipulować dokumentami, a nawet wysyłać dotyczące ich zmiany do repozytorium
- agent przynajmniej częściowo musi poruszać się w sandboxie, szczególnie w związku z obsługą terminala
- zakładamy też, że wszystkie przechowywane dane mają charakter **publiczny**

Do zbudowania tego projektu wykorzystamy **API OpenAI**, **Sandbox Daytona** oraz **Github Actions i Github Pages**. Dodatkowo fakt, że mamy do dyspozycji sandbox sprawi, że agent będzie mieć możliwość wykonywania kodu JavaScript/Node.

![Architektura cyfrowego ogrodu AI](https://cloud.overment.com/2026-03-02/ai_devs_4_garden-8919e468-9.png)

Patrząc na powyższe możliwości można zadać sobie pytanie **dlaczego budować agenta, przecież wystarczy tu "Claude Code"?** i jest to prawda. Claude Code posiada wszystkie te możliwości, może poza wygenerowaniem strony www na podstawie markdown. Tutaj chodzi jednak o to, abyśmy zrozumieli **co się dzieje "pod spodem"**, ponieważ zastosowanie Claude Code w skali produkcyjnej raczej mijałoby się z celem. Ewentualnie moglibyśmy rozważyć wykorzystanie logiki [Pi](https://pi.dev/) oraz jej obudowanie według naszych potrzeb. Nadal dawałoby nam to spore zrozumienie logiki, a jednocześnie otwierało drogę na produkcję. Tutaj decyzja zależy już od nas.

Minimalna implementacja agenta przedstawionego na ostatnim schemacie znajduje się w folderze **04\_01\_garden**. Po jego uruchomieniu **npm start** możemy poprosić o zarządzanie notatkami, a poleceniem **npm run preview** baza wiedzy w plikach markdown zostanie zamieniona na stronę www. Przykład może też być wgrany do zdalnego repozytorium Github, a po aktywacji Github Pages, strona zostanie automatycznie opublikowana na domyślnej domenie naszego konta.

![Wizualizacja strony www](https://cloud.overment.com/2026-03-03/ai_devs_4_layout-00852aa4-6.png)

Jesteśmy więc w miejscu w którym **rozmowa z agentem** może wiązać się z **modyfikacją plików** których treść stanie się naszą stroną. Co więcej, gdy przypomnimy sobie przykłady z lekcji **S02E03**, to jasne staje się także to, że agent będzie mógł działać według **procesów** opisanych w plikach. A w tym przypadku do dyspozycji mamy także Skille przypominające koncepcją [umiejętności Claude Code](https://code.claude.com/docs/en/skills).

Bez wątpienia mówimy tu o ogromnej elastyczności i wynikających z niej możliwości. Tylko co to dokładnie oznacza?

- Agent może poruszać się po **całej bazie** wiedzy z pomocą poleceń w terminalu.
- Agent może **tworzyć i edytować** dowolny dokument markdown
- Agent może **podążać za instrukcjami** opisanymi w plikach
- Agent może **uruchamiać generowane skrypty**
- Agent może **posługiwać się narzędziami** wykorzystując [Code Mode](https://www.anthropic.com/engineering/code-execution-with-mcp)
- Agent może **samodzielnie publikować** zmiany

Możemy więc:

- podłączyć [Firecrawl](https://www.firecrawl.dev/), aby monitorować zasoby w Internecie (np. nowości branżowe)
- podłączyć [Gemini](https://ai.google.dev/gemini-api/docs/interactions), aby analizować filmy, np. z wybranych kanałów YouTube
- podłączyć [Replicate](https://replicate.com/), aby generować dopasowane do stylu grafiki
- podłączyć [Resend](https://resend.com/), aby zarządzać kampaniami mailowymi
- ...i wiele, wiele innych

W teorii mówimy tutaj o potencjale automatyzacji dowolnego procesu biznesowego. Chwilę później orientujemy się, że:

- agent nie może przetwarzać zbyt długich dokumentów
- agent nie widzi obrazów obecnych w tekście
- agent nie przetwarza dokumentów binarnych (np. PDF)
- agent nie może dostać się na niektóre strony www
- agent nie może skorzystać z funkcji serwisów niedostępnych w API
- agent zbyt długo generuje odpowiedzi
- agent generuje zbyt duże koszty

I to właśnie można potraktować jako zderzenie **oczekiwań z rzeczywistością**. No ale wiemy już, że każdy z wymienionych problemów da się rozwiązać. Oznacza to, że **nie możemy zrobić wszystkiego, ale możemy zrobić cokolwiek**. Podobnie wygląda to przy tworzeniu rozwiązań produkcyjnych, gdzie również musimy wybrać obszary na których skupi się nasza uwaga.

Przykład **04\_01\_garden** jest więc w tym przypadku **punktem startowym** i na tym etapie jego użyteczność jest raczej ograniczona ze względu na brak interfejsu, mechanik kompresji kontekstu czy minimalną liczbę narzędzi. Jednocześnie projektując wdrożenia AI dobrze jest określić sobie podobny punkt, który będzie pełnił rolę **fundamentu** na którym będziemy budować dalej. Tymczasem warto uruchomić go i poprosić agenta o dopisanie **3-4 naszych ulubionych książek** podając ich nazwy i sprawdzić jak ich treść przekłada się na wygląd strony (npm run preview). Wówczas możemy zadać sobie pytanie: **czy taki agent może być dla nas użyteczny, a jeśli tak, to jak?**

## Synchroniczną i asynchroniczna współpraca z AI

Na temat różnic pomiędzy bezpośrednią współpracą z agentami, a ich funkcjonowaniem w tle, mówiliśmy już całkiem sporo. Natomiast w kontekście wdrożeń AI są to niemal dwie różne kategorie problemów. Wystarczy spojrzeć ponownie na przykład **04\_01\_garden** z tych dwóch perspektyw.

**Praca synchroniczna:**

- **Interfejs:** rola edytora, czatu oraz różnych sposobów komunikacji z agentem stanowią tu centralny element systemu i bezpośrednio wpływają na jego skuteczność
- **Personalizacja:** dopasowanie systemu do potrzeb użytkownika może obejmować budowanie kontekstu, modyfikowanie struktur, tworzenie własnych workflow czy umiejętności. Istotne będą także własne rozszerzenia i ich konfiguracja
- **Synchronizacja:** współpraca między użytkownikiem oraz agentami wymaga tego, aby każdy miał swobodny dostęp do aktualnych danych
- **Feedback:** system może posiadać znacznie większe uprawnienia, ponieważ krytyczne akcje i tak będą pod nadzorem człowieka

**Praca asynchroniczna:**

- **Integracja:** system musi działać według zdefiniowanych procesów bądź przestrzeni po której mogą poruszać się agenci. Wymagania, połączenie z usługami oraz ustalenie harmonogramu muszą być ustalone z góry i wpisać się w codzienność oraz styl pracy użytkownika.
- **Komunikacja:** interfejs użytkownika może zostać całkowicie pominięty, bądź przynajmniej mocno ograniczony. Działanie systemu może sprowadzać się wyłącznie do funkcjonowania w tle, bądź wyłącznie raportowania wyników z minimalnym zaangażowaniem ze strony człowieka.
- **Samodzielność:** procesy muszą być precyzyjnie zdefiniowane i na tyle skuteczne, aby nie wymagały interwencji po stronie człowieka. Jednocześnie system powinien uwzględniać ewentualne **modyfikacje** oraz **dopasowanie** do zmieniającego się otoczenia (np. integracji z nowymi systemami)
- **Autonomia:** choć samodzielna praca agentów występuje także w przypadku bezpośredniej współpracy z człowiekiem

![Porównanie synchronicznej i asynchronicznej współpracy z agentami](https://cloud.overment.com/2026-03-03/ai_devs_4_async:async-351d8e7d-9.png)

Powyższa wizualizacja wyraźnie obrazuje różnicę pomiędzy obszarami na których będziemy skupiać się w zależności od charakteru systemu. Widać na niej także rozkład zaangażowania pomiędzy użytkownikiem, a AI. Jednocześnie są to jedynie ogólne kategorie, a nie konkretne funkcjonalności czy procesy za które agent będzie odpowiedzialny.

W tym miejscu musimy więc zdecydować, w którą stronę chcemy pójść, lub ewentualnie podjąć decyzję o tym, jaki rodzaj **hybrydowego** rozwiązania chcemy zbudować. Ponieważ nic nie stoi na przeszkodzie, aby system działał w tle, a współpraca z użytkownikiem nadal była możliwa. W naszym przypadku będzie to konkretnie:

- **Edytor:** możliwość samodzielnego zarządzania notatkami w edytorze markdown. Użytkownik będzie więc musiał posiadać dostęp do najnowszej wersji dokumentów.
- **Interfejs:** użytkownik będzie miał możliwość przekazywania prostych poleceń (poza interfejsem czatu), związanych np. z zapisywaniem informacji bądź docieraniem do istniejących treści.
- **Workflow:** procesy realizowane przez agentów będą opisane w plikach, a rezultaty ich pracy zapisywane w ustalonych strukturach. To przestrzeń na research, cykliczne notatki, obserwacje, gromadzenie informacji czy historii.
- **Agenci:** agenci powinni mieć dostęp do dedykowanych narzędzi, ale nie będzie dochodziło między nimi do bezpośredniej współpracy, lecz jedynie wymiany informacji. Np. agent zarządzający pocztą będzie mógł skorzystać z efektów pracy agenta do przeszukiwania sieci, ale nie będzie miał możliwości zlecenia mu nowych zadań.

Mówimy więc tutaj o minimalnej konfiguracji, która pozwoli nam na wygodne zarządzanie rozwojem naszego "cyfrowego ogrodu", korzystając przy tym ze wsparcia AI, ale w raczej ograniczonym zakresie. Aby to wszystko miało sens, istotną rolę będzie odgrywać określenie **zasad** oraz **struktury** informacji w ramach których będziemy się poruszać. Jednocześnie obecność agenta nie powinna nam **przeszkadzać**.

Główne koncepcje naszego projektu widoczne są poniżej:

![Architektura cyfrowego ogrodu](https://cloud.overment.com/2026-03-03/ai_devs_4_garden_structure-94fe8562-e.png)

Nie jest to zatem typowy system wieloagentowy, choć faktycznie występuje w nim wielu agentów. Nie mówimy tu też o interfejsie czatu, ale mamy możliwość wymiany wiadomości z głównym agentem. Patrząc na to z szerszej perspektywy można powiedzieć, ze mamy do czynienia z **częściowo-autonomicznym blogiem**, ponieważ:

- użytkownik tworzy treści samodzielnie, ale jest **wspierany** przez AI
- agenci realizują procesy, ale mogą **współdzielić** zasoby w postaci wiedzy
- procesy nie opierają się wyłącznie o pliki tekstowe, ale **integracje** z otoczeniem
- działanie systemu ma charakter **autonomiczny**, ale tylko w wybranych obszarach
- zadania agentów są z góry zdefiniowane, ale mogą być przez nich **optymalizowane**
- system opiera się o istniejące moduły, ale z łatwością może być **rozbudowany** ze względu na swoją elastyczność

Patrząc na takie scenariusze, bliżej nam tutaj do współpracy **asynchronicznej**, w której kontakt z agentami będzie bardzo ograniczony.

W ten sposób przeszliśmy od **ogólnych fundamentów**, których możliwości są "nieograniczone" do wyraźnie **wyspecjalizowanego systemu**, którego rolą jest **wspieranie** użytkownika w jego rozwoju, zdobywaniu nowych umiejętności, gromadzeniu zasobów oraz dzieleniu się swoimi doświadczeniami. Takie ukierunkowanie wynika bezpośrednio z połączenia **potrzeb użytkownika** oraz **możliwości**, jakie daje nam generatywna sztuczna inteligencja. Jak widać nie mówimy tu o **zastąpieniu** człowieka czy **generowaniu treści na bloga**, lecz wyraźnej współpracy oraz wzmacnianiu możliwości po obu stronach.

Bardzo podobnie wygląda to w przypadku projektowania rozwiązań dla klientów czy na potrzeby wewnątrzfirmowe. Tam również możemy zacząć od ogólnych założeń, a potem stopniowo kształtować rozwiązanie tak, aby odpowiadało na potrzeby biznesowe bez wchodzenia w skrajności takie jak np. "pełna automatyzacja" procesów. Oczywiście nie wykluczamy tutaj, że scenariusze w których sztuczna inteligencja przejmuje wszystkie aktywności nie są możliwe, ale należy podchodzić do tego z rozwagą. Tym bardziej, że do tej pory mówiliśmy głównie o możliwościach, pomijając większość barier i istotnych ograniczeń.

## Mapowanie procesów w kontekście możliwości rozwiązań AI

Połączenie istniejących procesów oraz potrzeb biznesowych z możliwościami AI, wymaga zrozumienia każdego z tych elementów. Bo poza decyzją o tym, **"co chcemy zrobić?"** musimy podjąć także decyzję o tym **"czego nie chcemy robić?"** oraz **"jak chcemy to zrobić?"**. Samo zastosowanie AI nie odpowie nam automatycznie na takie pytania, tym bardziej że w grę wchodzi także decyzja, aby **nie stosować AI**, na przykład tam, gdzie korzyści będą mniejsze albo nawet w ogóle ich nie odczujemy.

Patrząc ponownie na nasz przykład, przy podejmowaniu decyzji kształtujących projekt, bierzemy pod uwagę przede wszystkim:

- **Użytkownik**: jest to osoba potrafiąca programować, więc możemy pozwolić sobie na nieco większy poziom złożoności narzędzi, co jednocześnie umożliwi zmniejszenie limitów narzucanych na agenta (np. możliwość uruchamiania kodu czy obsługę terminala). Musimy jednak zadbać o odpowiedni poziom bezpieczeństwa, więc wykorzystamy także **sandbox**.
- **Treść:** tworzy ją użytkownik niemal wyłącznie na własne potrzeby. W klasycznych cyfrowych ogrodach jest tworzona ręcznie, przy częściowym wsparciu automatyzacji. Jej pełne generowanie przez AI nie niesie wartości dla użytkownika, ale jej wzbogacanie już tak. Agent będzie miał więc pełne uprawnienia dostępu, ale będzie działał według ustalonych zasad.
- **Format:** cyfrowy ogród ma formę strony www, a kod HTML może edytować zarówno użytkownik-programista oraz model językowy. Ale w praktyce ręczne edytowanie HTML nie jest wygodne, szczególnie przy pisaniu notatek czy dłuższych form tekstowych. Dlatego formatem treści będzie markdown, a proces konwertowania do HTML zostanie zrealizowany wyłącznie poprzez kod.
- **Integracje:** powiedzieliśmy, że agent może wykonywać kod, więc będziemy mogli zastosować koncepcję "skills" oraz obsługę narzędzi przez "code mode". Taka konfiguracja pozwala nam zarówno na stosowanie **CLI** jak i **MCP** oraz natywnych narzędzi. Nie jesteśmy więc pod tym kątem w żaden sposób ograniczeni.
- **Publikacja:** generowana strona to statyczny HTML, więc w zupełności wystarczy nam tu wszystko to, co oferuje Github Pages. Dzięki Github Actions, treść strony zostanie zaktualizowana za każdym razem, gdy w repozytorium pojawią się jakieś zmiany. Publiczny charakter koncepcji "Cyfrowego Ogrodu" sprawia też, że problem prywatności treści nie istnieje tutaj "by design".
- **Dostępność:** agent powinien być dostępny przez API, aby możliwość zapisywania informacji bądź ich przypominania była dostępna z dowolnego miejsca. Oznacza to, że zarówno sama aplikacja jak i dokumenty markdown **muszą znajdować się na zdalnym serwerze** i być synchronizowane z komputerem użytkownika na przykład poprzez [Mutagen](https://mutagen.io/documentation/synchronization/)

Z takiego procesu myślowego powstaje nam pewnego rodzaju mapa określająca obszary na których możemy się skupić. Co prawda w naszej sytuacji byliśmy w stanie samodzielnie odpowiedzieć na wszystkie pytania, ponieważ jest to projekt, który tworzymy dla siebie. W praktyce nie zawsze będzie to takie oczywiste i to nie tylko ze względu na dostępność informacji, ale także określenie tego, **czy są one słuszne.** Dobrze jest więc przygotować się na **szybkie iteracje** oraz utrzymać możliwie wysoką elastyczność projektu.

![Mapa decyzyjna dotycząca architektury wdrożenia](https://cloud.overment.com/2026-03-04/ai_devs_4_decision_map-8088af1a-f.png)

Wdrożenie takiego planu na tym etapie jest już relatywnie "proste", ponieważ omówiliśmy już wszystkie mechaniki dotyczące AI, czyli: logikę agenta, obsługę narzędzi, pracę z plikami, sandbox, workflows czy kwestie bezpieczeństwa oraz optymalizacji. Reszta dotyczy już wyłącznie mechanik, które być może znamy już z kodu.

Przy wdrożeniu rozwiązań AI godny uwagi jest również balans pomiędzy logiką kodu, a zaangażowaniem modelu. Widoczna poniżej wersja wcześniejszego schematu z nałożonymi kolorami oraz etykietami jasno sugeruje, że elementy **aplikacji, które znamy z codziennej pracy** nadal stanowią zdecydowaną większość całej architektury.

![Balans pomiędzy rozwiązaniami programistycznymi i AI](https://cloud.overment.com/2026-03-04/ai_devs_4_decision_map_roles-4544c002-a.png)

Co ciekawe, jeszcze kilkanaście miesięcy temu mówiliśmy tu raczej o podziale 90-10 bądź 80-20. Wówczas scenariusze, w których AI rzeczywiście się sprawdzało, były bardzo ograniczone. Teraz logika agentów zwiększa rolę modeli i w niektórych sytuacjach możemy obserwować nawet **odwrócone proporcje**.

## Weryfikowanie początkowych założeń przez "proste" testy

Powiedziałem, że część decyzji, które podejmiemy na etapie określania założeń projektu będzie błędna. Choć tego samego możemy doświadczyć przy budowaniu projektów niewykorzystujących AI, tak tutaj do gry wchodzą także trudne do przewidzenia **zachowania modeli**, bądź komplikacje związane z API (np. koszty). Możliwe są też odwrotne scenariusze, na przykład gdy najnowsze modele umożliwiają zrobienie czegoś, co do tej pory wydawało się "niemożliwe".

Patrząc na nasz przykład, możemy przeprowadzić kilka prostych testów:

- **Wzbogacanie:** jednym z założeń jest uzupełnianie notatek użytkownika o dodatkową wiedzę. Może się jednak okazać, że model samodzielnie nie jest w stanie dobrze określić, co powinno być dodane i czy w ogóle powinno być dodawane. Wówczas może okazać się, że uzasadnione będzie dodanie właściwości **frontmatter** do pliku markdown, w której użytkownik będzie mógł zostawić notatkę, która ukierunkuje działanie agenta.
- **Budowanie:** tworzenie nowych wpisów (np. dodawanie zasobów wiedzy) może odbywać się w wyniku prostej akcji użytkownika, takiej jak przesłanie adresu URL. Agent może odczytać jego zawartość i samodzielnie zdecydować o tym, gdzie dany wpis ma się pojawić oraz w jaki sposób ma zostać opisany. Dobrym pomysłem jest zbudowanie zestawów danych i przygotowanie ewaluacji, aby sprawdzić jaki model i jego konfiguracja najlepiej poradzą sobie z tym zadaniem.
- **Dostępność:** jednym z najważniejszych elementów obecności AI w projekcie cyfrowego ogrodu jest możliwość łatwego dostępu do jego treści. Tutaj od razu na myśl przychodzi **chatbot** z którym możemy porozmawiać na temat posiadanych dokumentów. Pytanie jednak **czy jest to konieczne**. Może wystarczy nam dobrze skonfigurowana wyszukiwarka bądź aplikacja mobilna, dzięki którym natychmiast dostaniemy się do oryginalnych dokumentów.

Każdy z takich testów możemy zrealizować w bardzo krótkim czasie i uzyskać odpowiedź na pytania, na podstawie których zdecydujemy o sposobie wdrożenia projektu. Tym bardziej, że dziś przez "proste testy" nie mamy na myśli już prostych prototypów, ale nawet **wygenerowanie natywnej aplikacji mobilnej** z relatywnie zaawansowanymi funkcjonalnościami.

Przekładając to na realia biznesowe, może się okazać, że klient otrzyma do testów wybrane funkcjonalności już w zaledwie kilka dni, a w skrajnych przypadkach nawet po kilku godzinach, szczególnie w kontekście startupów bądź projektach agencyjnych. Ale nawet jeśli nie będziemy patrzeć na to wyłącznie przez pryzmat **szybkości** budowy prototypów, to nadal mówimy tu o możliwości **testowania wielu pomysłów równolegle** oraz **weryfikowaniu tez w rozbudowanych środowiskach testowych**, które wiernie oddają rzeczywistość bądź w niektórych przypadkach nawet o testach obejmujących realny kontekst użytkowników końcowych oraz ich feedback.

Poniżej mamy wizualizację, której celem jest jedynie **orientacyjne** oraz uproszczone zobrazowanie różnicy pomiędzy prototypowaniem bez AI oraz wspólnie z nim. W rzeczywistości konieczne byłoby uwzględnienie także kwestii komunikacji i wymiany informacji z klientem, oczekiwania na feedback itd., więc nie zawsze różnice będą tak wyraźne. Natomiast pomimo wszystko mamy tutaj jasny sygnał, że **dostępność AI** zmienia całkowicie sposób w jaki w ogóle patrzymy na etap prototypowania i weryfikacji założeń.

![Prototypowanie bez AI oraz z AI](https://cloud.overment.com/2026-03-04/ai_devs_4_prototyping-5052af56-a.png)

Warto też mieć na uwadze fakt, że prezentowana powyżej sytuacja odnosi się nie tylko do procesu wdrożeń AI dla klientów, ale także **budowania funkcjonalności**, **procesu nauki** czy tworzenia rozwiązań w celu **optymalizacji swojej codzienności**. Być może jest to oczywiste, ale mówimy tutaj o konieczności zmiany nawyków i tutaj może okazać się, że **istnieje różnica pomiędzy tym, co wiemy, a tym co robimy**.

## Źródła inspiracji oraz wiedzy

Wdrożenia AI, zwłaszcza w obszarze biznesowym, charakteryzują się tym, że trudno dotrzeć do informacji na ich temat poza artykułami marketingowymi publikowanymi przez firmy wdrożeniowe. Takie treści rzadko zawierają detale istotne z naszego punktu widzenia i mogą stanowić co najwyżej źródło inspiracji i ogólnych pomysłów.

Znacznie bardziej szczegółowe treści można znaleźć na blogach osób stojących za konkretnymi narzędziami. Niekiedy też mówimy tutaj o firmach, w których interesie również leży dostarczenie nam możliwie jakościowej wiedzy, która jednocześnie zachęci nas do skorzystania z ich produktów. Co więcej, nierzadko posiadają oni doświadczenie związane ze współpracą z klientami biznesowymi. Wśród nich są:

- Blog [LlamaIndex](https://www.llamaindex.ai/blog)
- Blog [Vercel](https://vercel.com/blog)
- Blog [Langfuse](https://langfuse.com/blog)
- Blog [Cloudflare](https://blog.cloudflare.com/code-mode/)
- Blog [HumanLayer](https://www.humanlayer.dev/blog)
- Blog [Philipp Schmid](https://www.philschmid.de/agent-harness-2026)
- Blog [ngrok](https://ngrok.com/blog) (ostatnio piszą sporo na temat AI)
- Blog [Manus](https://manus.im/blog)
- Projekty [Nous Research](https://github.com/NousResearch/hermes-agent)
- Projekt [Pi](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent)
- Prezentacje [Braintrust](https://www.youtube.com/@BraintrustData)
- Prezentacje [Databricks](https://www.youtube.com/@Databricks)
- Prezentacje [AI Engineer](https://www.youtube.com/@aiDotEngineer)

Warto także odnaleźć profile osób zaangażowanych w powyższe projekty i obserwować ich publikacje oraz treści, które podają dalej. Podobnie można zrobić z narzędziami z których korzystamy na co dzień, dla których istotną częścią modelu biznesowego jest współpraca z firmami.

## Fabuła

![https://vimeo.com/1177416984](https://vimeo.com/1177416984)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze piąty!

Przychodzę z dobrą wiadomością. Nasz wysłannik, dzięki Twojej pomocy, dotarł do miasta Skolwin i udało mu się wynegocjować dobre ceny dla wszystkich podzespołów niezbędnych do zbudowania małej turbiny wiatrowej. Chwilę będziemy czekać na dostawę tych części, ale przynajmniej wiemy, że niebawem trafią one w nasze ręce.

Pojawił się jednak pewien problem, ponieważ nasze ruchy, jak się okazuje, nie były zupełnie niezauważone.

Nie wspominałem Ci o tym, ale w świecie, w którym się znajdujemy, nie tylko komunikacja internetowa, radiowa, czy telefoniczna są podsłuchiwane. Kontroli podlega KAŻDA aktywność na terenie kraju. Trudno jest poruszać się, nie będąc zauważonym. Trudno jest handlować czymkolwiek, żeby system o tym nie wiedział, a tym bardziej trudno jest przelecieć niezauważonym na rakiecie przez środek pustkowia. Nie wiem co mieliśmy w głowie, gdy akceptowaliśmy ten plan...

Ale nie martw się. Odkręcimy to wszystko.

Jakiś czas temu przy pomocy ataku phishingowego zdobyliśmy dostęp do jednego z kont w centrum operacyjnym OKO. Pewnie zastanawiasz się, czym jest to tajemnicze "OKO". To element Systemu, który służy do monitorowania wszystkich nietypowych incydentów, które zdarzyły się na terenie kraju.

Musisz się tam zalogować i zmienić dane, jakie są widoczne dla operatora. W ten sposób zatrzemy ślady po naszej rakietowej eskapadzie.

Tylko pod żadnym pozorem — to bardzo ważne, powtarzam: pod żadnym pozorem! — nie wolno Ci niczego zmieniać w interfejsie webowym. Interfejs ten ma służyć Ci tylko do rozglądnięcia się po systemie i zdobycia odpowiednich informacji. Jeśli czegoś dotkniesz, operatorzy natychmiast będą wiedzieć, że tam byłeś, a wtedy odetną nam dostęp.

Wystawiliśmy Ci więc API do modyfikacji danych prezentowanych w ich systemie.

W notatce do tego nagrania znajdziesz informację, co konkretnie należy zmienić. Wykonaj to proszę dla nas. To bardzo ważne. Bez tych modyfikacji, Skolwin skończy tak, jak to poprzednie miasto.

## Zadanie praktyczne

Twoim zadaniem jest wprowadzenie zmian w Centrum Operacyjnym OKO za pomocą API wystawionego przez centralę.

Zdobyliśmy login i hasło do wejścia do tego systemu, ale nie wolno Ci wprowadzać tam żadnych ręcznych zmian. Cała edycja musi odbywać się przez nasze tylne wejście.

Zadanie nazywa się: **okoeditor**

Nasze API jest dostępne standardowo pod adresem `/verify`

Panel webowy operatora: https://oko.ag3nts.org/

- Login: Zofia
- Hasło: Zofia2026!
- Klucz: Twój apikey

Na początek zacznij od zapoznania się z API dostępnym pod /verify w Centrali.

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "okoeditor",
  "answer": {
    "action": "help"
  }
}
```

Gdy wprowadzisz wszystkie wymagane zmiany na stronie, wykonaj akcję **done**. Oto Twoja lista zadań:

- Zmień klasyfikację raportu o mieście Skolwin tak, aby nie był to raport o widzianych pojazdach i ludziach, a o zwierzętach.
- Na liście zadań znajdź zadanie związane z miastem Skolwin i oznacz je jako wykonane. W jego treści wpisz, że widziano tam jakieś zwierzęta np. bobry.
- Musimy przekierować uwagę operatorów na inne, niezamieszkałe miasto, aby ocalić Skolwin. Spraw więc, aby na liście incydentów pojawił się raport o wykryciu ruchu ludzi w okolicach miasta Komarowo.
- Gdy to wszystko wykonasz, uruchom akcję "done".
