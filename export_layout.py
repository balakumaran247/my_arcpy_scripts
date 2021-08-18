import arcpy, time, os

out_dir = r'D:\project\output'
mxd = arcpy.mapping.MapDocument("CURRENT")

inputDict = {
    'District':[]
}

inputLabel = {
    'District':'District_Label'
}

distsymb = 'group\\layer'
mwssymb = 'group\\layer'

for district in inputDict.keys():
    for df in arcpy.mapping.ListDataFrames(mxd):
        layers = arcpy.mapping.ListLayers(mxd, district, df)
        for layer in layers:
            layer.visible = True
            # Copies symbology
            arcpy.ApplySymbologyFromLayer_management (layer, distsymb)
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()
            time.sleep(2)
    zoom_df = arcpy.mapping.ListDataFrames(mxd)[1]
    zoom_layers = arcpy.mapping.ListLayers(mxd,district,zoom_df)
    for zoom_layer in zoom_layers:
        # If zoom to feature of layer
        # arcpy.SelectLayerByAttribute_management(zoom)
        # zoom_df.extent = zoom.getSelectedExtent()
        # If zoom to entire layer
        zoom_df.extent = zoom_layer.getExtent()
        zoom_df.scale = zoom_df.scale * 1.05
        arcpy.RefreshActiveView()
        # arcpy.SelectLayerByAttribute_management(zoom, "CLEAR_SELECTION")
        time.sleep(2)
    for TextElement in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if TextElement.name == "district_text":
                TextElement.text = inputLabel[district]+' District'
    for wtsd in inputDict[district]:
        for df in arcpy.mapping.ListDataFrames(mxd):
            wlayers = arcpy.mapping.ListLayers(mxd, wtsd+'*', df)
            for wlayer in wlayers:
                # Copies symbology
                arcpy.ApplySymbologyFromLayer_management (wlayer, mwssymb)
                wlayer.visible = True
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                time.sleep(2)
                if 'mwtsd' in wlayer.name.split('-'):
                    # Enable labels for the layer
                    for lblclass in wlayer.labelClasses:
                        lblclass.expression='[mws_code]'
                    wlayer.showLabels
                    df.extent = wlayer.getExtent()
                    df.scale = df.scale * 1.05
                    arcpy.RefreshActiveView()
                    time.sleep(2)
        for TextElement in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if TextElement.name == "project_text":
                TextElement.text = wtsd
        arcpy.RefreshActiveView()
        time.sleep(5)
        arcpy.mapping.ExportToJPEG(mxd,os.path.join(out_dir,wtsd+'.jpg'))
        for df in arcpy.mapping.ListDataFrames(mxd):
            wlayers = arcpy.mapping.ListLayers(mxd, wtsd+"*", df)
            for wlayer in wlayers:
                wlayer.visible = False
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()
                time.sleep(2)
    for df in arcpy.mapping.ListDataFrames(mxd):
        layers = arcpy.mapping.ListLayers(mxd, district, df)
        for layer in layers:
            layer.visible = False
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()
            time.sleep(2)