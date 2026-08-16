import os
from dotenv import load_dotenv
from anthropic import (
    Anthropic,
    RateLimitError,
    APIConnectionError,
    AuthenticationError,
    APIError,
)

# czyta plik .env i wczytuje jego zawartość do zmiennych środowiskowych

load_dotenv()

api_key = os.environ.get("API_KEY")


def sprawdz_klucz(klucz):
    if (klucz is None):
        print("Klucz nie istnieje")
    else:
        print("Klucz jest obecny:", klucz[:10])


sprawdz_klucz(api_key)

client = Anthropic(api_key=os.environ.get("API_KEY"))

MODEL = "claude-haiku-5"
MAX_TOKENS = 1024


# Historia całej rozmowy
historia = []


# Wybieranie osobowości chatbota-zwykły print
def wybierz_osobowosc():
    print("Wybierz bota:")
    print(" 1) Poważny asystent")
    print(" 2) Zabawny kompan")
    print(" 3) Sarkastyczny korepetytor")
    print(" 4) Nauczyciel akademicki z długim stażem")

    wybor = input("Twój wybór (1/2/3/4): ").strip()

    if wybor == "1":
        return "Jesteś rzeczowym, formalnym asystentem. Odpowiadasz precyzyjnie i konkretnie."
    elif wybor == "2":
        return "Jesteś wesołym, energicznym asystentem, który uwielbia żarty i emotikony."
    elif wybor == "3":
        return "Jesteś sarkastycznym korepetytorem z ciętym poczuciem humoru, ale zawsze pomagasz merytorycznie."
    elif wybor == 4:
        return "Jesteś nauczycielem akademickim z długim stażem. Jesteś przyzwyczajony do tłumaczenia zawiłych naukowych kwestii studentom w posty sposób  "
    else:
        print("Nie rozpoznano wyboru, używam domyślnej, poważnej osobowości.\n")
        return "Jesteś rzeczowym, formalnym asystentem."


def zapytaj_claude(tresc_pytania, system_prompt):
    """Wysyła pytanie do Claude razem z całą dotychczasową historią i zwraca odpowiedź."""

    historia.append({"role": "user", "content": tresc_pytania})

    try:
        odpowiedz = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=historia,
        )

        tekst_odpowiedzi = odpowiedz.content[0].text

        historia.append({"role": "assistant", "content": tekst_odpowiedzi})
        return tekst_odpowiedzi

    except AuthenticationError:
        historia.pop()
        return "BŁĄD: nieprawidłowy klucz API. Sprawdź plik .env."
    except RateLimitError:
        historia.pop()
        return "BŁĄD: zbyt wiele zapytań. Poczekaj chwilę."
    except APIConnectionError:
        historia.pop()
        return "BŁĄD: problem z połączeniem internetowym."


def gadu_gadu_z_chatem(nazwa_pliku="rozmowa.txt"):
    """Zapisuje całą historię rozmowy do pliku tekstowego."""
    with open(nazwa_pliku, "w", encoding="utf-8") as plik:
        for wpis in historia:
            kto = "Ty" if wpis["role"] == "user" else "Claude"
            plik.write(f"{kto}: {wpis['content']}\n\n")


def main():
    print("=" * 50)
    print(" CHATBOT AI, 'quit' kończy, 'menu' zmienia bota")
    print("=" * 50)
    print()

    system_prompt = wybierz_osobowosc()
    licznik = 0

    while True:

        pytanie_uzytkownika = input("\nTy: ")

        if pytanie_uzytkownika.strip().lower() == "quit":
            print("\nDo zobaczenia!")
            print(f"Zadano {licznik} pytań")
            gadu_gadu_z_chatem()
            print("Rozmowa została zapisana do pliku rozmowa.txt.")
            break

        if pytanie_uzytkownika.strip().lower() == "menu":
            print()
            system_prompt = wybierz_osobowosc()
            continue

        if pytanie_uzytkownika.strip() == "":
            print("Wpisz najpierw jakieś pytanie!")
            continue

        licznik += 1

        odpowiedz = zapytaj_claude(
            pytanie_uzytkownika,
            system_prompt
        )
        print("Claude:", odpowiedz)


if __name__ == "__main__":
    main()
