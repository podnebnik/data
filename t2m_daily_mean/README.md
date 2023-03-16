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

5. Set up a cron-job for daily download of ERA5 reanalysis data up to day (t-7), where (t) is today:
./scripts/download_daily_data.py

6. Construct time series by running:
./scripts/construct_time_series.py

7. Plot the data, saved in ./data/ using:
./scripts/plot.py

Here, Slovenia is represented by mere 39 grid-points on  regular latitude-longitude grid with 0.25° resolution, which are located within the national boundaries (figure below). The treatment of the area near the boundaries could be performed more accurately, however, the results are not expected to differ much, except for some mild temperature shift. For example, another figure shows that the temperatures are very highly correlated even if we compare the current representation of Slovenia by representation with a boundary-enclosing box. 
