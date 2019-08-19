import random
from functools import wraps

class CardPool():
	def __init__(self):
		self.pool = self.__init_pool()
		self.card_map = self.__init_map()
		self.left_num = 4 * 13

	def __init_pool(self):
		pool = list()

		card_type = ['梅花', '方块', '黑桃', '红桃']
		for each_type in card_type:
			for i in range(13):
				if i == 0 :
					pool.append(each_type + 'A')
				elif i < 10:
					pool.append(each_type + str(i+1))
				elif i == 10:
					pool.append(each_type + 'J')
				elif i == 11:
					pool.append(each_type + 'Q')
				else:
					pool.append(each_type + 'K')

		random.shuffle(pool)
		return pool


	def __init_map(self):
		card_map = dict()

		#生成一个卡牌的对应图，记录卡池中剩余卡组里的各点数的张数
		#其中1点和13点都表示A， 因为10,J,Q,K都是10点，所以10点应该有16张
		for i in range(1,12):
			if i == 10:
				card_map[i] = 4 * 4
			else:
				card_map[i] = 4

		return card_map


	def give_one_card(self):
		#从卡池中抽取一张卡
		card = self.pool.pop(random.randint(1, len(self.pool)-1))

		#从map中减少一张对应点数的卡牌数量
		if card[-1] == 'A':
			self.card_map[1] -= 1
			self.card_map[11] -= 1

		elif card[-1] in ['0', 'J', 'Q', 'K']:
			self.card_map[10] -= 1

		else:
			self.card_map[int(card[-1])] -= 1

		#卡牌数量减少
		self.left_num -= 1

		return card


class Player():
	def __init__(self,max_hand_card=5):
		self.__max_hand_card = max_hand_card
		self.hand_card_list = list()
		self.__hand_card_num = 0
		self.score = 0


	def __count_hand_score(self):
		self.score = 0
		have_A = False

		for each_card in self.hand_card_list:

			if each_card[-1] in ['J', 'Q', 'K', '0']:
				self.score += 10
			elif each_card[-1] == 'A':
				self.score += 1
				have_A = True
			else:
				self.score += int(each_card[-1])

		if have_A and self.score < 12:
			self.score += 10


	def get_init_cards(self, cardpool, num=2):
		#抽牌
		for i in range(num):
			self.hand_card_list.append(cardpool.give_one_card())
		self.__hand_card_num += num

		#计算手牌分数
		self.__count_hand_score()


	def get_one_card(self, cardpool):
		if self.__hand_card_num == self.__max_hand_card:
			print("手牌已经达到上限，无法继续叫牌")
			return

		#抽牌
		self.hand_card_list.append(cardpool.give_one_card())
		self.__hand_card_num += 1

		#计算手牌分数
		self.__count_hand_score()


	def get_hand_card_num(self):
		return self.__hand_card_num


	def clean_hand_card(self):
		self.hand_card_list = list()
		self.score = 0
		self.__hand_card_num = 0


class Banker(Player):
	def __init__(self):
		super(Banker, self).__init__()


	def __calc_posibility(self, player_score, cardpool):
		delta = player_score - self.score
		win_or_equal_count = 0

		#如果庄家自身点数小于11点，则抽到A算作11点，因此需要统计2-11点中符合条件的数量。
		#如果要统计获胜或者平局的话，那所需要的点数的 最小值应该是与max(2,玩家点数的差值)，最大值应该是与min(11,21点的差值)
		if self.score < 11 :
			for i in range(max(2,delta), min(11,21 - self.score) + 1):
				win_or_equal_count += cardpool.card_map[i]

		#如果庄家自身点数大于等于11点，则抽到的A算作1点，因此需要统计1-10点中符合条件的数量。
		#如果要统计获胜或者平局的话，那所需要的点数的 最小值应该是与玩家点数的差值，最大值应该是与21点的差值并且这个差值不可能超过10
		else:
			for i in range(delta, 21 - self.score + 1):
				win_or_equal_count += cardpool.card_map[i]

		return win_or_equal_count / cardpool.left_num

	def get_cards(self, player_score, cardpool):
		if self.score < player_score:
			#两种情况下继续抽牌
			#先判断如果庄家点数比玩家点数小11点或者11点以上的话，则不需要计算可能性，直接抽牌
			#再判断继续抽牌获胜或者平局的可能性大于30%时，继续抽牌。
			if player_score - self.score > 10 or self.__calc_posibility(player_score, cardpool) > 0.3:
				self.get_one_card(cardpool)
				self.get_cards(player_score, cardpool)


