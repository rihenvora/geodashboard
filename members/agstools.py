import geopandas
from bokeh.plotting import figure
from bokeh.colors import RGB
import numpy as np
import pandas as pd
from numpy import nan
from PIL import Image
import os
from imageio import imread
from bokeh.models import ColumnDataSource, MultiSelect, CustomJS, CustomJSFilter, CDSView
from pyproj import CRS

# Imports for geo_dashboard class
from bokeh.plotting import figure, show, save, output_file
from bokeh.io import output_notebook, export_png
from bokeh.tile_providers import CARTODBPOSITRON, get_provider, STAMEN_TERRAIN
from bokeh.models import ColumnDataSource, HoverTool, Toggle, Line, TextInput, CustomJS, Spinner, MultiChoice, RangeSlider, Div
from bokeh.models import CustomJSHover, Panel, Tabs, Plot, Range1d, DataRange1d, CDSView, CustomJSFilter, LabelSet, LinearAxis
from bokeh.models import MultiSelect, Button, TapTool
from bokeh.layouts import row, gridplot, column
from bokeh.transform import stack, factor_cmap, factor_hatch, log_cmap, linear_cmap
from bokeh.colors import RGB
from bokeh.palettes import Turbo256 as palette
from bokeh.palettes import linear_palette
from bokeh.models.widgets import DataTable, TableColumn, StringEditor
###

def loadNKTsoil_legend():
    """
    Returns the NKT in-house colour map for selected types of soil. The colors are in bokeh RGB data type.
    
    Inputs: None
    
    Outputs:
        soil_types: type: list of strings
        color_palette: list of bokeh RGB objects
    """
    
    soil_types=['very loose SAND', 'loose SAND', 'medium dense SAND', 'dense SAND','very dense SAND', 'SAND',
        'extremely low strength CLAY', 'very low strength CLAY', 'low strength CLAY', 
        'medium strength CLAY', 'high strength CLAY', 'very high strength CLAY', 'extremely high strength CLAY',
        'ultra high strength CLAY', 'CLAY', 'GRAVEL', 'SILT', 'PEAT', 'CHALK', 'OTHER', 'NAN']

    color_palette=[RGB(236,251,14), RGB(227,211,11), RGB(219,172,9), RGB(211,132,7), RGB(195,54,3), RGB(252,213,180), 
   	    RGB(92,242,250), RGB(121,209,220), RGB(107,165,224), 
        RGB(93,108,228), RGB(122,78,233), RGB(242,47,229), RGB(153,0,153), 
        RGB(153,0,153), RGB(149,179,215), RGB(148,139,84), RGB(122,220,134), RGB(220,121,178), RGB(28,98,65), RGB(181,181,181), RGB(255,255,255,0)]
    
    return soil_types, color_palette

def UTM_to_WebMercator(df, loc_x, loc_y, origin_epsg=32631):
    """
    Conversion of geographical reference frame from UTM to WebMercator for a number of coordinate pairs.
    
    Inputs: 
        df: type: pandas dataframe
        loc_x: type: string. The name of the dataframe column that contains the easting coordinates.
        loc_y: type: string. The name of the dataframe column that contains the northing coordinates.
        origin_espg: type: string. The espg name of the reference frame of the input dataframe.
    Outputs:
        copydf: type: pandas dataframe
    
    Comments:
    Some reference frames with the associated epsg codes are listed below. 
    UTM N31 - epsg: 32631
    Web Mercator - epsg: 3857
    """ 
    copydf= df.copy()
    crs = CRS.from_user_input(origin_epsg)
    #temp_gdf = geopandas.GeoDataFrame(copydf, geometry = geopandas.points_from_xy(copydf[loc_x], copydf[loc_y]), crs=origin_epsg)
    temp_gdf = geopandas.GeoDataFrame(copydf, geometry = geopandas.points_from_xy(pd.to_numeric(copydf[loc_x]), pd.to_numeric(copydf[loc_y])))
    temp_gdf.set_crs(crs, inplace=True)
    temp_gdf = temp_gdf.to_crs("EPSG:3857")
    xCoTrD= []
    yCoTrD = []
    for i in temp_gdf.geometry:
        xCoTrD.append(i.x)
        yCoTrD.append(i.y)
    copydf[loc_x] =  xCoTrD  
    copydf[loc_y] =  yCoTrD
    #print(copydf)
    return copydf

