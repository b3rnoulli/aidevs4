---
title: S04E04 — Projektowanie własnej bazy wiedzy dla AI
space_id: 2476415
status: scheduled
published_at: '2026-04-02T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/0404-1774694246.png'
circle_post_id: 31103404
---
## Film do lekcji

![https://vimeo.com/1177416750](https://vimeo.com/1177416750)

Programowanie wspólnie z agentami jest tak wartościowe między innymi z powodu personalizacji wynikającej z dostępu do kodu źródłowego. Nasze zapytania, nawet jeśli są dość ogólne, potrafią poprowadzić AI przez kolejne pliki, odkrywając informacje potrzebne do udzielenia odpowiedzi bądź podjęcia działań.

Zdarzają się jednak sytuacje, gdy agent nie rozumie tego, co chcemy zrobić, ponieważ z samego kodu nie da się odczytać potrzebnego kontekstu. Aby zaadresować ten problem zaczęliśmy tworzyć **plany** i pliki **specyfikacji** czy powtarzalne **umiejętności** wpływające na ogólną skuteczność agenta.

Gdy wychodzimy poza kontekst programowania, odpowiednik kodu źródłowego przestaje istnieć. Wówczas użyteczność agenta opiera się na treści instrukcji systemowej i bieżącej interakcji. I teraz patrząc na to z tej perspektywy, oczywiste staje się to, dlaczego tak dużo rozmawiamy na temat tworzenia baz wiedzy, systemów plików oraz zarządzania kontekstem. Po prostu to w tym obszarze leży potencjalnie największa wartość, jaką może dać nam AI zarówno w kontekście prywatnym jak i przy projektowaniu systemów agentowych.

## Rola budowania i generowania prywatnej bazy wiedzy

Dotychczasowe lekcje prezentowały różne przykłady przetwarzania treści oraz mechanizmy związane z przepływem informacji, w dużym stopniu kontrolowanym przez modele językowe. Jest bardzo prawdopodobne, że większość z nich nie ma znaczenia dla nas wszystkich, a z drugiej strony możliwe, że nawet jeden z nich znacząco wpłynie na codzienność wybranych osób. Jest to więc bardzo **indywidualne**, dlatego zamiast pytać "jak budować bazę wiedzy?", zastanowimy się nad tym **"jak zbudować WŁASNĄ bazę wiedzy?"**. Oznacza to, że odpowiedź będziemy musieli znaleźć sami i w dodatku niekiedy dojdziemy do wniosku, że w ogóle jej nie potrzebujemy.

Przez kilka ostatnich lekcji na różne sposoby patrzyliśmy na nasze otoczenie, próbując odnaleźć połączenia pomiędzy możliwościami agentów z funkcjonalnościami narzędzi oraz procesami składającymi się na naszą codzienność, logikę aplikacji czy firmowe procesy. Tym razem skupimy się na tym pierwszym.

Gdy zastanowimy się nad tym, co agenci powinni wiedzieć na nasz temat, zauważymy, że lista jest długa, ale jednocześnie nie jest nieskończona. Bo nawet jeśli przeskanujemy historię przeglądarki, to z dużym prawdopodobieństwem lista regularnie odwiedzanych domen będzie dość skromna. To samo dotyczy listy powtarzalnych aktywności i narzędzi z których korzystamy, nawet jeśli początkowo wydaje nam się, że jest inaczej. Następnie jeśli z tych list wybierzemy obszary, w których AI może nam pomóc oraz odrzucimy te do których nie chcemy podłączać agentów, to uzyskamy dość sensowne pozycje na których powinniśmy się skupić. W takim odkrywaniu bardzo dobrym towarzyszem jest AI. Dobrze jest więc otworzyć ulubiony interfejs czatu i po prostu porozmawiać.

![Mapowanie obszarów w których AI faktycznie może nam się przydać](https://cloud.overment.com/2026-03-08/ai_devs_4_knowledge_scope-06622f93-8.png)

Takie ćwiczenie pozwoli rozbić iluzję sugerującą, że AI z łatwością pozwoli na zautomatyzowanie wszystkiego, co robimy. Z drugiej strony, nie mamy tu gwarancji, że wypracowana lista jest kompletna. Tym bardziej, że nowe możliwości ujawniają się przez praktykę, a "najlepsze pomysły nie są **powodem** wykonanej pracy, lecz jej **rezultatem**". Mówiąc inaczej, musimy budować, popełniać błędy i eksplorować, aby dotrzeć do rzeczy na które trudno jest wpaść nawet podczas najlepszych sesji planowania.

Przy kształtowaniu bazy wiedzy dobrze jest też wziąć pod uwagę obszary, których **nie chcemy** automatyzować, ale które warto w niej uwzględnić. Przykładowo sam zajmuje się tworzeniem treści i chcę aby tak pozostało. Ale jeśli AI może mieć dostęp do materiałów, które tworzę, to mogę mieć z tego wartość, ponieważ zamiast ręcznie przekazywać kontekst, mogę zwyczajnie się do niego odwołać. Poza tym, agenci będą mogli do niego dotrzeć bez mojego udziału.

Mając więc w głowie te dwa obszary, **nasz oraz agentowy**, możemy zastanowić się nad docelową strukturą, uwzględniając przy tym przestrzeń na rzeczy, którymi będziemy zajmować się my, przestrzeń, w której będą działać agenci, oraz przestrzeń na wiedzę, która będzie stanowić kontekst dla agentów, a jednocześnie wnosić wartość dla nas.

Tutaj ponownie bardzo wartościowa jest iteracyjna rozmowa z AI podczas której będziemy stopniowo kształtować strukturę naszej bazy wiedzy. Mogą się w niej znaleźć elementy takie jak:

- **Profil:** obejmuje informacje na nasz temat i jest to przestrzeń prowadzona przede wszystkim przez nas, ponieważ zawiera informacje na temat "osobistego systemu", który może obejmować określenie naszych wartości, kierunku, preferencji, nawyków, przemyśleń czy szeroko rozumianego rozwoju. Agenci mogą mieć dostęp do wybranych obszarów tej przestrzeni o ile zawarte tam informacje mogą być pomocne przy ich działaniu.
- **Świat:** zawiera informacje o ludziach, miejscach, narzędziach czy źródłach wiedzy. Tutaj też znajdują się informacje przydatne dla agentów, na przykład dotyczące sposobu organizacji pracy czy konfiguracji narzędzi.
- **Tworzenie:** to nasza przestrzeń robocza na pracę koncepcyjną, eksperymenty, informacje o projektach, a także publikowane przez nas materiały.
- **Operacje:** to przestrzeń przede wszystkim dla agentów. Są tu opisy procesów oraz dane gromadzone w trakcie wykonywania zadań, na przykład research'u.
- **System:** to miejsce na treści aktualizowane wyłącznie przez system, na przykład powiadomienia, statusy urządzeń czy metadane z otoczenia.

![Przykładowa struktura bazy wiedzy](https://cloud.overment.com/2026-03-08/ai_devs_4_knowledge_structure-41f3bac5-6.png)

Nawet jeśli zaplanujemy teraz podobną strukturę, to wcale nie oznacza, że musimy ją natychmiast wdrażać. Tym bardziej, że jest to praktycznie niemożliwe lub przynajmniej niepotrzebne. W zamian znacznie lepiej jest wybrać **jeden obszar** lub nawet **jedną aktywność** i ją zaadresować. Przykładem może być omawiany już spersonalizowany newsletter, podcast, czy proste automatyzacje związane z planowaniem dnia czy aktywnościami związanymi z naszym hobby. Bardzo dobrym pomysłem, jest wybranie na początek czegoś, co się nam po prostu podoba, a dopiero później tym, co jest faktycznie użyteczne.

Na organizację treści można też spojrzeć przez pryzmat znanych technik notowania, na przykład Zettelkasten czy PARA lub przynajmniej ich elementów. Przykładowo koncepcja "atomowych" notatek czy ich łączenia z pomocą linków może być bardzo użyteczna z perspektywy agentów i procesu wyszukiwania. Ale z drugiej strony, agenci mogą też zyskać na strukturze katalogów i jasnym podziale uprawnień czy odpowiedzialności. Także różne zasady mogą obowiązywać nas, a inne agentów. Tym bardziej, że dla AI notatka może zawierać tekst, ale też fragmenty kodu bądź skrypty.

Poniżej widzimy przykładową strukturę notatki w której początkowy fragment (frontmatter) zawiera zarówno ustawienia na potrzeby publikacji na stronie www, ale też bieżący status, tagi czy kontrolę uprawnień i przypisanie odpowiedzialności a nawet "prompt".

![Przykładowa struktura notatki](https://cloud.overment.com/2026-03-08/ai_devs_4_knowledge_contents-850ed061-0.png)

Jeśli dobrze przemyślimy sobie strukturę i/lub zasady tworzenia notatek, to wspólnie z AI możemy ją rozwijać znacznie łatwiej, niż gdybyśmy musieli robić to samodzielnie. Dodatkowo użyteczność tych notatek będzie nieporównywalnie większa, jeśli agenci będą mogli się nimi posługiwać w rzeczywistych procesach.

I teraz co ważne, na tym etapie możemy nawet w ogóle nie pisać kodu, ponieważ katalog z bazą wiedzy możemy podłączyć bezpośrednio do Claude Code i wspólnie z agentem ukształtować pierwsze procesy, notatki czy szablony. Ten sam agent może później zająć się ich realizacją, ponieważ na tym etapie bez problemu podłączymy serwery MCP czy narzędzia CLI. Dopiero później możemy pomyśleć o uruchomieniu tego procesu na zdalnym serwerze, połączeniu interfejsów czy w ogóle napisania całej logiki agenta od podstaw.

## Zalety i ograniczenia formatu markdown

Format Markdown jest z nami od dawna i zwykle utożsamiany jest z kontekstem technicznym, prawdopodobnie ze względu na jego popularyzację przez Github mniej więcej w 2009 roku. W 2024 pojawił się nawet w Google Docs, co sugeruje także obecność w obszarach biznesowych i jest to uzasadnione, ponieważ Markdown to format którym bardzo naturalnie posługuje się AI.

Z programistycznego punktu widzenia Markdown to zwykły plik tekstowy, więc możemy go swobodnie transformować, przeszukiwać albo po prostu tworzyć. Fakt, że potrafią to również modele językowe sprawia oraz że mówimy o nim tak dużo w kontekście agentów i teraz także baz wiedzy sugeruje, że powinniśmy korzystać z niego przy każdej okazji.

Jeśli jednak pracujemy w zespole, gdzie często konieczna jest praca wielu osób na jednym pliku jednocześnie, czy współdzielenia dokumentów z różnymi poziomami uprawnień, to wówczas Notion bądź Google Docs będą zdecydowanie lepszym wyborem. I choć w nich również pojawia się format Markdown, tak jego wsparcie jest raczej ograniczone. Natomiast wartość którą dają wspomniane funkcjonalności będzie niemal zawsze wyższa niż elastyczność pliku tekstowego. Choć w teorii istnieje możliwość konwertowania Markdown do formatu Notion lub odwrotnie, w praktyce sprawdza się to bardzo przeciętnie, ponieważ większość informacji i tak jest tracona na etapie konwersji. Znacznie mądrzej jest więc podjąć decyzję, w których obszarach stosować Notion lub Docs, a w których pliki .md.

![Wybór Markdown i innych rozwiązań](https://cloud.overment.com/2026-03-09/ai_devs_4_markdown_vs-8af9d115-9.png)

Wzbogacanie formatu Markdown nie jest też niemożliwe, czego przykładem może być projekt [with-md](https://github.com/emotion-machine-org/with-md) w przypadku którego agenci mogą mieć nawet dostęp do dodatkowych informacji na temat treści. Na tym etapie jest to jednak jedynie koncepcja i narzędzie stworzone [na własne potrzeby](https://x.com/egeozin/status/2026344803097878939). Niewykluczone jednak, że pomysły takie jak ten prędzej czy później przerodzą się w pełnoprawne produkty czy nawet coś więcej.

W plikach markdown często będzie pojawiać się potrzeba osadzania obrazów. Edytory tekstowe niemal zawsze wspierają taką możliwość, ale wówczas pliki są zapisywane lokalnie, a w praktyce jest to bardzo ograniczające. Znacznie lepiej jest zadbać o to, aby obrazy były osadzane w treści w formie linków. Wówczas agent może się nimi posługiwać, co widzieliśmy w kontekście obsługi narzędzi w lekcji **S01E04**. Podobnie też agent może cytować takie linki w swoich wypowiedziach, co w przypadku plików lokalnych może być utrudnione bądź niemożliwe.

![Zdalne obrazy w treści markdown](https://cloud.overment.com/2026-03-09/ai_devs_4_external_links_practices-32d5ae17-5.png)

Jak widać powyżej, otwarte linki są niemal niezbędne, a jednocześnie dość trudno je kontrolować zarówno pod kątem uprawnień jak i terminu ważności. Dobrze jest więc ustalić zasady oraz mieć wgląd w listę dostępnych zasobów, a także ewentualną możliwość przywrócenia dostępności.

## Różnice pomiędzy bazą wiedzy a pamięcią długoterminową

W lekcji **S02E03** rozmawialiśmy na temat pamięci długoterminowej oraz zewnętrznych dokumentów, a także koncepcji agentów "uczących się" nowych informacji zamiast zwykłego indeksowania. Teraz mówimy o sytuacji w której pamięć długoterminowa i baza wiedzy stają się niemal tym samym, ponieważ funkcjonują w tej samej przestrzeni. Poza tym, mamy do czynienia z dynamiczną treścią tworzoną zarówno przez człowieka, jak i przez AI.

Gdy rozwijamy bazę wiedzy na potrzeby prywatne bądź firmowe, to tworzymy treści w sposób bardzo naturalny, pomijając rzeczy, które już wiemy bądź które łatwo można wywnioskować z otoczenia. Jednak z perspektywy agenta poruszającego się po takiej bazie wiedzy, nie zawsze jest to oczywiste, a luki wiedzy mają negatywny wpływ na jego skuteczność. Przykładowo:

- nazwy projektów czy imiona osób naturalnie sugerują nam ich kontekst. Wiemy więc gdzie znajdziemy informacje na ich temat oraz kiedy mogą być nam potrzebne, ale agent nie będzie w stanie do nich dotrzeć.
- linki pojawiające się w treści, których ścieżki oraz opis w żaden sposób nie sugerują ich zawartości (np. w przypadku skrócenia) są praktycznie "niewidoczne" dla agenta
- referencje do zdarzeń bez wyraźnego powiązania, na przykład "ostatnia rozmowa" czy "w poprzedniej wersji" uniemożliwiają dalszą eksplorację i zrozumienie kontekstu. Tutaj wystarczy nawet link do powiązanej notatki, aby zaadresować ten problem.
- unikanie powtórzeń przy powiązaniach notatek może utrudnić agentowi dotarcie do treści, gdy w trakcie przeszukiwania wczyta on jedynie fragment dokumentu, w którym powiązanie nie będzie istnieć
- zmiany w dokumentach nadpisują istniejące informacje, więc agent traci do nich dostęp. Jeśli tworzone są nowe wersje dokumentów, to agent musi wiedzieć która z nich jest najnowsza oraz jak do niej dotrzeć.

![Problemy z niewystarczającym kontekstem dla agentów](https://cloud.overment.com/2026-03-09/ai_devs_4_note_context-fb70430d-9.png)

Mówiąc więc wprost: **notatki muszą być tworzone tak, jakby osoba, która je czyta nie posiadała żadnego dodatkowego kontekstu.** A to całkowicie zmienia sposób w jaki rozwijamy bazę wiedzy. Jednocześnie dość jasno sugeruje też, dlaczego agenci mają dość duży problem w nawigacji gdy zostają wprost połączeni z zewnętrznymi dokumentami.

## Korzystanie z modeli przy edycji notatek

Gdy generujemy kod, którego w ogóle nie czytamy, a większość decyzji podejmuje LLM, możemy bardzo szybko wdrażać kolejne funkcjonalności. Jednak równie szybko tracimy orientację w tym, co się dzieje, i gdy coś idzie nie tak, trudno jest nam to naprawić. W przypadku baz wiedzy tworzonych przez AI jest jeszcze gorzej, ponieważ gubimy cały sens jej budowania. Tutaj ewentualnie wyjątek stanowi sytuacja w której świadomie podejmujemy decyzję, że rozwój leży niemal w całości po stronie agentów, ale wówczas odbywa się to według naszych zasad bądź przynajmniej w określonym przez nas celu.

Nie oznacza to, że musimy całkowicie zrezygnować z AI i nie chodzi tylko o katalogi dedykowane agentom, ale także obszary w których treści pochodzą bezpośrednio od nas. Wystarczy postawić wyraźną granicę, której agent nie może przekroczyć, na przykład:

- **Transformacja:** gdy pozostajemy źródłem informacji, a LLM odpowiada jedynie za jej formatowanie, delikatną korektę czy po prostu przepisanie (z obrazu bądź audio), tak trudno jest mówić o utracie kontroli nad bazą wiedzy. Wprost przeciwnie. Takie zaangażowanie AI może sprawić, że w ogóle będziemy rozwijać swoją cyfrową przestrzeń.
- **Szablony:** utrzymanie struktury notatki, którą omówiliśmy przed chwilą, nie jest oczywiste. Jeżeli utworzymy szablony na przykład w sekcji **system**, to agent będzie mógł je wykorzystać zgodnie z naszą prośbą, zdejmując z nas ten obowiązek.
- **Organizacja:** po dodaniu notatki agent może sprawdzić czy znajduje się ona we właściwym miejscu i jeśli nie, jedynie zasugerować i uzasadnić potencjalną zmianę.
- **Linkowanie:** bez względu na to czy zdecydujemy się na pracę w Obsidian, czy nie, linkowanie notatek jest szczególnie ważne. Na pewnym etapie staje się to dość skomplikowane, więc jest to przestrzeń na zastosowanie AI. Warto tylko utworzyć notatkę wyjaśniającą zasady według których mają powstać linki, bądź oprzeć się o sugestie ze strony modelu.
- **Walidacja:** mając zasady dotyczące linkowania, struktur czy organizacji, możemy skorzystać z AI do weryfikacji każdego z tych aspektów. Pozwoli nam to utrzymać standardy oraz zachować wysoką dyscyplinę organizacji wiedzy.
- **Komentowanie:** AI nie powinno tworzyć treści naszych notatek, ale możemy stworzyć przestrzeń na ich komentowanie.
- **Indeksowanie:** w kontekście budowania baz wiedzy często pojawiają się koncepcje **MoC** czyli Map of Content. Są to notatki pełniące rolę indeksu bądź wspomnianej "mapy" dla wybranych obszarów treści. Takie notatki mogą być generowane programistycznie, ale agent również może być zaangażowany w ich tworzenie bądź weryfikację.
- **Audytowanie:** nie wszystkie pomyłki i braki można zauważyć od razu, więc zaangażowanie agenta w dodatkową weryfikację struktury obejmującą na przykład łączenie notatek bądź archiwizowanie tych, które zaczynają stanowić szum, ma duży sens.

![Balans zaangażowania pomiędzy AI a człowiekiem](https://cloud.overment.com/2026-03-09/ai_devs_4_knowledge_balance-5eaa265d-b.png)

Kolejny wniosek, jaki się tutaj nasuwa jest prosty: **my odpowiadamy za treść oraz główne zasady, a AI za jej organizację**. Oczywiście balans zaangażowania jest uzależniony od obszaru bazy wiedzy oraz naszych potrzeb. Jednak taki podział można uznać za dobry punkt startowy.

## Połączenie z agentami

Przykład **04\_04\_system** zawiera minimalistyczną logikę systemu wieloagentowego, którego główną część stanowi baza wiedzy w formacie markdown. Jej struktura odzwierciedla to, co do tej pory powiedzieliśmy na temat możliwości organizacji notatek. Znajdziemy więc w niej katalogi **Me / World / Craft / Ops / System.**

Na początek warto zajrzeć do katalogu **workspace/system/templates** w którym znajdują się **"szablony"** notatek dla poszczególnych kategorii - profili osób, opisów miejsc, zdarzeń, narzędzi, zasobów itd. Zatem gdy poprosimy agenta o zapisanie informacji, to zamiast samodzielnie decydować o jej strukturze i lokalizacji, skorzysta z dostępnych szablonów oraz zasad.

![Szablony notatek](https://cloud.overment.com/2026-03-10/ai_devs_4_blueprints-c41d89ad-3.png)

Przykład działania tych szablonów można zobaczyć uruchamiając polecenie **npm run lesson19:examples -- 3** (flaga na końcu ograniczy liczbę przykładów). Przy ich wykonywaniu agent w pierwszej kolejności **rozejrzy się po strukturze** poprzez sprawdzenie notatki zawierającej "mapę treści", a następnie notatki odpowiedniego **szablonu**. Na tej podstawie podejmie decyzję o jej strukturze i utworzy nowy wpis **bądź doda informację do istniejącego!**

![Autonomiczne zarządzanie notatkami](https://cloud.overment.com/2026-03-10/ai_devs_4_decision-6a8aed19-e.png)

Gdy spojrzymy na listę powyższych kroków, zobaczymy, że na jedną notatkę przypada nawet kilkanaście zapytań do LLM. Dlatego im większa będzie nasza baza wiedzy, tym bardziej skorzystamy z możliwości AI, ponieważ wartość wynikająca ze spójności struktury poszczególnych notatek będzie ogromna. Poza tym, agent wyposażony w taką wiedzę nie tylko skutecznie zapisuje informacje, ale **nawiguje po nich**, a to otwiera nam dużą przestrzeń na autonomiczne działania.

I tutaj do gry wchodzi koncepcja o której już mówiliśmy na przykład w lekcji **S02E03**. Otóż w katalogu **workspace/ops** możemy opisać procesy realizowane wyłącznie przez agentów, uwzględniając przy tym współpracę pomiędzy nimi. I tak w katalogu **workspace/ops/daily-news** znajdziemy cztery pliki: **research | assemble | deliver** oraz **info.md**.

Główny agent może otrzymać polecenie "Wykonaj proces daily-news", które będzie wysłane do niego automatycznie każdego dnia. Dokument ten zawiera instrukcję opracowania aktualizacji na dany dzień, z uwzględnieniem podziału zadań **pomiędzy agentami.** Każdy z nich otrzymuje więc dalsze polecenie z prośbą o zapoznanie się z instrukcją dotyczącą ich zakresu oraz podjęcie opisanych tam działań. Proces zwizualizowany jest poniżej.

![Delegowanie zadań w powtarzalnych procesach](https://cloud.overment.com/2026-03-10/ai_devs_4_daily_news_delegation-d2fe03c4-7.png)

Czyli raz jeszcze: mówimy tutaj o zaledwie **czterech prostych plikach tekstowych**, które przekładają się na **powtarzalny proces** obejmujący w tym przypadku monitorowanie wybranych stron Internetowych.

![Instrukcje dla aktywności w powtarzalnych procesach](https://cloud.overment.com/2026-03-10/ai-devs_4_daily_news_process-8c77ab1b-6.png)

Powyższy przykład powinien wyglądać znajomo, ponieważ podobne rzeczy tworzyliśmy już w lekcji **S02E03**, **S02E04**, **S04E01**, **S04E02** oraz **S04E03**. Teraz jednak mówimy o połączeniu wszystkich tych koncepcji, czyli: bazy wiedzy, systemów wieloagentowych, agentów działających w tle, bezpośredniej pracy z agentami, systemu plików oraz koncepcji cyfrowego ogrodu. Co więcej, możemy wyjść z tym znacznie dalej, opisując kolejne procesy i podłączając kolejne narzędzia.

## Fabuła

![https://vimeo.com/1178447791](https://vimeo.com/1178447791)

## Transkrypcja filmu z Fabułą

**Azazel**

Numerze piąty!

Dzięki Twojej pomocy ocaliliśmy człowieka! Ma na imię Natan. Jego stan jest stabilny, ale musi trochę odpocząć. Gdy tylko wydobrzeje, będzie pomagał nam w pracy przy elektrowni.

Nie mogłem znaleźć jego danych na liście ocalałych. Wygląda na to, że to jeden z ludzi żyjących poza systemem. Rozmawialiśmy z nim długo. Można mu zaufać.

Natan opowiedział nam, jak wyglądało życie w mieście przed bombardowaniem. Główny problem, z którym się borykali, to brak jedzenia. Z wodą akurat nie było problemu, ponieważ udało im się wykopać studnie, ale jedzenie od zawsze było problemem.

Do tej pory stosowali handel wymienny z innymi miastami, ale odkąd Zygfryd uruchomił system "OKO", który nasłuchiwał komunikatów internetowych i radiowych, a także który rejestrował wszelki ruch, handel nie był już tak prosty jak niegdyś, a wysyłanie posłańców na pustynie przypominało misję samobójczą.

Dostaliśmy od Natana jego notatki. On sam ogarniał temat handlu, więc ma informacje na temat osób odpowiedzialnych za handel wymienny z innych miast. Widziałem tam też zapiski dotyczące oferowanych towarów, zamówień, transakcji.

To wszystko jest bardzo chaotyczne i chyba niezbyt kompletne, ale wierzę, że pomożesz nam ułożyć to w jednolitą strukturę.

Chodzi nam po głowie pewien pomysł, jak można tym wszystkim miastom pomóc.

Oczywiście nie mamy tyle jedzenia, aby nakarmić wszystkich potrzebujących, ale możemy zastosować pewną sztuczkę... aleee! o tym opowiem Ci jutro. Na dziś potrzebuję tylko poukładać te dane.

To co robimy zdecydowanie nie spodoba się Zygfrydowi, ale chyba właśnie o to chodzi - prawda?

W notatce do tego nagrania masz więcej szczegółów. Postaraj się ogarnąć te notatki jeszcze dziś!

## Zadanie praktyczne

Twoje zadanie polega na logicznym uporządkowaniu notatek Natana w naszym wirtualnym file systemie. Potrzebujemy dowiedzieć się, które miasta brały udział w handlu, jakie osoby odpowiadały za ten handel w konkretnych miastach oraz które towary były przez kogo sprzedawane.

Dokładny opis potrzebnej nam struktury znajdziesz poniżej.

Nazwa zadania to: **filesystem**

Wszystkie operacje wykonujesz przez /verify/

Link do notatek Natana: https://hub.ag3nts.org/dane/natan\_notes.zip

Podgląd utworzonego systemu plików: https://hub.ag3nts.org/filesystem\_preview.html

Na początek warto wywołać przez API funkcję 'help':

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "filesystem",
  "answer": {
    "action": "help"
  }
}
```

W udostępnionym API znajdziesz funkcje do tworzenia plików i katalogów, usuwania ich, listowania katalogów oraz dwie funkcje specjalne:

- **reset** - czyści cały filesystem (usuwa wszystkie pliki)
- **done** - wysyła utworzoną strukturę danych do Centrali w celu weryfikacji zadania.

### Komunikacja z API

Możesz wysyłać do API pojedyncze instrukcje lub wykonać wiele operacji hurtowo.

Przykładowo, utworzenie 2 plików może wyglądać tak:

Zapytanie 1:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "filesystem",
  "answer": {
    "action": "createFile",
    "path": "/plik1",
    "content": "Test1"
  }
}
```

Zapytanie 2:

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "filesystem",
  "answer": {
    "action": "createFile",
    "path": "/plik2",
    "content": "Test2"
  }
}
```

Możesz także wykorzystać **batch\_mode** i wysłać wszystko razem - dzięki tej funkcji, możliwe jest utworzenie całego filesystemu w jednym requeście.

```json
{
  "apikey": "tutaj-twoj-klucz",
  "task": "filesystem",
  "answer": [
    {
      "action": "createFile",
      "path": "/plik1",
      "content": "Test1"
    },
    {
      "action": "createFile",
      "path": "/plik2",
      "content": "Test2"
    }
  ]
}
```

### Oto nasze wymagania

- Potrzebujemy trzech katalogów: `/miasta`, `/osoby` oraz `/towary`
- W katalogu `/miasta` mają znaleźć się pliki o nazwach (w mianowniku) takich jak miasta opisywane przez Natana. W środku tych plików powinna być struktura JSON z towarami, jakie potrzebuje to miasto i ile tego potrzebuje (bez jednostek).
- W katalogu `/osoby` powinny być pliki z notatkami na temat osób, które odpowiadają za handel w miastach. Każdy plik powinien zawierać imię i nazwisko jednej osoby i link (w formacie markdown) do miasta, którym ta osoba zarządza.
- Nazwa pliku w `/osoby` nie ma znaczenia, ale jeśli nazwiesz plik tak jak dana osoba (z podkreśleniem zamiast spacji), a w środku dasz wymagany link, to system też rozpozna, o co chodzi.
- W katalogu `/towary/` mają znajdować się pliki określające, które przedmioty są wystawione na sprzedaż. We wnętrzu każdego pliku powinien znajdować się link do miasta, które oferuje ten towar. Nazwa towaru to mianownik w liczbie pojedynczej, więc "koparka", a nie "koparki"

### Oczekiwany filesystem

Efektem Twojej pracy powinny być takie trzy katalogi wypełnione plikami.

> **Uwaga**: w nazwach plików nie używamy polskich znaków. Podobnie w tekstach w JSON.
