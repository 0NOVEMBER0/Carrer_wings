import os
from dotenv import load_dotenv
from anthropic import (
    Anthropic,
    RateLimitError,
    APIConnectionError,
    AuthenticationError,
    APIError,
)

from flask import Flask, render_template, request



load_dotenv()

api_key = os.environ.get("API_KEY")

client = Anthropic(api_key=os.environ.get("API_KEY"))

MODEL = "claude-haiku-5"
MAX_TOKENS = 1024



app=Flask(__name__)


def wybierz_styl_odpowiedzi(odpowiedz):

    if odpowiedz == "1":
        return "Odpowiadasz wyczerpująco na dany temat,jesteś merytoryczny, dodajesz do swojej wypowiedzi wiele niezbędnych szczegółów."
    elif odpowiedz == "2":
        return "Odpowiadasz krótko na zadane pytanie, uwzględniasz jedynie najważniejsze informacje."
    else:
        return "Odpowiadasz na dany temat uwzględniając najważniejsze informacje, ale dodajesz też trochę szczegółów.Tekst nie jest ani za krótki,ani za długi"




def zapytaj_claude(tresc_pytania,system_prompt):
    try:
        odpowiedz = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
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


licznik=0


@app.route("/")

def strona_glowna():
    return render_template("index.html", odpowiedz=None)



@app.route("/zapytaj", methods=["POST"])




def zapytaj():
    global licznik
    tresc_pytania = request.form.get("pytanie", "").strip()
    odpowiedz= request.form.get("odpowiedz", "domyslna")

    if tresc_pytania == "":
        return render_template(
                "index.html", odpowiedz="Wpisz najpierw jakieś pytanie!"
            )

    system_prompt=wybierz_styl_odpowiedzi(odpowiedz)
    odpowiedz_claude = zapytaj_claude(tresc_pytania,system_prompt)
    licznik+=1
    

    return render_template(
            "index.html", odpowiedz=odpowiedz_claude, pytanie=tresc_pytania, licznik=licznik
    )



if __name__ == "__main__":
    app.run(debug=True)









