"""
程序为完成指定功能。创建功能完好，但删除无效
测试用例：
是否需要进行文件删除操作 (y/n) >>>>y
请输入需要删除的文件后缀名（如mp3，请不要再开头加上".")  >>>>>> png
请输入文件夹的名字(若不想设置请直接按回车键) >>>>
请输入文件名字中包含的关键字名称(如不需要请直接按回车键) >>>>
确认要删除文件吗？(y/n) >>>>>
输入有误，请重新输入。(y/n) >>>>>> y
删除成功。

进行到这一步进入文件夹查看，发现greedy文件夹下png文件仍然存在
原因及建议：本次项目重点之一为递归思想，功能为删除指定目录下的某种格式文件，不光只是删除指定目录第一层，更深层的该格式文件也要删除。
建议修改方案：查找指定目录后还要查找指定目录的子文件夹，直到最深一层，将所有层次中的指定格式文件删除，可使用递归思想达到目标。
"""


import os
import time
import logging
import random


def write_log(msg):
    logger = logging.Logger(__name__)
    logger.setLevel(logging.INFO)

    # add file handler logger
    # log 存放在上一级文件夹中
    path = os.path.join('..', 'file_operation.log')
    fh = logging.FileHandler(path)
    fh.setLevel(logging.INFO)
    # add stream handler logger
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)

    # add logger format
    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    formatter = logging.Formatter(fmt, datefmt)

    # set format
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    # add handdler
    logger.addHandler(fh)
    logger.addHandler(sh)

    # add log
    logger.info(msg)


def write_file(filepath, data=''):
    # 如果数据是图片，视频，声音，则用 wb 方法写入
    if isinstance(data, bytes):
        with open(filepath, 'wb') as f:
            f.write(data)

    # 否则数据为 string 类。 用 w 方法写入
    else:
        with open(filepath, 'w') as f:
            f.write(data)


def create_dir():
    '''
    在当前目录下创建 greedy -> python -> basic_learn -> basic_ai 文件夹
    '''
    # 创建 greedy 文件夹
    path = os.path.join(os.getcwd(), 'greedy')
    if not os.path.isdir(path):
        os.mkdir(path)

    # 创建 python 文件夹
    path = os.path.join(path, 'python')
    if not os.path.isdir(path):
        os.mkdir(path)

    # 创建 basic_learn 文件夹
    path = os.path.join(path, 'basic_learn')
    if not os.path.isdir(path):
        os.mkdir(path)

    # 创建 basic_ai 文件夹
    path = os.path.join(path, 'basic_ai')
    if not os.path.isdir(path):
        os.mkdir(path)


def create_files(filetype_list, words_list):
    # 获取当前目录下的所有文件
    files = os.listdir('.')

    # 在当前目录下随机创建n个文件
    n = random.randint(1, 10)
    for i in range(n):
        # 文件名为 时间戳+下列列表中随机抽取一个单词+贪心学院+后缀名
        file_name = str(int(time.time())) + random.choice(words_list) + '贪心学院' + '.' + random.choice(filetype_list)
        # 检测文件名是否存在
        while os.path.isfile(file_name):
            file_name = str(int(time.time())) + random.choice(words_list) + '贪心学院' + '.' + random.choice(filetype_list)

        # 创建该文件
        write_file(file_name)

    # 递归在子文件夹中创建文件
    for file in files:
        # 如果不是文件夹的话则跳过
        if not os.path.isdir(file):
            continue

        # 改变工作目录到子文件夹
        os.chdir(os.path.join(os.getcwd(), file))
        create_files(filetype_list, words_list)
        # 将工作目录更改回来
        os.chdir('..')


# 递归删除文件
def delete_file_helper(path, filekw, filetype):
    files = os.listdir(path)
    for each_file in files:
        # 如果文件后缀为指定后缀，并且含有关键字，则删除
        if each_file.split('.')[-1] == filetype and (filekw in each_file):
            os.remove(os.path.join(path, each_file))
            msg = '文件 {} 被删除，该文件的路径为: {}'.format(each_file, os.path.join(path, each_file))
            write_log(msg)
        # 如果是文件夹，则递归删除
        if os.path.isdir(os.path.join(path, each_file)):
            delete_file_helper(os.path.join(path, each_file), filekw, filetype)


