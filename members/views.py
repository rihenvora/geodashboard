import json
from msilib.schema import Component
import time
from warnings import filters
from django.shortcuts import render,redirect
from django.http import HttpResponse,FileResponse
from django.template import loader
#from django import forms
#from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage
#import altair as alt
import zipfile
import os
import mimetypes

from datetime import datetime


from python_ags4 import AGS4
import pandas as pd

from io import BytesIO
# from pandasgui import show as pdguishow

import numpy as np
import shapely
from bokeh import *
from bokeh.io import curdoc
from bokeh.embed import file_html,components
from bokeh.resources import CDN
from bokeh.models import *
from bokeh.models import Model
from bokeh.plotting import figure
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
import geopandas
from pyproj import CRS
from PIL import Image 
from .agstools import *

#Creating some global variables and keep it to access for different functions

tables,headings,cptTab, cptHead ,pcptDr,pcptSu,pcptPhi,html,html1,hdng1,hdng2,depth1,depth2,depth3,maxVClength,html2,html3,html4,dwnlodvc,KPs= '','','','','','','','','','','','','','','','','','','',''
source, depth_list, soiltype_list, full_soiltype_list,source_aug, depth_list_aug, soiltype_list_aug, full_soiltype_list_aug = '','','','','','','',''
table_keys,cpt_keys = '',''
def index(request):
    resp = {} #VAriable use for passing arguments to html page
    global tables,headings,cptTab, cptHead ,pcptDr,pcptSu,pcptPhi,html,html1,hdng1,hdng2,depth1,depth2,depth3,maxVClength,html2,html3,html4,dwnlodvc, source, depth_list, soiltype_list, full_soiltype_list,source_aug, depth_list_aug, soiltype_list_aug, full_soiltype_list_aug,KPs
    file,file1,file2,file3,file4='','','','','' #files which user will upload
    #Checking method is post or not and other form fields are done or not.
    if request.method == "POST" and 'ags' in request.POST and request.FILES['file'] != '' and request.FILES['file1'] !='' and request.FILES['file2'] !='':
        print("RIHEN")
        file = request.FILES['file']
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        #print(file)
        fss = FileSystemStorage('media')
        fs = fss.save(file.name,file)
        fs1 = fss.save(file1.name,file1)
        fs2 = fss.save(file2.name,file2)
        #file_url = fss.url(fs)
        request.FILES['file']=''
        request.FILES['file1']=''
        request.FILES['file2']=''
        # tables, headings = AGS4.AGS4_to_dataframe('Input_GeoViewer/AGS/204211_Cable Route_Laboratory Data.ags')
        tables, headings = AGS4.AGS4_to_dataframe('media/'+file.name)
        # tables, headings = AGS4.AGS4_to_dataframe('Input_GeoViewer/AGS/205080 Laboratory data_v2 noCPT.ags')
        cptTab, cptHead = AGS4.AGS4_to_dataframe('media/'+file1.name)
        #KPs = pd.read_excel('static/Norfolk Vanguard - Geotechnical Locations - 20210917.xlsx')
        KPs = pd.read_excel('media/'+file2.name)
        #sheet_name = pd.ExcelFile(KPs).sheet_names 
        # pdguishow(**tables)
        os.remove('media/'+file.name)
        os.remove('media/'+file1.name)
        os.remove('media/'+file2.name)
        #print(KPs.iloc[0])
        #print(KPs.keys())
        #print(list(cptTab.keys()))
        #print(list(tables.keys()))
        #global table_keys,cpt_keys
        table_keys = list(tables.keys())
        cpt_keys = list(cptTab.keys())
        exl_keys = list(KPs.keys())
        #print(sheet_name)
        #print("From INdex",testTab)
        #print(KPs.columns)
        #print(cptTab.keys())
        #print(cptTab.keys())
        

        resp = {
        'table_keys': table_keys,
        'cpt_keys' : cpt_keys, 
        'exl_keys' : exl_keys,       
        }

    return render(request,"index.html",resp)
    
    #return
    #template = loader.get_template('index.html')
    #return HttpResponse(template.render())

