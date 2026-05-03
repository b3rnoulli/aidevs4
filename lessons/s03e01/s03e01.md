---
title: S03E01 — Obserwowanie i ewaluacja
space_id: 2476415
status: scheduled
published_at: '2026-03-23T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/evals-1773910362.png'
circle_post_id: 30844594
---
## Film do lekcji

![https://vimeo.com/1175527097](https://vimeo.com/1175527097)

Nawet najmniejsze zmiany w instrukcji systemowej, opisie narzędzi czy formacie odpowiedzi mogą znacząco wpływać na zachowanie systemu. W przypadku prostych promptów relatywnie łatwo możemy dostrzec problemy i je naprawić. Sytuacja komplikuje się, gdy w ich treści pojawiają się dynamiczne dane, a struktura składa się z wielu modułów. Jeśli dołożymy do tego kontekst konwersacji, a potem rozgałęzienia w aktywnościach wielu agentów, wyzwaniem staje się nawet przeczytanie treści zapytania do API.

W tym miejscu wchodzą do gry narzędzia do ewaluacji zachowań agentów oraz ich monitorowania w sposób wykraczający poza podstawowe logowanie zdarzeń. Wiemy już jednak, że na zachowanie modelu mogą wpłynąć nawet najmniejsze zmiany, a skoro tak, to po co nam testy?

Z pewnością nie możemy myśleć o ewaluacji w ten sam sposób jak o testach integracyjnych czy E2E. Tutaj nie weryfikujemy deterministycznej logiki, lecz sprawdzamy w jakim stopniu otrzymany rezultat spełnia nasze założenia oraz czy nie wykracza poza ustalone ramy. Nie szukamy więc tu raczej 100% dopasowania do oczekiwanych wyników, lecz bardziej osiągnięcia wystarczającego poziomu dla ustalonych wskaźników. Poziomy te czasem mogą być zweryfikowane **programistycznie**, czasem z pomocą **LLM**, a niekiedy także będą oceniane przez **człowieka**.

Działania modelu charakteryzują się obecnością języka naturalnego, w przypadku którego rzadko możemy programistycznie określić zgodność z początkowymi założeniami. Jeśli teraz przedstawię się, mówiąc: „**Mam na imię Adam**”, a chwilę później: „**Jestem Adam**”, to w obu przypadkach sens zostaje zachowany, ale zmieniają się cechy tych dwóch wypowiedzi. Podobnie też możemy mówić tylko o częściowej zgodności z założeniami, co może zostać poddane ocenie.

Przyczyny konkretnych zachowań modeli mogą pozostawać dla nas nieznane i w praktyce trudno jednoznacznie powiedzieć, które elementy interakcji odegrały istotną rolę. Dlatego trudno też mówić o bezpośrednim **debugowaniu** agentów w tym zakresie. Jeśli jednak zaczniemy pracować nad promptami w aplikacji działającej już na produkcji, z pewnością zauważymy wpływ instrukcji na skuteczność realizacji zadań oraz satysfakcję użytkowników. Z tego powodu ewaluacje, które pozwalają przewidzieć negatywne efekty przed publikacją zmian, są wręcz wskazane, nawet jeśli nie dadzą nam pełnej pewności.

Poza tym sama ewaluacja może odbywać się nie tylko **przed publikacją** (offline eval), ale także **w trakcie działania aplikacji** (online eval). Interakcje z użytkownikami mogą być automatycznie oceniane i weryfikowane pod kątem potencjalnych naruszeń, których z jakiegoś powodu nie wychwyciły mechanizmy wbudowane bezpośrednio w system.

Natomiast samo **obserwowanie** logiki agentów okazuje się niezwykle przydatne w kontekście **analizy błędów**, **estymacji kosztów** czy zauważania problemów z wydajnością aplikacji. W przypadku bardziej złożonych systemów agentowych, monitorowanie jest także kluczowe na etapie developmentu, ponieważ w samym dość trudne bywa zrozumienie zależności pomiędzy agentami oraz ich narzędziami, bo zbyt dużo informacji jest dynamicznie wczytywana, więc nie znajduje się bezpośrednio w kodzie aplikacji.

Do pełnego obrazu na tym etapie musimy dodać także Guardrails, czyli mechaniki związane z moderacją i filtrowaniem treści oraz blokowaniem niepożądanych zapytań. Całość prezentuje się następująco:

![Observability i Evals](https://cloud.overment.com/2026-02-17/ai_devs_4_evals-7a5c150e-8.png)

Także Evals nie zastępują testów jednostkowych czy e2e, ponieważ ich uwaga jest skierowana na zachowanie modelu oraz agentów, aczkolwiek momentami może sięgać w elementy logiki. Choć wdrożenie ewaluacji oraz obserwowania aplikacji może być wymagające, tak warto po prostu zacząć. A jeśli projekt jest dopiero na etapie planowania założeń i architektury, to bezwzględnie należy je wziąć pod uwagę.

## Użyteczność obserwacji w praktyce

Załóżmy bardzo prosty scenariusz w którym agent zapytany o przeszukanie historii interakcji ze wskazaną osobą twierdzi, że nie ma jej w bazie wiedzy. Narzędzia nie zwracają wyraźnego błędu, a logika wyszukiwania wydaje się być w porządku. Dopiero po sprawdzeniu zachowania agenta i prześledzeniu jego kroków okazuje się, że przeszukiwał on niewłaściwy obszar z powodu pokrywających się opisów.

Poniżej wyraźnie widzimy ten problem, a równie łatwo jest go dostrzec w raportach obserwacji zachowań agenta. Natomiast zauważenie tego błędu w samym kodzie może być bardzo trudne. Tym bardziej, że mówimy tu nie tylko o nieścisłościach w pojedynczych instrukcjach, lecz różnych wariantach ich połączenia. Na przykład początkowo agent może poprawnie rozpoznawać obszary wiedzy, ale treść kontekstu może na pewnym etapie mieć na to negatywny wpływ.

![Debugowanie aplikacji](https://cloud.overment.com/2026-02-17/ai_devs_4_debugging-93b04837-2.png)

Przy wdrażaniu aplikacji, a nawet pojedynczych funkcjonalności, w których pojawiają się LLM-y, zawsze będzie pojawiać się wątek kosztów. Na tym etapie powinno być już dla nas oczywiste, że nawet przybliżone estymacje bywają niezwykle trudne. Pod uwagę musimy wziąć nie tylko tokeny związane z instrukcjami systemowymi czy definicjami narzędzi, ale całych interakcjach, które mogą się znacznie od siebie różnić. W praktyce wśród użytkowników znajdą się osoby, które z jakiegoś powodu będą osiągać limity znacznie szybciej niż pozostali. I choć tutaj **twarde limity** są krytyczne, tak przyczyną problemu nie musi być intencjonalne działanie, lecz jakiś błąd po naszej stronie.

![Czynniki wpływające na koszt tokenów](https://cloud.overment.com/2026-02-17/ai_devs_4_costs-1c8f8bc2-f.png)

Gdy mamy do dyspozycji statystyki aktywności oraz raporty kosztowe, nawet w małej skali stają się one niezwykle użyteczne i bezpośrednio przekładają się na większą precyzję estymacji. Dla wielu produktów może to być kwestia "być albo nie być". Poza tym monitorowanie kosztów to nie tylko możliwość estymacji, lecz także szybkie reagowanie w przypadku błędów aktualizacji albo działań intencjonalnych ze strony użytkowników lub osób trzecich. To z kolei przydaje się także w przypadku obsługi klienta, gdy użytkownik raportuje problem, a my bezpośrednio możemy sprawdzić jego ostatnie aktywności.

## Zasady monitorowania zachowań modelu

Niezależnie od tego na jaki sposób obserwowania aplikacji się zdecydujemy, będą obowiązywać nas podobne zasady. U ich podstaw stoi konieczność podłączenia się pod wszystkie **interakcje z LLM API** oraz **wywołania narzędzi**. Dobrze jest więc na etapie planowania architektury ułożyć te elementy tak, aby były możliwe scentralizowane. Jednocześnie samo zdarzenie nie jest jedyną informacją, która nas interesuje, ponieważ w praktyce, będziemy chcieli przekazać **niemal cały kontekst sesji!** Można to zrozumieć na przykładzie Langfuse, gdzie monitorowanie obejmuje elementy takie jak:

- **Session:** zwykle powiązana z wątkiem (np. czatu) bądź zadaniami agentów.
- **Trace:** zwykle pojedyncza interakcja użytkownika (np. wiadomość czatu)
- **Span:** dotyczy czasu trwania wybranych akcji (np. gromadzenie kontekstu)
- **Generation:** to interakcja z LLM, obejmuje cały kontekst zapytania i ustawienia
- **Agent:** obejmuje działanie agenta w trakcie interakcji
- **Tool:** obejmuje uruchomienie narzędzia (input/output)
- **Event:** obejmuje zdarzenia z aplikacji, niekoniecznie powiązane z LLM

Langfuse wymienia także inne [typy zdarzeń](https://langfuse.com/docs/observability/features/observation-types), natomiast te z listy powyżej są najbardziej uniwersalne. Poza tym, zasady w ich przypadku pozostają takie same - zależy nam nie tylko na przekazaniu informacji o tym, co ma miejsce **tu i teraz**, ale także **w jakim kontekście** się to odbywa. Chodzi więc o **identyfikator użytkownika**, **identyfikator sesji**, **identyfikatory agentów** czy dowolne inne dane, które są istotne z punktu widzenia naszej aplikacji.

![Przykład architektury aplikacji ze scentralizowaną logiką obserwowania z zachowaniem kontekstu](https://cloud.overment.com/2026-02-17/ai_devs_4_monitoring-2ab9aacf-1.png)

Także trudność w poprawnym podłączeniu monitoringu aplikacji jest podobna do klasycznych systemów logów. Tutaj jednak występuje także wyraźna potrzeba **grupowania** oraz **zagnieżdżania** obserwowanych zdarzeń.

> Wskazówka: przy podłączaniu do platform takich jak Langfuse warto skorzystać z ich oficjalnego SDK. Kod źródłowy powinien zostać przeanalizowany przez agenta kodującego w kontekście interfejsu. Na tej podstawie możemy stworzyć notatkę, której treść będzie świetnym źródłem informacji zawsze wtedy, gdy będziemy dodawać kolejne funkcjonalności związane z observability.

W lekcji **S01E05** omawialiśmy przykład **01\_05\_agent**, w przypadku którego możemy podać klucze API do Langfuse. Wówczas każda interakcja będzie automatycznie monitorowana i jest to najprostszy sposób na doświadczenie związanych z tym możliwości w praktyce.

Obserwowanie zachowań agentów wiąże się także bezpośrednio z **przetwarzaniem danych użytkowników**. Tutaj oczywiście możemy skorzystać z narzędzi open source, jednak musimy mieć na uwadze sposób przetwarzania tych danych. Jak za chwilę się przekonamy, mówimy o bardzo istotnym źródle danych, które możemy wykorzystać do ewaluacji aplikacji. Nawet jeśli będziemy jedynym podmiotem przetwarzającym te dane, nadal musimy zadbać o anonimizację obejmującą nazwy własne, adresy, dane kontaktowe, dane osobowe itp.

## Odtwarzanie stanu interakcji i debugowanie

Zapisywanie interakcji na potrzeby obserwowania zachowań nie musi mieć wyłącznie pasywnej formy. Niemal każda platforma (np. [Confident AI](https://www.confident-ai.com/)) posiada wbudowany **Playground** (lub jego odmianę), w którym łatwo możemy zmienić parametry zapytania i wykonać je ponownie na potrzeby testów. I choć nie mówimy tutaj o zachowaniu 100% funkcjonalności (np. połączenia z narzędziami), to jest to dobry sposób na zweryfikowanie założeń.

Zatem w ramach integracji z np. Langfuse musimy zadbać o przesyłanie **instrukcji systemowej**, **historii wiadomości** oraz **listy narzędzi**. Wówczas po uruchomieniu Playground mamy możliwość swobodnego edytowania każdego elementu interakcji oraz weryfikowania, jaki ma to wpływ na działanie modelu. Istnieje także możliwość **porównywania** różnych modeli.

![Playground do debugowania zachowań LLM](https://cloud.overment.com/2026-02-18/ai_devs_4_playground-1c0e26df-6.png)

> Ciekawostka: choć na poziomie teorii ma to dość umiarkowany sens, czasem sprawdza się zadanie modelowi pytania o **uzasadnienie** decyzji, na przykład dotyczącej wyboru narzędzi. Otrzymana odpowiedź bardzo często zawiera wskazówki, które pomagają zrozumieć przyczyny problemu oraz je zaadresować. Warto wiedzieć, że taka praktyka stoi w kontrze z "[Tracing the thoughts of a large language model](https://www.anthropic.com/research/tracing-thoughts-language-model)".

Takie debugowanie zachowania modelu lub agenta AI ma niewiele wspólnego z debugowaniem kodu. Nawet jeśli zmiana instrukcji lub opisów narzędzi pozytywnie wpłynie na zachowanie modelu w danym przypadku, nadal nie wiemy, czy nie spowoduje problemów gdzie indziej. To właśnie dlatego tak dużo mówiliśmy o generalizowaniu instrukcji oraz opisywaniu zasad i wzorców zamiast konkretnych poleceń. Wykrycie problemu, a nawet jego proste zaadresowanie, nie oznacza końca pracy. Warto sprawdzić, jak wprowadzone zmiany wpływają na resztę systemu.

## Wersjonowanie instrukcji systemowych

Instrukcje systemowe niemal zawsze stanowią integralną część kodu źródłowego aplikacji, a niekiedy są przechowywane w bazie danych. W tym pierwszym przypadku można mówić o automatycznej kontroli wersji, ponieważ za pomocą Gita możliwe jest przywracanie zmian. Jednak w systemach agentowych nie jest to wystarczające, ponieważ interesuje nas nie tylko treść instrukcji, lecz także powiązane z nią statystyki oraz historia uruchomień.

Tutaj ponownie te same platformy pozwalają nam **zapisywać instrukcje** oraz je **wersjonować**, a nawet uzależniać je od środowiska (np. deweloperskiego). Dodane prompty mogą być powiązane ze wszystkimi aktywnościami systemu, a także ewaluowane na wybranych zestawach danych testowych. Do gry wchodzi także **monitorowanie kosztów**, wydajności, ogólnej skuteczności czy nawet zadowolenia użytkowników.

![Statystyki promptów i ich wersjonowanie](https://cloud.overment.com/2026-02-18/ai_devs_4_prompts_versioning-3c71c451-4.png)

Platformy do monitorowania generatywnych aplikacji dość mocno sugerują wartość wynikającą z przechowywania instrukcji wewnątrz nich. Doświadczenie sugeruje jednak, że technicznie nie zawsze będzie to możliwe, co jest problemem ponieważ raczej będzie nam zależało na kompletnych statystykach. Wówczas wystarczającym rozwiązaniem może okazać się **jednostronna synchronizacja**, w przypadku której zmiany po stronie aplikacji są odzwierciedlane np. w Langfuse. Choć tracimy tu możliwość łatwego przełączania się pomiędzy wersjami promptów to i tak raczej nie będzie stanowiło to problemu, bo największa wartość i tak wiąże się z możliwością łatwej oceny bieżącego stanu.

Całość integracji widać na schemacie poniżej. Mamy więc tu **szablony agentów** (w plikach markdown), ale też mogą to być wszystkie pozostałe prompty obecne w naszym kodzie. Każdy z nich powinien być zarejestrowany na platformie Langfuse. Dalej mamy pełną integrację z poszczególnymi akcjami agentów, co otwiera nam przestrzeń na "debugowanie" oraz przeprowadzanie eksperymentów.

![Synchronizacja promptów](https://cloud.overment.com/2026-02-18/ai_devs_4_prompt_observability-a9adef49-e.png)

Integracja od strony technicznej z platformami takimi jak Langfuse, może być niemal w całości zrealizowana przez AI, ale związane z nią detale są uzależnione od nas, czyli:

- **Kontekst:** dane specyficzne dla naszego projektu takie jak licencje (np. trial), uprawnienia konta (np. manager), preferencje użytkownika (np. ustawienia trybu web search), rodzaj zapytania (np. zaplanowane zadanie CRON)
- **Metadata:** informacje na temat połączenia, interfejsu, wersji aplikacji, otoczenia (np. lokalizacji)

Poza tym sama struktura obserwacji również w dużym stopniu zależy od nas. Na przykład logowanie **span** wykorzystywane do monitorowania czasu wybranych aktywności jest wyłącznie naszą inicjatywą i możemy z nich całkowicie zrezygnować. Podobnie też sami decydujemy o stosowaniu typu "**event**", ponieważ on także jest uzależniony od kontekstu naszej aplikacji. Po utworzeniu **minimalnej** integracji z platformą do obserwowania aplikacji, od razu dostrzeżemy rzeczy, których będzie nam brakować. Równie szybko ujawnią się problemy związane z **brakującymi** bądź **nadmiernymi** logami.

W przykładzie **03\_01\_observability** znajduje się minimalny agent, którego aktywności trafiają bezpośrednio do Langfuse (należy uzupełnić klucze w pliku `.env`) i obejmują poprawne połączenie z narzędziami oraz promptami. Po jego uruchomieniu wystarczy przesłać zapytanie np. `curl -sS -X POST "http://127.0.0.1:3000/api/chat" -H "content-type: application/json" -d '{"message":"Use tools: UTC now and sum 1,2,3"}' -w "\nHTTP %{http_code}\n"`, a informacja o nim pojawi się w panelu Langfuse w ciągu około 1-2 minut.

## Narzędzia do ewaluacji skuteczności systemu

Po konfiguracji obserwacji systemu możemy przejść do działań związanych z ewaluacją. Proces te zwykle będą ze sobą powiązane, ponieważ treść logowanych zdarzeń może być poddawana ocenie. Taka zależność sprawia, że dostępne na rynku narzędzia zwykle będą oferować nam jedno i drugie.

**Eval** (skrót od "ewaluacja") to ustrukturyzowany test oceniający elementy systemu pod kątem ustalonych metryk. Ewaluacja może być ukierunkowana na optymalizację **jakości, stabilności, skuteczności, wydajności czy kosztów**. Sam eval składa się z:

- **Zadania:** składa się z **danych wejściowych** (input) oraz danych wyjściowych (output). Może obejmować pojedynczy prompt, bądź całą interakcję.
- **Danych:** to zestaw przykładów, które mogą zostać utworzone syntetycznie bądź na podstawie danych produkcyjnych. Zwykle mówimy o połączeniu obu tych form, a dane syntetyczne to dobry punkt startowy.
- **Oceny:** określa jak zachowanie modelu jest dopasowane do oczekiwanego rezultatu poprzez zakres 0-1 (zwykle przedstawiany jako 0 - 100%). Ocena może być generowana deterministycznie z pomocą kodu, bądź przez LLM.

Opracowanie ewaluacji to zwykle bardzo żmudny proces, często wymagający dużej ilości pracy manualnej i weryfikacji. Co więcej, osiągnięcie wysokiego wyniku nie zawsze oznacza, że rezultat jest zgodny z oczekiwaniami. Czasem może się okazać, że to nie system, lecz testy wymagają optymalizacji, bo np. wynik został oceniony gorzej, mimo że w praktyce jest znacznie lepszy.

![Ocena skuteczności ewaluacji](https://cloud.overment.com/2026-02-19/ai_devs_4_evals_decision-79cca19e-9.png)

Powiedzieliśmy, że ewaluacje mogą odbywać się w trybie **offline** i **online**. W tym pierwszym przypadku chodzi więc o opracowanie testów weryfikujących skuteczność promptów (lub agentów czy systemów RAG), uruchamianych w środowisku developerskim lub na etapie wdrażania aplikacji (np. w ramach CI/CD).

Platformy takie jak Langfuse umożliwiają konfigurację i uruchomienie ewaluacji z poziomu interfejsu, ale także **z poziomu API**. Możemy więc zaprojektować eksperymenty bezpośrednio w kodzie i tam również analizować ich wyniki. Rezultaty będą też widoczne na platformie.

W przykładzie **03\_01\_evals** mamy przykład prostego agenta, którego logika również jest połączona z platformą Langfuse. Jednak w tym przypadku mamy do dyspozycji także skrypt **npm run evals:tools** oraz **npm run evals:response**, który uruchamia eksperyment dotyczący skuteczności posługiwania się narzędziami oraz precyzji odpowiedzi Dodatkowo **dataset** pojawi się na platformie Langfuse w zakładce **Datasets**, a wewnątrz niego dostępne będą także wszystkie statystyki dotyczące skuteczności.

Po uruchomieniu eksperymentu warto zapoznać się z jego wynikami oraz dostępnymi metrykami. Na początku mogą wydawać się przytłaczające, ale dość szybko można oswoić się z kluczowymi danymi. Poza tym ich struktura i rola będą uzależnione od naszych potrzeb, więc na tym etapie potrzebujemy jedynie ogólnego zrozumienia dostępnych możliwości.

![](https://cloud.overment.com/2026-02-19/ai_devs_4_experiment-d7a895d5-5.png)

Sens eksperymentów w dużym stopniu zależy od jakości zestawów danych, które w naszym przypadku znajdują się w pliku **tool-use.synthetic.json** i, jak sugeruje nazwa, zostały wygenerowane przez AI. Dla nas, jako programistów, kluczowe będą najważniejsze zasady projektowania takich datasetów. W tym miejscu wchodzimy w obszar, o którym moglibyśmy rozmawiać przez kilka lekcji, więc skupimy się tylko na najistotniejszych aspektach.

Przy projektowaniu danych testowych należy zwrócić uwagę na:

- **Pokrycie:** przykłady muszą obejmować wszystkie kategorie zachowań, tak aby eksperyment pokazywał nie tylko pozytywne scenariusze, ale także te negatywne, wykraczające poza podstawowe założenia.
- **Różnorodność:** scenariusze powinny być różnorodne na tyle, aby pokazać jak najszerszy obraz działania promptu / agenta w różnych warunkach.
- **Balans:** pokrycie scenariuszy pod kątem różnorodności oraz ilości testów nie powinno być skrzywione w wybranych kierunkach, ponieważ może to zaburzać wyniki eksperymentu. Przykładowo przy testowaniu agenta dysponującego 5 narzędziami, powinniśmy rozdysponować uwagą pomiędzy każdym z nich oraz przypadkom wykraczającym poza "szczęśliwe ścieżki".

Bardzo wartościową perspektywę w kontekście evals daje także zespół [Braintrust](https://www.braintrust.dev/), który zwraca uwagę strukturę promptu. W kontekście agentów podczas trwającej interakcji to **odpowiedzi narzędzi** szybko zaczynają stanowić większość promptu. Warto je więc uwzględniać także na etapie projektowania ewaluacji.

![Anatomia promptu](https://cloud.overment.com/2026-02-21/ai_devs_4_prompt_anatomy-a5279e56-1.png)

W praktyce, projektowanie datasetów będzie miało charakter iteracyjny oraz zwykle będzie angażować człowieka w zakresie weryfikacji rezultatów, a także dalszych modyfikacji.

![Główne zasady projektowania zestawów testowych](https://cloud.overment.com/2026-02-19/ai_devs_4_datasets-044ad554-1.png)

Te wszystkie możliwości są dostępne w bardzo zbliżonych formach w ramach platform takich jak:

- [Langfuse](https://langfuse.com/)
- [Promptfoo](https://www.promptfoo.dev/)
- [Confident AI](https://www.confident-ai.com/)
- [Braintrust](https://www.braintrust.dev/)
- [Grafana](https://grafana.com/)

Na podstawie własnych doświadczeń mogę polecić dwa pierwsze narzędzia. Pozostałe (a także wiele innych dostępnych na rynku) również warto przejrzeć pod kątem konkretnych funkcjonalności, które mogą okazać się istotne dla naszego projektu. W niektórych sytuacjach możemy też dojść do wniosku, że wystarczą nam proste, wewnętrzne skrypty, bez konieczności korzystania z zewnętrznych platform.

## Wartość i wyzwania związane z ewaluacją

Już nawet na podstawie tego, co powiedzieliśmy do tej pory, ewaluacje mogą budzić wiele wątpliwości. Po pierwsze ich obecność **nie gwarantuje nam** czegokolwiek. Aplikacja wciąż może zachowywać się niezgodnie z oczekiwaniami, a i na pewnym etapie trudno też powiedzieć gdzie w ogóle leży problem. Poza tym ewaluacja to często także dodatkowe koszty oraz potrzebne zasoby na ich opracowanie.

Na rynku pojawiają się także opinie, że najszybciej rozwijające się produkty **w ogóle nie testują zachowań modeli**! Kilka interesujących cytatów:

- Garry Tan (YCombinator): Evals are emerging as the real moat for AI startups.
- Kevin Veil (OpenAI): Writing evals is going to become a core skill for product managers.
- Mike Krieger (Anthropic): Writing evals is probably the most important thing right now.

A z drugiej strony mamy [wywiad z twórcą Claude Code](https://www.youtube.com/watch?v=iF9iV4xponk), który mówi **no evals**.

Myślę jednak, że w tej sytuacji można mówić o podobnym podejściu jak w przypadku testów E2E. Dla części programistów są one krytyczne, a dla innych całkowicie opcjonalne. Podobnie jest tutaj. Ostatecznie decyzja o tym, czy będziemy testować aplikację, czy nie, zależy od nas i powinna być dopasowana do zasobów oraz celu, który chcemy osiągnąć.

Z całą pewnością istotnym aspektem wdrożenia i utrzymania ewaluacji jest tempo w jakim chcemy się poruszać. Opracowanie datasetów, ich monitorowanie i ciągłe usprawnianie to także problem związany z **czasem**. Bo może się okazać, że na początkowych etapach nasze rozwiązania będą zmieniać się zbyt szybko, aby uzasadnić sens inwestowania zasobów w ewaluacje. Ale jeśli będziemy budować produkt w których stabilność czy efektywność kosztowa będą priorytetem, to wówczas trudno wyobrazić sobie ich rozwój bez ewaluacji.

## Wybór wskaźników sukcesu oraz zasad oceny

Narzędzia do ewaluacji oferują nam różne kryteria oceny (asercje) oraz metryki sukcesu. Część z nich będzie deterministyczna, a część będzie opierać się na generowanych przez modele rezultatach. Warto więc wiedzieć jakie opcje mamy tutaj do dyspozycji, aby móc swobodnie się po nich poruszać.

Dokumentacja Promptfoo dość dobrze zbiera w jednym miejscu [deterministyczne](https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic/) oraz [oparte o model](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/) kryteria oceny. Wśród nich mamy między innymi:

- **bezpośrednie porównania** takie jak **contains / is-json / equals / starts with** do sprawdzania obecności słów kluczowych czy wymaganych struktur. Tutaj do gry wchodzą również wyrażenia regularne
- **programistyczne porównania**, w przypadku których wykorzystujemy logikę JavaScript / Python w celu zweryfikowania treści. Może to obejmować nawet zapytania HTTP czy różnego rodzaju transformacje
- **llm-rubric** czyli ocena rezultatu przez model, pod kątem kryteriów opisanych w języku naturalnym
- **conversation-relevance** czyli ocena rezultatów pod kątem zgodności z kontekstem bieżącej interakcji
- **context-recall** skupia się na ocenie tego, jak skutecznie został przywołany kontekst (np. przez wyszukiwanie hybrydowe) na podstawie którego agent będzie udzielał odpowiedzi

Są to główne kryteria którymi będziemy kierować się przy ocenie wyników LLM. Każda odpowiedź może być weryfikowana pod kątem kilku z nich, więc możliwości konfiguracji jest nieskończenie wiele. Natomiast i tak będziemy chcieli je osadzić w konkretnych obszarach, takich jak:

- **Ocena skuteczności promptów:** dotyczy zarówno pojedynczych instrukcji, jak i umiejętności agentów
- **Skuteczność wyboru narzędzi:** weryfikuje czy agent sięga po odpowiednie narzędzia
- **Skuteczność posługiwania się narzędziami:** weryfikuje czy agent posługuje się narzędziami we właściwy sposób oraz jak dużo czasu potrzebuje na wykonanie zadania (np. liczba powtórzeń czy błędów)
- **Satysfakcja użytkownika:** opiera się o aktywny feedback ze strony użytkowników (np. przez "łapki w górę / dół")
- **Specyficzne testy:** dotyczy konkretnych aktywności, związanych na przykład ze skutecznością wyszukiwania.

Wybór kryteriów oceny oraz wskaźników sukcesu w dużym stopniu determinuje zestawy danych testowych, których potrzebujemy. Obecnie przy ich tworzeniu bardzo pomocne okazują się modele. Na podstawie opisanych przez nas kryteriów mogą nam pomóc przede wszystkim w ich uzupełnieniu oraz sprawdzeniu poprawności, a następnie w utworzeniu serii scenariuszy dla różnych przypadków. Później scenariusze te mogą być uzupełnione o odpowiadające im zestawy danych testowych.

Jak nietrudno się domyślić, AI świetnie odnajdzie się także w ocenie wyników eksperymentów oraz analizie logów aktywności wybranych użytkowników. Przykładowo w Langfuse możemy wyeksportować cały obiekt JSON dla danej interakcji lub eksperymentu i omówić go wspólnie z AI.

## Skuteczność agenta AI i wykrywanie naruszeń

Zatem budując system agentowy, musimy zastanowić się nad tym, jak dużą wartość da nam wprowadzenie ewaluacji. Jednocześnie wdrożenie samych narzędzi do monitorowania aktywności agentów wydaje się być **fundamentem**, a to otwiera nam dość prostą drogę do wdrożenia przynajmniej pojedynczych testów.

Najbardziej kluczowe mogą okazać się te weryfikujące skuteczność głównych elementów, czyli **wyboru narzędzi** oraz **ich obsługi** (przynajmniej w minimalnym stopniu). To pozwala na szybkie testowanie skuteczności nowych modeli oraz podejmowania decyzji o przełączaniu się na ich mniejsze wersje. Nikt też nie powiedział, że ewaluacje muszą być utrzymywane w systemie i nie możemy ich stworzyć jedynie tymczasowo, aby określić które obszary mogą być obsłużone przez mniejsze modele.

Poza korzystaniem z różnych modeli, bardzo wskazane jest podłączenie ewaluacji pod kątem **naruszeń** zarówno w kontekście **danych wejściowych** jak i **odpowiedzi modelu**. Są to miejsca w przypadku których może dojść nawet do daleko idących konsekwencji związanych z nieprawidłowym użytkowaniem produktu bądź błędów modelu. Dobrze jest więc wiedzieć, gdy coś idzie nie tak, nawet jeśli informacja dotrze do nas z niewielkim opóźnieniem. To samo dotyczy problemów związanych z **wydajnością, kosztami czy czasem reakcji**, aczkolwiek tutaj reagowanie na anomalie zwykle musi być zaadresowane w kodzie aplikacji.

Także podsumowując, umiejętność projektowania ewaluacji jest istotna i warto mieć z nią styczność przynajmniej w minimalnym wymiarze poprzez stopniowe wprowadzanie testów tam, gdzie system najbardziej tego wymaga.

## Fabuła

![https://vimeo.com/1175525087](https://vimeo.com/1175525087)

## Transkrypcja filmu z Fabułą

"Numerze piąty!

Znowu mi zaimponowałeś. Mamy już wodę. Powiedziałbym nawet, że przesadnie dużo wody, bo nasi technicy złożyli już zapotrzebowanie na kalosze. Ale lepiej w tę stronę.

Jak wiesz z logów, które ostatnio analizowałeś, mamy jeszcze kilka problemów do rozwiązania i niestety nie możemy zająć się wszystkimi jednocześnie. Teraz skupimy się na problemie firmware'u. Cały czas zgłasza błędy, produkuje dziwne zapisy z czujników, a do tego chyba nasz operator, który komentuje te wszystkie checki, nie robi tego zbyt rzetelnie.

Mamy prawie 10 tysięcy odczytów z różnych sensorów: czujniki wody, temperatury, napięcia, ciśnienia i jeszcze jakieś mieszane. Ja się na tym nie znam, ale wiem jedno: część z tych danych jest po prostu błędna, a Ty musisz powiedzieć, które to są.

Dzięki Twojej pracy namierzymy uszkodzone sensory, a jednocześnie będziemy mieć dowód na to, że operator po prostu się obija i czasami wpisuje nieprawdziwe informacje do notatek tylko po to, aby wyłączyć alarm.

Gdy namierzymy, co działa niepoprawnie, będziemy mogli wymienić te podzespoły na nowe. Co prawda nie posiadamy żadnych części zamiennych, ale wiesz, że jesteśmy dobrzy w kombinowaniu. Poradzimy sobie.

Więcej szczegółów jak i dane z czujników przesłałem Ci wraz z tym nagraniem."

## Zadanie

Twoim zadaniem jest znalezienie anomalii w odczytach sensorów.

Czujniki w naszej elektrowni potrafią mierzyć różne wartości. Czasami są to odczyty temperatury, ciśnienia, napięcia i kilka innych. Czujniki bywają jedno- albo wielozadaniowe. Wszystkie jednak zwracają dane w dokładnie takim samym formacie, co oznacza, że jeśli sprawdzasz dane z czujnika temperatury, to znajdziesz tam poza temperaturą także np. zapis napięcia, ale będzie on równy zero, ponieważ nie jest to wartość, którą ten czujnik powinien zwracać. Przy czujnikach zintegrowanych (2-3 zadaniowe), sensor może zwracać wszystkie pola definiowane przez sensory składowe.

Każdy odczyt czujnika jest też skomentowany przez operatora — czasami jednym słowem, a czasami jakąś dłuższą wypowiedzią. Niestety nie zawsze te notatki są poprawnie wpisywane. Pojawia się niekiedy błąd ludzki, a czasami to nierzetelność operatora.

Musisz zgłosić nam wszelkie anomalie. **Prześlij nam identyfikatory plików**, które zawierają przekłamane dane z czujników lub niepoprawną notatkę operatora.

Nazwa zadania to: **evaluation**

Odpowiedź wysyłasz do Centrali do **/verify** w formacie jak poniżej:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "evaluation",
  "answer": {
    "recheck": ["0001","0002","0003", "..."]
  }
}
```

Dane z sensorów pobierzesz tutaj: https://hub.ag3nts.org/dane/sensors.zip

Dane wysyłasz do centrali jako tablicę JSON (jak wyżej) zawierającą identyfikatory.

Akceptujemy poniższe formaty danych:

- stringi z identyfikatorem liczbowym — \["0001", "0002","4321"]
- liczby bez zera wiodącego — \[1, 2, 987]
- nazwy plików z błędami (pełne z zerami) — \["0001.json","0002.json","4321.json"]
- dane mieszane — \["0001.json",2,"4321"]

Każdy czujnik zwraca dane w poniższym formacie:

```json
{
  "sensor_type": "temperature/voltage",
  "timestamp": 1774064280,
  "temperature_K": 612,
  "pressure_bar": 0,
  "water_level_meters": 0,
  "voltage_supply_v": 230.4,
  "humidity_percent": 0,
  "operator_notes": "Readings look stable and within expected range."
}
```

Format danych w pojedynczym pliku JSON:

- **sensor\_type** — nazwa aktywnego sensora lub zestawu sensorów rozdzielonych znakiem `/`, np. `temperature`, `water`, `voltage/temperature`
- **timestamp** — unixowy znacznik czasu
- **temperature\_K** — odczyt temperatury w Kelwinach
- **pressure\_bar** — odczyt ciśnienia w barach
- **water\_level\_meters** — odczyt poziomu wody w metrach
- **voltage\_supply\_v** — odczyt napięcia zasilania w V
- **humidity\_percent** — odczyt wilgotności w procentach
- **operator\_notes** — notatka operatora po angielsku

W każdym pliku obecne są wszystkie pola pomiarowe. Dla sensorów nieaktywnych wartość powinna być ustawiona na **0**.

Zakres poprawnych wartości dla aktywnych sensorów:

- **temperature\_K**: od 553 do 873
- **pressure\_bar**: od 60 do 160
- **water\_level\_meters**: od 5.0 do 15.0
- **voltage\_supply\_v**: od 229.0 do 231.0
- **humidity\_percent**: od 40.0 do 80.0

Zadanie zostaje zaliczone, gdy prześlesz w jednym zapytaniu **identyfikatory wszystkich plików zawierających anomalie**.

Jako anomalie definiujemy:

- dane pomiarowe nie mieszczą się w normach
- operator twierdzi, że wszystko jest OK, ale dane są niepoprawne
- operator twierdzi, że znalazł błędy, ale dane są OK
- czujnik zwraca dane, których nie powinien zwracać (np. czujnik poziomu wody zwraca napięcie prądu)

### Wskazówki

Tam jest 10 000 plików JSON do analizy. Próba wrzucenia tego do LLM-a będzie DROGA. W tych danych mnóstwo informacji się powtarza.

Podpowiedź (spoiler w Base64):

`RHdpZSBwb2Rwb3dpZWR6aToKMSkgTExNLXkgbWFqxIUgc3fDs2ogY2FjaGUsIGFsZSBUeSB0YWvFvGUgbW/FvGVzeiBjYWNob3dhxIcgb2Rwb3dpZWR6aSBtb2RlbHUgcG8gc3dvamVqIHN0cm9uaWUuIEN6eSBuaWVrdMOzcmUgZGFuZSBuaWUgc8SFIHpkdXBsaWtvd2FuZT8KMikgQ3p5IHByemVwcm93YWR6ZW5pZSBrbGFzeWZpa2Fjamkgd3N6eXN0a2ljaCBkYW55Y2ggcHJ6ZXogbW9kZWwgasSZenlrb3d5IGLEmWR6aWUgb3B0eW1hbG5lIGtvc3p0b3dvPyBCecSHIG1vxbxlIGN6xJnFm8SHIGRhbnljaCBkYSBzacSZIG9kcnp1Y2nEhyBwcm9ncmFtaXN0eWN6bmllPw==`

- Zastanów się, którą część zadania powinien wykonać model językowy, aby nie przepalać zbytecznie tokenów i jak możesz taką weryfikację zoptymalizować pod względem kosztów. Które rodzaje anomalii powinny być wykrywane przez model językowy, a które przez programistyczne podejście?
- Kiedy dojdziesz do anomalii, które wymagają analizy przez LLM: czy musisz wysyłać do analizy każdy plik osobno? Przypomnij sobie też cenniki modeli — płaci się więcej za output niż za input. W jaki sposób możesz zminimalizować to, co zwraca model, mimo że wysyłasz do niego dużo danych?
- Przyjrzyj się plikom z danymi — technicy czasem są leniwi, i niektóre notatki są bardzo podobne do siebie. Możesz wykorzystać to do zoptymalizowania kosztów.