def delete_file(filetype, folder, filekw='贪心学院'):
    '''
    如果目录不存在，则返回false
    如果用户决定不删了，或者删除成功了，则返回true
    '''
    path = os.getcwd()
    # 获取目标目录的绝对路径
    while(os.path.split(path)[-1] != folder):
        # 获取当前目录下的文件
        files_list = os.listdir(path)
        # 如果是文件夹，则进入子文件夹，并break出for循环
        for each_file in files_list:
            if os.path.isdir(os.path.join(path, each_file)):
                path = os.path.join(path, each_file)
                break
        # 如果没有文件夹了，说明输入的文件夹名字有误
        else:
            print('输入的文件夹名字有误。请重新输入。')
            return False

    is_delete = input('确认要删除文件吗？(y/n) >>>>> ')
    while (is_delete.lower() not in ['y', 'n']):
        is_delete = input('输入有误，请重新输入。(y/n) >>>>>> ')

    if is_delete == 'n':
        return True

    # 获取文件列表
    delete_file_helper(path, filekw, filetype)
    print('删除成功。')
    return True


def recover_file():
    # 读取log内容
    with open(os.path.join('..', 'file_operation.log'), 'r') as f:
        logs = f.readlines()

    # 清空log文件内容
    with open(os.path.join('..', 'file_operation.log'), 'w') as f:
        f.write('')

    # 恢复文件
    for one_log in logs:
        file_path = one_log.split(':')[-1].strip()
        # 获取文件完整路径
        write_file(file_path)


def main():
    # 创建一个 file-delete文件夹，并更改工作目录到该文件夹下
    if not os.path.isdir('file_delete'):
        os.mkdir('file_delete')
    os.chdir('file_delete')

    # 初始化文件类型、单词列表
    filetype_list = ['jpg', 'png', 'txt', 'mp4', 'csv', 'json', 'xlsx', 'pdf', 'gif', 'mp3']
    words_list = ['greedy', 'python', 'basic', 'hello', 'world', 'good', 'bad', 'ai', 'learning']
    # 创建文件夹
    create_dir()
    # 创建文件
    create_files(filetype_list, words_list)

    # 询问是否进行删除文件的操作
    is_remove_file = input('是否需要进行文件删除操作 (y/n) >>>>')
    while(is_remove_file.lower() not in ['y', 'n']):
        is_remove_file = input('输入有误，请重新输入。y为删除，n为不删除。(y/n) >>>> ')

    # 进行删除文件的操作
    if is_remove_file == 'y':
        # 输入文件后缀名
        file_type = input('请输入需要删除的文件后缀名（如mp3，请不要再开头加上".")  >>>>>> ')
        while file_type not in filetype_list:
            file_type = input('输入的文件后缀名有误，请重新输入。 >>>>>> ')

        # 输入文件夹，如果函数返回false，则需要重新输入
        res = False
        while not res:
            folder = input('请输入文件夹的名字(若不想设置请直接按回车键) >>>> ')
            keyword = input('请输入文件名字中包含的关键字名称(如不需要请直接按回车键) >>>> ')
            # 初始化folder参数
            if not folder:
                folder = os.path.split(os.getcwd())[-1]
            # 查看是否有filekw参数
            if not keyword:
                res = delete_file(file_type, folder)
            else:
                res = delete_file(file_type, folder, filekw=keyword)

    # 是否恢复文件
    is_recover_file = input('是否恢复已经删除的文件(y/n) >>>>> ')
    while is_recover_file.lower() not in ['y', 'n']:
        is_recover_file = input('输入有误，请重新输入。(y/n) >>>>>> ')

    if is_recover_file == 'y':
        recover_file()
        print('文件已经被恢复了。')


'''
拓展部分，实现剪切功能
'''


def cut_file(filename, old_path='.', new_path='.'):
    '''
    filename: 文件名称
    old_path: 文件原路径，可以是相对路径，也可以是绝对路径。默认为当前文件夹。
    new_path: 文件目标路径，可以是相对路径，也可以是绝对路径。默认问当前文件夹
    '''
    # 复制文件
    with open(os.path.join(old_path, filename), 'rb') as f:
        write_file(os.path.join(new_path, filename), data=f.read())
    # 删除原文件
    os.remove(os.path.join(old_path, filename))


if __name__ == '__main__':
    main()
    # cut_file('项目要求.txt', new_path='file_delete')
