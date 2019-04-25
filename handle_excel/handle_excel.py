# encoding:utf8

import os
import xlrd
import xlsxwriter
from datetime import date, datetime

def get_cell_val(sheet, i, j, datemode=0):
    ctype = sheet.cell(i, j).ctype
    cell = sheet.cell_value(i, j)
    if ctype == 2 and cell % 1 == 0: # 如果是整形
        cell = int(cell)
    elif ctype == 3:
        # 转换为datetime对象
        if cell >= 1.0 and cell < 61.0:
            date_value = xlrd.xldate_as_datetime(cell, datemode)
            cell = date_value.strftime('%Y/%m/%d %H:%M:%S')
            return cell
        date_value = xlrd.xldate_as_tuple(cell, datemode)
        if date_value[0]==0 and date_value[1] == 0 and date_value[2] == 0:
            cell = '%d:%02d:%02d'%(date_value[3], date_value[4], date_value[5])
        elif date_value[3]==0 and date_value[4] == 0 and date_value[5] == 0:
            cell = date(*date_value[:3]).strftime('%Y/%m/%d')
        else:
            cell = datetime(*date_value).strftime('%Y/%m/%d %H:%M:%S')
    elif ctype == 4:
        cell = True if cell == 1 else False
    return cell

def read_context_from_excel(filename):
    if not os.path.exists(filename):
        return []
    
    arr = []
    workbook = xlrd.open_workbook(filename=filename)
    for sheetname in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheetname)
        cur_sheet = []
        for i in range(sheet.nrows):
            rows = []
            for j in range(sheet.ncols):
                rows.append(get_cell_val(sheet, i, j, datemode=workbook.datemode))
            cur_sheet.append(rows)
        arr.append(cur_sheet)
    return arr

def save_to_excel(filename, arr):
    workbook = xlsxwriter.Workbook(filename=filename)
    for i in range(len(arr)):
        sheet = workbook.add_worksheet()
        for j in range(len(arr[i])):
            for k in range(len(arr[i][j])):
                sheet.write(j, k, arr[i][j][k])
    workbook.close()

if __name__ == "__main__":
    arr = read_context_from_excel('1.xlsx')
    save_to_excel(filename='2.xlsx', arr=arr)
