# arcpy scripts
Python scripts to automate geoprocessing of spatial data using arcpy or gdal.

ftp_watch.py :

establishes a connection with ftp and finds out if there are any new files available.


attrToSHP_N_Clip.py :

converts each attribute into a seperate shp file and for each output it clips another shp file to its boudnary.


Dissolve_Intersect.py :

- converts level-3 classification attribute entry to level-1 and performs dissolve process on every shapefile.
- calculates area of every feature
- intersects the (n)th year LULC shp file with the (n+1)th year.
- generates the pivot table presenting the area changes between classes and exports them as csv file.


Mosaic.py :

removes the '0' values in bands and mosaic the tif files of corresponding project years.


gdalbuildvrt.py :

since Mosaic.py takes tremendous amount of time and space, GDAL virtual raster (VRT) format is used to mosaic the tif files of corresponding project years.
