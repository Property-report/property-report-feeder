from jinja2 import Environment, FileSystemLoader
from src import config
from src.views.upload_document import document_upload
import os
from datetime import datetime
from urllib.request import urlretrieve
import pdfkit
import pdfrw
import requests
from PIL import Image


def create_pdf_report_external(report_id, json_data, data):

    pdf_template = json_data.get("pdf_name", "")
    address = json_data.get("address", "")
    longitude = json_data.get('lon')
    latitude = json_data.get('lat')
    headervalue = json_data.get('headervalue')
    headingvaluefound = json_data.get('headingvaluefound')

    longitude = data.get('lon')
    latitude = data.get('lat')
    get_polygon_info = data.get('get_polygon_info',{}).get('map_url')
    historical_floods_image = data.get('get_polygon_info',{}).get('historical_floods_image')

    if headingvaluefound == "true":
        url = f'https://maps.googleapis.com/maps/api/streetview?size=1000x1000&location={latitude},{longitude}&heading=90&pitch=-5&key=AIzaSyCiO1aQT1C_5Mh5rVXrMs2G7X3WfKKTQxY'
        url1 = f'https://maps.googleapis.com/maps/api/streetview?size=1000x1000&location={latitude},{longitude}&heading=180&pitch=-5&key=AIzaSyCiO1aQT1C_5Mh5rVXrMs2G7X3WfKKTQxY'
        url2 = f'https://maps.googleapis.com/maps/api/streetview?size=1000x1000&location={latitude},{longitude}&heading=270&pitch=-5&key=AIzaSyCiO1aQT1C_5Mh5rVXrMs2G7X3WfKKTQxY'
        url3 = f'https://maps.googleapis.com/maps/api/streetview?size=1000x1000&location={latitude},{longitude}&heading=360&pitch=-5&key=AIzaSyCiO1aQT1C_5Mh5rVXrMs2G7X3WfKKTQxY'
        urlpov = f'https://maps.googleapis.com/maps/api/streetview?size=1000x1000&location={latitude},{longitude}&heading={headervalue}&pitch=-5&key=AIzaSyCiO1aQT1C_5Mh5rVXrMs2G7X3WfKKTQxY'

        urlretrieve(
            url, f"/opt/src/views/templates/pdf_templates/streetmapimage.jpeg")
        urlretrieve(
            url1, f"/opt/src/views/templates/pdf_templates/streetmapimage1.jpeg")
        urlretrieve(
            url2, f"/opt/src/views/templates/pdf_templates/streetmapimage2.jpeg")
        urlretrieve(
            url3, f"/opt/src/views/templates/pdf_templates/streetmapimage3.jpeg")

        urlretrieve(
            urlpov, f"/opt/src/views/templates/pdf_templates/streeimagepov.jpeg")
    else:
        url = None
        url1 = None
        url2 = None
        url3 = None
        urlpov = None

    if get_polygon_info != None:
        urlretrieve(
            get_polygon_info, f"/opt/src/views/templates/pdf_templates/polygonimage.jpeg")

    if historical_floods_image != None:
        image = Image.open(historical_floods_image)
        image.save('/opt/src/views/templates/pdf_templates/historical_floods.png', 'PNG')

    home_mark = f'markers=color:blue%7Clabel:H%7C{latitude},{longitude}'

    # Your API key
    api_key = 'AIzaSyDBkRCuc0YSSUH3use_T6Rtu8NDauUshjo'
    # Other parameters for the API request
    zoom = 14
    size = '600x300'

    locationscafe = []
    if data.get('cafes', {}).get('results', []) != []:
        cafeno = 1
        for cafe in data.get('cafes', {}).get('results', []):
            locationscafe.append({"lat": cafe['geometry']['location']['lat'],
                                 "lng": cafe['geometry']['location']['lng'], 'label': str(cafeno)})
            cafe.update({"number": cafeno})
            cafeno = cafeno+1

    if locationscafe != []:
        min_lat = min(location['lat'] for location in locationscafe)
        max_lat = max(location['lat'] for location in locationscafe)
        min_lng = min(location['lng'] for location in locationscafe)
        max_lng = max(location['lng'] for location in locationscafe)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in locationscafe])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/mapcafe.png', 'wb') as f:
            f.write(response.content)

    locationssupermarkets = []
    if data.get('supermarkets', {}).get('results', []) != []:
        supermarketsno = 1
        for cafe in data.get('supermarkets', {}).get('results', []):
            locationssupermarkets.append(
                {"lat": cafe['geometry']['location']['lat'], "lng": cafe['geometry']['location']['lng'], 'label': str(supermarketsno)})
            cafe.update({"number": supermarketsno})
            supermarketsno = supermarketsno+1

    if locationssupermarkets != []:

        min_lat = min(location['lat'] for location in locationssupermarkets)
        max_lat = max(location['lat'] for location in locationssupermarkets)
        min_lng = min(location['lng'] for location in locationssupermarkets)
        max_lng = max(location['lng'] for location in locationssupermarkets)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers

        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in locationssupermarkets])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/mapsmarkets.png', 'wb') as f:
            f.write(response.content)

    locationrestaraunts = []
    if data.get('restaraunts', {}).get('results', []) != []:
        restarauntsno = 1
        for gym in data.get('restaraunts', {}).get('results', []):
            locationrestaraunts.append(
                {"lat": gym['geometry']['location']['lat'], "lng": gym['geometry']['location']['lng'], 'label': str(restarauntsno)})
            gym.update({"number": restarauntsno})
            restarauntsno = restarauntsno+1

    if locationrestaraunts != []:
        min_lat = min(location['lat'] for location in locationrestaraunts)
        max_lat = max(location['lat'] for location in locationrestaraunts)
        min_lng = min(location['lng'] for location in locationrestaraunts)
        max_lng = max(location['lng'] for location in locationrestaraunts)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in locationrestaraunts])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/maprestaraunts.png', 'wb') as f:
            f.write(response.content)

    if data.get('lon_lat', {}) != {}:

        zoom = 14
        size = '600x300'

        # Construct the URL for the API request with markers

        url = f"https://maps.googleapis.com/maps/api/staticmap?center={data['lon_lat']['latitude']},{data['lon_lat']['longitude']}&zoom={zoom}&size={size}&markers=color:blue%7C{data['lon_lat']['latitude']},{data['lon_lat']['longitude']}&key={api_key}"

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/maplocation.png', 'wb') as f:
            f.write(response.content)

    locationsschoolstate = []

    locationsschoolsindependant = []
    schoolsnoind = 1
    schoolsnostate = 1

    if data.get('nearby_schools', {}).get('independent', {}) != {}:
        for gym in data.get('nearby_schools', {}).get('independent', {}).get('Boarding', []):
            locationsschoolsindependant.append(
                {"lat": gym['lat'], "lng": gym['lng'], 'label': str(schoolsnoind)})
            gym.update({"number": schoolsnoind})
            schoolsnoind = schoolsnoind+1

        for gym in data.get('nearby_schools', {}).get('independent', {}).get('Day', []):
            locationsschoolsindependant.append(
                {"lat": gym['lat'], "lng": gym['lng'], 'label': str(schoolsnoind)})
            gym.update({"number": schoolsnoind})
            schoolsnoind = schoolsnoind+1

    if data.get('nearby_schools', {}).get('state', {}) != {}:
        for gym in data.get('nearby_schools', {}).get('state', {}).get('Primary', []):
            locationsschoolstate.append(
                {"lat": gym['lat'], "lng": gym['lng'], 'label': str(schoolsnostate)})
            gym.update({"number": schoolsnostate})
            schoolsnostate = schoolsnostate+1

        for gym in data.get('nearby_schools', {}).get('state', {}).get('Secondary', []):
            locationsschoolstate.append(
                {"lat": gym['lat'], "lng": gym['lng'], 'label': str(schoolsnostate)})
            gym.update({"number": schoolsnostate})
            schoolsnostate = schoolsnostate+1

    if locationsschoolsindependant != []:

        min_lat = min(location['lat']
                      for location in locationsschoolsindependant)
        max_lat = max(location['lat']
                      for location in locationsschoolsindependant)
        min_lng = min(location['lng']
                      for location in locationsschoolsindependant)
        max_lng = max(location['lng']
                      for location in locationsschoolsindependant)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in locationsschoolsindependant])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/mapschoolsindependant.png', 'wb') as f:
            f.write(response.content)

    if locationsschoolstate != []:

        min_lat = min(location['lat'] for location in locationsschoolstate)
        max_lat = max(location['lat'] for location in locationsschoolstate)
        min_lng = min(location['lng'] for location in locationsschoolstate)
        max_lng = max(location['lng'] for location in locationsschoolstate)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in locationsschoolstate])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/mapschoolstate.png', 'wb') as f:
            f.write(response.content)

    locationsgyms = []
    if data.get('gyms', {}).get('results', []) != []:
        gymsno = 1
        for gym in data.get('gyms', {}).get('results', []):
            locationsgyms.append({"lat": gym['geometry']['location']['lat'],
                                 "lng": gym['geometry']['location']['lng'], 'label': str(gymsno)})
            gym.update({"number": gymsno})
            gymsno = gymsno+1

    if locationsgyms != []:

        min_lat = min(location['lat'] for location in locationsgyms)
        max_lat = max(location['lat'] for location in locationsgyms)
        min_lng = min(location['lng'] for location in locationsgyms)
        max_lng = max(location['lng'] for location in locationsgyms)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in locationsgyms])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/mapgym.png', 'wb') as f:
            f.write(response.content)

    locationspost_office = []
    if data.get('post_offcies', {}).get('results', []) != []:
        post_officeo = 1
        for gym in data.get('post_offcies', {}).get('results', []):
            locationspost_office.append(
                {"lat": gym['geometry']['location']['lat'], "lng": gym['geometry']['location']['lng'], 'label': str(post_officeo)})
            gym.update({"number": post_officeo})
            post_officeo = post_officeo+1

    if locationspost_office != []:

        min_lat = min(location['lat'] for location in locationspost_office)
        max_lat = max(location['lat'] for location in locationspost_office)
        min_lng = min(location['lng'] for location in locationspost_office)
        max_lng = max(location['lng'] for location in locationspost_office)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in locationspost_office])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/mappostoffice.png', 'wb') as f:
            f.write(response.content)

    buslist = []
    if data.get('get_bus_and_tubes', []) != []:
        busno = 1
        for gym in data.get('get_bus_and_tubes', []):
            if gym['type'] == "bus_stop":
                buslist.append(
                    {"lat": gym['latitude'], "lng": gym['longitude'], 'label': str(busno)})
                gym.update({"number": busno})
                busno = busno+1
    if buslist != []:
        min_lat = min(location['lat'] for location in buslist)
        max_lat = max(location['lat'] for location in buslist)
        min_lng = min(location['lng'] for location in buslist)
        max_lng = max(location['lng'] for location in buslist)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in buslist])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/mapbuses.png', 'wb') as f:
            f.write(response.content)

    trainlist = []
    if data.get('get_train_stations', []) != []:
        trainno = 1
        for gym in data.get('get_train_stations', []):
            trainlist.append(
                {"lat": gym['latitude'], "lng": gym['longitude'], 'label': str(trainno)})
            gym.update({"number": trainno})
            trainno = trainno+1

    if trainlist != []:

        min_lat = min(location['lat'] for location in trainlist)
        max_lat = max(location['lat'] for location in trainlist)
        min_lng = min(location['lng'] for location in trainlist)
        max_lng = max(location['lng'] for location in trainlist)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in trainlist])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/maptrain.png', 'wb') as f:
            f.write(response.content)

    tubes = False
    tubelist = []
    if data.get('get_bus_and_tubes', []) != []:
        tubeno = 1
        for gym in data.get('get_bus_and_tubes', []):
            if gym['type'] == "tube_station":
                tubelist.append(
                    {"lat": gym['latitude'], "lng": gym['longitude'], 'label': str(tubeno)})
                gym.update({"number": tubeno})
                tubeno = tubeno+1
                tubes = True

    if tubelist != []:
        min_lat = min(location['lat'] for location in tubelist)
        max_lat = max(location['lat'] for location in tubelist)
        min_lng = min(location['lng'] for location in tubelist)
        max_lng = max(location['lng'] for location in tubelist)
        path = f'{min_lat},{min_lng}|{min_lat},{max_lng}|{max_lat},{max_lng}|{max_lat},{min_lng}|{min_lat},{min_lng}'

        # Construct the URL for the API request with markers
        markers = '&'.join(
            [f'markers=color:red%7Clabel:{location["label"]}%7C{location["lat"]},{location["lng"]}' for location in tubelist])
        url = f'https://maps.googleapis.com/maps/api/staticmap?size={size}&path=color:0x0000ff|weight:1|fillcolor:0xFFFF0033|{path}&key={api_key}&{markers}&{home_mark}'

        # Make the GET request and save the image
        response = requests.get(url)
        with open('/opt/src/views/templates/pdf_templates/maptube.png', 'wb') as f:
            f.write(response.content)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    data.update(address)
    # shutil.copy(f"{config.doc_location}pdf_templates/{template_name}.pdf", f"{config.doc_location}pdf_templates_copy/")
    create_pdf_report(f"{pdf_template}.html", data, f"/opt/src/views/templates/pdf_templates/{report_id}.pdf",
                      json_data['logo_url'], headingvaluefound, get_polygon_info, historical_floods_image, tubes)

    upload = document_upload(
        'property_reports', f"/opt/src/views/templates/pdf_templates/{report_id}.pdf", report_id, "pdf")

    os.remove(
        f"/opt/src/views/templates/pdf_templates/{report_id}.pdf")
    if headingvaluefound == "true":

        os.remove(
            f"/opt/src/views/templates/pdf_templates/streetmapimage.jpeg")
        os.remove(
            f"/opt/src/views/templates/pdf_templates/streetmapimage1.jpeg")
        os.remove(
            f"/opt/src/views/templates/pdf_templates/streetmapimage2.jpeg")
        os.remove(
            f"/opt/src/views/templates/pdf_templates/streetmapimage3.jpeg")
        os.remove(
            f"/opt/src/views/templates/pdf_templates/streeimagepov.jpeg")
    if get_polygon_info != None:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/polygonimage.jpeg")
    if historical_floods_image != None:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/historical_floods.jpeg")
    if locationscafe != []:

        os.remove(
            f"/opt/src/views/templates/pdf_templates/mapcafe.png")
    if locationssupermarkets != []:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/mapsmarkets.png")
    if locationsgyms != []:
        os.remove(f"/opt/src/views/templates/pdf_templates/mapgym.png")

    if locationspost_office != []:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/mappostoffice.png")
    if locationrestaraunts != []:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/maprestaraunts.png")
    if tubelist != []:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/maptube.png")
    if trainlist != []:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/maptrain.png")
    if buslist != []:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/mapbuses.png")
    if locationsschoolstate != []:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/mapschoolstate.png")

    if locationsschoolsindependant != []:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/mapschoolsindependant.png")

    if data.get('lon_lat', {}) != {}:
        os.remove(
            f"/opt/src/views/templates/pdf_templates/maplocation.png")

    return True