def only_upper(s):
    """
    Returns only the uppercase characters of a string.
    
    Inputs: 
        s: type: string
    
    Outputs:
        type: string
    """
    return "".join(c for c in s if c.isupper())

def parse_GEOL(s):
    """
    Takes as input a (extended) description of a geology layer, e.g. from the GEOL tab of ags files and returns a description in
    a brief and standardised format. This is used to categorise the layer in a set of limited soil types.
    
    Inputs: 
        s: type: string
    
    Outputs:
        type: string
    """

    soil_types = ['CLAY/CLAYSTONE', 'MUDSTONE', 'SILTSTONE', 'SILT', 'CLAYTILL', 'GRAVEL', 'CHALK', 'COBBLES', 'COBBLE', 'BOULDERS', 'PEAT','SAND','CLAY']
    soil_type = 'OTHER' # Every layer is initially categorised as "OTHER", unless it later falls inside one of the above categories.

    soilsFound={}
    for i in soil_types:
        
        if i in s:
            soilsFound[i]=s.find(i)
            s=s.replace(i,'')
    if soilsFound == {}:
        pass
    else:
        soil_type = min(soilsFound, key=soilsFound.get)
            

    # Define the priority order of the strength for SAND and for CLAY, i.e. which is selected if a range of strength values is present. Higher values have priority.
    strength_sand = {'very loose':0, 'loose':1, 'medium dense':2, 'very dense':4, 'dense':3}
    strength_clay = {'extremely low strength':2, 'very low strength':0, 'low strength':1, 'medium strength':3,
                     'very high strength':5, 'extremely high strength':6, 'ultra high strength':7, 'high strength':4}
    aux_list = -1
    soil_strength = ''
    if soil_type == 'SAND':
        for j in strength_sand.keys():
            if j in s:
                if strength_sand[j] > aux_list:
                    aux_list = strength_sand[j]
                s=s.replace(j,'')
#                 print(s)
        
        for strength, number in strength_sand.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            if number == aux_list:
                soil_strength = strength + ' '
    
    elif soil_type in  ['CLAY']:
        for k in strength_clay.keys():
            if k in s:
                if strength_clay[k] > aux_list:
                    aux_list = strength_clay[k]
                s=s.replace(k,'')
        
        for strength, number in strength_clay.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            if number == aux_list:
                soil_strength = strength + ' '
                
    return soil_strength + soil_type


def soil_layers_fromAGS(table, investig_names):
    
    assert len(investig_names)>0, 'Empty list of investigations passed.'
    
    bottomList=[]
    GeoDescr=[]
    fullGeoDescr=[]
    
    for i in investig_names:
        bottomList.append(pd.to_numeric(table.loc[table['LOCA_ID'] == i]['GEOL_BASE']).tolist())
        descr = table.loc[table['LOCA_ID'] == i]['GEOL_DESC'].tolist()
        
        briefOnly=[]
        fullG=[]
        for s in descr: 
            briefOnly.append(parse_GEOL(s)) # Create the standard geology description
            fullG.append(s)
        GeoDescr.append(briefOnly)
        fullGeoDescr.append(fullG)
    
    # Fill the layers with dummy values so that they all have the same length
    maxVClength = max(map(len, bottomList))
    print('Maximum number of layers is {}.'.format(maxVClength))
    y=np.array([xi+[nan]*(maxVClength-len(xi)) for xi in bottomList])
    
    yh = np.round(np.diff(y, n=1, axis=1, prepend=0),2) # take the difference to find the layer thickness
    #print(yh)
    
    thicknessList=[]
    for i in range(yh.shape[1]):
        thicknessList.append(list(yh[:,i]))
        
    layerTypes = np.array([xi+["NaN"]*(maxVClength-len(xi)) for xi in GeoDescr])
    fullLayerTypes = np.array([xi+["NaN"]*(maxVClength-len(xi)) for xi in fullGeoDescr])
    
    geologyList=[]
    fullGeologyList=[]
    for i in range(layerTypes.shape[1]):
        geologyList.append(list(layerTypes[:,i]))
        fullGeologyList.append(list(fullLayerTypes[:,i]))
        
    return thicknessList, geologyList, fullGeologyList, maxVClength

