import requests
import json
from geopy.distance import great_circle

ecole = input("École ?\n")

rEcole=requests.get('https://api.opendata.onisep.fr/downloads/57da952417293/57da952417293.json')
json_data=json.loads(rEcole.text)
try:
    for val in json_data:
        if(val['sigle']==ecole):
            long=val['longitude_x']
            lat=val['latitude_y']
    coor_ecole = (float(lat), float(long))
    dist=100000
except:
    print("Etablissement non trouvé")

payload={'lat':lat, 'lng':long, 'fDstL':'0', 'fDstU':'50'}
r = requests.get('https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json', params=payload)
json_data = json.loads(r.text)

try:
    print("\nCalcul de l'avion le plus proche\n")
    for val in json_data['acList']:
        latAvion = val['Lat']
        longAvion = val['Long']
        coor_avion = (float(latAvion),float(longAvion))
        dist_avion=great_circle(coor_ecole, coor_avion).km
        if(dist_avion < dist):
            avionPlusProche=val
            dist=dist_avion
except:
    print("Pas d'avion dans un rayon de 50km")

print("L'avion le plus proche de "+ecole+" avec une distance de "+str(dist)+" :\n")
try:
    print('Identifiant : '+avionPlusProche['Icao'])
except:
    pass
try:
    print('Modèle : '+avionPlusProche['Mdl'])
except:
    pass
try:
    print('Compagnie aérienne : '+avionPlusProche['Op'])
except:
    pass
try:
    print('De : '+avionPlusProche['From'])
except:
    pass
try:
    print('Vers : '+avionPlusProche['To'])
except:
    pass
