"""代码批注:
        1、代码缺少注释，写代码应注重可读性，在代码越来越复杂的情况下注释就显得很必要，可以提高代码的交接效率与可复用性。
        2、代码逻辑及层次不够清晰，不同类之间不要互相牵扯，类中的函数就执行跟他本身有关的操作，如天气每天随机变化，小草下雨生长次数就加1，小牛吃草就生长次数加1，逻辑可以放到主函数里（如判断生长次数是否到3，是否该唤醒小牛吃草）将主要逻辑按故事顺序在主函数里排下来使得代码更加简介明了有层次感，如项目需求又有改动，很快就能定位到需要改动的部分，不至于这里改一点那里改一点。
        3、总体项目完成度很不错，基本把功能都实现了，使用到了面向对象以及函数式编程，使用了继承，很不错，可以活学活用，再接再厉，老师相信经过你的第二次整理代码会更加合理简洁！
"""

import threading
import time
import random


class Weather:
    def __init__(self):
        self.rain = self.__get_weather()

    # 获取天气，20%的概率下雨
    def __get_weather(self):
        return random.randint(1, 10) <= 2


class Grass(threading.Thread):
    def __init__(self, cond):
        super().__init__(name='小草')
        self.__growth = 0  # 当growth达到3的时候表示成熟
        self.cond = cond

    # 小草成长
    def grow(self):
        self.__growth += 1

    # 检验小草是否成熟
    def mature(self):
        return self.__growth >= 3

    # 获取小草的成长值
    def get_growth(self):
        return self.__growth

    # 清空小草的成长值
    def eaten(self):
        self.__growth = 0

    def run(self):
        global cows_list

        while (True):
            # 当所有牛都成熟了，就结束循环
            if min(cows_list) >= 5:
                break

        # 小草线程结束，唤醒小牛线程，并释放锁
        self.cond.acquire()
        self.cond.notify()
        self.cond.release()


class Cow(threading.Thread):
    def __init__(self, cond):
        super().__init__(name='牛')
        self.cond = cond

    def run(self):
        global cows_list
        global i

        # 线程挂起，等待被唤醒
        self.cond.acquire()
        self.cond.wait()

        while (True):
            # 当所有牛都成熟了，就结束循环
            if min(cows_list) >= 5:
                break

            # 随机选取一头牛
            i = random.randint(0, len(cows_list) - 1)
            # 如果该牛已经成熟，则换一只牛
            while (cows_list[i] >= 5):
                i = random.randint(0, len(cows_list) - 1)
            # 小牛成长值加1
            cows_list[i] += 1

            # 挂起小牛线程，唤醒小草进程
            self.cond.notify()
            self.cond.wait()

        # 释放锁
        self.cond.release()


def main():
    path = 'recording.txt'
    # 创建牛列表
    global cows_list
    # 用于记录哪只牛吃了草
    global i

    cows_list = [0] * 10  # 达到5的时候表示成熟

    cond = threading.Condition()
    grass = Grass(cond)
    cow = Cow(cond)

    cow.start()
    grass.start()

    with open(path, 'a') as f:

        # 直到每头牛都成熟了，就退出循环
        while(min(cows_list) < 5):
            time.sleep(1)
            print('--' * 15)
            print('新的一天开始了。')
            f.write('--------------------------------------------\n')
            f.write('新的一天开始了。\n')
            f.flush()

            # 获取天气
            weather = Weather()

            # 如果今天下雨了，小草就长大一点
            if weather.rain:
                grass.grow()
                print('今天下雨了，小草长大了一点。成长值变为了 %d 。' % grass.get_growth())
                f.write('今天下雨了，小草长大了一点。成长值变为了 %d 。\n' % grass.get_growth())
                f.flush()
            else:
                print('今天是晴天。')
                f.write('今天是晴天。\n')
                f.flush()

            # 判断小草是否成熟了
            if grass.mature():
                # 获取锁
                grass.cond.acquire()
                cow.cond.acquire()

                print('小草已经成熟了。小牛可以吃草了。')
                f.write('小草已经成熟了。小牛可以吃草了。\n')

                # 小草线程挂起，唤醒小牛进程
                grass.cond.notify()
                grass.cond.wait()

                # 释放锁
                grass.cond.release()
                cow.cond.release()

                print('小牛 %d 号吃了草，成长值变为了 %d 。' % (i + 1, cows_list[i]))
                print('草被牛吃光了.')
                f.write('小牛 %d 号吃了草，成长值变为了 %d 。\n' % (i + 1, cows_list[i]))
                f.write('草被牛吃光了.\n')
                grass.eaten()

                f.flush()

        print('小牛们都变成老牛了。')
        f.write('小牛们都变成老牛了。\n')
        f.flush()


if __name__ == '__main__':
    main()