def cds(cptNames,depth,su,dr,phi,title,multi,title1,title2,multi1,multi2):
    #print(phi)
    length = len(cptNames)
    colors = linear_palette(palette, length)
    #print(colors)
    #print([varx[1] for varx in enumerate(cptNames)])
    if len(phi)>0:
        sourceCPT = ColumnDataSource(dict(names = cptNames, depth = depth, su = su, dr = dr,phi = phi, color=colors))
    else:
        sourceCPT = ColumnDataSource(dict(names = cptNames, depth = depth, su = su, dr = dr, color=colors))
    #print(type(sourceCPT))
    
    multi_select = MultiSelect(value=cptNames, options=cptNames, height=300, title='CPT investigations')
    # This callback is crucial, otherwise the filter will not be triggered when the slider changes
    multi_select_callback = CustomJS(args=dict(source=sourceCPT), code="""
        source.change.emit();
    """)
    multi_select.js_on_change('value', multi_select_callback)

    cpt_filter = CustomJSFilter(args = dict(multiselect=multi_select), code=
    '''
    var indices = [];
    var select = multiselect.value
    // iterate through rows of data source and see if each satisfies some constraint
    for (var i = 0; i < source.get_length(); i++){
        if (select.includes(source.data['names'][i]) ){
            indices.push(true);
        } else {
            indices.push(false);
        }
    }
    return indices;
    ''')
    #print(cpt_filter)
    viewCPT = CDSView(source=sourceCPT, filters=[cpt_filter])

    pcptSu,pcptDr,pcptPhi='','',''
    pcptSu = getFigure(multi,title,sourceCPT,viewCPT)
    pcptDr = getFigure(multi1,title1,sourceCPT,viewCPT)
    #print(pcptDr,pcptPhi,pcptSu,multi_select)
    #print(phi)
    if len(phi) == 0:
        print("Phi Empty")
        img1 = row(pcptSu,pcptDr,multi_select)
        #print(title," ends here")
        
    else:
        print("Phi not empty")
        pcptPhi = getFigure(multi2,title2,sourceCPT,viewCPT)
        img1 = row(pcptSu,pcptDr,pcptPhi,multi_select)
    #output_file("testpage.html")
    #print(file_html(img1, CDN, "my plot"))
    #show(pcptSu)
    return file_html(img1, CDN, "my plot"),multi_select,pcptSu,pcptDr,pcptPhi
    #return img1,multi_select,pcptSu,pcptDr,pcptPhi
    

def getFigure(multi,title,sourceCPT,viewCPT):
    print("Get Figure Start")
    pcptSu = figure(width=400, height=700,title=title, x_axis_label=multi.upper()+" [KPa]",
                    y_axis_label="Depth [m]",sizing_mode ="stretch_both",output_backend="webgl")
    #pcptSu.multi_line(multi, 'depth', source = sourceCPT, view=viewCPT, line_color = 'color',legend = 'names')
    pcptSu.multi_line(multi, 'depth', source = sourceCPT, view=viewCPT, line_color = 'color')
    pcptSu.y_range.flipped = True
    #pcptSu.legend.click_policy="mute"

    pcptSu.add_tools(HoverTool(show_arrow=False, 
            line_policy='next',
            tooltips=[
    #             ("(x,y)", "($x{(0)}, $y{(0)})"),
                ("CPT", "@names"),
                ("Depth [m]", "$data_y"),
                (multi+" [KPa]", "$data_x")
            ]
        ))

    curdoc().clear()
    #script, div = components(pcptSu)
    print("Get Figure RIhen")
    #save(pcptSu)
    return pcptSu

