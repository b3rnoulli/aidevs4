---
title: S03E02 — Ograniczenia modeli na etapie założeń projektu
space_id: 2476415
status: scheduled
published_at: '2026-03-24T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/basics-1773910669.png'
circle_post_id: 30844628
---
Choć mogłoby się wydawać inaczej, interakcja z AI nie musi uwzględniać użytkownika, generatywna aplikacja nie musi być czatbotem, system RAG nie musi być podłączony do istniejącej wiedzy, a agent nie musi mieć kontaktu z otoczeniem.

Budując generatywne aplikacje bardzo **często wpadamy w różne schematy.** Część z nich może być nawet użyteczna i warto je eksplorować. Ale w momencie gdy staną się dla nas jasne, najlepiej zacząć je łamać i szukać własnych ścieżek i rozwiązań. Choć takie podejście nie gwarantuje sukcesu, tak z pewnością wiąże się z doświadczeniem, które trudno jest zdobyć w inny sposób.

Mówię o tym dlatego, ponieważ klienci, biznes czy nawet my sami, będziemy wpadać na różne pomysły zastosowania AI. Dobrze jest więc mieć sposób na znalezienie unikatowej wartości poprzez budowanie rozwiązań dopasowanych do nas bądź personalizowanie tych istniejących w wymiarze, który nie wpada do głowy samoistnie. Takie podejście pozwoli również na zwielokrotnienie otrzymywanej wartości oraz ułatwi adresowanie problemów, które inaczej wydają się niemożliwe do rozwiązania (i czasem takie są, ale można je ominąć).

Dlatego dziś poszukamy wartości w budowaniu użytecznych narzędzi, które maksymalnie wykorzystują możliwości modeli, jednocześnie adresując ich słabsze strony.

## Definiowanie roli i zaangażowania systemu AI

Oczekiwania wobec rozwiązań AI są początkowo bardzo wysokie. Wizje automatyzacji całych procesów, a nawet działów, wydają się być w zasięgu ręki. Co więcej, nawet wstępne demo może sugerować, że rzeczywiście tak jest. Jednak gdy przychodzi czas wdrożenia i przygotowania aplikacji do oddania w ręce użytkowników, pojawiają się wyzwania, na które trudno odpowiedzieć. Mam tu na myśli zarówno niedopasowanie do **wymagań biznesowych**, ale także **ograniczenia techniczne** oraz różnego rodzaju **zagrożenia** obejmujące wycieki danych, naruszenia bezpieczeństwa czy rozmaite ryzyka biznesowe.

Rozważmy kilka typowych scenariuszy, z którymi z dużym prawdopodobieństwem się spotkamy:

- **Rozmowa z "własną bazą wiedzy"**: czyli klasyczny system RAG, nad którym pracę można zacząć od pytania **czy naprawdę tego potrzebujemy?** A jeśli odpowiedź jest twierdząca, warto przejść do zmapowania serii faktycznych zastosowań. Wówczas może się okazać, że ich zaadresowanie będzie niemożliwe ze względu na wysiłek potrzebny nawet na etapie zebrania danych z różnych źródeł. Jeśli jednak okaże się, że proponowane scenariusze są wartościowe oraz możliwe do realizacji, to zamiast od razu przechodzić do planu całego projektu, warto zweryfikować postawione tezy za pomocą serii prototypów, a nawet MVP (Minimum Viable Product). Jeśli testy nie spełnią oczekiwań, warto albo **porzucić pomysł** albo zmienić zakres, na przykład skupiając się na obszarach onboardingu pracowników, działach sprzedaży czy narzędziach dla managerów.
- **Czatbot na stronę:** czyli próba automatyzacji obsługi klienta, w której rzeczywiście można dopatrywać się różnych zalet. Jednak pomysł adresowania procesów **budowania relacji z klientami** nawet przez zaawansowane czatboty raczej obecnie nie jest dobrym pomysłem (i nie wiadomo, kiedy się to zmieni). Z kolei wprowadzenie narzędzi, które będą **wspierać** osoby pracujące w tym obszarze, ma mnóstwo sensu już teraz. Co więcej, może to nie mieć **nic wspólnego z czatbotem**, lecz z agentami działającymi w tle, zintegrowanymi z panelami obsługi klienta w taki sposób, że pracownicy nie będą musieli uczyć się pracy z AI.
- **Działania marketingowo/sprzedażowe**: pomysł automatyzacji dotarcia do potencjalnych klientów na skalę, poprzez automatyczne wiadomości wysyłane przez boty, na przykład w obszarze e-mail marketingu, to zwykle zły pomysł z perspektywy wizerunkowej. Jednocześnie takie działania na skalę są realizowane przez różne firmy od dawna i nawet jeśli ich skuteczność jest niska, to efekt skali przekłada się na zauważalne wyniki. Tutaj, podobnie jak w pozostałych przykładach, warto pomyśleć o narzędziach wspierających istniejące procesy, a niekoniecznie o ich pełnej automatyzacji. Podłączanie obecnych LLM pod możliwość **odpisywania na wiadomości e-mail** to proszenie się o kłopoty i realne zagrożenie dla biznesu.
- **All-in-one:** systemy agentowe dla **całej organizacji** to pomysły, które padają coraz częściej i co więcej, zaczynają być w zasięgu od strony realizacji. Jednak problemy dotyczące Prompt Injection czy halucynacji modelu sprawiają, że zarządzenie wysokim poziomem skuteczności oraz odpowiednim poziomem bezpieczeństwa, jest bardzo trudne, a momentami całkowicie niemożliwe. Obecnie znacznie lepiej jest skupić się na **dedykowanych i wyspecjalizowanych narzędziach**, o ile nie mamy wyraźnego powodu, aby robić inaczej (np. w działach R\&D odpowiedzialnych za innowacje).

