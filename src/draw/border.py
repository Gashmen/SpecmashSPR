import ezdxf

def create_border_A3(doc,y_min_upside,x_min_rightside):
    '''
    Создает рамку А3 формата с аттрибутами сразу
    :param doc:
    :param y_min_upside:
    :param x_min_rightside:
    :return:
    '''
    block_border = doc.blocks['Border_A3']
    values = {attdef.dxf.tag: '' for attdef in block_border.query('ATTDEF')}
    if doc.blocks.get('Border_A3'):
        border_insert = doc.modelspace().add_blockref(name='Border_A3',
                                                      insert=(x_min_rightside,y_min_upside))
        border_insert.add_auto_attribs(values)

        return border_insert

def write_rudes(attrib_rudes, rudes:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_rudes.dxf.tag == 'RUDES':
        if rudes != None:
                attrib_rudes.dxf.text = rudes

def write_rudesdata(attrib_rudesdata, rudesdata:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_rudesdata.dxf.tag == 'RUDESDATA':
        if rudesdata != None:
                attrib_rudesdata.dxf.text = rudesdata

def write_rucheck(attrib_rucheck, rucheck:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_rucheck.dxf.tag == 'RUCHECK':
        if rucheck != None:
                attrib_rucheck.dxf.text = rucheck

def write_rucheckdata(attrib_rucheckdata, rucheckdata:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_rucheckdata.dxf.tag == 'RUCHECKDATA':
        if rucheckdata != None:
                attrib_rucheckdata.dxf.text = rucheckdata

def write_runcont(attrib_runcont, runcont:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_runcont.dxf.tag == 'RUNCONT':
        if runcont != None:
                attrib_runcont.dxf.text = runcont

def write_runcontdata(attrib_runcontdata, runcontdata:str):
    '''
    Заполнение аттрибута scale
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_runcontdata.dxf.tag == 'RUNCONTDATA':
        if runcontdata != None:
                attrib_runcontdata.dxf.text = runcontdata

def wrire_rupem(attrib_rupem,rupem):
    if attrib_rupem.dxf.tag == 'RUPEM':
        if rupem != None:
                attrib_rupem.dxf.text = rupem

def wrire_rupemdata(attrib_rupemdata,rupemdata):
    if attrib_rupemdata.dxf.tag == 'RUPEMDATA':
        if rupemdata != None:
                attrib_rupemdata.dxf.text = rupemdata

def write_RUTITLE_attrib(attrib_rutitle, rutitle_text:str):
    '''
    Заполнение аттрибута rutitle
    :param attrib_rutitle: В цикле проверки аттрибутов передается аттрибут
    :param rutitle_text: Значение str от rutitleLineEdit
    :return:
    '''
    if attrib_rutitle.dxf.tag == 'RUTITLE':
        if rutitle_text != None:
            if len(rutitle_text) <= 36:
                attrib_rutitle.dxf.text = rutitle_text
            else:
                attrib_rutitle.dxf.text = rutitle_text[:36]

def write_project_title_1(attrib_project_title_1, project_title_1):
    if attrib_project_title_1.dxf.tag == 'PROJECT_TITLE_1':
        if project_title_1 != None:
                attrib_project_title_1.dxf.text = project_title_1

def write_project_title_2(attrib_project_title_2, project_title_2):
    if attrib_project_title_2.dxf.tag == 'PROJECT_TITLE_2':
        if project_title_2 != None:
                attrib_project_title_2.dxf.text = project_title_2

def write_project_title_3(attrib_project_title_3, project_title_3):
    if attrib_project_title_3.dxf.tag == 'PROJECT_TITLE_3':
        if project_title_3 != None:
                attrib_project_title_3.dxf.text = project_title_3

def write_company_attrib(attrib_company, companylineedit_text:str):
    '''
    Заполнение аттрибута Company
    :param attrib_company: В цикле проверки аттрибутов передается аттрибут
    :param companylineedit_text: Значение str от companylineedit
    :return:
    '''
    if attrib_company.dxf.tag == 'COMPANY':
        if companylineedit_text != None:
            if len(companylineedit_text) <= 27:
                attrib_company.dxf.text = companylineedit_text
            else:
                attrib_company.dxf.text = companylineedit_text[:27]



def write_project_attrib(attrib_projecttitle, projecttitle_text:str):
    '''
    Заполнение аттрибута projecttitle 1 2 3
    :param attrib_projecttitle: В цикле проверки аттрибутов передается аттрибут
    :param rutitle_text: Значение str от projecttitleLineEdit
    :return:
    '''
    if len(projecttitle_text) <= 25:
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_2':
            attrib_projecttitle.dxf.text = projecttitle_text

    elif 26 <= len(projecttitle_text) <= 50:
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_2':
            attrib_projecttitle.dxf.text = projecttitle_text[:25]
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_3':
            attrib_projecttitle.dxf.text = projecttitle_text[25:]

    elif 51 <= len(projecttitle_text) <= 75:
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_1':
            attrib_projecttitle.dxf.text = projecttitle_text[:25]
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_2':
            attrib_projecttitle.dxf.text = projecttitle_text[25:50]
        if attrib_projecttitle.dxf.tag == 'PROJECT_TITLE_3':
            attrib_projecttitle.dxf.text = projecttitle_text[50:]


def write_scale(attrib_SCALE, SCALE:float):
    '''
    Заполнение
    :param attrib_SCALE: В цикле проверки аттрибутов передается аттрибут
    :param SCALE: 2,2.5,4,....
    :return:
    '''
    if attrib_SCALE.dxf.tag == 'SCALE':
        if SCALE != None:
                attrib_SCALE.dxf.text = f'1:{SCALE}'

def write_page_number(attrib_RUSHEET, sheet_number = 1):
    '''Пишет номер страницы'''
    if attrib_RUSHEET.dxf.tag == 'RUSHEET':
        if sheet_number != None:
                attrib_RUSHEET.dxf.text = str(sheet_number)

def write_page_numbers(attrib_RUSHTS, sheet_count = 2):
    '''Пишет номер страницы'''
    if attrib_RUSHTS.dxf.tag == 'RUSHTS':
        if sheet_count != None:
                attrib_RUSHTS.dxf.text = str(sheet_count)


