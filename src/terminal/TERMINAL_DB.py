import ezdxf

def define_names_terminal(doc_dict_blocks:dict):
    '''
    self.doc_dict_blocks = {block.dxf.name: block for block in self.doc_base.blocks
                        if '*' not in block.dxf.name}
    :param doc_dict_blocks:
    :return:
    '''
    names_of_terminal = list()
    for block_name in doc_dict_blocks.keys():
        if 'screw' in block_name.lower() or 'sparing' in block_name.lower():
            if '_'.join(block_name.split('_')[0:4]) not in names_of_terminal:
                names_of_terminal.append(block_name)
    # names_of_terminal.append('SUPU')
    return names_of_terminal

def define_manufacturer(names_of_terminal):
    MANUFACTURER = set((name_of_terminal.split('_')[0] for name_of_terminal in names_of_terminal))
    # MANUFACTURER = ['SUPU']
    return MANUFACTURER

def define_type_of_terminal(names_of_terminal:list, manufacturer:str):
    if manufacturer:
        TYPE_OF_TERMINAL = list()
        for terminal in names_of_terminal:
            if manufacturer == terminal.split('_')[0]:
                if terminal.split('_')[1].lower() == 'screw':
                    TYPE_OF_TERMINAL.append('Винтовые')
                elif terminal.split('_')[1].lower() == 'spring':
                    TYPE_OF_TERMINAL.append('Пружинные')
        return list(set(TYPE_OF_TERMINAL))
    else:
        return ['']

def define_appointment_of_terminal(names_of_terminal:list, manufacturer:str,type_of_terminal:str):

    if manufacturer and type_of_terminal:
        TYPEOFTERMINAL = 'SCREW' if type_of_terminal == 'Винтовые' else 'SPRING'
        appointment_of_terminal = list()
        for terminal in names_of_terminal:
            if manufacturer == terminal.split('_')[0] and terminal.split('_')[1] == TYPEOFTERMINAL:
                if terminal.split('_')[2] == 'WHITE':
                    appointment_of_terminal.append('L')
                elif terminal.split('_')[2] == 'BLUE':
                    appointment_of_terminal.append('N')
                elif terminal.split('_')[2] == 'GREEN':
                    appointment_of_terminal.append('PE')
        return list(set(appointment_of_terminal))
    else:
        return ['']

def define_conductorsection_terminal(names_of_terminal:list,manufacturer:str,type_of_terminal: str,appointment_of_terminal:str):

    if manufacturer and type_of_terminal and appointment_of_terminal:
        TYPEOFTERMINAL = 'SCREW' if type_of_terminal == 'Винтовые' else 'SPRING'
        APPOINMENT = 'WHITE' if appointment_of_terminal == 'L' else 'BLUE' if appointment_of_terminal == 'N' else 'GREEN'
        conductor_section = list()
        for terminal in names_of_terminal:
            if manufacturer == terminal.split('_')[0] and\
                    terminal.split('_')[1] == TYPEOFTERMINAL and\
                    terminal.split('_')[2] == APPOINMENT:
                conductor_section.append(terminal.split('_')[3])
        return sorted(list(set(conductor_section)),key = lambda x: float(x))
    else:
        return ['']


def define_name_of_terminal(name_from_qt:str):
    TYPEOFTERMINAL = 'SCREW' if name_from_qt.split('_')[1] == 'Винтовые' else 'SPRING'
    APPOINMENT = 'WHITE' if name_from_qt.split('_')[2] == 'L' else 'BLUE' if name_from_qt.split('_')[2] == 'N' else 'GREEN'
    return '_'.join([name_from_qt.split('_')[0],TYPEOFTERMINAL,APPOINMENT,name_from_qt.split('_')[3] ])

def change_name_from_to(name:str):
    '''
    Смена имени для клеммы с английского на русский и наоборот по структуре на 06.02.23
    '''
    const_names = {'Концевой стопор':'Terminal_end_stop_frontside',
                   'Концевая пластина':'Terminal_end_plate_frontside_2.5'}
    if name in list(const_names.keys()):
        return const_names[name]


    return_name = name
    rus_language = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    #Проверка если есть русские буквы в строке, то значит это приход
    dict_translator = {'Винтовые':'SCREW','Пружинные':'SPRING', 'PE':'GREEN','L':'WHITE','N':'BLUE',
                       }
    rus = None
    for letter in name.lower():
        if letter in rus_language:
            rus = True
            break
    if rus == None:
        dict_eng = {eng_word:rus_word for rus_word,eng_word in dict_translator}
        for word_eng in dict_eng.keys():
            if word_eng in return_name:
                return_name.replace(word_eng,dict_eng[word_eng])
    else:
        return_name = return_name.split('_')
        for word_rus in dict_translator:
            if word_rus in return_name:
                return_name[return_name.index(word_rus)] = dict_translator[word_rus]
        return_name = '_'.join(return_name)
    return return_name



if __name__ == '__main__':
    print(define_type_of_terminal(names_of_terminal=define_names_terminal(),manufacturer='SUPU'))