def intersect_agsLocs(tables, tab1='LOCA', tab2='GEOL'):
    """
    Takes as main input a dictionary of pandas dataframes, as returned by the ags4 package for 
    reading ags files. Optional inputs are the names of the 2 specific dataframes to be used (default is "LOCA" and "GEOL").
    They should have a field named "LOCA_ID". Returns a description in
    a brief and standardised format. This is used to categorise the layer in a set of limited soil types.
    
    Inputs: 
        s: type: string
    
    Outputs:
        type: string
    """
    
    # Get the names of the locations from 'LOCA' tab.
    names_LOCA = tables[tab1].loc[2:,'LOCA_ID'].values.tolist()
    #print("names loca",names_LOCA)

    # Get names of soil investigations directly from relevant tab, e.g. 'GEOL'
    names_GEOL = tables[tab2].loc[2:,'LOCA_ID']
    #print("names geol",names_GEOL)
    names_GEOL = names_GEOL[names_GEOL.isin(names_LOCA)] # Filter to get the ones which also exist in 'LOCA' tab (coordinates) 
    names = np.unique(names_GEOL.values).tolist() # Get list of unique values
    #print('Compared locations of tabs ' + tab1 + ' and ' + tab2 + ' and returned a list of common locations.')
    #print("names from agstools",names)
    #There is chances that AGS might appear in VC's list just to make sure that it should be removed before returning final list
    if 'AGS' in names:
            names.remove('AGS')
    #print("names from agstools",names)
    return names

def replaceNans(mylist):
    for ind,i in enumerate(mylist):
        if i==None:
            mylist[ind]="NaN"
    return mylist

def VCgeologySource(names, xCoTr, yCoTr, mylist, mylist2, mylist3):
    test_source = ColumnDataSource(data=dict(name=names, x=xCoTr, y=yCoTr))
    
    noOfLayers = len(mylist)
    depth_list = []
    soiltype_list =[]
    full_soiltype_list=[]
    # Create lists with values based on number of layers
    for i in range(noOfLayers):
        name1 = 'd'+str(i+1) 
        name2 = 'c'+str(i+1)   
        name3 = 'f'+str(i+1)
        
        depth_list.append(name1)
        soiltype_list.append(name2)
        full_soiltype_list.append(name3)
        test_source.data[name1]=np.nan_to_num(mylist[i])
        test_source.data[name2]=np.nan_to_num(mylist2[i])
        test_source.data[name3]=np.nan_to_num(mylist3[i])

    print("from ags tools ",test_source)   
    print("from ags tools ",depth_list)
    print("from ags tools ",soiltype_list)
    print("from ags tools ",full_soiltype_list)                       
    return test_source, depth_list, soiltype_list, full_soiltype_list

def makeGeolFiltering(source, geolList_short, soiltype_list):
    # This block is implementing the filtering of vibrocores based on soil type
    # First take the set of all (unique) soil types that exist in the project
    myset = list({x for l in geolList_short for x in l})
    soilsForFilter = []
    soil_types = loadNKTsoil_legend()[0]
    for i in soil_types:
        if i in myset:
            soilsForFilter.append(i)
    for j in myset:
        if j not in soil_types:
            soilsForFilter.append(j)
    soilsForFilter.remove('NaN')
    # myset.sort(key=lambda v: ''.join([c for c in v if c.isupper()]))

    multi_selectGEOL = MultiSelect(value=soilsForFilter, options=soilsForFilter, height=300, width=250, title='Soil types in Vibrocore')
    # This callback is crucial, otherwise the filter will not be triggered when the slider changes
    multi_select_callback = CustomJS(args=dict(source=source), code="""
        source.change.emit();
    """)
    multi_selectGEOL.js_on_change('value', multi_select_callback)

    vc_filter = CustomJSFilter(args = dict(multiselect=multi_selectGEOL, layers=soiltype_list), code=
    '''
    var indices = [];
    var select = multiselect.value

    // iterate through rows of data source and see if each satisfies some constraint
    for (var i = 0; i < source.get_length(); i++){
        var flag = false
        for (var j = 0; j < layers.length; j++){
            if (select.includes(source.data[layers[j]][i]) ){
            flag = true;
            }
        }
        if (flag == true) {
            indices.push(true);
        } else {
            indices.push(false);
        }
    }
    return indices;
    ''')
    viewVC = CDSView(source=source, filters=[vc_filter])
    return multi_selectGEOL, viewVC
    
