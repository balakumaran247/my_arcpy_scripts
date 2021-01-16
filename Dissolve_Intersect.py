import arcpy, os, shutil
import pandas as pd

no_of_terms = 3
year = "2010_11"
folder_name = "Project_2010_11"
t0_file = "Project_2010_11_T0"
t1_file = "Project_2010_11_T1"
t2_file = "Project_2010_11_T2"
t3_file = "Project_2010_11_T3"
t4_file = ""
t5_file = ""

drive_path = "E:\Project"

out_path = r"C:\Users\HP\Desktop\dissolve\output"

for filename in os.listdir(out_path):
    file_path = os.path.join(out_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

t0_input = os.path.join(drive_path, year, folder_name, str("T0"), str(t0_file) + ".shp")
t1_input = os.path.join(drive_path, year, folder_name, str("T1"), str(t1_file) + ".shp")
t2_input = os.path.join(drive_path, year, folder_name, str("T2"), str(t2_file) + ".shp")
t3_input = os.path.join(drive_path, year, folder_name, str("T3"), str(t3_file) + ".shp")
t4_input = os.path.join(drive_path, year, folder_name, str("T4"), str(t4_file) + ".shp")
t5_input = os.path.join(drive_path, year, folder_name, str("T5"), str(t5_file) + ".shp")

t0_output = os.path.join(out_path, str("T0") + ".shp")
t1_output = os.path.join(out_path, str("T1") + ".shp")
t2_output = os.path.join(out_path, str("T2") + ".shp")
t3_output = os.path.join(out_path, str("T3") + ".shp")
t4_output = os.path.join(out_path, str("T4") + ".shp")
t5_output = os.path.join(out_path, str("T5") + ".shp")

t0_t1_output = os.path.join(out_path, str("T0_T1") + ".shp")
t1_t2_output = os.path.join(out_path, str("T1_T2") + ".shp")
t2_t3_output = os.path.join(out_path, str("T2_T3") + ".shp")
t3_t4_output = os.path.join(out_path, str("T3_T4") + ".shp")
t4_t5_output = os.path.join(out_path, str("T4_T5") + ".shp")

t0_dissolve_in = os.path.join(out_path, str("T0") + ".dbf")
t1_dissolve_in = os.path.join(out_path, str("T1") + ".dbf")
t2_dissolve_in = os.path.join(out_path, str("T2") + ".dbf")
t3_dissolve_in = os.path.join(out_path, str("T3") + ".dbf")
t4_dissolve_in = os.path.join(out_path, str("T4") + ".dbf")
t5_dissolve_in = os.path.join(out_path, str("T5") + ".dbf")

t0_dissolve_out = os.path.join(out_path, str("T0") + ".xls")
t1_dissolve_out = os.path.join(out_path, str("T1") + ".xls")
t2_dissolve_out = os.path.join(out_path, str("T2") + ".xls")
t3_dissolve_out = os.path.join(out_path, str("T3") + ".xls")
t4_dissolve_out = os.path.join(out_path, str("T4") + ".xls")
t5_dissolve_out = os.path.join(out_path, str("T5") + ".xls")

t0t1_intersect_in = os.path.join(out_path, str("T0_T1") + ".dbf")
t1t2_intersect_in = os.path.join(out_path, str("T1_T2") + ".dbf")
t2t3_intersect_in = os.path.join(out_path, str("T2_T3") + ".dbf")
t3t4_intersect_in = os.path.join(out_path, str("T3_T4") + ".dbf")
t4t5_intersect_in = os.path.join(out_path, str("T4_T5") + ".dbf")

t0t1_intersect_out = os.path.join(out_path, str("A_Pivot_T0_T1") + ".xls")
t1t2_intersect_out = os.path.join(out_path, str("A_Pivot_T1_T2") + ".xls")
t2t3_intersect_out = os.path.join(out_path, str("A_Pivot_T2_T3") + ".xls")
t3t4_intersect_out = os.path.join(out_path, str("A_Pivot_T3_T4") + ".xls")
t4t5_intersect_out = os.path.join(out_path, str("A_Pivot_T4_T5") + ".xls")

combined_dissolve_out = os.path.join(out_path, str("A_Combined_Dissolve") + ".xls")

def dissolve_func(input, output):
	try:
		arcpy.Dissolve_management(input, output, ["Code"])
	except:
		try:
			arcpy.Dissolve_management(input, output, ["Code_1"])
		except:
			arcpy.Dissolve_management(input, output, ["Code_12"])
	arcpy.AddField_management(output, "Area", "DOUBLE")
	arcpy.CalculateField_management(output,'Area','!shape.area@hectares!','PYTHON')

def intersect_func(input, output):
	arcpy.Intersect_analysis(input, output)
	arcpy.AddField_management(output, "Area", "DOUBLE")
	arcpy.CalculateField_management(output,'Area','!shape.area@hectares!','PYTHON')

inputList = [t0_input, t1_input, t2_input, t3_input, t4_input, t5_input]
outputList = [t0_output, t1_output, t2_output, t3_output, t4_output, t5_output]
TToutputList = [t0_t1_output, t1_t2_output, t2_t3_output, t3_t4_output, t4_t5_output]
dissolveInList = [t0_dissolve_in, t1_dissolve_in, t2_dissolve_in, t3_dissolve_in, t4_dissolve_in, t5_dissolve_in]
dissolveOutList = [t0_dissolve_out, t1_dissolve_out, t2_dissolve_out, t3_dissolve_out, t4_dissolve_out, t5_dissolve_out]
IntersectInList = [t0t1_intersect_in, t1t2_intersect_in, t2t3_intersect_in, t3t4_intersect_in, t4t5_intersect_in]
IntersectOutList = [t0t1_intersect_out, t1t2_intersect_out, t2t3_intersect_out, t3t4_intersect_out, t4t5_intersect_out]

for rep in range(no_of_terms+1):
	dissolve_func(inputList[rep], outputList[rep])
	arcpy.TableToExcel_conversion(dissolveInList[rep], dissolveOutList[rep])
	if rep != 0:
		intersect_func([inputList[rep-1], inputList[rep]], TToutputList[rep-1])
		arcpy.TableToExcel_conversion(IntersectInList[rep-1], IntersectOutList[rep-1])

combined_df = pd.DataFrame()

def excel_func(inputDF):
	inputDF = inputDF.drop(['FID'], axis=1)
	inputDF = inputDF.T
	inputDF = inputDF.reset_index(drop=True)
	new_header = inputDF.iloc[0]
	inputDF = inputDF[1:]
	inputDF.columns = new_header
	return inputDF

excel_list = [t0_dissolve_out, t1_dissolve_out, t2_dissolve_out, t3_dissolve_out, t4_dissolve_out, t5_dissolve_out]
for ind, i in enumerate(excel_list):
	if ind < no_of_terms+1:
		combined_df = combined_df.append(excel_func(pd.read_excel(i)), ignore_index=True)

combined_df = combined_df.fillna(0)
combined_df.to_excel(combined_dissolve_out)