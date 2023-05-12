from django.test import TestCase
#for testing purpose comment from here
'''hdng1 = 'Here starts the dredging calculation part'

        depthRes = 5
        KPsOfDOL1 = [0, 0.015, 1.05, 4.64, 28.45, 30.177, 33.515, 36.815, 38.270, 54.94, 62.065, 64.322, 70.865, 84.35]
        DOL_List1 = [1.2, np.nan, 0.4, 1.4, 1.8, 2.1, 1.4, 1.8, 1.4, 0.4, 1.4, 0.4, 0.9]
        
        KPsOfDOL2 = [0, 0.015, 1.05, 4.64, 28.45, 30.177, 33.515, 36.815, 38.270, 54.94, 62.065, 64.322, 75.14, 84.13, 103.914]
        DOL_List2 = [1.2, np.nan, 0.4, 1.4, 1.8, 2.1, 1.4, 1.8, 1.4, 0.4, 1.4, 0.4, 3.2, 0.4]

        KPsOfDOL3 = [0, 0.015, 1.05, 4.64, 28.45, 30.177, 33.515, 36.815, 38.270, 54.94, 62.065, 64.322, 75.14, 84.13, 95.834, 131.226]
        DOL_List3 = [1.2, np.nan, 0.4, 1.4, 1.8, 2.1, 1.4, 1.8, 1.4, 0.4, 1.4, 0.4, 3.2, 0.4, 0.9]
        depth1 = readExcel('static/NV_NKT_RPL_Rev_B_West_Profile_250122.xlsx',KPsOfDOL1, DOL_List1)
        depth2 = readExcel('static/NV_NKT_RPL_Rev_B_East_Profile_250122.xlsx',KPsOfDOL2, DOL_List2)
        depth3 = readExcel('static/NV_NKT_RPL_Rev_B_Boreas_Profile_250122.xlsx',KPsOfDOL3, DOL_List3)

        hdng2='Find the GEOL locations that are also present in LOCA tab' 

        # Transform the bathymetry/mobility profiles to Web Mercator projection
        depth1 = UTM_to_WebMercator(depth1, "POINT_X", "POINT_Y")
        depth2 =  UTM_to_WebMercator(depth2, "POINT_X", "POINT_Y")
        depth3 = UTM_to_WebMercator(depth3, "POINT_X", "POINT_Y")
        #depth3.head()
        
        yy = tables['GEOL'].loc[:,['LOCA_ID','GEOL_BASE','GEOL_DESC']]

        vcNames = yy.LOCA_ID.unique().tolist()
        vcNames = [i for i in vcNames if i in names]
        # print(vcNames)

        depthList, geoList, geoListFull, maxVClength = soil_layers_fromAGS(yy, vcNames)

        # Use water depth of soil investigations
        loca=''
        if 'LOCA_WDEP' in tables['LOCA']:
            loca = 'LOCA_WDEP'
        elif 'LOCA_LOCZ' in tables['LOCA']:
            loca = 'LOCA_LOCZ'

        
        #print(loca)
        
        zz = tables['LOCA'].loc[:,['LOCA_ID', loca]]
        # Create the empty lists
        VC_depths = []

        for i in vcNames:
            VC_depths.append(float(pd.to_numeric(zz.loc[zz['LOCA_ID'] == i][loca])))

        source, depth_list, soiltype_list, full_soiltype_list = VCgeologySource(names, xCoTr, yCoTr, depthList, geoList, geoListFull)
        source_aug, depth_list_aug, soiltype_list_aug, full_soiltype_list_aug = VCgeologySource(names, xCoTr, yCoTr, depthList, geoList, geoListFull)
        
        sourceDepth1 = ColumnDataSource(data=dict(KP=depth1['KP'], LAT2021=depth1['2021 Bathy LAT (m)'], X1=depth1['POINT_X'], 
            Y1=depth1['POINT_Y'], LAT2025=depth1['2025_BE_Bathy'], RSBL=depth1['RSBL'], dHeight=depth1['Dredge height'], TOC=depth1['TOC'],
            DOL=-depth1['DOL'], ESL=depth1['ESL']))
        sourceDepth2 = ColumnDataSource(data=dict(KP=depth2['KP'], LAT2021=depth2['2021 Bathy LAT (m)'], X1=depth2['POINT_X'], 
            Y1=depth2['POINT_Y'], LAT2025=depth2['2025_BE_Bathy'], RSBL=depth2['RSBL'], dHeight=depth2['Dredge height'], TOC=depth2['TOC'],
            DOL=-depth2['DOL'], ESL=depth2['ESL']))
        sourceDepth3 = ColumnDataSource(data=dict(KP=depth3['KP'], LAT2021=depth3['2021 Bathy LAT (m)'], X1=depth3['POINT_X'], 
            Y1=depth3['POINT_Y'], LAT2025=depth3['2025_BE_Bathy'], RSBL=depth3['RSBL'], dHeight=depth3['Dredge height'], TOC=depth3['TOC'],
            DOL=-depth3['DOL'], ESL=depth3['ESL']))
        #print(depth1.head())


        confidenceX, confidenceY = [], []
        # confidenceX.append(list(depth1.loc[0:260,'POINT_X']))
        # confidenceX.append(list(depth1.loc[260:8000,'POINT_X']))
        # confidenceX.append(list(depth1.loc[8000:16000,'POINT_X']))

        confidenceX.append(list(depth1.loc[(depth3.KP>30.18) & (depth3.KP<33.52) , 'POINT_X']))
        confidenceX.append(list(depth1.loc[(depth3.KP>47.54) & (depth3.KP<48.94) , 'POINT_X']))

        # confidenceY.append(list(depth1.loc[0:260,'POINT_Y']))
        # confidenceY.append(list(depth1.loc[260:8000,'POINT_Y']))
        # confidenceY.append(list(depth1.loc[8000:16000,'POINT_Y']))

        confidenceY.append(list(depth1.loc[(depth3.KP>30.18) & (depth3.KP<33.52) , 'POINT_Y']))
        confidenceY.append(list(depth1.loc[(depth3.KP>47.54) & (depth3.KP<48.94) , 'POINT_Y']))

        toolPic = 'https://img.nauticexpo.de/images_ne/photo-g/40164-4639733.jpg'
        hDDPic = 'https://www.gatewayok.com/wp-content/uploads/2016/08/HDD3.png'
        # toolList = [hDDPic]+[toolPic]*2
        toolList = [toolPic]*2

        # toolNames = ['HDD', 'iTrencher', 'iTrencher']
        toolNames = ['iTrencher', 'iTrencher']

        # toolPic= 'https://docs.bokeh.org/static/snake.jpg'
        sourceConf = ColumnDataSource(dict( x = confidenceX, y = confidenceY, tool = toolNames,
        #                                 legend = 'confidence', 
                                        color = ['green', 'green'], imgs = toolList, confLevel=['High', 'High']))

        TOOLTIPSconf = """
            <div>
                <div>
                    <span style="font-size: 24px; font-weight: bold;">Tool: @tool</span>
                </div>
                <div>
                    <img
                        src="@imgs" height="136" alt="@imgs" width="204"
                        style="float: left; margin: 0px 15px 15px 0px;"
                        border="2"
                    ></img>
                </div>
                <div>
                    <span style="font-size: 30px; font-weight: bold;">Confidence: @confLevel</span>
                    <!--<span style="font-size: 30px; color: #966;">[$index]</span>-->
                </div>
            </div>
        """
        print([toolPic]*2)

        KPs = pd.read_excel('static/Norfolk Vanguard - Geotechnical Locations - 20210917.xlsx')
        KPs.head()
        KP = []
        DCC = []
        for i in names:
            tt = KPs.loc[KPs['LOCA_ID'] == i]
            kp_post = float(tt['RPL = ITTRound2IndicativeExportRoutes.shp'])
        
        # if kp_post<84.3:
            KP.append(kp_post)
            DCC.append(abs(float(tt['Unnamed: 7'])))
        source.data['KP']=KP
        source.data['DCC']=DCC

        #print(source)

        # Add the water depths and KPs to the vibrocore source, for overlaying to the bathymetry chart.
        source_aug.data['d0']=VC_depths
        source_aug.data['c0']=len(names)*['NAN']

        depth_list_aug = depth_list.copy()
        soiltype_list_aug = soiltype_list.copy()
        depth_list_aug.insert(0,'d0')
        soiltype_list_aug.insert(0,'c0')

        for i in depth_list_aug:
                source_aug.data[i]=list(-np.array(source_aug.data[i]))

        source_aug.data['KP']=KP #list(np.linspace(0,82,76))
        source_aug.data['DCC']=DCC

        #print(source_aug)

        # Create the callback JS texts using the agstools scripts
        code = selected_ind_Cb('dHeight', depthRes) # Callback for calculating volumes only for selected part of routes
        code2 = depth_Cb('dHeight', depthRes) # Callback for calculating volumes for updated depth variable
        code3 = width_Cb('dHeight', depthRes) # Callback for calculating volumes for updated trench width variable
        code4 = heightLine_Cb('LAT2025', 'RSBL', 'dHeight')
        code4new = heightLineWithDOL_Cb('LAT2025', 'TOC', 'dHeight', 'ESL')
        code5 = slope_Cb('dHeight', depthRes) # Callback for calculating volumes for updated trench side slope variable

        # Enter the coordinates of the HHW SAC polygon
        HHWSAC_lon = [170875.4, 191024.2, 233437.0, 246461.4, 256480.1, 256814.1, 245125.5, 230765.3, 221971.1,208724.0,189020.5]
        HHWSAC_lat = [6982997.9, 6991326.0, 6982997.9, 6967659.9, 6935600.6, 6922555.8, 6917967.5, 6920903.7, 6918518.0,6910998.5,6963045.8]

        sourceSAC = ColumnDataSource(data=dict(lon=HHWSAC_lon, lat = HHWSAC_lat))


        # Import and process some shape files for plotting on the map

        
        sf  = getShapeFile('static/Shapefiles/UNV_EVEC_SabPgon_v01_191010lico25831.shp')
        sfW  = getShapeFile('static/Shapefiles/2020-08-20_Wrecks_merged.shp')
        sfS  = getShapeFile('static/Shapefiles/103434-Survey_Boundaries-20200520-ETRS89-31N.dxf')
        sfZB  = getShapeFile('static/Shapefiles/C1315_Cathie_AIS_210712 C1315_NVNB_ShippingZones_v02_210629_ttw_25831_Buf250m.shp')
        #sfZ  = getShapeFile('static/Shapefiles/C1315_Cathie_AIS_210712 C1315_NVNB_ShippingZones_v02_210629_ttw_25831.shp')
        sfG = getShapeFile('static/Shapefiles/Norfolk_Geotechnical_Samples_All.shp')
                
        x, y = [], []
        [(x.append(list(polygon.exterior.coords.xy[0])), y.append(list(polygon.exterior.coords.xy[1]))) for polygon in sf['geometry'] if type(polygon.boundary) == shapely.geometry.linestring.LineString ]

        xW, yW = [], []
        [(xW.append(list(point.coords.xy[0])[0]), yW.append(list(point.coords.xy[1])[0])) for point in sfW['geometry']]# if type(polygon.boundary) == shapely.geometry.linestring.LineString ]

        xL, yL = [], []
        [(xL.append(list(line.coords.xy[0])), yL.append(list(line.coords.xy[1]))) for line in sfS['geometry']]; # if type(polygon.boundary) == shapely.geometry.linestring.LineString ]

        xZB, yZB = [], []
        [(xZB.append(list(polygon.exterior.coords.xy[0])), yZB.append(list(polygon.exterior.coords.xy[1]))) for polygon in sfZB['geometry'] if type(polygon.boundary) == shapely.geometry.linestring.LineString ]


        #xG, yG = [], []
        #[(xG.append(list(point.coords.xy[0])[0]), yG.append(list(point.coords.xy[1])[0])) for point in sfZ['geometry']]# if type(polygon.boundary) == shapely.geometry.linestring.LineString ]

        xG, yG = [], []
        [(xG.append(list(point.coords.xy[0])[0]), yG.append(list(point.coords.xy[1])[0])) for point in sfG['geometry']]# if type(polygon.boundary) == shapely.geometry.linestring.LineString ]
        
        #print(sfZB[0:26])

        for ind, i in enumerate(sf.geometry):
            if type(i)==shapely.geometry.linestring.LineString:
                pass
            else:
                #print(ind, type(i))
                continue
        #print(sf)
        TOOLS = "box_select,lasso_select, wheel_zoom, pan, crosshair, box_zoom, undo, reset"
        ### Create the map plot that shows routes, features, etc.
        html2,toggle1, toggle2, toggle3, toggle4,p = getOffshoremap(TOOLS,sourceSAC,x,y,xL,yL,xW,yW,xZB,yZB,xG,yG,sourceDepth1,sourceDepth2,sourceDepth3,TOOLTIPSconf,sourceConf,source)
        #html2,toggle1, toggle4,p = getOffshoremap(TOOLS,xL,yL,source)
        
        soil_types, color_palette = loadNKTsoil_legend()

        multi_select2, viewVC = makeGeolFiltering(source, geoList, soiltype_list)

        DCC_range_slider = RangeSlider(name='DCC Range Slider', start=0, end=1000,
                                value=(0, 500), step=5, title = 'DCC range [m]', width=150)


        # This callback is crucial, otherwise the filter will not be triggered when the slider changes
        DCC_slider_callback = CustomJS(args=dict(source=source_aug), code="""
            source.change.emit();
        """)
        DCC_range_slider.js_on_change('value', DCC_slider_callback)

        custom_filter_DCC = CustomJSFilter(args = dict(slider=DCC_range_slider), code=slider_filter('DCC'))

        view_DCC = CDSView(source=source_aug, filters=[custom_filter_DCC])

        #(TOOLS,sourceDepth1,ttl)
        p1 = getPs(TOOLS,sourceDepth1,ttl="Depth along route NVW")
        p1.vbar_stack( depth_list_aug, x='KP',  width=0.3,  
                    fill_color=[
                        factor_cmap(state, palette=color_palette, factors=soil_types) 
                        for state in soiltype_list_aug],
                    line_color=None, legend_label="soil profile",
                    #hatch_pattern=[
        #                 factor_hatch(state, patterns=[".", " "," "," "," ", ".", " "," "], factors=soil_types)
        #                 for state in ["c1","c2","c3","c4","c5"]],
                    source=source_aug, view=view_DCC)
        
        p3 = getPs(TOOLS,sourceDepth2,ttl="Depth along route NVE")
        p4 = getPs(TOOLS,sourceDepth3,ttl="Depth along route NB")

        s2 = ColumnDataSource(data=dict(x=[0, 50], ym=['0', 0.], myText=["Dredge volume [m3]:", ""]))
        s3 = ColumnDataSource(data=dict(x=[0, 50], ym=['0', 0.], myText=["Dredge volume [m3]:", ""]))
        s4 = ColumnDataSource(data=dict(x=[0, 50], ym=['0', 0.], myText=["Dredge volume [m3]:", ""]))

        explText = """Dredge corridor is a trapezium.
                                 Calculation does not take into account laterally uneven seabed profile."""
        volumeText = p1.text(x=10, y=-5, text='myText', source=s2, name="mytextbox")
        p1.add_layout(volumeText)
        p1.add_tools(HoverTool(tooltips=explText, names=['mytextbox']))

        volumeText2 = p3.text(x=10, y=-5, text='myText', source=s3, name="mytextbox2")
        p3.add_layout(volumeText2)
        p3.add_tools(HoverTool(tooltips=explText, names=['mytextbox2']))

        volumeText3 = p4.text(x=10, y=-5, text='myText', source=s4, name="mytextbox3")
        p4.add_layout(volumeText3)
        p4.add_tools(HoverTool(tooltips=explText, names=['mytextbox3']))


        TOOLS_bar = "box_select, wheel_zoom, pan, box_zoom, reset,tap, undo"

        # Here the option to sort the vibrocores by KP is created. 
        sortedByKP = True

        if sortedByKP == True:
            sort_df = pd.DataFrame(data={'names': source.data['name'], 'KP': source.data['KP']})
            sort_df.sort_values(by=['KP'], inplace=True)
            VC_x_range = list(sort_df['names'])
        else:
            VC_x_range = names
            
        p2 = figure(tools=TOOLS_bar, x_range=VC_x_range, plot_width=1700, plot_height=300, y_axis_label='Depth [m]')
        p2.toolbar.logo = None

        p2.y_range.flipped = True
        p2.xaxis.major_label_orientation = "vertical"

        p2.vbar_stack( depth_list, x="name",  width=0.8,  
                    fill_color=[
                        factor_cmap(state, palette=color_palette, factors=soil_types) 
                        for state in soiltype_list],
                    line_color="black", view=viewVC,
                    #hatch_pattern=[
        #                 factor_hatch(state, patterns=[".", " "," "," "," ", ".", " "," "], factors=soil_types)
        #                 for state in ["c1","c2","c3","c4","c5"]],
                    source=source)

        c_custom=CustomJSHover(code="""
                            //var value
                            //return value
                            var value
                            if (value.valueOf()==new String("NaN").valueOf()) {
                                return '';
                            } else {
                                return ', ' + value;
                            }
                            """)
        # Define the custom formatter for soil type hover tool, from 2nd layer onwards
        formatters = {}
        if len(soiltype_list)>2:
            for i in soiltype_list[1:]:
                formatters['@'+i] = c_custom
            
        hoverString = '(@c1'+ ''.join(['@'+i+'{custom}' for i in soiltype_list[1:]])+')'
        p2.add_tools(HoverTool(
                tooltips=[
                    #("index", "$index"),
                    ("Vibrocore", "@name"),
                    ('KP', "@KP"),
                    ("DCC", "@DCC{0} m"),
                    ("Layers", hoverString)
                ], formatters=formatters
            ))

        
        # Add a spinner widget with numerical values for dredge level
        spinner1 = Spinner(title="Burial tool depth DOL[m]", low=-10, high=10, step=0.1, value=0, width=170)

        # spinner.js_link('value', points.glyph, 'size')
        spinner2 = Spinner(title="Dredge corr. bottom width [m]", low=0, high=50, step=0.5, value=20, width=170)

        spinner3 = Spinner(title="Corridor walls slope 1/X [m]", low=0, high=10, step=0.5, value=3, width=170)




        callback1NVW = CustomJS(args=dict(s=sourceDepth1, s2=s2, sp1=spinner1, sp2=spinner2, sp3=spinner3), code=code)
        callback1NVE = CustomJS(args=dict(s=sourceDepth2, s2=s3, sp1=spinner1, sp2=spinner2, sp3=spinner3), code=code)
        callback1NB = CustomJS(args=dict(s=sourceDepth3, s2=s4, sp1=spinner1, sp2=spinner2, sp3=spinner3), code=code)

        callback2NVW = CustomJS(args=dict(s=sourceDepth1, s2=s2, sp2=spinner2, sp3=spinner3), code=code2)
        callback2NVE = CustomJS(args=dict(s=sourceDepth2, s2=s3, sp2=spinner2, sp3=spinner3), code=code2)
        callback2NB = CustomJS(args=dict(s=sourceDepth3, s2=s4, sp2=spinner2, sp3=spinner3), code=code2)

        callback3NVW = CustomJS(args=dict(s=sourceDepth1, s2=s2, sp1=spinner1, sp3=spinner3), code=code3)
        callback3NVE = CustomJS(args=dict(s=sourceDepth2, s2=s3, sp1=spinner1, sp3=spinner3), code=code3)
        callback3NB = CustomJS(args=dict(s=sourceDepth3, s2=s4, sp1=spinner1, sp3=spinner3), code=code3)

        callback5NVW = CustomJS(args=dict(s=sourceDepth1, s2=s2, sp1=spinner1, sp2=spinner2), code=code5)
        callback5NVE = CustomJS(args=dict(s=sourceDepth2, s2=s3, sp1=spinner1, sp2=spinner2), code=code5)
        callback5NB = CustomJS(args=dict(s=sourceDepth3, s2=s4, sp1=spinner1, sp2=spinner2), code=code5)

        callback4NVW = CustomJS(args=dict(s=sourceDepth1), code=code4new)
        callback4NVE = CustomJS(args=dict(s=sourceDepth2), code=code4new)
        callback4NB = CustomJS(args=dict(s=sourceDepth3), code=code4new)

        # Define callbacks
        sourceDepth1.selected.js_on_change('indices', callback1NVW)
        sourceDepth2.selected.js_on_change('indices', callback1NVE)
        sourceDepth3.selected.js_on_change('indices', callback1NB)

        # First update the dredging heights, so they are available for the dredge volume update
        spinner1.js_on_change('value', callback4NVW), spinner1.js_on_change('value', callback4NVE), spinner1.js_on_change('value', callback4NB)
        spinner1.js_on_change('value', callback2NVW), spinner1.js_on_change('value', callback2NVE), spinner1.js_on_change('value', callback2NB)
            
        spinner2.js_on_change('value', callback3NVW), spinner2.js_on_change('value', callback3NVE), spinner2.js_on_change('value', callback3NB)
        spinner3.js_on_change('value', callback5NVW), spinner3.js_on_change('value', callback5NVE), spinner3.js_on_change('value', callback5NB)

        tab1 = Panel(child=p1, title="NVW")
        tab2 = Panel(child=p3,title="NVE")
        tab3 = Panel(child=p4,title="NB")
        tabs = Tabs(tabs=[tab1, tab2, tab3])


        psu = figure(width=400, height=700, tools=TOOLS_bar, title="Laboratory test results", x_axis_label="su [kPa]", y_axis_label="Depth [m]")
        psu.toolbar.logo = None
        psu.y_range.flipped = True

        range_slider = RangeSlider(name='Range Slider', start=0, end=max(srcLVAN.data['LVAN_VNPK']),
                                value=(0, max(srcLVAN.data['LVAN_VNPK'])), step=5, title = 'Su range [kPa]', width=150)

        # This callback is crucial, otherwise the filter will not be triggered when the slider changes
        slider_callback = CustomJS(args=dict(source=srcLVAN, source2=srcLPEN), code="""
            source.change.emit();
            source2.change.emit();
        """)
        range_slider.js_on_change('value', slider_callback)

        custom_filter = CustomJSFilter(args = dict(slider=range_slider), code=slider_filter('LVAN_VNPK'))

        custom_filter2 = CustomJSFilter(args = dict(slider=range_slider), code=slider_filter('LPEN_PPEN'))                               
        

        div1 = Div(text='<b>NVW Dredge volume [m<sup>3</sup>]</b>', width=170, height=10)
        div2 = Div(text='<b>NVE Dredge volume [m<sup>3</sup>]</b>', width=170, height=10)
        div3 = Div(text='<b>NB Dredge volume [m<sup>3</sup>]</b>', width=170, height=10)
        div1NVW = Div(text='', width=170, height=10)
        div2NVE = Div(text='', width=170, height=10)
        div3NB = Div(text='', width=170, height=10)
        ChangeTextScript = """
            o1.text=s2.data['ym'][0];
        """
        callbackDiv1=CustomJS(args=dict(o1=div1NVW, s2=s2),code=ChangeTextScript)
        callbackDiv2=CustomJS(args=dict(o1=div2NVE, s2=s3),code=ChangeTextScript)
        callbackDiv3=CustomJS(args=dict(o1=div3NB, s2=s4),code=ChangeTextScript)

        sourceDepth1.selected.js_on_change('indices', callbackDiv1)
        sourceDepth2.selected.js_on_change('indices', callbackDiv2)
        sourceDepth3.selected.js_on_change('indices', callbackDiv3)
        spinner1.js_on_change('value', callbackDiv1), spinner1.js_on_change('value', callbackDiv2), spinner1.js_on_change('value', callbackDiv3)
        spinner2.js_on_change('value', callbackDiv1), spinner2.js_on_change('value', callbackDiv2), spinner2.js_on_change('value', callbackDiv3)
        spinner3.js_on_change('value', callbackDiv1), spinner3.js_on_change('value', callbackDiv2), spinner3.js_on_change('value', callbackDiv3)

        view = CDSView(source=srcLVAN, filters=[custom_filter])
        view2 = CDSView(source=srcLPEN, filters=[custom_filter2])
        LVANplot = psu.circle('LVAN_VNPK', 'SPEC_DPTH', legend_label="LVAN", source=srcLVAN, view=view, name='LVAN')
        LPENplot = psu.square('LPEN_PPEN', 'SPEC_DPTH', color='red', legend_label="LPEN", source=srcLPEN, view=view2,name='LPEN')

        psu.add_tools(HoverTool(
                tooltips=[
                    ("Vibrocore", "@LOCA_ID"),
                    ("Specimen depth [m]", "@SPEC_DPTH{0.00}"),
                    ("LVAN su [kPa]", "@LVAN_VNPK{0.0}")         
                ], names = ['LVAN']
            ))

        psu.add_tools(HoverTool(
                tooltips=[
                    ("Vibrocore", "@LOCA_ID"),
                    ("Specimen depth [m]", "@SPEC_DPTH{0.00}"),
                    ("LPEN su [kPa]", "@LPEN_PPEN{0.0}")         
                ], names = ['LPEN']
            ))

        down_button = Button(label="Download NVW profiles", button_type="success", width =170)
        down_button.js_on_click(CustomJS(args=dict(source=sourceDepth1),
                                    code=download_csv()))
        
        columns = [
            TableColumn(field="name", title="Vibrocore", width=100),
            TableColumn(field="KP", title="KP", width=50),
            TableColumn(field="DCC", title="DCC", width=50),
        ]
        for i,j in zip(depth_list, full_soiltype_list):
            num=''.join(c for c in i if c.isdigit())
            columns.append(TableColumn(field=i, title="Height Layer {}".format(num), editor=StringEditor(), width=90))
            columns.append(TableColumn(field=j, title="Geology Layer {}".format(num), width=300))
        data_table = DataTable(source=source, columns=columns,
                            width=400, height=200, sizing_mode="stretch_width", editable=True, autosize_mode="none")
        taptool = p2.select(type=TapTool)

        plegend, plogo = createLogoAndLegendNew(['static/Images/soil_legend3.png', 'static/Images/NKT logo.png'])

        #print(depth_list)
        #print(soiltype_list)
        #print(type(source.data['d1'][0]))
        #print(len(source.data['name']))
        #print(source.data['name'])
        xrandom=np.linspace(0,76,76)
        #print(len(list(xrandom)))

        tab4 = Panel(child=row([p, column(toggle1, toggle2, toggle3, toggle4)]), title="Offshore Map Norfolk")
        tab5 = Panel(child=row([column(spinner1,spinner2, spinner3, div1, div1NVW, div2, div2NVE, div3, div3NB, DCC_range_slider,down_button), tabs]),title="Dredging")
        tab6 = Panel(child=column(row(p,plegend,multi_select2), p2, data_table),title="Soil profiles")
        tab7 = Panel(child=row(psu, range_slider, pcptsu, pcptdr, multi_select),title="Geotechnical")
        tabsOuter = Tabs(tabs=[tab4, tab5, tab6, tab7])
        myapp = gridplot([[tabsOuter]], toolbar_location="left", toolbar_options={'logo': None})
        curdoc().clear()
        img3 = myapp
        for model in img3.select({'type': Model}):
            prev_doc = model.document
            model._document = None
            if prev_doc:
                prev_doc.remove_root(model)
        #html3 = curdoc().add_root(column(file_html(img3, CDN, "my plot1")))
        html3 = file_html(img3, CDN, "my plot1")'''
            #-------------------- For Testing purpose commenting code
