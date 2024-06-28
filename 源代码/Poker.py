import random
"""
1. 扑克游戏: 简单起见, 扑克只有52张牌(没有大小王), 需要将52张牌发到4个玩家的手上
            每个玩家手上有13张牌, 按照黑桃、红心、草花、方块的顺序和点数从小到大排列。
2. 在上面代码的基础上实现了一个简单的扑克游戏: 21点游戏 (Black Jack)
            备注: 21点游戏部分借鉴参考了CSDN上的一篇文章(https://blog.csdn.net/Zhangguohao666/article/details/103948545)
                  原文是用函数的形式实现了21点游戏, 而我将原文的功能以类(Blackjack)的形式进行了封装
                  此外, 在实现Blackjack类中, 继承了已有的PokerGame类中的一部分属性和方法, 尽可能实现了代码复用
:Author: 李振荣
:Version: V1.0.1
"""


class Face:
    """
    定义牌面类, 表示扑克牌的基本属性
    suits: 所有的花色，取值范围为 "♠", "♥", "♣", "♦"。
    ranks: 所有的点数，取值范围为 2-10, "J", "Q", "K", "A"。
    """
    suits = ["♠", "♥", "♣", "♦"]                 #按照黑桃、红心、草花、方块的顺序
    ranks = ["A", "2", "3", "4","5", "6", "7", "8", "9", "10", "J", "Q", "K"]  #按点数的数值大小顺序


class Card:
    """
    定义牌类, 表示一张扑克牌
    即由牌面类(Face)里的花色(suit)和(点数)构成一张牌
    suit: 花色
    rank: 点数
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return f'{self.suit}{self.rank}'

#测试一张牌
#card_test = Card(Face.suits[1],Face.ranks[1])        
#print(card_test)


class PokerGame:
    """
    定义扑克游戏类, 包含进行一次扑克牌游戏的方法
    cards: 初始化一副牌
    current: 每次发牌时最上面的一张牌 
    """

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Face.suits for rank in Face.ranks]
        self.current = 0
    
    def shuffle(self):
        """洗牌"""
        random.shuffle(self.cards)
        self.current = 0

    def deal(self):
        """发牌"""
        card = self.cards[self.current]
        self.current += 1
        return card
    
    def receive(self, players):
        """用户获得牌"""
        for _ in range(13):
            for player in players:
                player.receive_card(self.deal())
            
#测试洗牌功能
#game_test = PorkerGame()
#game_test.shuffle()
#print(game_test.cards)


class Player:
    """
    定义玩家类, 包含玩家的属性以及一些方法
    name: 玩家姓名
    cards: 玩家的手牌
    """
    def __init__(self, name):
        self.name = name
        self.cards = []

    def receive_card(self, card):
        """摸到一张牌"""
        self.cards.append(card)

    def hand_sort(self):
        """用户手牌排序"""   
        # 按照黑桃、红心、草花、方块的顺序和点数从小到大排列
        self.cards.sort( key = lambda card: (Face.suits.index(card.suit), Face.ranks.index(card.rank)) )


class Blackjack(PokerGame):
        """
        21点扑克牌游戏 (人机对战)
        电脑为庄家, 用户为玩家
        本类继承了PokerGame类的一些属性和方法
        house: 电脑(庄家)的手牌
        user: 用户(玩家)的手牌

        """
        def __init__(self):
            super().__init__()       #继承PokerGame类的构造
            PokerGame.shuffle(self)  #使用PokerGame类的shuffle(洗牌)方法
            self.deck = self.cards   #继承PokerGame类中的属性cards (一副洗好的牌)
            #上面三行代码实现了在Blackjack类中得到一副随机的牌组

            self.house = []
            self.user = []

        def calculate(self, hand):
            """计算并返回一手牌的点数和"""
            values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}
            result = 0 #初始化点数和为0
            numAces = 0 #A的个数

            # 计算点数和A的个数
            for card in hand:
                result += values[card.rank]
            if card.rank == 'A':
                numAces += 1
    
            # 如果点数和>21，则尝试把A当做1来计算
            # (即减去10)，多个A循环减去10，直到点数<=21
            while result > 21 and numAces > 0:
                result -= 10
                numAces -= 1
            return result

        def start(self):
            """开始进行21点(blackjack)游戏"""
            
            # 依次给玩家和庄家各发两张牌
            for i in range(2):
                self.house.append(PokerGame.deal(self))
                self.user.append(PokerGame.deal(self))
            # 打印手牌
            print('电脑的牌：', end = ''); print(self.house)
            print('用户的牌：', end = ''); print(self.user)
            
            # 询问玩家（用户）是否继续拿牌，如果是，继续给玩家发牌
            answer = input('您是否选择继续拿牌（y/n，缺省为y）：')
            while answer in ('', 'y', 'Y'):
                self.user.append(PokerGame.deal(self))
                print('用户拿到的牌为：', end = ''); print(self.user)
                 # 计算牌点
                if self.calculate(self.user) > 21:
                    print('LOSE  用户失败!')
                    return
                answer = input('您是否选择继续拿牌（y/n，缺省为y）：')
        
            # 庄家(电脑)按“庄家规则”确定是否拿牌
            while self.calculate(self.house) < 17:
                self.house.append(PokerGame.deal(self))
                print('电脑拿到的牌为：', end =''); print(self.house)
                # 计算牌点
                if self.calculate(self.house) > 21:
                    print('WIN  用户获胜!')
                    return

            # 当庄家（电脑）和玩家（用户）均停牌，即按照各自的选择或者机制不再要牌时
            # 分别计算庄家（电脑）和玩家（用户）的点数，比较点数大小，输出输赢结果信息
            houseTotal, userTotal = self.calculate(self.house), self.calculate(self.user)
            if houseTotal > userTotal:
                print('电脑获胜!')
            elif houseTotal < userTotal:
                print('用户获胜!')
            elif houseTotal == 21 and 2 == len(self.house) < len(self.user) : # 拥有blackjack的庄家赢牌
                print('电脑获胜!')
            elif userTotal == 21 and 2 == len(self.user) < len(self.house) : # 拥有blackjack的玩家赢牌
                print('用户获胜!')
            else:
                print('平局！')



if __name__ == '__main__':
    
    """
    # 测试发牌和手牌排序
    game1 = PokerGame()
    game1.shuffle()
    players = [Player('张三'), Player('李四'), Player('王五'), Player('赵六')]
    game1.receive(players)
    for player in players:
        player.hand_sort()
        print(f'{player.name}: ', end='')
        print(player.cards)
    """

    # 如果要测试发牌效果, 建议先注释掉下面两行代码, 然后解除上方代码的注释 
    game2 = Blackjack()
    game2.start()


    