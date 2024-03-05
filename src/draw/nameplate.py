import ezdxf
import datetime
from ezdxf.entities import Attrib


def create_nameplate_doc(doc_base, scale, topside_insert):
    '''
    Удаляем все ненужное из dxf_base и возвращаем doc_nameplate
    '''

    block_nameplate = doc_base.blocks['nameplate']
    values = {attdef.dxf.tag: '' for attdef in block_nameplate.query('ATTDEF')}
    nameplate_insert = doc_base.modelspace().add_blockref(name='nameplate',insert=topside_insert.dxf.insert)
    nameplate_insert.dxf.xscale = 1 / scale
    nameplate_insert.dxf.yscale = 1 / scale
    nameplate_insert.dxf.zscale = 1 / scale
    nameplate_insert.add_auto_attribs(values)
    return nameplate_insert

def write_attrib_box_full_name(attrib,full_name,add_numbers='.XXXX.XX'):
    '''
    Заполнение аттрибута BOX_FULL_NAME
    :param attrib: аттрибут в nameplate
    :param full_name: КВП.261610
    :param add_numbers: .{номер заявки}.{номер изделия в этой заявке}
    :return:
    '''

    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'BOX_FULL_NAME':
            attrib.dxf.text = f'{full_name}-{str(datetime.datetime.now())[2:4]}{add_numbers}'

def write_explosion_tag(attrib, gasdustore='1 Ex e IIC',temperature_class='T6', IP='66'):

    '''self.gasdustoreComboBox_shellpage.currentText() + ' ' + self.temperature_class_comboBox_shellpage.currentText() + ' Gb, IP66'''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'EXPLOSION_TAG':
            attrib.dxf.text = f'{gasdustore} {temperature_class} Gb, IP{IP}'

def write_minus_temperature(attrib, minus_temperature = '-60'):
    '''Написание минусовой температуры
    self.mintempLineEdit_shellpage.text()
    '''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'MINUS_TEMPERATURE':
            attrib.dxf.text = f'{minus_temperature}'

def write_plus_temperature(attrib, plus_temperature = '+40'):
    '''Написание плюсовой температуры
    self.maxtempLineedit_shellpage.text()
    '''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'PLUS_TEMPERATURE':
            attrib.dxf.text = f'+{plus_temperature}'

def write_voltage_current_frequency(attrib, voltage='XXX',current='XX',frequency='XX/XX'):
    '''Заполнените тэга V_I_F'''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'V_I_F':
            attrib.dxf.text = f'~{voltage}В {current}А {frequency}Гц'

def write_batch_number(attrib, batch_number='XXXXXXXXX'):
    '''Заполнение тэна BATCH_NUMBER'''
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'BATCH_NUMBER':
            attrib.dxf.text = f'Парт. № {batch_number}'

def write_just_attrib_1(attrib,just_attrib_1 = 'ОТКРЫВАТЬ'):
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'JUST_ATTRIB_1':
            attrib.dxf.text = f'{just_attrib_1}'

def write_just_attrib_2(attrib,just_attrib_2 = 'ОТКЛЮЧИВ ОТ СЕТИ'):
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'JUST_ATTRIB_2':
            attrib.dxf.text = f'{just_attrib_2}'

def write_just_attrib_3(attrib,just_attrib_3 = 'C  ≤ Ta ≤          C'):
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'JUST_ATTRIB_3':
            attrib.dxf.text = f'{just_attrib_3}'

def write_just_attrib_4(attrib,just_attrib_4 = 'o'):
    if isinstance(attrib, Attrib):
        if attrib.dxf.tag == 'JUST_ATTRIB_4':
            attrib.dxf.text = f'{just_attrib_4}'

