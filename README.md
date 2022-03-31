# WRF
This dataset will be updated automatically every six hours.

This program will download the WRF forecast data in grib2 format from the Central Weather Bureau's API.
https://data.gov.tw/dataset/58977

Then the following data will be extracted by using pygrib and converted to csv files and stored in the csv folder

Temperature_level_2: Temperature at 2 meters above ground
Dew_point_temperature_level_2: Dew point at 2 meters above the ground
Relative_humidity_level_2: Relative humidity at 2 meters above ground
Total_precipitation_level_0: Total Precipitation
u-component_of_wind_level_10: zonal wind velocity at 10 m (Wu)
v-component_of_wind_level_10: meridional wind velocity at 10 m (Wv)
Net_short-wave_radiation_flux_(surface): Solar irradiance(W/m^2)
