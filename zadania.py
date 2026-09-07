
#zadanie 1


exam_points = {"Mariusz":30, "Mateusz":55, "Marta":76, "Roman":30,
    "Arleta":59, "Adrian":96, "Monika":91, "Andrzej":22,
    "Krzysztof":83, "Krystyna":93, "Piotr":44, "Dawid":10, "Agnieszka":15}

max_score=0
failed_students=[]
top_students=[]

for student,score in exam_points.items():
    if score<=45:
        failed_students.append(student)

    elif score>90 and score<=100:
        top_students.append(student)

    if score>max_score:
       max_score=score
       best_student=(student,score)

print(f"Students who failed: { failed_students}")
print(f"The best students: { top_students}")
print(f"The student with the highest score: {best_student[0]}")


#zadanie 2
alphabet=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","W","X","Y","Z"]
names = ['Paweł', 'Kewin', 'Ireneusz', 'Bolesław', 'Mateusz',
'Edward', 'Piotr', 'Jan', 'Denis', 'Amir', 'Igor', 'Borys',
'Robert', 'Ariel', 'Kuba', 'Rafał', 'Mateusz', 'Emanuel']
name_dict = {}

for letter in alphabet:
    for name in names:
        if name[0]==letter:
            name_dict.setdefault(letter,[]).append(name)

print(name_dict)

#zadanie 3
n=0
n1=1
number_of_elements=30
Fibb=[n,n1]
while len(Fibb)<30:
    num_fibb=n+n1
    Fibb.append(num_fibb)
    n=n1
    n1=num_fibb

print(Fibb)


#zadanie 3

def equation(a,b,c):
    delta=b**2-4*a*c
    if delta>0:
        x1=(-b+delta**0.5)/(2*a)
        x2=(-b-delta**0.5)/(2*a)
        solution=(x1,x2)
        print(f"Equation has 2 solutions: {solution}")
    elif delta==0:
        solution=(-b)/(2*a)
        print(f"Equation has 1 solution: {solution}")
    else:
        print(f"Equation doesn't have solutions")

equation(2,-9,4)