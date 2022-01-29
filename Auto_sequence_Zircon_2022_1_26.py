# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 21:28:11 2021

@author: hujie
"""
# import pandas as pd
#界面
import PySimpleGUI as sg
initial_val = [['Sample','SRM 610','JA001.d']]
input_col =[[sg.T('元素标样',justification='c',size= (10,1)),sg.T('数量(自动计算)',justification='l',size= (12,1))],
            [sg.Input('SRM 610', key= 'Elemstand',justification='r',size= (10,1)),sg.Input('11',background_color='yellow', key= 'nElemstand',justification='r',size= (12,1))],
            [sg.T('年龄标样',justification='c',size= (10,1)),sg.T('数量',justification='l',size= (12,1))],
            [sg.Input('91500', key= 'Agestand',justification='r',size= (10,1)),sg.Input('22',background_color='yellow', key= 'nAgestand',justification='r',size= (12,1))],
            [sg.T('年龄副标',justification='c',size= (10,1)),sg.T('数量',justification='l',size= (12,1))],
            [sg.Input('PLE', key= 'Agemonst',justification='r',size= (10,1)),sg.Input('20',background_color='yellow', key= 'nAgemonst',justification='r',size= (12,1))],
            [sg.T('样品总数')],
            [sg.Input('100', key= 'Total_samples',justification='r',size= (20,1))],
            [sg.T('样品组长度')],
            [sg.Input('10', key= 'sqz_single',justification='r',size= (20,1))],
            [sg.T('元素标样测试频率')],
            [sg.Input('2', key= 'element_frq_input',justification='r',size= (20,1))],
            [sg.T('样品前缀')],
            [sg.Input('Samp', key= 'Sampstart',justification='r',size= (20,1))],
            [sg.T('文件前缀')],
            [sg.Input('JA', key= 'Filestart',justification='r',size= (20,1))],
            [sg.Button('生成序列',key = 'Generate')],
            [sg.FileSaveAs('导出CSV',key='Export_Table',enable_events = True,disabled=True,file_types = (('Comma-Separated Values', '.csv'),))]  # TODO: better names
            ]

Headings = ['样品类型', '样品名称', '文件名称']
layout =[[sg.T('Auto Sequence Zircon',font='Default 20')],
                      [sg.Table(values=initial_val, headings=Headings, def_col_width=10,
                               # background_color='black',
                               auto_size_columns=False,
                               display_row_numbers=False,
                               justification='center',
                               num_rows=20,
                               # alternating_row_color='black',
                               key='Zircon_table',
                               row_height=25, visible=True),sg.Col(input_col)],
         [sg.T('作者：胡杰，Email:hujie@cdut.edu.cn',font='Default 14')],
        [sg.T('成都理工大学低温热年代学实验室',font='Default 14')],
         ]
window = sg.Window('Auto Sequence Zircon', layout, default_element_size=(20, 1), element_padding=(1, 1), return_keyboard_events= True, resizable=False, finalize=True)

# window = sg.Window('Window Title', layout)
while True:
    event, values = window.read()
#
    if event == 'Generate':

        # File = pd.DataFrame([],columns = Headings)

        nsample = int(values['Total_samples'])  #样品数
        sz_sq = int(values['sqz_single'])      #小序列长度
        element_frq = int(values['element_frq_input'])
        print(element_frq)

        #标样
        Elem_stand = values['Elemstand']
        Age_stand = values['Agestand']
        Age_monst = values['Agemonst']

        #样品前缀
        Samp_start = values['Sampstart']
        #文件前缀
        File_start = values['Filestart']

        number_sqz = nsample//sz_sq   #小序列数量
        number_last_sqz = nsample % sz_sq  #余数

        #空序列用来装所有的样品明
        top_standards_with_610 = [Elem_stand, Age_stand, Age_stand,Age_monst] #偶数组打610
        top_standards_no_610 = [Age_stand, Age_stand,Age_monst]  #奇数组不打610
        mid = [Age_monst] #检测标样
        all_sqz = []
        if number_last_sqz == 0: # 当余数等于0时候,满序列
            for i in range(number_sqz):
                spz_small = [Samp_start+str(j+i*sz_sq+1).zfill(3) for j in range(sz_sq)]  #一小组的
                if i % element_frq == 0:
                    top_standards = top_standards_with_610
                else:
                    top_standards = top_standards_no_610
                sqz_sample_name = top_standards+ spz_small   #一小组
                all_sqz.extend(sqz_sample_name)

        elif number_last_sqz <=4:# 当余数小于等于4时候，多余的放在最后序列上
            for i in range(number_sqz-1): #前面的样品

                spz_small = [Samp_start+str(j+i*sz_sq+1).zfill(3) for j in range(sz_sq)]  #一小组的
                if i%element_frq == 0:
                    top_standards = top_standards_with_610
                else:
                    top_standards = top_standards_no_610
                sqz_sample_name = top_standards +spz_small # 一小组
                all_sqz.extend(sqz_sample_name)
            # all_sqz.extend(sqz_sample_name)
            #多余的样品
            if (i+1)%element_frq  == 0:
                top_standards = top_standards_with_610
            else:
                top_standards = top_standards_no_610
            extra_sqz = top_standards+[Samp_start + str(j+1 + (i+1) * sz_sq).zfill(3) for j in range(sz_sq+number_last_sqz)]  #剩余的样品
            # sqz_sample_name = top_standards + first_five +  last_five  # 一小组
            all_sqz.extend(extra_sqz)

            # extra_sample = [Samp_start + str(j + (i+1) * sz_sq + 1).zfill(3) for j in range(number_last_sqz)]
            # all_sqz.extend(extra_sample)

        else: #当余数达到5时候，重新生成一小断
            for i in range(number_sqz):

                spz_small = [Samp_start+str(j+i*sz_sq+1).zfill(3) for j in range(sz_sq)]  #一小组的
                if i % element_frq == 0:
                    top_standards = top_standards_with_610
                else:
                    top_standards = top_standards_no_610
                sqz_sample_name = top_standards + spz_small  # 一小组
                all_sqz.extend(sqz_sample_name)
            #额外的一小列
            extra_sample =top_standards+[Samp_start + str(j + (number_sqz) * sz_sq + 1).zfill(3) for j in range(number_last_sqz)]
            all_sqz.extend(extra_sample)

        end_standards = [Age_monst,Age_stand,Age_stand,Elem_stand]
        all_sqz.extend(end_standards)
        number_of_Elemstand = 0 #元素标样数量
        number_of_Agestand = 0#主标数量
        number_of_Agemonst = 0 #副标数量
        for namez in all_sqz:
            if namez == Elem_stand:
                number_of_Elemstand = number_of_Elemstand+1
            elif namez == Age_stand:
                number_of_Agestand = number_of_Agestand+1
            elif namez == Age_monst:
                number_of_Agemonst = number_of_Agemonst + 1
            else:
                pass

        #样品类型
        Samples_kinds = ['Sample']*len(all_sqz)
        #文件名称
        Files_sz = [File_start+str(j+1).zfill(3)+'.d' for j in range(len(all_sqz))]
        # File['样品类型'] = Samples_kinds
        # File['样品名称'] = all_sqz
        # File['文件名称'] = Files_sz
        # window['Zircon_table'].update(values=File[:].values.tolist())
        data_tuple = list(zip(Samples_kinds,all_sqz,Files_sz)) # zip方法里面都是tuple
        data_list = [list(tz) for tz in data_tuple ] #把里面的tuple转化为list
        window['Zircon_table'].update(values=data_list)
        window['Export_Table'].Update(disabled=False)
        window['nElemstand'].Update(number_of_Elemstand)
        window['nAgestand'].Update(number_of_Agestand)
        window['nAgemonst'].Update(number_of_Agemonst)
        # mline: sg.Multiline = window['Fit_information']
        # mline.update('slope: \n', append=False) # False is used to clear the previous text
        # mline.update(slopes, append=True)
        # mline.update('\nBreaks: \n', append=True)
        # mline.update(breaks, append=True)
        # mline.update('\nR square: \n', append=True)
        # mline.update(rsq, append=True)
        print(all_sqz)

    elif event == 'Export_Table':
        file_name_excel = values['Export_Table']
        import csv
        try:
            with open(file_name_excel, 'w',newline='')as f:  # newline = ''是为了防止出现空行
                f_csv = csv.writer(f)
                # f_csv.writerow(Headings)
                f_csv.writerows(data_list)
        except:
            pass
        # from openpyxl import Workbook
        # from openpyxl.worksheet.table import Table, TableStyleInfo

        # wb = Workbook()
        # ws = wb.active
        # # add column headings. NB. these must be strings
        # ws.append(Headings)
        # for row in data_list:
        #     ws.append(row)


    elif event in ('Exit', None):
        break
window.close()