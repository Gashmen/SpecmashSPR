import openpyxl
filefullpath = 'C:\\Users\\g.zubkov\\PycharmProjects\\Project_not_for_exe\\src\\examples\\AGCC.287-6930-2061428-A01-0001_A_RU.xlsx'
ws = openpyxl.load_workbook(filefullpath)
wb = ws.active

list_for_add = []

for cell in wb['C']:
    if cell.value != None:
        if str(cell.value) != '':
            if ',' in cell.value:
                if str(cell.value).endswith(','):
                    for _ in str(cell.value)[:-1].split(','):
                        list_for_add.append(_)
                else:
                    for _ in cell.value.split(','):
                        list_for_add.append(_)




for count,value in enumerate(list_for_add,start=1):
    wb[f'F{count}'].value = value

ws.save('C:\\Users\\g.zubkov\\PycharmProjects\\Project_not_for_exe\\src\\examples\\test.xlsx')