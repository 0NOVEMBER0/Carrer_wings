import os
import pandas as pd
from dotenv import load_dotenv
from anthropic import (
    Anthropic,
    RateLimitError,
    APIConnectionError,
    AuthenticationError,
    APIError,
)

from flask import (
    Flask,
    render_template,
    request,
)
from werkzeug.utils import secure_filename


load_dotenv()

api_key = os.environ.get("API_KEY")

client = Anthropic(api_key=os.environ.get("API_KEY"))

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
DANE_PREVIEW_WIERSZY = 50


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def zapytaj_claude(tresc_pytania):
    try:
        odpowiedz = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": tresc_pytania}],
        )
        return odpowiedz.content[0].text

    except AuthenticationError:
        return "BŁĄD: nieprawidłowy klucz API."

    except RateLimitError:
        return "BŁĄD: zbyt wiele zapytań. Spróbuj za chwilę."

    except APIConnectionError:
        return "BŁĄD: problem z połączeniem internetowym."

    except APIError as blad:
        return f"BŁĄD: {blad}"


@app.route("/")
def strona_glowna():
    return render_template("index.html", odpowiedz=None)


@app.route("/analizuj", methods=["POST"])
def analizuj():
    plik = request.files.get("plik_csv") or request.files.get(
        "plik_xlsx")  # HW -XLSX

    if not plik or plik.filename == "":
        return render_template("analiza.html", blad="Nie wybrano pliku lub podano plik, który jest pusty.")

    if not plik.filename.endswith((".csv", ".xlsx")):
        return render_template("analiza.html", blad="Błędne rozszerzenie. Prześlij plik w formacie .csv lub w formacie .xlsx")

    try:
        if plik.filename.endswith("csv"):
            df = pd.read_csv(plik)
        else:
            df = pd.read_excel(plik)

    except Exception as e:
        return render_template("analiza.html", blad=f"Nie udało się wczytać pliku: {e}")

    liczba_wierszy, liczba_kolumn = df.shape
    podglad = df.head(5).to_string(index=False)
    kolumny = ", ".join(df.columns.tolist())
    braki = df.isna().sum()

    prompt = f"""Mam plik CSV z danymi. Oto podstawowe informacje:
            - Liczba wierszy: {liczba_wierszy}
            - Liczba kolumn: {liczba_kolumn}
            - Nazwy kolumn: {kolumny}
            - Kolumny z brakami: {braki}
            - Pierwsze 5 wierszy:
            {podglad}
            Napisz krótkie podsumowanie tych danych po polsku. Co to może
            być za zbiór danych? Co można z niego wyczytać?"""

    podsumowanie = zapytaj_claude(prompt)

    return render_template(
        "analiza.html",
        nazwa_pliku=plik.filename,
        liczba_wierszy=liczba_wierszy,
        liczba_kolumn=liczba_kolumn,
        podsumowanie_ai=podsumowanie,
    )


@app.route("/zapytaj", methods=["POST"])
def zapytaj():
    tresc_pytania = request.form.get("pytanie", "").strip()
    if tresc_pytania == "":
        return render_template("index.html", odpowiedz="Wpisz najpierw jakieś pytanie!")
    odpowiedz_claude = zapytaj_claude(tresc_pytania)
    return render_template("index.html", odpowiedz=odpowiedz_claude, pytanie=tresc_pytania)


@app.route("/analiza-strona")
def analiza_strona():
    return render_template("analiza.html")


if __name__ == "__main__":
    app.run(debug=True)
