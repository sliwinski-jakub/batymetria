import pandas as pd
import csv


data = pd.read_csv(input("Podaj nazwe pliku csv z danymi z pomiaru batymetrycznego: "))
print(data.head())
depth = data['Depth'].to_list()
time = data['TimeOffset[ms]'].to_list()

datagps = pd.read_csv(input("Podaj nazwe pliku csv z danymi z pomiaru GPS: "))
print(datagps.head())
X = datagps['X'].to_list()
Y = datagps['Y'].to_list()
H = datagps['H'].to_list()
czas = datagps['czas'].to_list()

XYgps = []
ngps = 0
for i in X:
    XYgps.append([i, Y[ngps]])
    ngps = ngps + 1

tyczka = float(input("Podaj dlugosc tycznki anteny GPS [m]: "))
undulacja = 39.934

d = []
for i in depth:
    d.append(i*0.3048)


podany_czas = int(input("Wprowadz numer soundingu o znanej godzinie: "))
godzina = str(input("Wprowadz godzine pomiaru (gg:mm:ss): "))
g = 10*float(godzina[0]) + float(godzina[1])
m = 10*float(godzina[3]) + float(godzina[4])
s = 10*float(godzina[6]) + float(godzina[7])
cz = (g*3600)+(m*60)+s

time0 = []
for i in time:
    time0.append(i/1000)

time_podany = time0[podany_czas - 1]
czas_poczatku_pomiaru = cz - time_podany

sdeptx = []
for i in time0:
    sdeptx.append(czas_poczatku_pomiaru + i)

gl_czdict = {}
n=0
for i in sdeptx:
    gl_czdict[i] = d[n]
    n = n + 1

sgps = []
for i in czas:
    g0 = float(i[11])
    g1 = float(i[12])
    m3 = float(i[14])
    m4 = float(i[15])
    s6 = float(i[17])
    s7 = float(i[18])
    sgps.append(((10*g0+g1)*3600)+((10*m3+m4)*60)+(10*s6+s7))

ns = 0
XY_czdict = {}
for i in sgps:
    XY_czdict[i] = XYgps[ns]
    ns = ns + 1

nsh = 0
H_czdict = {}
for i in sgps:
    H_czdict[i] = H[nsh]
    nsh = nsh + 1

sdept = []
for i in sdeptx:
    if i >= min(sgps) and i <= max(sgps) + 1:
        sdept.append(i)

sgp = []
for i in sgps:
    if i >= min(sdeptx) and i <= max(sdeptx):
        sgp.append(i)

czasdict = {}
gpsId = 1
for gle in sdept:
    key = None
    if gpsId >= len(sgp) or gle <= sgp[gpsId]:
        key = sgp[gpsId - 1]
    else:
        key = sgp[gpsId]
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

dobreg_tyczka_undulacja = []
for i in sdep0:
    dobreg_tyczka_undulacja.append(gl_czdict[i] + tyczka + undulacja)

dtu = 0
glebokoscibzw = []
for i in sgp:
    glebokoscibzw.append(H_czdict[i] - dobreg_tyczka_undulacja[dtu])
    dtu = dtu + 1

wynik = []
idw = 0
for i in sgp:
    wynik.append([XY_czdict[i], glebokoscibzw[idw]])
    idw = idw + 1

with open(input("Podaj nazwe pliku .csv, do ktorego zapisac wynik: "), 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for i in wynik:
        csvwriter.writerow(i)

with open('Zbiorczy.csv', 'a', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for i in wynik:
        csvwriter.writerow(i)

print (f'zestawienie: {wynik}')
print (f'Glbokosci bezwzgledne={glebokoscibzw}')