def readExcel(filepath,kps,dol):
    depth = pd.read_excel(filepath)
    depth1=depth.loc[0::1, ['Easting', 'Northing', 'KP','RSBL_Z', 'BE_2025_Z']]
    depth1['2021 Bathy LAT (m)'] = np.nan
    depth1.rename(columns={'Easting': 'POINT_X', 'Northing': 'POINT_Y', 'BE_2025_Z':'2025_BE_Bathy', 'RSBL_Z':'RSBL'}, inplace=True)
    depth1["DOL"] = np.nan
    KPsOfDOL1 = kps
    DOL_List1 = dol

    for i in range(len(DOL_List1)):
        depth1.loc[(depth1.KP>=KPsOfDOL1[i]) & (depth1.KP<KPsOfDOL1[i+1]) , 'DOL'] = DOL_List1[i]
    ## depth3.loc[(depth3.KP>0) & (depth3.KP<64.3) , 'DOL'] = 1.9
    # depth1['2025_BE_Bathy']=-depth1['2025_BE_Bathy']
    # depth1['RSBL']=-depth1['RSBL']
    depth1['TOC']=depth1['RSBL']-depth1["DOL"]
    depth1['ESL']=depth1['TOC']
    depth1['Dredge height'] = depth1['2025_BE_Bathy']-depth1['ESL']

    return depth1


def getShapeFile(fpth):
    print("Start Shape file")
    sf = geopandas.read_file(fpth)
    try:
        #sf = sf.set_crs('epsg:32631')
        crs = CRS.from_user_input(32631)
        #print(crs)
        sf.set_crs(crs, inplace=True,allow_override=True)
        sf = sf.to_crs("EPSG:3857")
    except Exception as e:
        print(e)
    print("Shape ends")
    return sf

def getOffshoremap(TOOLS,xL,yL,source1):
    #print(len(source1.data['DCC']))
    print("Getting offshoremap")
#def getOffshoremap(TOOLS,sourceSAC,x,y,xL,yL,xW,yW,xZB,yZB,xG,yG,sourceDepth1,sourceDepth2,sourceDepth3,TOOLTIPSconf,sourceConf,source):
    tile_provider = get_provider(CARTODBPOSITRON)
    #tile_provider = get_provider('OSM')

    
    # range bounds supplied in web mercator coordinates>
    p = figure(tools=TOOLS, output_backend="webgl",
            x_axis_type="mercator", y_axis_type="mercator", title='Offshore map, cable routes and soil investigations',
            x_axis_label='Longitude [deg]', y_axis_label='Latitude [deg]',sizing_mode="stretch_width", toolbar_location="left",
            plot_width=350,plot_height=950)
    
                
    p.toolbar.logo = None
    p.add_tile(tile_provider)

    # Add various geographical features

    RPL = p.multi_line('x','y',  source = ColumnDataSource(dict(x = xL, y = yL)), color = 'black'
                        ,legend_label="RPL", line_color = "black")

    # Use js_link to connect button active property to glyph visible property
    toggle1 = Toggle(label="Toggle Areas", button_type="success", active=True, height=50, width=150)

    toggle1.js_link('active', RPL, 'visible')

    toggle4 = Toggle(label="Toggle Soil Invest.", button_type="success", active=True, height=50, width=150)


    # Add soil investigations and their names on plot
    plot1 = p.inverted_triangle('x', 'y', legend_label="Vibrocores", source=source1)

    VClabels = LabelSet(x='x', y='y', text='name', text_font_size ='7pt',
                x_offset=5, y_offset=-5, angle=-np.pi/4, source=source1, render_mode='canvas')
    #show(plot1)
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
    #             ("(x,y)", "($x{(0)}, $y{(0)})"),
                ("vibrocore", "@name"),
                ("KP", "@KP"),
                ("DCC", "@DCC"),
            ]
        ))


    img_p = p
    print("offshore map got")
    return file_html(img_p, CDN, "my plot"),toggle1, toggle4, p