def slope_Cb(dHeight, resolution):
    string="""
            const inds = s.selected.indices;
            const d = s.data;
            var ym = 0
            var temp1 = 0
            var volume = 0
            var dep = sp1.value
            var width = sp2.value
            var slope = cb_obj.value

            if (inds.length == 0)
                return;


            for (var i = 0; i < inds.length; i++) {{

                if (isNaN(d['{one}'][inds[i]])) {{
                }} else {{
                    temp1 = d['{one}'][inds[i]];
                    if (temp1>0) {{
                        ym += temp1*(width+slope*temp1);
                    }}
                }}
            }}


            //s2.data['ym'] = [ym, ym]
            volume= Math.round({two}*ym)
            s2.data['myText'][0] = "Dredge volume [m3] : " + volume.toLocaleString('en', {{useGrouping:true}})
	    s2.data['ym'][0] = volume.toLocaleString('en', {{useGrouping:true}})

            s.change.emit();
            s2.change.emit();
        """.format(one = dHeight, two = resolution)
    return string

def width_Cb(dHeight, resolution):
    string="""
            const inds = s.selected.indices;
            const d = s.data;
            var ym = 0
            var temp1 = 0
            var volume = 0
            var dep = sp1.value
            var width = cb_obj.value
            var slope = sp3.value

            if (inds.length == 0)
                return;


            for (var i = 0; i < inds.length; i++) {{

                if (isNaN(d['{one}'][inds[i]])) {{
                }} else {{
                    temp1 = d['{one}'][inds[i]];
                    if (temp1>0) {{
                        ym += temp1*(width+slope*temp1);
                    }}
                }}
            }}


            //s2.data['ym'] = [ym, ym]
            volume= Math.round({two}*ym)
            s2.data['myText'][0] = "Dredge volume [m3] : " + volume.toLocaleString('en', {{useGrouping:true}})
	    s2.data['ym'][0] = volume.toLocaleString('en', {{useGrouping:true}})

            s.change.emit();
            s2.change.emit();
        """.format(one = dHeight, two = resolution)
    return string


def depth_Cb(dHeight, resolution):
    string="""
            const inds = s.selected.indices;
            const d = s.data;
            var ym = 0
            var temp1 = 0
            var volume = 0
            var dep = cb_obj.value
            var width = sp2.value
            var slope = sp3.value

            if (inds.length == 0)
                return;


            for (var i = 0; i < inds.length; i++) {{

                if (isNaN(d['{one}'][inds[i]])) {{
                }} else {{
                    temp1 = d['{one}'][inds[i]];
                    if (temp1>0) {{
                        ym += temp1*(width+slope*temp1);
                    }}
                }}
            }}


            //s2.data['ym'] = [ym, ym]
            volume= Math.round({two}*ym)
            s2.data['myText'][0] = "Dredge volume [m3] : " + volume.toLocaleString('en', {{useGrouping:true}})
	    s2.data['ym'][0] = volume.toLocaleString('en', {{useGrouping:true}})

            s.change.emit();
            s2.change.emit();
        """.format(one = dHeight, two = resolution)
    return string

def selected_ind_Cb(dHeight, resolution):
    string="""
            const inds = s.selected.indices;
            const d = s.data;
            var ym = 0
            var temp1 = 0
            var volume = 0
            var dep = sp1.value
            var width = sp2.value
            var slope = sp3.value

            if (inds.length == 0) {{
                //return;
                volume=0;
                }}
                else {{


                    for (var i = 0; i < inds.length; i++) {{

                        if (isNaN(d['{one}'][inds[i]])) {{
                        }} else {{
                            temp1 = d['{one}'][inds[i]];
                            if (temp1>0) {{
                                ym += temp1*(width+slope*temp1);
                            }}
                        }}
                    }}


                    //s2.data['ym'] = [ym, ym]
                    volume= Math.round({two}*ym)
                    }}
            s2.data['myText'][0] = "Dredge volume [m3] : " + volume.toLocaleString('en', {{useGrouping:true}})
	    s2.data['ym'][0] = volume.toLocaleString('en', {{useGrouping:true}})

            s.change.emit();
            s2.change.emit();
        """.format(one = dHeight, two = resolution)
    return string

