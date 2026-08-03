import pandas as pd
df = pd.read_csv("spotify.csv")

print(df.shape)


#ZADANIE1
playlist=df[
    (df["energy"]>0.8)
    & (df["danceability"]>0.8)
    &(df["valence"]>0.7)
].sort_values("popularity",ascending=False).head(20)

print(playlist[["track_name","artists","track_genre","danceability","valence","energy"]])

playlist.to_csv("energy_mix.csv",index=False)

#ZADANIE 2

raport=df.groupby("track_genre").agg(
    mean_popularity=("popularity","mean"),
    mean_temp=("tempo","mean"),
    n_songs=("track_genre","count")
).sort_values("mean_popularity",ascending=False)

raport_v2=raport[raport["n_songs"]>=100]
print(raport_v2)

raport_v3=raport_v2.head(15)
raport_v3.to_csv("Popularne_gatunki.csv",index=True)


#Zadanie3


df["duration_min"]=df["duration_ms"]/60000

long_and_popular=df[
    (df["duration_min"]>6)
    & (df["popularity"]>60)
].sort_values("duration_min",ascending=False)

long_and_popular.to_csv("Hity.csv",index=False)



#MINI RAPORT-MÓJ ULUBIONY GATUNEK

print("\n\n MINI RAPORT- ULUBIONY GARUNEK")
track_genre=df["track_genre"].unique()
print(track_genre)
my_f=df[df["track_genre"]=="rock"]
mean_p=my_f["popularity"].mean()
print(f'Średnia popularność: {mean_p}')
mean_d=my_f["duration_ms"].mean()
print(f'Średnia długość [w minutach]: {mean_d/60000} \n')
popular_hits=my_f.sort_values("popularity",ascending=False).head(5)
print(f'5 NAJWIĘKSZYCH HITÓW:\n {popular_hits}')

popular_hits.to_csv("Rock_hits.csv",index=False)


#ĆWICZENIA DODATKOWE 
print("Korelacja między głośnością, a energicznością")
print(df["energy"].corr(df["loudness"]))
print(df["loudness"].corr(df["energy"]))