def getPs(TOOLS,sourceDepth1,ttl):
    #print(ttl)
    print("GEtting Ps")
    p1 = figure(tools=TOOLS, width=1100, height=500, title=ttl, x_axis_label="KP [km]", y_axis_label="Depth [m]"
           , sizing_mode="stretch_width")
    p1.toolbar.logo = None
    ######################

    ###################

    # # Add second axis to the right for the slope values
    # p1.extra_y_ranges = {"foo": Range1d(start=0, end=25)}
    # p1.add_layout(LinearAxis(y_range_name="foo", axis_label='Slope [degrees]'), 'right')

    # add multiple renderers
    l1 = p1.line('KP', 'LAT2021', legend_label="LAT 2021", line_color="blue", line_width=2, source=sourceDepth1, name='lat2021')
    # l1.nonselection_glyph = Line(line_color='gray',line_alpha=0.2)
    # l1.selection_glyph = Line(line_color='blue')
    l2 = p1.line('KP', 'LAT2025', legend_label="LAT 2025", line_color="red", line_width=2, source=sourceDepth1, name='lat2025')
    l3 = p1.line('KP', 'RSBL', legend_label="RSBL", line_color="green", line_width=2, source=sourceDepth1, name='rsbl')

    ## Test feature
    h1 = p1.line('KP', 'dHeight', legend_label="Dredge h", line_color="black", line_width=2, source=sourceDepth1, name='dHeight')
    toc1 = p1.line('KP', 'TOC', legend_label="Top of Cable", line_color="brown", line_width=2, source=sourceDepth1, name='toc')
    dol1 = p1.line('KP', 'DOL', legend_label="Depth of Lowering", line_color="orange", line_width=2, source=sourceDepth1, name='dol')
    esl1 = p1.line('KP', 'ESL', legend_label="Engineering seabed level", line_color="purple", line_width=2, source=sourceDepth1, name='esl')

    p1.add_tools(HoverTool(tooltips=[
                ("KP", "@KP"),
                ("LAT 2021", "@LAT2021"),
                ("LAT 2025", "@LAT2025"),
                ("RSBL", "@RSBL"),
                ("TOC", "@TOC"),
                ("DOL", "@DOL"),
                ("ESL", "@ESL"),
            ], names=['lat2021','lat2025','rsbl', 'toc', 'dol', 'esl']))

    p1.add_tools(HoverTool(tooltips=[("KP", "@KP"),("Dredge height", "@dHeight")], names=['dHeight']))
    p1.legend.click_policy="hide"
    print("Got P")
    return p1


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        #print("Root - ",root)
        
        for file in files:
            #print("File - ",file)
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))
            #print(ziph.filename)
            os.remove(root+file)
    ##print(MEDIA_ROOT)
    getvc = ziph.filename
    #getvc = ziph
    return getvc
    

def getVCDownload(source,depth_list,color_palette,soiltype_list,soil_types):
    print("Dowloading VCs")
    noVCs = len(source.data['name'])
    #print(source.data)
    print(noVCs)
    #taking time variable in order to keep uniquenes in folder naming
    now = datetime.now()
    #current_time = now.strftime("%H%M%S")

    #creating directory for storing files
    dirname = "vc_"+str(datetime.now().strftime('%Y%m%d%H%M%S')) #2010.08.09.12.08.45 
    os.mkdir(os.path.join('static/Images/ExportVC/', dirname))

    tic = time.perf_counter()
    for i in range(noVCs):
#       print(i)
        ts = {}
        for k, v in source.data.items():
            #print(k, v)
    #         print(v[i])
            ts[k]=[]
            ts[k].append(v[i])
        tempSource = ColumnDataSource(ts)

        vcName = tempSource.data['name']
    #     print(vcName[0])
    #     print(tempSource.data)
        myfig = figure(plot_width=250, x_range=vcName, plot_height=3500, y_axis_label='Depth [m]',sizing_mode="stretch_both")
        myfig.y_range.flipped = True

        myfig.xaxis.major_label_orientation = "vertical"
        myfig.y_range.start = 3.1
        myfig.y_range.end = 0
        myfig.axis.visible = False
        myfig.grid.visible = False
        myfig.toolbar.logo = None
        myfig.toolbar_location = None

        myfig.vbar_stack( depth_list, x="name",  width=1,  
                fill_color=[
                    factor_cmap(state, palette=color_palette, factors=soil_types) 
                    for state in soiltype_list],
                line_color="black", 
                #hatch_pattern=[
        #                 factor_hatch(state, patterns=[".", " "," "," "," ", ".", " "," "], factors=soil_types)
        #                 for state in ["c1","c2","c3","c4","c5"]],
                source=tempSource)
        

        #print(type(myfig))
        path = "static\Images\ExportVC\\"+str(dirname)+"\\"+vcName[0]+".png"
        #img=Image.open(myfig)
        #img.save(path)
        print("exporting")

        export_png(myfig, filename=path)
    toc = time.perf_counter()
    print(toc)
    print(f"Created the picture in {(toc - tic)/60:0.4f} Min")   
    print("Zipping VCs")
    #ZipFile("Filename you want to give to zip file") as zipf:
        #zipdir('directory path to locate files')
    with zipfile.ZipFile('static/Images/ExportVC/'+dirname+'.zip', 'x', zipfile.ZIP_DEFLATED) as zipf:
            zipvc = zipdir('static/Images/ExportVC/'+dirname+'/', zipf)
    #print(type(zipvc))
    print("Zip Done")
    return zipvc
            

