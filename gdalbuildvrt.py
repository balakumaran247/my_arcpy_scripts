from osgeo import gdal
import os, fnmatch, datetime

files = []

directory = r'D:\Mosaic\Project'

for dirpath,_,filenames in os.walk(directory):
    for f in filenames:
        if fnmatch.fnmatch(f, '*.tif'):
            files.append(os.path.abspath(os.path.join(dirpath, f)))

output = r'D:\Mosaic\reprojected'

expected_proj = 'PROJCS["WGS_1984_UTM_Zone_44N"'

for tif_file in files[:]:
    tif = gdal.Open(tif_file)
    proj = tif.GetProjectionRef().split(',')[0]
    dest_path = os.path.join(output, tif_file.split('\\')[-1].split('.')[0]+'_reproj.tif')
    if os.path.isfile(dest_path):
        files.remove(tif_file)
    if proj != expected_proj and not os.path.isfile(dest_path):
        gdal.Warp(dest_path, tif_file, dstSRS='EPSG:32644', format="GTiff", resampleAlg='near')
        files.remove(tif_file)
    tif = None

for dirpath,_,filenames in os.walk(output):
    for f in filenames:
        if fnmatch.fnmatch(f, '*.tif'):
            files.append(os.path.abspath(os.path.join(dirpath, f)))

now=datetime.datetime.now()
date=now.strftime("%Y%m%d")

vrt_options = gdal.BuildVRTOptions(resampleAlg='near')

vrt = os.path.join('D:\Mosaic', date + "_" + 'vrt' + '.vrt')

gdal.BuildVRT( vrt, files, options=vrt_options)
