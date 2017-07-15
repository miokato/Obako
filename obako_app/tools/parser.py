import pandas as pd


def csv_to_dic(path):
    df = pd.read_csv(path, index_col=0)
    dic = {}
    for k, v in zip(df['standard'], df['akita']):
        dic[k] = v

    return dic


class Parser(object):
    def __init__(self, dic):
        self.dic = dic

    def parse(self, s_text):
        parsed = self.dic[s_text]
        return parsed


def translate(text):
    path = 'obako_app/data/akitaben.csv'
    dic = csv_to_dic(path)

    parser = Parser(dic)
    akitaben = parser.parse(text)
    #print('standard : {} -> akita : {}'.format(text, akitaben))
    return akitaben


if __name__ == '__main__':
    print(translate('娘'))