def create_pdf_report(input_pdf_path, data, output_pdf_path, logo, headerfound, polygonimagemap, historical_floods, tubes):
    if data.get('lon_lat') != {}:
        if headerfound == "true":
            street_image_url = f"/opt/src/views/templates/pdf_templates/streetmapimage.jpeg"
            street_image_url2 = f"/opt/src/views/templates/pdf_templates/streetmapimage1.jpeg"
            street_image_url3 = f"/opt/src/views/templates/pdf_templates/streetmapimage2.jpeg"
            street_image_url4 = f"/opt/src/views/templates/pdf_templates/streetmapimage3.jpeg"
            streeimagepov = f"/opt/src/views/templates/pdf_templates/streeimagepov.jpeg"

        else:
            street_image_url = None
            street_image_url2 = None
            street_image_url3 = None
            street_image_url4 = None
            streeimagepov = None
    if polygonimagemap != None:
        polygonimage = f"/opt/src/views/templates/pdf_templates/polygonimage.jpeg"
    else:
        polygonimage = None
    if historical_floods != None:
        historicalflood_image = f"/opt/src/views/templates/pdf_templates/historical_floods.jpeg"
    else:
        historicalflood_image = None
    mapcafe = f"/opt/src/views/templates/pdf_templates/mapcafe.png"
    mapsmarkets = f"/opt/src/views/templates/pdf_templates/mapsmarkets.png"
    mapgym = f"/opt/src/views/templates/pdf_templates/mapgym.png"
    mappostoffice = f"/opt/src/views/templates/pdf_templates/mappostoffice.png"
    maprestaraunts = f"/opt/src/views/templates/pdf_templates/maprestaraunts.png"
    maptrain = f"/opt/src/views/templates/pdf_templates/maptrain.png"
    mapschoolstate = f"/opt/src/views/templates/pdf_templates/mapschoolstate.png"
    mapschoolsindependant = f"/opt/src/views/templates/pdf_templates/mapschoolsindependant.png"

    maptube = None
    if tubes != False:
        maptube = f"/opt/src/views/templates/pdf_templates/maptube.png"
    mapbuses = f"/opt/src/views/templates/pdf_templates/mapbuses.png"
    maplocation = f"/opt/src/views/templates/pdf_templates/maplocation.png"

    # Create the Jinja2 environment
    template_loader = FileSystemLoader(
        searchpath=f"{config.doc_location}/templates")
    env = Environment(loader=template_loader)

    # Load the template
    template = env.get_template(f'/pdf_templates/{input_pdf_path}')

    rendered_template = template.render(
        data=data,
        tubes=tubes,
        logo=logo,
        polygonimage=polygonimage,
        historicalflood_image=historicalflood_image,
        streeimagepov=streeimagepov,
        mapcafe=mapcafe,
        mapschoolsindependant=mapschoolsindependant,
        mapschoolstate=mapschoolstate,
        mapgym=mapgym,
        maptrain=maptrain,
        mapbuses=mapbuses,
        maplocation=maplocation,
        maptube=maptube,
        mappostoffice=mappostoffice,
        maprestaraunts=maprestaraunts,
        mapsmarkets=mapsmarkets,
        street_image_url=street_image_url,
        street_image_url2=street_image_url2,
        street_image_url3=street_image_url3,
        street_image_url4=street_image_url4,
        air_polution=f"{config.doc_location}/templates/pdf_templates/air-pollution.png",
        tax=f"{config.doc_location}/templates/pdf_templates/tax.png",
        suggestion=f"{config.doc_location}/templates/pdf_templates/suggestion.png",
        epcrating=f"{config.doc_location}/templates/pdf_templates/energy.png",
        listedbuildings=f"{config.doc_location}/templates/pdf_templates/listedbuildings.png",
        epcratingurl=f"{config.doc_location}/templates/pdf_templates/EPC-Graph.jpeg",
        get_build_cost=f"{config.doc_location}/templates/pdf_templates/get_build_cost.png",
        fullpropimage=f"{config.doc_location}/templates/pdf_templates/propreport.png",
        rent=f"{config.doc_location}/templates/pdf_templates/rent.png",
        housemapview=f"{config.doc_location}/templates/pdf_templates/house-street-view.png",
        mapview=f"{config.doc_location}/templates/pdf_templates/street-view.png",
        epc=f"{config.doc_location}/templates/pdf_templates/epc.png",
        house=f"{config.doc_location}/templates/pdf_templates/house.png",
        dentist=f"{config.doc_location}/templates/pdf_templates/tooth.png",
        wifi=f"{config.doc_location}/templates/pdf_templates/wifi.png",
        flood=f"{config.doc_location}/templates/pdf_templates/flood.png",
        management=f"{config.doc_location}/templates/pdf_templates/management.png",
        age_bamd=f"{config.doc_location}/templates/pdf_templates/age-band.png",
        gp=f"{config.doc_location}/templates/pdf_templates/gp.png",
        police=f"{config.doc_location}/templates/pdf_templates/police.png",
        pound=f"{config.doc_location}/templates/pdf_templates/pound.png",
        rental_demand=f"{config.doc_location}/templates/pdf_templates/rental_demand.png",
        planning=f"{config.doc_location}/templates/pdf_templates/planning.png",
        school=f"{config.doc_location}/templates/pdf_templates/school.png",
        transport=f"{config.doc_location}/templates/pdf_templates/transport.png",
        airport=f"{config.doc_location}/templates/pdf_templates/airport.png",
        post_office=f"{config.doc_location}/templates/pdf_templates/post-office.png",
        restaraunt=f"{config.doc_location}/templates/pdf_templates/restaraunt.png",
        cafe=f"{config.doc_location}/templates/pdf_templates/coffee-cup.png",
        gym=f"{config.doc_location}/templates/pdf_templates/dumbbell.png",
        supermarker=f"{config.doc_location}/templates/pdf_templates/food.png",
        location=f"{config.doc_location}/templates/pdf_templates/location.png",
        underground=f"{config.doc_location}/templates/pdf_templates/underground.png",
        bus=f"{config.doc_location}/templates/pdf_templates/bus.png",
        train=f"{config.doc_location}/templates/pdf_templates/train.png"

    )

    pdf = pdfkit.from_string(rendered_template, output_pdf_path)


def fill_pdf(input_pdf_path, output, data_dict):

    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        if annotations:
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        if key in data_dict.keys():
                            if type(data_dict[key]) == bool:
                                if data_dict[key] == True:
                                    annotation.update(pdfrw.PdfDict(
                                        AS=pdfrw.PdfName('Yes')))
                            else:
                                annotation.update(
                                    pdfrw.PdfDict(
                                        AP=data_dict[key], V='{}'.format(data_dict[key]))
                                )

                                annotation.update(pdfrw.PdfDict(AP=''))

    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(
        NeedAppearances=pdfrw.PdfObject('true')))
#   buf = io.BytesIO()
    pdfrw.PdfWriter().write(output, template_pdf)
#   buf.seek(0)
#   return template_pdf
