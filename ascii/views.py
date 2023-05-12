from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os 
import numpy as np
from django.core.files.storage import FileSystemStorage

import math
from bokeh import *
from bokeh.models import *
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.embed import file_html,components
from bokeh.resources import CDN
from bokeh.models import *
from bokeh.models import Model,Legend
from bokeh.layouts import gridplot
from bokeh.models.glyphs import Line as Line_glyph

from bokeh.palettes import Dark2_5 as palette
import itertools
import random


# Create your views here.

def ascii(request):
    resp = {} #VAriable use for passing arguments to html page
    #Checking method is post or not and other form fields are done or not.
    if request.method == "POST" and request.FILES['file'] != '' and request.FILES['file1'] !='':
        print("RIHEN")
        file1_dr = request.FILES['file1']
        c0 = request.POST['c0']
        c1 = request.POST['c1']
        c2 = request.POST['c2']
        # c00 = request.POST['c00']
        # c01 = request.POST['c01']
        # c02 = request.POST['c02']
        depth_level = request.POST['depth_level']
        user_su = request.POST['su']

        if user_su == '':
            user_su = float(10.0)
        
        if depth_level == '':
            depth_level = float(6.0)
        
        #Keep this value as default DR value also optional value may be entered by user
        if c0 == '':
            c0 = 205
        if c1 == '':
            c1 = 0.51
        if c2 == '':
            c2 = 2.93
        '''if c00 == '':
            c00 = 2.494
        if c01 == '':
            c01 = 0.46
        if c02 == '':
            c02 = 0.0296'''
        final1 = []
        final2 = []
        conef = []
        frictionf = []
        fric_ratiof = []
        bqf = []
        isbtf = []
        suf = []
        drf = []
        icf = []
        location=[]
        zonef=[]
        colorf=[]
        depthf=[]
        locf=[]
        #colors has a list of colors which can be used in plots 
        colors = itertools.cycle(palette)
        #print(len(colors))

        fss = FileSystemStorage('media')
        fs1 = fss.save(file1_dr.name,file1_dr)

        df1 = pd.read_excel('media/'+file1_dr.name,sheet_name="Dr_Calc",skiprows=8)
        #df1 = pd.read_excel(file1_dr,sheet_name="Dr_Calc",skiprows=8)
        os.remove('media/'+file1_dr.name)
        df1.drop(index=df1.index[0],axis=0,inplace=True)
        
        for file in request.FILES.getlist("file"):
            #print(file.name)
            #pass
            #file_ascii = request.FILES['file']
            file_ascii = file
            

            #print(file)
            
            fs = fss.save(file_ascii.name,file_ascii)
            
            #file_url = fss.url(fs)
            request.FILES['file']=''
            request.FILES['file1']=''
            #KPs = pd.read_excel('static/Norfolk Vanguard - Geotechnical Locations - 20210917.xlsx')
            df_test = pd.read_excel('media/'+file_ascii.name,sheet_name="Sheet1",nrows=28)
            
            #df_test = pd.ExcelFile('media/'+file_ascii.name)
            #print(df_test.sheet_names)
            loc = df_test['version'][26].split("_")
            #print(loc[0].strip(":"))
            location.append(loc[0].strip(":"))
            df = pd.read_excel('media/'+file_ascii.name,sheet_name="Sheet1",skiprows = 55)
            
            #sheet_name = pd.ExcelFile(KPs).sheet_names 
            # pdguishow(**tables)
            os.remove('media/'+file_ascii.name)
            #os.remove('media/'+file1_dr.name)

            
            #print("------",df.index,"-----------")
            columns = [x.lower() for x in list(df.columns)]
            df.drop(index=df.index[0], axis=0, inplace=True)# removed just one row which has string values
            

            #print(df)
            if 'Rec' in df.columns:
                df = df.drop('Rec' , axis='columns')
            df.dropna(axis=1, how='all',inplace=True) #removing columns which has only NaN values init
            df.dropna(axis=0, how='all',inplace=True) #removing rows which has only NaN values init
            #df.drop(index=df.index[len(df)-4:len(df)], axis=0, inplace=True)
            df = df.fillna(np.nan)
            columns = [x.lower() for x in list(df.columns)]
            #print(columns)
            columns.remove('isbt')
            #print(columns)

            depth_dr= list(df1["Depth"])
            qcmpa = [float(x) for x in df["Qnet-"] if isinstance(x, float)]
            k01 = [float(x) for x in df1["Unnamed: 5"] if isinstance(x, float)]
            depth = [float(x) for x in df["Depth"] if isinstance(x, float)]
            qnet = list(df["Qnet-"])
            friction = [float(x) for x in df["Friction"] if isinstance(x, float)]
            cone = list(df["Cone"])
            qt = list(df["qt"])
            fric_ratio = [float(x) for x in df["Fric_ratio"] if isinstance(x, float)]
            bq = list(df["Bq"])
            ic = list(df["Ic_S1"])
            sbt=[]

            #depth.sort()
            #print(depth)

            #fro calculation of ISBT
            qtpa = [float(round(float(x)/0.1,4)) for x in qcmpa if isinstance(x, float)] #equivalent to qc/pa

            #print(qtpa)
            #checking nad removing nan values
            while(math.isnan(float(depth[-1]))):
                depth.remove(depth[-1])
            
            #checking if depth is less then inserted depth level.
            while(float(depth[-1])<float(depth_level)):
                depth.append(float(round(depth[-1]+0.02,2)))
            
            #checking if depth is more then inserted depth level.
            while(float(depth[-1])>float(depth_level)):
                depth.remove(depth[-1])

            #checking if depth initial value is 0 or not.    
            if(depth[0]==0.0):
                depth.remove(depth[0])
            
            #print("Outer--",depth)
            
            
            #check length of all columns are aligning with depth length or not for plot 
            qtpa = checklength(qtpa,depth)
            qnet = checklength(qnet,depth)
            cone = checklength(cone,depth)
            friction = checklength(friction,depth)
            ic = checklength(ic,depth)
            bq = checklength(bq,depth)
            fric_ratio = checklength(fric_ratio,depth)
            qcmpa = checklength(qcmpa,depth)

            #multiplying friction with 40 to make it friction plot visible
            freq = [float(round(x*40,4)) for x in friction ]
            
            #print(len(qtpa),len(fric_ratio))
            #print(type(columns))
            #checking if file has Isbt column or not heere we have already endsured that if ISBT column has null value we already removed if not it has value.
            if 'isbt' in columns:
                sbt = list(df["Isbt"])
            else:
                #here we need to add code for sbt calculation
                
                '''
                /*
                * formula[(3.47-log(qcpa))^2 + log(fric_ratio+1.22)^2]^0.5
                * qc = cone resistance or corrected cone resistance
                * friction ratio = (fs/qc)*100%
                * fs sleeve friction
                * As of now values are slight different. Need to check other parameters as well for proper understanding
                */
                '''
                for i in range(0,len(qtpa)):
                    #print(i,fric_ratio[i],(math.log(abs(fric_ratio[i]))+1.22))
                    lft = round(pow((3.47 - round(math.log(qtpa[i],10),6)),2),6)
                    rgt = round(pow((round(math.log(abs(float(fric_ratio[i])),10),10)+1.22),2),6)
                    #print(i,depth[i],isbt[i],"log qc",round(math.log(qtpa[i],10),6),"log fr ratio",round(math.log(abs(float(fric_ratio[i])),10),10),"lft--",lft,"rgt--",rgt,"final--",round(pow((lft + rgt),0.5),2))
                    formula_sbt = round(pow((lft + rgt),0.5),2)
                    sbt.append(formula_sbt)
                    
            #print(sbt)
            sbt = checklength(sbt,depth)

            #Creating sbtdir and keep su and dr values 
            #su = 1 2 3 4 9
            #dr = 5 6 7 8
            sbtdir = {"depth":[],"sbt":[],"zone":[],"su":[],"dr":[],"color":[],"location" : []}
            for i in range(0,len(sbt)):
                if sbt[i] < 1.31 and sbt[i] > 0.00:
                    sbtdir["depth"].append(depth[i])
                    sbtdir["sbt"].append(sbt[i])
                    sbtdir["zone"].append(7)
                    sbtdir["su"].append(np.nan)
                    sbtdir["dr"].append(calculateDR(qcmpa[i],c0,k01[i],c1,c2))
                    sbtdir["color"].append(next(colors))
                    sbtdir["location"].append(loc[0].strip(":"))
                    
                elif sbt[i] > 1.31 and sbt[i] < 2.05:
                    sbtdir["depth"].append(depth[i])
                    sbtdir["sbt"].append(sbt[i])
                    sbtdir["zone"].append(6)
                    sbtdir["su"].append(np.nan)
                    sbtdir["dr"].append(calculateDR(qcmpa[i],c0,k01[i],c1,c2))
                    sbtdir["color"].append(next(colors))
                    sbtdir["location"].append(loc[0].strip(":"))

                elif sbt[i] > 2.05 and sbt[i] < 2.60:
                    sbtdir["depth"].append(depth[i])
                    sbtdir["sbt"].append(sbt[i])
                    sbtdir["zone"].append(5)
                    sbtdir["su"].append(np.nan)
                    sbtdir["dr"].append(calculateDR(qcmpa[i],c0,k01[i],c1,c2))
                    sbtdir["color"].append(next(colors))
                    sbtdir["location"].append(loc[0].strip(":"))

                elif sbt[i] > 2.60 and sbt[i] < 2.95:
                    sbtdir["depth"].append(depth[i])
                    sbtdir["sbt"].append(sbt[i])
                    sbtdir["zone"].append(4)
                    sbtdir["su"].append(calculateSU(qnet[i],user_su))
                    sbtdir["dr"].append(np.nan)
                    sbtdir["color"].append(next(colors))
                    sbtdir["location"].append(loc[0].strip(":"))

                elif sbt[i] > 2.95 and sbt[i] < 3.60:
                    sbtdir["depth"].append(depth[i])
                    sbtdir["sbt"].append(sbt[i])
                    sbtdir["zone"].append(3)
                    sbtdir["su"].append(calculateSU(qnet[i],user_su))
                    sbtdir["dr"].append(np.nan)
                    sbtdir["color"].append(next(colors))
                    sbtdir["location"].append(loc[0].strip(":"))

                elif math.isnan(sbt[i]):
                    sbtdir["depth"].append(depth[i])
                    sbtdir["sbt"].append(sbt[i])
                    sbtdir["zone"].append(np.nan)
                    sbtdir["su"].append(np.nan)
                    sbtdir["dr"].append(np.nan)
                    sbtdir["color"].append(next(colors))
                    sbtdir["location"].append(loc[0].strip(":"))

                else:
                    sbtdir["depth"].append(depth[i])
                    sbtdir["sbt"].append(sbt[i])
                    sbtdir["zone"].append(2)
                    sbtdir["su"].append(calculateSU(qnet[i],user_su))
                    sbtdir["dr"].append(np.nan)
                    sbtdir["color"].append(next(colors))
                    sbtdir["location"].append(loc[0].strip(":"))
            
            #print(sbtdir["location"])
            #print(dr)
            #Creating list of list of different file column in one for plotting in respected graph
            conef.append(cone)
            frictionf.append(freq)
            fric_ratiof.append(fric_ratio)
            bqf.append(bq)
            icf.append(ic)
            isbtf.append(sbt)
            suf.append(sbtdir["su"])
            drf.append(sbtdir["dr"])
            zonef.append(sbtdir["zone"])
            colorf.append(sbtdir["color"])
            depthf.append(sbtdir["depth"])
            locf.append(sbtdir["location"])

        renderer_list=[] #creating render list for keeping all line graph in hidden plot
        #color_list=[] #creating color list for keeping all line graph in hidden plot
        item_list=[] #creating item list for keeping all line graph in hidden plot
        item_dict={} #creating item dictionary for keeping all line graph in hidden plot
       
        for iloc in range(0,len(location)):
            item_dict[location[iloc]]=[]

        #print("RIHEN___",sp_dict)

        #print(len(sp_dict["legend"]),len(sp_dict["color"]),len(depth))
        
        p,rendrer,color = getExtraAxisGraphs(conef,frictionf,Range1d(-10,100),Range1d(-0.2,2.5),(7,0),depth,"cone","Friction",'#d7191c','orange',"Friction ","cone ","Friction and Cone v/s Depth",1,colors,location,showy=True,simg=False)

        '''for c in color:
            color_list.append(c) '''
        
        item_list.append(rendrer)
        #print(renderer_list)
        #print(type(rendrer))
        
        
        p1,rendrer,color = getExtraAxisGraphs(fric_ratiof,bqf,Range1d(-1,8),Range1d(-0.5,1),p.y_range,depth,"Fric Ratio","BQ",'black','green',"Fric_ratio ","BQ ","fs,qc v/s Depth",1,colors,location,showy=False,simg=False)
        
        '''for c in color:
            color_list.append(c)'''

        item_list.append(rendrer)
        
        p2,rendrer,color = getExtraAxisGraphs(icf,isbtf,Range1d(0.5,9),Range1d(0.5,9),p.y_range,depth,"IC","ISBT",'black','green',"IC ","ISBT ","IC,ISBT v/s Depth",0,colors,location,showy=False,simg=False)
        item_list.append(rendrer)
        
        p3,rendrer,color = getNormalGraph(suf,depth,Range1d(start = 0,end= 10),p.y_range,"SU v/s Depth","SU","SU ",colors,location)
        
        '''for c in color:
            color_list.append(c)''' 
        item_list.append(rendrer)


        p4,rendrer,color = getNormalGraph(drf,depth,Range1d(start = 0,end= 120),p.y_range,"Dr v/s Depth","Dr","Dr ",colors,location)
        
        '''for c in color:
            color_list.append(c)'''
        item_list.append(rendrer)
        #print(item_list)

        sp,rendrer,color = getSoilGraph(isbtf,depth,Range1d(start = 1,end= 4),p.y_range,"Soil Profile","SBT Index","SBT Index ",colors,location)
        item_list.append(rendrer)

        dum_fig = figure(plot_width=80,plot_height=600,outline_line_alpha=0,toolbar_location=None)

        # set the components of the figure invisible
        for fig_component in [dum_fig.grid[0],dum_fig.ygrid[0],dum_fig.xaxis[0],dum_fig.yaxis[0]]:
            fig_component.visible = False
        # Lines with the same color will share a same legend item
        #legend_items = [LegendItem(label=color,renderers=[renderer for renderer in renderer_list if renderer.glyph.line_color==color]) for color in color_list]

        #legend_items = [LegendItem(label=loc,renderers=[item_list[item][1] for item in range(0,len(item_list)) if item_list[item][0]==loc]) for loc in location]
        for item in range(0,len(item_list)):
            for it in range(0,len(item_list[item])):
                for r in item_list[item][it][1]:
                    renderer_list.append(r)
                    item_dict[item_list[item][it][0]].append(r)
        
        
        legend_items=[]
        for keys, value in item_dict.items():
            legend_items.append((keys,value))

        dum_fig.renderers += renderer_list
        # set the figure range outside of the range of all glyphs
        dum_fig.x_range.end = 130
        dum_fig.x_range.start = 140
        # add the legend
        dum_fig.add_layout( Legend(click_policy='hide',location='top',border_line_alpha=0,items=legend_items) )
        
        final1.append(Row(p,p1,p3,p4,sp))
        fig_grid = gridplot(final1,ncols=1,toolbar_location='right')
        
        final = gridplot([[fig_grid,dum_fig]],toolbar_location=None)

        #curdoc().clear()
        img3 = final
        for model in img3.select({'type': Model}):
            prev_doc = model.document
            model._document = None
            if prev_doc:
                prev_doc.remove_root(model)
        curdoc().add_root(img3)
        
        resp = {
            'final' : file_html(img3, CDN, "my plot"),
            'sbtdir' : zip(sbtdir["depth"],sbtdir["sbt"],sbtdir["zone"],sbtdir["location"])
        }

    return render(request,"index-ascii.html",resp)



    #return render(request,"index-ascii.html")
    #return HttpResponse("TEST")


