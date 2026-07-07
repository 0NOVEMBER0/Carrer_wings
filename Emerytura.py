from datetime import datetime

current_year = datetime.now().year
name = input("IMIE: \n")
year_of_birth = int(input("ROK URODZENIA: \n"))
sex = input("PłEĆ (WPISZ M LUB K): \n")


if (sex.upper() == "K"):
    czas_do_emerytury = 60-(current_year-year_of_birth)
    if (czas_do_emerytury > 10):
        print(
            f"{name}, zostało Ci {czas_do_emerytury} lat do emerytury, trochę się naczekasz")
    if (0 < czas_do_emerytury <= 10):
        print(
            f"{name}, zostało Ci {czas_do_emerytury} lat do emerytury, już niewiele, keep going!")
    if (czas_do_emerytury <= 0):
        print("Farciara, już na wolnym --")
elif (sex.upper() == "M"):
    czas_do_emerytury = 65-(current_year-year_of_birth)
    if (czas_do_emerytury > 10):
        print(
            f"{name}, zostało Ci {czas_do_emerytury} lat do emerytury, trochę się naczekasz")
    if (0 < czas_do_emerytury <= 10):
        print(
            f"{name}, zostało Ci {czas_do_emerytury} lat do emerytury, już niewiele, keep going!")
    if (czas_do_emerytury <= 0):
        print("Farciarz, już na wolnym --")
