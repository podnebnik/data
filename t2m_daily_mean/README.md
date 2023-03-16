How to use the 2m temperature package?

1. Set up Climate Data Store (CDS) API:
https://cds.climate.copernicus.eu/api-how-to 

2. Install Climate Data Operators (CDO):
https://code.mpimet.mpg.de/projects/cdo/wiki 
https://anaconda.org/conda-forge/cdo 

3. Install xarray (to open netcdf files):
https://anaconda.org/anaconda/xarray 

4. Install Dask:
https://anaconda.org/conda-forge/dask

5. Set up a cron-job for 
a) daily download of ERA5 reanalysis data up to day t-7, which updates NetCDF files in ./sources:
./scripts/download_daily_data.py

b) constructing the time series and saving them to .csv files in ./data:
./scripts/construct_time_series.py

c) plotting the data, saved in ./data:
./scripts/plot.py
