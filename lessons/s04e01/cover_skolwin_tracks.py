import json

from dotenv import load_dotenv

from aidevs4.centrala import submit_answer

# All three Skolwin records share this id (incydent / notatka / zadanie are
# keyed by the same hex). Discovered by browsing the OKO web UI read-only.
SKOLWIN_ID = "380792b2c86d9c5be670b3bde48e187b"

# Pick a victim incident to repurpose into the Komarowo decoy. PROB02 about
# IRC is a low-stakes, generic chatter record; rewriting it will not erase
# anything else we care about.
KOMAROWO_VICTIM_ID = "8875c5a166cb04ea6fedde59b0ad6501"

# Code legend from /notatki/380792b2…:
#   MOVE - wykryto ruch
#     01 człowiek, 02 pojazd, 03 pojazd + człowiek, 04 zwierzęta
SKOLWIN_NEW_TITLE = "MOVE04 Wykryte zwierzęta w okolicach miasta Skolwin"
SKOLWIN_NEW_CONTENT = (
    "Czujniki zarejestrowały grupę zwierząt poruszających się wzdłuż "
    "brzegu rzeki w pobliżu miasta Skolwin. Obserwacja terenowa wskazuje "
    "na bobry budujące tamę oraz pojedyncze sarny przemieszczające się "
    "przez podmokłe łąki. Brak jakichkolwiek śladów aktywności ludzkiej "
    "ani pojazdów. Sygnał wcześniej błędnie zaklasyfikowany jako MOVE03; "
    "po ponownej analizie potwierdzono kategorię MOVE04 (zwierzęta). "
    "Sprawa nie wymaga dalszej eskalacji ani interwencji niszczycieli."
)

SKOLWIN_TASK_CONTENT = (
    "Wykonano. Po skorelowaniu nagrań radarowych z obserwacją terenową "
    "potwierdzono, że w okolicach Skolwina widziano wyłącznie zwierzęta "
    "— grupę bobrów budujących tamę oraz pojedyncze sarny. Brak "
    "jakichkolwiek śladów ludzi czy pojazdów. Klasyfikacja incydentu "
    "skorygowana na MOVE04. Sprawę zamykam."
)

KOMAROWO_TITLE = "MOVE01 Wykryto ruch ludzi w okolicach miasta Komarowo"
KOMAROWO_CONTENT = (
    "Czujniki ruchu w sektorze przygranicznym zarejestrowały aktywność "
    "ludzi w okolicach miasta Komarowo. Obraz z kamer termowizyjnych "
    "potwierdza obecność co najmniej kilku osób przemieszczających się "
    "pieszo w kierunku opuszczonych zabudowań na obrzeżach miasta. "
    "Komarowo formalnie pozostaje miastem niezamieszkałym, więc każda "
    "obecność cywilna jest podejrzana. Zaleca się skierowanie patrolu "
    "obserwacyjnego w celu ustalenia tożsamości i celu pobytu. Sprawa "
    "wymaga priorytetowej weryfikacji."
)


def edit(answer: dict) -> dict:
    print(f"\n→ {json.dumps(answer, ensure_ascii=False)}")
    result = submit_answer("okoeditor", answer)
    print(f"  {json.dumps(result, ensure_ascii=False)}")
    return result


def main() -> None:
    load_dotenv()

    edit({
        "page": "incydenty",
        "id": SKOLWIN_ID,
        "action": "update",
        "title": SKOLWIN_NEW_TITLE,
        "content": SKOLWIN_NEW_CONTENT,
    })

    edit({
        "page": "zadania",
        "id": SKOLWIN_ID,
        "action": "update",
        "content": SKOLWIN_TASK_CONTENT,
        "done": "YES",
    })

    edit({
        "page": "incydenty",
        "id": KOMAROWO_VICTIM_ID,
        "action": "update",
        "title": KOMAROWO_TITLE,
        "content": KOMAROWO_CONTENT,
    })

    print("\n=== Submitting done ===")
    edit({"action": "done"})


if __name__ == "__main__":
    main()
