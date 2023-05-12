def dataTwo():
    if request.method == 'POST':
        
        #take user input  
        file1 = request.files['upload-file1']
        file2 = request.files['upload-file2']
        
        #save uploaded file
        file1.save( 'static/upload/' + secure_filename(file1.filename))
        file2.save( 'static/upload/' + secure_filename(file2.filename))
        
        # creating or loading an excel workbook for file1, file2
        newWorkbook = openpyxl.load_workbook(file1)
        newWorkbook2 = openpyxl.load_workbook(file2)
        
        #defining sheetnames variable for sheetnames in file1,file2
        sheetNames=newWorkbook.sheetnames
        sheetNames2 = newWorkbook2.sheetnames
        
        #Hover mouse information
        TOOLTIPS = [("KP[km]", '@{KP [km]}'),
                    ("DOL[m]", '@{DOL [m]}'), 
                    ("DOC[m]", '@{DOC [m]}'),
                    ]
        #plot figure for circle
        p = figure(plot_width = 2000, plot_height = 800, tooltips = TOOLTIPS, match_aspect=True, toolbar_location="above" )
        
        #plot figure for Line
        p2 = figure(plot_width = 2000, plot_height = 800, tooltips = TOOLTIPS, match_aspect=True, toolbar_location="above")
        
        
        
        #read file1,file2 sheet_name = Listing
        file1_data_listing = pd.read_excel('static/upload/' + file1.filename, sheet_name='Listing')
        file2_data_listing = pd.read_excel('static/upload/' + file2.filename, sheet_name='Listing')
        
        
        #get df for file 1, 2 sheet_name = listing
        file1_Listing_df =  pd.DataFrame(file1_data_listing)
        file2_Listing_df =  pd.DataFrame(file2_data_listing)
        
        #remove extra space from column name in file 1,2 sheet_name = listing
        file1_Listing_df.columns = [x.replace("\n", " ") for x in file1_Listing_df.columns.to_list()]
        file2_Listing_df.columns = [x.replace("\n", " ") for x in file2_Listing_df.columns.to_list()]
        
        #define source for bokeh plot for file1, 2 sheet_name = listing
        file1_SOURCE1 = ColumnDataSource(data=file1_Listing_df)
        file2_SOURCE1 = ColumnDataSource(data=file2_Listing_df)
        
        #plot all values to bokeh (both circle and line tabs) from files 1, 2 sheet_name = listing
        
        #DOL Requirement and colorpickers
        file1_DOLReq_circletab = p.line(x = "KP [km]" , y = "Unnamed: 18", source = file1_SOURCE1,  color = 'black', width = 1, legend_label = file1.filename + " DOL Req.", line_dash = 'dashed')
        file1_DOLReq_linetab = p2.line(x = "KP [km]" , y = "Unnamed: 18", source = file1_SOURCE1,  color = 'black', width = 1, legend_label = file1.filename + " DOL Req.", line_dash = 'dashed')
        
        file1_DOLRReq_circletab_colorpicker = ColorPicker(title= 'file1 DOL Req. Circle')
        file1_DOLRReq_circletab_colorpicker.js_link('color', file1_DOLReq_circletab.glyph, 'line_color')
        file1_DOLRReq_circletab_colorpicker.color = 'black'
        
        file1_DOLReq_linetab_colorpicker = ColorPicker(title= 'file1  DOC Req. Line')
        file1_DOLReq_linetab_colorpicker.js_link('color', file1_DOLReq_linetab.glyph, 'line_color')
        file1_DOLReq_linetab_colorpicker.color = 'black'
        
        #file 2
        file2_DOLReq_circletab = p.line(x = "KP [km]" , y = "Unnamed: 18", source = file2_SOURCE1,  color = 'black', width = 1, legend_label = file2.filename + " DOL Req.", line_dash = 'dashed')
        file2_DOLReq_linetab = p2.line(x = "KP [km]" , y = "Unnamed: 18", source = file2_SOURCE1,  color = 'black', width = 1, legend_label = file2.filename + " DOL Req.", line_dash = 'dashed')
        
        file2_DOLRReq_circletab_colorpicker = ColorPicker(title= 'File2  DOL Req. ')
        file2_DOLRReq_circletab_colorpicker.js_link('color', file2_DOLReq_circletab.glyph, 'line_color')
        file2_DOLRReq_circletab_colorpicker.color = 'black'
        
        file2_DOLReq_linetab_colorpicker = ColorPicker(title= 'file2 DOC Req. Line')
        file2_DOLReq_linetab_colorpicker.js_link('color', file2_DOLReq_linetab.glyph, 'line_color')
        file2_DOLReq_linetab_colorpicker.color = 'black'
        
        #DOL and colorpicker
        file1_DOL_circletab = p.circle(x = "KP [km]", y = "DOL [m]", source = file1_SOURCE1,  color = '#00429d', size = 5, legend_label = file1.filename + " DOL [m]")
        file1_DOL_linetab = p2.line(x = "KP [km]", y = "DOL [m]", source = file1_SOURCE1,  color = '#00429d', width = 1, legend_label = file1.filename + " DOL [m]")
        
        file1_DOL_circletab_colorpicker = ColorPicker(title = 'File 1 DOL  ')
        file1_DOL_circletab_colorpicker.js_link('color', file1_DOL_circletab.glyph, 'line_color')
        file1_DOL_circletab_colorpicker.color = '#00429d'
        
        file1_DOL_linetab_colorpicker = ColorPicker(title = 'File 1 DOL  ')
        file1_DOL_linetab_colorpicker.js_link('color', file1_DOL_linetab.glyph, 'line_color')
        file1_DOL_linetab_colorpicker.color = '#00429d'
        
        #file2
        #DOL and colorpicker
        file2_DOL_circletab = p.circle(x = "KP [km]", y = "DOL [m]", source = file2_SOURCE1,  color = '#00429d', size = 5, legend_label = file2.filename + " DOL [m]")
        file2_DOL_linetab = p2.line(x = "KP [km]", y = "DOL [m]", source = file2_SOURCE1,  color = '#00429d', width = 1, legend_label = file2.filename + " DOL [m]")
        
        file2_DOL_circletab_colorpicker = ColorPicker(title = 'File 2 DOL  ')
        file2_DOL_circletab_colorpicker.js_link('color', file2_DOL_circletab.glyph, 'line_color')
        file2_DOL_circletab_colorpicker.color = '#00429d'
        
        file2_DOL_linetab_colorpicker = ColorPicker(title = 'File 2 DOL  ')
        file2_DOL_linetab_colorpicker.js_link('color', file2_DOL_linetab.glyph, 'line_color')
        file2_DOL_linetab_colorpicker.color = '#00429d'
        
        
        #DOC and colorpickers
        file1_DOC_circletab = p.circle(x = "KP [km]" , y = "DOC [m]", source = file1_SOURCE1,  color = '#abd400', size = 5, legend_label= file1.filename + " DOC [m]")
        file1_DOC_linetab=p2.line(x = "KP [km]" , y = "DOC [m]", source = file1_SOURCE1,  color = '#abd400', width=1, legend_label= file1.filename + " DOC [m]")
       
       
        file1_DOC_circletab_colorpicker = ColorPicker(title = 'File 1 DOC  ')
        file1_DOC_circletab_colorpicker.js_link('color', file1_DOC_circletab.glyph, 'line_color')
        file1_DOC_circletab_colorpicker.color = '#abd400'
        
        file1_DOC_linetab_colorpicker = ColorPicker(title = 'file1 DOC Line ')
        file1_DOC_linetab_colorpicker.js_link('color', file1_DOC_linetab.glyph, 'line_color')
        file1_DOC_linetab_colorpicker.color = '#abd400'
        
        #file2
        #DOC and colorpickers
        file2_DOC_circletab = p.circle(x = "KP [km]" , y = "DOC [m]", source = file2_SOURCE1,  color = '#abd400', size = 5, legend_label= file2.filename + " DOC [m]")
        file2_DOC_linetab=p2.line(x = "KP [km]" , y = "DOC [m]", source = file2_SOURCE1,  color = '#abd400', width=1, legend_label= file2.filename + " DOC [m]")
       
       
        file2_DOC_circletab_colorpicker = ColorPicker(title = 'File 2 DOC  ')
        file2_DOC_circletab_colorpicker.js_link('color', file2_DOC_circletab.glyph, 'line_color')
        file2_DOC_circletab_colorpicker.color = '#abd400'
        
        file2_DOC_linetab_colorpicker = ColorPicker(title = 'file2 DOC Line ')
        file2_DOC_linetab_colorpicker.js_link('color', file2_DOC_linetab.glyph, 'line_color')
        file2_DOC_linetab_colorpicker.color = '#abd400'
        
        
        #checking for 'T1500' sheet in workbook and plotting bokeh points 
        if 'T1500' in sheetNames:
          #read file1 sheet_name = 'T1500'
          file1_data_T1500 = pd.read_excel('static/upload/' + file1.filename, sheet_name='T1500') 
          
          #get df for file1 sheet_name = 'T1500'
          file1_T1500_df =  pd.DataFrame(file1_data_T1500)
          
          #remove extra space from column name in file 1 sheet_name = T1500
          file1_T1500_df.columns = [x.replace("\n", " ") for x in file1_T1500_df.columns.to_list()]
        
          #define source for bokeh plot for file1 sheet_name = T1500
          file1_SOURCE1_T1500 = ColumnDataSource(data=file1_T1500_df)
        
          #plot all values to bokeh (both circle and line tabs) from file1 sheet_name = T1500
        
          #Average Sword Depth for sheetname  = T1500 and colorpickers
          file1_ASD_T1500_circletab = p.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file1_SOURCE1_T1500 ,  color = '#2ca08b', width = 1, legend_label= file1.filename +" T1500  Average Sword Depth", line_dash = 'dashed')
          file1_ASD_T1500_linetab = p2.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file1_SOURCE1_T1500 ,  color = '#2ca08b', width = 1, legend_label= file1.filename +" T1500  Average Sword Depth", line_dash = 'dashed')
          
       
          file1_ASD_T1500_circletab_colorpicker = ColorPicker(title= 'File 1 Average Sword Depth pass 1   ')
          file1_ASD_T1500_circletab_colorpicker.js_link('color', file1_ASD_T1500_circletab.glyph, 'line_color')
          file1_ASD_T1500_circletab_colorpicker.color = '#2ca08b'
        
          file1_ASD_T1500_linetab_colorpicker = ColorPicker(title= 'File 1 Average Sword Depth pass 1 Line ')
          file1_ASD_T1500_linetab_colorpicker.js_link('color', file1_ASD_T1500_linetab.glyph, 'line_color')
          file1_ASD_T1500_linetab_colorpicker.color = '#2ca08b'

          
        
        else:
          pass
        
        #file2
        #checking for 'T1500' sheet in workbook and plotting bokeh points 
        if 'T1500' in sheetNames2:
          #read file2 sheet_name = 'T1500'
          file2_data_T1500 = pd.read_excel('static/upload/' + file2.filename, sheet_name='T1500') 
          
          #get df for file1 sheet_name = 'T1500'
          file2_T1500_df =  pd.DataFrame(file2_data_T1500)
          
          #remove extra space from column name in file 1 sheet_name = T1500
          file2_T1500_df.columns = [x.replace("\n", " ") for x in file2_T1500_df.columns.to_list()]
        
          #define source for bokeh plot for file1 sheet_name = T1500
          file2_SOURCE1_T1500 = ColumnDataSource(data=file2_T1500_df)
        
          #plot all values to bokeh (both circle and line tabs) from file2 sheet_name = T1500
        
          #Average Sword Depth for sheetname  = T1500 and colorpickers
          file2_ASD_T1500_circletab = p.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file2_SOURCE1_T1500 ,  color = '#2ca08b', width = 1, legend_label= file2.filename +" T1500  Average Sword Depth", line_dash = 'dashed')
          file2_ASD_T1500_linetab = p2.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file2_SOURCE1_T1500 ,  color = '#2ca08b', width = 1, legend_label= file2.filename +" T1500  Average Sword Depth", line_dash = 'dashed')
          
       
          file2_ASD_T1500_circletab_colorpicker = ColorPicker(title= 'File 2 Average Sword Depth pass 1  ')
          file2_ASD_T1500_circletab_colorpicker.js_link('color', file2_ASD_T1500_circletab.glyph, 'line_color')
          file2_ASD_T1500_circletab_colorpicker.color = '#2ca08b'
        
          file2_ASD_T1500_linetab_colorpicker = ColorPicker(title= 'File 2 Average Sword Depth pass 1  ')
          file2_ASD_T1500_linetab_colorpicker.js_link('color', file2_ASD_T1500_linetab.glyph, 'line_color')
          file2_ASD_T1500_linetab_colorpicker.color = '#2ca08b'

          
        
        else:
          pass
        
        #checking for 'T1500 2nd Pass' sheet in workbook and plotting bokeh points 
        if 'T1500 2nd Pass' in sheetNames:
          #read file1 sheet_name = 'T1500 2nd Pass'
          file1_data_T1500_2nd_Pass = pd.read_excel('static/upload/' + file1.filename, sheet_name='T1500 2nd Pass') 
          #get df for file1 sheet_name = 'T1500 2nd Pass'
          file1_T1500_2nd_Pass_df =  pd.DataFrame(file1_data_T1500_2nd_Pass)
          #remove extra space from column name in file 1 sheet_name = T1500
          file1_T1500_2nd_Pass_df.columns = [x.replace("\n", " ") for x in file1_T1500_2nd_Pass_df.columns.to_list()]
        
          #define source for bokeh plot for file1 sheet_name = T1500
          file1_SOURCE1_T1500_2nd_Pass = ColumnDataSource(data=file1_T1500_2nd_Pass_df)
        
          #plot all values to bokeh (both circle and line tabs) from file1 sheet_name = T1500 2nd Pass
        
          #Average Sword Depth and colorpickers
          file1_ASD_T1500_2nd_Pass_circletab = p.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file1_SOURCE1_T1500_2nd_Pass ,  color = '#2ca08b', width = 1, legend_label= file1.filename +" T1500 2nd Pass Average Sword Depth", line_dash = 'dashed')
          file1_ASD_T1500_2nd_Pass_linetab = p2.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file1_SOURCE1_T1500_2nd_Pass ,  color = '#2ca08b', width = 1, legend_label= file1.filename +" T1500 2nd Pass Average Sword Depth", line_dash = 'dashed')
          
       
          file1_ASD_T1500_2nd_Pass_circletab_colorpicker = ColorPicker(title= 'File 1 Average Sword Depth pass 2 ')
          file1_ASD_T1500_2nd_Pass_circletab_colorpicker.js_link('color', file1_ASD_T1500_2nd_Pass_circletab.glyph, 'line_color')
          file1_ASD_T1500_2nd_Pass_circletab_colorpicker.color = '#2ca08b'
        
          file1_ASD_T1500_2nd_Pass_linetab_colorpicker = ColorPicker(title= 'File 1 Average Sword Depth pass 2 ')
          file1_ASD_T1500_2nd_Pass_linetab_colorpicker.js_link('color', file1_ASD_T1500_2nd_Pass_linetab.glyph, 'line_color')
          file1_ASD_T1500_2nd_Pass_linetab_colorpicker.color = '#2ca08b'
          
         
        
        else:
          pass
        
        #file2
        #checking for 'T1500 2nd Pass' sheet in workbook and plotting bokeh points 
        if 'T1500 2nd Pass' in sheetNames2:
          #read file2 sheet_name = 'T1500 2nd Pass'
          file2_data_T1500_2nd_Pass = pd.read_excel('static/upload/' + file2.filename, sheet_name='T1500 2nd Pass') 
          #get df for file2 sheet_name = 'T1500 2nd Pass'
          file2_T1500_2nd_Pass_df =  pd.DataFrame(file2_data_T1500_2nd_Pass)
          #remove extra space from column name in file 2 sheet_name = T1500
          file2_T1500_2nd_Pass_df.columns = [x.replace("\n", " ") for x in file2_T1500_2nd_Pass_df.columns.to_list()]
        
          #define source for bokeh plot for file2 sheet_name = T1500 2nd Pass
          file2_SOURCE1_T1500_2nd_Pass = ColumnDataSource(data = file2_T1500_2nd_Pass_df)
        
          #plot all values to bokeh (both circle and line tabs) from file2 sheet_name = T1500 2nd Pass
        
          #Average Sword Depth and colorpickers
          file2_ASD_T1500_2nd_Pass_circletab = p.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file2_SOURCE1_T1500_2nd_Pass ,  color = '#2ca08b', width = 1, legend_label= file2.filename +" T1500 2nd Pass Average Sword Depth", line_dash = 'dashed')
          file2_ASD_T1500_2nd_Pass_linetab = p2.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file2_SOURCE1_T1500_2nd_Pass ,  color = '#2ca08b', width = 1, legend_label= file2.filename +" T1500 2nd Pass Average Sword Depth", line_dash = 'dashed')
          
       
          file2_ASD_T1500_2nd_Pass_circletab_colorpicker = ColorPicker(title= 'File 2 Average Sword Depth pass 2 Tab')
          file2_ASD_T1500_2nd_Pass_circletab_colorpicker.js_link('color', file2_ASD_T1500_2nd_Pass_circletab.glyph, 'line_color')
          file2_ASD_T1500_2nd_Pass_circletab_colorpicker.color = '#2ca08b'
        
          file2_ASD_T1500_2nd_Pass_linetab_colorpicker = ColorPicker(title= 'File 2 Average Sword Depth pass 2 ')
          file2_ASD_T1500_2nd_Pass_linetab_colorpicker.js_link('color', file2_ASD_T1500_2nd_Pass_linetab.glyph, 'line_color')
          file2_ASD_T1500_2nd_Pass_linetab_colorpicker.color = '#2ca08b'
          
         
        
        else:
          pass
        
        #checking for 'T1500 3rd Pass' sheet in workbook and plotting bokeh points 
        if 'T1500 3rd Pass' in sheetNames:
          #read file1 sheet_name = 'T1500 3rd Pass'
          file1_data_T1500_3rd_Pass = pd.read_excel('static/upload/' + file1.filename, sheet_name='T1500 3rd Pass') 
          #get df for file1 sheet_name = 'T1500 2nd Pass'
          file1_T1500_3rd_Pass_df =  pd.DataFrame(file1_data_T1500_3rd_Pass)
          #remove extra space from column name in file 1 sheet_name = T1500
          file1_T1500_3rd_Pass_df.columns = [x.replace("\n", " ") for x in file1_T1500_3rd_Pass_df.columns.to_list()]
        
          #define source for bokeh plot for file1 sheet_name = T1500
          file1_SOURCE1_T1500_3rd_Pass = ColumnDataSource(data=file1_T1500_3rd_Pass_df)
        
          #plot all values to bokeh (both circle and line tabs) from file1 sheet_name = T1500 3rd Pass
        
          #Average Sword Depth and colorpickers
          file1_ASD_T1500_3rd_Pass_circletab = p.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file1_SOURCE1_T1500_3rd_Pass ,  color = '#2ca08b', width = 1, legend_label= file1.filename +" T1500 3rd Pass Average Sword Depth", line_dash = 'dashed')
          file1_ASD_T1500_3rd_Pass_linetab = p2.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file1_SOURCE1_T1500_3rd_Pass ,  color = '#2ca08b', width = 1, legend_label= file1.filename +" T1500 3rd Pass Average Sword Depth", line_dash = 'dashed')
          
       
          file1_ASD_T1500_3rd_Pass_circletab_colorpicker = ColorPicker(title= 'File 1 Average Sword Depth pass 3 ')
          file1_ASD_T1500_3rd_Pass_circletab_colorpicker.js_link('color', file1_ASD_T1500_3rd_Pass_circletab.glyph, 'line_color')
          file1_ASD_T1500_3rd_Pass_circletab_colorpicker.color = '#2ca08b'
        
          file1_ASD_T1500_3rd_Pass_linetab_colorpicker = ColorPicker(title= 'File 1 Average Sword Depth pass 3 ')
          file1_ASD_T1500_3rd_Pass_linetab_colorpicker.js_link('color', file1_ASD_T1500_3rd_Pass_linetab.glyph, 'line_color')
          file1_ASD_T1500_3rd_Pass_linetab_colorpicker.color = '#2ca08b'
        
         
        else:
          pass
        
        #file 2
        #checking for 'T1500 3rd Pass' sheet in workbook and plotting bokeh points 
        if 'T1500 3rd Pass' in sheetNames2:
          #read file2 sheet_name = 'T1500 3rd Pass'
          file2_data_T1500_3rd_Pass = pd.read_excel('static/upload/' + file2.filename, sheet_name='T1500 3rd Pass') 
          #get df for file2 sheet_name = 'T1500 3rd Pass'
          file2_T1500_3rd_Pass_df =  pd.DataFrame(file2_data_T1500_3rd_Pass)
          #remove extra space from column name in file 1 sheet_name = T1500
          file2_T1500_3rd_Pass_df.columns = [x.replace("\n", " ") for x in file2_T1500_3rd_Pass_df.columns.to_list()]
        
          #define source for bokeh plot for file1 sheet_name = T1500
          file2_SOURCE1_T1500_3rd_Pass = ColumnDataSource(data=file2_T1500_3rd_Pass_df)
        
          #plot all values to bokeh (both circle and line tabs) from file1 sheet_name = T1500 3rd Pass
        
          #Average Sword Depth and colorpickers
          file2_ASD_T1500_3rd_Pass_circletab = p.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file2_SOURCE1_T1500_3rd_Pass ,  color = '#2ca08b', width = 1, legend_label= file2.filename +" T1500 3rd Pass Average Sword Depth", line_dash = 'dashed')
          file2_ASD_T1500_3rd_Pass_linetab = p2.line(x = "KP [km]" , y = "Average Sword Depth [m]", source = file2_SOURCE1_T1500_3rd_Pass ,  color = '#2ca08b', width = 1, legend_label= file2.filename +" T1500 3rd Pass Average Sword Depth", line_dash = 'dashed')
          
       
          file2_ASD_T1500_3rd_Pass_circletab_colorpicker = ColorPicker(title= 'file2 Average Sword Depth Pass 3 Circle Tab ')
          file2_ASD_T1500_3rd_Pass_circletab_colorpicker.js_link('color', file2_ASD_T1500_3rd_Pass_circletab.glyph, 'line_color')
          file2_ASD_T1500_3rd_Pass_circletab_colorpicker.color = '#2ca08b'
        
          file2_ASD_T1500_3rd_Pass_linetab_colorpicker = ColorPicker(title= 'File 2 Average Sword Depth pass 3 ')
          file2_ASD_T1500_3rd_Pass_linetab_colorpicker.js_link('color', file2_ASD_T1500_3rd_Pass_linetab.glyph, 'line_color')
          file2_ASD_T1500_3rd_Pass_linetab_colorpicker.color = '#2ca08b'
          
         
        else:
          pass
        
        #style attritubes of plots
        p.title.text = 'DOL/DOC Trenching Visualization'
        p.xaxis.axis_label = "KP [km]"
        p.yaxis.axis_label = "DOL [m] / DOC [m]"
        p.y_range.flipped = True
        p.legend.click_policy="hide"
        p.title.align = "center"
        p.title.text_font_size = "20px"
        p.legend.label_text_font_size = "8px"
        p.add_layout(p.legend[0], 'right')
        
        p2.legend.click_policy = "hide"
        p2.y_range.flipped = True
        p2.title.text = 'DOL/DOC Trenching Visualization'
        p2.xaxis.axis_label = "KP [km]"
        p2.yaxis.axis_label = "DOL [m] / DOC [m]"
        p2.title.align = "center"
        p2.title.text_font_size = "20px"
        p2.legend.label_text_font_size = "8px"
        p2.add_layout(p2.legend[0], 'right')
        
        # set up Y RangeSlider
        range_slider = RangeSlider(
            title="Adjust y-axis range",
            start=-6,
            end=6,
            step=0.1,
            #value=(p.y_range.start, p.y_range.end),
            value = (4,-2)
        )
        range_slider.js_link("value", p.y_range, "start", attr_selector=0)
        range_slider.js_link("value", p2.y_range, "start", attr_selector=0)
        range_slider.js_link("value", p.y_range, "end", attr_selector=1)
        range_slider.js_link("value", p2.y_range, "end", attr_selector=1)
        
        
        # set up X RangeSlider
        x_range_slider = RangeSlider(
            title="Adjust x-axis range",
            start=0,
            end=500,
            step=1,
            #value=(p.y_range.start, p.y_range.end),
            value = (0,500)
        )
        x_range_slider.js_link("value", p.x_range, "start", attr_selector=0)
        x_range_slider.js_link("value", p2.x_range, "start", attr_selector=0)
        x_range_slider.js_link("value", p.x_range, "end", attr_selector=1)
        x_range_slider.js_link("value", p2.x_range, "end", attr_selector=1)
        
        if  'T1500 3rd Pass' in sheetNames:
          tabf_line = Row( file1_DOLReq_linetab_colorpicker,  \
                                 file1_DOL_linetab_colorpicker, \
                                 file1_DOC_linetab_colorpicker,\
                                  file1_ASD_T1500_linetab_colorpicker, \
                                  file1_ASD_T1500_2nd_Pass_linetab_colorpicker,\
                                file1_ASD_T1500_3rd_Pass_linetab_colorpicker\
                                ) 
          
          tabf_circle = Row(file1_DOLRReq_circletab_colorpicker,   \
                                 file1_DOL_circletab_colorpicker, \
                                 file1_DOC_circletab_colorpicker,\
                                 file1_ASD_T1500_circletab_colorpicker,  \
                                 file1_ASD_T1500_2nd_Pass_circletab_colorpicker,\
                                 file1_ASD_T1500_3rd_Pass_circletab_colorpicker,\
                                ) 
        
        else:
          if  'T1500 2nd Pass' in sheetNames:
            tabf_line = Row( file1_DOLReq_linetab_colorpicker,  \
                                  file1_DOL_linetab_colorpicker, \
                                 file1_DOC_linetab_colorpicker,\
                                  file1_ASD_T1500_linetab_colorpicker, \
                                  file1_ASD_T1500_2nd_Pass_linetab_colorpicker,\
                                 ) 
            
            tabf_circle = Row(file1_DOLRReq_circletab_colorpicker,   \
                                 file1_DOL_circletab_colorpicker,  \
                                 file1_DOC_circletab_colorpicker,\
                                 file1_ASD_T1500_circletab_colorpicker,  \
                                 file1_ASD_T1500_2nd_Pass_circletab_colorpicker,\
                                 ) 
            
          else:
            if 'T1500' in sheetNames:
              tabf_line = Row( file1_DOLReq_linetab_colorpicker,  \
                                  file1_DOL_linetab_colorpicker, \
                                 file1_DOC_linetab_colorpicker,\
                                  file1_ASD_T1500_linetab_colorpicker, \
                                 ) 
              
              tabf_circle = Row(file1_DOLRReq_circletab_colorpicker,  \
                                 file1_DOL_circletab_colorpicker,  \
                                 file1_DOC_circletab_colorpicker,\
                                 file1_ASD_T1500_circletab_colorpicker,  \
                                 ) 
        #file2
        if  'T1500 3rd Pass' in sheetNames2:
          tabf_line_file2 =  Row( file2_DOLReq_linetab_colorpicker,  \
                                  file2_DOL_linetab_colorpicker, \
                                 file2_DOC_linetab_colorpicker,\
                                  file2_ASD_T1500_linetab_colorpicker, \
                                  file2_ASD_T1500_2nd_Pass_linetab_colorpicker,\
                                 file2_ASD_T1500_3rd_Pass_linetab_colorpicker\
                                ) 
          
          tabf_circle_file2 =  Row(file2_DOLRReq_circletab_colorpicker,   \
                                 file2_DOL_circletab_colorpicker,  \
                                 file2_DOC_circletab_colorpicker,\
                                 file2_ASD_T1500_circletab_colorpicker,  \
                                 file2_ASD_T1500_2nd_Pass_circletab_colorpicker,\
                                 file2_ASD_T1500_3rd_Pass_circletab_colorpicker,\
                                ) 
        
        else:
          if  'T1500 2nd Pass' in sheetNames2:
            tabf_line_file2 = Row( file2_DOLReq_linetab_colorpicker,  \
                                  file2_DOL_linetab_colorpicker, \
                                 file2_DOC_linetab_colorpicker,\
                                  file2_ASD_T1500_linetab_colorpicker, \
                                 file2_ASD_T1500_2nd_Pass_linetab_colorpicker,\
                                 ) 
            
            tabf_circle_file2 = Row(file2_DOLRReq_circletab_colorpicker,   \
                                 file2_DOL_circletab_colorpicker,  \
                                 file2_DOC_circletab_colorpicker,\
                                 file2_ASD_T1500_circletab_colorpicker,  \
                                 file2_ASD_T1500_2nd_Pass_circletab_colorpicker, \
                                 ) 
          else:
            if 'T1500' in sheetNames2:
              tabf_line_file2 = Row( file2_DOLReq_linetab_colorpicker,  \
                                  file2_DOL_linetab_colorpicker, \
                                 file2_DOC_linetab_colorpicker,\
                                  file2_ASD_T1500_linetab_colorpicker, \
                                 ) 
              
              tabf_circle_file2 = Row(file2_DOLRReq_circletab_colorpicker,   \
                                 file2_DOL_circletab_colorpicker, \
                                 file2_DOC_circletab_colorpicker,\
                                 file2_ASD_T1500_circletab_colorpicker,  \
                                 ) 
              
        #making tabs for line and circle plot
        tab1 = Panel(child=column(x_range_slider, range_slider,p,tabf_circle, tabf_circle_file2), title="Circle")
        tab2 = Panel(child=column(x_range_slider, range_slider, p2,tabf_line, tabf_line_file2), title="Line")
        
        #combining tabs
        tabd = Tabs(tabs=[ tab1, tab2 ])
              
        #getting everything into html
        html2 = file_html( tabd,  CDN)
         
          
        
        return render_template('index2.html', html2 = html2)
        
        