def calculateSU(qnet,user_su):
    if float(qnet)>0.00:
        return float(round(qnet/float(user_su),4))
    else:
        return np.nan

def calculateDR(qcmpa,c0,k01,c1,c2):
    mul1 = float(qcmpa)*1000
    mul = float(c0*pow(k01,c1))
    lg = mul1/mul
    #print(qc,"-------------",lg,mul1,mul)
    formula = float(round(((1/c2)*math.log(lg))*100,4))
    return formula

# Check length of all fields are equal or not
#if not append with np.nan or remove last elements.
#Here we are checking with Depth as for graph our one of axis is Depth.
#function signature:
#list1: list whose length to check
#list2 : list against which length is need to check.
#returning list after both list are of same length.
def checklength(list1,list2):
    if(len(list1)<len(list2)):
        while(len(list1) != len(list2)):
            list1.append(np.nan)
    elif(len(list1)>len(list2)):
        while(len(list1) != len(list2)):
            list1.remove(list1[-1])
    
    return list1


def getExtraAxisGraphs(x_axis_list_1,x_axis_list_2,x1_range,x2_range,y_range,y_axis_list,x1_label,x2_label,color1,color2,x1legend,x2legend,title,xtra,colors,location,showy,simg):
    #y_range = Range1d(7,0)
    p = figure(width=1000, height=1000,x_axis_label = x1_label, y_axis_label = "Depth",sizing_mode ="stretch_both",output_backend="webgl",x_axis_location="above",x_range = x1_range,y_range=y_range)
    items=[]
    
    tst,tst2,color1,color2='','','',''
    color=[]
    for i in range(0,len(x_axis_list_1)):
        color1= next(colors)
        color2 = next(colors)
        tst=p.line(x_axis_list_1[i], y_axis_list, line_width=1, color=color1, alpha=0.8)
        tst2=p.line(x_axis_list_2[i], y_axis_list, line_width=1, color=color2, alpha=0.8,line_dash="dashed")
        if i > 0:
            tst.visible = False
            tst2.visible = False
        p.add_tools(HoverTool(tooltips=location[i]+"  @y,  @x", renderers=[tst,tst2], mode="mouse"))
        items.append((location[i],[tst,tst2]))
    #print("RIHEN",items[0][0])
    color.append(color1)
    color.append(color2)
    #legend1= Legend(items=items, orientation="vertical")
    #p.add_layout(legend1, 'below')
    if(xtra == 1):
    # exta x axis
        p.extra_x_ranges.update({'x_above':  x2_range})
        p.add_layout(LinearAxis(x_range_name='x_above',axis_label=x2_label), 'above')
    if not showy:
        p.yaxis.visible = False
    
    if simg:
        p.image_url(url=[r'/static/Images/tree.png'],
                x=0, y=0,w=1000,h=1000, w_units='screen',h_units='screen', anchor="center",global_alpha=0.2)
    
    

    return p,items,color,