def continue_decorator(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if_continue = func(*args, **kwargs)
		if if_continue.upper() == 'Y':
			return True
		elif if_continue.upper() == 'N':
			return False
		else:
			print("输入错误，请重新输入")
			return wrapper(*args, **kwargs)
	return wrapper


@continue_decorator
def continue_game():
	return input("是否继续进行下一轮游戏? >>>>> (Y/N) ")


@continue_decorator
def cotinue_get_card():
	return input("是否继续叫牌? >>>>> (Y/N) ")


def every_round(cards, banker, player):
	#庄家和玩家先抽取两张牌
	banker.get_init_cards(cards)
	player.get_init_cards(cards)

	#打印目前双方的手牌
	print("庄家目前的手牌为 >>> [*, '%s']" % banker.hand_card_list[1])
	print("你目前的手牌为 >>>>> {}".format(player.hand_card_list))

	#玩家叫牌
	print("玩家正在进行叫牌...")
	while(player.get_hand_card_num() < 5):
		if_next_card = cotinue_get_card()
		if not if_next_card:
			break
		player.get_one_card(cards)
		print("你目前的手牌为 >>>>> {}".format(player.hand_card_list))

		#检测玩家点数是否超过21点
		if player.score > 21:
			print("玩家点数超过21点，本回合游戏结束。")
			print("庄家获胜。")
			return -1

	print("玩家叫牌结束，轮到庄家进行叫牌。")

	#庄家叫牌
	print("庄家正在进行叫牌..")
	banker.get_cards(player.score, cards)

	#检测庄家点数是否超过21点
	if banker.score > 21:
		print("庄家点数超过21点，本回合游戏结束。")
		print("玩家获胜。")
		return 1

	print("庄家叫牌结束。")

	#判定结果
	if banker.score == player.score:
		print("平局。")
		return 0
	elif banker.score < player.score:
		print("玩家获胜。")
		return 1
	else:
		print("庄家获胜。")
		return -1


def main():
	input("按Enter键开始游戏。")

	#初始化游戏
	cards = CardPool()
	banker = Banker()
	player = Player()
	total_score = [0, 0]
	game_round = 0

	#进入每一局游戏
	if_next_round = True
	while (if_next_round):
		print("-"*30)
		#初始化每回合参数
		game_round += 1

		#清理手牌
		banker.clean_hand_card()
		player.clean_hand_card()

		print("第%d回合开始。" % game_round)

		#如果卡池内的卡数量少于15张，则重新进行洗牌
		if cards.left_num < 15:
			print("剩余扑克牌数量少于15张，正在进行重新洗牌。")
			cards = CardPool()
			print("重新洗牌完成，游戏继续。")

		#进行游戏，并返回游戏结果
		result = every_round(cards,banker,player)
		total_score[result == 1] = total_score[result == 1] + 1 if result != 0 else total_score[result == 1]

		#打印本回合最终手牌
		print("庄家的手牌为 >>>  {}".format(banker.hand_card_list))
		print("你的手牌为 >>>>>  {}".format(player.hand_card_list))
		print('目前的比分是>>>>> 庄家 %d - %d 玩家' % (total_score[0], total_score[1]))

		if_next_round = continue_game()


	print("游戏结束。")


# def unit_test():
# 	player = Player()
# 	print(player.count_test(['方块A', '方块3', '方块K']))


if __name__ == '__main__':
	#unit_test()
	main()