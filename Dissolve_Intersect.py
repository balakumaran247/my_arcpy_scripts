import os
import arcpy
from arcpy import env
import pandas as pd
import os
import shutil
import numpy as np

no_of_terms = 5
year = "2009_10"
folder_name = "Project_2009_10"
t0_file = "Project_2009_10_T0"
t1_file = "Project_2009_10_T1"
t2_file = "Project_2009_10_T2"
t3_file = "Project_2009_10_T3"
t4_file = "Project_2009_10_T4"
t5_file = "Project_2009_10_T5"

drive_path = r"E:\Project"
env_path = r"C:\Users\HP\Desktop\dissolve\env"
env.workspace = env_path
out_path = r"C:\Users\HP\Desktop\dissolve\output"
rm_files = []

for filename in os.listdir(out_path):
    rm_files.append(os.path.join(out_path, filename))
for filename in os.listdir(env_path):
    rm_files.append(os.path.join(env_path, filename))

for file_path in rm_files:
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

original_files = [t0_file, t1_file, t2_file, t3_file, t4_file, t5_file]
for count in range(no_of_terms+1):
    original_file = original_files[count]
    term_name = "T"+str(count)
    o_path = os.path.join(drive_path, year, folder_name,
                            term_name, original_file+".shp")
    arcpy.CopyFeatures_management(o_path, original_file+".shp")

code_variants = {
    'Code_1': '!Code_1!',
    'Code_12': '!Code_12!',
    'Code_13': '!Code_13!',
    'Code_1_2': '!Code_1_2!',
}

inputList = arcpy.ListFeatureClasses()

for file in inputList:
    for i in arcpy.ListFields(file):
        if i.name in list(code_variants.keys()):
            arcpy.AddField_management(file, "Code", "TEXT")
            arcpy.CalculateField_management(
                file, "Code", code_variants[i.name], "PYTHON")
            arcpy.DeleteField_management(file, list(code_variants.keys()))
    arcpy.AddField_management(file, "Descrpn", "TEXT")
    expr = "getClass(!Code!)"
    codeblock = """def getClass(desc):
        agri_des=['AGCR','AGPL','AGAQ']
        bui_des=['BUMN','BURH','BURV','BUTP','BUUR','BURM','BURU','BUUC','BUUP']
        forest_des=['FRDE','FRPL','FRMG']
        water_des=['WBCN','WBLP','WBRS','WBRT']
        waste_des=['WLBR','WLGU','WLSA','WLSD','WLSP','WLST','WLWL']
        if desc in agri_des:
            return 'Agriculture'
        elif desc in bui_des:
            return 'Built'
        elif desc in forest_des:
            return 'Forest'
        elif desc in water_des:
            return 'WB_Water'
        elif desc in waste_des:
            return 'WL_Waste'
        else:
            return 'Unknown'"""
    arcpy.CalculateField_management(file, "Descrpn", expr, "PYTHON", codeblock)

outputList = ["T0.shp", "T1.shp", "T2.shp", "T3.shp", "T4.shp", "T5.shp"]
TToutputList = ["T0_T1.shp", "T1_T2.shp",
                "T2_T3.Shp", "T3_T4.shp", "T4_T5.shp"]
dissolveInList = ["T0.dbf", "T1.dbf", "T2.dbf", "T3.dbf", "T4.dbf", "T5.dbf"]
dissolveOutList = ["T0.xls", "T1.xls", "T2.xls", "T3.xls", "T4.xls", "T5.xls"]
IntersectInList = ["T0_T1.dbf", "T1_T2.dbf",
                    "T2_T3.dbf", "T3_T4.dbf", "T4_T5.dbf"]
IntersectOutList = ["T0_T1.xls", "T1_T2.xls",
                    "T2_T3.xls", "T3_T4.xls", "T4_T5.xls"]
pivotOutList = ["T0_T1.csv", "T1_T2.csv",
                "T2_T3.csv", "T3_T4.csv", "T4_T5.csv"]


def dissolve_func(input, output):
    arcpy.Dissolve_management(input, output, ["Descrpn"])
    arcpy.AddField_management(output, "Arrr", "DOUBLE")
    arcpy.CalculateField_management(
        output, 'Arrr', '!shape.area@hectares!', 'PYTHON')


def intersect_func(input, output):
    arcpy.Intersect_analysis(input, output)
    arcpy.AddField_management(output, "Arrr", "DOUBLE")
    arcpy.CalculateField_management(
        output, 'Arrr', '!shape.area@hectares!', 'PYTHON')


for rep in range(no_of_terms+1):
    dissolve_func(inputList[rep], outputList[rep])
    arcpy.TableToExcel_conversion(dissolveInList[rep], dissolveOutList[rep])
    if rep != 0:
        intersect_func([inputList[rep-1], inputList[rep]], TToutputList[rep-1])
        arcpy.TableToExcel_conversion(
            IntersectInList[rep-1], IntersectOutList[rep-1])

combined_df = pd.DataFrame()
combined_dissolve_out = os.path.join(
    out_path, folder_name + "_Combined" + ".xls")


def excel_func(inputDF):
    inputDF = inputDF.drop(['FID'], axis=1)
    inputDF = inputDF.T
    inputDF = inputDF.reset_index(drop=True)
    new_header = inputDF.iloc[0]
    inputDF = inputDF[1:]
    inputDF.columns = new_header
    return inputDF


excel_list = [os.path.join(env_path, i) for i in dissolveOutList]
for ind, i in enumerate(excel_list):
    if ind < no_of_terms+1:
        combined_df = combined_df.append(
            excel_func(pd.read_excel(i)), ignore_index=True)

combined_df = combined_df.fillna(0)
for rep in range(no_of_terms):
    combined_df.loc[outputList[rep+1]]=combined_df.loc[rep+1]-combined_df.loc[rep]
combined_df.to_excel(combined_dissolve_out)

for term in range(no_of_terms):
    pivot_file = os.path.join(env_path, IntersectOutList[term])
    df = pd.read_excel(pivot_file)
    pivot_df = df.pivot_table(index=['Descrpn'], columns=['Descrpn_1'], values=
                            ['Arrr'], aggfunc='sum', fill_value=0)
    pivot_df.loc[:, 'Total'] = pivot_df.sum(axis=1)
    pivot_df.loc['Total', :] = pivot_df.sum(axis=0)
    pivot_df[pivot_df.columns] = pivot_df[pivot_df.columns].replace(
                                                                ['0', 0], np.nan)
    pivot_df.to_csv(os.path.join(
        out_path, folder_name + '_' + pivotOutList[term]))
