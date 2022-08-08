import os, sys, random, string


'''
Функция создания случайного имени для файла/папки.
Данная функция может принимать параметр folder, при наличие которого функция создаст уникальное имя для указанной директории.
'''
def generate_random_file_name(folder=None):
    symbols = string.ascii_letters + string.digits
    get_name = lambda: ''.join([i for i in random.choices(symbols, k=random.randint(3,10))])

    if folder:
        temp = set(os.listdir(folder))
        while len(os.listdir(folder)) == len(temp):
            name = get_name()
            temp.add(name)
        return name

    return get_name()




def main():
    '''
    Сначала необходимо "спарсить" переданные аргументы.
    '''
    try:
        if len(sys.argv) in [4,5]:
            folder, ext, count_files = sys.argv[1:4]
            


            subfolders = False
            if len(sys.argv) == 5:
                subfolders = True if sys.argv[4] in ['true', 'True', 'TRUE'] else False
        else:
            raise IndexError
    except IndexError as e:
        txt = f"""
Ошибка! Необходимо указать параметры!

- python {sys.argv[0]} *folder* *ext* *count_files* *subfolders*

# folder - папка в которой будут создаваться файлы и папки (обязательный параметр)

# ext - расширение файлов которые будут создаваться (обязательный параметр)

# count_files - количество файлов для генерации (обязательный параметр)

# subfolders - генерить файлы и подпапки (True/False) (по умолчанию False, не создавать подпапки с файлами)
        """
        print(e, txt, sep='\n')
        return

    
    '''
    Отправной точкой будет создание директории, где будут создаваться новые файлы и папки
    '''
    os.mkdir(folder)


    '''
    Объявим 3 переменные, которые потребуются в дальнейшем:
    created_files - в ней будет содержаться о количестве уже создавшихся файлов;
    folds - список, в котором будет содержаться названия подпапок;
    chance - условная переменная, которая будет отвечать за вероятность создания новой папки и/или поднятия на уровень выше.
    max_level - 
    '''

    created_files = 0
    folds = list()
    chance = 33
    max_level = 5


    '''
    Создадим цикл WHILE, который прекратит свою работу, когда количество созданных файлов станет равным заданному количеству в переменную count_files;

    Внутри цикла будет расположен блок IF. 
    1) Eсли параметр subfolders выставлен в True, а также текущий уровень меньше 5 и выпадет вероятность на создание папки,
    то создадим новую папку со случайным именем и добавим ее в список folds.
    2) Если какое-то из условий выше False, тогда проверим, находимся ли в каком-то подпапке и с определенной вероятностью поднимимся выше
    3) Иначе будет создан новый файл с расширением ext и в него будет записаная случайная информация, а переменная created_files увеличится на 1.

    '''

    while created_files != int(count_files):
        if subfolders and len(folds) < max_level and (random.randint(0,100) < chance):
            random_name = generate_random_file_name(folder)
            folds.append(random_name)
            os.mkdir(folder+'/'+'/'.join(folds))

        elif folds and (random.randint(0,100) < chance):
            folds.pop()

        else:
            with open(f'{folder+"/"+"/".join(folds)}/{generate_random_file_name(folder)}.{ext}', 'wb') as cur_file:
                data = bytes(''.join([i for i in random.choices(string.printable, k=random.randint(30, 1500))]), encoding='utf-8')
                cur_file.write(data)
            created_files += 1
        
if __name__ == '__main__':
    main()

    print('Работа скрипта завершена!')

# Написать скрипт на python, который генерит заданное количество файлов различного содержимого.
# Скрипт будет использоваться для создания тестового окружения.

# входные параметры:
# folder - папка в которой будут создаваться файлы и папки (обязательный параметр)
# ext - расширение файлов которые будут создаваться (обязательный параметр)
# count_files - количество файлов для генерации (обязательный параметр)
# subfolders - генерить файлы и подпапки (по умолчанию false, не создавать подпапки с файлами)

# принцип работы скрипта:
# скрипт генерит 'count_files' файлов с различным содержимым (пока что не принципиально с чем, но в будущем можем 
# подправить под определенное содержимое) и с заданным расширением 'ext' в папке 'folder'.
# Если задан параметр 'subfolders', то так же создаются подпапки (с рандомным названием и рандомной вложеностью, максимум 5 уровня)
# и в этих подпапках тоже создаются файлы (но могут и не создаваться).