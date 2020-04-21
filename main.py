import pandas as pd
import csv


data = pd.read_csv('Chart 6_6_11 [0].csv')
print(data.head())
depth = data['Depth'].to_list()
time = data['TimeOffset[ms]'].to_list()

datagps = pd.read_csv('gps 6_6_11 [0].csv')
print(datagps.head())
X = datagps['X'].to_list()
Y = datagps['Y'].to_list()
H = datagps['H'].to_list()
czas = datagps['czas'].to_list()

tyczka = 1
undulacja = 39.934

d = []
for i in depth:
    d.append(i*0.3048)

podany_czas = 133
g133 = 10
m133 = 20
s133 = 26
cz133 = (g133*3600)+(m133*60)+s133

time0 = []
for i in time:
    time0.append(i/1000)

time133 = time0[podany_czas - 1]
czas_poczatku_pomiaru = cz133 - time133

sdeptx = []
for i in time0:
    sdeptx.append(czas_poczatku_pomiaru + i)

sgps = []
for i in czas:
    g0 = float(i[11])
    g1 = float(i[12])
    m3 = float(i[14])
    m4 = float(i[15])
    s6 = float(i[17])
    s7 = float(i[18])
    sgps.append(((10*g0+g1)*3600)+((10*m3+m4)*60)+(10*s6+s7))

sdept = []
for i in sdeptx:
    if i >= sgps[0]:
        sdept.append(i)

czasdict = {}
gpsId = 1

for gle in sdept:
    key = None
    if gpsId >= len(sgps) or gle <= sgps[gpsId]:
        key = sgps[gpsId - 1]
    else:
        key = sgps[gpsId]
        gpsId = gpsId + 1

    if not key in czasdict:
        czasdict[key] = []
    czasdict[key].append(gle)

lista_b = []
for i in czasdict:
    lista_b.append(czasdict[i])

sdep0 = []
for linijka in lista_b:
    sdep0.append(min(linijka))

licznik = 0
drugilicznik = 0
dobreg = []
liczbapkt = 0
for i in sdeptx:
    liczbapkt = liczbapkt + 1

while licznik < liczbapkt:
    if sdeptx[licznik] in sdep0:
        dobreg.append(d[licznik])
        drugilicznik = drugilicznik + 1
        licznik = licznik + 1
    else:
        licznik = licznik + 1

dobreg_tyczka_undulacja = []
for i in dobreg:
    dobreg_tyczka_undulacja.append(i + tyczka + undulacja)

dtu = 0
glebokoscibzw = []
for i in dobreg_tyczka_undulacja:
    glebokoscibzw.append(H[dtu]-i)
    dtu = dtu + 1

for i, x in enumerate(X):
    X[i] = round(x, 3)

for i, x in enumerate(Y):
    Y[i] = round(x, 3)

for i, x in enumerate(glebokoscibzw):
    glebokoscibzw[i] = round(x, 3)

wynik = []
idw = 0
for i in X:
    wynik.append([i, Y[idw], glebokoscibzw[idw]])
    idw = idw + 1

with open('Zakrzowek_6_6_11.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for i in wynik:
        csvwriter.writerow(i)

print (len(X))
print (f'zestawienie (X, Y, Dep): {wynik}')
print (f'X={X}')
print (f'Y={Y}')
print (f'Glbokosci bezwzgledne={glebokoscibzw}')