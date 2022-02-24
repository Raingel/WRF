# %%
from datetime import timedelta
import pygrib
import pandas as pd
import requests
import os
import re
import shutil
# %%
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-A",
                    "--API",
                    type=str,
                    default="",
                    help="CWB API key")

#jupyter會傳一個-f進來，不這樣接會有錯誤
args, unknown = parser.parse_known_args()

# %%
ROOT = './'
API_KEY=args.API
WRF_datalist = [
             'M-A0064-000',
             'M-A0064-006',
             'M-A0064-012',
             'M-A0064-018',
             'M-A0064-024',
             'M-A0064-030',
             'M-A0064-036',
             'M-A0064-042',
             'M-A0064-048',
             'M-A0064-054',
             'M-A0064-060',
             'M-A0064-066',
             'M-A0064-072',
             'M-A0064-078',
             'M-A0064-084'
]
PARSE_LIST=[62,63,64,66,67,68,76]

# %%
GRB_URIs = []
for s in WRF_datalist[:]:
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/{}?Authorization={}&downloadType=WEB&format=JSON'.format(s,API_KEY)
    r = requests.get(url)
    print (s, 'json loaded')
    GRB_URI=r.json()['cwbopendata']['dataset']['resource']['uri']
    GRB_URIs.append(GRB_URI)
    print ('got GRB URI', GRB_URI)

# %%
for GRB_URI in GRB_URIs:
    for i in range(0,10):
        #Try 10 times
        print ('try', i+1)
        try:
            grb_data = requests.get(GRB_URI)
            grb_path = os.path.join(ROOT,'grib',GRB_URI[-8:])
            with open(grb_path, 'wb') as f:
                f.write(grb_data.content)
            print (s, ' downloaded')
            break #leave loop if download successfully
        except Exception as e:
            print (s, e)

# %%
def grb_to_csv(grb, grb_name):
    result = grb.values
    lats, lons = grb.latlons()
    pd.DataFrame(lats).to_csv(os.path.join(ROOT,'csv',grb_name+'_lats.csv'), index=False)
    pd.DataFrame(lons).to_csv(os.path.join(ROOT,'csv',grb_name+'_lons.csv'), index=False)
    pd.DataFrame(result).to_csv(os.path.join(ROOT,'csv',grb_name+'_value.csv'), index=False)

# %%
#regenerate csv dir
shutil.rmtree(os.path.join(ROOT,'csv'))
os.mkdir(os.path.join(ROOT,'csv'))
#scan grib dir
for f in os.scandir(ROOT+"grib"):
    if f.name[-4:] == 'grb2':
        grbs = pygrib.open(f.path)
        for grb in grbs:
            grb_name = "{}_level_{}_fcst_{}_valid_{}{}".format(grb['parameterName'].replace(' ','_'), grb['level'], grb['forecastTime'],grb['validityDate'],grb['validityTime'])
            grb_no = re.search('^([0-9]{1,2}):', str(grb)).group(1)
            #print (grb['parameterName'], grb['level'], grb['forecastTime'])
            if int(grb_no) in PARSE_LIST:
                grb_to_csv(grb, grb_name)
            print(grb_name, 'converted')

# %%



# %%