def getUserData(request):
    #print("FUnction Called")
    #return HttpResponse(request.POST['text'])
    print("from func",request.POST['tab_keys'],request.POST['cp_keys'])
    #Taking all inputs from user and storing to local variable.
    cpdf = request.POST['cp_keys']
    lvan = request.POST['tab_keys']
    su_usr = request.POST['su_column']
    dpth = request.POST['depth_column']
    dr_usr = request.POST['dr_column']
    vc_excl = request.POST['vc_name']
    kp_excl = request.POST['kp_name']
    dcc_excl = request.POST['dcc_name']

    cptdf = cptTab[cpdf] # Take the dataframe with the INTERPRETED CPT values from the relevant ags file
    #print(cptdf.keys())
    cptNames = list(cptdf['LOCA_ID'].unique()[2:]) # Make a list with the unique names of all CPT investigations
    #print(cptNames)
    # List of lists with the CPT properties of each single CPT
    depth, su, dr,phi, cptOPTIONS = [], [], [], [], []
    # [(x.append(list(polygon.exterior.coords.xy[0])), y.append(list(polygon.exterior.coords.xy[1]))) for polygon in sf['geometry'] if type(polygon.boundary) == shapely.geometry.linestring.LineString ]

    headings['GEOL']
    tables['GEOL'].loc[0:10,'GEOL_DESC']

    #print(type(tables))
    #if tables.get(tables['LHVN']) == None:
    LVAN = tables[lvan].loc[2:, ['LOCA_ID', 'SPEC_DPTH', lvan+'_VNPK']] 
    LVAN['LVAN_VNPK'] = pd.to_numeric(LVAN[lvan+'_VNPK'])
    LVAN['SPEC_DPTH'] = pd.to_numeric(LVAN['SPEC_DPTH'])
    srcLVAN = ColumnDataSource(LVAN)
    srcLVAN.column_names

    LPEN = tables['LPEN'].loc[2:, ['LOCA_ID', 'SPEC_DPTH', 'LPEN_PPEN']]
    LPEN['SPEC_DPTH'] = pd.to_numeric(LPEN['SPEC_DPTH'])
    LPEN['LPEN_PPEN'] = pd.to_numeric(LPEN['LPEN_PPEN'])
    srcLPEN = ColumnDataSource(LPEN)
    srcLPEN.column_names

    for ind, i in enumerate(cptNames):
        slicedf = cptdf.loc[cptdf['LOCA_ID']==i]
        
        depth.append(list(pd.to_numeric(slicedf[dpth])))
        
        dr.append(list(pd.to_numeric(slicedf[dr_usr])))
        if su_usr == "Calculate SU":
            #su.append(calculateSu(slicedf))
            frr = list(pd.to_numeric(slicedf[cpdf+'_FRR']))
            qnet = list(pd.to_numeric(slicedf[cpdf+'_QNET']))
            lfrr=[] #for taking value in list format instead of object
            for j in range(0,len(frr)):
                if frr[j] <2:
                    lfrr.append(frr[j])
                else:
                    lfrr.append(round(qnet[j]/15,4))
            su.append(lfrr)
        else:
            su.append(list(pd.to_numeric(slicedf[su_usr])))
        
        cptOPTIONS.append((str(ind+1),i)) #= [("1", "foo"), ("2", "bar"), ("3", "baz"), ("4", "quux")]
    #print(su)
    '''print('The number of CPT investigations found is '+ str(len(cptNames)))
    print(len(su))
    print(len(cptOPTIONS))'''
    title = "CPT Undr. shear strength Su (Gridlink)"
    title1= "CPT Relative density Dr (Gridlink)"
    title2="CPT Relative density Phi"
    multi = 'su'
    multi1 = 'dr'
    multi2 = 'phi'
    
    html,multi_select,pcptsu,pcptdr,pcptPhi = cds(cptNames,depth,su,dr,phi,title,multi,title1,title2,multi1,multi2)

    names = intersect_agsLocs(tables)
    #print("RIHEN---",names)
    nn = tables['LOCA']
    df1 = nn[nn['LOCA_ID'].isin(names)]
    
    #Selecting easting and Northing
    #Need to take input from user
    if 'LOCA_LOCX' in tables['LOCA']:
        #print("intable")
        easting, northing = 'LOCA_LOCX', 'LOCA_LOCY'
    else:
        easting, northing = 'LOCA_NATE', 'LOCA_NATN'
    
    gdf = UTM_to_WebMercator(df1, easting, northing, origin_epsg="EPSG:32631")
        
    xCoTr, yCoTr = gdf[easting].tolist(), gdf[northing].tolist()
    #print(len(xCoTr),len(yCoTr))
    #print(xCoTr)
    #---------From here testing started
    yy = tables['GEOL'].loc[:,['LOCA_ID','GEOL_BASE','GEOL_DESC']]

    vcNames = yy.LOCA_ID.unique().tolist()
    vcNames = [i for i in vcNames if i in names]

    #print(vcNames)

    depthList, geoList, geoListFull, maxVClength = soil_layers_fromAGS(yy, vcNames)

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
    #print("Source",source)
    print("Reading Excel")

    KP = []
    DCC = []

    loca1 = vc_excl
    kppost = kp_excl
    dcc = dcc_excl
    
    for i in names:
        tt = KPs.loc[KPs[loca1] == i]
        #print(tt)
        #kp_post = float(tt['RPL = ITTRound2IndicativeExportRoutes.shp'])
        #DCC.append(abs(float(tt['Unnamed: 7'])))
        #kp_post = ''
        #Checking if value is pandas series or not 
        if isinstance(tt[kppost], pd.Series):
            # if its pandas series then accessing value form it.
            #print(tt[kppost])
            for d in tt[kppost]:
                kp_post = float(d)
            KP.append( float(kp_post))
        else:
            #kp_post = float(tt[kppost])
            KP.append(float(tt[kppost]))
    # if kp_post<84.3:
            
        #Checking if value is pandas series or not 
        if isinstance(tt[dcc], pd.Series):
            # if its pandas series then accessing value form it.
            for dc in tt[dcc]:
                dc_post = dc
            DCC.append(abs(float(dc_post)))
        else:
            DCC.append(abs(float(tt[dcc])))
    
    source.data['KP']=KP
    source.data['DCC']=DCC

    print(len(source.data['name']))
    #sf  = getShapeFile('static/Shapefiles/103434-Survey_Boundaries-20200520-ETRS89-31N.dxf')
    print("Getting shape file")
    sf  = getShapeFile('static/Shapefiles/shp/New Folder/P1705_NWab_GEOTECHNIC_PLAN_PNT_20220503_rev00.shp')
    
    xL, yL = [], []
    cxL, cyL = [], []
    [(cxL.append(list(line.coords.xy[0])), cyL.append(list(line.coords.xy[1]))) for line in sf['geometry']]; # if type(polygon.boundary) == shapely.geometry.linestring.LineString ]

    #print(type(cyL[0]))
    if len(cxL[0])==1:
        xlist,ylist=[],[]
        for x in range(0,len(cxL)):
            #print(type(str(cxL[x])))
            xlist.append(float(str(cxL[x]).strip("'[]")))
            ylist.append(float(str(cyL[x]).strip("'[]")))
        #print(xlist)
        xL.append(xlist)
        yL.append(ylist)
    else:
        xL, yL = cxL,cyL

    ''' xL, yL = [], []
    [(xL.append(list(line.coords.xy[0])), yL.append(list(line.coords.xy[1]))) for line in sf['geometry']]; # if type(polygon.boundary) == shapely.geometry.linestring.LineString ]'''

    TOOLS = "box_select,lasso_select, wheel_zoom, pan, crosshair, box_zoom, undo, reset"
    #print("DCC Length",len(source.data['DCC']))
    html2,toggle1, toggle4,p = getOffshoremap(TOOLS,xL,yL,source)
    
    soil_types, color_palette = loadNKTsoil_legend()

    multi_select2, viewVC = makeGeolFiltering(source, geoList, soiltype_list)

    plegend, plogo = createLogoAndLegendNew(['static/Images/soil_legend3_2.png', 'static/Images/NKT logo.png'])

    TOOLS_bar = "box_select, wheel_zoom, pan, box_zoom, reset,tap, undo"

    # Here the option to sort the vibrocores by KP is created. 
    sortedByKP = True
    #print(len(source.data['name']))
    #print(len(source.data['KP']))
    if sortedByKP == True:
        sort_df = pd.DataFrame(data={'names': source.data['name'], 'KP': source.data['KP']})
        sort_df.sort_values(by=['KP'], inplace=True)
        VC_x_range = list(sort_df['names'])
    else:
        VC_x_range = names
        
    p2 = figure(tools=TOOLS_bar, x_range=VC_x_range, plot_width=1700, plot_height=300, y_axis_label='Depth [m]',sizing_mode="stretch_width",output_backend="webgl")
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

    tab4 = Panel(child=row([p, column(toggle1, toggle4)]), title="Offshore Map")
    tab6 = Panel(child=column(row(p,plegend,multi_select2), p2, data_table),title="Soil profiles")
    if pcptPhi == '':
        tab7 = Panel(child=row(pcptsu, pcptdr, multi_select), title="CPT")
    else:
        tab7 = Panel(child=row(pcptsu, pcptdr, pcptPhi, multi_select), title="CPT")
    tabsOuter = Tabs(tabs=[tab4, tab6, tab7])

    myapp = gridplot([[tabsOuter]], toolbar_location="left", toolbar_options={'logo': None})
    curdoc().clear()
    img3 = myapp
    for model in img3.select({'type': Model}):
        prev_doc = model.document
        model._document = None
        if prev_doc:
            prev_doc.remove_root(model)
    #html3 = curdoc().add_root(img3)
    html3 = file_html(img3, CDN, "my plot1")
    #html3 = json.dumps(json_item(img3))
    #print(type(html3))

    #dwnlodvc = getVCDownload(source,depth_list,color_palette,soiltype_list,soil_types)
    resp = {
        'pcptsu' : html,
        'html3' : html3,
        'dwnlodvc' : dwnlodvc    
    }
    #return render(request,"index.html",resp)
    return HttpResponse(json.dumps(resp))

def getInterpretedCpt(request):
    #print("FUnction Called")
    #return HttpResponse(request.POST['text'])
    #print("from func",request.POST['cp_keys'])
    cptdf = cptTab[request.POST['cp_keys']]
    #print("RIhen",cptdf.iloc[0])
    cptdflst = list(cptdf.keys())
    #print(cptdflst)
    response = {
        'cpt' : request.POST['cp_keys'],
        'cptdflst' : cptdflst
    }
    return HttpResponse(json.dumps(response))

def getLVAN(request):
    #print("FUnction Called")
    #return HttpResponse(request.POST['text'])
    print("from func",request.POST['tab_keys'])
    response = {
        'tab' : request.POST['tab_keys']
    }
    return HttpResponse(json.dumps(response))
