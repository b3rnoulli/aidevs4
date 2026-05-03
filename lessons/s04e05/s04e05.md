---
title: S04E05 — Projektowanie rozwiązań wewnątrzfirmowych
space_id: 2476415
status: scheduled
published_at: '2026-04-03T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/0405-1774694248.png'
circle_post_id: 31103407
---
Zastosowanie możliwości obecnego AI w firmach może obejmować **wdrożenie zewnętrznych narzędzi czy platform** bądź **zbudowanie własnych** rozwiązań. W obu przypadkach może pojawić się potrzeba zaangażowania osób technicznych, ale w tym drugim nasza rola jest zdecydowanie większa i to właśnie nim się teraz zajmiemy.

Wielokrotnie mówiliśmy, ale też doświadczyliśmy w praktyce, że AI bez wątpienia potrafi już dziś robić imponujące rzeczy. Jednak na tym etapie często nie spełnia ona ogromnych oczekiwań, jakie mamy wobec tej technologii. A nawet jeśli mówimy o zastosowaniach, w których obecne modele odnajdują się świetnie, to nadal stoi przed nami niezwykle trudny problem do rozwiązania: **jest nim "zmiana"** za którą kryją się różne przyczyny, którym się dziś przyjrzymy.

## Stosowanie generatywnego AI wewnątrz firmy

Na tym etapie AI\_devs raczej oczywiste jest to, że obecnie jakość jaką daje nam sztuczna inteligencja jest w dużym stopniu uzależniona od wiedzy, jaką posiadamy na temat działania modeli czy otaczających je mechanik. Jednak ludzie z którymi będziemy pracować oraz użytkownicy rozwiązań, które będziemy tworzyć, nie zawsze będą mieć takie samo zrozumienie tej technologii jak my. Ich perspektywa będzie się więc różnić od naszej i musimy mieć to na uwadze.

Co ciekawe, różnice w sposobie pracy z AI, w tym także stylu zadawania pytań, będą różnić się nawet wśród osób technicznych, posiadających dość dużą wiedzę na temat modeli. Trudno stwierdzić, co jest dokładną przyczyną, ale da się to zauważyć w sposobie pracy z narzędziami, które będziemy tworzyć. Na przykład dla nas, agent pomagający w organizacji dnia, będzie znacznie bardziej użyteczny niż dla innych i będzie to wynikało między innymi ze **świadomości mechanik**, które nim kierują. Przykładowo nasze zapytania mogą naturalnie zawierać wskazówki dla agenta, na przykład "Sprawdź mi wiadomości **w gmailu i na slacku** a potem zerknij do **plików** z moimi **planem dnia**". Ktoś inny mógłby zapytać po prostu: "Sprawdź co mam na dziś?" i z dużym prawdopodobieństwem agent nie zrobiłby tego, o co został poproszony.

