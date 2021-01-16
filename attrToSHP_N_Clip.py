import arcpy
import os
from arcpy import env  
from arcpy.sa import *

inputFile = u"E:\\Project.shp"
outDir = u"E:\\Data\\Project\\"

rows = arcpy.SearchCursor(inputFile)
row = rows.next()
attribute_values = set([])

while row:
    attribute_values.add(row.attrib_name)
    row = rows.next()

for each_attribute in attribute_values:
    outSHP = outDir + each_attribute + u"_bnd" + u".shp"
    print outSHP
    arcpy.Select_analysis (inputFile, outSHP, "\"attrib_name\" = '" + each_attribute + "'")

env.workspace = outDir
exportDir = r"E:\Data\Project_MWS"
input = r"E:\MWS.shp"

shpList = arcpy.ListFeatureClasses()

for file in shpList:
	name = exportDir + "\\" + os.path.splitext(str(file))[0].split('_b')[0] + "_MWS" + ".shp"
	print (name)
	arcpy.Clip_analysis(input, file, name)

print ("completed")
del rows, row, attribute_values, shpList