def heightLine_Cb(lat, rsbl, dheight):
    string="""

            const d = s.data;
            var dep = cb_obj.value
            var temp = 0

            for (var i = 0; i < s.get_length(); i++) {{

                if (isNaN(d['{one}'][i])) {{
                }} else if (isNaN(d['{two}'][i])) {{
                }} else {{
                    temp = d['{one}'][i]-(d['{two}'][i]+dep);
                    if (temp>0) {{
                        s.data['{three}'][i]=temp;
                    }} else {{
                        s.data['{three}'][i]=0;
                    }}

                }}
            }}
            s.change.emit();

        """.format(one = lat, two = rsbl, three=dheight)
    return string

def heightLineWithDOL_Cb(lat, toc, dheight, esl):
    string="""

            const d = s.data;
            var dep = cb_obj.value
            var temp = 0
            var temp2 =0

            for (var i = 0; i < s.get_length(); i++) {{

                if (isNaN(d['{one}'][i])) {{
                }} else if (isNaN(d['{two}'][i])) {{
                }} else {{
                    temp2 = s.data['{two}'][i]+dep
                    s.data['{four}'][i] = temp2
                    temp = d['{one}'][i]-temp2;
                    if (temp>0) {{
                        s.data['{three}'][i]=temp;
                    }} else {{
                        s.data['{three}'][i]=0;
                    }}

                }}
            }}
            s.change.emit();

        """.format(one = lat, two = toc, three=dheight, four=esl)
    return string

def slider_filter(test_type):
    string='''
        var indices = [];
        var limits = slider.value
        // iterate through rows of data source and see if each satisfies some constraint
        for (var i = 0; i < source.get_length(); i++){{
            if (source.data['{one}'][i] >limits[0] && source.data['{one}'][i] <limits[1]){{
                indices.push(true);
            }} else {{
                indices.push(false);
            }}
        }}
        return indices;
        '''.format(one=test_type)
        
    return string

def download_csv():
    string='''
        function table_to_csv(source) {
            const columns = Object.keys(source.data)
            const nrows = source.get_length()
            const lines = [columns.join(',')]

            for (let i = 0; i < nrows; i++) {
                let row = [];
                for (let j = 0; j < columns.length; j++) {
                    const column = columns[j]
                    row.push(source.data[column][i].toString())
                }
                lines.push(row.join(','))
            }
            return lines.join('\\n').concat('\\n')
        }


        const filename = 'data_result.csv'
        const filetext = table_to_csv(source)
        const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' })

        //addresses IE
        if (navigator.msSaveBlob) {
            navigator.msSaveBlob(blob, filename)
        } else {
            const link = document.createElement('a')
            link.href = URL.createObjectURL(blob)
            link.download = filename
            link.target = '_blank'
            link.style.visibility = 'hidden'
            link.dispatchEvent(new MouseEvent('click'))
        }

        '''
    return string

def createLogoAndLegend(paths):
    # Import images for NKT logo and soil legend

    # Open image, and make sure it's RGB*A*
    legend_img = Image.open(paths[0]).convert('RGBA')
    xdim, ydim = legend_img.size
    print("Dimensions: ({xdim}, {ydim})".format(**locals()))

    # Create an array representation for the image `img`, and an 8-bit "4
    # layer/RGBA" version of it `view`.
    img = np.empty((ydim, xdim), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))

    # Copy the RGBA image into view, flipping it so it comes right-side up
    # with a lower-left origin
    view[:,:,:] = np.flipud(np.asarray(legend_img))
    dim = max(xdim, ydim)

    plegend = figure(x_range=(0,1), y_range=(0,1), plot_width=854, plot_height=250, tools='', sizing_mode="scale_width")
    plegend.toolbar.logo = None

    plegend.image_rgba(image=[img], x=0, y=0, dw=1, dh=1)

    ###############
    
    # Open image, and make sure it's RGB*A*
    logo_img = Image.open(paths[1]).convert('RGBA')
    xdim, ydim = logo_img.size
    print("Dimensions: ({xdim}, {ydim})".format(**locals()))

    # Create an array representation for the image `img`, and an 8-bit "4
    # layer/RGBA" version of it `view`.
    img = np.empty((ydim, xdim), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))

    # Copy the RGBA image into view, flipping it so it comes right-side up
    # with a lower-left origin
    view[:,:,:] = np.flipud(np.asarray(logo_img))
    dim = max(xdim, ydim)

    plogo = figure(x_range=(0,1), y_range=(0,1), plot_width=300, plot_height=110, tools='', min_border_bottom = 30)
    plogo.toolbar.logo = None

    plogo.image_rgba(image=[img], x=0, y=0, dw=1, dh=1)
    ###############

    # Disable interaction with the images
    plegend.xaxis.visible = False 
    plegend.yaxis.visible = False
    plegend.xgrid.grid_line_color = None
    plegend.ygrid.grid_line_color = None

    plogo.xaxis.visible = False
    plogo.yaxis.visible = False
    plogo.xgrid.grid_line_color = None
    plogo.ygrid.grid_line_color = None

    return plegend, plogo

