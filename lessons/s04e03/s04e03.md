---
title: S04E03 — Kontekstowa współpraca z AI
space_id: 2476415
status: scheduled
published_at: '2026-04-01T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/0403-1774694244.png'
circle_post_id: 31103396
---
## Film do lekcji

![https://vimeo.com/1177419174](https://vimeo.com/1177419174)

Każdego dnia ma miejsce mnóstwo działań, które nie wymagają bezpośredniego zaangażowania z naszej strony. Aplikacje i serwisy mają wbudowane automatyzacje, systemy powiadomień, harmonogramy czy reguły, które przekładają się na gotowe rezultaty. W przypadku większości z nich nawet nie jesteśmy świadomi złożoności logiki, która pracuje dla nas. Są jednak sytuacje, w których sami konfigurujemy reguły i automatyzacje, a nawet tworzymy dedykowane narzędzia, które dają nam dodatkowe możliwości.

Na przestrzeni dotychczasowych lekcji widzieliśmy mnóstwo przykładów agentów zdolnych do wykonywania pracy bez naszego aktywnego zaangażowania. Rozmawialiśmy także o scenariuszach w których taki system staje się proaktywny i podejmuje działania na podstawie tego, co dzieje się wokół.

Bez wątpienia mówimy o dużych możliwościach. Jednak już wiele razy przekonaliśmy się, jak wiele barier pojawia się w praktyce i że ich ominięcie nie zawsze jest oczywiste. Dlatego dziś przyjrzymy się temu, jak faktycznie możemy zintegrować AI z naszą codziennością, ale nie w kontekście bezpośredniej interakcji. Będzie to zatem rozszerzenie tematów z lekcji **S03E03** i **S04E01** oraz wszystkiego, czego nauczyliśmy się o projektowaniu agentów i narzędzi AI. Jednak tym razem skupimy się już bezpośrednio na kontekście codziennych aktywności i różnych obszarów biznesu.

## Szerokie spojrzenie na kontekstową pracę z AI

Urządzenia, aplikacje i usługi stanowiące część naszej codzienności zostało zaprojektowane z myślą o tym, że to ludzie są ich użytkownikami. Teraz mówimy o sytuacji, gdzie interakcja coraz częściej obejmuje także boty. Przekłada się to na wzrost znaczenia API, dostępności treści stron internetowych w kontekście scrapowania czy zakresu uprawnień związanych ze sterowaniem urządzeniami. Obserwujemy także znaczący wzrost możliwości modeli i agentów w zakresie mechanik z kategorii "Computer Use".

Aby określić, co w ogóle jest możliwe, warto się rozejrzeć i sprawdzić, co w ogóle robimy na co dzień oraz z jakich narzędzi korzystamy. Zwykle mówimy tutaj o:

- **Mac / Windows / Linux:** systemy operacyjne już na start oferują nam ogromne możliwości konfiguracji i ustawień. Począwszy od narzędzi CLI i różnego rodzaju skryptów startowych, przez harmonogramy, po możliwość programowania akcji (np. przez AppleScript) czy dostępu do urządzeń (np. mikrofonu). Przydatne są także tzw. „deep-linki”, o których wspominaliśmy na przykład w kontekście pracy z Obsidianem.
- **iOS / Android / Inne:** systemy mobilne czy urządzenia z kategorii "smart" to również duża przestrzeń do automatyzacji zarówno w zakresie podejmowania akcji, jak i nawet samego odczytywania informacji z czujników (np. lokalizacji).
- **Komunikatory:** automatyzacja wiadomości zwykle kojarzy się negatywnie ze spamem od botów. Jednocześnie wszystkie popularne komunikatory pozwalają na dość swobodną automatyzację, co możemy wykorzystać w kontekście agentowym, na przykład do monitorowania aktywności, przekazywania feedbacku czy wymiany informacji. Agenci bardzo naturalnie stają się częścią firmowej i prywatnej komunikacji.
- **Kalendarze:** zdarzenia mają tu znaczenie nie tylko w kontekście spotkań z innymi, ale także planowania pracy czy zarządzania aktywnościami wokół wydarzeń, np. przygotowaniem, realizacją, podsumowaniami czy analizą skuteczności. Kalendarz może być również wykorzystywany do komunikacji z agentem w zakresie zadań czy informowania o naszej dostępności.
- **Maile:** podobnie jak w przypadku komunikatorów, masowe wysyłanie maili generowanych przez AI jest raczej złą praktyką. Widzieliśmy już jednak jak AI może pomóc nam w organizowaniu wątków, dostarczaniu informacji do szkiców wiadomości, a nawet opracowywaniu spersonalizowanych newsletterów. E-mail stanowi też dobry kanał komunikacji do asynchronicznej współpracy z agentami.
- **Internet:** połączenie agentów AI w zakresie **odczytu** informacji z mediów społecznościowych czy wybranych stron www może wnieść mnóstwo wartości szczególnie w zakresie monitorowania wybranych tematów czy aktywności twórców. Świetnie sprawdzają się tutaj integracje z YouTube czy platformą X oraz wszelkiego rodzaju kanały RSS czy bezpośrednie scrapowanie treści (oczywiście z uwzględnieniem regulaminów).
- **Zarządzanie zadaniami:** połączenia AI z narzędziami do zarządzania projektami mogą sięgać znacznie dalej niż proste zarządzanie, opisywanie czy przeszukiwanie wpisów. Agenci na tym etapie mogą już mieć jasne odpowiedzialności i działać w wybranych zakresach. Należy jednak tu zachować dużą ostrożność w kontekście Prompt Injection oraz zakresu uprawnień. Dość interesujące podejście w tym zakresie prezentują narzędzia takie jak [Vibe-Kanban](https://vibekanban.com/).
- **Zdalne repozytoria:** agenci już teraz pojawiają się w projektach na Githubie, a niektórzy programiści przełączają się na tryb pracy "mobilnej", gdzie implementacja przynajmniej części funkcjonalności odbywa się bez uruchomienia komputera. Choć AI obecne w procesie review czy nawet na etapie rozwiązywania wybranych ticketów może mieć sens, tak trzeba mieć na uwadze przypadki takie jak [wykradanie tokenów](https://snyk.io/blog/cline-supply-chain-attack-prompt-injection-github-actions/) należy brać całkowicie na serio. Tym bardziej, że takie sytuacje mogą mieć miejsce nawet przy bezpośredniej współpracy z agentem do kodowania, gdy coś umknie naszej uwadze.
- **Edytory tekstu:** generowane treści obecnie nie niosą zbyt wiele wartości i nadal dość łatwo rozpoznać "płytkie" artykuły czy generyczne komentarze w mediach społecznościowych. Ale gdy wykorzystamy AI jako narzędzie **wspierające** proces tworzenia treści, na przykład w kontekście kontroli jakości, procesu kreatywnego, tworzenia grafik czy w połączeniu z CMS do zarządzania dokumentacją bądź całymi stronami WWW (np. blogiem), perspektywa znacząco się zmienia. Pozwala to zachować, a nawet podnieść wartość treści, a także zwiększyć efektywność ich tworzenia.
- **Narzędzia sprzedażowe:** proces researchu, zarządzania bazą kontaktów, utrzymaniem procesów w systemach CRM, przygotowaniu ofert czy analizie lejków sprzedażowych to obszary w których mądre zastosowanie AI może wprost przełożyć się na wyniki finansowe i mieć potencjalnie największy zwrot. Należy jedynie mieć na uwadze fakt, ze sprzedaż mocno opiera się o budowanie relacji, a automatyzacje AI wdrożone w niewłaściwy sposób potrafią je bardzo szybko zniszczyć.
- **Narzędzia graficzne:** rozwijające się możliwości modeli w zakresie rozumienia obrazów, a nawet wideo można wykorzystać w połączeniu z programami graficznymi, np. Figma / Blender czy nawet Unreal Engine. Tutaj można powiedzieć, że "jesteśmy dość wcześnie", ale też postęp w ostatnim czasie jest znaczący. Podobnie wygląda to w kontekście generowania grafik, gdzie jak mieliśmy się już okazję przekonać, precyzja modeli nawet przy generowaniu rozbudowanych opisów jest bardzo duża.
- **Rozrywka / Rozwój / Lifestyle:** AI może być świetnym towarzyszem nauki, rozrywki oraz szeroko rozumianego rozwoju (niekoniecznie w roli psychologa!). Poznawanie nowych języków programowania, narzędzi czy rozwoju różnego rodzaju umiejętności wspólnie z AI coraz bardziej przypomina pracę z trenerem. Nic też nie wyklucza połączenia na przykład nauki języka z native speakerem oraz ćwiczeń wspólnie z AI.

Warto więc teraz wypisać sobie **wszystkie narzędzia z których korzystamy**, a następnie zapoznać się z możliwościami ich integracji i tutaj mówimy zarówno o API, możliwości scrapowania treści stron (np. dokumentacji), jak i dostępności aplikacji desktopowych (np. w kontekście deep-link). Warto też zerknąć na opcje powiadomień mailowych, ponieważ one również mogą być wykorzystane w kontekście automatyzacji (np. jako wyzwalacz akcji).

![Kontekstowa integracja AI](https://cloud.overment.com/2026-03-06/ai_devs_4_contextual-8aafd7e1-2.png)

Zastosowanie AI w wymienionych obszarach nie jest oczywiste, bo każdy z nas pracuje w nieco inny sposób oraz z nieco innymi narzędziami. Modele nie są też obecnie dobrymi doradcami w tym zakresie, ponieważ ich sugestie są bardzo generyczne i trudno odnaleźć w nich realną wartość. Dlatego jeśli od razu nic nie przychodzi nam do głowy, to warto obserwować to jak pracujemy bądź to, jak realizowane są obecnie procesy biznesowe i nieustannie zadawać sobie pytanie **jak AI może nam tutaj pomóc?** oraz **czy powinniśmy tu angażować AI?**

Przenieśmy więc to w bardziej konkretny wymiar. Osobisty "stack" może obejmować:

- **Pakiet GSuite:** czyli przede wszystkim Gmail i Google Drive, wliczając w to także Google Docs, Google Sheets i Google Calendar. Wszystkie te usługi są dostępne przez API z poziomu Google Console.
- **Linear:** czyli popularne narzędzie do zarządzania projektami z bardzo solidnym API obejmującym webhooki.
- **Slack/Discord/Telegram:** komunikatory pozwalają nie tylko na przesyłanie wiadomości, ale także ich obserwowanie. Jeśli nie chcemy dawać AI dostępu do pełnej korespondencji to w przypadku na przykład Slacka, możemy obserwować jedynie wiadomości oznaczone konkretną emotikonką.
- **Obsidian / iA Writer:** czyli edytory markdown z pełnym wsparciem x-scheme-url oraz dostępnością z poziomu CLI.
- **Firecrawl:** prawdopodobnie najlepsze dostępne narzędzie do scrapowania stron www. Alternatywnie dobrze wypada też Jina.
- **Zencal:** czyli narzędzie do udostępniania kalendarza w celu rezerwacji spotkań w ustalonych okienkach czasowych. Tutaj także mamy do dyspozycji API i webhooki.
- **Easytools:** czyli narzędzie do sprzedaży cyfrowych produktów oraz ich obsługi. Tutaj do dyspozycji mamy API oraz natywne integracje
- **ElevenLabs:** oferuje świetne modele speech-to-text i text-to-speech, aczkolwiek jeśli wystarczą nam domyślne warianty głosów, to modele Gemini czy OpenAI również są w porządku.
- **Tally:** narzędzie do tworzenia formularzy, posiada swoje API oraz możliwość podłączania webhooków w celu obserwowania zgłoszeń
- **Google Maps:** przydaje się w codziennym kontekście odnajdywania adresów czy pozyskiwania aktualnych informacji na temat miejsc.
- Uploadthing
- **Daytona / E2B / Sandbox SDK:** czyli sandboxy tworzone przede wszystkim z myślą o agentach
- **Replicate:** oferuje dostęp do modeli generowania obrazu, wideo, a także różnego rodzaju modyfikacji (np. skalowania). Dostępny jest także finetuning
- **Github:** chyba nikomu nie trzeba przedstawiać. Świetnie sprawdzają się także Github Actions.
- **YouTube / X:** dostępne w formie API sprawdzają się przy obserwowaniu nowości branżowych czy aktywności firm oraz produktów. Połączenie wpisów / filmów ze scrapperem stron www daje niemal pełny wgląd w najważniejsze informacje (np. changelogi)
- **Dropshare / Uploadthing:** czyli narzędzia do udostępniania plików, bardzo przydatne w kontekście agentów, o czym mieliśmy już okazję się przekonać.
- **HTMLCSSToImage:** to narzędzie do konwertowania szablonów HTML na obrazy. Świetnie sprawdza się na przykład na potrzeby social media czy blogów.
- **Convex/Supabase:** czyli bazy danych z łatwym i praktycznie natychmiastowym dostępem z poziomu API
- **Attio:** system CRM z całkiem dobrym API oraz przemyślanym interfejsem
- **Dub:** narzędzie do generowania skróconych linków z opcją analityki, świetne do monitorowania skuteczności i konwersji z działań marketingowych
- **Resend:** czyli narzędzie do newsletterów i maili transakcyjnych, które można wykorzystywać także w prywatnym kontekście.
- **SMS API:** czyli bramka SMS, świetnie sprawdzająca się do prywatnych powiadomień.
- **E-Signatures / Fakturownia / Quaderno:** czyli narzędzia do umów, faktur i rozliczeń, przydatne w kontekstach biznesowych

![Przykładowy zestaw narzędzi z potencjałem na integrację AI](https://cloud.overment.com/2026-03-07/ai_devs_4_tool_stack-7a0914f8-8.png)

Wspólnym elementem **wszystkich** wymienionych powyżej usług jest dostępność **API**, które zwykle oferuje bardzo szerokie uprawnienia. Warto też przyjrzeć się strukturze endpointów oraz zwracanym danym, ponieważ w kontekście AI może się okazać, że są one niekompletne albo zbyt ograniczone.

Z takimi informacjami możemy zastanowić się nad scenariuszami w których AI faktycznie może nam pomóc. Chodzi nam więc o **ograniczenie** naszego zaangażowania, przy zachowaniu rozsądku w zakresie **uprawnień** agentów. Największa trudność leży jednak w zaprojektowaniu logiki tak, aby nam nie przeszkadzała. Bo przykładowo:

- załóżmy, że chcemy usprawnić proces indywidualnych konsultacji z klientami
- zakres obejmuje rezerwację terminu sesji, przygotowanie do spotkania oraz opracowanie wniosków po jego zakończeniu, **wliczając w to także rozliczenia** (wystawienie faktury, oceny, przypomnienie o płatności itd.)

Jeśli w takiej konfiguracji spotkamy sytuację, w której klient będzie chciał zarezerwować więcej niż jedną sesję i dodatkowo opłacić je z góry, to źle zaprojektowany system przyniesie nam więcej problemów niż wartości. Podobne sytuacje możemy też spotkać na co dzień przy programowaniu systemów, gdy zaadresowane założenia okazują się niewystarczające w zderzeniu z rzeczywistością.

Zastanówmy się więc nad scenariuszami, które mogą przydać się w codziennej pracy oraz kontekście biznesowym.

## Definiowanie założeń zadań i procesów realizowanych w tle

Myśląc o aktywnościach w których rola AI może być znacząca, możemy spojrzeć albo przez pryzmat **wybranej aplikacji bądź serwisu** albo **przepływie informacji pomiędzy nimi**. W kontekście agentowym warto także uwzględnić **kontekst** z bazy wiedzy. Przejdźmy więc przez bardzo konkretne scenariusze z obu tych obszarów.

**Kontekst indywidualny:**

- **Przegląd wydarzeń:** agent podłączony do kalendarza nie musi ograniczać się wyłączenie do zarządzania wpisami. Model posiada rozległą wiedzę na temat technik zarządzania czasem, np. "time blocking" oraz prezentować wpisy w formie która pozwoli nam dostrzec problemy związane z harmonogramem czy zbieżnością z założonymi celami. Wiadomości z potencjalnymi sugestiami mogą być przesyłane do nas tylko wtedy, gdy rzeczywiście jest taka potrzeba.
- **Sugestie wydarzeń:** są zdarzenia, które trudno jest zaplanować z góry, a jednocześnie trzeba o nich pamiętać bądź zauważyć potrzebę ich utworzenia. Agent może więc zdjąć z nas konieczność pamiętania o przynajmniej części z nich. Sugestie mogą pojawiać się w oddzielnym kalendarzu i wrazie potrzeby być przeniesione do głównego. Ich tworzenie może być oparte zarówno o nasze notatki, jak i obserwowanie otoczenia.
- **Dodatkowy e-mail:** agent może posiadać swój własny adres e-mail na który mogą newslettery, systemowe powiadomienia czy przekierowane wątki np. w wyniku automatycznie nadanych etykiet sygnalizujących konieczność "wzbogacenia" wiadomości o dodatkowy kontekst. W celu bezpieczeństwa agent może posiadać możliwość wysłania wiadomości wyłącznie do nas oraz mieć dostęp "read only" do bazy wiedzy czy innych usług. Na nasz główny adres e-mail mogą trafiać jedynie najbardziej istotne informacje bądź ich zbiorcze wersje.
- **Aktywne katalogi:** koncepcja katalogu, którego zawartość uruchamia automatyzację, jest dość powszechna. Teraz jednak nawet nasz "cyfrowy ogród" z lekcji **S04E01** może posiadać miejsca (np. **concept / review / ready / published**) w których pojawiające się dokumenty mogą być transformowane w tle, a następnie przenoszone do kolejnych katalogów gdzie albo kolejny agent, albo człowiek będzie mógł się nimi zająć. Takie katalogi mogą też być automatycznie powiązane z systemem do zarządzania zadaniami.
- **Manager Schowka:** zawartość schowka jest prawdopodobnie ostatnią rzeczą, którą chcemy przesyłać na serwery dostawców. Jeśli jednak dysponujemy odpowiednim sprzętem i możemy uruchomić lokalne modele, to wówczas możemy obserwować go pod kątem zasobów wiedzy, wzmianek dotyczących potencjalnych wydarzeń, zadań czy przydatnych notatek (np. konfiguracji narzędzi).
- **Przegląd zadań:** podobnie jak w przypadku wydarzeń, mówimy tutaj nie tylko o zarządzaniu wpisami, ale także różnych formach prezentacji czy wykorzystania nawet bazowej wiedzy modelu do chociażby **zainicjowania** procesu kreatywnego. Możliwość zmniejszenia efektu "czystej kartki" bardzo ułatwi część zadań, a inne może wnieść na inny poziom, na przykład poprzez sugerowanie technik o których mogliśmy nie wiedzieć. Aby to jednak miało sens konieczne jest albo precyzyjne określenie kategorii treści które agent powinien komentować, albo połączenie go z bogatą wiedzą na temat naszych projektów.
- **Panel zarządzania:** znane z mediów społecznościowe "ściany" są u swoich podstaw dobrą koncepcją. Spersonalizowane aktualności obejmujące zarówno kontekst zewnętrzny (np. nowości branżowe) jak i wewnętrzny (np. obszary, które wymagają naszej uwagi). Podobne koncepcje funkcjonowały jeszcze przed popularyzacją LLM pod nazwą "Second Brain". Przeglądając materiały na ten temat można znaleźć mnóstwo inspiracji, które można połączyć bądź rozwinąć poprzez połączenie AI.
- **Nasłuchiwanie sygnału:** każdy z nas może inaczej zdefiniować czym jest "sygnał" informacyjny i zwykle można to dość dobrze opisać. Agenci monitorujący wybrane źródła (kanały youtube, profile X, newslettery, blogi) mogą informować nas o najbardziej istotnych wydarzeniach. Ranga wydarzenia może być uzależniona także od częstotliwości pojawiania się w informacjach w danym okresie czasu. Np. jeśli w ciągu miesiąca jakieś narzędzie było wielokrotnie omawiane, to prawdopodobnie my również powinniśmy zwrócić na nie uwagę.
- **Kontrola jakości:** treści trafiające do kolejki publikacji (np. newsletter) mogą być weryfikowane nie tylko przez ludzi, ale także agentów. Przykładowo wykrycie uszkodzonego bądź niewłaściwego linku w newsletterze to potencjalnie duży zysk. Podobną wartość może też dać sprawdzenie tekstu pod kątem poprawności językowej czy merytorycznej.
- **Tworzenie powiązań:** rozwijając bazy wiedzy z czasem może dochodzić do duplikacji informacji bądź potrzeby powiązania informacji ze sobą. Obecnie agenci raczej nie robią tego na tyle skutecznie, aby można było całkowicie oddać im ten proces. Ale generowanie sugestii naw podstawie najnowszych zmian w repozytorium ma bardzo duży sens.

**Przepływ danych:**

- **Szablony projektowe:** przy powtarzalnych projektach (np. organizacji wydarzeń) zwykle stosujemy frameworki obejmujące listy aktywności, szablony oraz wytyczne dotyczące ich realizacji. Wówczas przydzielanie zadań, dostępów i zasobów odbywa się częściowo automatycznie, na podstawie prostych integracji, na przykład z Todoist lub ClickUp. Uwzględnienie w tym procesie agentów AI nie tylko pozwoli uniknąć „efektu pustej kartki”, ale także monitorować statusy i dbać o utrzymanie standardów oraz założeń projektu.
- **Materiały promocyjne:** działania marketingowe oparte o tworzenie treści często obejmują posługiwanie się szablonami bądź konkretnym stylem graficznym. Wykorzystując wiedzę z lekcji **S01E04** możemy skorzystać z pomocy agentów przy opracowaniu propozycji grafik, okładek, wizualizacji, a nawet materiałów wideo. Propozycje mogą być dopasowane do treści oraz wymagań danej kampanii reklamowej.
- **Przekierowania:** zgłoszenia przesyłane przez użytkowników czy potencjalnych klientów mogą być natychmiast przekierowane do właściwych osób, co bezpośrednio przekłada się na wzrost jakości np. działu obsługi klienta czy skuteczności działu sprzedażowego. Integracje z formularzami, ankietami czy dedykowanymi skrzynkami e-mail połączone nawet z prostą "bazą wiedzy" (mogą to być nawet pojedyncze pliki) pozwoli LLM skutecznie ocenić zarówno miejsce przekierowania, jak i potencjalnie priorytet danego zgłoszenia.
- **Optymalizacja workflow:** agenci działający według procesu opisanego na przykład jako workflow mogą nie tylko skupiać się na jego wykonaniu, ale także na obserwacji jego skuteczności. Może to obejmować zarówno skanowanie logów aktywności, jak i bezpośredni odczyt rezultatów zapisanych w różnych aplikacjach. Na tej podstawie możemy otrzymywać rekomendacje usprawnień dotyczące naszych działań lub działań samych agentów. Takie podejście może obejmować na przykład działy sprzedaży, marketingu czy procesy produktowe.
- **Monitorowanie wskaźników:** produkty działające np. w modelach subskrypcyjnych wymagają dbania o wskaźniki takie jak MRR, Churn czy poziom satysfakcji klientów mierzony na przykład jako NPS. Ich wartości zwykle są powiązane z wieloma czynnikami, które częściowo można monitorować przez narzędzia analityczne, ale wiele z nich wynika bezpośrednio z feedbacku użytkowników (ankiet, wiadomości, spotkań, onboardingu itd), którego analiza jest bardzo czasochłonna. Agenci AI mogą pomóc przynajmniej w ustaleniu priorytetu i szybszym wychwyceniem na przykład powtarzających się błędów czy próśb o nowe funkcjonalności.
- **Raporty:** LLM raczej nie powinny odpowiadać za generowanie kompleksowych raportów na podstawie których podejmowane są ważne decyzje. Jednocześnie narzędzia wspierające proces, na przykład przez proste transformacje i klasyfikacje danych, których nie da się zrealizować poprzez kod, są bardzo pomocne. Podobnie też sama analiza raportów może być równolegle wykonana przez LLM, który z odpowiednim kontekstem, może zauważyć rzeczy, które umkną ludziom.

Wymienione powyżej przykłady pokazują przede wszystkim to, że **optymalizacja i automatyzacja procesów** w połączeniu z AI może przejść na kolejny poziom. Chodzi tu zarówno o możliwość robienia rzeczy, które wcześniej były trudne do automatyzacji (np. analizy otwartych odpowiedzi w ankietach), jak i zwiększenie **elastyczności** tych rozwiązań.

Jasne jest również, że wdrożenie nawet teoretycznie prostych usprawnień w praktyce nie jest takie oczywiste, zarówno z perspektywy technicznej, jak i biznesowej. Z drugiej strony mamy budowanie nawet prostych rozwiązań na własne potrzeby. Tutaj, z pomocą AI, możemy nawet generować aplikacje w Swift, Rust czy C#, które otworzą nam dostęp do natywnych funkcjonalności urządzeń, takich jak globalne skróty klawiszowe, aktualnie otwarta aplikacja czy kontrolowanie podłączonego sprzętu.

![Możliwości dostępu do statusu urządzeń](https://cloud.overment.com/2026-03-08/ai_devs_4_devices-a3f8cc93-8.png)

Agent, który ma dostęp do takich informacji, może dopasować swoje zachowanie i zdecydować na przykład o formie komunikacji z nami. Przykładowo, gdy pracujemy w wybranych programach, system może automatycznie włączać tryb DND (nie przeszkadzać), który blokuje powiadomienia. Ale gdy dzieje się coś istotnego, agent może skontaktować się z nami, na przykład przez SMS lub telefonicznie. Albo, gdy agent otrzyma od nas wiadomość, może uzyskać dostęp do lokalizacji i wykorzystać ją przy organizacji notatek w swojej pamięci. Takie scenariusze w kontekście prywatnym mają raczej luźny charakter ciekawostki, ale budowanie takiej logiki to dobre ćwiczenie w tworzeniu agentów zdolnych do dynamicznego dopasowywania się do zmieniających się warunków otoczenia.

## Zarządzenie zdarzeniami i komunikacją

Gdy wybierzemy scenariusze i zbudujemy narzędzia dla agentów, spotkamy wyzwanie związane z harmonogramem, zdarzeniami oraz systemem powiadomień. Bo nie sztuką jest ustawienie automatycznych akcji, które zaczną produkować mnóstwo treści której nikt nigdy nie przeczyta. Poza tym, gdy wcześniej mówiłem o wyzwaniach związanych ze zbyt małą elastycznością klasycznych automatyzacji, tak tutaj szybko spotkamy odwrotny problem. W skrajnych sytuacjach może on doprowadzić nawet do zapętlania się logiki bądź innych nieoczekiwanych rezultatów.

W przypadku kontekstowej pracy z AI, najlepiej jest zaprojektować system tak, aby problem związany z konfliktami **w ogóle nie występował**. Oznacza to, że agenci tak długo jak to możliwe powinni pracować niezależnie, skupiając się wyłącznie na konkretnych obszarach. Wówczas agent klasyfikujący zgłoszenia nie musi wiedzieć nic o agencie przeprowadzającym ich zbiorcze zestawienia. Podobnie też agent weryfikujący treści przed publikacją nie musi wiedzieć czegokolwiek o agentach opracowujących research dla tego dokumentu.

![Przykład izolacji dla agentów działających w tle](https://cloud.overment.com/2026-03-08/ai_devs_4_isolation-c3c45b45-b.png)

Brzmi to jak coś oczywistego, jednak takie nie jest. W praktyce bardzo naturalnie zaczynamy dążyć do rozbudowanych systemów wieloagentowych w których nakładające się zależności powstają samoistnie. Co gorsza, ich zauważenie nie zawsze jest oczywiste. Problemy mogą ujawniać się dopiero po dłuższym czasie, albo w wyniku nawarstwiających się informacji, albo rozbudowy systemu.

Obserwowanie działania systemu również może zostać w pewnym stopniu realizowane przez agentów. Bo tak jak w przypadku ewaluacji mówiliśmy o koncepcji LLM-as-a-judge, tak samo tutaj możemy uwzględnić cykliczne weryfikowanie przepływu informacji. Przykładowo jeśli system agentowy wysyła nam codziennie newsletter z aktualizacjami, które przestajemy czytać, to jaki jest sens utrzymywać ten proces? Albo w sytuacji gdy agenci zbierają dane z różnych źródeł spośród których część przestaje być dostępna, to wówczas powinny być one oznaczone oraz usunięte automatycznie albo po potwierdzeniu ze strony człowieka.

![Agenci obserwujący skuteczność działania systemu](https://cloud.overment.com/2026-03-08/ai_devs_self-observing-system-1c5aa317-0.png)

Naturalnie, pełna izolacja agentów nie zawsze będzie możliwa, ponieważ część zadań będzie wprost wymagała informacji lub akcji, do których dostęp mają inni agenci. W takim przypadku będziemy stosować rozwiązania, które omawialiśmy między innymi w lekcji **S02E04**. Po prostu, w przypadku systemów, które mają działać niemal w pełni autonomicznie, warto unikać niepotrzebnych komplikacji. Nie oznacza to jednak, że powinniśmy z tego całkowicie rezygnować. Po prostu w ich przypadku zaangażowanie ze strony człowieka bywa potrzebne zdecydowanie częściej, a jeśli system będzie musiał oczekiwać na manualne akcje bądź decyzje, jego efektywność zdecydowanie spadnie.

## Fabuła

![https://vimeo.com/1178448661](https://vimeo.com/1178448661)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze piąty!

Wygląda na to, że mamy nasze długo oczekiwane szczęśliwe zakończenie. Elektrownia działa, a turbina wiatrowa stabilizuje napięcie. Ha! Nawet chłodzenie udało nam się ogarnąć! Baterie zaczynają się ładować i idzie to szybciej niż przypuszczaliśmy. Technicy mówią, że potrzebujemy jeszcze może tygodnia albo trochę więcej, żeby wykonać skok w czasie.

Możnaby teraz usiąść, pooglądać Netflixa i odpocząć, ale jest jeszcze jedna sprawa, o której chciałem Ci powiedzieć.

Pamiętasz zbombardowane miasto? Domatowo. To w którym nikt nie przeżył. No właśnie... "nikt nie przeżył". Też tak myślałem. Tak wynikało z raportów systemu OKO. Jednak nasi technicy odebrali nietypowy sygnał. Na falach radiowych ludzki głos powtarza cyklicznie, co pewien czas jakieś słowa. Sygnał pochodzi z tego miasta i to nie jest nagranie, bo przechwyciliśmy go już kilka razy i za każdym razem brzmiał inaczej.

Tam ktoś jest. Może jedna osoba, może rodzina, a może... może jest ich więcej? Trzeba im pomóc.

Numerze piąty! Oddaję w Twoje ręce kierowanie misją ratunkową. Musimy dowiedzieć się, skąd nadano ten sygnał i wysłać tam naszych ludzi. Nie mamy wiele czasu ani też wiele zasobów, więc rozporządzaj jednym i drugim mądrze.

Więcej szczegółów przesyłam wraz z filmem. Przeczytaj instrukcje bardzo dokładnie, a na początek koniecznie zbadaj nagrania pozyskanych sygnałów.

## Zadanie praktyczne

Twoim zadaniem jest odnalezienie partyzanta ukrywającego się w ruinach Domatowa i przeprowadzenie sprawnej akcji ewakuacyjnej. Do dyspozycji masz transportery oraz żołnierzy zwiadowczych. Musisz tak rozegrać tę operację, aby odnaleźć człowieka, którego szukamy, nie wyczerpać punktów akcji i zdążyć wezwać helikopter zanim sytuacja wymknie się spod kontroli.

Po mieście możesz poruszać się zarówno transporterami, jak i pieszo. Transportery potrafią jeździć tylko po ulicach. Zanim wyślesz kogokolwiek w teren, przeanalizuj bardzo dokładnie układ terenu. Gdy tylko któryś ze zwiadowców znajdzie człowieka, wezwij śmigłowiec ratunkowy tak szybko, jak to tylko możliwe.

Nazwa zadania: **domatowo**

Odpowiedź wysyłasz do `/verify`

Przechwycony sygnał dźwiękowy:

> "Przeżyłem. Bomby zniszczyły miasto. Żołnierze tu byli, szukali surowców, zabrali ropę. Teraz jest pusto. Mam broń, jestem ranny. Ukryłem się w jednym z najwyższych bloków. Nie mam jedzenia. Pomocy."

Podgląd mapy miasta: https://hub.ag3nts.org/domatowo\_preview

Z API komunikujesz się zawsze przez `https://hub.ag3nts.org/verify` i wysyłasz JSON z polami `apikey`, `task` oraz `answer`.

Podstawowy format komunikacji wygląda tak:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "..."
  }
}
```

Na początek warto pobrać opis dostępnych akcji:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "help"
  }
}
```

### Co masz do dyspozycji

- maksymalnie 4 transportery
- maksymalnie 8 zwiadowców
- 300 punktów akcji na całą operację
- mapę 11x11 pól z oznaczeniami terenu

Najważniejsze typy akcji mają swoją cenę:

- utworzenie zwiadowcy: 5 punktów
- utworzenie transportera: 5 punktów opłaty bazowej oraz dodatkowo 5 punktów za każdego przewożonego zwiadowcę
- ruch zwiadowcy: 7 punktów za każde pole
- ruch transportera: 1 punkt za każde pole
- inspekcja pola: 1 punkt
- wysadzenie zwiadowców z transportera: 0 punktów

### Rozpoznanie terenu

Najpierw zapoznaj się z układem miasta. Możesz pobrać całą mapę:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "getMap"
  }
}
```

Możesz także wyświetlić podgląd mapy uwzględniający tylko konkretne jej elementy, podając je w opcjonalnej tablicy `symbols`.

### Tworzenie jednostek

Możesz utworzyć transporter z załogą zwiadowców - tutaj przykład 2-osobowej załogi:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "create",
    "type": "transporter",
    "passengers": 2
  }
}
```

Możesz też wysłać do miasta pojedynczego zwiadowcę:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "create",
    "type": "scout"
  }
}
```

### Ewakuacja

Helikopter można wezwać dopiero wtedy, gdy któryś zwiadowca odnajdzie człowieka. Finalne zgłoszenie wygląda tak:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "domatowo",
  "answer": {
    "action": "callHelicopter",
    "destination": "F6"
  }
}
```

W polu `destination` podajesz współrzędne miejsca, do którego ma przylecieć śmigłowiec. Musisz tam wskazać pole, na którym zwiadowca potwierdził obecność człowieka.

### Co musisz zrobić

- rozpoznaj mapę miasta i zaplanuj trasę tak, by nie przepalić punktów akcji
- utwórz odpowiednie jednostki i rozlokuj je na planszy
- wykorzystaj transportery do szybkiego dotarcia w kluczowe miejsca
- wysadzaj zwiadowców tam, gdzie dalsze sprawdzanie terenu wymaga działania pieszo
- przeszukuj kolejne pola akcją `inspect` i analizuj wyniki przez `getLogs`
- gdy odnajdziesz partyzanta, wezwij helikopter akcją `callHelicopter`

Jeśli poprawnie odnajdziesz ukrywającego się człowieka i zakończysz ewakuację, Centrala odeśle flagę.