'''# Add the polygon of the SAC
    green_box = p.patch('lon', 'lat', color='green', alpha=0.2, line_width=2, source=sourceSAC, legend_label="HHW SAC")
    p.add_layout(green_box)


    # Add the route KP
    # route1 = p.line("X1","Y1" , line_width=2, color='red', source=sourceDepth1)
    route1 = p.circle("X1","Y1" , color='red',legend_label="NVW Route KP", source=sourceDepth1)
    route2 = p.circle("X1","Y1" , color='green',legend_label="NVE Route KP", source=sourceDepth2)
    route3 = p.circle("X1","Y1" , color='brown',legend_label="NB Route KP", source=sourceDepth3)
    p.add_layout(route1), p.add_layout(route2), p.add_layout(route3)

    # Add various geographical features
    sabel=p.patches('x', 'y', source = ColumnDataSource(dict(x = x, y = y)), line_color = "white"
                    ,legend_label="Sabellaria" , color = 'red', alpha=0.5, line_width = 0.5)
    wrecks = p.circle('x', 'y', source = ColumnDataSource(dict(x = xW, y = yW)), color = 'black'
                    ,legend_label="Wrecks", line_color = "black", size = 1)
    survey = p.multi_line('x','y',  source = ColumnDataSource(dict(x = xL, y = yL)), color = 'orange'
                        ,legend_label="Survey lines", line_color = "orange")
    colorZones = linear_palette(palette, len(xZB))
    shipZonesBuffer = p.patches('x', 'y', source = ColumnDataSource(dict(x = xZB, y = yZB, c=colorZones)), line_color = "white"
                    ,legend_label="CBRA Zones" , color = 'c', alpha=0.3, line_width = 2)
    geotech = p.triangle_dot('x', 'y', source = ColumnDataSource(dict(x = xG, y = yG)), color = 'yellow'
                    ,legend_label="Geotechnical", line_color = "yellow")

    # Use js_link to connect button active property to glyph visible property
    toggle1 = Toggle(label="Toggle Areas", button_type="success", active=True, height=50, width=150)
    toggle1.js_link('active', green_box, 'visible')
    toggle1.js_link('active', sabel, 'visible')
    toggle1.js_link('active', wrecks, 'visible')
    toggle1.js_link('active', survey, 'visible')

    toggle2 = Toggle(label="Toggle KPs", button_type="success", active=True, height=50, width=150)
    toggle2.js_link('active', route1, 'visible')
    toggle2.js_link('active', route2, 'visible')
    toggle2.js_link('active', route3, 'visible')

    toggle3 = Toggle(label="Toggle Confidence", button_type="success", active=True, height=50, width=150)
    toggle4 = Toggle(label="Toggle Soil Invest.", button_type="success", active=True, height=50, width=150)

    # Add confidence level feature 
    conf = p.multi_line('x', 'y', line_color = 'color', line_width = 3, legend_label="Burial Confidence", source = sourceConf)
    conf.level = 'overlay'
    toggle3.js_link('active', conf, 'visible')

    # Add soil investigations and their names on plot
    plot1 = p.inverted_triangle('x', 'y', legend_label="Vibrocores 2016 Fugro", source=source)

    VClabels = LabelSet(x='x', y='y', text='name', text_font_size ='8pt',
                x_offset=5, y_offset=5, source=source, render_mode='canvas')
    p.add_layout(VClabels)
    plot1.js_on_change('visible', CustomJS(args=dict(ls=VClabels),
                                                code="ls.visible = cb_obj.visible;"))


    toggle4.js_link('active', plot1, 'visible')
    toggle4.js_link('active', VClabels, 'visible')

    # Customise legend
    p.legend.label_text_font_size = '10pt'
    p.legend.glyph_height = 10
    p.legend.glyph_width = 10
    p.legend.click_policy="hide" # Make legend hide glyph

    # Add hover tooltips
    p.add_tools(HoverTool(renderers=[plot1],
            tooltips=[
                #("index", "$index"),
                ("(x,y)", "($x{(0)}, $y{(0)})"),
                ("vibrocore", "@name"),
            ]
        ))
    p.add_tools(HoverTool(renderers=[green_box],
            tooltips=[
                ("(x,y)", "($x{(0)}, $y{(0)})"),
            ]
        ))

    p.add_tools(HoverTool(renderers=[route1], tooltips=[("NVW KP", "@KP")]))
    p.add_tools(HoverTool(renderers=[route2], tooltips=[("NVE KP", "@KP")]))
    p.add_tools(HoverTool(renderers=[route3], tooltips=[("NB KP", "@KP")]))
    p.add_tools(HoverTool(renderers=[conf], tooltips=TOOLTIPSconf))

    img_p = p

    return file_html(img_p, CDN, "my plot"),toggle1, toggle2, toggle3, toggle4,p'''
    #--TIll Here
# Create your tests here.


    

    


'''def UTM_to_WebMercator1(df, loc_x, loc_y, origin_epsg=32631):

    df1 = pd.DataFrame(df)
    crs = CRS.from_user_input(origin_epsg)
    #print(crs)
    
    temp_gdf = geopandas.GeoDataFrame(
        df1, geometry = geopandas.points_from_xy(df1[loc_x], df1[loc_y]))
    temp_gdf.set_crs(crs, inplace=True)
    #temp_gdf.set_crs(origin_epsg)
    temp_gdf = temp_gdf.to_crs("EPSG:3857")
    xCoTrD= []
    yCoTrD = []
    for i in temp_gdf.geometry:
        xCoTrD.append(i.x)
        yCoTrD.append(i.y)
    df1[loc_x] =  xCoTrD  
    df1[loc_y] =  yCoTrD
    #print(df1)
    return df1'''
    