def createLogoAndLegendURL(paths):
    # Import images for NKT logo and soil legend

    plegend = figure(x_range=(0,1), y_range=(0,1), plot_width=854, plot_height=250, tools='', sizing_mode="scale_width")
    plegend.toolbar.logo = None

    plegend.image_url(url=[os.getcwd()+r'\\'+paths[0]], x=0, y=1, w=1, h=1)
    ###############
    
    plogo = figure(x_range=(0,1), y_range=(0,1), plot_width=300, plot_height=110, tools='', min_border_bottom = 30)
    plogo.toolbar.logo = None

    plogo.image_url(url=[os.getcwd()+r'\\'+paths[1]], x=0, y=1, w=1, h=1)
    ###############

    # Disable interaction with the images
    plegend.xaxis.visible = False 
    plegend.yaxis.visible = False
    plegend.xgrid.grid_line_color = None
    plegend.ygrid.grid_line_color = None

    plogo.xaxis.visible = False
    plogo.yaxis.visible = False
    plogo.xgrid.grid_line_color = None
    plogo.ygrid.grid_line_color = None

    return plegend, plogo

def createLogoAndLegendNew(paths):
    # Import images for NKT logo and soil legend fwy24453@nezid.com

    
    viewIn = imread(paths[0])
    shape = viewIn.shape
    width,height =shape[0],shape[1]
    img = np.empty((width,height), dtype=np.uint32)
    
    view = img.view(dtype=np.uint8).reshape((width, height, 4))
    for i in range(width):
        for j in range(height):
            view[width-1-i, j, 0] = viewIn[i,j,0]
            view[width-1-i, j, 1] = viewIn[i,j,1]
            view[width-1-i, j, 2] = viewIn[i,j,2]
            view[width-1-i, j, 3] = viewIn[i,j,3]

    plegend = figure(x_range=(0,1), y_range=(0,1), plot_width=380, plot_height=111, tools='', sizing_mode="scale_width")
    plegend.toolbar.logo = None

    plegend.image_rgba(image=[img], x=0, y=0, dw=1, dh=1)

    ###############
    
    viewIn = imread(paths[1])
    shape = viewIn.shape
    width,height =shape[0],shape[1]
    img = np.empty((width,height), dtype=np.uint32)
    
    view = img.view(dtype=np.uint8).reshape((width, height, 4))
    for i in range(width):
        for j in range(height):
            view[width-1-i, j, 0] = viewIn[i,j,0]
            view[width-1-i, j, 1] = viewIn[i,j,1]
            view[width-1-i, j, 2] = viewIn[i,j,2]
            view[width-1-i, j, 3] = viewIn[i,j,3]

    plogo = figure(x_range=(0,1), y_range=(0,1), plot_width=300, plot_height=110, tools='', min_border_bottom = 30)
    plogo.toolbar.logo = None

    plogo.image_rgba(image=[img], x=0, y=0, dw=1, dh=1)
    ###############

    # Disable interaction with the images
    plegend.xaxis.visible = False 
    plegend.yaxis.visible = False
    plegend.xgrid.grid_line_color = None
    plegend.ygrid.grid_line_color = None

    plogo.xaxis.visible = False
    plogo.yaxis.visible = False
    plogo.xgrid.grid_line_color = None
    plogo.ygrid.grid_line_color = None

    return plegend, plogo



