import pandas as pd
import re
from _datetime import datetime
from random import randint


def time_zone():
    hour = datetime.now().hour
    if 6 <= hour <= 11:
        return 'morning'
    elif 11 < hour <= 13:
        return 'lunch'
    elif 13 < hour <= 23:
        return 'evening'
    elif 23 < hour <= 24:
        return 'afterfive'
    else:
        return 'midnight'


class Mode(object):

    def talk(self):
        sents = list(self.dic['akita'])
        sent = sents[randint(0, len(self.dic)-1)]
        return sent


class Morning(Mode):
    def __init__(self, controller, dic):
        self.name = 'morning'
        self.controller = controller
        self.dic = dic.query("state=='morning'")

    def to_morning(self):
        controller.state = controller.morning

    def to_lunch(self):
        controller.state = controller.lunch

    def to_evening(self):
        controller.state = controller.evening

    def to_afterfive(self):
        controller.state = controller.afterfive

    def to_midnight(self):
        controller.state = controller.midnight


class Lunch(Mode):
    def __init__(self, controller, dic):
        self.name = 'lunch'
        self.controller = controller
        self.dic = dic.query("state=='morning'")

    def to_morning(self):
        controller.state = controller.morning

    def to_lunch(self):
        controller.state = controller.lunch

    def to_evening(self):
        controller.state = controller.evening

    def to_afterfive(self):
        controller.state = controller.afterfive

    def to_midnight(self):
        controller.state = controller.midnight


class Evening(Mode):
    def __init__(self, controller, dic):
        self.name = 'evening'
        self.controller = controller
        self.dic = dic.query("state=='evening'")

    def to_morning(self):
        controller.state = controller.morning

    def to_lunch(self):
        controller.state = controller.lunch

    def to_evening(self):
        controller.state = controller.evening

    def to_afterfive(self):
        controller.state = controller.afterfive

    def to_midnight(self):
        controller.state = controller.midnight


class AfterFive(Mode):
    def __init__(self, controller, dic):
        self.name = 'afterfive'
        self.controller = controller
        self.dic = dic.query("state=='friday'")

    def to_morning(self):
        controller.state = controller.morning

    def to_lunch(self):
        controller.state = controller.lunch

    def to_evening(self):
        controller.state = controller.evening

    def to_afterfive(self):
        controller.state = controller.afterfive

    def to_midnight(self):
        controller.state = controller.midnight


class MidNight(Mode):
    def __init__(self, controller, dic):
        self.name = 'midnight'
        self.controller = controller
        self.dic = dic

    def to_morning(self):
        controller.state = controller.morning

    def to_lunch(self):
        controller.state = controller.lunch

    def to_evening(self):
        controller.state = controller.evening

    def to_afterfive(self):
        controller.state = controller.afterfive

    def to_midnight(self):
        controller.state = controller.midnight


class TalkController(object):
    def __init__(self):
        path = 'obako_app/data/akitaben.csv'
        dic = pd.read_csv(path, index_col=0)

        self.morning = Morning(self, dic)
        self.lunch = Lunch(self, dic)
        self.evening = Evening(self, dic)
        self.afterfive = AfterFive(self, dic)
        self.midnight = MidNight(self, dic)
        self.state = self.morning

    def change_state(self):
        zone = time_zone()
        if zone == 'morning':
            self.state.to_morning()
        elif zone == 'lunch':
            self.state.to_lunch()
        elif zone == 'evening':
            self.state.to_evening()
        elif zone == 'afterfive':
            self.state.to_afterfive()
        elif zone == 'midnight':
            self.state.to_midnight()

    def talk(self):
        sent = self.state.talk()
        return sent


class Concierge(object):
    def __init__(self):
        # self.parser = Parser()
        self.controller = TalkController()

    def talk(self):
        # とりあえず現状は時間帯でランダムな答えを返す。今後はクエリをパースして、適当な返答を返す。
        self.controller.change_state()
        res = self.controller.talk()

        return res

def csv_to_dic(path):
    df = pd.read_csv(path, index_col=0)
    dic = {}
    for k, a, s in zip(df['state'], df['akita'], df['standard']):
        dic[k] = (a, s)

    return dic


class Parser(object):
    def __init__(self, dic):
        self.dic = dic

    def parse(self, sentence):
        for standard, akita in self.dic.items():
            sentence = re.sub(standard, akita, sentence)

        return sentence


if __name__ == '__main__':
    controller = TalkController()
    controller.change_state()
    print(controller.talk())

    concierge = Concierge()
    print(concierge.talk())

    # print(translate('不細工な娘と肉鍋料理食べに行ったよ'))






