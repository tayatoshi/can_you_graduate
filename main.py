# coding: utf-8
'''
====14学則用====
・使用する際は自己責任でお願いします。信用できない方は使用しないことをお勧めします。
・コードが汚いなどの苦情は受け付けませんし、傷つくのでSNSにも書かないでください。
・ただし賛辞と優しいコードレビューはお受けいたします
'''

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print('成績のcsvファイル名を入力:',end='')
file_name = str(input())
data = pd.read_csv(file_name)
sum_tanni = data[data.isnull().sum(axis=1)==6]
data = data.fillna(False)
conki = data[data['評語']=='？']
sum_tanni = sum_tanni.dropna(axis=1)
sum_tanni.columns = ['科目名称','合計単位']
data = sum_tanni
concat_data = pd.concat([data,conki[['科目名称','単位']]]).sort_index().reset_index(drop=True).fillna(False)

for i in data['合計単位'].index:
    #単位の数字だけ抽出
    tanni = data['合計単位'][i].split('.')[0].split(' ')[1]
    data['合計単位'][i] = int(tanni)
    #科目名称を見やすくしてるだけ
    data['科目名称'][i] = data['科目名称'][i].split(' ')[1:]


def tanni(trace=False):
    tokusetu ,tagakubu, free, kibann, sentan,sotupro, zemi, adj_sum= 0,0,0,0,0,0,0,0
    for i in data.index:
        # 自由単位
        if '自由科目' in data['科目名称'][i]:
            free = free + data['合計単位'][i]
        # 他学部設置科目
        elif '他学部等設置科目' in data['科目名称'][i]:
            tagakubu = tagakubu + data['合計単位'][i]
        # 特設科目
        elif '特設科目' in data['科目名称'][i]:
            tokusetu = tokusetu + data['合計単位'][i]
        # 基盤科目
        elif '基盤科目' in data['科目名称'][i]:
            kibann = kibann + data['合計単位'][i]
        # 先端科目
        elif '先端科目' in data['科目名称'][i]:
            sentan = sentan + data['合計単位'][i]
        # 先端科目
        elif '研究会' in data['科目名称'][i]:
            zemi = zemi + data['合計単位'][i]
        # 卒業プロジェクト
        elif '卒業プロジェクト' in data['科目名称'][i]:
            sotupro = sotupro + data['合計単位'][i]
        adj_sum = data['合計単位'].sum() - free
        #他学部は60以下、特設は20以下、自由は除く
        if tagakubu>60:
            too = tagakubu - 60
            adj_sum = adj_sum - too
        if tokusetu>20:
            too = tokusetu - 20
            adj_sum = adj_sum - too

    if trace == True:
        print()
        print('自由科目：{}'.format(free))
        print('他学部等設置科目：{}'.format(tagakubu))
        print('特設科目：{}'.format(tokusetu))
        print('先端科目：{}'.format(sentan))
        print('研究会：{}'.format(zemi))
        print('卒業プロジェクト：{}'.format(sotupro))
        print('要件単位：{}'.format(adj_sum))
        print()

    return {'adj_sum':adj_sum, 'sentan':sentan,'sotupro':sotupro,'zemi':zemi}

