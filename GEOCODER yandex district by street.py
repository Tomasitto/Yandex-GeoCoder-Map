
import requests # библиотека нужна для обращения к api
import json # библиотека нужна для конвертации XML в JSON
from pprint import pprint
import folium




#запишем полученный ключ для геокодера
key = '4b9fa08d-4d0b-4614-bf1a-5c39c0e23117'
params = { # словарь с параметрами запроса
    "format" : "json", # определяем формат ответа на запрос
}
sp = []
sp_name = []
# https://geocode-maps.yandex.ru/1.x/?apikey=a7c43a59-6515-48e0-84f2-2264750cf238&geocode=Москва, Дмитровское шоссе
def mapmaker(address):
    #создадим url для запроса координат
    url = 'https://geocode-maps.yandex.ru/1.x/?apikey=' + key + '&geocode=Москва, ' + address
     
    #сделаем запрос к геокодеру
    response = requests.get(url, params=params)
    #получим координаты точки
    coord = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
 
    #создадим url для запроса по координатам
    url_coord = 'https://geocode-maps.yandex.ru/1.x/?apikey=' + key + '&geocode=' + coord
 
    #делаем запрос по координатам
    response_coord = requests.get(url_coord, params=params)
    #pprint(response_coord.json())
    #получаем район из результатов запроса
    try:
        district = response_coord.json()['response']['GeoObjectCollection']['featureMember'][1]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['Locality']['DependentLocality']['DependentLocality']['DependentLocalityName']
        sp.append(response_coord.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'])
        sp_name.append(address)
    except:
           district = 'Данные отсутствуют'
    return district, sp, sp_name

m = ['проспект Мира',
'Профсоюзная улица',
'Ленинградский проспект',
'Пресненская набережная'
'Варшавское шоссе',
'Ленинский проспект',
'проспект Вернадского',
'Кутузовский проспект',
'Каширское шоссе',
'Кировоградская улица']

for i in m:
    mapmaker(i)

m = folium.Map(location=[55.7512, 37.618423], zoom_start=10, tiles="Stamen Terrain")

tooltip = "Click me!"
print(sp)
sp_2 = []
sp_f = []
print(len(sp))
for i in range(len(sp)):
    a = sp[i].split()
    c_0 = float(a[1])
    c_1 = float(a[0])
    sp_2.append(c_0)
    sp_2.append(c_1)
    sp_f.append(sp_2)
    sp_2 =[]

print(sp_f)
print(sp_name)
for i in range(len(sp_f)):
    folium.Marker(sp_f[i], popup = sp_name[i], tooltip = tooltip).add_to(m)

m
