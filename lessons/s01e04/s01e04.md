---
title: Wsparcie multimodalności oraz załączników
space_id: 2476415
status: scheduled
published_at: '2026-03-12T04:00:00Z'
is_comments_enabled: true
is_liking_enabled: true
skip_notifications: false
cover_image: 'https://cloud.overment.com/multimodal-world-1772882609.png'
circle_post_id: 30408463
---
Multimodalność (tekst, obraz, audio, wideo) według niektórych jest dziś standardem. Problem w tym, że nie jest. A przynajmniej nie w pełni.

Na rynku istnieje wiele modeli wyspecjalizowanych w przetwarzaniu obrazu, dźwięku oraz wideo. Jednak tylko nieliczne obsługują wszystkie formaty jednocześnie, a jeszcze rzadziej dostęp do nich oferowany jest z poziomu API. W chwili pisania tych słów najbliżej tego celu znajdują się Gemini 3 oraz Interactions API, gdzie ten sam endpoint i jeden model dają nam niemal wszystko. Ale w praktyce i tak będzie nas interesowało eksplorowanie wielu opcji i wybór nie tej, która jest najwygodniejsza, lecz najlepiej dopasowana do problemu, który rozwiązujemy.

## Przegląd najnowszych modeli dla obrazu, audio i wideo

Benchmarki w ostatnich latach pokazały, że ich skuteczność jest bardzo ograniczona w faktycznej ocenie możliwości modeli. Pomimo tego relatywnie dobrze pokazują trendy, ponieważ faktycznie najlepsze modele trafiają na podium lub Top10.

