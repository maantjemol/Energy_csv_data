import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetchFundaData (postcode: str):
  postcode = postcode.lower()
  postcode = postcode.replace(" ", "")
  burp0_url = getUrl(postcode)
  burp0_headers = {"Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"104\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"macOS\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}
  fundata =requests.get(burp0_url, headers=burp0_headers)
  
  soup = BeautifulSoup(fundata.text, "html.parser")
  span = soup.select('span[data-instant-search-output="searchButtonTotal"]')
  if span:
    print(int(span[0].text.replace(" bouwgrond", "")), postcode)
    return int(span[0].text.replace(" bouwgrond", ""))
  else:
    print("no data")
    return 0



def getUrl(zip):
  zip = zip.lower()
  zip = zip.replace(" ", "")
  return f"https://www.fundainbusiness.nl/bouwgrond/{zip}/+5km/"

def updataData():
  df = pd.read_csv("test.csv")
  df["funda_url"] = df.apply(lambda x: getUrl(x["zip_code"]), axis=1)
  df["available"] = df.apply(lambda x: fetchFundaData(x["zip_code"]), axis=1)
  csv_data = df.to_csv()

  with open("fundata.csv", "w") as f:
    f.write(csv_data)

if __name__ == "__main__":
  updataData()