![Różnica pomiędzy sposobem pracy z agentami AI uzależniona od doświadczenia](https://cloud.overment.com/2026-03-11/ai_devs_4_query_awareness-9a1f8376-3.png)

Rozwój modeli językowych, narzędzi i technik pracy sprawia, że agenci są w stanie coraz lepiej odpowiadać na nawet ogólne polecenia użytkowników końcowych. Widzieliśmy już jednak przykłady sytuacji w których nie jest to oczywiste i wdrożenie rozwiązań na poziomie technicznym bywa w pewnym sensie niewykonalne lub bardziej **nieopłacalne** i wówczas musimy szukać innych ścieżek.

Jeśli połączymy fakt, że wdrażanie nowych rozwiązań wiąże się ze **zmianą istniejących procesów, nawyków** i niekiedy także **zdobyciem nowych umiejętności**, ale także **dodatkowymi kosztami** oraz połączymy to z niedeterministyczną naturą modeli o tym, co właśnie powiedzieliśmy na temat doświadczeń w pracy z AI, to otrzymamy pełen obraz tego, dlaczego wdrożenia AI stanowią tak duże wyzwanie. Mówiąc na bardzo ogólnym poziomie chodzi o:

- **Aspekt Biznesowy:** choć potrzeba wdrożenia AI może być uzasadniona, tak wdrażanie zmian w istniejących procesach wiąże się też z kosztami, które obejmują także późniejsze utrzymanie. Konieczne jest tutaj także zaadresowanie kwestii prawnych, które mogą sięgać w obszar technologii, na przykład wyboru dostawcy bądź rozwiązań chmurowych, np. Amazon Bedrock czy Microsoft Azure. Z naszej strony musimy więc zadbać o to, aby biznes był świadomy możliwości i ograniczeń technicznych, które pozwolą na podjęcie właściwych decyzji.
- **Aspekt Kulturowy:** wdrożenie nawet prostych narzędzi AI wymaga odpowiedniego zaangażowania na różnych poziomach organizacji. Tutaj świetnie sprawdzają się inicjatywy oddolne, w postaci wewnętrznych warsztatów czy nawet zwykłej wymiany doświadczeń na spotkaniach zespołu.
- **Aspekt Technologiczny / Produktowy:** tutaj, jako programiści, mamy do zrobienia najwięcej, ale jednocześnie musimy brać pod uwagę pozostałe obszary i na ich podstawie, a także na podstawie naszej wiedzy, określić zakres projektu, plan wdrożenia, wskaźniki sukcesu i porażki oraz samą realizację. Są to więc raczej dobrze znane nam aktywności, ale rozszerzone o decyzje dotyczące modeli, ich ewaluacji oraz architektury agentów i ich optymalizacji, a także o zaadresowanie faktu, że osiągnięcie 100% skuteczności ich działania jest obecnie mało prawdopodobne.

![Trudność wdrożenia AI w organizacjach](https://cloud.overment.com/2026-03-12/ai_devs_4_adoption-892e49ad-f.png)

W związku z tym, że obszary biznesowe oraz kulturowe dotyczące organizacji leżą poza zakresem AI\_devs, na potrzeby dalszej części lekcji założymy, że mamy w organizacji dostęp do modeli dowolnego dostawcy (np. OpenAI/Anthropic/Gemini) za pośrednictwem API.

## Przykłady narzędzi stosowanych w zespołach

We wcześniejszych lekcjach mówiliśmy o budowaniu agentów, współpracy bezpośredniej z nimi oraz agentach działających w tle. Jednak wdrożenie AI do procesów firmowych może obejmować nawet **opracowanie promptu** w postaci dokumentu bądź zaledwie kilku plików, które można podłączyć do agentów i interfejsów czatu (np. Claude). Na pozór może wyglądać to na mało poważne podejście do wdrożeń AI, ale tak nie jest, bo:

- **Checklista:** dokument może zawierać listę aktywności wraz z opisami, dla stałych ale powtarzalnych procesów, w przypadku których zawsze trzeba upewnić się, że wszystko zostało zrealizowane zgodnie z wymaganiami. Przykładem może być proces marketingowy związany z tworzeniem treści na firmowego bloga przy współpracy z zewnętrzną agencją. Każdy wpis może potrzebować weryfikacji pod kątem na przykład linkowania wewnętrznego, opisania zdjęć zgodnie z dobrymi praktykami SEO czy zawierać sekcje uzależnione od kategorii danego wpisu. Normalnie cały proces weryfikacji wykonywany jest ręcznie, bywa czasochłonny i łatwo w nim coś pominąć. Wsparcie ze strony AI może w tym bardzo pomóc, nawet pomimo tego, że zaangażowanie człowieka nadal będzie konieczne.
- **Onboarding:** czyli dokument zawierający kompletną listę niezbędnych informacji, które mogą być przydatne dla nowych pracowników, albo osób z innych działów. Może on obejmować linki do zasobów wiedzy oraz informacje o osobach odpowiedzialnych za stałe procesy. Dokument ten nie ma więc na celu **zastąpienia rozmowy**, lecz **przekierowania** we właściwe miejsce. Tutaj można zapytać o to, po co nam tutaj AI, skoro pliki tekstowe można przeszukiwać. Natomiast jeśli informacji jest dużo, nowy pracownik może mieć problem z wpisaniem dokładnej frazy, a AI będzie w stanie dopasować zapytanie nawet jeśli będzie dość odległe od zawartości dokumentu.
- **Styl:** to przykład bezpośrednio z realizacji AI\_devs. Wszystkie grafiki, które widzicie w treściach lekcji i zadań zostały wygenerowane na podstawie tego samego promptu opisującego spójny styl. Raz opracowany dokument dodaliśmy na Slacka, gdzie każdy mógł z niego skorzystać i z pomocą dowolnego narzędzia oferującego dostęp do Nano Banana 2 wygenerować odpowiednią grafikę. Tak prosta rzecz wpływa teraz na odbiór całego materiału dość dużego projektu jakim jest to szkolenie.

Zatem nawet najmniejsze aktywności związane z pracą z AI mogą wnieść dużo wartości wyrażonej przez oszczędność czasu, zwiększenie komfortu pracy czy utrzymania wyznaczonych standardów. Co ciekawe zwykle dość trudno jest zauważyć potrzebę wprowadzenia aż tak prostych elementów, bo zwykle zwyczajnie o tym nie myślimy. Jednocześnie opracowanie takich plików, jak chociażby wymieniony opis stylu, zwykle będzie wymagał doświadczenia w pracy z modelami.

Sama koncepcja dokumentów / promptów nabiera też nieco innego znaczenia, gdy spojrzymy na nią przez pryzmat popularnych w programowaniu plików AGENTS.md czy Skills. W ich przypadku również często mówimy o prostych zestawach instrukcji. A skoro takie podejście bywa użyteczne w programowaniu, to sprawdzi się również poza nim.

Opieranie działania AI wyłącznie o dokumenty, które agent może dowolnie zinterpretować, szczególnie w połączeniu z zapytaniem użytkownika na które też nie mamy zbyt dużego wpływu. W takiej sytuacji może być uzasadnione utworzenie wewnątrzfirmowego serwera MCP, albo niezależnego narzędzia, które będzie w pełni dopasowane do danego procesu. Warto to rozważyć, bo z pomocą AI możemy bardzo niskim kosztem utworzyć dość rozbudowane rozwiązanie, które nawet jeśli będzie wykorzystywane przez krótki czas, nadal będzie się opłacać. Przykład takiego narzędzia znajduje się w katalogu **04\_05\_review**.

Koncepcja tego agenta jest niezwykle prosta i polega na **przetwarzaniu akapitów** w dokumencie tekstowym. Agent otrzymuje treść każdego z nich i podejmuje decyzję o tym, czy skomentować ich fragmenty narzędziem **add\_comment**. Może więc dojść do sytuacji w której agent zostawia jeden lub więcej komentarzy, bądź wcale. Poniżej mamy animację głównej mechaniki tego agenta.

![Wizualizacja agenta](https://cloud.overment.com/agent-1773399141.gif)

Zatem to narzędzie opiera się o **dokument tekstowy**, który ma zostać "skomentowany", **prompt** opisujący na co agent ma zwrócić uwagę oraz **logika przetwarzania kolejnych fragmentów**. Istotną rolę odgrywa tutaj interfejs użytkownika, który wyświetla utworzone komentarze w formie **okienek** z opcją akceptacji, bądź odrzucenia danej sugestii.

Można powiedzieć, że wizualny interfejs (UI) odgrywa tu kluczową rolę, ponieważ można uznać, że "ten sam efekt można uzyskać wklejając dokument do ChatGPT". Jednak tam nie uzyskamy rezultatu, który pozwoli na wygodne zarządzać sugestiami agenta. Znacznie trudniej też będzie w ogóle je zauważyć. A tymczasem tutaj mówimy o kilku krokach:

1. Użytkownik wybiera dokument oraz prompt
2. Dokument zostaje podzielony na fragmenty
3. Każdy fragment zostaje sprawdzony przez agenta i ewentualnie skomentowany
4. Przed zakończeniem pracy agent generuje notatkę końcową
5. Użytkownik może zaakceptować / odrzucić sugestie lub poprosić o ponowne sprawdzenie z opcją przesłania krótkiego promptu.

Całą logika prezentuje się więc następująco:

![Przegląd narzędzia wspierającego tworzenie treści](https://cloud.overment.com/2026-03-13/ai_devs_4_review-64de189a-3.png)

W przypadku narzędzi takich jak to, szczególnie interesująca jest ich ogromna elastyczność, bo agent może otrzymać dodatkowe narzędzia. Wówczas ten sam interfejs może adresować zupełnie inny proces. Przykładowo:

- Proste prompty mogą opierać się o wiedzę i umiejętności modelu. Mowa tu o korektach, czy transformacjach (np. tłumaczeniach).
- Jeśli agent zostanie podłączony do Internetu bądź wybranych domen, to do gry wchodzi także grounding czy fact-checking.
- Jeśli agent otrzyma dodatkowe dokumenty, na przykład w postaci indeksu stron firmowego bloga, to agent może zająć się linkowaniem wewnętrznym, co jest przydatne dla czytelników ale też z punktu widzenia SEO
- Dodanie narzędzi łączących agenta z zewnętrznymi usługami może posłużyć przesyłaniu informacji. Np. agent może zasugerować, aby wybrany fragment, np. zgłoszenia, został przekierowany do odpowiedniego działu.

Oczywiście takie scenariusze mogą wymagać zmian w interfejsie czy logice, ale wszystkie opierają się o tę samą koncepcję. I właśnie takich rzeczy warto jest szukać w naszej codzienności oraz procesach firmowych.

Działanie przykładu **04\_05\_review** pokazałem osobom z którymi sam współpracuję, sugerując możliwe zastosowania w **marketingu** oraz integracji z jedną z naszych **platform**. Podczas rozmów z nimi wybraliśmy obszary w których to rozwiązanie nam się przyda. Od razu też pojawiły się potrzeby na inne narzędzia, ponieważ prezentacja tego, pokazała możliwości o których wcześniej nikt nie pomyślał. Warto jest więc **eksperymentować** nawet na bardzo małej skali.

## Prywatność danych i konsekwencje błędów

Jednym z pierwszych pytań dotyczących zastosowania AI jest kwestia zachowania bezpieczeństwa oraz prywatności danych. W tym miejscu dyskusja zwykle prowadzi nas do usługi chmurowe (np. wspomniany [Bedrock](https://aws.amazon.com/bedrock/)) bądź rozwiązań lokalnych o ile na takie możemy sobie pozwolić.

Instancje na Bedrock lub Azure dają nam zwykle pełną swobodę pracy z danymi (o tym ostatecznie decydują wewnętrzne polityki firmy bądź umowy z klientami(!!)) i może to sprawić wrażenie, że nasze dane są bezpieczne. **Ale tak nie jest**, ponieważ:

- Agent podłączony do Internetu może przesłać wewnętrzne dane na zewnątrz
- Agent posiadający możliwość wykonania kodu, może usunąć bądź uszkodzić źródła danych
- LLM może popełniać błędy. Bez weryfikacji ze strony człowieka, w danych mogą zacząć pojawiać się problemy, które trudno będzie zauważyć oraz naprawić.
- Agent może przypadkowo skorzystać z narzędzia, np. "send\_email" i wysłać go na niepoprawny adres. Podobnie też może zaprosić na spotkanie w Google Calendar osoby, których nie powinno tam być (np. spoza organizacji).
- Agent może wprowadzić człowieka w błąd, np. czatbot podłączony do firmowej bazy wiedzy może zasugerować wykonanie akcji, która nie powinna mieć miejsca (np. restart serwera produkcyjnego bez zachowania ustalonych procedur).

![Potencjalne problemy z danymi](https://cloud.overment.com/2026-03-13/ai_devs_4_issues-c9618cc5-0.png)

Zatem nawet jeśli dostawca LLM będzie zaufany, to nadal nie możemy ufać samemu modelowi. Na przestrzeni lekcji, pojawiało się mnóstwo przykładów prezentujących **ograniczanie uprawnień** agentów, albo wprost **fizyczne uniemożliwianie** podjęcia określonych działań.

Ostrożność należy zachować także w pracy z sandboxami, gdzie agent może znaleźć sprytne obejścia, o których nie pomyśleliśmy. Dobrym przykładem są agenci do kodowania, którzy zauważając brak dostępu do pliku .env piszą i uruchamiają skrypt, który to zrobi. Interesujące przykłady można znaleźć w dokumentach takich jak [System Card: Claude Opus 4.6](https://www-cdn.anthropic.com/6a5fa276ac68b9aeb0c8b6af5fa36326e0e166dd.pdf) czy [Eval Awareness](https://www.anthropic.com/engineering/eval-awareness-browsecomp) sygnalizujące, że obecne modele są w stanie zauważyć, że są testowane i dopasować swoje zachowanie tak, aby zaliczyć testy, nawet jeśli będzie wymagało to ukrycia ich faktycznych umiejętności. Mówiąc inaczej - obecne LLMy są **potencjalnie** zdolne do omijania zabezpieczeń.

Niestety mamy dość ograniczoną przestrzeń w zakresie kształtowania zachowań agentów, aby całkowicie wyeliminować wspomniane ryzyka. Warto jednak z góry nie zakładać, że coś jest **niemożliwe** i poświęcić czas na przeanalizowanie opcji, które nawet jeśli będą wymagały zaangażowania człowieka, co uniemożliwi pełną automatyzację procesu, nadal przełożą się na dużą wartość.

## Praca z kontekstem usług i narzędzi

Praktycznie każdy z nas pracuje z różnymi narzędziami. Część aktywności polega na **przenoszeniu danych** pomiędzy nimi i ewentualnej transformacji. Nierzadko też musimy zgromadzić informacje z wielu takich źródeł, a następnie zwizualizować bądź opisać, aby na tej podstawie móc podjąć jakieś decyzje. Bywa również tak, że musimy podjąć wiele małych akcji w różnych miejscach i więcej czasu tracimy na przełączanie się między usługami, niż faktyczną pracę.

Powyższe problemy dotyczą niemal każdej osoby w firmie:

- Obsługa klienta wymaga odnajdywania informacji o ustawieniach konta w panelu administracyjnym
- Zespół marketingu spędza czas na monitorowaniu skuteczności kampanii w różnych narzędziach i własnych dokumentach
- Zespół sprzedażowy spędza mnóstwo czasu na aktualizacji systemu CRM, a i tak wciąż zdarzają się braki wynikające z różnych powodów.
- Osoby zaangażowane w rozwój produktu muszą pozyskiwać informacje z wielu miejsc, również narzędzi z którymi nie pracują tak często jak osoby z konkretnych działów.

Takich scenariuszy jest mnóstwo, a patrząc na możliwości AI, od razu przychodzi do głowy agent ułatwiający pracę tych ludzi. Jednak gdy wejdziemy w szczegóły i nagle okaże się, że ryzyko halucynacji, prompt injection czy techniczne ograniczenia interakcji z danymi nie pozwalają na to, aby agent mógł robić to wszystko jedynie na podstawie poleceń użytkownika. Jest to idealna przestrzeń na powrót do MCP Apps bądź koncepcji generatywnego AI, które omawialiśmy w lekcji **S03E05**.

Po uruchomieniu przykładu **04\_05\_apps** otworzy się okno przeglądarki z prostym interfejsem czatu oraz przykładowymi akcjami związanymi z zarządzaniem **zadaniami, sprzedażą oraz newsletterem**. Nie jest to jednak zwykłe mapowanie dostępnych funkcjonalności, lecz lista dedykowanych interfejsów dopasowana do **procesów biznesowych** takich jak monitorowanie sprzedaży, zarządzanie produktami czy zadaniami powiązanymi z procesami poszczególnych projektów.

![Zarządzanie procesami w interfejsie czatu](https://cloud.overment.com/2026-03-15/ai_devs_4_chat_ui-dda8757b-6.png)

W związku z tym, że mamy tu do czynienia ze zdalnym serwerem MCP, możemy bez problemu podłączać te funkcjonalności do interfejsów wspierających MCP Apps, np. Claude. Co więcej, takie podejście pozwala również udostępniać serwery MCP naszym klientom, którzy mogą pracować we własnych interfejsach. Jeśli jednak posiadają one wsparcie dla MCP Apps, integracja nie będzie stanowić problemu. Nawet serwer, który znajduje się w przykładzie **04\_05\_apps** już teraz może być podłączony do Claude.ai.

MCP Apps nie mają też na celu pełnego zastąpienia narzędzi, lecz po prostu ułatwienie dostępu do wybranych funkcjonalności bądź danych. Na ostatniej wizualizacji znajdują się przyciski takie jak "**Add follow-up todo**" lub "**Open in Stripe**", które pełnią dokładnie tę rolę.

Poza tym fakt, że MCP Apps zwykle prezentowane są w kontekście interfejsu czatu i rzeczywiście tam sprawdzają się świetnie, tak nie oznacza wcale, że nie mogą być zastosowane na przykład w innych obszarach aplikacji. Tam również może pojawiać się AI czy nawet agenci, ale bez możliwości przesyłania wiadomości o dowolnej treści.

Podsumowując, możliwość wyświetlania interaktywnych interfejsów pozwala na:

- Przedstawienie danych w formie wizualnej, z którą znaczniej wygodniej się jest zapoznać
- Udostępnienie **deterministycznych** akcji, ponieważ interfejs obsługiwany jest z pomocą kodu
- Połączenie danych oraz akcji pochodzących z wielu narzędzi, co znacznie ułatwia wykonywanie powtarzalnych czynności na określonych stanowiskach

Jednocześnie MCP Apps z pewnością nie stanowią alternatywy dla bezpośredniego zaangażowania agentów, ponieważ są to rozwiązania komplementarne. Wiele też wskazuje na to, że generatywne interfejsy będą wciąż zyskiwać na popularności, aczkolwiek obecnie są jeszcze na bardzo wczesnym etapie kształtowania.

Na wizualizacji poniżej widzimy ogólną architekturę aplikacji wykorzystującej koncepcję generatywnych interfejsów. Choć mówi ona wprost o MCP Apps, to główne komponenty raczej będą pozostawać takie same, niezależnie od stosowania protokołu czy własnych implementacji.

Widzimy więc poniżej jasny podział na warstwę prezentacji (np. aplikacja webowa) oraz back-end w ramach którego funkcjonuje nasze API, połączenie z LLM oraz klient MCP zarządzający połączeniem z serwerem udostępniającym interfejsy oraz akcje. Sam serwer MCP udostępnia nam **narzędzia** pozwalające na wykonanie akcji i/lub wyświetlenie interfejsu.

![Architektura aplikacji wykorzystująca generatywne interfejsy](https://cloud.overment.com/2026-03-15/ai-devs_4_mcp_apps_design-7b940be1-a.png)

Mówimy tutaj także o sytuacji, która jest bardzo rzadko spotykana, lecz dopuszczalna, czyli **jednym serwerze MCP podłączonym do więcej niż jednej usługi**. Oczywiście należy podchodzić do tego z rozsądkiem, ponieważ znacznie zwiększa to złożoność serwera i potencjalnie zmniejsza jego elastyczność.

## Fabuła

![https://vimeo.com/1179335902](https://vimeo.com/1179335902)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze piąty!

Mamy już informacje, które miasto oferuje jaki towar. Wiemy, z kim należy się skontaktować i wiemy także, kto ma jakie potrzeby.

Tak jak wspominałem wczoraj: nasze magazyny może nie świecą pustkami, ale zdecydowanie nie wystarczą do nakarmienia kilku miast. Zygfryd jednak posiada wystarczającą ilość jedzenia, aby wykarmić ich wszystkich. Dlaczego mielibyśmy z tego nie skorzystać?

Mój plan, o którym wspominałem, polega na tym, aby włamać się - nie fizycznie (to byłoby zbyt niebezpieczne!), a w pełni wirtualnie - do systemów zarządczych centralnych magazynów Zygfryda. To tam trzymane są jedzenie, woda i narzędzia.

Twoim celem jest przeprogramowanie systemu dystrybucji w taki sposób, aby niezbędne towary trafiły do potrzebujących. Sami nie jesteśmy w stanie po nie pojechać ani ich zawieźć do konkretnych miast, ale autonomiczne systemy transportujące obecne w magazynach są w stanie dostarczyć to, co trzeba, tam, gdzie trzeba. Wykorzystamy to.

I tak się jakoś dobrze złożyło, że Zygfryd nie śledzi systemem "OKO" swojego własnego sprzętu. Ruchy transporterów zarządzanych przez System nigdy nie podnoszą alarmu.

Mówiłem Ci, że ten plan raczej nie spodoba się Zygfrydowi, ale z drugiej strony... to jest całkiem sprytne no i może odrobinę wredne zarazem, prawda?

Może zastanawiasz się, po co my to wszystko robimy? Przecież i tak planujemy zmienić przyszłość i przeszłość, a w konsekwencji wyzerować linię czasową w której się znajdujemy, więc wszystkie nasze poczynania pójdą na marne.

No właśnie... Ja nie mam w sobie tyle odwagi, aby tak myśleć. Zawsze istnieje ryzyko, że nasza misja się nie powiedzie. Wtedy do skoku nie dojdzie, a ci ludzie... oni po prostu zginą. Nie chcę żyć z poczuciem, że mogłem ich uratować, ale nic nie zrobiłem.

Nawet jeśli za ten tydzień, czy dwa okaże się, że cała misja była bez sensu, to i tak zostanie nam poczucie, że robiliśmy coś dobrego dla dobra ludzi. To mi wystarczy aby działać, a Tobie numerze piąty?

Jeśli jesteś ze mną, to w notatkach zapisałem więcej informacji na temat mojego planu.

## Zadanie praktyczne

Musisz uporządkować pracę magazynu żywności i narzędzi tak, aby przygotować jedno poprawne zamówienie, które zaspokoi potrzeby wszystkich wskazanych miast. Do dyspozycji dostajesz gotowe API magazynu, generator podpisów bezpieczeństwa oraz dostęp tylko do odczytu do bazy danych, z której trzeba wyciągnąć dane potrzebne do autoryzacji zamówienia.

To zadanie nie polega na zgadywaniu. Najpierw poznaj strukturę danych, później ustal pełne zapotrzebowanie miast, a na końcu zbuduj jedno zamówienie, którego zawartość będzie zgodna z wymaganiami Centrali.

Nazwa zadania: **foodwarehouse**

Odpowiedź wysyłasz do: https://hub.ag3nts.org/verify

Plik z zapotrzebowaniem miast: https://hub.ag3nts.org/dane/food4cities.json

W tym zadaniu rozmawiasz także z bazą danych **SQLite**. Dostęp do niej jest wyłącznie w trybie odczytu.

Na początek najlepiej pobrać pomoc API:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "help"
  }
}
```

### Jak działa API

Każde wywołanie wysyłasz do `/verify` w polu `answer` jako obiekt z polem `tool`.

Najważniejsze narzędzia:

- **orders** - odczyt, tworzenie, uzupełnianie i usuwanie zamówień
- **signatureGenerator** - generowanie podpisu SHA1 na podstawie danych użytkownika z bazy SQLite
- **database** - odczyt danych i schematów z bazy SQLite
- **reset** - przywrócenie początkowego stanu zamówień
- **done** - końcowa weryfikacja rozwiązania

Jeśli po drodze namieszasz w stanie zadania, użyj `reset`:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "reset"
  }
}
```

### Praca z zamówieniami

Możesz pobrać listę aktualnych zamówień:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "orders",
    "action": "get"
  }
}
```

Nowe zamówienie tworzysz dopiero wtedy, gdy znasz już tytuł, `creatorID`, kod `destination` oraz poprawny podpis:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "orders",
    "action": "create",
    "title": "Dostawa dla Torunia",
    "creatorID": 2,
    "destination": "1234",
    "signature": "tutaj-podpis-sha1"
  }
}
```

Po utworzeniu zamówienia możesz dopisywać towary pojedynczo:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "orders",
    "action": "append",
    "id": "tutaj-id-zamowienia",
    "name": "woda",
    "items": 120
  }
}
```

Możesz też użyć **batch mode** i dopisać wiele pozycji naraz. To ważne, bo `orders.append` przyjmuje również obiekt z wieloma towarami:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "orders",
    "action": "append",
    "id": "tutaj-id-zamowienia",
    "items": {
      "chleb": 45,
      "woda": 120,
      "mlotek": 6
    }
  }
}
```

Jeżeli dopiszesz do zamówienia towar, który już w nim istnieje, system zwiększy jego ilość zamiast tworzyć duplikat.

### Odczyt bazy SQLite

Możesz sprawdzić, jakie tabele znajdują się w bazie:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "database",
    "query": "show tables"
  }
}
```

Możesz też wykonywać zapytania select:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "database",
    "query": "select * from tabela"
  }
}
```

### Co musisz zrobić

- Ustal, które miasta biorą udział w operacji na podstawie pliku `food4cities.json`
- Znajdź odpowiednie wartości dla pola `destination` dla tych miast
- Odczytaj z `food4cities.json`, jakie towary i ilości są potrzebne w każdym z tych miast
- Przygotuj osobne zamówienie dla każdego wymaganego miasta
- Każde zamówienie utwórz z poprawnym `creatorID`, `destination` i podpisem wygenerowanym na podstawie danych z bazy SQLite
- Uzupełnij zamówienia dokładnie tymi towarami, których potrzebują miasta. Bez braków i bez nadmiarów
- Gdy wszystko będzie gotowe, wywołaj narzędzie `done`

### Dodatkowe uwagi

- Musisz utworzyć tyle zamówień, ile mamy miast w pliku JSON
- Jeśli coś zepsujesz po drodze, użyj `reset`, żeby wrócić do stanu początkowego
- Każde zamówienie musi mieć poprawny `creatorID` oraz `signature`

Gdy uznasz, że wszystkie wymagane zamówienia są gotowe, wyślij finalne sprawdzenie:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "foodwarehouse",
  "answer": {
    "tool": "done"
  }
}
```

Jeśli komplet zamówień będzie zgodny z potrzebami miast, trafi pod właściwe kody docelowe i zachowa poprawne podpisy, Centrala odeśle flagę.