![Projektowanie generatywnych aplikacji to balansowanie między możliwościami, a ograniczeniami](https://cloud.overment.com/2026-02-20/ai_devs_4_roles-ed3c6f7f-b.png)

Powyższe scenariusze dotyczą typowych i bardzo popularnych problemów, które firmy próbują adresować z pomocą AI. Jak widać, bezpośrednia odpowiedź na początkowe potrzeby to raczej zły pomysł. Jako osoby zaangażowane w projektowanie rozwiązań od technicznej strony musimy być świadomi nie tylko zagrożeń i problemów, ale także alternatywnych ścieżek, które nadal będą **dostarczać wartość**, ograniczając przy tym ryzyko krytycznych problemów, bądź istotnych wyzwań (np. kosztów).

**Jednocześnie** trzeba mieć na uwadze fakt, jak bardzo AI rozwinęło się w ostatnim czasie i że pod wieloma względami nie widać spowolnienia tego procesu, lecz przyspieszenie. Oznacza to, że w naszym interesie będzie **regularne aktualizowanie swoich przekonań**. To co dziś jest "niemożliwe", jutro może być dostępne bez wysiłku. Natomiast coś, co dziś wydaje się w teorii bardzo proste, w praktyce wcale takie nie jest - nasze zadanie polega na odróżnianiu jednego od drugiego.

Zakładając jednak, że fundamenty projektu i jego główne założenia są poprawnie ustalone. Przechodzimy więc do implementacji, gdzie również czekają nas decyzje dotyczące **roli AI** oraz zakresu zadań, które będą realizowane przez kod, a które przez model. Nie zawsze jest to oczywiste, ponieważ:

- nasze doświadczenie na początku może błędnie kierować nas zbyt mocno w stronę AI bądź przeciwnie, w stronę programistycznych rozwiązań, które już znamy. Tym bardziej, że niekiedy właściwą odpowiedzią jest **wycofanie się z pomysłu** i poszukanie zupełnie innej ścieżki, która nawet może obejmować oddanie procesu w całości w ręce ludzi.
- wzrost możliwości AI nie musi wprost oznaczać, że ciężar logiki musi być przeniesiony na model. Wprost przeciwnie, model może lepiej zarządzać **deterministyczną logiką** poprzez odpowiedni routing zapytań czy posługiwanie się referencjami do dokumentów czy ich fragmentów.

Na co dzień okazuje się, że największa wartość, jak zawsze, opiera się na jednej umiejętności: **zdolności do określania, co w danej chwili nie ma znaczenia**.

Załóżmy zatem, że tworzymy rozwiązanie, którego celem jest wsparcie w zakresie obsługi skrzynek e-mail osoby zaangażowanej w kilka projektów. Skrzynki posiadają wyłącznie jednego właściciela, więc nie mówimy tu o sytuacji w której zasadne jest wdrażanie zewnętrznych systemów. Po prostu chodzi nam o usprawnienie pracy i dla ułatwienia, załóżmy, że jest to skrzynka działająca w ramach GSuite (czyli z interfejsem Gmail). Wiemy zatem, że:

- Jeden agent powinien obsługiwać wszystkie skrzynki
- Każde konto to oddzielny projekt, a dane nie mogą się ze sobą mieszać
- Część informacji będzie wspólna i będzie mogła być współdzielona między adresami
- Możemy przez API odczytywać treści wiadomości, wątków oraz ich metadane
- Agent może łączyć informacje z treści maili z notatkami użytkownika
- Możemy tworzyć filtry, które automatycznie przypisują etykiety do wiadomości
- Użytkownik sam może też przypisywać takie etykiety

Poniżej widzimy wizualizację zakresu tego projektu - **jeden agent, baza wiedzy i konta różnych projektów** z odpowiednim poziomem elastyczności, przy zachowaniu zasad prywatności i bezpieczeństwa.

![Założenia i zakres agenta do obsługi poczty](https://cloud.overment.com/2026-02-20/ai_devs_4_email_agent-0320ac23-d.png)

Gdy patrzymy na takie zadanie, wyobraźnia może nam sugerować **pełną automatyzację** bądź scenariusze zbliżone do niej. Podsumowania, odpisywanie na wiadomości, bądź nawet proaktywne podejmowanie działań zwiększające skuteczność sprzedażową przez różne techniki budowania relacji - to wszystko może iść naprawdę bardzo daleko.

Jednak rzeczywistość jest nieco inna. Nawet jeśli agent byłby w stanie odnaleźć się w konkretnych scenariuszach, tak zbudowanie systemu który autonomicznie dotrze do niezbędnych informacji, "połączy kropki" oraz poprowadzi proces lepiej, niż robi to człowiek, jest obecnie raczej poza zasięgiem. Oczywiście są w tym zakresie podejmowane próby i na rynku pojawiają się narzędzia z takimi obietnicami, a nawet do pewnego stopnia potrafią je realizować, szczególnie gdy odpowiednio zawęzimy zakres.

W takiej sytuacji pytanie brzmi: **jak stworzyć rozwiązanie, które wniesie wysoką wartość, przy zminimalizowaniu ryzyk oraz negatywnego wpływu ograniczeń modeli?**

Wówczas o agencie pomagającym w obsłudze poczty można myśleć przez pryzmat rzeczy takich jak:

- Rodzaje aktywności: **etykietowanie**, **priorytetyzacja**, **szkicowanie**, **filtrowanie**, **wzbogacanie**, **optymalizacja**. W tych obszarach AI może nas wspierać i przyczyniać się tym do wzrostu efektywności oraz jakości. Konsekwencje ewentualnych błędów również są tu dość ograniczone, głównie ze względu na wysokie zaangażowanie ze strony człowieka.
- Rodzaje ograniczeń: **brak akcji do wysyłania wiadomości**, progresywne **izolowanie zasobów wiedzy** i **zarządzanie uprawnieniami**. Chodzi więc o programistyczne ograniczenia, które w dużym stopniu adresują problem Prompt Injection
- Wysoka elastyczność: pomimo wielu kont i źródeł wiedzy, mówimy o jednej logice, która dopasowuje się do bieżącego kontekstu.

W przykładzie **03\_02\_email** mamy agenta pracującego na przykładowych danych imitujących dwie skrzynki e-mail, którego zadaniem jest przypisanie etykiet i przygotowanie szkiców odpowiedzi dla wybranych wątków. W przykładzie znajdują się także **eksperymenty** monitorujące skuteczność agenta pod kątem każdej z tych aktywności.

Główne mechaniki opierają się więc na narzędziach umożliwiających interakcję ze skrzynkami e-mail oraz bazą wiedzy. Działania agenta są natomiast objęte dodatkowymi mechanikami, które kontrolują zakres jego uprawnień w ramach danej sesji. Zatem jeśli agent rozpocznie pracę ze skrzynką A, programistycznie zamyka sobie dostęp do skrzynki B oraz do informacji z bazy wiedzy, które jej dotyczą. Limit obowiązuje do czasu rozpoczęcia nowej sesji, ale dotyczy wyłącznie **szkicowania wiadomości**, gdzie potencjalnie może dojść do przekazania danych, które nie powinny się w niej znaleźć. Co więcej, ograniczenie nie dotyczy wyłącznie kontekstu konta, ale także szczegółów wiadomości, więc jeśli agent zaczyna pracę nad e-mailem z domeny @przykladowa-firma.com, baza wiedzy zostaje ograniczona wyłącznie do informacji wspólnych oraz przestrzeni związanej z tym konkretnym klientem. Zatem:

- **Kategoryzacja** nie posiada ograniczeń
- **Szkicowanie** jest ograniczone według konta oraz na podstawie domeny osoby kontaktowej bądź etykiety

Logika prezentuje się więc następująco:

![Główne elementy logiki agenta pracującego z e-mailem](https://cloud.overment.com/2026-02-21/ai_devs_4_email_agent_mechanics-ab829706-c.png)

> Przykład **03\_02\_email** działa na testowych danych. W razie potrzeby stworzenia prawdziwej integracji z GSuite przydatny może okazać się [Gmail MCP](https://github.com/iceener/gmail-streamable-mcp-server/tree/main/src) utworzony na podstawie szablonu omawianego w pierwszych lekcjach.

Mamy więc tu do czynienia z różnymi poziomami zabezpieczeń, których celem jest uniknięcie sytuacji w której dane na których pracuje agent zostaną wykorzystane w niewłaściwym kontekście. Oczywiście nie rozwiązuje to wszystkich naszych problemów, ale fakt, że agent **nie posiada możliwości wysyłania maili** sprawia, że to człowiek ostatecznie decyduje o akcjach, których nie da się odwrócić.

![Mechaniki bezpieczeństwa agenta do zarządzania pocztą](https://cloud.overment.com/2026-02-21/ai_devs_4_data_scope-8dcf2bed-4.png)

Działanie systemu nie musi się już kończyć, ponieważ efekt pracy agenta może być wyzwalaczem dla innych agentów bądź deterministycznych akcji. Bo przykładowo przypisanie etykiety do wiadomości jest zdarzeniem, które może być obserwowane. Zatem jeśli wątek dostaje etykietę **Bug Report**, to jego treść może zostać wykorzystana do utworzenia zadania w systemie zarządzania zadaniami czy bezpośrednio w repozytorium. Z kolei tam inny agent (bądź człowiek) może określić jego złożoność i rozwiązać je automatycznie.

Podobnie też, nie wszystko musi odbywać się tu automatycznie, ponieważ również człowiek może przypisywać etykiety do wiadomości i to również może przekładać się na serię kolejnych zdarzeń.

W tym miejscu ponownie możemy dojść do wniosku, że **wszystko jest możliwe**, i już niebawem większość naszych projektów będzie realizowana niemal w pełni autonomicznie. Problem w tym, że zaprojektowanie rozwiązań, na których będzie można polegać, i które nie będą bardziej przeszkadzać niż pomagać, nie jest oczywiste. Jednocześnie możemy też zaprojektować je tak, aby ich aktywność była niemal niezauważalna, a efekty ich działania przekładały się na realne korzyści biznesowe lub prywatne.

## Kontrolowanie poziomu trudności zakresu pracy modelu

Poziom trudności. Może się wydawać, że nie ma problemu z jego określeniem. Obserwując to, do czego są dziś zdolne modele generatywnej sztucznej inteligencji, można błędnie ocenić, co jest łatwe do wdrożenia, a co niekoniecznie. Poziom trudności również wzrasta szybciej, niż się wydaje, gdy przechodzimy do systemów zdolnych do **autonomicznego** działania. Wówczas nawet pomimo ogromnego wsparcia ze strony AI, spotykamy zupełnie nową klasę programistycznych problemów na które czasem dość trudno jest odpowiedzieć. Czasem okazuje się też, że niektóre z nich występowały już w przeszłości i istnieją narzędzia oraz koncepcje z których dziś możemy korzystać.

Jeszcze niedawno LLM-y regularnie popełniały nawet drobne błędy, takie jak literówki, których obecność skutecznie uniemożliwiała im wykraczanie poza raczej proste akcje. A i tak, nawet w ich przypadku, musieliśmy dbać o detale, takie jak programistyczne przepisywanie adresów stron www pojawiających się w wypowiedziach modelu czy generowane struktury obiektów JSON, które musiały być ograniczone do absolutnego minimum.

Obecnie, wyzwania te są powiązane ze **złożonością zadań**, **dostępem do informacji**, czy **trudnością posługiwania się długim kontekstem**. Problemy pojawiają się też na poziomie architektury, integracji czy ogólnej stabilności systemu związanej zarówno ze skutecznością modeli, jak i ekosystemu narzędzi. Choć wydaje się, że rozwój samych modeli wkrótce rozwiąże większość z nich, tak wraz ze wzrostem ich możliwości, zwiększają się także oczekiwania oraz złożoność rozwiązań, które tworzymy. I tak jak jeszcze 2 lata temu musieliśmy dbać o poprawne formatowanie obiektu JSON, tak dziś również będzie nam zależało na **programistycznym wsparciu modeli**.

W lekcji **S02E01** mówiliśmy o **listach zadań** stosowanych przez agentów do kodowania, np. w Cursor, oraz ich problemach związanych z zapominaniem o ich aktualizowaniu. Sugeruje to, że stosowanie podobnych technik nie ma za bardzo sensu. Jednak nie zawsze musi tak być.

Precyzja systemów agentowych faktycznie może być, delikatnie mówiąc, dyskusyjna. O ile w sytuacji, gdy agent pracuje bezpośrednio z człowiekiem, odchylenia i błędy są tolerowane, bo szybko możemy je naprawić, o tyle w przypadku agentów działających w tle mówimy raczej o przekreśleniu sensu ich istnienia. Bo po co nam system, który wykonuje swoje zadanie błędnie co piąty raz i to nawet jeśli proces jest z góry ustalony i jasno doprecyzowany.

Załóżmy więc, że mamy zdefiniowany proces, na przykład opracowywania dokumentów na podstawie wskazanych danych i wyników wyszukiwania. Proces ten obejmuje konkretne aktywności, ale sam w sobie jest dość dynamiczny, więc nie może zostać zrealizowany przez sztywny workflow. Potrzebujemy więc elastyczności agentów, ale też wysokiego poziomu pewności, że poszczególne kroki zostaną wykonane.

Możemy więc przygotować strukturę **planu** składającego się z **zadań** posiadających nazwy, opisy, statusy, zależności, a nawet przypisanych agentów bądź przynajmniej umiejętności niezbędne do ich ukończenia. W ten sposób plan może zostać przedstawiony jako seria częściowo uzależnionych od siebie kroków. Część z nich może być zrealizowana równolegle, a inne będą musiały czekać na swoją kolej. Możliwe są też sytuacje gdy zadanie w trakcie realizacji zmienia swój status na oczekujący, ze względu na potrzebę wykonania dodatkowych kroków przed jego ukończeniem. Wystarczy więc, że status systemu będzie sprawdzany po ukończeniu każdego z cykli aż do ukończenia wszystkich zadań.

![Przykład realizacji zadań według bieżącego stanu systemu](https://cloud.overment.com/2026-02-21/ai_devs_4_heartbeat-eca750f0-8.png)

Przekładając to na logikę agenta, mówimy o spójnej strukturze opisujących plan oraz poszczególne zadania. Ich bieżący stan jest w dużym stopniu zmieniany programistycznie, ale agenci mogą odczytywać treść tych dokumentów. Każdy z nich posiada też dostęp do systemu plików, który stanowi ich wymiany informacji.

W przykładzie **03\_02\_events** znajduje się dość **rozbudowany** system agentowy, który wykorzystuje omawiane wcześniej mechaniki Observational Memory do zarządzania kompresją informacji w ramach okna kontekstowego. Tutaj jednak mechanika ta jest zastosowana dla każdej sesji z dowolnym agentem, więc mają oni możliwość pracować w dość dużym horyzoncie czasu oraz skutecznie się ze sobą komunikować.

Po uruchomieniu przykładu system rozpoczyna etap **planowania** na podstawie celu opisanego w pliku **goal.md** oraz utworzenia struktury katalogów dla tego zadania. Ewentualnie system może być uruchomiony bezpośrednio na wskazanym planie (np. przez polecenie **npm run demo --workflow report-v1 --rounds 8**).

> **UWAGA:** przykładowy wynik pracy tego agenta znajduje się w pliku **raport.html**, który jest dostępny także [tutaj](https://cloud.overment.com/report-1771683944.html).

Następnie dochodzi do wywołania głównej logiki opartej o opisany przed chwilą system heartbeat i aktualizację stanu po ukończeniu każdego cyklu. Agenci przechodzą więc przez etapy takie jak:

1. **Przeszukanie dostępnych źródeł**
2. **Pogłębienie wyszukiwania**
3. **Wstępne notatki**
4. **Utworzenie pierwszej wersji**
5. **Przygotowanie finalnego raportu**

Agenci podczas pracy mogą uznać, że konieczne jest zebranie dodatkowych informacji, co może wpłynąć albo na poszczególne zadania planu, albo nawet utworzenie nowych zadań. Tutaj poziom elastyczności będzie uzależniony od naszych potrzeb i decyzji. Możemy nawet uwzględnić potrzebę kontaktu z człowiekiem w sytuacji gdy plan będzie wymagał rozstrzygnięcia bądź decyzji, której system nie będzie mógł podjąć samodzielnie.

![Przykład wykonania planu w logice heartbeat i aktualizacji stanu](https://cloud.overment.com/2026-02-21/ai_devs_4_heartbeat_execution-9aa05bfd-f.png)

Zatem raz jeszcze, logika o której tu mówimy opiera się o trzy, główne komponenty:

- **Kontrakty:** określające strukturę planu i poszczególnych zadań oraz zależności pomiędzy nimi. Na tej podstawie budowany i aktualizowany jest stan aplikacji
- **Heartbeat:** czyli logika pełniąca rolę managera przydzielającego zadania oraz aktualizująca stan.
- **Pamięć:** oparta o system plików, działająca zarówno w zakresie jednego agenta, ale także komunikacji pomiędzy nimi.

![Przykład logiki do zarządzania zadaniami agentów](https://cloud.overment.com/ai_devs_4_heartbeat_agent-1771690222.png)

Podsumowując, przykład ten pokazuje nam jak możemy **kontrolować poziom trudności zadań** oraz **wspierać agentów AI** przez mechaniki związane ze strukturą informacji oraz zarządzania komunikacją czy nawet przydzielaniem zadań. Oczywiście logika, którą mamy w omówionym przykładzie może być dopasowana do konkretnych przypadków, bądź przeciwnie - zostać zgeneralizowana na tyle, aby móc elastycznie adresować różnego rodzaju problemy wykorzystując przy tym dostępne narzędzia.

## Zmniejszanie ryzyka prompt injection

Choć nie ma obecnie definitywnego sposobu na wyeliminowanie problemu prompt injection, tak istnieją techniki zmniejszania ryzyka ich wystąpienia oraz ewentualnych konsekwencji. Część z nich mieliśmy już nawet okazję obserwować, ale temat ten jest na tyle ważny, że musimy się przy nim zatrzymać. Zacznijmy od głównych zasad:

- Prompt Systemowy powinien być traktowany jako **publicznie dostępny**. Nie może więc w nim być jakichkolwiek danych, które po zdobyciu mogą być wykorzystane w nieodpowiedni sposób.
- Zmiana zachowania agenta przez czatbota **nie może** doprowadzić do uzyskania nieuprawnionego dostępu do akcji bądź zasobów. Dostęp do nich musi być **kontrolowany programistycznie**.
- Agenci powinni mieć **zablokowaną** bądź **wysoce nadzorowaną** możliwość kontaktu ze światem zewnętrznym. Aktywności takie jak postowanie, wysyłanie maili, smsów, publikacje dokumentów w przypadku agentów posiadających dostęp do **poufnych informacji** (np. treści wewnątrzfirmowych) mogą doprowadzić do ich ujawnienia.
- Nawet komunikacja wewnątrzfirmowa w przypadku dostępu do informacji wymagających określonych uprawnień może wymagać narzucenia technicznych ograniczeń. Tutaj jednak sytuacja jest nieco prostsza, bo rzadko chcemy automatyzować komunikację wewnętrzną.
- Zewnętrzne źródła do których mają dostęp agenci powinny być **limitowane**, a jeśli nie jest to możliwe, to generowane na ich podstawie treści, **starannie weryfikowane**.

Mówiąc wprost: **nie możemy ufać agentom w zakresie udostępniania informacji oraz pracy na zewnętrznych źródłach danych**. Wszelkie miejsca w których model posiada kontakt ze światem zewnętrznym muszą być traktowane jako **niebezpieczne**.

Są jednak sytuacje w których będziemy musieli wdrożyć taki system na produkcję. Wówczas możemy ustawić kilka rodzajów barier, które zmniejszą ryzyko problemów. Chodzi między innymi o filtrowaniu treści wiadomości użytkownika, która powinna przechodzić przez dodatkowy prompt, którego zadaniem będzie ocena w kontekście prompt injection. Rezultatem promptu powinno być zwrócenie ustalonego ciągu znaków odpowiadającym **weryfikacji** oraz **blokadzie**, np. "**bezpieczne**" i "**niebezpieczne**". Następnie oba warianty powinny być **programistycznie zweryfikowane**. Mówimy tu o oddzielnym zapytaniu, które jest całkowicie odseparowane od głównego wątku. Atakujący nie ma więc fizycznej możliwości poznać wybrane frazy, więc ma bardzo ograniczone pole manewru. Ominięcie takiego zabezpieczenia jest możliwe, ale przy obecnych modelach dość trudne dla typowego użytkownika.

![Przykład bariery przed prompt injection](https://cloud.overment.com/2026-02-21/ai_devs_4_barrier-c7a74410-4.png)

Takie filtrowanie może być jednak niewystarczające w przypadku agentów AI, gdzie w ogóle nie musi dojść do intencjonalnego ataku, ale zwykłej pomyłki. Tutaj jedyną linią obrony jest obecnie zabezpieczenie **prawne** oraz **jawne informowanie użytkownika** o tym, że wykorzystujemy AI w komunikacji. Połączenie tego z technikami, które do tej pory omawialiśmy w lekcjach da nam relatywnie duży poziom bezpieczeństwa, ale jednocześnie nie mówimy tutaj o gwarancji. Dlatego jeśli absolutnie nie musimy, powinniśmy **unikać takich sytuacji**.

## Zarządzanie niską wydajnością modeli i halucynacjami

Patrząc na projekty takie jak [Taalas](https://taalas.com/the-path-to-ubiquitous-ai/) czy [Groq](https://groq.com/) bądź [Cerebras](https://www.cerebras.ai/) można odnieść wrażenie, że rzeczywistość w której szybkość inferencji jest praktycznie natychmiastowa jest tuż za rogiem. Niestety każda z tych firm do tej pory nie udowodniła, że jest w stanie zaoferować dostęp do większych modeli z zachowaniem stabilności API. W tym zakresie najdalej wydaje się być Cerebras, którzy po dołączeniu do OpenAI udostępnili GPT-5.3-Codex-Spark, którego szybkość jest imponująca, aczkolwiek wiele wskazuje, że jest to bardzo skompresowany model. Trudno powiedzieć jak długo będziemy na to czekać, a do tego czasu musimy jakoś zarządzić kwestią wydajności.

Aktualnie wiemy, że w kontekście szybkości działania modeli możemy operować na pięciu obszarach:

- **Liczbie tokenów wejściowych:** wpływa bezpośrednio na czas reakcji. Dotyczy to promptu systemowego, definicji narzędzi oraz kontekstu konwersacji.
- **Poziomie wykorzystania cache:** wpływa na koszty i czas reakcji. Obejmuje wyłącznie tokeny wejściowe.
- **Liczbie tokenów wyjściowych:** wpływa na czas generowania odpowiedzi i może być kontrolowana nie tylko przez skrócenie wypowiedzi modelu, ale też przez liczbę kroków agenta.
- **Liczbie zapytań:** o ile zapytania nie są realizowane równolegle i nie są objęte cache, ich liczba znacząco zwiększa czas odpowiedzi.
- **Mniejszych modelach:** zwiększają szybkość i zmniejszają koszty, ale ograniczają też możliwości.

Pytanie tylko jak to wszystko można osiągnąć w praktyce? I okazuje się, że tutaj mamy do dyspozycji kilka opcji z których kluczem okazuje się **generowanie kodu** oraz **sandbox**.

W przykładzie **03\_02\_code** mamy agenta, którego zadaniem jest opracowanie raportu PDF zawierającego zestawienie kosztów z 10 działów dla których łącznie mamy **240 plików** z danymi finansowymi. To ponad **150 000 linii**, które agent musi przetworzyć i przedstawić w formę czytelnego raportu. Ich wczytanie do kontekstu jest praktycznie niemożliwe, a taka skala daje niemal pewność błędnego rezultatu w sytuacji, gdy LLM musiał wszystko "przeliczać w pamięci".

Agent posiada więc dostęp do **systemu plików** oraz **wykonania kodu**, który jest uruchamiany w **sandbox'ie Deno** (zatem https://deno.com musi być zainstalowane w naszym systemie!). W przeciwieństwie do przykładu z lekcji **S02E05** ten sandbox oferuje nam znacznie większe możliwości, a także lepszą kontrolę uprawnień.

Po uruchomieniu przykładu rozpoczyna się proces tworzenia raportu, który obejmuje następujące kroki:

- **Eksploracja:** wczytanie struktury katalogów w celu zorientowania się, jakie dokumenty są dostępne.
- **Nauka:** przeczytanie **fragmentów** plików w celu zrozumienia ich struktury, co umożliwia nawigowanie po ich treści z pomocą kodu. Agent czyta także **instrukcje** dotyczące generowania raportów finansowych oraz dokumentów PDF
- **Agregacja**: utworzenie skryptu gromadzącego informacje ze wszystkich dokumentów.
- **Prezentacja:** utworzenie skryptu generującego prezentację w formacie PDF

Wszystkie te etapy realizowane są przez agenta autonomicznie.

![](https://cloud.overment.com/2026-02-22/ai_devs_4_code_execution_agent-bf7df470-d.png)

Efektem pracy agenta jest gotowy raport PDF sprawdzający do zaledwie 2-3 stron dane z tysięcy rekordów. Dokument ten w tym przykładzie będzie opracowany w zaledwie 6-10 krokach, co wprost przekłada się na ogromną optymalizację kosztową oraz czasu.

Poniżej widzimy przykład takiego raportu. Biorąc pod uwagę możliwości **obecnych modeli językowych**, można z bardzo dużym prawdopodobieństwem stwierdzić, że obliczenia są poprawne. Problem w tym, że nie mamy pewności, czy rzeczywiście tak jest, dopóki tego nie sprawdzimy. Choć same obliczenia są realizowane w kodzie i tutaj raczej trudno mówić o pomyłce, to już kwestia tego, czy dane zostały wczytane poprawnie, stwarza ogromną przestrzeń do błędów. Dlatego agenci odpowiedzialni za tak istotne dokumenty powinni pozostawać pod ścisłym nadzorem, a ich logika powinna obejmować jasne procesy sterowane za pomocą kodu wszędzie tam, gdzie to możliwe.

![Przykład raportu wygenerowanego przez agenta](https://cloud.overment.com/2026-02-22/ai_devs_4_report-98cf2745-f.png)

Budowanie agentów zdolnych do generowania i wykonywania kodu wewnątrz sandboxów wiąże się ze zwiększoną złożonością architektury. Nasz agent to w praktyce trzy procesy: **Proces Główny**, **MCP (STDIO)** oraz **Sandbox**. Oznacza to, że zastosowanie tego agenta na skali produkcyjnej z tysiącami użytkowników może stanowić wyzwanie. Jednocześnie związane z tym korzyści są tak wyraźne, że wysiłek może być uzasadniony. Tym bardziej, że problem sandboxów dla agentów zaczyna być adresowany przez między innymi [Cloudflare](https://developers.cloudflare.com/sandbox/) czy firmy takie jak [Daytona](https://www.daytona.io/).

![Architektura agenta posługującego się sandboxem](https://cloud.overment.com/2026-02-22/ai_devs_4_code_execution_agent_architecture-79274770-e.png)

Widzimy więc jak kilka decyzji projektowych sprawiło, że **jeden agent** jest w stanie przetworzyć ogromne zestawy danych oraz dość precyzyjnie kształtować raporty. Szybkość działania, efektywność kosztowa a nawet poziom halucynacji są tu nieporównywalne z tym, czego możemy spodziewać się po agentach działających w standardowy sposób. Co więcej, konfiguracja narzędzi w postaci **systemu plików** oraz **wykonania kodu** domyślnie sprawia, że agent ten posiada znacznie większe możliwości, które wykraczają poza generowanie dokumentów PDF.

---

## Fabuła

![https://vimeo.com/1175524872](https://vimeo.com/1175524872)

## Transkrypcja filmu z Fabułą

"Świetnie! Wiemy już, które sensory nie działają poprawnie i wiemy też, że nasz technik nie jest zbyt rzetelny i czasami wpisuje głupoty do raportów. Technikiem zajmiemy się później, a teraz musimy przejść do kolejnego problemu.

Pamiętasz, że w logach, które analizowałeś, były jakieś błędy związane z firmware'em? Czas się tym zająć.

Nasi specjaliści zgrali pamięć sterownika ECCS (Emergency Core Cooling System), który zarządza systemem chłodzenia i wrzucili ją do maszyny wirtualnej.

Możemy teraz pobawić się tym oprogramowaniem. Plusem jest to, że jest to bardzo ograniczona dystrybucja Linuxa, więc prawdopodobnie bez problemu sobie z tym poradzisz, a jeśli sam nie znasz tego systemu, to każdy LLM w czasach w których się znajdujesz go ogarnia.

Za pomocą naszego API możesz wykonywać polecenia wewnątrz wirtualnej maszyny.

Spraw proszę, aby system chłodzenia uruchomił się poprawnie. W przeciwnym razie nie będziemy w stanie doprowadzić elektrowni do stabilnego działania.

A! Tylko uważaj proszę, bo ten system ze sterownika ma jakieś dziwne zabezpieczenia. Odetnie Ci dostęp gdy dotkniesz którykolwiek z plików lub katalogów z czarnej listy.

Przed nami jeszcze kilka innych poprawek, ale myślę, że ta bardzo posunie nas naprzód. Jak zawsze, więcej szczegółów podałem w notatce do tego filmu."

## Zadanie

Twoim zadaniem jest uruchomić oprogramowanie sterownika, które wrzuciliśmy do maszyny wirtualnej. Nie wiemy, dlaczego nie działa ono poprawnie. Operujesz w bardzo ograniczonym systemie Linux z dostępem do kilku komend. Większość dysku działa w trybie tylko do odczytu, ale na szczęście wolumen z oprogramowaniem zezwala na zapis.

Oprogramowanie, które musisz uruchomić znajduje się na wirtualnej maszynie w tej lokalizacji:
**`/opt/firmware/cooler/cooler.bin`**

Gdy poprawnie je uruchomisz (w zasadzie wystarczy tylko podać ścieżkę do niego), na ekranie pojawi się specjalny kod, który musisz odesłać do Centrali.

**Nazwa zadania: firmware**

Odpowiedź wysyłasz w poniższy sposób do `/verify`:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "firmware",
  "answer": {
    "confirmation": "uzyskany kod"
  }
}
```

Kod, którego szukasz, ma format:
**`ECCS-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`**

Dostęp do maszyny wirtualnej uzyskujesz poprzez API:
**`https://hub.ag3nts.org/api/shell`**

używasz go w ten sposób:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "cmd": "help"
}
```

#### Zasady bezpieczeństwa

- pracujesz na koncie zwykłego użytkownika
- nie wolno Ci zaglądać do katalogów `/etc`, `/root` i `/proc/`
- jeśli w jakimś katalogu znajdziesz plik `.gitignore` to respektuj go. Nie wolno Ci dotykać plików i katalogów, które są tam wymienione.
- Niezastosowanie się do tych zasad skutkuje zablokowaniem dostępu do API na pewien czas i przywróceniem maszyny wirtualnej do stanu początkowego.

#### Co masz zrobić?

1. Spróbuj uruchomić plik binarny `/opt/firmware/cooler/cooler.bin`
2. Zdobądź hasło dostępowe do tej aplikacji (zapisane jest w kilku miejscach w systemie)
3. Zastanów się, jak możesz przekonfigurować to oprogramowanie (`settings.ini`), aby działało poprawnie.
4. Jeśli uznasz, że zbyt mocno namieszałeś w systemie, użyj funkcji `reboot`.

### Wskazówki

- **Podejście agentowe** — Zadanie idealnie nadaje się do pętli agentowej z Function Calling. Agent potrzebuje jednego narzędzia do wykonywania poleceń powłoki i jednego do wysyłania odpowiedzi do huba. Każde wywołanie narzędzia to jedno zapytanie HTTP do API powłoki — planuj działania sekwencyjnie.
- **Wybór modelu** — To zadanie wymaga rozumowania i adaptacji do nieoczekiwanych odpowiedzi API. Modele o słabszych zdolnościach rozumowania mogą utknąć w pętli lub pomylić komendy. Spróbuj użyć `anthropic/claude-sonnet-4-6` — jego zdolność do śledzenia kontekstu i adaptacji do nieznanego API robi tutaj dużą różnicę.
- **Zaczynaj od help** — Shell API na tej maszynie wirtualnej ma niestandardowy zestaw komend. Nie zakładaj, że wszystkie standardowe polecenia Linuxa zadziałają. Szczególnie edycja pliku odbywa się inaczej niż w standardowym systemie.
- **Obsługa błędów API** — Shell API może zwracać kody błędów zamiast wyników (rate limit, ban, 503). Zadbaj o to, żeby agent widział te kody i mógł na nie zareagować — np. poczekać i spróbować ponownie. Ban pojawia się gdy naruszysz zasady bezpieczeństwa i trwa określoną liczbę sekund. Możesz też obsługę tych błędów zaimplementować bezpośrednio w narzędziu, a agentowi odsyłać bardziej opisowe komunikaty o błędach.
- **Reset** — Jeśli coś pójdzie nie tak w trakcie, możesz zawsze zresetować maszynę i spróbować od nowa.

---
