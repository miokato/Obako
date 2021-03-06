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

    def talk(self, prediction):
        sents = list()
        for i, j in zip(self.dic['akita'], self.dic['standard']):
            s = i + ' (' + j + ')'
            sents.append(s)

        #sents = list(self.dic['akita'])
        sent = sents[randint(0, len(self.dic)-1)]
        return sent


class Morning(Mode):
    def __init__(self, controller, dic):
        self.name = 'morning'
        self.controller = controller
        self.dic = dic.query("state=='morning'")

    def to_morning(self):
        self.controller.state = self.controller.morning

    def to_lunch(self):
        self.controller.state = self.controller.runch

    def to_evening(self):
        self.controller.state = self.controller.evening

    def to_afterfive(self):
        self.controller.state = self.controller.afterfive

    def to_midnight(self):
        self.controller.state = self.controller.midnight


class Lunch(Mode):
    def __init__(self, controller, dic):
        self.name = 'lunch'
        self.controller = controller
        self.dic = dic.query("state=='morning'")

    def to_morning(self):
        self.controller.state = self.controller.morning

    def to_lunch(self):
        self.controller.state = self.controller.runch

    def to_evening(self):
        self.controller.state = self.controller.evening

    def to_afterfive(self):
        self.controller.state = self.controller.afterfive

    def to_midnight(self):
        self.controller.state = self.controller.midnight


class Evening(Mode):
    def __init__(self, controller, dic):
        self.name = 'evening'
        self.controller = controller
        self.dic = dic.query("state=='evening'")

    def to_morning(self):
        self.controller.state = self.controller.morning

    def to_lunch(self):
        self.controller.state = self.controller.runch

    def to_evening(self):
        self.controller.state = self.controller.evening

    def to_afterfive(self):
        self.controller.state = self.controller.afterfive

    def to_midnight(self):
        self.controller.state = self.controller.midnight


class AfterFive(Mode):
    def __init__(self, controller, dic):
        self.name = 'afterfive'
        self.controller = controller
        self.dic = dic.query("state=='friday'")

    def to_morning(self):
        self.controller.state = self.controller.morning

    def to_lunch(self):
        self.controller.state = self.controller.runch

    def to_evening(self):
        self.controller.state = self.controller.evening

    def to_afterfive(self):
        self.controller.state = self.controller.afterfive

    def to_midnight(self):
        self.controller.state = self.controller.midnight


class MidNight(Mode):
    def __init__(self, controller, dic):
        self.name = 'midnight'
        self.controller = controller
        self.dic = dic

    def to_morning(self):
        self.controller.state = self.controller.morning

    def to_lunch(self):
        self.controller.state = self.controller.runch

    def to_evening(self):
        self.controller.state = self.controller.evening

    def to_afterfive(self):
        self.controller.state = self.controller.afterfive

    def to_midnight(self):
        self.controller.state = self.controller.midnight


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

    def talk(self, prediction):
        sent = self.state.talk(prediction)
        return sent


class Parser(object):
    def __init__(self):
        path = 'obako_app/data/word.csv'
        df = pd.read_csv(path, index_col=0)
        self.dic = df.set_index(df['word']).to_dict(orient='index')

        pattern = r'。|？'
        self.patter = re.compile(pattern)

    def parse(self, message):
        results = dict()
        sents = self.patter.split(message)
        sents = [s for s in sents if len(s) > 1]
        for sent in sents:
            for k, v in self.dic.items():
                if k in sent:
                    results[k] = v

        return results


class Predictor(object):
    def __init__(self):
        pass

    def predict(self, mes):
        return mes


class Concierge(object):
    def __init__(self):
        self.parser = Parser()
        self.predictor = Predictor()
        self.controller = TalkController()

    def talk(self, raw_message):
        # メッセージを解析、メッセージオブジェクトを返す
        parsed_mes = self.parser.parse(raw_message)
        # メッセージの内容から返信オブジェクトを作成し返す
        prediction = self.predictor.predict(parsed_mes)
        # 時間帯によりコントローラーの状態を変更
        self.controller.change_state()
        # 返信オブジェクトをコントローラに渡し、返信内容を決定
        res = self.controller.talk(prediction)
        # 返信文を返す
        return res


if __name__ == '__main__':
    mes = 'おはよう。今日もいい天気だね'
    parser = Parser()
    sents = parser.parse(mes)
    print(sents)







