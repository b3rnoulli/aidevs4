---
title: S02E04 — Organizowanie kontekstu dla wielu wątków
space_id: 2476415
status: scheduled
published_at: '2026-03-19T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/library-1773304299.png'
circle_post_id: 30573311
---
» [Lekka wersja przeglądarkowa](https://cloud.overment.com/s02e04-organizowanie-kontekstu-dla-wielu-watkow-1773309057.html) oraz [markdown](https://cloud.overment.com/s02e04-organizowanie-kontekstu-dla-wielu-watkow-1773309028.md) «

Interakcje sięgające poza pojedynczą sesję to kolejny etap rozwoju systemów agentowych. Do tej pory widzieliśmy przykłady zarządzania kontekstem oraz kompresowania go, co pozwalało na wydłużenie trwania bieżącej sesji, nawet pomimo limitów okna kontekstu. Wśród przykładów pojawiały się także zadania wykonywane przez więcej niż jednego agenta, ale bez potrzeby bezpośredniej komunikacji między nimi.

Teraz przyjrzymy się bliżej technikom projektowania systemów wieloagentowych, które wiążą się z koniecznością zarządzania kontekstem wykraczającym poza pojedynczą sesję. Otwiera to przed nami zupełnie nowe możliwości w zakresie organizowania narzędzi, zarządzania kontekstem oraz realizacji wieloetapowych zadań. Jednocześnie stawia przed nami szereg nowych wyzwań związanych z komunikacją pomiędzy agentami oraz autonomiczną koordynacją ich pracy.

## Koncepcja wielowątkowej interakcji z modelem językowym

Wielowątkowe interakcje z zwykle kojarzą się z prowadzeniem wielu indywidualnych sesji. Narzędzia takie jak ChatGPT dodatkowo wzmacniają te skojarzenia ze względu na historię rozmów. Natomiast w kontekście systemów agentowych mówimy o różnych konfiguracjach, które kształtują sposób komunikacji oraz wzajemne zależności. Warto podkreślić, że architektury, o których tu mowa, są z nami od lat. Po prostu dziś możemy stosować je w połączeniu z modelami językowymi, co znacząco zwiększa ich elastyczność.

Mamy więc do dyspozycji przede wszystkim:

- **Pipeline:** to sekwencja w której kolejni agenci przekazują rezultaty swojej pracy, bez możliwości powrotu do wcześniejszych etapów.
- **Blackboard:** opiera się o wspólny stan dostępny dla niezależnych agentów. Ten przykład widzieliśmy w lekcji S02E03 przy okazji agentów "Researcher'ów" gromadzących dane z różnych źródeł
- **Orchestrator:** polega na zarządzaniu pracy agentów z pomocą głównego agenta-koordynatora, który zleca zadania, kontroluje przepływ informacji oraz kontaktuje się z człowiekiem. To podejście stosowane jest aktualnie w na przykład w Claude Code.
- **Tree:** to rozbudowana wersja koordynatora, która uwzględnia także role managerów. Pozwala to na wykonywanie znacznie bardziej złożonych zadań, ale też zwiększa złożoność systemu.
- **Mesh i Swarm:** są dziś jeszcze rzadziej spotykane w produkcyjnych systemach agentowych wykorzystujących LLM, bo trudniej je kontrolować i debugować. W **mesh** komunikacja jest adresowana: agent zwykle wie, do kogo pisze (np. do „File Managera” od uploadu). Natomiast w **swarm** komunikacja jest bardziej rozproszona, ponieważ wiele agentów może podjąć działanie związane ze zleconym zadaniem, a wynik powstaje w wyniku selekcji bądź agregacji.

![Przykłady architektur systemów wieloagentowych](https://cloud.overment.com/2026-02-12/ai_devs_4_agentic_architectures-53bb1485-e.png)

Z praktycznego punktu widzenia będziemy skupiać się na stosowaniu pierwszych czterech architektur, nierzadko jednocześnie korzystając z więcej niż jednej. Nasze zadanie będzie polegało na zaimplementowaniu **mechanik**, dostarczeniu **narzędzi** oraz ustalenia głównych **zasad** systemu. Wszystkie te elementy już omawialiśmy, ale w kontekście jednej sesji i agenta.

Patrząc na to technicznie, komunikacja między agentami wymaga **zbudowania narzędzi** takich jak:

- **delegate:** zleca zadanie wybranemu agentowi
- **message:** umożliwia obustronną komunikację między agentami

Agent dysponujący takimi narzędziami może przekazać zadanie, lub jego część, innym agentom. Uruchomienie **delegate** otwiera nowy wątek przypisany do innego agenta. Pozwala to na **zmianę instrukcji systemowej** oraz zestawu dostępnych narzędzi. Agent po zakończeniu swojej pracy, po prostu odpowiada, co staje się tym samym **wynikiem działania narzędzia "delegate"** dla nadrzędnego agenta.

![Przykład delegowania zadań pomiędzy agentami](https://cloud.overment.com/2026-02-12/ai_devs_4_delegation-4c08dbfc-b.png)

Ukończenie zadania niekiedy będzie niemożliwe, na przykład z powodu niewystarczających informacji. Wówczas agent, który je realizuje, może skorzystać z narzędzia **message**, aby skontaktować się z nadrzędnym agentem. Jego pętla zostanie **wstrzymana** do czasu dostarczenia danych (swoją drogą to dobry scenariusz dla [generatorów](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/function*)).

Poniżej znajduje się przykład, w którym agent, poproszony o dodanie kuponu rabatowego do wybranych produktów, **prosi o doprecyzowanie** czasu trwania promocji. Informacja ta trafia do agenta nadrzędnego, który nie jest w stanie jej dostarczyć samodzielnie, więc kontaktuje się z użytkownikiem. Po dostarczeniu brakujących danych, agent korzysta z narzędzia **message**, co wznawia działanie agenta tworzącego kody rabatowe. Wynik jego pracy zostaje później przekazany użytkownikowi.

![Przykład dwukierunkowej komunikacji pomiędzy agentami](https://cloud.overment.com/2026-02-12/ai_devs_4_bidirectional_communication-e577cdbb-3.png)

Taka dwukierunkowa komunikacja może przybrać znacznie bardziej zaawansowaną formę, na przykład w przypadku zadań angażujących **wielu agentów**, których zadania mogą być od siebie **zależne**. Co więcej, zależności te mogą występować także w konfiguracji obejmującej konieczność **wysłania zdarzenia**, do więcej niż jednego agenta. To prowadzi nas do architektur opartych na zdarzeniach.

![Komunikacja w systemie wieloagentowym oparta o zdarzenia](https://cloud.overment.com/2026-02-12/ai_devs_4_events-c204c7bb-e.png)

Przenosząc to na praktyczny przykład, załóżmy, że mamy użytkownika pytającego o status zamówienia. W tym przypadku:

- **Użytkownik**: przesyła wiadomość trafiającą do systemu zdarzeń (**user.message**)
- **Intent Agent:** otrzymuje powiadomienie o nowej wiadomości i określa jej rodzaj w zdarzeniu **ticket.classified**
- **Tracker i Credit**: to serwisy reagujące na zdarzenie **ticket.classified**, które deterministycznie pobierają informacje na temat zamówienia (**tracking.found**) oraz przydzielają zniżkę za opóźnienie **credit.applied**
- **Draft Agent:** nasłuchuje na zdarzenia dotyczące zgłoszenia i zauważa, że do napisania szkicu odpowiedzi brakuje mu wiedzy na temat klienta (np. czy jest to stały klient). Wysyła więc zdarzenie **customer.lookup\_requested** i oczekuje na dostarczenie tych danych. W chwili gdy otrzyma komplet danych, pisze wiadomość dla klienta, **która zostaje przekazana do obsługi klienta** w celu **weryfikacji przez człowieka**.

![Przykład praktycznego zastosowania architektury wykorzystując zdarzenia](https://cloud.overment.com/2026-02-12/ai_devs_4_agentic_events-32ffb396-5.png)

Także projektowanie systemów wieloagentowych może znacznie wykraczać poza proste powiązania oraz podstawową komunikację. Co więcej, w ich tworzeniu i rozwoju niezwykle przydatni są agenci do kodowania, szczególnie w zakresie **wizualizacji**, na przykład z pomocą składni Mermaid (wystarczy poprosić np. Cursor o przedstawienie logiki w Mermaid) bądź w plikach HTML. Obecnie jednak warto czuwać nad decyzjami projektowymi, ponieważ modele często komplikują lub pomijają istotne wątki.

## Rola globalnego kontekstu i jego zawartość

W lekcji S02E01 rozmawialiśmy o kontekście współdzielonym między sesjami. W przypadku systemów wieloagentowych mówimy dokładnie o tym samym, choć jego treść kształtuje nie tylko zachowanie konkretnego agenta, ale także **sposób interakcji między nimi**. Istotną różnicą jest tutaj również fakt, że **agenci mogą pracować na tych samych treściach jednocześnie**. Trudność polega na tym, aby odpowiednio tym zarządzić.

Zacznijmy od tego, że problemy dotyczące globalnego kontekstu (np. pamięci czy bazy wiedzy) mogą ujawnić się już nawet w przypadku "jednego" agenta. Powodem jest fakt, że **ten sam agent, może być uruchomiony wielokrotnie** i działać równolegle. Taka sytuacja sprawia, że zaczynamy mówić o systemie **wieloagentowym**, ale opartym o jednym "szablonie" agenta. Może więc tu dojść do sytuacji, że dwa różne zapytania skierowane w tym samym czasie doprowadzą do **utraty informacji**.

Poniżej mamy przykład interakcji z jednym agentem, ale działającym w dwóch instancjach. Agent otrzymuje informacje, które prowadzą do aktualizacji jednej z notatek pamięci długoterminowej. W efekcie jedna z informacji zostaje utracona, ponieważ **agent B** zapisał plik później niż **agent A**.

![Przykład konfliktu w zapisie wspomnień przez wielu agentów](https://cloud.overment.com/2026-02-12/ai_devs_4_context_conflict-7cba7e3a-a.png)

Problem konfliktów pomiędzy różnymi wersjami dokumentów jest nam w programowaniu doskonale znany. Równie znane jest nam rozwiązanie w postaci systemów kontroli wersji, które w takich sytuacjach wymagają od nas podjęcia decyzji o tym, w jaki sposób zmiany powinny być zastosowane.

Choć mogłoby się wydawać, że to samo rozwiązanie możemy wprost przenieść na systemy wieloagentowe, tak praktyka sugeruje coś innego. Bo w przypadku rozwiązywania konfliktów, osoba która to robi **posiada informację** o tym, które zmiany powinny zostać zapisane oraz w jaki sposób. Choć agent ma szansę poradzić sobie w takiej sytuacji, tak nierzadko będzie mu **brakować informacji**, aby to zrobić.

Mamy więc tutaj kilka opcji:

- **Wykrywanie konfliktów**: agenci zwykle najpierw czytają treść, którą chcą zmodyfikować. Jeśli pomiędzy odczytem a zapisem doszło do modyfikacji, możemy wykryć to przez sprawdzenie sum kontrolnych (eng. checksum) bądź nawet sum [hash'y obliczanych dla każdej z linii](https://x.com/_can1357/status/2021828033640911196)
- **Unikanie konfliktów:** części konfliktów można uniknąć już na poziomie założeń określających przynależność zasobów, poziom uprawnień (tylko do odczytu) czy ich izolację, na przykład na poziomie sesji.
- **Agent zarządzający:** agent zarządzający wybranymi obszarami zewnętrznego kontekstu (na przykład pamięcią) może posiadać dodatkowe uprawnienia wglądu w historię interakcji, czy posiadać możliwość kontaktu z człowiekiem.
- **Historia zmian:** jak widzieliśmy na przykładzie Observational Memory, niektóre rodzaje informacji mogą być przechowywane z zachowaniem pełnej historii zmian. Wówczas rzadziej dochodzi do bezpośrednich konfliktów, a agent widzi, jak dane zmieniały się w czasie.
- **Zmiany manualne:** podobnie jak w przypadku Git, wszędzie tam, gdzie automatyczne rozwiązania nie wystarczą, w proces rozwiązywania konfliktów może być zaangażowany człowiek.

![Strategie zarządzania globalnym kontekstem agentów](https://cloud.overment.com/2026-02-13/ai_devs_4_managing_context-1e26a7d6-7.png)

Podobnie jak w przypadku agenta dysponującego zewnętrzną wiedzą, którą może wykorzystywać przy realizowaniu zadań, tutaj również kontekst ten wpływ na zachowanie agentów oraz interakcji pomiędzy nimi. Może to sugerować, że dokumenty powinny mówić wprost **co agenci mają robić oraz kiedy**, natomiast to zadanie należy do systemu. Zewnętrzny kontekst nie powinien być z nim zbyt mocno powiązany.

Poniżej widzimy przykład kilku kategorii danych w **zewnętrznym kontekście**, z których w różnych konfiguracjach mogą korzystać agenci, oczywiście ze ścisłym zakresem uprawnień (na poziomie agenta oraz użytkownika z którym trwa bieżąca sesja). Nie ma tu jednak bezpośredniego połączenia z agentami.

![Przykład współdzielenia pamięci pomiędzy agentami](https://cloud.overment.com/2026-02-13/ai_devs_4_shared_knowledge-cf27fdb9-3.png)

Odseparowanie zewnętrznego kontekstu od logiki agentów jest ważne także z perspektywy zarządzania nim. Choć powyższy schemat sugeruje, że odpowiada za to agent **Memory Manager**, tak wskazane jest, aby dokumenty były dostępne także dla ludzi. Chodzi tu zarówno o utrzymanie odpowiednich struktur, ale też otworzenie na faktyczną **kolaborację** pomiędzy ludźmi, a agentami.

## Współdzielenie kontekstu

Myśląc o systemach wieloagentowych zintegrowanych na przykład z firmową bazą wiedzy czy prywatnym projektem "second brain", szybko przychodzą do głowy wizje pełnej autonomii. Równie szybko okazuje się, że zdanie mówiące o tym, że **Gen-AI potrafi więcej niż myślimy i mniej niż nam się wydaje** jest bardzo prawdziwe, bo wraz ze złożonością logiki (którą trudno prześledzić i zrozumieć jak kod) szybko pojawiają się pytania bez jasnych odpowiedzi oraz mnóstwo frustracji. Całkowicie też rozjeżdża się wizja projektu z widocznymi rezultatami.

Choć możemy tworzyć kolejne schematy i coraz bardziej skomplikowane powiązania między nimi, warto jednocześnie wrócić myślami do sytuacji, w których modele popełniają proste błędy, przez co albo nie docierają do potrzebnych informacji, albo z jakiegoś powodu je ignorują. Poza tym dynamiczny charakter środowiska, w którym działają agenci, w połączeniu z wieloznacznością języka naturalnego wcale nie pomaga.

Dlatego przejdziemy teraz przez potencjalne wyzwania oraz obszary, na które warto zwrócić uwagę przy organizacji kontekstu oraz zasad posługiwania się nim zarówno przez agentów, jak i ludzi.

1. **Sesja vs. Pamięć:** różnica między nimi wydaje się oczywista - informacje z sesji są tymczasowe, a z pamięci długoterminowe. Jednak jest to zbyt duże uproszczenie, ponieważ w sesji pojawiają się treści, które muszą zostać utrwalone i ktoś musi o tym decydować. W przypadku czatbotów, jest to relatywnie proste, bo system może reagować na polecenia użytkownika bądź samodzielnie sugerować potrzebę zapisania wspomnień. Jednak agenci często działający w tle potrzebują tutaj więcej autonomii, zgeneralizowanych założeń balansowanych z wytycznymi weryfikowanymi na poziomie kodu (na przykład dostępu do katalogów).
2. **Degradacja komunikacji:** przekazywanie informacji pomiędzy agentami wiąże się z utratą lub zniekształceniem danych. Problem ten szybko narasta wraz ze złożonością sesji oraz samego zadania. Dlatego instrukcje narzędzi związane z **delegowaniem** oraz **wymianą wiadomości** powinny być starannie opracowane, a system powinien zakładać, że agent może otrzymać jedynie częściowe informacje, co może wymagać dodatkowej weryfikacji.
3. **Własna interpretacja:** nawet jeśli agent otrzyma komplet potrzebnych informacji, to nadal może zinterpretować je na swój sposób. Ryzyko to jest zdecydowanie mniejsze w przypadku dość oczywistych zadań (np. "zaktualizuj dane klienta X") i większe w przypadku tych otwartych (np. "znajdź wszystkie informacje na temat klienta X").
4. **Kontekst informacji:** gdy już dochodzi do trwałego zapisywania danych, bardzo łatwo zgubić kontekst, który może być jasny w treści konwersacji, ale zmienić się w niezależnej notatce. Na przykład notatka na temat osoby o imieniu „Anna” może zostać pomylona podczas rozmowy na temat kogoś innego o tym samym imieniu.
5. **Duplikowanie informacji:** nawet przy dobrej architekturze informacji może dojść do sytuacji w której wiedza na ten sam temat znajdzie się w więcej niż jednym miejscu. Jest to problem, którego raczej trudno uniknąć, ale można na niego reagować. Obecnie nawet mniejsze (i tańsze) modele mogą skanować dane modyfikowane w danym okresie czasu i wykrywać potencjalne duplikaty. Widzieliśmy to już przy okazji przykładu z bazami grafowymi.
6. **Metadane:** w klasycznych aplikacjach każda zapisana informacja, poza treścią, może zawierać metadane opisujące źródło pochodzenia, datę utworzenia lub inne detale przydatne na potrzeby interfejsu użytkownika albo późniejszych analiz. W przypadku agentów metadane mogą być wykorzystane **podczas komunikacji** pomiędzy agentami, jak i z użytkownikiem. Nawet proste pytanie "o czym rozmawialiśmy podczas drogi do Warszawy" pokazuje jak istotne mogą być wzbogacone informacje.

Powyższe zasady w pewnym stopniu mogą wydawać się oczywiste i nawet średnio odkrywcze gdy już o nich wiemy. Wyzwanie z nimi związane ujawnia się jednak w praktyce - czasem na etapie projektowania systemu, a znacznie częściej w chwili, gdy zaczyna funkcjonować na produkcji.

Najlepszą sugestią, jaką można dać na tym etapie, jest **zaprojektowanie systemu tak prostego, jak to możliwe** oraz utrzymywanie go w takiej formie przez jak najdłuższy czas. Systemy wieloagentowe nie muszą od razu przejmować kontroli nad całą organizacją ani dążyć do zastępowania całych działów. Jednocześnie jeden system może obsługiwać wiele niezależnych obszarów, przy bardzo ograniczonej wymianie informacji pomiędzy agentami.

## Podział obowiązków i narzędzi pomiędzy agentami

Możliwości i wyzwania związane z zarządzaniem kontekstem w systemach wieloagentowych najlepiej widać na konkretnych przykładach. Jeszcze lepiej, gdy zaczniemy z nich korzystać, ponieważ trudno pokazać wszystkie problemy związane z działaniem tego systemu, a tym bardziej wyrobić sobie intuicję czy określić zasady.

Przyjrzyjmy się więc agentom, których celem będzie stworzenie tzw. Daily Ops, czyli aktualizacji zbudowanej na podstawie informacji pochodzących z wielu źródeł. Dane mogą więc pochodzić z zewnętrznych systemów (maili, kalendarzy, list zadań czy osobistych notatek), ale same aktualizacje nie mogą się powtarzać na przestrzeni dni bądź pominięte aktywności muszą zwiększyć swój priorytet.

Zbudowanie **Daily Ops** będzie wymagać:

- Zadania CRON, które raz dziennie wyśle powiadomienie **w imieniu użytkownika** z prośbą o przygotowanie Daily Ops dla bieżącego dnia **na podstawie instrukcji** zawartej w pliku **daily-ops.md** (bądź dowolnym, innym miejscu)
- Przeczytania instrukcji przez agenta **koordynującego** pracę innych agentów. Jego zadaniem jest rozdzielenie zadań, które w tym przypadku będą bardzo precyzyjne i proste do osiągnięcia (bo chodzi wyłącznie o pobranie statusów)
- Zestawienia otrzymanych odpowiedzi z **historią z ostatnich dni**, **celami długoterminowymi** czy **wpisami z pamięci** oraz **wygenerowania dokumentu** na dany dzień według ustalonego szablonu.
- (opcjonalnie) przesłania dokumentu na e-mail użytkownika bądź SMS.

Całość na poziomie koncepcyjnym prezentuje się następująco:

![Schemat działania systemu wieloagentowego nad zadaniem Daily Ops](https://cloud.overment.com/2026-02-13/ai_devs_4_ops_agent-4ca77029-6.png)

Bardzo uproszczona wersja implementacji takiego systemu znajduje się w przykładzie **02\_04\_ops**, w której mamy **szablony agentów** posiadających dostęp do narzędzi (które dla uproszczenia zwracają statyczne dane z plików). Natomiast samo generowanie Daily Ops odbywa się już w wyniku współpracy agentów.

Poniżej znajduje się schemat opracowany na podstawie logów jednego z uruchomień, obejmujący:

1. Przesłanie do głównego agenta treści zadania.
2. Odczytanie przez niego wskazanego pliku workflow
3. Zlecenie zadań wszystkim agentom (mogą działać równolegle)
4. Odczytanie najnowszej historii, notatki z celami i preferencjami
5. Przygotowanie końcowego dokumentu

![Przykład przygotowania notatki Daily Ops przez system agentowy](https://cloud.overment.com/2026-02-13/ai_devs_4_ops_execution-15b2bf7e-4.png)

Jest to więc zachowanie w pełni zgodne z naszymi początkowymi założeniami. Od razu można zauważyć, że etap analizowania preferencji/historii/celu jest dość obszerny, więc jest to dobry kandydat do dalszych uproszczeń ale nie będziemy się na nich skupiać.

Patrząc na tę logikę z programistycznego punktu widzenia, można zapytać: **po co tu agenci?** Jest to uzasadnione, ponieważ podobne narzędzia widzieliśmy na długo przed popularyzacją modeli językowych. Tam jednak mówiliśmy o deterministycznej logice i raczej sztywnych zasadach prezentacji treści. Tutaj mamy znacznie większą dowolność, elastyczność i personalizację, ale **nie odpowiada to na nasze pytanie**.

Decyzja o tym, czy zastosowanie agentów ma sens, czy może wystarczy prosty workflow, albo całkowita rezygnacja z LLM, jest warta rozważenia **w każdym przypadku**. Dobrze jest wziąć tu pod uwagę kwestie takie, jak:

- **Zadania otwarte:** nawet jeśli proces ma jasny cel, a nawet listę aktywności potrzebnych do jego realizacji, ale w trakcie może pojawić się potrzeba reagowania na dane z otoczenia, to logika agentów będzie uzasadniona.
- **Dynamiczne dane:** jeśli struktura danych (input/output) nie jest z góry określona bądź informacje wymagają transformacji wykraczających poza możliwości kodu, to również zasadne jest skorzystanie z agentów.
- **Dynamiczne zależności:** jeśli pomiędzy danymi występują zależności, które trudno wykryć na poziomie kodu (występują na poziomie języka i znaczenia), to logika agentów jest prawdopodobnie jedynym wyjściem.
- **Iterowanie:** choć iteracje w kodzie są możliwe, tak jeśli zależą od kryteriów zapisanych językiem naturalnym oraz wymagają iterowania obejmującego kroki niemożliwe do zdefiniowania z góry, to logika agentów jest zasadna.
- **Elastyczna architektura:** gdy opracowanie **Daily Ops** może obejmować nowe obszary i potrzebna jest wysoka elastyczność głównej logiki, to ponownie wybór agentów będzie uzasadniony.
- **Dopasowanie wyniku:** jeśli sposób personalizacji rezultatu wykracza poza szablony, które można uzupełnić programistycznie, to agenci bądź przynajmniej LLM będą potrzebni.

Jednak wszędzie tam, gdzie pojawiają się wymagania obecnie niemożliwe do zaadresowania z pomocą LLM (np. "zerowe" koszty, szybki czas reakcji, pełna przewidywalność), to pozostanie przy klasycznej implementacji w kodzie będzie jedyną opcją.

Umiejętność odnalezienia balansu pomiędzy logiką agentów, prostszymi workflow w których pojawia się LLM bądź logice zapisanej w kodzie, jest jedną z kluczowych umiejętności. Projektowanie agentów może być początkowo atrakcyjne (zarówno z technicznej jak i biznesowej perspektywy), ale warto zachować rozsądek. Tym bardziej, że budowanie agentów nadal obecnie posiada mnóstwo wad.

## Koordynacja pracy agentów przez managerów

Obecnie systemy wieloagentowe posiadają agenta bądź agentów odpowiedzialnych za zarządzanie pracą pozostałych. Ich rola zwykle polega na rozbijaniu zadań na mniejsze etapy, kształtowaniu i monitorowaniu planu realizacji oraz zarządzaniu komunikacją. Posiadają więc minimalną ilość narzędzi, ale jednocześnie relatywnie szerokie uprawnienia dostępu do informacji. Poza tym, odpowiadają za kontakt z użytkownikiem.

Podstawowy obraz agenta zarządzającego pozostałymi widzieliśmy przed chwilą w przykładzie **Daily Ops**, jednak jego rola obejmuje elementy, którym warto się przyjrzeć.

- **Wiedza o systemie:** agent zarządzający posiada wiedzę na temat systemu w którym funkcjonuje. Obejmuje to dane użytkownika, szeroki dostęp do pamięci długoterminowej oraz większe uprawnienia dostępu do informacji z bieżącej sesji. Agent ten zna także role dostępnych agentów oraz zakres ich odpowiedzialności.
- **Dostęp do informacji:** agent ma możliwość wglądu nie tylko w rezultaty pracy agentów, ale także przestrzeń roboczą. Posiada także dostęp do niemal całej pamięci długoterminowej przynajmniej w trybie "tylko do odczytu".
- **Dostęp do narzędzi:** są to narzędzia **delegate/message** oraz zwykle **recall/search\_memory** do przeszukiwania pamięci. Jego rola i tak jest duża, więc warto unikać przeciążania go dodatkowymi narzędziami.
- **Delegowanie zadań:** w trakcie trwania sesji główny wątek, kluczowe informacje, plan działania oraz postępy są dostępne w kontekście agenta zarządzającego.
- **Transport wiedzy:** zdarzają się sytuacje w których inni agenci zlecają zadania agentowi zarządzającemu. Zwykle ma to formę próśb o dodatkowe informacje bądź przekazanie rezultatów ich pracy do innych agentów.
- **Decyzyjność:** w sytuacji gdy dany agent spotyka problem, potrzebuje potwierdzenia bądź decyzji, to na pierwszej linii stoi agent zarządzający. Musi więc posiadać jasne wytyczne dotyczące jego uprawnień oraz tego, kiedy ma skontaktować się z użytkownikiem.
- **Weryfikacja:** agent zarządzający weryfikuje także efekty wykonanego zadania. Powinien więc posiadać wytyczne dotyczące sposobu oceny, bądź mieć możliwość delegowania tego procesu do innego agenta.

Widzimy zatem, że nawet mimo minimalnej liczby narzędzi rola agenta zarządzającego będzie kluczowa dla działania całego systemu. Przy obecnym rozwoju modeli językowych konieczne jest ograniczanie jego roli, ale z umiarem, ponieważ każdy etap komunikacji dodatkowo komplikuje proces zarządzania kontekstem.

Działanie systemu agentowego raczej nie jest perfekcyjne i obecnie nie mówimy jeszcze o pełnej autonomii. Co więcej, nie wszystkie błędy w działaniu systemu będą zauważalne od razu, ponieważ część z nich może polegać na różnego rodzaju pomyłkach. Musimy też przygotować się na sytuacje, w których na przykład **brak dostępu do informacji** bądź **brak decyzji** nie spowoduje zatrzymania działania systemu, lecz doprowadzi do wykonania zadania z pominięciem wybranych etapów.

W rezultacie projektowanie systemów wieloagentowych funkcjonujących w otoczeniu ludzi, oraz współpracujących z nimi, coraz częściej obejmuje tworzenie paneli zarządzania. Pozwalają one na monitorowanie bieżących aktywności systemu, dostarczania informacji czy rozwiązywania problemów. Obecnie jeszcze trudno powiedzieć jak wiele dzieli nas od pełnej autonomii (w niektórych przypadkach już ją zaczynamy osiągać), dlatego poza projektowaniem logiki agentów, duża część naszej uwagi musi być skierowana w stronę ludzi. I to nadal człowiek pełni rolę kluczowego koordynatora systemu agentowego.

Przykład interfejsów, o których można już teraz pomyśleć, widoczny jest poniżej. Oczywiście jego elementy i struktura mogą być całkowicie inne, dopasowane do danego systemu i potrzeb użytkownika. I nie musi to wcale oznaczać, że każdy z nas staje się teraz managerem, ale że przynajmniej część naszej pracy będzie wymagać interakcji z panelem takim jak ten poniżej.

![Przykładowy dashboard zarządzania systemem wieloagentowym](https://cloud.overment.com/2026-02-13/ai_devs_4_dashboard-b6e59c3e-3.png)

Widzimy tutaj **ogólne statystyki systemu**, **trwające sesje**, **harmonogram zadań** oraz **obszary wymagające uwagi**. Agenci sprawiają, że pojedyncze okno czatu, które znamy z ChatGPT czy Cursor, nie jest już wystarczające.

Na ten moment to tyle. Do szczegółów związanych z projektowaniem takich interfejsów przejdziemy w kolejnych lekcjach. Tymczasem warto zastanowić się, jak systemy agentowe mogą wpłynąć na naszą codzienność, wewnątrzfirmowe narzędzia oraz produkty i rozwiązania, które oferujemy klientom.

## Fabuła

![https://vimeo.com/1171929842](https://vimeo.com/1171929842)

## Transkrypcja filmu z Fabułą

> OK... Czyli głównie chodziło o systemy chłodzenia i firmware. Poradzimy sobie z tym, ale teraz ten temat musimy zostawić na później. Pojawił się inny problem. Od zawsze współpracowaliśmy z ruchem oporu. To oni dostarczali nam informacje, korzystaliśmy z pracy ich rąk, gdy trzeba było wykonać jakąś fizyczną akcję, a w zamian dzieliliśmy się z nimi tym, co sami wiemy. Można powiedzieć, że jesteśmy w całkiem dobrych relacjach. To znaczy: byliśmy. To skomplikowane. Mamy swojego człowieka w ruchu oporu i doniósł nam on, co się tam w środku dzieje. Nastąpiło pewne rozbicie. Nie wiem, w które informacje możemy wierzyć, a które to zwykłe plotki, ale nie brzmi to dobrze. Ruch oporu co do zasady NIE WSPÓŁPRACUJE Z SYSTEMEM - to ważne! Ale gdy już współpracuje, to znaczy, że musi mieć ważny powód... Wygląda na to, że przedstawiciele ruchu zdecydowali się nawiązać współpracę z operatorami Systemu. Może "współpraca" to za duże słowo. Ponoc wysłali pewien donos. Jak się domyślasz, sprawa dotyczy nas. Znaczy mnie, Ciebie, elektrowni i całego zespołu, który tam teraz jest. Obawiam się, że nasz plan jest zagrożony, a może i zagrożone jest życie ludzi, którzy znajdują się tam na miejscu. Członkowie ruchu wiedzą, że System potrzebuje elektryczności, aby kontrolować ludzkość. Krok po kroku sabotują elektrownie, aby tej energii niezbędnej do życia Systemu było coraz mniej, a tymczasem my... uruchamiamy elektrownię. Według ruchu działamy na niekorzyść ludzkości. Podejrzewają nawet, że być może zbrataliśmy się z Zygfrydem. Oczywiście zdania są podzielone i spora część członków ruchu oporu jest po naszej stronie, ale jednak nie wszyscy i to powoduje rozbicie w ich strukturach. Informator przekazał nam dostęp do skrzynki mailowej jednego z operatorów Systemu. Znajdź tam proszę maile od Wiktora z ruchu oporu. To jeden z tych, którzy się wyłamali i zdecydowali na współpracę z Systemem. Wysłał wiadomość z jakiejś anonimowej skrzynki. Dowiedz się, co planują w związku z naszą elektrownią. Jest szansa, że Wiktor nie ograniczy się tylko do jednego maila i nadal będzie informował operatorów o naszych działaniach.

## Zadanie

Zdobyliśmy dostęp do skrzynki mailowej jednego z operatorów systemu. Wiemy, że na tę skrzynkę wpadł mail od Wiktora - nie znamy jego nazwiska, ale wiemy, że doniósł na nas. Musimy przeszukać skrzynkę przez API i wyciągnąć trzy informacje:

- **date** - kiedy (format `YYYY-MM-DD`) dział bezpieczeństwa planuje atak na naszą elektrownię
- **password** - hasło do systemu pracowniczego, które prawdopodobnie nadal znajduje się na tej skrzynce
- **confirmation\_code** - kod potwierdzenia z ticketa wysłanego przez dział bezpieczeństwa (format: SEC- + 32 znaki = 36 znaków łącznie)

Skrzynka jest cały czas w użyciu - w trakcie pracy mogą na nią wpływać nowe wiadomości. Musisz to uwzględnić.

Co wiemy na start:

- Wiktor wysłał maila z domeny `proton.me`
- API działa jak wyszukiwarka Gmail - obsługuje operatory `from:`, `to:`, `subject:`, `OR`, `AND`

**Nazwa zadania: `mailbox`**

#### Jak komunikować się z API?

Skrzynka mailowa dostępna jest przez API zmail:

```
POST https://hub.ag3nts.org/api/zmail
Content-Type: application/json
```

Sprawdzenie dostępnych akcji:

```json
{
  "apikey": "tutaj-twój-klucz",
  "action": "help",
  "page": 1
}
```

Pobranie zawartości inboxa:

```json
{
  "apikey": "tutaj-twój-klucz",
  "action": "getInbox",
  "page": 1
}
```

#### Jak wysłać odpowiedź?

Wysyłasz do `/verify`:

```json
{
  "apikey": "tutaj-twój-klucz",
  "task": "mailbox",
  "answer": {
    "password": "znalezione-hasło",
    "date": "2026-02-28",
    "confirmation_code": "SEC-tu-wpisz-kod"
  }
}
```

Gdy wszystkie trzy wartości będą poprawne, hub zwróci flagę `{FLG:...}`.

### Co należy zrobić w zadaniu?

1. **Wywołaj akcję `help`** na API zmail, żeby poznać wszystkie dostępne akcje i parametry.
2. **Spraw aby agent korzystał z wyszukiwarki maili** - na podstawie opisu zadania może zbudować odpowiednie zapytania.
3. **Pobierz pełną treść** znalezionych wiadomości, żeby przeczytać ich zawartość.
4. **Szukaj informacji po kolei** - nie musisz znaleźć wszystkich na raz.
5. **Korzystaj z feedbacku huba**, żeby wiedzieć, których wartości jeszcze brakuje lub które są błędne.
6. **Kontynuuj przeszukiwanie skrzynki**, aż zbierzesz wszystkie trzy wartości i hub zwróci flagę.
7. **Pamiętaj, że skrzynka jest aktywna** - jeśli szukasz czegoś i nie możesz znaleźć, spróbuj ponownie, bo nowe wiadomości mogły dopiero wpłynąć.

### Wskazówki

- **Podejście agentowe z Function Calling** - to zadanie doskonale nadaje się do pętli agentowej z narzędziami. Agent może mieć do dyspozycji: wyszukiwanie maili, pobieranie treści wiadomości po ID, wysyłanie odpowiedzi do huba i narzędzie do zakończenia pracy. Pętla powinna działać iteracyjnie - szukaj, czytaj, wyciągaj wnioski, szukaj dalej. Można też podejść bardziej ogólnie i pozwolić agentowi po prostu na wywołania API z parametrami które sam ustali na podstawie pomocy.
- **Dwuetapowe pobieranie danych** - API zmail działa w dwóch krokach: najpierw wyszukujesz i dostajesz listę maili z metadanymi (bez treści), a dopiero potem pobierasz pełną treść wybranych wiadomości po ich identyfikatorach. Nie próbuj odgadywać treści na podstawie samego tematu - zawsze pobieraj pełną wiadomość przed wyciąganiem wniosków.
- **Aktywna skrzynka** - skrzynka jest cały czas w użyciu i nowe wiadomości mogą wpływać w trakcie Twojej pracy. Jeśli przeszukałeś całą skrzynkę i nie możesz czegoś znaleźć, warto spróbować ponownie - szukana informacja mogła właśnie dotrzeć. Nie zakładaj od razu, że informacja nie istnieje.
- **Wybór modelu** - do tego zadania wystarczy tańszy model jak `google/gemini-3-flash-preview`. Zadanie polega na przeszukiwaniu i ekstrakcji faktów, nie na złożonym rozumowaniu. Droższy model (`anthropic/claude-sonnet-4-6`) nie da tutaj istotnej przewagi, a pętla agentowa może wykonać kilkanaście zapytań do LLM.
- **Operatory wyszukiwania** - API obsługuje składnię podobną do Gmail. Możesz łączyć operatory. Możesz zacząć od szerokich zapytań, żeby nie przegapić istotnych maili, a potem zawęzić wyszukiwanie.
