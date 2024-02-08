from ezdxf.fonts import fonts

def move_fonts(fonts_directory=None):
    if fonts_directory != None:
        folder_from = fonts_folder

    '''Далее папки куда надо закинуть шрифты'''
    folder_to = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Windows\\Fonts'
    folder_to_windows = f'C:\\Windows\\Fonts'

    try:
        if not os.path.isdir(folder_to) or not os.path.isdir(folder_from):
            raise BaseException('Нет папок для добавления шрифта')
    except:
        raise BaseException('Не пускает проверить наличие папок для шрифтов')
    try:
        for f in os.listdir(folder_from):
            if os.path.isfile(os.path.join(folder_from, f)):
                if f not in os.listdir(folder_to):
                    shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, f))
                if f not in os.listdir(folder_to_windows):
                    shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to_windows, f))
            if os.path.isdir(os.path.join(folder_from, f)):
                os.system(f'rd /S /Q {folder_to}\\{f}')
                shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, f))
    except:
        raise BaseException('Ошибка при добавление шрифтов в папки')