class geo_Dashboard(object):
    
    def __init__(self, proj_name='Project', routeNames=[]):
        self.sourceBathyDict={}
        self.bathyFigs={}
        self.routeNames = routeNames
        self.mainMapToggles = []
        pass
    
    def make_main_map(self):
        
        # Get the map layer for the main plot
        tile_provider = get_provider(CARTODBPOSITRON)

        TOOLS = "box_select,lasso_select, wheel_zoom, pan, crosshair, box_zoom, undo, reset"
        # range bounds supplied in web mercator coordinates>
        self.mainMap = figure(tools=TOOLS, output_backend="webgl", width=400, height=180, x_range=(246000, 266000), y_range=(6700000, 7050000),
                   x_axis_type="mercator", y_axis_type="mercator", title='Offshore map, cable routes and soil investigations',
                  x_axis_label='Longitude [deg]', y_axis_label='Latitude [deg]', toolbar_location="left", sizing_mode="scale_width")
          
        self.mainMap.toolbar.logo = None
        self.mainMap.add_tile(tile_provider)
        
        
        
        
    def map_add_rplBathy(self):
        
        routeColors = ['red','green','brown','orange','magenta', 'blue']
        toggle2 = Toggle(label="Toggle KPs", button_type="success", active=True, height=50, width=150)
        self.mainMapToggles.append(toggle2)
        
        # Add the route KP
        counter=0
        for key, value in self.sourceBathyDict.items():
            
            route1 = self.mainMap.circle("X1","Y1" , color=routeColors[counter], legend_label=f"{key} Route KP", source=value)
            self.mainMap.add_layout(route1)

            toggle2.js_link('active', route1, 'visible')
            self.mainMap.add_tools(HoverTool(renderers=[route1], tooltips=[(f"{key} KP", "@KP")]))
            counter+=1

        # Customise legend
        self.mainMap.legend.label_text_font_size = '10pt'
        self.mainMap.legend.glyph_height = 10
        self.mainMap.legend.glyph_width = 10
        self.mainMap.legend.click_policy="hide" # Make legend hide glyph
        
    def make_bathy_source(self, depthDict):

        for key, value in depthDict.items():
            self.sourceBathyDict[key]= ColumnDataSource(data=dict({'KP':value['KP'], 'LAT2021':value['2021 Bathy LAT (m)'], 
                                        'X1':value['POINT_X'], 'Y1':value['POINT_Y'], 'LAT2025':value['2028_BE_Bathy'],
                                        'RSBL':value['RSBL'], 'dHeight':value['Dredge height'], 'TOC':value['TOC'],
                                        'DOL':-value['DOL'], 'ESL':value['ESL']}))
    
    def make_bathy_fig(self, width=1100, height=500):
        
        TOOLS = "box_select,lasso_select, wheel_zoom, pan, crosshair, box_zoom, undo, reset"
        self.bathyTabsList = []
        
        for key, value in self.sourceBathyDict.items():
            p1 = figure(tools=TOOLS, width=width, height=height, title=f"Depth along route {key}", x_axis_label="KP [km]",
                        y_axis_label="Depth [m]", sizing_mode="scale_width")
            p1.toolbar.logo = None
            ######################


            # # Add second axis to the right for the slope values
            # p1.extra_y_ranges = {"foo": Range1d(start=0, end=25)}
            # p1.add_layout(LinearAxis(y_range_name="foo", axis_label='Slope [degrees]'), 'right')

            # add multiple renderers
            l1 = p1.line('KP', 'LAT2021', legend_label="LAT 2021", line_color="blue", line_width=2, source=value, name='lat2021')
            # l1.nonselection_glyph = Line(line_color='gray',line_alpha=0.2)
            # l1.selection_glyph = Line(line_color='blue')
            l2 = p1.line('KP', 'LAT2025', legend_label="LAT 2028", line_color="red", line_width=2, source=value, name='lat2025')
            l3 = p1.line('KP', 'RSBL', legend_label="RSBL", line_color="green", line_width=2, source=value, name='rsbl')

            ## Test feature
            h1 = p1.line('KP', 'dHeight', legend_label="Dredge h", line_color="black", line_width=2, source=value, name='dHeight')
            toc1 = p1.line('KP', 'TOC', legend_label="Top of Cable", line_color="brown", line_width=2, source=value, name='toc')
            dol1 = p1.line('KP', 'DOL', legend_label="Depth of Lowering", line_color="orange", line_width=2, source=value, name='dol')
            esl1 = p1.line('KP', 'ESL', legend_label="Engineering seabed level", line_color="purple", line_width=2, source=value, name='esl')

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
            
            self.bathyFigs[key] = p1
            self.bathyTabsList.append(Panel(child=p1, title=key))
        self.bathyTabs = Tabs(tabs=self.bathyTabsList)
        
    def make_bathy_callbacks(self, depthResolution):
        
        # Create the callback JS texts using the agstools scripts
        codeBathy1 = selected_ind_Cb('dHeight', depthResolution) # Callback for calculating volumes only for selected part of routes
        codeBathy2 = depth_Cb('dHeight', depthResolution) # Callback for calculating volumes for updated depth variable
        codeBathy3 = width_Cb('dHeight', depthResolution) # Callback for calculating volumes for updated trench width variable
