import geopandas as gpd
import geopy
import pandas as pd

def get_zip_code(point, geolocator):
    location = geolocator.reverse(f"{point.y}, {point.x}")
    print(location.raw['address']['postcode'])
    return location.raw['address']['postcode']

def parseDataFile(filename: str):
  data = gpd.read_file(filename)

  data["beschikbare_capaciteit_invoeding_huidig_mva"] = pd.to_numeric(data['beschikbare_capaciteit_invoeding_huidig_mva'],errors='coerce')
  data["beschikbare_capaciteit_afname_huidig_mva"] = pd.to_numeric(data['beschikbare_capaciteit_afname_huidig_mva'],errors='coerce')


  isExist = data["status"] != "Gepland, locatie onbekend"
  isInvoeding = data["beschikbare_capaciteit_invoeding_huidig_mva"].notnull() 
  isAfname = data["beschikbare_capaciteit_afname_huidig_mva"].notnull() 
  isInvoedingGd0 = data["beschikbare_capaciteit_invoeding_huidig_mva"] > 0
  isAfnameGd0 = data["beschikbare_capaciteit_afname_huidig_mva"] > 0

  data = data[isExist]
  data = data[isInvoeding]
  data = data[isAfname]
  data = data[isInvoedingGd0]
  data = data[isAfnameGd0]

  data = data.to_crs(epsg=4326)

  geolocator = geopy.Nominatim(user_agent="check_1")
  data["zip_code"] = data.apply(lambda x: get_zip_code(x.geometry.centroid, geolocator), axis=1)

  csv_data = data.to_csv().replace("POINT ", "")
  #write data to file:
  with open("test.csv", "w") as f:
    f.write(csv_data)


if __name__ == "__main__":
  parseDataFile("beschikbare_capaciteit_elektriciteitsnet.gpkg")

'git commit -m "updated CSV" fundata.csv'