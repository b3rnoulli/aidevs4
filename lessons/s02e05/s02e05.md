---
title: S02E05 — Projektowanie agentów
space_id: 2476415
status: scheduled
published_at: '2026-03-20T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/designing-a-team-1773303933.png'
circle_post_id: 30573319
---
![https://vimeo.com/1173227948](https://vimeo.com/1173227948)

» [Lekka wersja przeglądarkowa](https://cloud.overment.com/s02e05-projektowanie-agentow-1773309060.html) oraz [markdown](https://cloud.overment.com/s02e05-projektowanie-agentow-1773309033.md) «

Projektowanie agentów obejmuje także tworzenie ich instrukcji systemowej, przypisywanie narzędzi, umiejętności, wiedzy i ustawień oraz określanie ich roli w systemie. Coraz częściej oznacza to również **generowanie** agentów oraz ręczne lub autonomiczne **optymalizowanie**. Jeśli dodatkowo agent nie działa samodzielnie, lecz funkcjonuje w systemie wieloagentowym, konfiguracja staje się jeszcze bardziej wymagająca i rodzi pytania, na które niekiedy trudno odpowiedzieć.

Dlatego dziś skupimy się na kluczowych **zasadach**, które pozwolą nam projektować lepszych agentów pod kątem ich instrukcji / promptów. Do tej pory skupialiśmy się w dużym stopniu na architekturze i logice kodu. Tym razem wchodzimy w przestrzeń Prompt Engineeringu, który nadal pozostaje kluczowym elementem systemów wieloagentowych (pomimo powszechnej narracji, mówiącej o tym, że obecnie liczy się wyłącznie Context Engineering).

## Projektowanie instrukcji i zakresu odpowiedzialności

Powiedzieliśmy już sporo na temat kształtowania narzędzi, pamięci, a nawet podziału obowiązków między agentami. Kształtowanie instrukcji agentów wydaje się w tym wszystkim najprostszym etapem, bo "obecne modele są bardzo inteligentne". Problem w tym, że część ich zachowania nie będzie zależeć od poziomu inteligencji, lecz od "świadomości" ich roli oraz zasad poruszania się w otoczeniu. Możemy tu wyróżnić kilka obszarów:

- **Ustawienia:** to przede wszystkim **nazwa** oraz **opis**, na podstawie których agent może zostać wywołany przez innych agentów. Ustawienia obejmują także listę narzędzi, aktywne tryby (np. pamięć), uprawnienia (np. dostęp do folderów) oraz konfigurację agenta (np. model lub dostępność dla innych agentów). Choć sekcja ustawień jest raczej stała, domyślne wartości mogą być dostępne do zmiany podczas tworzenia instancji agenta. W takim przypadku szablon agenta może być **plikem tekstowym**, ale nie jest to wymagane.
- **Profil:** jest to opis "osobowości" oraz cech nadających charakter agenta. Nie mówimy tutaj tylko o prostym "Jesteś ekspertem (...)", ale też sterowaniu tonem wypowiedzi, poziomem złożoności, długością, formatem czy sięganiem po techniki pracy, rozumowania, analizy czy rozwiązywania problemów. Profil skupia uwagę modelu w pewnym sensie tak, jak zdanie "nie myśl o niebieskich motylach" zwykle kieruje nasze myśli w tę stronę. Dlatego cechy zawarte w profilu nie są tylko kwestią kosmetyczną, ale będą realnie wpływać na jakość pracy agenta.
- **Zasady:** o zasadach w instrukcji systemowej mówiliśmy już wcześniej. Natomiast teraz obejmują one także sposób komunikacji, radzenia sobie z problemami, dostępem do wiedzy czy oczekiwanych zachowań, gdy coś idzie niezgodnie z planem. Zgeneralizowanie tych zasad jest bardzo trudne, ponieważ z jednej strony nie możemy powiedzieć agentowi wszystkiego o naszym systemie, a jednocześnie musimy to zrobić - poprzez "zasady", a nie bezpośrednie "instrukcje".
- **Limity:** systemy agentowe dają modelom znacznie większe możliwości, niż te, które mają domyślnie. Nie chodzi wyłącznie o posługiwanie się narzędziami, ale pracę z informacjami. Na przykład jeśli agent posiada dostęp do lokalizacji użytkownika to czy oznacza, że jest ona zawsze aktualna czy należy ją pobierać co jakiś czas? Jeśli tak, to jak poznać kiedy ten czas nadszedł? Tym bardziej, że model domyślnie nie wie "**kiedy jest teraz?**" o ile mu tego nie powiemy. Informacje o limitach, aktualności posiadanej wiedzy czy dynamicznym poziomie uprawnień to coś, na co musimy zwrócić uwagę w instrukcji systemowej.
- **Styl:** sposób wypowiedzi agenta to nie tylko kwestia kosmetyczna, ale też jeden z kluczowych aspektów użyteczności. Wystarczy, że agent będzie mógł być podłączony do więcej niż jednego interfejsu, na przykład tekstowego i głosowego. Z lekcji S01E04 wiemy, że agent głosowy musi unikać na przykład dyktowania długich linków czy „wyświetlania” obrazów. Ale w tej sytuacji to nie narzędzie wpływa na sposób wypowiedzi, lecz **środowisko**, w którym aktualnie znajduje się agent.
- **Sesja:** Zmienne zależne od sesji również stanowią część instrukcji systemowej. Agent musi ostatecznie wiedzieć, z kim rozmawia, oraz jak dostosować swoje zachowanie do użytkownika, na przykład w związku z indywidualnymi preferencjami lub uprawnieniami. Z sesją mogą być też powiązane dynamiczne dane, takie jak bieżąca aktywność agentów, która nie będzie widoczna bezpośrednio w historii komunikacji.

Prompt agenta pod wieloma względami powinien kierować się zasadami, które omówiliśmy już w lekcji **S01E01**. Jednocześnie teraz nie skupiamy się wyłącznie na tym, co robi dany agent, ale również jego roli w systemie wieloagentowym oraz zmieniającym się środowisku.

Uchwycenie wszystkich zależności, ich nazwanie oraz ujęcie ich w odpowiednich instrukcjach nie jest proste. Tym bardziej że złożoność takich systemów rośnie bardzo szybko i nawet jeśli korzystamy z pomocy LLM do tworzenia promptów, może się okazać, że to również nam nie pomoże. Dlatego ponownie nie skupiamy się na systemie, który autonomicznie poprowadzi cały dział w firmie, a nawet "tylko" jeden proces. Nie ma nic złego w stworzeniu rozwiązania, które **wspiera** wybrane aktywności, a dopiero później stopniowo przejmuje kolejne. Możemy też podjąć decyzję o pozostawieniu procesu w rękach ludzi i to również jest w porządku.

## Zasady projektowania instrukcji agenta

Przenieśmy teraz projektowanie promptów agentów na nieco bardziej praktyczny poziom. Zrobimy to, analizując instrukcję główną agenta jednego z systemów, którego rolą jest nadzorowanie pracy pozostałych. Na wstępie zaznaczę tylko, że poza treścią istotne są tu przede wszystkim zasady wpływające na kształt instrukcji.

Poniżej widzimy pierwszą sekcję promptu agenta: `<identity>`. Jej rolą jest nadanie motywu przewodniego, który łączy **cechy charakteru**, **stylu wypowiedzi** oraz **zachowania**. Obejmuje obszary takie jak **zarządzanie, delegowanie, pamięć, świadomość otoczenia, stałe i tymczasowe informacje, autonomię, reagowanie na błędy, kontakt z użytkownikiem, komunikację oraz relacje**. Jest to zatem cała persona agenta, przedstawiona z szerokiej perspektywy. Nie ma tutaj detali ani ścisłego powiązania z narzędziami czy elementami konfiguracji. Są jednak obecne wyraźne odniesienia do każdego z nich.

> Interaktywna wersja poniższych wizualizacji jest dostępna [tutaj](https://cloud.overment.com/prompt-identity-anatomy-1771174103.html).

![Anatomia sekcji Identity promptu agenta AI](https://cloud.overment.com/2026-02-15/ai_devs_4_prompt_identity-82f06177-0.png)

Taka instrukcja powstała przy ścisłej współpracy z AI. Kontekst opierał się o **możliwości systemu**, **wiedzę o roli pozostałych agentów** oraz **moje preferencje**. Wiedziałem więc, że potrzebuję zaadresować kwestię delegowania zadań, dostępu do informacji oraz wzmocnić zachowania związane z autonomicznym działaniem. Wśród nich znalazły się także moje spostrzeżenia wynikające bezpośrednio z doświadczeń związanych z pracą z agentami AI oraz typowych błędów (np. pomijania wczytywania wspomnień, gdy polecenie nie sugeruje tego wprost, ale kontekst rozmowy już tak). Ostatecznie dojście do widocznego rezultatu wymagało **kilkunastu iteracji**.

Trzeba też tu podkreślić to, o czym już mówiliśmy: **obecność instrukcji w kontekście nie gwarantuje, że model będzie ich przestrzegać** oraz że poprawnie je zinterpretuje. Jednocześnie takie patrzenie na instrukcje systemowe do pewnego stopnia może mieć sens, czego dowodem jest projekt [Gemma Scope](https://www.neuronpedia.org/gemma-scope#microscope) pozwalający podejrzeć w jaki sposób modele Gemma "widzą" poszczególne koncepcje i jak łączą je ze sobą.

![](https://cloud.overment.com/2026-02-15/ai_devs_4_scope-6e6e5fc2-6.png)

Jednocześnie nie oznacza to, że kształtując instrukcję będziemy w stanie dokładnie sterować tym, jak model postrzega cały kontekst. Po prostu "ruchomych elementów" jest tu zdecydowanie za dużo. Z drugiej strony patrzenie na instrukcje przez ten pryzmat daje pewne wyczucie na temat tego, co może być istotne, a co nie.

W treści instrukcji nadałem także dość specyficzny ton oraz słownictwo, które momentami może wydawać się dziwne, np. "instynkt". Jest to celowy zabieg polegający na tym, aby nie tylko **mówić modelowi** co ma robić, ale także **pokazywać** to. Po prostu w tym przypadku zależy mi na tym, aby agent miał luźny styl komunikacji, ale też wchodził w obszary cech charakteru postaci, których imiona znajdują się na wizualizacji. Jest to także forma prowadzenia modelu poprzez skojarzenia, a nawet w pewnym sensie dążenia do wykorzystania faktu halucynacji na swoją korzyść. Zamiast oczekiwać od modelu, że zrobi **dokładnie to czego oczekujemy**, projektujemy system w taki sposób, aby stworzyć przestrzeń **by pozytywnie nas zaskoczył**. Być może nie jest to do końca inżynieryjne podejście do rozwijania oprogramowania, ale obecnie budowanie agentów z LLM jest na tak wczesnym etapie, że potencjalnie każdy pomysł może nas czegoś nauczyć i doprowadzić tam, gdzie jeszcze nikogo nie było. Oczywiście tak długo jak tylko rozwiązanie które tworzymy, pozwala nam na stosowanie takiego podejścia.

Tymczasem kolejnym elementem instrukcji agenta może być jego **protokół**, określający sposób działania, uwzględniający dostępne zasoby oraz stałe elementy otoczenia, takie jak jego pamięć, relacje wobec innych agentów czy samego systemu. Poniżej znajduje się druga wizualizacja,

> Interaktywna wersja poniższych wizualizacji jest dostępna [tutaj](https://cloud.overment.com/prompt-protocol-anatomy-1771174239.html).

![Anatomia sekcji Protocol & Memory promptu agenta AI](https://cloud.overment.com/2026-02-15/ai_devs_4_protocol-b0559b52-a.png)

**Protokół** widoczny powyżej ma na celu osadzić agenta w jego roli i wyznaczyć **zasady**, którymi ma się kierować. Zawiera także informacje o tym, jak zarządzać kontekstem i wspomnieniami, jak odnajdywać się w sytuacji, w której agent zostanie poproszony o coś, czego nie jest w stanie zrobić, oraz w jaki sposób ma prosić o pomoc. Ponownie nie ma tutaj nawiązań do **narzędzi**, którymi dysponuje agent, ponieważ te mogą być dynamiczne. Są za to już wzmianki **konkretnych katalogów**, a nawet plików, w których agent może znaleźć potrzebne informacje. Jednocześnie zachowany jest w tym balans, który nie wiąże agenta zbyt mocno z bieżącą strukturą katalogów. Można nawet dyskutować czy te pojedyncze wzmianki są uzasadnione, ale to już kwestia decyzji uzależnionej od kontekstu bieżącego projektu.

Przyznam, że nie mam stuprocentowej pewności, czy zaprezentowana instrukcja nie zawiera wyraźnych błędów. Jest to jednak najnowsza wersja, która aktualnie funkcjonuje w moim systemie. Przykładowo jedną z głównych wątpliwości jest balans pomiędzy kontekstem, który agent zarządzający musi zgromadzić samodzielnie, a tym, który pozostali agenci muszą zgromadzić indywidualnie. Trudno jest na poziomie ogólnych instrukcji odróżnić tą wiedzę, poza zasadą mówiącą o "niezbędnym kontekście, który wykracza poza specjalizację danego agenta".

Tymczasem kolejna sekcja dotyczy obszaru, który nie zawsze będzie niezbędny, lecz w tym przypadku pozostaje istotny: **ton wypowiedzi**. W związku z tym, że mówimy tu o agencie pełniącym rolę **prywatnego asystenta**, to dobrze jest ukształtować jego zachowanie tak, aby odbiegało od domyślnego stylu wypowiedzi modelu. Niestety LLM szybko zapominają o tych instrukcjach i bez przypomnień już po kilku wiadomościach wracają (przynajmniej na ten moment) do swojego oryginalnego tonu. Jednocześnie z tego powodu sekcja ta jest nieco bardziej rozbudowana. Widzimy więc w niej **przykłady wyrażeń**, **serie skojarzeń**, instrukcje **dostosowania tonu** do bieżącej sytuacji, a także antywzorce. Poza tym jest to także miejsce w którym pojawiają się przykłady **few-shot**, ponieważ uznałem, że sposób wypowiedzi jest na tyle uniwersalny, że nie będą miały one negatywnego wpływu na skuteczność agenta.

> Interaktywna wersja poniższych wizualizacji jest dostępna [tutaj](https://cloud.overment.com/prompt-voice-anatomy-1771179608.html).

![Anatomia sekcji Voice promptu agenta AI](https://cloud.overment.com/2026-02-15/ai_devs_4_voice-8607d4fe-6.png)

W przypadku tej sekcji można też pomyśleć nie tylko o prezentacji oczekiwanego stylu wypowiedzi, ale także zachowań związanych bezpośrednio z logiką. Przykład tego nie oddaje, ponieważ podjąłem decyzję o tym, aby jednak uniknąć mieszania odpowiedzialności. Jest to jednak warte rozważenia.

I ostatnia sekcja w tym przypadku dotyczy narzędzi, w tym także informacji na temat dostępnych agentów. Jej treść jest niemal w pełni wygenerowana, ponieważ „skład zespołu” może się zmieniać w zależności od sesji. Co więcej, wiemy już, że same opisy narzędzi i ich schematy opisują się same, więc nie ma potrzeby uwzględniania tu dodatkowych instrukcji. Wyjątek stanowi tylko wzmianka na temat możliwości sprawdzenia katalogu **templates/** zawierającego instrukcje pozostałych agentów, a także wzmianka o narzędziu **send\_notification**, która jest tu uwzględniona tylko po to, aby agent nie mylił powiadomienia z inną formą komunikacji.

Ostatecznie też po sekcji `<tools>` mamy także dynamiczną sekcję **WORKSPACE\_SECTION** do której trafiają treści związane z mechaniką "observational memory” z lekcji **S02E03**. Zaraz pod nią mamy także ostatnie zdanie, przypominające CTA (Call to Action), którego rola polega na jasnym zasygnalizowaniu zakończenia instrukcji systemowej.

> Bonus: W przykładzie 02\_04\_agent znajduje się prosty agent wyposażony w mechanikę Observational Memory, która umożliwia prowadzenie długiej interakcji z agentem. Na potrzeby przykładu znacznie obniżyłem progi tokenów, więc kompresja kontekstu ma miejsce już po kilku krótkich wiadomościach.
> Uruchomienie przykładu składa się z dwóch kroków:
>
> - w jednym oknie terminala należy uruchomić npm run lesson10:agent
> - w drugim oknie terminala należy uruchomić npm run lesson10:agent:demo
>   Wówczas w katalogu workspace/memory zaczną być tworzone “obserwacje” oraz “refleksje”. Observational Memory omawialiśmy już w S02E03, ale pomyślałem, ze dobrze będzie pokazać przykładową implementację w kodzie.

![Anatomia sekcji Tools promptu agenta AI](https://cloud.overment.com/2026-02-15/ai_devs_4_tools-04689358-3.png)

Sekcja `<tools>` mogłaby być zdecydowanie bardziej rozbudowana w sytuacji, gdybyśmy korzystali z mechaniki „progressive disclosure”, ponieważ narzędzia byłyby wtedy wczytywane dynamicznie, więc agent musiałby posiadać wiedzę o tym, jak może ich szukać.

Tymczasem doszliśmy do końca instrukcji systemowej głównego agenta. Dodam tylko, że kształtowanie promptów dla pozostałych agentów kieruje się niemal takimi samymi zasadami. Tym bardziej że subagent w niektórych systemach będzie miał też możliwość wzywania innych agentów. A nawet jeśli tak nie będzie, to nadal potrzebna będzie jakaś forma komunikacji z agentem nadrzędnym.

## Przypisywanie zestawu narzędzi oraz ustawień

Strategia przypisywania narzędzi do agentów nie jest jasno określona. Zwykle mówi się o tym, że 10-15 narzędzi przypisanych do jednego agenta to maksymalna liczba. Jednak praktyka sugeruje, że jest to zbyt duże uproszczenie. Niektóre usługi (np. Github) będą udostępniać znacznie więcej akcji niż integracje z mniej złożonymi serwisami. Z drugiej strony do pracy z Githubem (czyli znaną platformą, której API jest dobrze znane modelom) może wystarczyć nam **jedno narzędzie** w postaci dostępu do CLI. Jednak nawet wtedy może okazać się, że agent musi posiadać określoną wiedzę, aby robić to skutecznie w naszym imieniu.

Nie ma więc oczywistych reguł, które określają liczbę narzędzi agenta. Tym bardziej, że przykład Claude Code pokazuje, że sama możliwość interakcji z terminalem pozwala osiągnąć niezwykle dużo. Jednocześnie nie oznacza to, że dany agent będzie skutecznie posługiwał się nawet trzema narzędziami. Innym razem może pojawić się potrzeba, aby więcej niż jeden agent miał dostęp do tych samych integracji, ale korzystał z nich w inny sposób.

Możliwości modeli bez wątpienia się zwiększają. Techniki stopniowego odkrywania narzędzi, również dają nam mnóstwo elastyczności pod tym względem. Dobrze jest więc nie ograniczać się do "przyjętych standardów", lecz eksperymentować w celu odkrycia najlepszej konfiguracji dla nas.

Poniżej mamy przykład systemu w którym główny agent posiada dostęp do narzędzi umożliwiających komunikację z innymi agentami i użytkownikiem. Dodatkowo ma także dostęp do sieci i systemu plików. Pozostali agenci są wyspecjalizowani w obszarach takich jak **operacje, research, komunikacja email, rozrywka, design oraz nawigacja**. Wśród agentów niektórzy współdzielą wybrane narzędzia (np. web search), a inni mają ich znacznie więcej niż pozostali (aż 27!).

![Przykład podziału narzędzi pomiędzy agentami](https://cloud.overment.com/2026-02-15/ai_devs_4_assignment-3d1d49f7-e.png)

Przypisanie tych samych narzędzi do różnych agentów to sposób na zmniejszenie potrzeby wymiany informacji między agentami, przy jednoczesnym unikaniu ich przeciążania. Zdarzają się jednak sytuacje, gdy zaczyna to stanowić problem, ponieważ jeśli jeden agent ma dostęp do pamięci ograniczonej pod kątem uprawnień i nie znajdzie poszukiwanych informacji, może założyć, że ich po prostu nie ma.

Przy podejmowaniu takich decyzji podczas budowy agentów dobrze jest mieć z tyłu głowy myśl: **czy system, który buduję, stanie się lepszy wraz z rozwojem modeli?** Jeśli odpowiedź jest negatywna, to (przynajmniej na razie) oznacza, że możemy budować niewłaściwą rzecz. Jeśli nie mamy bardzo dobrego powodu, żeby robić to dalej, powinniśmy przemyśleć dalszą strategię.

Nie oznacza to także, że powinniśmy być nastawieni wyłącznie pozytywnie, do tego co (być może) nadejdzie. Ograniczenia i problemy, które dziś nas dotykają również są niezwykle ważne. Dlatego projektując system agentowy musimy wziąć pod uwagę ryzyka wynikające z **połączenia pomiędzy narzędziami**. Jeśli system samodzielnie jest w stanie przesłać informacje z jednego miejsca w drugie, to jest to ryzyko potencjalnych problemów. Wystarczy, że agent wyposażony w odpowiednio zabezpieczony system plików utworzy notatkę w Jira w sekcji, która nie jest objęta ograniczeniami.

Takie narzucanie ograniczeń na agentów niekiedy będą niezbędne, ale też szybko może okazać się, że tak bardzo zmniejszają użyteczność systemu, że całość traci sens. Dlatego coraz częściej widzimy systemy agentowe funkcjonujące w ramach sandboxów. Wówczas możemy pozwolić sobie na znacznie więcej przy odpowiednim balansowaniu ryzyka. Przykład **02\_05\_sandbox** prezentuje prostą implementację w której agent ma jednocześnie ogromną swobodę, a jednocześnie wyraźnie nakreślony zakres działania.

W przeciwieństwie do agentów, których widzieliśmy do tej pory, ten na początku ma dostęp jedynie do **pojedynczych narzędzi**, takich jak: **list\_servers**, **list\_tools**, **get\_tool\_schema** i **execute\_code**. Pozostałe narzędzia są odkrywane dynamicznie, więc początkowo nie zajmują przestrzeni w oknie kontekstowym.

Po uruchomieniu przykładu, agent otrzymuje prośbę o dopisanie zakupów do listy i orientuje się, że nie ma narzędzi, które mu to umożliwią. Decyduje się więc sprawdzić dostępne serwery MCP, a następnie wyświetla ich narzędzia oraz schematy. Na ich podstawie **pisze kod TypeScript i uruchamia go w piaskownicy!**

![Przykład działania agenta funkcjonującego w piaskownicy z opcją wykonywania kodu](https://cloud.overment.com/2026-02-15/ai_devs_4_sandbox-28b2ebd4-4.png)

Takie generowanie kodu ma bardzo dużo zalet, ponieważ agent może elastycznie łączyć ze sobą narzędzia i operować nawet na ogromnych ilościach danych, które w tej sytuacji nie muszą trafiać do kontekstu agenta, bo funkcjonują wyłącznie jako zmienne reprezentowane w kodzie. Oczywiście czasem może pojawić się potrzeba, aby agent musiał zapoznać się z ich treścią, ale nadal mówimy tu o istotnym usprawnieniu.

Poziom zabezpieczeń również jest tu relatywnie wysoki, ponieważ agent może być ograniczony pod kątem kontaktu ze światem zewnętrznym czy miejsc w które przesyła informacje. Nie oznacza to jednak, że sandbox rozwiązuje wszystkie nasze problemy, bo po części stwarza nam szereg nowych, związanych ze wzrostem złożoności architektury i związanej z nią kosztów.

## Przypisywanie wiedzy oraz kontekstu

Podobnie jak w przypadku narzędzi trudno jest wskazać sztywne reguły, które wpływają na przepływ wiedzy między agentami lub na sposoby organizacji pamięci długoterminowej. Tym bardziej że w praktyce mówimy o różnych kategoriach danych, pojawiających się na różnych etapach interakcji. Poza tym widzieliśmy, jak dokumenty mogą stanowić fundament komunikacji, ponieważ agenci mogą wymieniać się referencjami, wstrzykiwać dynamiczne placeholdery, a nawet generować kod, który może odwoływać się do plików bez wczytywania ich treści do kontekstu. Ostatecznie pojawia się tu także wątek pamięci długoterminowej, której rola wcale nie musi ograniczać się do wiedzy agenta, bo równie dobrze może nią być dynamiczna baza wiedzy firmowej lub nawet treść personalnego bloga.

Mamy więc tutaj:

- **Dokumentach sesji:** czyli załącznikach przesłanych przez użytkownika oraz plikach utworzonych przez agentów w trakcie danej sesji. Do tych danych mają dostęp wszyscy agenci zaangażowani w bieżącą interakcję i nie są one globalnie dostępne.
- **Wiedza publiczna:** to rodzaj pamięci długoterminowej, która może być współdzielona pomiędzy agentami **oraz użytkownikami** systemu.
- **Wiedza prywatna:** to przestrzeń na dane użytkownika, jego kontekst, zasoby wiedzy, a nawet dokumenty opisujące sposób realizacji powiązanych z nim procesów.
- **Wiedza agentów:** obejmuje wszystkie informacje dotyczące bezpośrednio konkretnych agentów, ich sposobu zachowania czy instrukcji obsługi narzędzi oraz zasad komunikacji. Agenci mogą też przechowywać tutaj swoje wspomnienia, wnioski i obserwacje.
- **Pamięć podręczna:** dotyczy tymczasowych informacji, które mogą być współdzielone pomiędzy sesjami, albo dotyczą wyłącznie chwilowych danych wygenerowanych w ramach sandboxów. Mówimy więc tutaj o treści **wyników wyszukiwania** czy **treści stron www**.
- **Runtime:** czyli baza danych, która może być warstwą **niewidoczną dla agentów**, ale stanowiąca podstawę ich funkcjonowania w kontekście sesji, interakcji czy harmonogramu zadań.

Przykład takiej organizacji informacji może wyglądać tak, jak prezentuje poniższy schemat.

![Przykład architektury informacji agentów](https://cloud.overment.com/2026-02-22/ai_devs_4_data_flow-b4393680-c.png)

W związku z tym, że mamy tu do czynienia z **wieloma** obszarami wiedzy i tym samym **złożonymi zasadami** zarządzania nią. Część tych reguł jest zapisana w kodzie, ponieważ załączniki czy generowane dokumenty zawsze trafiają do ustalonych z góry struktur. Natomiast wiedza **publiczna, prywatna** oraz pamięć **agentów** muszą być określane na podstawie treści, co nie zawsze jest takie oczywiste. Przykładowo:

- Informacja o nowym projekcie może być **prywatna** bądź **publiczna**.
- Instrukcja wykonania zadania może być **prywatna**, **publiczna** bądź dotyczyć **agenta**
- Informacja o profilu danej osoby również może wystąpić w każdym obszarze, a nawet niekiedy w więcej niż jednym z nich!

Trudno więc oczekiwać, że agent będzie poprawnie organizował informacje, skoro proces decyzyjny jest tak dynamiczny. Co więcej, sam wybór kategorii to nie wszystko, ponieważ w jej obrębie również trzeba wybrać konkretną lokalizację, a nierzadko także **połączyć je** z istniejącymi już treściami. Jest więc tu wiele pytań, na które bardzo trudno odpowiedzieć, szczególnie jeśli system ma funkcjonować autonomicznie z minimalnym zaangażowaniem po stronie człowieka. Tym bardziej, że zapisanie informacji to tylko jeden etap, ponieważ agenci muszą także wiedzieć, jak się nimi posługiwać podczas wykonywania zadań.

Praktyczne doświadczenie sugeruje tutaj, że jak zwykle warto trzymać się możliwie **prostych zasad** i utrzymywać struktury tak proste, jak to możliwe. Niekiedy można zadać sobie pytanie, czy zaawansowane pamięć długoterminowa rzeczywiście jest nam potrzebna i czy nie wystarczą proste dokumenty, których utrzymanie będzie niezwykle łatwe. Poza tym, na przestrzeni kolejnych tygodni zobaczymy jeszcze wiele przykładów organizacji zewnętrznych informacji, co pomoże później w podejmowaniu decyzji o tym, które z podejść sprawdzą się najlepiej w przypadku rozwiązań które przyjdzie nam budować na co dzień.

## Fabuła

![https://vimeo.com/1171928484](https://vimeo.com/1171928484)

## Transkrypcja filmu z Fabułą

> Numerze piąty!
>
> Jeśli nie zaczniemy działać, to z naszej elektrowni zostanie tylko dziura w ziemi. Wiesz dobrze co planują operatorzy Systemu.
>
> Naszych ludzi możemy ewakuować - mamy na to jeszcze czas, ale po weekendzie nie będzie już do czego wracać. Elektrowni nie będzie, zasilania nie będzie, skoku w czasie nie będzie... i niczego nie będzie.
>
> Ale powiem Ci, że jeszcze nie wszystko stracone i może... hmmm... to dziwnie zabrzmi, ale może nawet dobrze się stało, że próbują nas zaatakować. Tylko ten atak musi odbyć się na naszych warunkach.
>
> Pamiętasz nasze problemy z systemem chłodzenia elektrowni? Jesteśmy pośrodku niczego. Gdy budowano tę elektrownię - jeszcze w latach 80 - wybrano to miejsce ze względu na pobliskie Jezioro Żarnowieckie. To ono miało być źródłem wody do chłodzenia reaktora.
>
> Tylko teraz zamiast jeziora mamy bardziej sadzawkę, bo poziom wody spadł o dobre 80%. To jednak nie jest główny problem. Realnym problemem jest tama, która odgradza nas od tych resztek wody. Musimy się jej pozbyć.
>
> Nie dysponujemy ładunkami wybuchowymi. Nie dysponujemy także dronami. Ale... czy ktoś aby nie planował nas zbombardować?
>
> Plan jest szalony - zupełnie jakby skok w czasie w celu ratowania świata nie brzmiał jak coś szalonego - ale nie mamy innego wyjścia jak tylko spróbować.
>
> Bombardowanie zaplanowane jest na poniedziałek. To jednak my wykonamy pierwszy ruch. Zdobyłem dla Ciebie dostęp do systemu sterowania dronami. Przejmiesz kontrolę nad jednym z nich. Twoim zadaniem jest... nas zbombardować. Tak, dobrze usłyszałeś - mówiłem, że to trochę szalone.
>
> Wyślesz uzbrojonego drona w naszym kierunku, ale nie zrzucisz ładunku wybuchowego na elektrownię - wycelujesz go wprost na pobliską tamę. W systemie zaznaczysz, że jest to lot, którego celem jest zniszczenie elektrowni.
>
> Będzie lot na mniej więcej poprawne koordynaty, będzie bomba, będzie wybuch, udokumentujemy to odpowiednio, a automatyczny system odznaczy zadanie jako wykonane. Budynek zostanie wymazany z map Systemu jako zniszczony i o to nam właśnie chodzi.
>
> To nie sprawi, że będziemy już bezpieczni, ale da nam wystarczająco dużo czasu, aby zająć się innymi problemami.

## Zadanie

Wiemy już co planuje zrobić Dział Bezpieczeństwa Systemu. Chcą zrównać z ziemią elektrownię w Żarnowcu. Mamy jednak sposób, aby pokrzyżować im te plany. Bombardowanie naszej tymczasowej bazy, zaplanowane jest na nadchodzący tydzień, jednak my wykonamy ruch wyprzedzający. Pamiętasz, że ostatnio mieliśmy problemy z chłodzeniem rdzeni? No to załatwmy sobie chłodzenie z pobliskiego jeziora.

Przejęliśmy kontrolę nad uzbrojonym dronem wyposażonym w ładunek wybuchowy. Twoim zadaniem jest zaprogramować go tak, aby wyruszył z misją zbombardowania wymaganego obiektu, ale faktycznie bomba ma spaść nie na elektrownię, a na pobliską tamę. Jeśli wszystko pójdzie zgodnie z planem, powinniśmy skutecznie doprowadzić wodę do systemu chłodniczego. Jeśli się pomylisz, to przynajmniej problem z brakiem wody zastąpimy problemem z powodzią - nazwijmy to "zrównoważonym rozwojem" ;)

Kod identyfikacyjny elektrowni w Żarnowcu: **PWR6132PL**

**Nazwa zadania: `drone`**

#### Skąd wziąć dane?

Dokumentacja API drona (HTML):

```
https://hub.ag3nts.org/dane/drone.html
```

Mapa poglądowa terenu elektrowni:

```
https://hub.ag3nts.org/data/tutaj-twój-klucz/drone.png
```

Mapa jest podzielona siatką na sektory. Przy tamie celowo podbito intensywność koloru wody, żeby ułatwić jej lokalizację.

#### Jak komunikować się z hubem?

Instrukcje dla drona wysyłasz na endpoint `/verify`:

```json
{
  "apikey": "tutaj-twój-klucz",
  "task": "drone",
  "answer": {
    "instructions": ["instrukcja1", "instrukcja2", "..."]
  }
}
```

API zwraca komunikaty błędów jeśli coś jest nie tak - czytaj je uważnie i dostosowuj instrukcje. Gdy odpowiedź zawiera `{FLG:...}`, zadanie jest ukończone.

### Co należy zrobić w zadaniu?

1. **Przeanalizuj mapę wizualnie** - możesz do modelu wysłać URL pliku, nie musisz go pobierać - policz kolumny i wiersze siatki, zlokalizuj sektor z tamą.
2. **Zanotuj numer kolumny i wiersza** sektora z tamą w siatce (indeksowanie od 1).
3. **Przeczytaj dokumentację API drona** pod podanym URL-em.
4. **Na podstawie dokumentacji** zidentyfikuj wymagane instrukcje.
5. **Wyślij sekwencję instrukcji** do endpointu `/verify`.
6. **Przeczytaj odpowiedź** - jeśli API zwróci błąd, dostosuj instrukcje i wyślij ponownie.
7. Gdy w odpowiedzi pojawi się `{FLG:...}`, zadanie jest ukończone.

### Wskazówki

- **Analiza obrazu** - Do zlokalizowania tamy na mapie potrzebny jest model obsługujący obraz (vision). Zaplanuj dwuetapowe podejście: najpierw przeanalizuj mapę modelem vision, żeby zidentyfikować sektor tamy, potem użyj tej informacji w pętli agentowej z modelem tekstowym. `openai/gpt-4o` dobrze radzi sobie z dokładnym zliczaniem kolumn i wierszy siatki, natomiast niedawno wypuszczony model `openai/gpt-5.4` jest w tym jeszcze lepszy. Warto go wypróbować. Właściwe zlokalizowanie sektora mapy jest kluczowe.
- **Dokumentacja pełna pułapek** - Dokumentacja drona celowo zawiera wiele kolidujących ze sobą nazw funkcji, które zachowują się różnie w zależności od podanych parametrów. Nie musisz używać wszystkich - skup się na tym, co faktycznie potrzebne do wykonania misji. Oszczędzaj tokeny i konfiguruj tylko to, co konieczne.
- **Podejście reaktywne** - Nie musisz rozgryźć całej dokumentacji przed pierwszą próbą. API zwraca precyzyjne komunikaty błędów - możesz wysłać swoją najlepszą próbę i korygować na podstawie feedbacku. Iteracyjne dopasowywanie jest tu naturalną strategią.
- **Reset** - Jeśli mocno namieszasz w konfiguracji drona, dokumentacja zawiera funkcję `hardReset`. Przydatna gdy kolejne błędy wynikają z nawarstwionych wcześniejszych pomyłek.
