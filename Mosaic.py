import os
from arcpy import env
from arcpy.sa import *
import datetime

project_year = ["2013_14", "2014_15", "2015_16", "2016_17", "2017_18"]

now=datetime.datetime.now()
date=now.strftime("%Y%m%d")

backgroundRemoved = {
  "2013_14": "BackgroundRemoved1314",
  "2014_15": "BackgroundRemoved1415",
  "2015_16": "BackgroundRemoved1516",
  "2016_17": "BackgroundRemoved1617",
  "2017_18": "BackgroundRemoved1718",
}

mosaicPath = r"D:\Mosaic"
dataPath = r"D:\Data"

for year in project_year:
  outws = os.path.join(mosaicPath, backgroundRemoved[year])
  env.workspace = outws
  removedlist = arcpy.ListDatasets("*", "Raster")

  env.workspace = os.path.join(dataPath, year)
  rasterlist = arcpy.ListDatasets("*", "Raster")

  for i in rasterlist:
    if not i in removedlist:
      outname = os.path.splitext(str(i))[0]
      print (outname)
      outnamepath = os.path.join(outws, outname + '.tif')
      arcpy.CopyRaster_management( i , outnamepath ,"","0","0","","","8_BIT_UNSIGNED")

  env.workspace = outws
  tifflist = arcpy.ListDatasets("*", "Raster")

  input = ""
  for filename in tifflist:
    assign = filename + ";"
    input += assign
  outputname = date + "_" + year + '.tif'

  try:
    arcpy.MosaicToNewRaster_management( input , mosaicPath , outputname , "", "8_BIT_UNSIGNED", "", "3", "LAST","FIRST")
  except:
    print("An exception occurred")
