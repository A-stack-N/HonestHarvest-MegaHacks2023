from math import *
import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import folium
from folium.plugins import FastMarkerCluster

def user_location():
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRRQM5KaU47g-eAlk8lZ2pcB0Y-IH34czV7sz6QzAXIFvUDBD-lDJpHudskKtz2ofcqhf3jTh__8NG4/pub?output=csv")

    df['city'] = df["What city do you live in(ex. Mountain House)?"]
    df['state'] = df['What state do you live in(US)?']
    df['produce'] = df['What produce are you interested in?']
    df['phone'] = df['What is your phone number?']
    df['hear'] = df['How did you hear about us?']
    df['gmail'] = df['Please enter your email below']

    df['ADDRESS'] = df['city'].astype(str) + ',' + \
                    df['state'] + ',' + ' United States'

    #1 - convienient function to delay between geocoding calls
    #To make sure program doesnt crash with large amount addresses
    locator = Nominatim(user_agent="my_user_agent")
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    df['location'] = df['ADDRESS'].apply(geocode)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    #4 - split point column into longitude, latitude, and altitude columns
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index = df.index)
    #clean out unwanted columns 
    df = df.drop(['gmail', 'city', 'state', 'produce', 'hear', 'phone', 'ADDRESS', 'location', 'point', 'altitude'], axis=1)
    dfresult = df.dropna()

    df1 = dfresult.iloc[-1]
    lat1 = df1.loc['latitude']
    lon1 = df1.loc['longitude']
    return lat1, lon1


def farmer_location():
    fdf = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vTwlgb2JXMH1hkE9tQhLOCNHc2RvtoLEhyabNDvTFilSKJo3bn3IYj4ryRuIFrMrBmYMFnN2I1yJ7yi/pub?output=csv")

    fdf['city'] = fdf["What city do you live in(ex. Mountain House)?"]
    fdf['state'] = fdf['What state do you live in(US)?']
    fdf['produce'] = fdf['What produce are you interested in selling?']
    fdf['phone'] = fdf['What is your phone number?']
    fdf['hear'] = fdf['How did you hear about us?']
    fdf['gmail'] = fdf['Please enter your email below']

    fdf['ADDRESS'] = fdf['city'].astype(str) + ',' + \
                    fdf['state'] + ',' + ' United States'
    
    locator = Nominatim(user_agent="my_user_agent")
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    fdf['location'] = fdf['ADDRESS'].apply(geocode)
    fdf['point'] = fdf['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    #4 - split point column into longitude, latitude, and altitude columns
    fdf[['latitude', 'longitude', 'altitude']] = pd.DataFrame(fdf['point'].tolist(), index = fdf.index)
    #clean out unwanted columns 
    fdf = fdf.drop(['gmail', 'city', 'state', 'produce', 'hear', 'phone', 'ADDRESS', 'location', 'point', 'altitude'], axis=1)
    fdfresult = fdf.dropna()

    fdf1 = fdfresult.iloc[-1]
    lat2 = fdf1.loc['latitude']
    lon2 = fdf1.loc['longitude']
    return lat2, lon2

lat1, lon1 = user_location()
lat2, lon2 = farmer_location()

def distance(lat1, lon1, lat2, lon2):
  def haversin(x):
    return sin(x/2)**2 
  return 2 * asin(sqrt(
      haversin(lat2-lat1) +
      cos(lat1) * cos(lat2) * haversin(lon2-lon1)))*775.6
print("Distance is " + str(distance(lat1, lon1, lat2, lon2)) + " miles.")

user_location()
farmer_location()