#         codeBathy4 = heightLine_Cb('LAT2025', 'RSBL', 'dHeight')
        codeBathy4new = heightLineWithDOL_Cb('LAT2025', 'TOC', 'dHeight', 'ESL')
        codeBathy5 = slope_Cb('dHeight', depthResolution) # Callback for calculating volumes for updated trench side slope variable
        explText = """Dredge corridor is a trapezium.
                                 Calculation does not take into account laterally uneven seabed profile."""
        ChangeTextScript = """
                o1.text=s.data['ym'][0];
            """
        
        self.volumeBoxes = {}
        self.bathyWidgetColumn=[]
        
        # Add spinner widgets with numerical values for dredge calculations. These are common for all routes.
        spinner1 = Spinner(title="Burial tool depth DOL[m]", low=-10, high=10, step=0.1, value=2.5, width=170)
        spinner2 = Spinner(title="Dredge corr. bottom width [m]", low=0, high=50, step=0.5, value=18, width=170)
        spinner3 = Spinner(title="Corridor walls slope 1/X [m]", low=0, high=10, step=0.5, value=4, width=170)
        self.bathyWidgetColumn+=[spinner1, spinner2, spinner3]
        
        for key, value in self.sourceBathyDict.items():
            self.volumeBoxes[key]=ColumnDataSource(data=dict(x=[0, 50], ym=['0', 0.], myText=["Dredge volume [m3]:", ""]))    
            
            volumeText = self.bathyFigs[key].text(x=10, y=-5, text='myText', source=self.volumeBoxes[key], name=f"mytextbox{key}")
#             self.bathyFigs.add_layout(volumeText)
            self.bathyFigs[key].add_tools(HoverTool(tooltips=explText, names=[f"mytextbox{key}"]))
            
            value.data['dHeight']-= spinner1.value
                        
            callback1 = CustomJS(args=dict(s=self.sourceBathyDict[key], s2=self.volumeBoxes[key], sp1=spinner1, sp2=spinner2, sp3=spinner3), code=codeBathy1)
            callback2 = CustomJS(args=dict(s=self.sourceBathyDict[key], s2=self.volumeBoxes[key], sp2=spinner2, sp3=spinner3), code=codeBathy2)
            callback3 = CustomJS(args=dict(s=self.sourceBathyDict[key], s2=self.volumeBoxes[key], sp1=spinner1, sp3=spinner3), code=codeBathy3)
            callback5 = CustomJS(args=dict(s=self.sourceBathyDict[key], s2=self.volumeBoxes[key], sp1=spinner1, sp2=spinner2), code=codeBathy5)
            callback4 = CustomJS(args=dict(s=self.sourceBathyDict[key]), code=codeBathy4new)
            
            # Define callbacks
            self.sourceBathyDict[key].selected.js_on_change('indices', callback1)            
            
            spinner1.js_on_change('value', callback4)
            spinner1.js_on_change('value', callback2)
            spinner2.js_on_change('value', callback3)
            spinner3.js_on_change('value', callback5)
            
            self.bathyWidgetColumn.append(Div(text=f'<b>{key} Dredge volume [m<sup>3</sup>]</b>', width=170, height_policy='fit'))
            self.bathyWidgetColumn.append(Div(text='', width=170, height=10, margin=(5,5,15,5)))
            
            # Index -1 for last entry in bathyWidgetColumn
            callbackDiv1=CustomJS(args=dict(o1=self.bathyWidgetColumn[-1], s=self.volumeBoxes[key]),code=ChangeTextScript) 
            self.sourceBathyDict[key].selected.js_on_change('indices', callbackDiv1)
            
            spinner1.js_on_change('value', callbackDiv1)
            spinner2.js_on_change('value', callbackDiv1)
            spinner3.js_on_change('value', callbackDiv1)
            
    @staticmethod
    def say_hi():
        print('hi')