def for_grad(result,konki=False):
    # 124単位以上
    # 先端科目30単位以上
    # 研究会2単位以上
    # 卒プロ1,2履修
    tani_result = False
    sentan_result = False
    zemi_result = False
    sotupro1_result = False
    sotupro2_result = False

    if result['adj_sum'] >=124:
        tani_result = True
    if result['sentan'] >=30:
        sentan_result = True
    if result['zemi'] >=2:
        zemi_result = True
    if result['sotupro'] == 2:
        sotupro1_result = True
    if result['sotupro'] == 4:
        sotupro2_result = True

    print('========14学則卒業要件========')
    print('124単位以上       ：{}'.format(tani_result))
    print('先端科目30単位以上：{}'.format(sentan_result))
    print('研究会2単位以上   ：{}'.format(zemi_result))
    print('卒プロ1履修       ：{}'.format(sotupro1_result))
    print('卒プロ2履修       ：{}'.format(sotupro2_result))
    print('==============================')
    print('卒業要件単位 ：{}単位'.format(result['adj_sum']))
    if 124-result['adj_sum'] <= 0:
        print('単位数は十分。すごい。うらやましい。')
    else:
        print('残り {} 単位'.format(124-result['adj_sum']))
    if konki == True:
        K = get_konki(concat_data)
        if result['adj_sum'] + K['all'] - K['free']>=124:
            tani_result = True
        if result['sentan'] + K['sentan'] >=30:
            sentan_result = True
        if result['zemi'] + K['zemi'] >=2:
            zemi_result = True
        if result['sotupro'] + K['sotupro'] == 2:
            sotupro1_result = True
        if result['sotupro'] + K['sotupro'] == 4:
            sotupro2_result = True
        print('                ')
        print('今期全ての単位が取れた場合')
        print('========14学則卒業要件========')
        print('124単位以上       ：{}'.format(tani_result))
        print('先端科目30単位以上：{}'.format(sentan_result))
        print('研究会2単位以上   ：{}'.format(zemi_result))
        print('卒プロ1履修       ：{}'.format(sotupro1_result))
        print('卒プロ2履修       ：{}'.format(sotupro2_result))
        print('==============================')
        print('卒業要件単位 ：{}単位'.format(result['adj_sum']+K['all']-K['free']))
        if 124-result['adj_sum']-K['all'] + K['free'] <= 0:
            print('単位数は十分。すごい。うらやましい。')
        else:
            print('残り {} 単位'.format(124-result['adj_sum']-K['all']+K['free']))

def get_konki(arg):
    konnki_tanni_index = list(arg[arg['単位']!=False].index)
    konnki_tanni_class = [i-1 for i in konnki_tanni_index if i-1 not in konnki_tanni_index]
    conki_INDEX=list(set(konnki_tanni_index + konnki_tanni_class))
    conki_INDEX.sort()
    konki_data = arg.iloc[conki_INDEX,:]
    conki_if_all = int(konki_data['単位'].sum())
    for i in konnki_tanni_class:
        if konki_data['単位'][i] == False:
            konki_data['科目名称'][i] = konki_data['科目名称'][i].split(' ')[1:]
    kamoku = None
    for i in conki_INDEX:
        if konki_data['単位'][i] == False:
            kamoku = konki_data['科目名称'][i]
        else:
            konki_data['科目名称'][i]=kamoku
    konki_data = konki_data[konki_data['単位']!=False]

    konki_sentan = 0
    konki_sotupro = 0
    konki_free = 0
    konki_tokusetu = 0
    konki_tagakubu = 0
    konki_zemi = 0
    for i in konki_data.index:
        if '特設科目' in konki_data['科目名称'][i]:
            konki_tokusetu = konki_tokusetu + konki_data['単位'][i]
        if '自由科目' in konki_data['科目名称'][i]:
            konki_free = konki_free + konki_data['単位'][i]
        if '他学部等設置科目' in konki_data['科目名称'][i]:
            konki_tagakubu = konki_tagakubu + konki_data['単位'][i]
        if '先端科目' in konki_data['科目名称'][i]:
            konki_sentan = konki_sentan + konki_data['単位'][i]
        if '卒業プロジェクト' in konki_data['科目名称'][i]:
            konki_sotupro = konki_sotupro + konki_data['単位'][i]
        if '研究会' in konki_data['科目名称'][i]:
            konki_zemi = konki_zemi + konki_data['単位'][i]
    return {'all':conki_if_all,'sentan':int(konki_sentan),'sotupro':int(konki_sotupro),'free':int(konki_free),\
            'tokusetu':int(konki_tokusetu),'tagakubu':int(konki_tagakubu),'zemi':int(konki_zemi)}

result = tanni(trace = True)
for_grad(result,konki = True)