def getNormalGraph(list1,list2,x_range,y_range,title,x_label,x_legend,colors,location):
    p4 = figure(width=800, height=900,x_axis_label = x_label, sizing_mode ="stretch_both",output_backend="webgl",tooltips="X = @x Y = @y",x_axis_location="above", y_range=y_range,x_range =x_range)
    items=[]
    tst,color1 = '',''
    color=[]
    for i in range(0,len(list1)):
        color1=next(colors)
        tst=p4.line(list1[i], list2, line_width=1, color=color1, alpha=0.8)
        if i > 0:
            tst.visible = False
        p4.add_tools(HoverTool(tooltips=location[i]+"  @y,  @x", renderers=[tst], mode="mouse"))
        items.append((location[i],[tst]))
    color.append(color1)
    #legend1 = Legend(items=items, orientation="vertical")
    #p4.add_layout(legend1, 'below')
    p4.yaxis.visible = False

    return p4,items,color

def getSoilGraph(list1,list2,x_range,y_range,title,x_label,x_legend,colors,location):
    #print(zonef)
    #c1set=["#dd2119","#b5693f","#667bb3","#455382","#449484","#fff801","#f8a04e","#959595","#dedede"]
    c1set=["#FF9600","#C8A046","#B4DCD2","#509696","#645AC8","#C86400"]
    c1col = ["1","2","3","4","5","6","7","8","9"]
    #print(depth)
    p = figure(width=800, height=900,x_axis_label = x_label, sizing_mode ="stretch_both",output_backend="webgl",x_axis_location="above", y_range=y_range,x_range =x_range)
    # p = figure(width=800, height=500,x_axis_label = x_label, sizing_mode ="stretch_both",output_backend="webgl",title=title,tooltips="X = @x Y = @y",x_axis_location="above", y_range=y_range,x_range ='cpt 1')
    # temp_df = {}
    # zone = [str(x) for x in range(1,10)]
    # for z in zone:
    #     temp_df[z] = []

    # temp_df['depth'] = []
    # temp_df['location'] = []

    # for z in range(0,len(list1[0])):
    #     print(str(list1[0][z]))
    #     if(math.isnan(list1[0][z])):
    #         None
    #     else:
    #         temp_df[str(list1[0][z])].append(list2[z])
    #         temp_df["depth"].append(list2[z])
    #         temp_df['location'].append('CPT 1')

    # for i in zone:
    #     while(len(temp_df[i]) != len(temp_df['depth'])):
    #             temp_df[i].append(0)
    #     #print(i,len(temp_df[i]),len(temp_df["depth"]),len(temp_df["location"]))
    
    # #print(temp_df)

    # p.vbar_stack(zone, x='location', width=0.1, source=temp_df,color=c1set,legend_label=c1col)
    # p.outline_line_color = None
    # p.legend.title = 'CPT 1'
    # p.legend.click_policy="hide"
    # p.yaxis.visible = False

    df = ColumnDataSource(data =dict(
        x=[0.655,1.68,2.325,2.775,3.275,4.3],
        y = [8,8,8,8,8,8],
        width = [1.31,0.74,0.55,0.35,0.65,1.4],
        color = c1set,
        legend_label  = ['gravelly Sand to Sand','Sand to Sailty Sand','Sailty Sand to Sandy SILT','clayey SILT to Silty CLAY','silty Clay to Clay','Organic Soil'],
    ))
    p.add_layout(Legend(),'below')
    p.vbar(x='x',top = 'y',width='width',color='color',source=df,alpha=0.8,legend_field ='legend_label')
    items=[]
    tst,color1 = '',''
    color=[]
    for i in range(0,len(location)):
        # for z in range(0,len(list1[0])):
        #     if(math.isnan(list1[0][z])):
        #         col = None
        #     else:
        #         col = c1set[list1[0][z]]
        tst = p.line(list1[i], list2, line_width=1, color= "#000000", alpha=1)
        if i > 0:
            tst.visible = False
        p.add_tools(HoverTool(tooltips=location[i]+"\n Depth =  @y,"+"\n Zone = @x", renderers=[tst], mode="mouse"))
        items.append((location[i],[tst]))
    color.append('#000000')
    # p.legend.title = 'CPT 1'
    # p.legend.click_policy="hide"
    p.yaxis.visible = False
    return p,items,color
    