import threading
import time
import random


class Weather:
    def __init__(self):
        self.rain = self.__get_weather()

    def __get_weather(self):
        return random.randint(1, 10) <= 2


class Grass(threading.Thread):
    def __init__(self, cond, filepath):
        super().__init__(name='小草')
        self.__growth = 0  # 当growth达到3的时候表示成熟
        self.cond = cond
        self.filepath = filepath

    def grow(self):
        self.__growth += 1
        print('草长大了一点，成长值为 %d 。' % self.__growth)
        self.write_recording('草长大了一点，成长值为 %d 。' % self.__growth)

    def mature(self):
        return self.__growth >= 3

    def write_recording(self, content):
        with open(self.filepath, 'a') as f:
            f.write(content + '\n')

    def run(self):
        global cows_list
        self.cond.acquire()

        while(True):
            time.sleep(1)
            # 当所有牛都成熟了，就结束循环
            if min(cows_list) >= 5:
                break

            print("--" * 15)
            print("新的一天开始了。")
            self.write_recording("--" * 15)
            self.write_recording("新的一天开始了。")

            weather = Weather()
            if weather.rain:
                print('今天下雨了。')
                self.write_recording('今天下雨了。')
                self.grow()
            else:
                print('今天是晴天。')
                self.write_recording('今天是晴天。')

            if self.mature():
                print("草已经长大了，牛可以吃草了。")
                self.write_recording("草已经长大了，牛可以吃草了。")
                self.cond.notify()
                self.cond.wait()

                self.__growth = 0
                print("草被牛吃光了。")
                self.write_recording("草被牛吃光了。")

        self.cond.notify()
        self.cond.release()


class Cow(threading.Thread):
    def __init__(self, cond, filepath):
        super().__init__(name='牛')
        self.cond = cond
        self.filepath = filepath

    def write_recording(self, content):
        with open(self.filepath, 'a') as f:
            f.write(content + '\n')

    def run(self):
        global cows_list
        self.cond.acquire()
        # 休眠，等待被草唤醒
        self.cond.wait()

        while (True):
            # 当所有牛都成熟了，就结束循环
            if min(cows_list) >= 5:
                break

            # 随机选取一头牛
            i = random.randint(0, len(cows_list) - 1)
            while (cows_list[i] >= 5):
                i = random.randint(0, len(cows_list))
            cows_list[i] += 1
            print('小牛 %d 号吃了草，成长值变为了 %d 。' % (i+1, cows_list[i]))
            self.write_recording('小牛 %d 号吃了草，成长值变为了 %d 。' % (i+1, cows_list[i]))
            self.cond.notify()
            self.cond.wait()

        print('--' * 15)
        print('喂养结束。')
        print("小牛们都变成老牛了。")
        self.write_recording('--------------------------------\n')
        self.write_recording('喂养结束。\n')
        self.write_recording('小牛们都变成老牛了。\n')
        self.cond.notify()
        self.cond.release()


def main():
    path = 'recording.txt'
    global cows_list
    cows_list = [0] * 10  # 达到5的时候表示成熟

    cond = threading.Condition()
    grass = Grass(cond, path)
    cow = Cow(cond, path)

    cow.start()
    grass.start()

    cow.join()
    grass.join()


if __name__ == '__main__':
    main()
