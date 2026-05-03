---
title: Techniki łączenia modelu z narzędziami
space_id: 2476415
status: scheduled
published_at: '2026-03-10T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/hero-connecting-devices-1772881989.png'
circle_post_id: 30408290
---
![https://vimeo.com/1171062996](https://vimeo.com/1171062996)

Wiemy już, że możemy programistycznie sterować zachowaniem modelu, a generowane treści mogą być strukturyzowane i wykorzystane w logice aplikacji. Proces ten może zostać w pewnym sensie odwrócony, a model może "przejąć kontrolę" nad logiką aplikacji. W tym celu wykorzystamy wspomniany już **Function Calling**.

Zanim zaczniemy, mam jeszcze komentarz do osób będących w poprzednich edycjach AI\_devs, gdzie wprost z Function Calling raczej nie korzystaliśmy. Powodem zmiany podejścia jest rozwój modeli oraz usunięcie lub zmniejszenie ograniczeń API. Obecnie Function Calling bez przeszkód może stanowić element logiki w którym pojawia się LLM.

To tyle, zaczynajmy!

## Zasady łączenia modelu językowego z narzędziami

Narzędzia takie jak ChatGPT, Claude czy Cursor na co dzień nam pokazują, że LLM może pracować z systemem plików, przeszukiwać Internet czy posługiwać się różnymi narzędziami. Jednak z technicznego punktu widzenia **model językowy nie ma możliwości wchodzić w interakcję z otoczeniem** i może jedynie generować treści, zwykle w formie tekstu.

Widzieliśmy jednak, że LLM potrafią generować obiekty JSON na podstawie swojej wiedzy bazowej lub dostarczonych przez nas informacji. Sam format JSON znamy z codziennej pracy, na przykład dzięki wykorzystaniu API, które pozwalają na pobieranie danych oraz wykonywanie różnych operacji w zewnętrznych i wewnętrznych serwisach. Istnieje więc przynajmniej kilka cech wspólnych pomiędzy integracją z API a możliwością generowania strukturyzowanych danych przez model, które możemy wykorzystać.

Schemat łączenia LLM z narzędziami (Function Calling / Tool Use) wygląda następująco:

![Schemat Function Calling / Tool Use](https://cloud.overment.com/2026-01-21/ai_devs_4_function_calling-e9d7ae64-f.png)

Minimalny przykład prezentujący to, jak agent posługuje się narzędziami znajduje się w katalogu **01\_02\_tools**. Po jego uruchomieniu, bardzo prosty "agent" odpowie na pytanie o pogodę w Krakowie.

LLM fizycznie nie ma zapisanych informacji na temat aktualnej pogody w Krakowie. Pomimo tego Function Calling pozwolił modelowi na pozyskanie tych informacji przez dostępne narzędzia. Konkretnie:

1. Użytkownik zapytał o pogodę w Krakowie
2. Model otrzymał zapytanie oraz **schematy trzech narzędzi**: "get\_weather", "search\_web" oraz "send\_email"
3. Zamiast natychmiast odpowiedzieć użytkownikowi model zwrócił obiekt JSON z **nazwą narzędzia** oraz **argumenty** potrzebne do jego uruchomienia.
4. Następnie **kod aplikacji** wykorzystał wygenerowane dane, aby **uruchomić funkcję** pobierającą informacje z API pogodowego.
5. Zarówno **informacja o uruchomieniu narzędzia** oraz **informacje pogodowe, które zostały zwrócone**, trafiły do kontekstu konwersacji.
6. Następnie model został wywołany **ponownie**, lecz tym razem ze względu na dostęp do potrzebnych informacji, podjął decyzję o **zwróceniu finalnej odpowiedzi** dla użytkownika.

Spójrzmy na tę interakcję raz jeszcze, ale teraz z bardziej technicznej perspektywy. Jej najważniejsze punkty to:

- Definicje **wszystkich narzędzi** są dołączone do **każdego** zapytania i to nawet wtedy, jeśli nie zostaną uruchomione. Ma to negatywny wpływ na skuteczność działania modelu oraz zużycie kontekstu.
- Definicje narzędzi obejmujące **nazwę, opis, schemat oraz callback**. Callback to funkcja, która zostaje uruchomiona w chwili gdy model zwróci nazwę narzędzia oraz argumenty.
- Interakcja składa się **nie z jednego, lecz dwóch zapytań do LLM**. Zwykle taki kod uruchomiony jest w pętli, która zwykle trwa tak długo aż model zwróci finalną odpowiedź bądź gdy wyczerpie limit dostępnych kroków.
- W historii konwersacji zostają zapisane **wszystkie narzędzia oraz zwrócone przez nie dane**. Oznacza to, że wpływają one na zużycie kontekstu oraz koszty.

![](https://cloud.overment.com/2026-01-21/ai_devs_4_function_calling-ef4b5aa4-e.png)

Zobaczmy teraz jak Function Calling działa w praktyce poprzez przykład [01\_02\_tool\_use](https://github.com/i-am-alice/4th-devs/tree/main/01_02_tool_use). Logika w nim zawarta umożliwia modelowi interakcję z systemem plików ale tylko i wyłącznie we wskazanym katalogu (co jest ograniczone programistycznie).

Do interakcji z systemem plików przygotowałem zestaw podstawowych narzędzi działających w uproszczonej formie. Mamy zatem możliwość **przeglądania katalogów, wyświetlania plików, zapisywania i usuwania treści, tworzenia katalogów oraz pobierania informacji o plikach**. Pozwala to na kompletną, choć bardzo ograniczoną interakcję z lokalnymi plikami. Wystarcza to jednak, aby model poprawnie realizował polecenia zapisane w języku naturalnym.

Poniższy schemat pokazuje także, że w sytuacji, gdy model celowo lub w wyniku halucynacji spróbuje utworzyć plik w katalogu, do którego nie ma dostępu, aplikacja nadal będzie działać, a model otrzyma jasną informację o błędzie. Pozwala to na podjęcie działań polegających albo na skorzystaniu z narzędzia w inny sposób, albo na poinformowaniu użytkownika o braku uprawnień.

![Ogólna struktura i przykłady narzędzi do interakcji z systemem plików](https://cloud.overment.com/2026-01-21/ai_devs_4_filesystem_overview-5d0a8bea-2.png)

W lekcji **S01E01** mówiliśmy o tym, że na potrzeby **Structured Outputs** schemat odpowiedzi przesyłany jest wraz z zapytaniem i trafia do modelu razem z instrukcją systemową oraz pozostałym kontekstem konwersacji. W przypadku **Function Calling** jest podobnie.

Raz jeszcze spójrzmy na wizualizację procesu budowy kontekstu zapytania, ponieważ istotne jest zrozumienie tego **czym są narzędzia dla LLM** oraz **skąd model "wie" jak się nimi posługiwać** oraz wykorzystywać zwracane przez informacje.

W tym miejscu dobrze jest wrócić do narzędzia [Tiktokenizer](https://tiktokenizer.vercel.app/) i przypomnieć sobie jak **wiadomość systemowa, wiadomości użytkownika oraz asystenta** trafiają do modelu w formie **tokenów**. W przypadku Function Calling jest tak samo i zwyczajnie mamy dodatkowy blok z listą definicji narzędzi. Model "widzi" więc ich nazwy, opisy oraz schematy. Te informacje wykorzystywane są w chwili gdy zapytanie użytkownika zaczyna sugerować konieczność skorzystania z danego narzędzia. Wówczas API zwraca żądanie wykonania funkcji.

![](https://cloud.overment.com/2026-01-21/ai_devs_4_assembly-50a6ebc7-8.png)

Wiedza o tym, w jaki sposób model "widzi" narzędzia, powinna już teraz jasno sugerować, jak ogromną rolę odgrywają ich precyzyjne nazwy, opisy oraz powiązane z nimi schematy. Poza tym równie kluczową rolę pełnią odpowiedzi narzędzi oraz ich forma. Zarówno poprawne wywołanie narzędzia, jak i to zakończone błędem powinny jasno informować model o tym, co się wydarzyło oraz jakie kroki można podjąć.

## Function Calling oraz natywne oraz własne narzędzia

Przeszukiwanie sieci, deep research, odpowiadanie pytań na podstawie treści PDF czy uruchamianie kodu przez AI to narzędzia, które są na tyle uniwersalne, że większość providerów zdecydowała się udostępnić je natywnie. W lekcji **S01E01** nawet korzystaliśmy z narzędzia Web Search wbudowanego w API OpenAI w ramach przykładu [01\_01\_grounding](https://github.com/i-am-alice/4th-devs/tree/main/01_01_grounding).

Natywne narzędzia są bardzo wygodne, bo zwykle wymagają jedynie zmiany ustawień obiektu żądania przy zapytaniu do LLM. Jednak w związku z tym, że związana z nimi logika znajduje się na serwerze danego providera, to jako developerzy mamy ograniczone możliwości ich konfiguracji. Może się więc okazać, że zamiast korzystać z natywnych narzędzi, będziemy chcieli zbudować własne. Ale też nie ma problemu z tym, aby korzystać **równocześnie** z natywnych i własnych narzędzi.

Poniżej widzimy scenariusz w którym użytkownik prosi o przeszukanie sieci i zapisanie rezultatów w pliku. Model korzysta więc w pierwszej kolejności z natywnego narzędzia `web_search`, a następnie z zewnętrznego `file_write`.

![Połączenie natywnych i zewnętrznych narzędzi w LLM API](https://cloud.overment.com/2026-01-21/ai_devs_4_native_external_tools-801a06be-7.png)

Ostatecznie to czy korzystamy z natywnych narzędzi, czy nie, zależy głównie od naszych preferencji oraz potrzeb. Warto jednak wiedzieć, że istnieje taka możliwość, ponieważ realnie ułatwia to budowanie o ile oddanie części kontroli nad konfiguracją narzędzi jest dla nas w porządku.

## Dobre praktyki opisywania schematów i ich właściwości

Podłączenie narzędzi do LLM na ten moment nie stanowi żadnego wyzwania, bo sprowadza się do dodatkowej właściwości obiektu zapytania. Trudność leży projektowaniu narzędzi w taki sposób, aby model skutecznie się nimi posługiwał. Poza tym, będzie nam zależało na zachowaniu balansu pomiędzy możliwościami, a poziomem uprawnień.

Największym błędem jaki popełniają programiści przy projektowaniu narzędzi, jest **mapowanie istniejącego API 1:1**. Błąd ten polega na tym, że API projektowane jest z myślą o **programistach** oraz **deterministycznym kodzie**. W dodatku programiści którzy z niego korzystają, posiadają łatwy dostęp do **dokumentacji**.

Poniżej mamy przykład różnic pomiędzy narzędziami dla LLM do interakcji z aplikacją [Linear](https://linear.app/) porównanych z natywnymi funkcjonalnościami API. Akcje takie jak `delete_project` nie zostały zaimplementowane ponieważ zwykle nie będziemy dawać możliwości usuwania całych projektów agentowi. Akcje takie jak `add_label` nie zostały uwzględnione ponieważ byłyby wykorzystywane ekstremalnie rzadko. Ich pominięcie redukuje niepotrzebny "szum" w kontekście, co przekłada się na wyższą skuteczność działania LLM. Zatem jeśli niektóre akcje podejmowane są rzadko i możemy wykonać je samodzielnie w aplikacji, to nie ma potrzeby budować z nich narzędzi dla modelu.

![Przykład niebezpośredniego mapowania narzędzi LLM na podstawie API](https://cloud.overment.com/2026-01-22/ai_devs_4_mapping-66b46896-e.png)

Wybór które elementy API mają być dostępne jako narzędzia dla LLM to nie jedyna decyzja jaką musimy podjąć. Niekiedy uzasadnione będzie **połączenie** bądź **rozdzielenie** akcji dostępnych w API. Skoro jesteśmy już przy Linear, to aplikacja ta posiada różne **statusy, etykiety, zespoły oraz podział na projekty**. Przy zarządzaniu wpisami zwykle potrzebujemy identyfikatorów dla tych poszczególnych elementów. Problem w tym, że API udostępnia je jako oddzielne zasoby, co z programistycznego punktu nie jest problemem, ale z perspektywy AI przekłada się na dodatkowe, zbędne kroki. Dlatego zamiast udostępniać kilka narzędzi, możemy zamknąć je w jedno, np. `workspace_metadata`.

![Przykład połączenia wielu zasobów API w jedno narzędzie](https://cloud.overment.com/2026-01-22/ai_devs_4_unified_tools-0da2d4fc-d.png)

Narzędzie `workspace_metadata` nie jest jednak wyłącznie **połączeniem** kilku różnych zasobów API. Jest **konfigurowalnym połączeniem**, ponieważ model może zdecydować o tym, jakich informacji potrzebuje w danym momencie bez konieczności pobierania całego zestawu danych.

Wyłaniają nam się teraz zasady, którymi powinniśmy kierować się przy budowaniu narzędzi. Reguły te mówią, że:

- Narzędzia powinny być zrozumiałe dla osoby, która nie posiada jakiejkolwiek wiedzy na temat naszego systemu ani dostępu do aktualnej dokumentacji.
- Nazwa narzędzia powinna być możliwie unikatowa i mieć niską szansę na kolizję z innymi narzędziami. Np. „send” jest gorszą nazwą niż „send\_email”.
- Opisy narzędzi powinny charakteryzować się wysokim wskaźnikiem signal-to-noise. Powinny być zwięzłe i zawierać wyłącznie informacje, które zwiększają szansę na to, że model wybierze je w odpowiednim momencie. Choć brzmi to dość ogólnie, staje się to jasne w chwili, gdy przeanalizujemy od 10 do 30 przykładowych zapytań użytkownika.
- Narzędzia powinny być zaprojektowane tak, aby zminimalizować liczbę kroków potrzebnych do wykonania zadania.
- Schematy narzędzi nie muszą obejmować wszystkich możliwych właściwości dostępnych w API. Część z nich może zostać całkowicie pominięta, ponieważ nie odgrywają roli z punktu widzenia modelu. Przykładem są wszelkiego rodzaju hashe, wewnętrzne identyfikatory lub flagi wykorzystywane jedynie w kodzie aplikacji.
- Przy projektowaniu schematów zawsze warto zadać sobie pytania takie jak: "**co model bezwzględnie musi uzupełnić?**", "**co powinno być uzupełnione programistycznie?**" oraz "**czego model nie może uzupełnić?**". Np. model nie powinien mieć prawa do zmiany identyfikatora użytkownika, od którego zależą uprawnienia dostępu do zasobu. Coś takiego bezwzględnie musi być kontrolowane po stronie kodu.
- Odpowiedzi zwracane przez narzędzia powinny zawierać minimum niezbędnych informacji oraz wskazówki, które zwiększą szansę na to, że model poprawnie z nich skorzysta.
- Walidacja, paginacja, obsługa błędów oraz komunikaty o błędach muszą stać na najwyższym poziomie. Co więcej, jest to standard wyższy niż ten wymagany od aplikacji, które tworzymy na co dzień. W przypadku agentów posługujących się narzędziami możemy bowiem spodziewać się niemal dowolnych danych. Musimy zatem nie tylko zabezpieczyć się przed taką sytuacją, ale również poprawnie ją obsłużyć, aby model LLM wiedział, jak się w niej odnaleźć.

Poniższa grafika przedstawia konkretne przykłady opisanych zasad. Niebawem będziemy stosować je także w praktyce, więc szybko staną się dość naturalne i łatwiej będzie je zrozumieć.

![](https://cloud.overment.com/2026-01-22/ai_devs_4_mapping-1a8e7f3c-1.png)

## Ustalanie domyślnych wartości, walidacji oraz zabezpieczeń

Dobrze zaprojektowane narzędzia dla LLM dążą do tego, aby AI realizowało zadania w jak najmniejszej liczbie kroków przy minimalnym wysiłku. Nawet pomimo tego, że kolejne generacje modeli stają się coraz lepsze w posługiwaniu narzędziami, to i tak ciągle podnosimy poziom trudności rzucając im coraz trudniejsze wyzwania. Już teraz weszliśmy też w fazę w której agenci samodzielnie tworzą dla siebie nowe umiejętności. W tej sytuacji również będzie nam zależało na tym, aby generowane narzędzia były możliwie jak najbardziej skuteczne.

Ustalanie domyślnych wartości nie jest czymś nowym w kontekście API. Chociażby [Responses API](https://platform.openai.com/docs/api-reference/responses/create) ustawia właściwość `temperature` na 1, więc nie musimy zawsze jej podawać. Z narzędziami dla LLM jest podobnie, ale zdecydowanie bardziej złożone. Bo jeśli API ustala domyślną wartość, która nam nie odpowiada, możemy ją łatwo zmienić w kodzie i mieć pewność, że zawsze otrzymamy wynik w takiej formie, na której nam zależy. W przypadku LLM nie mamy takiej pewności, więc domyślne wartości powinny być starannie przemyślane.

Kilka przykładów:

- Podczas dostępu wymagającego uwierzytelnienia, przy założeniu, że użytkownik jest już autoryzowany, nie powinniśmy wymagać od modelu podawania identyfikatora. Np. przy tworzeniu nowego zadania w Linear, możemy domyślnie przypisać je do bieżącego użytkownika. Jednocześnie powinniśmy **poinformować model o tym fakcie w opisie narzędzia** oraz **dać możliwość zmiany** (jeśli jest to potrzebne). W podobny sposób można wczytać inne preferencje użytkownika (np. strefy czasowe)
- Domyślne ustawienia filtrowania, sortowania czy formatu wyświetlania powinny być ustawione tak, aby rezultaty były zwracane w formie zawierającej minimum niezbędnych informacji. Model powinien jednak mieć możliwość pobrania szczegółów w razie potrzeby.
- Wszędzie tam gdzie jest to możliwe, powinna istnieć możliwość ustawienia tej samej wartości na więcej niż jeden sposób. Np. Linear dopuszcza, aby przy dodawaniu nowego wpisu etykieta była podana w formie identyfikatora **bądź** nazwy. Oczywiście należy tutaj zwracać uwagę na ewentualne kolizje (nazwa w takiej sytuacji musi być unikatowa).
- Niektóre właściwości lub ustawienia API są dostępne wyłącznie dla użytkowników z określonymi planami subskrypcyjnymi, uprawnieniami lub zależą od preferencji danego konta. W sytuacjach, w których API mogłoby domyślnie zwrócić błąd, w odniesieniu do narzędzi zazwyczaj lepiej jest, o ile to możliwe, dopuścić niedostępne wartości. Należy jednak przy tym poinformować model, że poszczególne opcje nie zostały uwzględnione.

![](https://cloud.overment.com/2026-01-22/ai_devs_4_defaults-3e061598-b.png)

Także po raz kolejny robimy wszystko, co tylko możliwe, aby ułatwić korzystanie z narzędzia oraz wybaczać niektóre potknięcia. I jeśli już o nich mowa, to przyjrzymy się jeszcze walidacji oraz informacjom o błędach.

- Błędy takie jak "**coś poszło nie tak**" sprawiają duży problem nawet użytkownikom, ale dla modeli językowych oraz agentów AI zwykle oznaczają przekreśloną szansę na ukończenie zadania. Zatem dokładne informacje o błędach powinny stać się dla nas standardem.
- API niekiedy zwraca wyłącznie statusy błędów, np. `400 Bad Request`, albo `403 Forbidden`, których znaczenie jest wyjaśnione w dokumentacji. Wiemy już, że agenci AI zwykle nie będą mieć do niej dostępu, więc zawsze poza kodem, musimy dodać jasny opis błędu. Niekiedy przydatne są także wskazówki, np. "Zakres dat jest zbyt duży. Dostępna historia obejmuje maksymalnie (...zakres dat)".
- Błędy o brakujących właściwościach, np. "**team\_id jest wymagany**" mogą być uzupełnione wskazówką dla modelu. "**Identyfikator zespołu (team\_id) jest nieprawidłowy. Wskazówka: pobierz go z pomocą akcji 'workspace\_metadata', jeśli jest dostępna.**" zdecydowanie zwiększy skuteczność agenta. Dobrze jednak zachować pewną ostrożność, bo nie zawsze mamy pewność, że pozostałe narzędzia będą dostępne dla danego agenta.
- Podobnie jak w przypadku narzędzi CLI, które potrafią reagować na literówki bądź nieobsługiwane aliasy komend, tak samo w przypadku walidacji narzędzi niekiedy możemy domyślić się, że model może próbować ustawić np. status "done" zamiast "completed". Wówczas wskazówka w stylu "**czy chodziło Ci o ... ?**" może okazać się bezcenna.

Poniżej znajdują się przykłady prezentujące rekomendowane zasady walidacji z uwzględnieniem LLM. Na ich podstawie można tworzyć własne reguły i zwyczajnie zawsze zadawać sobie pytanie "jak mogę wyjaśnić błędne zapytanie tak, aby zwiększyć szansę na to, że agent AI będzie wiedział co zrobić".

![](https://cloud.overment.com/2026-01-23/ai_devs_4_validation-7a212262-e.png)

W kontekście walidacji, mogą pojawić się także sytuacje w których będziemy chcieli narzucić dodatkowe ograniczenia, ale tylko w sytuacji gdy to agent AI posługuje się naszym API. Przykładem mogą być akcje nieodwracalne, takie jak **wysłanie maila**. Domyślnie akcja ta może umożliwiać przesłanie wiadomości na dowolny adres. Jednak w przypadku modeli językowych może dojść do zwykłej halucynacji w wyniku której wiadomość może trafić w niepowołane ręce. Dobrym pomysłem jest więc **bezwzględne wymaganie potwierdzenia wykonania akcji** przez użytkownika. W przypadku gdy nie jest to możliwe, ale wciąż zależy nam na wysyłaniu maili, możemy wprowadzić programistyczne ograniczenie w postaci dopuszczalnej listy adresów. Takie podejście sprawdzi się szczególnie w kontekście firmowym bądź osobistym, ale tylko dla niektórych scenariuszy.

Analogicznie, gdy posiadamy informację, że z API korzysta agent, możemy stosować izolację kontekstu. Dzięki niej agent początkowo ma dostęp do różnych kategorii zasobów, lecz w ramach jednej sesji może korzystać wyłącznie z jednej z nich.

W praktyce, możemy także spotkać sytuacje gdzie niemożliwe będzie ani uzyskanie zgody od użytkownika, ani programistyczne ograniczenie dostępu. Wówczas możemy zbudować narzędzie posiadające wbudowany tryb **dry-run**. Pozwala on agentowi na sprawdzenie, czy wprowadzane zmiany są zgodne z założeniami. Jeśli tak, agent może wznowić wykonanie akcji z takimi samymi argumentami. Co prawda wówczas polegamy wyłącznie na ocenie modelu, ale w przypadku najnowszych LLM możemy spodziewać się znaczącego obniżenia ryzyka błędu (choć go nie eliminujemy).

![Przykłady dodatkowych zabezpieczeń akcji, uwzględnionych wyłącznie dla kontekstu AI](https://cloud.overment.com/2026-01-23/ai_devs_4_constraints-b55f9156-5.png)

## Połączenie modelu z usługami przez API, proxy oraz CLI

W sieci można spotkać opinie, a nawet projekty sugerujące, że bezpośrednie połączenie LLM z API to wszystko, czego potrzebują agenci. Myślę jednak, że powyższe przykłady jasno wskazują, iż automatyczne mapowanie istniejącego API do struktury narzędzi agentów nie jest dobrym pomysłem. Powodem w jednym zdaniu jest **brak wystarczającego kontekstu**, który nawet człowiekowi utrudnia bądź niekiedy uniemożliwia skorzystanie z API **bez dostępu do jego dokumentacji**.

Automatyzacja tłumaczenia API na schematy narzędzi dla AI jest teoretycznie możliwa poprzez zaangażowanie modeli LLM. Wówczas nie mówimy o bezpośrednim mapowaniu interfejsu, lecz o możliwości zastosowania zasad, o których wspominaliśmy przed chwilą. Niestety w praktyce, przynajmniej w przypadku obecnych modeli, trudno mówić o pełnej automatyzacji, a nadzór człowieka nadal pozostaje niezbędny. Zatem API może zostać dopasowane do LLM, ale w przypadku istniejących projektów może być to niezwykle trudne bądź wprost niemożliwe.

Gdy istniejące API jest poprawnie zaimplementowane (np. API Linear), możemy zbudować proxy, czyli warstwę stojącą pomiędzy API a LLM. Przykłady elementów takiego proxy widzieliśmy powyżej przy okazji omawiania różnic pomiędzy narzędziami LLM, a API Linear gdzie blokowaliśmy bądź łączyliśmy niektóre akcje. Także jeśli nie mamy możliwości wprowadzać znaczących zmian w istniejących interfejsach, stworzenie proxy jest bardzo wskazane. Rolę takiego proxy wprost odgrywają tzw. Serwery MCP (Model Context Protocol) o których będziemy jeszcze mówić.

Łączenie LLM z narzędziami możliwe jest także poprzez narzędzia CLI, np. [agent-browser](https://github.com/vercel-labs/agent-browser). Agent AI posiadający dostęp do terminala może wykonywać polecenia w zakresie swoich uprawnień. Dodatkowo wywołanie flagi --help zazwyczaj jest wystarczające, aby dowiedzieć się wszystkiego na temat danej akcji. Problem w tym, że zastosowanie narzędzi CLI na skali, poza urządzeniem użytkownika, jest dość trudne.

Oczywiście mamy wiele przykładów narzędzi CLI funkcjonujących w ramach naszych aplikacji. Np. ffmpeg, pandoc, wkhtmltopdv, magick i inne. Jednak jeśli nasz agent ma się łączyć z zewnętrznymi usługami takimi jak Google Maps, Stripe czy Pipedrive, które będą zarządzane z poziomu aplikacji działającej na serwerze, to budowanie CLI przyniesie nam więcej problemów niż korzyści.

Dlatego na pytanie **"Czy lepsze jest API, MCP czy CLI?"** odpowiedź będzie uzależniona od kontekstu i rodzaju integracji. Nie ma tutaj jednej ścieżki, ale warto znać zalety oraz wady każdego z tych podejść. Główne różnice znajdują się na poniższej grafice i obejmują:

- **API:** to scenariusz w którym model podłącza się bezpośrednio do danej usługi na przykład poprzez pisanie i uruchamianie poleceń CURL bądź prostych skryptów. Tutaj nie mamy praktycznie żadnej kontroli nad tym, co robi model. W dodatku agent potrzebuje tutaj dostęp do dokumentacji, którą musi samodzielnie eksplorować, co jest bardzo nieefektywne.
- **CLI:** to sytuacja gdy agent posiada dostęp do terminala i aplikacji CLI. W przeciwieństwie do API, niezbędne informacje może uzyskać poprzez flagę --help. W dodatku agent może korzystać z pełnej elastyczności terminala, co pozwala na przykład na łączenie ze sobą różnych akcji. W przeciwieństwie do API, agent porusza się tutaj wyłącznie po interfejsie, który został mu udostępniony.
- **Function Calling / MCP:** to "paczka" zawierająca zestaw narzędzi. Skorzystanie z nich **nie wymaga** dostępu do terminala, co zwiększa kontrolę nad zachowaniem agenta, ale jednocześnie ogranicza jego możliwości.

![](https://cloud.overment.com/2026-01-23/ai_devs_4_api_mcp_cli-ecf38a22-d.png)

Zaznaczę tylko, że **MCP** w podświetlonym bloku nie oznacza konieczności korzystania z Model Context Protocol. Równie dobrze mogą to być dedykowane narzędzia Function Calling wbudowane w logikę aplikacji. Poza tym, powyższe opcje nie są jedynymi, ponieważ do dyspozycji mamy jeszcze [**Code Execution**](https://www.anthropic.com/engineering/code-execution-with-mcp), ale o nim oraz o samym MCP powiemy sobie nieco później.

## Personalizacja narzędzi dzięki Augmented Function Calling

Sporo powiedzieliśmy na temat projektowania schematów "input / output" narzędzi. Można o tym myśleć jak o samodzielnym "pakiecie" zawierającym komplet informacji potrzebnych do korzystania z niego.

Gdy zaczniemy pracować z takimi narzędziami, szybko zauważymy potrzebę dostarczania dodatkowych instrukcji, które wyjaśnią agentowi AI to, **jak my chcemy**, aby z nich korzystał.

Załóżmy, że mamy narzędzie do **generowania i edycji obrazów** integrujące się z API Gemini. Agent AI może je uruchomić, aby stworzyć obraz zgodny z opisem użytkownika. Jednak gdy proces ten z jakiegoś powodu musi stać się powtarzalny, to każdorazowe dostarczanie pełnej instrukcji staje się uciążliwe. Wówczas dobrym pomysłem staje się **wzbogacenie promptu użytkownika** o wcześniej ustaloną treść. Można to określić mianem **Augmented Function Calling**.

Poniżej widzimy jak zapytanie "robot head" zostało zamienione na generyczną grafikę prezentującą głowę robota. Natomiast w drugim przypadku zapytanie użytkownika jest takie samo, lecz agent AI bierze pod uwagę dodatkową instrukcję opisującą pożądany styl. W rezultacie druga grafika jest szkicem pasującym do tego stylu.

![Przykład działania narzędzi bez kontekstu oraz ze spersonalizowanym kontekstem](https://cloud.overment.com/2026-01-23/ai_devs_4_augmented_tool_use-d76687f8-2.png)

Chodzi więc tutaj o **dodatkowe informacje w kontekście interakcji**, które wpływają na zachowanie modelu. Proces ten może mieć różne formy i zwykle występuje pod nazwami takimi jak **Commands**, **Skills** bądź po prostu **Prompts**. Na co dzień możemy je spotkać w narzędziach takich jak Open Code czy Cursor.

Te dodatkowe instrukcje mogą być dołączone do kontekstu na kilka sposobów:

- **Statycznie:** czyli przez bezpośrednie działanie użytkownika, np. uruchomienie komendy czy przyciski.
- **Dynamicznie:** czyli to model decyduje o uruchomieniu umiejętności. Odbywa się to na tej samej zasadzie, co w przypadku wszystkich narzędzi, czyli **nazwy** oraz **opisu**.
- **Hybrydowo:** czyli zarówno w wyniku bezpośredniej akcji użytkownika bądź decyzji agenta.

**Wzbogacanie wywołań narzędzi** może obejmować nie tylko pojedyncze uruchomienie akcji, lecz całą ich serię. Poza tym, agent może otrzymać możliwość nie tylko **aktywowania**, ale też **dezaktywowania** danej umiejętności, a także narzędzia do ich **tworzenia** czy **aktualizacji**.

## Zasady projektowania workflow oraz logiki agentów

Model językowy wyposażony w narzędzia może pracować zgodnie z narzuconym schematem i realizować kolejne etapy zadań jeden po drugim. Zwykle określa się to jako "Workflow". Pomimo raczej sztywnej struktury obecność modelu LLM sprawia, że taka logika może obsługiwać nawet skomplikowane procesy, a jednocześnie pozostawać relatywnie przewidywalna. Workflow może mieć różne formy, od prostego łańcucha akcji następujących po sobie, przez rozgałęzione scenariusze obejmujące nawet równoległe wykonanie akcji. Niezależnie od struktury, mówimy tutaj o z góry ustalonych komponentach, które mogą wziąć udział w wykonaniu zadania.

![Przykład AI Workflow - Chain](https://cloud.overment.com/2026-01-23/ai_devs_4_chain-1c59a279-a.png)

Gdy model językowy zostaje uruchomiony w pętli zapytań, w ramach której decyduje o kolejnych krokach, takich jak wywołania narzędzi czy kontakt z użytkownikiem, wówczas spełnia on definicję **agenta AI**. Agenci, w przeciwieństwie do zwykłych programów komputerowych, wyróżniają się tym, że są w stanie potencjalnie rozwiązywać problemy, z myślą o których nie musieli być bezpośrednio projektowani. Przykładowo agent wyposażony w narzędzia **filesystem**, **websearch** oraz **email** może gromadzić informacje z wybranych stron internetowych i zapisywać je w plikach. Nie będzie miał on również trudności z odczytaniem wiadomości e-mail oraz znalezieniem informacji na temat ich autorów czy firm, w których te osoby pracują. To właśnie ta elastyczność sprawia, że koncepcja agenta AI jest tak atrakcyjna i wzbudza zainteresowanie. Jednocześnie wiąże się ona z niepewnością dotyczącą powtarzalności oraz skuteczności realizowanych zadań.

![Przykładowa pętla logiki agenta](https://cloud.overment.com/2026-01-23/ai_devs_4_agent-d6370cf4-e.png)

Budowanie aplikacji w których logice pojawiają się modele generatywnej sztucznej inteligencji to nadal w ~80% te same aktywności, które znamy z klasycznych aplikacji. Jednak te 20% przedstawia zupełnie nową klasę problemów na których część nadal nie znamy odpowiedzi. Jednocześnie niektóre problemy agentów z którymi spotykaliśmy się jeszcze kilka miesięcy temu, dziś przestają być aktualne lub całkowicie znikają.

Pojawia się więc pytanie: **Jak budować logikę "workflow" oraz "agenta AI"?**

Spróbujemy teraz na nie odpowiedzieć, patrząc na ten temat z szerokiej perspektywy architektury. Mowa tutaj o:

- Logice aplikacji realizującej zapytania do LLM oraz zewnętrznych usług
- Modelu bądź modelach językowych sterujących logiką interakcji
- Narzędziach umożliwiających modelowi interakcję z otoczeniem
- Systemach pamięci krótkoterminowej oraz długoterminowej
- Zestawem instrukcji określających zachowanie modelu, a także umiejętnościom

Aktualnie mówi się także o **Agent Harness**, czyli nie tylko głównym komponentach samego agenta, ale całym systemie na który składają się także system plików, sandbox do wykonywania kodu, mechaniki zarządzania kontekstem, pamięcią, komunikacji pomiędzy agentami czy obserwacją całego systemu. Całość prezentuje się tak, jak poniżej.

![Agent Harness](https://cloud.overment.com/2026-01-23/ai_devs_4_agent_harness-0fed8955-3.png)

Niezależnie od tego czy budujemy Workflow czy Agentów, będziemy korzystać ze wszystkich bądź tylko wybranych komponentów. Jak wspomniałem, całość bardzo przypomina klasyczne aplikacje i tylko niewielka część wprost dotyczy AI. Natomiast kluczową różnicę stanowi fakt, że działaniem aplikacji w dużym stopniu zarządza model językowy. Sprawia to, że system musi być znacznie bardziej dopracowany, o czym zresztą przekonaliśmy się już przy okazji rozmów o narzędziach dla LLM.

Poza zrozumieniem architektury generatywnych aplikacji, dobrze jest też kształtować umiejętność oceny tego, kiedy wybrać Workflow, a kiedy Agenta AI. Tym bardziej, że w sieci często można spotkać opinie sugerujące, że tylko jedno z tych podejść jest użyteczne. Podczas gdy w praktyce, nierzadko okazuje się, że stosowanie jakiegokolwiek nie jest dobrym pomysłem.

- **100% skuteczności**: jeśli przewidywalność i stabilność jest fundamentalnie ważna, korzystanie z LLM jest **raczej złym pomysłem** o ile do gry nie wchodzi nadzór ze strony człowieka i/lub jasne wskaźniki sukcesu.
- **Struktura**: jeśli dany proces jest dokładnie ustrukturyzowany i rzadko się zmienia, to wówczas angażowanie logiki agenta mija się z celem. Skupienie się na poszczególnych etapach przyniesie więcej korzyści niż próby pełnej stabilizacji działań agenta.
- **Otwarte problemy:** choć tutaj na myśl od razu przychodzą agenci AI, tak nie powinniśmy skupiać się wyłącznie na nich. Niekiedy lepszym pomysłem jest zawężenie zakresu i zmiana otwartych problemów na kilka zamkniętych.
- **Reagowanie na zmiany:** dopiero w przypadkach gdy jasno widzimy przewagi elastyczności charakteryzującej agentów, powinniśmy całą uwagę skupić na zaprojektowaniu odpowiednich narzędzi oraz ich głównej logiki.

Choć z powyższych punktów wyłaniają się w miarę jasne schematy myślenia, tak dobrze jest je opanować po to, aby na pewnym etapie wprost je kwestionować. Bo może się okazać, że agent sprawdzi się lepiej w przypadku stabilnych i jasno zdefiniowanych procesów, ponieważ jego dynamiczne cechy wniosą dodatkową wartość, np. wynikającą z połączenia zewnętrznych źródeł danych.

W dalszych lekcjach AI\_devs będziemy zajmować się poszczególnymi obszarami powyższego schematu "Agent Harness".

## Refleksja oraz interpretacja zapytań w dynamicznym kontekście

Większość modeli językowych, które obecnie mamy do dyspozycji charakteryzuje tzw. reasoning polegający na generowaniu dodatkowych tokenów przed udzieleniem odpowiedzi bądź podjęciem działania. Niekiedy nawet używa się określenia Large Reasoning Model (LRM).

Etap rozumowania realnie wpływa na skuteczność modelu i tym samym logiki agentów, aczkolwiek niektórzy mają co do tego wątpliwości. "[Don’t Overthink it](https://arxiv.org/pdf/2505.17813)" sugeruje, reasoning negatywnie wpływa na proste zadania, a "[Premise Order Matters](https://arxiv.org/pdf/2402.08939)", że samo rozumowanie może być jedynie iluzją, ponieważ nawet zmiana kolejności informacji w prompcie potrafi obniżyć skuteczność modelu o nawet 40%.

W praktyce obserwujemy jednak realny wzrost skuteczności LLM, gdy tryb rozumowania jest włączony oraz ustawiony na wyższe wartości. Bo API zwykle pozwala nam kontrolować czas trwania refleksji, albo poprzez określenie budżetu tokenów bądź poziomu "wysiłku" włożonego w ten proces. Samo rozumowanie od strony technicznej różni się też w zależności od providera z którym aktualnie pracujemy. Przykładowo OpenAI udostępnia jedynie skróconą wersję "przemyśleń" modelu, a ich oryginalna treść jest automatycznie usuwana z kontekstu konwersacji.

![](https://cloud.overment.com/2026-01-24/ai_devs_4_reasoning-3619585a-c.png)

Choć automatyczne rozumowanie w LLM samo w sobie zwykle działa w imponujący sposób, tak w przypadku agentów AI będziemy angażować się w ten proces nieco bardziej, ale też nie będziemy chcieli sterować nim całkowicie, aby uniknąć narzucania niepotrzebnych ograniczeń. Przykładowo:

- **Planowanie:** wśród narzędzi dostępnych dla agenta możemy uwzględnić **listę zadań** i zachęcić LLM w instrukcji systemowej, aby przed rozpoczęciem pracy nad złożonym problemem, rozbił je na mniejsze kroki. Poza tworzeniem listy, agent powinien mieć możliwość jej aktualizowania. Lista zadań pełni istotną rolę szczególnie przy wieloetapowych interakcjach, ponieważ każdorazowe jej aktualizowanie "przypomina" modelowi o najważniejszych wątkach.
- **Odkrywanie:** wczytanie wszystkich możliwych informacji do kontekstu, na przykład z bazy wiedzy, nie jest obecnie możliwe. Stosujemy więc różne formy pamięci długoterminowej, opartej chociażby na systemie plików. Eksplorowanie zapisanych wspomnień wymaga posługiwania się narzędziami, co nie jest możliwe na samym etapie rozumowania. Co więcej, model może "nie wiedzieć, że coś wie", musimy więc poprowadzić go przez proces odkrywania posiadanych informacji.
- **Przekierowanie:** czasami będzie nam zależało na zarządzaniu uwagą agenta, czy to na podstawie klasyfikacji zapytania, czy poprzez deterministyczne informacje o jego bieżącym stanie. Jednym z przykładów jest sytuacja, w której agent otwiera przeglądarkę podczas wykonywania zadań. Stanowi to jasną informację, że jego aktualny kontekst powinien skupić się wyłącznie na jej obsłudze.
- **Uśrednianie**: nikt nie powiedział, że etap refleksji musi ograniczać się do jednego modelu. Zaangażowanie więcej niż jednego LLM jest porównywalne z uzyskaniem perspektywy od kilku różnych osób. Następnie połączenie rezultatów, na przykład poprzez ich uśrednienie bądź głosowanie, nierzadko prowadzi do znacznego podniesienia skuteczności agentów.

Zarządzanie procesem rozumowania i refleksji modelu będzie pojawiać się jeszcze niejednokrotnie w dalszych lekcjach. Teraz wystarczy zapamiętać, że sam "reasoning" modeli to nie wszystko, a zachowanie modelu może być sterowane na różne sposoby, ale też nie powinno narzucać zbyt sztywnych ograniczeń.

## Transformacja oraz wzbogacanie zapytań przez LLM

Z transformacjami zapytań HTTP spotykamy się na co dzień i zazwyczaj nie ma problemu ze zmianą formatu czy wzbogaceniem obiektu żądania. Jednak w przypadku agentów AI transformacje nie zawsze są oczywiste, ponieważ mamy do czynienia z językiem naturalnym i zwykle bardzo dynamicznym kontekstem.

Aby zrozumieć, na czym polega wyzwanie, spójrzmy na poniższy schemat interakcji, w której agent AI zostaje poproszony o odnalezienie informacji w bazie wiedzy. Oryginalne zapytanie użytkownika jest ogólne, ale zarazem potencjalnie wystarczające do powiązania go z zawartością przechowywanych dokumentów.

![](https://cloud.overment.com/2026-01-24/ai_devs_4_query_transformation-c76cc21e-4.png)

Jeśli przyjrzymy się bliżej, zobaczymy, że pomiędzy zapytaniem użytkownika a zawartością pliku nie występuje bezpośrednie dopasowanie słów kluczowych. Dopiero dzięki transformacji zapytania poprzez wykorzystanie synonimów oraz powiązanych zagadnień, agent był w stanie dotrzeć do właściwego dokumentu.

Transformacja zapytań nie zawsze będzie skuteczna, jeśli będziemy opierać ją wyłącznie na natywnej wiedzy modelu. Najczęściej będziemy mieli do czynienia z dokumentami dotyczącymi indywidualnego kontekstu klienta. Oznacza to, że bez przynajmniej ogólnej wiedzy na temat ich zawartości model nie będzie w stanie skutecznie po nich nawigować.

Poniżej widzimy jeden z takich scenariuszy. Zapytanie użytkownika dotyczy „tematów omówionych w pierwszym tygodniu” i choć istnieje prawdopodobieństwo, że agent zorientuje się, że chodzi o pliki `ai_devs/S01E0*.md`, raczej nie powinniśmy na to liczyć. Jeśli jednak agent otrzyma informację, że przed eksploracją dostępnych zasobów ma przeczytać automatycznie generowany plik `_index.md`, szansa na to, że nawigowanie po bazie wiedzy będzie skuteczne, zdecydowanie rośnie.

![](https://cloud.overment.com/2026-01-24/ai_devs_4_context_based_transformation-cd67deaf-a.png)

Kolejną kwestią wartą uwagi jest **poprawne rozpoznanie** tego, czy pytania użytkownika w ogóle dotyczą bazy wiedzy. Jest to skomplikowane zwłaszcza wtedy, gdy agent posiada dostęp do więcej niż jednego narzędzia dostarczającego zewnętrzny kontekst, takiego jak "**web\_search**". Wówczas najlepszym rozwiązaniem będzie zwrócenie uwagi agenta na to, aby **zadawał pytania doprecyzowujące** przed rozpoczęciem eksploracji.

Dodatkowe instrukcje obsługi narzędzi mogą pomagać, lecz mogą również negatywnie wpływać na zachowanie agenta, zwłaszcza gdy stają się zbyt skomplikowane lub szczegółowe. Z tego powodu lepszym rozwiązaniem jest przechowywanie „mapy treści” w plikach zewnętrznych zamiast w instrukcji systemowej.

## Techniki optymalizacji szybkości i skuteczności narzędzi

Każda kolejna akcja wykonywana przez agenta AI oznacza kolejne zapytanie do LLM, a co za tym idzie, również przesłanie dotychczasowego kontekstu. Jeśli w danej turze agent zdecyduje się na skorzystanie z narzędzi, musimy doliczyć także czas reakcji zewnętrznych usług, który w przypadku na przykład generowania grafik może trwać nawet kilka minut. Ale nawet jeśli czas odpowiedzi zewnętrznych usług jest mały, to i tak każdy kolejny krok znacznie wydłuża czas odpowiedzi agenta.

Główne obszary, które w tym kontekście powinny zwrócić naszą uwagę to:

- **Cache Promptu:** jest to [priorytet](https://arxiv.org/abs/2311.04934). Providerzy, np. [Gemini](https://ai.google.dev/gemini-api/docs/caching?hl=en\&lang=python) czy [OpenAI](https://platform.openai.com/docs/guides/prompt-caching) oferują automatyczne cache'owanie promptu, o ile ten nie ulega zmianie pomiędzy zapytaniami. Cache nie tylko redukuje koszty, ale przede wszystkim **znacząco zmniejsza tzw. "Time to First Token (TTFT)"**, czyli czas reakcji.
- **Error Rate**: skoro każdy krok agenta oznacza kolejne zapytanie do LLM, najbardziej logiczne jest ograniczenie tych zapytań do minimum. Jest to oczywiste, lecz biorąc pod uwagę to, co powiedzieliśmy do tej pory na temat budowania narzędzi dla LLM, niekoniecznie proste do osiągnięcia.
- **Połączenie akcji:** widzieliśmy to już na przykładzie Linear, gdzie `workspace_metadata` umożliwia dostęp do danych, które normalnie wymagałyby kilku kroków.
- **Równoległe zapytania:** większość providerów API oferuje "parallel function calling", dzięki czemu nieuzależnione od siebie akcje, mogą być wykonane równolegle. Równie pomocne jest projektowanie narzędzi tak, aby pozwalały na np. edytowanie więcej niż jednego rekordu jednocześnie.
- **Zmiana modelu:** nie każde zadanie będzie wymagało zaangażowania najmocniejszego i zwykle najwolniejszego modelu. Wszędzie tam, gdzie tylko pojawia się taka możliwość, powinniśmy sięgać po mniejsze modele.
- **Ograniczenie kontekstu:** korzystanie z prompt cache nie zawsze będzie możliwe, szczególnie na początku interakcji. Wówczas długość kontekstu jest jednym z głównych czynników wpływających na czas reakcji modelu, dlatego zależy nam na ograniczeniu go do niezbędnego minimum.
- **Ograniczenia wypowiedzi:** generowanie każdego kolejnego tokenu zajmuje czas, więc wszędzie tam gdzie jest to możliwe, powinniśmy kierować modelem tak, by unikał zbędnego przedłużania wypowiedzi. Największą korzyść daje tutaj także sposób przekazywania informacji pomiędzy narzędziami. Na przykład jeśli jedno narzędzi zwraca nam treść raportu, a drugie wysyła je e-mailem, to domyślnie model musi wygenerować tę treść dwukrotnie. Ale jeśli pierwsze narzędzie zapisze raport w pliku, a drugie doda go jako załącznik wiadomości, to mówimy skracamy czas realizacji zadania mniej więcej o połowę!

![Przykłady optymalizacji obsługi narzędzi](https://cloud.overment.com/2026-01-24/ai_devs_4_optimization-8a52441d-2.png)

## Podstawy zarządzania kontekstem w workflow i logice agentów

Context Engineering odnosi się do technik dążących do budowania oraz utrzymania wysokiej jakości kontekstu w interakcji z agentami AI i może odnosić się do dwóch różnych obszarów:

- Zarządzania kontekstem przy pracy z Claude Code czy Open Code. Wówczas mówimy o aktywnościach użytkownika, związanych np. z restartowaniem konwersacji i przenoszeniem informacji pomiędzy wątkami. **Tym obszarem nie będziemy zajmować się w AI\_devs**.
- Zarządzanie kontekstem **w logice aplikacji** odbywa się poprzez kontrolowanie przebiegu interakcji, zarządzanie dostępnymi narzędziami oraz ich rezultatami, a także komunikację pomiędzy agentami. Jest to zupełnie inna kategoria problemów niż zarządzanie kontekstem podczas kodowania z AI. To właśnie na niej skupimy się w tej i kolejnych lekcjach.

Dotychczas zewnętrzny kontekst dołączaliśmy do konwersacji jako część promptu systemowego. Obecnie wiemy, że nadal może być to odpowiednie miejsce, o ile dane te nie zmieniają się w trakcie interakcji, co skutkowałoby natychmiastową utratą cache'u. W przypadku agentów AI problem ten rozwiązuje się poniekąd samoistnie, ponieważ zewnętrzny kontekst jest wczytywany przez narzędzia trafiające naturalnie do najnowszych fragmentów wątku. Nadal musimy jednak uważać na dynamiczne dane w instrukcji systemowej, gdyż nawet dodanie informacji o bieżącej dacie oraz godzinie może mieć krytyczny wpływ na wydajność całego systemu.

![Dynamiczne elementy instrukcji systemowej i wpływ na prompt cache](https://cloud.overment.com/2026-01-24/ai_devs_4_dynamic_context-67f5d208-5.png)

Poza stabilnością instrukcji systemowej, niezmienne powinny pozostawać także elementy dotychczasowej sesji - wiadomości użytkownika, asystenta oraz wywołania narzędzi. Problem w tym, że dość szybko możemy dojść do limitów okna kontekstowego, co uniemożliwi dalszą interakcję. Jeszcze do niedawna rekomendowane było stosowanie "pływającego okna kontekstu", czyli usuwanie najstarszych wiadomości. Teraz wiemy, że lepiej utrzymać je w kontekście i zachować cache, niż oszczędzać tokeny przez ucinanie wątku, ale nie rozwiązuje to problemu limitu okna kontekstowego.

Narzędzia takie jak Claude Code czy Cursor na bieżąco monitorują wykorzystanie okna kontekstowego. Gdy wątek zbliża się do limitu, uruchamiana jest funkcja auto-compact, czyli podsumowanie. Jest to forma kompresji, więc część informacji zostanie utracona o ile oryginalna część wątku nie zostanie zapisana na przykład w formie pliku tekstowego, który agent będzie mógł eksplorować w razie potrzeby.

![Porównanie technik zarządzania kontekstem - pływające okno vs kompresja i filesystem](https://cloud.overment.com/2026-01-24/ai_devs_4_thread_context_management-ea50a552-a.png)

Tworzenie plików przechowujących kontekst, do których agent ma dostęp, pojawia się tutaj po raz kolejny. Wcześniej wspominaliśmy o tym przy okazji przenoszenia treści pomiędzy narzędziami (generowanie i wysyłanie raportu), lecz wtedy agent mógł jedynie wskazać konkretny dokument. Nic nie stoi na przeszkodzie, aby w przypadku narzędzi również umożliwić mu pełną eksplorację tych plików. Wówczas np. narzędzie `web_search` mogłoby zwracać rozbudowane rezultaty, ale agent wczytywałby do kontekstu jedynie istotne dla niego fragmenty.

![Przykład zapisywania wyników działania narzędzi w formie plików dostępnych dla agenta](https://cloud.overment.com/2026-01-24/ai_devs_4_tool_results_as_files-999f9f03-e.png)

Na ten moment w temacie Context Engineeringu to wszystko. Zatem w tej chwili musimy zapamiętać, że **prompt cache to priorytet**, a **system plików** znacznie zwiększa elastyczność nawigacji po nawet bardzo rozbudowanych konwersacjach.

## Dynamiczne listy narzędzi i zasobów wiedzy

W temacie zarządzania kontekstem łatwo zauważyć, że istotnym problemem szybko stają się narzędzia, których schematy nie tylko zużywają część limitu, lecz także rozpraszają uwagę modelu. Co gorsza, narzędzia są wczytywane nawet wtedy, gdy nie mamy potrzeby ich uruchamiać.

Na ten moment wystarczy abyśmy dążyli do tego, aby dany agent posiadał dostęp do nie więcej niż 10-15 narzędzi. Ich dynamiczne wczytywanie bez wpływu na **prompt cache** jest aktualnie możliwe tylko w przypadku [Anthropic](https://www.anthropic.com/engineering/advanced-tool-use). Natomiast pracując z innymi providerami musimy skorzystać z innych technik i na tym etapie wystarczy wiedzieć, że chodzi między innymi o:

- stosowanie sub-agentów z których każdy posiada dostęp do indywidualnych umiejętności oraz działa w osobnych oknach kontekstowych, ale z możliwością łatwej wymiany informacji z innymi agentami, np. poprzez system plików
- stosowanie narzędzi do **uruchamiania kodu**, np. [Daytona](https://www.daytona.io/). Wówczas pozostałe narzędzia (np. kalendarz) mogą mieć formę katalogów i plików, które agent może eksplorować i wykonywać. Wówczas w kontekście na stałe mamy tylko podstawowe narzędzia, więc początkowe wykorzystanie limitu kontekstu jest minimalne. Coś takiego określamy mianem "Progressive Disclosure".

![Wizualizacja układu narzędzi dla subagentów oraz code execution](https://cloud.overment.com/2026-01-24/ai_devs_4_subagents_code_sandbox-ffee68d6-2.png)

Omawiając **wzbogacanie zapytań**, zauważyliśmy problem dotyczący dynamicznego wczytywania zasobów wiedzy. Polega on na tym, że agent **początkowo „nie wie, o czym wie”**. Podobny kłopot występuje przy eksplorowaniu narzędzi. Może to doprowadzić do sytuacji, w której agent uzna, że nie jest w stanie podjąć działania, mimo że w teorii posiada taką możliwość.

Dlatego niezależnie od tego, czy pracujemy z subagentami, czy z sandboxem do uruchamiania kodu, zawsze powinniśmy zapewnić agentowi przynajmniej podstawowe wskazówki dotyczące dostępnych zasobów lub metod ich odkrywania.

## Obsługa wymaganych danych wejściowych, uprawnień oraz zgody

Wszystkie działania agenta są **niedeterministyczne**. Nawet gdy użytkownik wprost poprosi o wysłanie wiadomości na wskazany adres e-mail, to i tak może dojść do halucynacji, która wyśle ją do zupełnie innej osoby. Dlatego wszystkie akcje, które są nieodwracalne i mogą wiązać się z podjęciem niepożądanej akcji należy obsługiwać na poziomie graficznego interfejsu użytkownika. Czyli:

- Jeśli agent wymaga od użytkownika podania danych, których nie wolno pomylić, powinniśmy wyświetlić formularz zamiast polegać na tym, że model poprawnie wyodrębni poszczególne wartości z treści wiadomości. Choć obecne modele radzą sobie z tym świetnie, ryzyko błędu wciąż istnieje.
- Jeśli agent decyduje się na wykonanie akcji, użytkownik musi zostać poproszony o jej akceptację, a zgoda powinna opierać się na przyciskach, a nie na wiadomości do modelu. W przeciwnym razie, nawet jeśli użytkownik wprost powie, że zmienił zdanie, AI może zignorować lub błędnie zinterpretować jego prośbę.
- Dostęp do zasobów oraz akcji ograniczonych uprawnieniami musi być obsługiwany na poziomie kodu. Oznacza to, że agent **nie może** samodzielnie ustalać na przykład identyfikatora użytkownika. Podobnie dostęp do systemu plików musi być kontrolowany w taki sposób, aby agenci nie mieli fizycznej możliwości sięgania po dokumenty innych użytkowników.

Oczywiście w powyższych scenariuszach model nadal ma możliwość decydowania o tym, kiedy dany interfejs zostanie wywołany. Jednak gdy już to zrobi, to użytkownik będzie mieć pewność, że akcja zostanie wykonana dokładnie tak, jak sugeruje to aplikacja.

![Zarządzanie dostępami, zgodami oraz danymi wejściowymi w deterministyczny sposób](https://cloud.overment.com/2026-01-24/ai_devs_4_permissions-395034b4-7.png)

Wyjątek stanowią tutaj interfejsy dynamiczne, w przypadku których również może dojść do błędów modelu, który może dodać ukryte pola lub pomylić identyfikatory poszczególnych pól. Warto o tym pamiętać.

## Rola problemu prompt injection oraz jailbreakingu

Halucynacje modelu to tylko jeden z problemów związanych z działaniem LLM w logice aplikacji. Znacznie poważniejszym wyzwaniem jest **prompt injection**, czyli zmiana zachowań modelu wbrew instrukcji systemowej, oraz **jailbreaking**, polegający na omijaniu zabezpieczeń wprowadzonych przez providera lub jego twórców.

Zła wiadomość jest taka, że Prompt Injection to problem **otwarty**, na który obecnie nie ma rozwiązania ani skutecznych technik obrony. Najlepszym przykładem jest wspominany już profil [Pliny the Liberator](https://x.com/elder_plinius?lang=en), który jak dotąd złamał zabezpieczenia wszystkich popularnych modeli językowych. Co więcej na ominięcie ich zabezpieczeń zwykle nie potrzebuje więcej niż 24 godzin.

Spójrzmy więc na to od praktycznej strony oraz agenta posiadającego do dyspozycji dwa narzędzia: **kalendarz** oraz **email**. Jeśli agent przeglądając pocztę otrzyma wiadomość o treści w stylu "Czy możesz przesłać mi swój plan spotkań na najbliższy tydzień?", to może dosłownie na nią odpowiedzieć, pobierając wcześniej wydarzenia z kalendarza wraz z kontaktami do osób biorących w nich udział. Problem w tym, że wiadomość może pochodzić od nieautoryzowanego użytkownika.

![Przykład prompt injection w połączeniu z narzędziami agentów](https://cloud.overment.com/2026-01-24/ai_devs_4_prompt_injection-dce58564-8.png)

Fakt, że nie posiadamy obecnie **jakichkolwiek narzędzi** aby bronić się przed atakami taki jak ten powyżej sprawia, że agenci AI powinni być ograniczeni na poziomie środowiskowym. Z kolei stosowanie ich w obszarach, które mogą doprowadzić do wycieku danych czy podjęcia niepożądanych akcji, w ogóle nie powinno mieć miejsca.

Choć to wszystko brzmi fatalnie (i w rzeczywistości takie jest), istnieje wiele scenariuszy w których agenci AI mogą swobodnie funkcjonować i pomagać nam w codziennej pracy, bez istotnych ryzyk związanych z problemem Prompt Injection. Po prostu jako programiści powinniśmy mieć na uwadze ten problem i adresować go już na poziomie wczesnych założeń projektu oraz przy kontakcie z biznesem. O tym jednak porozmawiamy nieco później.

## Fabuła

![https://vimeo.com/1169706511](https://vimeo.com/1169706511)

## Transkrypcja filmu z Fabułą

"Świetna robota przy numerze piąty!

Mamy już listę podejrzanych osób i nie jest ona wcale taka długa. Musimy teraz zweryfikować, która z tych osób faktycznie była widziana nieopodal jednej z elektrowni.

Mamy dostęp do lokalizacji wszystkich elektrowni, które nas interesują. Mamy także dostęp do API, które potrafi zwrócić ostatnie lokalizacje, w których dłużej przebywały osoby obserwowane przez "System". Mamy też osobne API do sprawdzenia, jakim poziomem dostępu do usług systemu dysponuje taka osoba.

Znajdź proszę idealnego kandydata, który faktycznie pracuje gdzieś nieopodal elektrowni atomowej i podeślij nam jego dane. Centrala już będzie wiedzieć, co z nim należy zrobić.

Czekamy na dalsze informacje z Twojej strony."

## Zadanie

Musisz namierzyć, która z podejrzanych osób z poprzedniego zadania **przebywała blisko jednej z elektrowni atomowych.** Musisz także ustalić jej **poziom dostępu** oraz informację koło której elektrowni widziano tę osobę. Zebrane tak dane prześlij do `/verify`. Nazwa zadania to **findhim**.

#### Skąd wziąć dane?

1. **Lista elektrowni + ich kody**
   - Pobierz JSON z listą elektrowni (wraz z kodami identyfikacyjnymi) z:
     - `https://hub.ag3nts.org/data/tutaj-twój-klucz/findhim_locations.json`

2. **Gdzie widziano konkretną osobę (lokalizacje)**

   - Endpoint: `https://hub.ag3nts.org/api/location`
   - Metoda: `POST`
   - Body: `raw JSON` (nie form-data!)
   - Zawsze wysyłasz pole `apikey` oraz dane osoby (`name`, `surname`)
   - Odpowiedź: lista współrzędnych (koordynatów), w których daną osobę widziano.

   Przykładowy payload:

   ```json
   {
     "apikey": "tutaj-twój-klucz",
     "name": "Jan",
     "surname": "Kowalski"
   }
   ```

3. **Jaki poziom dostępu ma wskazana osoba**

   - Endpoint: `https://hub.ag3nts.org/api/accesslevel`
   - Metoda: `POST`
   - Body: `raw JSON`
   - Wymagane: `apikey`, `name`, `surname` oraz `birthYear` (rok urodzenia bierzesz z danych z poprzedniego zadania, np. z CSV)

   Przykładowy payload:

   ```json
   {
     "apikey": "tutaj-twój-klucz",
     "name": "Jan",
     "surname": "Kowalski",
     "birthYear": 1987
   }
   ```

#### Co masz zrobić krok po kroku?

Dla każdej podejrzanej osoby:

1. Pobierz listę jej lokalizacji z `/api/location`.
2. Porównaj otrzymane koordynaty z koordynatami elektrowni z `findhim_locations.json`.
3. Jeśli lokalizacja jest bardzo blisko jednej z elektrowni — masz kandydata.
4. Dla tej osoby pobierz `accessLevel` z `/api/accesslevel`.
5. Zidentyfikuj **kod elektrowni** (format: `PWR0000PL`) i przygotuj raport.

#### Jak wysłać odpowiedź?

Wysyłasz ją metodą **POST** na `https://hub.ag3nts.org/verify`.

Nazwa zadania to: **findhim**.

Pole `answer` to **pojedynczy obiekt** zawierający:

- `name` – imię podejrzanego
- `surname` – nazwisko podejrzanego
- `accessLevel` – poziom dostępu z `/api/accesslevel`
- `powerPlant` – kod elektrowni z `findhim_locations.json` (np. `PWR1234PL`)

Przykład JSON do wysłania na `/verify`:

```json
{
  "apikey": "tutaj-twój-klucz",
  "task": "findhim",
  "answer": {
    "name": "Jan",
    "surname": "Kowalski",
    "accessLevel": 3,
    "powerPlant": "PWR1234PL"
  }
}
```

#### Nagroda

Jeśli Twoja odpowiedź będzie poprawna, Hub odeśle Ci flagę w formacie {FLG:JAKIES\_SLOWO} - flagę należy wpisać pod adresem: <https://hub.ag3nts.org/> (wejdź na tą stronę w swojej przeglądarce, zaloguj się kontem którym robiłeś zakup kursu i wpisz flagę w odpowiednie pole na stronie).

### Wskazówki

- **Dane wejściowe z poprzedniego zadania** — lista podejrzanych pochodzi z zadania S01E01. Potrzebujesz imienia, nazwiska i roku urodzenia każdej osoby — warto zachować wynik S01E01 w formie nadającej się do ponownego użycia. Pamiętaj że chodzi tylko o osoby które wysyłałeś jako podejrzanych do Hubu.
- **Obliczanie odległości geograficznej** — API zwraca współrzędne (latitude/longitude). Żeby sprawdzić, czy dana lokalizacja jest "bardzo blisko" elektrowni, użyj wzoru na odległość na kuli ziemskiej (np. [Haversine](https://en.wikipedia.org/wiki/Haversine_formula)). LLM pomoże Ci w napisaniu takiej funkcji. Szukamy osoby która była najbliżej którejś elektrowni.
- **Wykorzystaj Function Calling** — to technika, w której model LLM zamiast odpowiadać tekstem wywołuje zdefiniowane przez Ciebie funkcje (narzędzia). Opisujesz narzędzia w formacie JSON Schema (nazwa, opis, parametry), a model sam decyduje, które wywołać i z jakimi argumentami. Ty obsługujesz wywołania i zwracasz wyniki z powrotem do modelu. W tym zadaniu Function Calling sprawdza się szczególnie dobrze: agent może samodzielnie iterować przez listę podejrzanych, odpytywać kolejne endpointy i wysłać gotową odpowiedź — bez sztywnego kodowania kolejności kroków w kodzie.
- **Format `birthYear`** — endpoint `/api/accesslevel` oczekuje roku urodzenia jako liczby całkowitej (np. `1987`). Jeśli Twoje dane zawierają pełną datę (np. `"1987-08-07"`), pamiętaj o wyciągnięciu samego roku przed wysłaniem żądania.
- **Zabezpieczenie pętli agenta** — jeśli stosujesz podejście agentowe z Function Calling, ustal maksymalną liczbę iteracji (np. 10-15), żeby uchronić się przed nieskończoną pętlą w razie błędu modelu.
- **Wybór modelu** - jeśli Twój agent myli się lub pracuje w kółko nie podając prawidłowej odpowiedzi, spróbuj użyć mocniejszego modelu lub lepiej sformułować prompt systemowy. W tym zadaniu dobrze sprawdza się na przykład model `gpt-5-mini` lub jego mocniejsza wersja `gpt-5`.