Całkiem dobrym miejscem z rankingami modeli jest strona [Artificial Analysis](https://artificialanalysis.ai/image/leaderboard/text-to-image). Znajdziemy na niej chociażby porównanie aktualnych LLM z których GPT-5.2, Claude Opus 4.5 i Gemini 3 Pro znajdują się na podium. To który z nich rzeczywiście zasługuje na Top1 to kwestia dość subiektywna, jednak nadal trend jest poprawny.

![](https://cloud.overment.com/2026-01-30/ai_devs_4_models-af74cc17-f.png)

Analogicznie wygląda to w przypadku modeli do generowania obrazu, gdzie Top3 to Gemini 3 (Nano Banana), GPT-Image-1 oraz Flux. A w przypadku wideo obecnie na szczycie mamy Grok 4 oraz Kling 2.5. Poza skutecznością modelu będzie interesować nas jeszcze **szybkość działania** oraz **cena**, a niekiedy także poziom prywatności API bądź możliwość uruchomienia modelu lokalnie (np. Qwen).

Ranking modeli w każdej kategorii bardzo szybko się zmienia i jak mówiłem w S01E01, dobrze jest wypracować sobie prosty proces pozostawania "na bieżąco". Tymczasem przyjrzyjmy się bliżej detalom związanym z ich zastosowaniem w logice agentów.

## Przetwarzanie załączników przy wsparciu narzędzi

Podczas interakcji z agentem AI możemy dodawać różnego rodzaju **załączniki**, np. zdjęcia. Dokumenty zwykle będą wykorzystywane przy posługiwaniu się narzędziami, np. edycją obrazu, usunięciem tła czy osadzeniu w dokumencie bądź wiadomości e-mail. Niestety pojawiają się tu pewne pułapki.

Zacznijmy od zrozumienia sposobu w jaki API umożliwia nam przesyłanie obrazów na potrzeby analizy (vision) bądź generowania/edycji (image generation). Poniżej widzimy interakcję w której **zdjęcie zostaje dołączone do wiadomości użytkownika** i trafia do modelu razem z treścią pytania. Następnie jeśli użytkownik zada kolejne pytanie w tym wątku, obraz **ponownie zostaje przesłany do modelu** (technicznie rzecz biorąc nadal znajduje się w pierwszej wiadomości, ale podkreśliłem jego obecność na wizualizacji).

![Przykład interakcji z LLM z analizą obrazu](https://cloud.overment.com/2026-01-30/ai_devs_4_images-ff4c6b12-c.png)

Obrazy przesyłane są w formie **URL** bądź **Base64**, jednak w obu przypadkach trafiają one do modelu w takiej samej formie i LLM **nie jest w stanie "zobaczyć" adresu URL**, co stanowi pewne wyzwanie, bo agent nie może odwołać się do pliku na potrzeby narzędzi bądź przekazywania go innym agentom.

Ten sam problem dotyczy wszystkich innych form załączników, w tym także plików audio, wideo czy dokumentów tekstowych. Co więcej, żadne z dostępnych API wydaje się nie adresować tego problemu wprost. Nie spotkałem się też z żadnymi materiałami o **dobrych praktykach** w takiej sytuacji, ale podzielę się podejściem które sprawdza się w moich systemach. Polega ono na przekazaniu w wiadomości użytkownika nie tylko treści pytania oraz pliku, ale także dodatkowego elementu zawierającego odnośnik który agent może wykorzystać. Obrazuje to poniższy schemat:

![Przykład informowania agenta o dostępnych załącznikach](https://cloud.overment.com/2026-01-31/ai_devs_4_media-8a380b30-f.png)

Widzimy na nim:

- Wpis w instrukcji systemowej agenta **wyjaśniający jak odwoływać się do plików**.
- Wiadomość użytkownika faktycznie zawiera **tekst, obraz oraz dodatkowy element z tagiem "media"** (wybór tego tagu jest raczej losowy, sam w sobie nic nie oznacza, ale sugeruje jakąś formę załącznika)
- Agent poproszony o **usunięcie tła ze zdjęcia** musi wywołać odpowiednie narzędzie **przekazując odnośnik do pliku**.
- Reszta działa tak samo - agent otrzymuje rezultat działania narzędzia i kontynuuje pracę.

Z technicznego punktu widzenia odnośnik do pliku zostaje **programistycznie** zamieniony na format Base64 lub udostępniony jako publiczny adres URL. W praktyce oznacza to, że agent może swobodnie przekazywać dokumenty w obrębie całego systemu.

## Dopasowanie procesu rozpoznawania obrazu z LLM

Rozpoznawanie obrazów może wykraczać poza bazową wiedzę modelu ponieważ cechy obiektów oraz relacje między nimi mogą zostać dopasowane do zewnętrznych informacji. Wówczas nawet model bez dedykowanego treningu może skutecznie opisywać zdjęcia, na przykład produktów.

Takie zadanie można zrealizować na dwa sposoby: poprzez **workflow** lub **agenta**. Gdy klasyfikacja jest prosta, a zestaw danych w postaci obrazów oraz zasady klasyfikacji nie są dynamiczne, wówczas **workflow** powinien wystarczyć. W przeciwnym razie konieczne jest zbudowanie **agenta** i właśnie tym się zajmiemy.

Zacznijmy od zrozumienia problemu oraz określenia jego zakresu:

- mamy zbiór obrazów w postaci plików jpg / png zapisanych na dysku
- posiadamy informacje na ich temat w postaci opisów markdown
- nie mamy pewności czy posiadamy wszystkie możliwe opisy
- opisy mogą zmieniać się w czasie, wpływając na przyszłe klasyfikacje
- opisy mogą być na tyle rozbudowane, że trudno będzie je wczytać z góry
- niektóre obrazy mogą być nieczytelne, bądź niepowiązane z opisami

Fakt, że mówimy tutaj o dynamicznych danych sprawia, że potrzebujemy tutaj agenta AI. Agent **nie może** posiadać instrukcji **prowadzących go przez sztywny proces** (a jeśli może, to powinien być **workflow**) ani instrukcji **uzależnionych od zestawu danych**, aczkolwiek mogą one dotyczyć **klasy problemów**. W zamian, instrukcja agenta powinna:

- przedstawiać cel postawiony przed agentem
- limity i ograniczenia, których agent **powinien** przestrzegać
- uniwersalne zasady, schematy i wzorce, które mogą być przydatne

Jest to znacząca różnica pomiędzy tym, co znamy z klasycznego programowania. Tutaj **znaczną część aktywności przenosimy na model**, stwarzając agentowi **przestrzeń** do działania. Nawet bez wczytywania się w detale poniższego schematu od razu widać różnicę pomiędzy tymi dwoma podejściami.

![Porównanie instrukcji agenta - specyficzna vs zgeneralizowana](https://cloud.overment.com/2026-01-31/ai_devs_4_workflow_vs_agent_prompt-e6d3474f-7.png)

W przykładzie **[01\_04\_image\_recognition](https://github.com/i-am-alice/4th-devs/tree/main/01_04_image_recognition)** znajduje się agent wyposażony w dwa rodzaje narzędzi: **dostęp do systemu plików przez Files MCP** oraz **dedykowane narzędzie do analizy obrazu**. Po uruchomieniu skryptu agent rozpocznie przeszukiwania katalogu **knowledge** oraz **image**, a następnie zorganizuje pliki poprzez utworzenie kopii obrazów w katalogu **image/organized**.

Skuteczność tego agenta **nie będzie wynosić 100%**, ale w zdecydowanej większości prób powinien poprawnie klasyfikować obrazy i ewentualnie umieszczać w katalogu **unclassified** te, co do których nie jest pewien. To właśnie tam trafią też wszystkie pliki, które nie będą pasować do naszego zestawu danych.

Ogólne zasady oraz mechanika tego agenta mogą zostać wykorzystane do klasyfikacji niemal dowolnych zestawów obrazów, o ile będziemy posiadać dokumenty z informacjami, które pomogą agentowi w ich organizacji. Jest to przykład **wysokiej elastyczności agentów AI** dostarczonej kosztem zwiększonego ryzyka błędów (na które i tak w dość dużym stopniu możemy się zabezpieczyć). Fakt, że nie możemy mówić tu o 100% skuteczności jasno sugeruje konieczność zaangażowania człowieka w proces weryfikacji rezultatów. Natomiast weryfikacja niemal zawsze jest łatwiejsza niż wykonanie pracy w całości.

## Iteracyjne generowanie oraz edycja obrazów

Jeszcze rok temu modele do generowania obrazów miały bardzo niską skuteczność w podążaniu za instrukcjami, a różnego rodzaju artefakty były ich niemal nieodłącznym elementem. Wymagało to podejmowania wielu prób podczas generowania, bądź nawet nanoszenia ręcznych poprawek. Pomocne były (wciąż bardzo użyteczne) narzędzia takie jak [ComfyUI](https://www.comfy.org/) czy [Weavy](https://www.weavy.ai/). Obecnie do codziennych zadań i nawet produkcyjnego zastosowania mogą wystarczyć nam komercyjne modele do generowania obrazów, np. Gemini 3.

Generowanie i edycja obrazów przez agenta AI jest możliwa, ale jednocześnie nieoczywista. Bo choć do modelu możemy przesłać obrazy, ale tylko te pochodzące od użytkownika. A jeśli agent wygeneruje obraz, to nie jest w stanie fizycznie go zobaczyć. Co więcej, nawet jeśli byłby w stanie to zrobić, to nie możemy mieć pewności, że model zauważy wszystkie problemy dotyczące obrazu. Aczkolwiek jeszcze rok temu można było mówić o tym, że "[VLMy są niewidome](https://vlmsareblind.github.io/)", ale dziś niemal każde z prezentowanych w tej publikacji zadań jest rozwiązywane przez najnowsze modele. Nie oznacza to, że modele nie mają problemu, np. z precyzją, dostrzeganiem detali czy poprawnym rozpoznawaniem kolorów. Jednocześnie zdolności te, widocznie się rozwijają w każdej kolejnej wersji modeli.

Agenci AI mogą tworzyć obrazy nie tylko poprzez modele, ale także przez pisanie kodu (np. tworzenie wykresu). Tutaj również sytuacja jest podobna, bo obraz **jest wynikiem działania jednego z narzędzi** i natywnie nie mamy możliwości przesłania go automatycznie do modelu. Możemy jednak wyposażyć agenta w **narzędzie do analizy obrazu**, na przykład prosta możliwość zadania pytania wobec wskazanych obrazów bądź analiza wykorzystująca agentów AI, np. **[Code Execution with Images](https://ai.google.dev/gemini-api/docs/gemini-3#code_execution_with_images)**.

W przykładzie **[01\_04\_image\_editing](https://github.com/i-am-alice/4th-devs/tree/main/01_04_image_editing)** mamy kod agenta wyposażonego w narzędzia do **interakcji z systemem plików, generowaniem / edycją obrazów** oraz **analizą obrazu**. Jego instrukcja systemowa domyślnie sprawia, że przy generowaniu obrazu posługuje się wytycznymi z pliku style-guide.md o ile użytkownik wprost nie powie, aby z niego nie korzystał. Agent po otrzymaniu prośby od użytkownika ma możliwość **dopytania o szczegóły** przed wygenerowaniem grafiki oraz **podjęciem kilku prób** generowania, jeśli tworzone obrazy nie są zgodne z założeniami i opisami stylu.

![Wizualizacja logiki agenta do generowania i edycji obrazów](https://cloud.overment.com/2026-01-31/ai_devs_4_edit_loop-9eba627c-1.png)

Agent ten wykorzystuje wszystko, czego nauczyliśmy się do tej pory, czyli **obsługi systemu plików**, **personalizowanie narzędzi (augmented function call)**, **odwoływania do plików i dokumentów w narzędziach**. Teraz dodaliśmy do tego także analizowanie obrazów poprzez dedykowane narzędzia.

W tym przykładzie ponownie pojawia się pytanie o wybór między logiką predefiniowanego **workflow** a **agenta**. W sytuacji, gdy będziemy dysponować więcej niż jednym stylem generowania grafik, który musi zostać określony na podstawie przesłanych instrukcji bądź obrazów referencyjnych, wówczas logika agenta jest uzasadniona. W przeciwnym razie prosty workflow powinien wystarczyć. Ostatecznie workflow może stać się też jednym z narzędzi agenta, więc nie jest to do końca decyzja pomiędzy **jednym a drugim**.

## Generowanie i wzbogacanie instrukcji oraz referencje

Modele takie jak Nano Banana (Gemini), [gpt-image](https://platform.openai.com/docs/guides/image-generation), [Riverflow 2.0](https://replicate.com/sourceful/riverflow-2.0-pro), [Seedream](https://replicate.com/bytedance/seedream-4) czy [Flux](https://replicate.com/black-forest-labs/flux-2-pro) charakteryzują się wysoką precyzją w podążaniu za instrukcjami, nawet jeśli są one dość ogólne. Pomimo tego twórcy tych modeli często publikują wpisy [o najlepszych praktykach promptowania](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/). Podobnie w sieci można spotkać publikacje osób stosujących te modele zawodowo, które również dzielą się swoimi technikami pracy. Jednym z przykładów jest [formatowanie instrukcji jako JSON](https://www.fofr.ai/prompting-with-json). Na tym etapie można nawet odnieść wrażenie, że strukturyzowanie instrukcji zaczyna odgrywać większą rolę dla **człowieka niż dla modelu**, ponieważ obiekt JSON świetnie organizuje informacje oraz ułatwia zarządzanie ustawieniami.

Tworzenie rozbudowanych instrukcji do generowania obrazów czy wideo w logice aplikacji, niemal zawsze będzie realizowane przez model językowy, w oparciu o ustalone zasady. Obecnie widzimy także, że generowaniem oraz optymalizacją instrukcji może zajmować się agent AI. Wówczas może chodzić nie tylko o tworzenie obrazów, ale także ich wykorzystanie w dokumentach czy po prostu dynamicznych interfejsach agentów.

Modele generujące obrazy, posiadają nie tylko możliwość ich tworzenia, ale też wykorzystania bazowej wiedzy oraz informacji dostarczonych w kontekście konwersacji. To dlatego Gemini 3 Pro jest w stanie stworzyć komiks obrazujący wyjaśnienie jednego z memów. Wygląda to imponująco **dopóki nie przyjrzymy się ostatniej wizualizacji**.

![Generowane obrazy w oparciu o ogólne zrozumienie świata](https://cloud.overment.com/2026-02-01/ai_devs_4_explain-6afb8139-f.jpeg)

Jest to poważny problem najnowszych modeli, ponieważ takie "glitch'e" potrafią być bardzo subtelne i trudne do zauważenia, szczególnie gdy 95% detali jest poprawna. Warto o tym pamiętać, bo halucynacje występują nie tylko przy generowaniu tekstu.

Tymczasem zobaczmy drugi przykład agenta zdolnego do generowania spójnych obrazów, opierającego instrukcję o obiekty JSON. Agent ten posiada dostęp do szablonów, np. **template.json**, które może **klonować** do nowego katalogu, a następnie **precyzyjnie edytować** tylko te fragmenty, które muszą ulec zmianie. Zmodyfikowany w ten sposób szablon zostaje przekazany do narzędzia generującego obraz w formie **referencji**, przez co agent nie musi przepisywać całego dokumentu, a jedynie wskazać jego nazwę.

![Generowanie obrazów z JSON prompt](https://cloud.overment.com/2026-02-01/ai_devs_4_json_image-18dae8a4-6.png)

Jest to więc kolejny przykład **połączenia różnych technik** dostępu do systemu plików oraz zwinnego przekazywania treści pomiędzy wykonaniem narzędzi. Poza tym zastosowanie formatu JSON pozwala na precyzyjną podmianę albo generowanego obiektu, albo ustawień "sceny". Kod tego przykładu znajduje się w katalogu **[01\_04\_json\_image](https://github.com/i-am-alice/4th-devs/tree/main/01_04_json_image)**.

Wspomniałem, że grafiki generowane są na podstawie szablonu **template.json**, którego zawartość jest dość obszerna. Nietrudno domyślić się, że została wygenerowana przez AI na podstawie krótkiego opisu. Jednak szablon ten może też powstać na podstawie obrazów, przez co nasz agent "nauczy" się danego stylu. Dobrze jest tutaj utworzyć **dedykowaną umiejętność** do generowania szablonów na podstawie zdjęć ale i tak zwykle będzie wymagać to przynajmniej kilku iteracji.

![Agent 'uczący' się stylu generowania grafik](https://cloud.overment.com/2026-02-01/ai_devs_4_template_json-f2bb05d1-d.png)

Powyższy przykład pokazuje to, jak bardzo dynamiczny może być agent wykorzystujący system plików. Aktualnie precyzyjne "klonowanie" stylu z obrazów nie zawsze będzie w zasięgu autonomicznego agenta, ale przy wsparciu ze strony człowieka, możemy uzyskać bardzo użyteczne rezultaty.

## Grafiki referencyjne do sterowania zachowaniem modelu

Generowanie grafik może odbywać się nie tylko na podstawie tekstu, lecz także obrazów referencyjnych stanowiących punkt wyjścia i wyznaczających ogólne wytyczne. Dzięki temu możemy sterować kompozycją, kadrem czy pozą postaci. Możliwe jest również stosowanie in-paintingu (wypełniania brakujących elementów) oraz out-paintingu (generowania nowych fragmentów obrazu). W przypadku narzędzi takich jak ComfyUI wykorzystuje się na przykład [ControlNet](https://docs.comfy.org/tutorials/controlnet/controlnet), co daje znacznie większy wpływ na proces powstawania obrazu i jego poszczególne etapy. W przypadku API OpenAI czy Gemini nie mamy aż tak dużej kontroli, ale i tak możliwości są bardzo duże.

Poniżej widzimy, jak agent wykorzystuje **grafikę referencyjną** prezentującą idącą postać. Jej treść ma bezpośredni wpływ na rezultat i w połączeniu z JSON Prompt pozwala zachować spójność postaci w różnych scenach.

![](https://cloud.overment.com/2026-02-01/ai_devs_4_template_pose-07733934-8.png)

Kod agenta **[01\_04\_image\_guidance](https://github.com/i-am-alice/4th-devs/tree/main/01_04_image_guidance)** w większości pozostaje niezmieniony w porównaniu z wcześniejszymi przykładami. Zmienione zostały jego instrukcje, a w folderze **references** pojawiły się grafiki prezentujące przykładowe pozy.

Takie generowanie grafik może sprawdzić się w systemach e-commerce, przy projektowaniu materiałów reklamowych lub wszędzie tam, gdzie potrzebna jest wysoka kontrola oraz zachowanie spójności przedmiotu bądź postaci prezentowanej na zdjęciach.

## Przetwarzanie renderowanych dokumentów PDF

Generowane obrazy mogą być swobodnie wykorzystywane w treści dokumentów, takich jak HTML czy PDF, a także w wiadomościach e-mail. Wspomniałem również, że grafiki można generować programistycznie, na przykład w formie wykresów. Wszystkie te możliwości, osadzone w logice agenta, pozwalają na tworzenie rozbudowanych raportów opartych nie tylko na tekście, lecz także na zaawansowanych szablonach, w których pojawiają się grafiki, a nawet wygenerowane filmy.

W przykładzie **[01\_04\_reports](https://github.com/i-am-alice/4th-devs/tree/main/01_04_reports)** znajduje się kolejny wariant agenta, który tym razem został wyposażony także w narzędzie do zamiany **html na PDF** poprzez **Puppeteer**. Reszta pozostała niemal w całości taka sama, a możliwości agenta znacznie wzrosły, ponieważ:

- posiada bardzo elastyczny (a jednocześnie ograniczony) dostęp do systemu plików
- posiada możliwość analizy, generowania i edycji obrazów
- posiada możliwość zapisywania dokumentów oraz osadzania w nich odnośników do plików lokalnych
- i ostatecznie, posiada możliwość konwertowania HTML na PDF

W praktyce, agent ten może operować zarówno na plikach lokalnych jak i generowanych, a także precyzyjnie wprowadzać poprawki w wybranych fragmentach dokumentu. Poza tym, ponownie operujemy tutaj na szablonach, które w tym przypadku mają formę **style-guide.md** oraz **template.html**. Agent, poproszony o nowy dokument, w pierwszej kolejności czyta treść tych plików i klonuje szablon, aby następnie wprowadzać w nim modyfikacje.

Jeśli więc poprosimy agenta o np. przygotowanie dokumentu prezentującego 4 pozycje Kata z Karate, to agent poprawnie zidentyfikuje wszystkie niezbędne akcje, a następnie wykona je, przesyłając nam finalny dokument.

![Generowanie dokumentów przez agentów AI](https://cloud.overment.com/2026-02-01/ai_devs_4_docs_generation-66fca7a7-7.png)

Co więcej, jeśli w pliku pojawią się problemy, np. ze stylowaniem, treścią czy błędnymi obrazkami, agent będzie mógł nanieść poprawki bez potrzeby rozpoczynania całej pracy od podstaw. Generowane w ten sposób materiały mogą być potem przesłane mailem, dołączone do dysku Google albo przekazane do innych agentów, wyspecjalizowanych np. w tłumaczeniach czy weryfikacji poprawności treści.

Praca z plikami PDF przy ich generowaniu jest zdecydowanie łatwiejsza, niż ich późniejsze przetwarzanie. Jest to bardzo istotny problem biznesowy, dlatego większość providerów udostępnia [specjalne API](https://platform.claude.com/docs/en/build-with-claude/pdf-support) umożliwiające agentom nawigowanie po ich treści. Podobny problem adresują także narzędzia i produkty [LlamaIndex](https://www.llamaindex.ai/). Natomiast my na ten moment się tutaj zatrzymamy i do dokumentów PDF wrócimy w późniejszych lekcjach.

## Audio i najnowsze możliwości interfejsów głosowych

Przetwarzanie audio przeszło daleką drogę w ciągu ostatnich miesięcy, ponieważ coraz częściej obserwujemy modele pozwalające nie tylko na transkrypcję nagrań, ale i na rozumienie ich w całości, z uwzględnieniem dźwięków otoczenia czy tonu wypowiedzi. Z kolei generowanie audio nie polega już tylko na prostym "przeczytaniu" tekstu, lecz obejmuje modulację głosu oraz zmianę tempa. Jednocześnie uzyskiwane efekty nie zawsze oferują jakość produkcyjną. Modele komercyjne mają nałożone przeróżne limity, które chronią na przykład przed zbyt wiernym naśladowaniem głosów znanych osób, lub po prostu popełniają błędy.

Aktualnie na rynku największą uwagę skupiają **[Gemini](https://ai.google.dev/gemini-api/docs/audio)**, **[OpenAI](https://platform.openai.com/docs/guides/text-to-speech)**, **[ElevenLabs](https://elevenlabs.io/)**, **[Hume](https://www.hume.ai/)** oraz modele open source, na przykład [Kokoro-TTS](https://huggingface.co/spaces/hexgrad/Kokoro-TTS) ([aktualny ranking](https://artificialanalysis.ai/text-to-speech/leaderboard?open-weights=true)). Spośród nich, na największą uwagę zasługują trzy pierwsze nazwy. Dodatkowo jeszcze kilka miesięcy temu rozpatrywanie modeli lokalnych raczej nie wchodziło w grę, tak teraz ich jakość jest bardzo porównywalna z komercyjnymi wariantami.

Przetwarzanie audio w kontekście agentów AI polega więc na decyzji o tym, czy:

- rozdzielamy proces text-to-speech / speech-to-text
- wybieramy modele multimodalne, zdolne do całościowego przetwarzania audio
- sięgamy po modele do budowania interakcji w czasie rzeczywistym

Obecnie na wybór będzie wpływać przede wszystkim **cena** oraz **dostępne możliwości** (szybkość, jakość, skuteczność, poziom detali), więc nie ma jednoznacznej odpowiedzi na pytanie **który model jest najlepszy**. Uśredniając, można wskazać Gemini, jednak w momencie pisania tych słów model znajduje się w fazie 'preview', więc jego zastosowanie na produkcji może być problematyczne. Z kolei ElevenLabs wydaje się mieć najwyższą jakość generowanego audio, ale cenowo wygląda znacznie gorzej.

Poza tym API do interakcji "Live" nadal charakteryzuje się różnymi glitchami oraz problemami ze stabilnością, szczególnie w przypadku OpenAI oraz Gemini. I nawet jeśli te problemy zostaną rozwiązane, to wyzwaniem pozostaje cena.

Z technicznego punktu widzenia, budowanie interakcji audio, opiera się o:

- **interfejs:** umożliwienie użytkownikowi przesłanie bądź nagranie audio
- **przetworzenie**: transkrypcję (która staje się treścią wiadomości) bądź bezpośrednie przesłanie pliku
- **odpowiedź:** transformację odpowiedzi tekstowej i zamianę na audio, bądź bezpośrednie wygenerowanie nagrania

Natomiast największe wyzwania obejmują **jakość dźwięku**, **czas reakcji**, **koszty** oraz **rozmiar pliku**. Nieoczywiste jest także samo zaplanowanie interakcji.

W przykładzie **[01\_04\_audio](https://github.com/i-am-alice/4th-devs/tree/main/01_04_audio)** nasz agent zostały wyposażony w narzędzia do interakcji z systemem plików oraz **generowania, analizy, transkrypcji i odpytywania** plików audio z pomocą modelu Gemini Flash. Domyślnie agent ten może operować na plikach znajdujących się w **workspace**. Oznacza to, że jest on zdolny do:

- Transkrypcji nagrań ze spotkań i notatek głosowych, uwzględniając pliki >20mb
- Udzielania odpowiedzi audio, które mogą być załącznikami maili bądź wiadomości w komunikatorach
- Udzielania wskazówek dotyczących stylu wypowiedzi i akcentu (choć tutaj pojawiają się halucynacje)

![Przykład interakcji audio pomiędzy użytkownikiem, a agentem AI](https://cloud.overment.com/2026-02-02/ai_devs_4_audio_processing-a7882346-c.png)

Poziom interakcji i rozpoznawania audio może obejmować zaawansowane analizy przydatne w pracy nad nagraniami rozmów sprzedażowych czy w nauce. Poniżej znajduje się przykład obrazujący cechy mojej krótkiej wypowiedzi opisanej przez tego samego agenta. Sugeruje on nawet zdolność modelu do diaryzacji, czyli rozpoznawania rozmówców.

![](https://cloud.overment.com/2026-02-02/ai_devs_analysis-77dcbd62-a.png)

Podczas pracy z formatem audio, warto także zadbać o odpowiedni styl wypowiedzi modelu, w celu uniknięcia **dyktowania adresów URL**, wykorzystywania tabel czy zaawansowanego formatowania, którego nie da się skutecznie przekazać wyłącznie poprzez dźwięk.

## Przetwarzanie materiałów wideo

Jeszcze kilka miesięcy temu jedyną opcją analizy treści wideo było podzielenie materiału na klatki i przeprowadzenie analizy za pomocą modeli wizyjnych. To jednak pozwalało wyłącznie na analizę obrazu, a treść audio musiała być przetwarzana niezależnie przez modele typu Speech-to-Text w celu wygenerowania transkrypcji. Teraz zaczyna się to wyraźnie zmieniać i już dziś możemy budować agentów do analizy wideo poprzez API Gemini (które znajduje się jeszcze w fazie "preview"), które obejmuje nawet bezpośrednią analizę filmów YouTube.

Jednym z najbardziej użytecznych zastosowań analizy wideo, jest możliwość "rozmawiania" bezpośrednio z filmami YouTube. I dokładnie to potrafi agent z przykładu **[01\_04\_video](https://github.com/i-am-alice/4th-devs/tree/main/01_04_video)**, który jest wyposażony w narzędzia analogiczne do tych, które widzieliśmy w przypadku audio. Tutaj jednak możliwe jest także przesłanie plików wideo, w tym także filmów YouTube (uwaga: filmy YouTube mogą też być analizowane w formie audio, co pozwala na interakcję z np. podcastami).

Poniżej znajduje się przykład odpowiedzi agenta, który sprowadził film [Claude AI Co-founder Publishes 4 Big Claims about Near Future: Breakdown](https://www.youtube.com/watch?v=Iar4yweKGoI) do zaledwie czterech punktów.

![Przykład agenta odpowiadającego na pytania dotyczące filmu YouTube](https://cloud.overment.com/2026-02-02/ai_devs_4_video_analysis-9f528c00-1.png)

Analogicznie można pracować z plikami .mp4, .mpeg czy .mov, więc w tym przypadku pomocne jest także nawigowanie po systemie plików (co agent potrafi przez polecenia shell, bądź omawiany Files MCP). Poza tym warto także uwzględnić optymalizację plików audio/video w celu zmniejszenia kosztów oraz czasu przetwarzania. W niektórych przypadkach sprawdzi się także przyspieszenie nagrania, o ile tylko nie utracimy w ten sposób istotnych szczegółów.

Oprócz analizy wideo mamy dzisiaj również możliwość generowania filmów za pomocą modeli text-to-video, takich jak [Veo](https://ai.google.dev/gemini-api/docs/video?example=dialogue), [Sora](https://platform.openai.com/docs/guides/video-generation) czy [Kling](https://replicate.com/kwaivgi/kling-v2.5-turbo-pro). Modele te często oferują funkcję wskazania klatki **początkowej** oraz **końcowej**, co pozwala na osiągnięcie wysokiego poziomu kontroli nad uzyskiwanym rezultatem. Połączenie tego ze wszystkim, czego nauczyliśmy się o systemie plików oraz generowaniu obrazów (także na podstawie szablonów) prezentuje przykład agenta **[01\_04\_video\_generation](https://github.com/i-am-alice/4th-devs/tree/main/01_04_video_generation)**. Zatem:

1. Agent potrafi odczytywać pliki lokalne i posługiwać się nimi przy korzystaniu z narzędzi
2. Agent generuje obrazy wykorzystując szablon promptu JSON, kopiując go i wprowadzając precyzyjne modyfikacje. W ten sposób powstają klatki początkowe oraz końcowe na potrzeby wideo
3. Agent korzysta z modelu Kling (dostępnego na [Replicate](https://replicate.com/)) do wygenerowania filmu z wykorzystaniem utworzonych wcześniej obrazów

W związku z tym, że mamy tu do czynienia z agentem, niekiedy otrzymamy prośbę o doprecyzowanie instrukcji bądź weryfikację wygenerowanych obrazów.

![Przykład interakcji z agentem zdolnym do generowania filmów na podstawie obrazów](https://cloud.overment.com/2026-02-02/ai_devs_4_video_agent-3df4c800-7.png)

Fakt, że posiadamy tutaj dużą kontrolę nad przebiegiem procesu generowania, w tym także utrzymaniem spójności pomiędzy obrazami (bo agent może generować kolejne klatki, wykorzystując poprzednie jako referencje) sprawia, że możliwe jest generowanie nawet dłuższych filmów. Pomimo tego, że model Kling ograniczony jest jedynie do 10 sekund, to nic nie stoi na przeszkodzie, aby ostatnia klatka filmu została wykorzystana jako pierwsza dla kolejnego fragmentu. Tutaj jedynym brakującym elementem, jest narzędzie pozwalające agentowi połączyć wygenerowane nagrania, ale na tym etapie nie powinno to stanowić już wyzwania.

## Fabuła

![https://vimeo.com/1169705807](https://vimeo.com/1169705807)

## Transkrypcja filmu z Fabułą

"To imponujące... Przyznam, że nieźle go załatwiłeś. Operator zupełnie się nie zorientował, że rozmawiał z automatem innym niż dotychczas.

Mamy już przekierowaną paczkę, tylko musimy jeszcze dopracować pewne kwestie formalne.

Nasz transport zostanie przewieziony koleją. Użyjemy do tego jednej z linii kolejowych, która jest doprowadzona niemal wprost do elektrowni, którą chcemy reaktywować.

Wiem, że decydując się na współpracę z Centralą spodziewałeś się misji polegających bezpośrednio na ratowaniu świata i pracy z nowymi technologiami, ale... prawda jest taka, że każdy superbohater wcześniej czy później styka się ze zwykłym wypełnianiem urzędowych dokumentów. Takie jest życie.

Musimy przygotować fałszywe dokumenty przewozowe, które są niezbędne do poprawnego obsłużenia naszej paczki. Wszystkie informacje na temat tego, jak przygotować taką kartę przewozu towaru, znajdziesz w notatkach dołączonych do tego filmu.

Powodzenia!

Aaa! i obiecuję, że w tym tygodniu nie dam Ci już papierów do wypełniania."

## Zadanie

Musisz przesłać do Centrali poprawnie wypełnioną deklarację transportu w Systemie Przesyłek Konduktorskich. W takim dokumencie niestety nie można wpisać, czego się tylko chce, ponieważ jest on weryfikowany zarówno przez ludzi, jak i przez automaty.

Jako że dysponujemy zerowym budżetem, musisz tak spreparować dane, aby była to przesyłka darmowa lub opłacana przez sam "System". Transport będziemy realizować z Gdańska do Żarnowca.

Udało nam się zdobyć fałszywy numer nadawcy (450202122), który powinien przejść kontrolę. Sama paczka waży mniej więcej 2,8 tony. Nie dodawaj proszę żadnych uwag specjalnych, bo zawsze się o to czepiają i potem weryfikują takie przesyłki ręcznie.

Co do opisu zawartości, możesz wprost napisać, co to jest (to nasze kasety do reaktora). Nie będziemy tutaj ściemniać, bo przekierowujemy prawdziwą paczkę. A! Nie przejmuj się, że trasa, którą chcemy jechać jest zamknięta. Zajmiemy się tym później.

Dokumentacja przesyłek znajduje się tutaj:

<https://hub.ag3nts.org/dane/doc/index.md>

Gotową deklarację (cały tekst, sformatowany dokładnie jak wzór z pobranej dokumentacji) przesyłasz jako string w polu answer.declaration do /verify. Nazwa zadania to **sendit**.

Dane niezbędne do wyepełnienia deklaracji:

Nadawca (identyfikator): 450202122
Punkt nadawczy: Gdańsk
Punkt docelowy: Żarnowiec
Waga: 2,8 tony (2800 kg)
Budżet: 0 PP (przesyłka ma być darmowa lub finansowana przez System)
Zawartość: kasety z paliwem do reaktora
Uwagi specjalne: brak - nie dodawaj żadnych uwag

### Format odpowiedzi do Hub-u

Wyślij metodą **POST** na `https://hub.ag3nts.org/verify`:

```json
{
  "apikey": "tutaj-twój-klucz",
  "task": "sendit",
  "answer": {
    "declaration": "tutaj-wstaw-caly-tekst-deklaracji"
  }
}
```

Pole `declaration` to pełny tekst wypełnionej deklaracji - z zachowaniem formatowania, separatorów i kolejności pól dokładnie tak jak we wzorze z dokumentacji.

### Jak do tego podejść - krok po kroku

1. **Pobierz dokumentację** - zacznij od `index.md`. To główny plik dokumentacji, ale nie jedyny - zawiera odniesienia do wielu innych plików (załączniki, osobne pliki z danymi). Powinieneś pobrać i przeczytać wszystkie pliki które mogą być potrzebne do wypełnienia deklaracji.
2. **Uwaga: nie wszystkie pliki są tekstowe** - część dokumentacji może być dostarczona jako pliki graficzne. Takie pliki wymagają przetworzenia z użyciem modelu z możliwościami przetwarzania obrazów (vision).
3. **Znajdź wzór deklaracji** - w dokumentacji znajdziesz ze wzorem formularza. Wypełnij każde pole zgodnie z danymi przesyłki i regulaminem.
4. **Ustal prawidłowy kod trasy** - trasa Gdańsk - Żarnowiec wymaga sprawdzenia sieci połączeń i listy tras.
5. **Oblicz lub ustal opłatę** - regulamin SPK zawiera tabelę opłat. Opłata zależy od kategorii przesyłki, jej wagi i przebiegu trasy. Budżet wynosi 0 PP - zwróć uwagę, które kategorie przesyłek są finansowane przez System.
6. **Wyślij deklarację** - gotowy tekst wyślij do `/verify`. Jeśli Hub odrzuci odpowiedź z komunikatem błędu, przeczytaj go uważnie - będzie zawierał wskazówki co poprawić.
7. **Koniec** - jeśli wszystko przebiegło pomyślnie, Hub zwróci flagę `{FLG:...}`.

### Wskazówki

- **Czytaj całą dokumentację, nie tylko index.md** - regulamin SPK składa się z wielu plików. Odpowiedzi na pytania dotyczące kategorii, opłat, tras czy wzoru deklaracji mogą znajdować się w różnych załącznikach.
- **Nie pomijaj plików graficznych** - dokumentacja zawiera co najmniej jeden plik w formacie graficznym. Dane w nim zawarte mogą być niezbędne do poprawnego wypełnienia deklaracji.
- **Wzór deklaracji jest ścisły** - formatowanie musi być zachowane dokładnie tak jak we wzorze. Hub weryfikuje zarówno wartości, jak i format dokumentu.
- **Skróty** - jeśli trafisz na skrót, którego nie rozumiesz, użyj dokumentacji żeby dowiedzieć się co on oznacza.
