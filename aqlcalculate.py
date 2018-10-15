"""
版本：3.0
日期：20181013
作者：sky
作用：计算空气质量分指数
"""
import json
import csv
import os


def cal_linear(iaqi_low, iaqi_high, bp_lo, bp_hi, cp):
    iaqi=(iaqi_high-iaqi_low)*(cp-bp_lo)/(bp_hi-bp_lo)+iaqi_low
    return iaqi

def cal_pm_iaqi(pm):
    if 0 <= pm < 35:
        iaqi = cal_linear(0, 50, 0, 35, pm)
    elif 36 <= pm <76:
        iaqi = cal_linear(50, 100, 35, 75, pm)
    elif 76 <= pm <116:
        iaqi = cal_linear(100, 150, 75, 115, pm)
    else:
        iaqi = 0

    return iaqi

def cal_co_iaqi(co):
    if 0 <= co < 3:
        iaqi = cal_linear(0, 50, 0, 3, co)
    elif 3 <= co < 5:
        iaqi = cal_linear(50, 100, 2, 4, co)
    else:
        iaqi = 0

    return iaqi

def cal_aqi(pm):
    '''aqi计算'''
    pm_val=pm[0]
    co_val=pm[1]

    pm_iaqi = cal_pm_iaqi(pm_val)
    co_iaqi = cal_co_iaqi(co_val)

    iaqi_list = []
    iaqi_list.append(pm_iaqi)
    iaqi_list.append(co_iaqi)

    aqi = max(iaqi_list)
    return aqi

def jiema_json(l):
    with open(l, mode='r', encoding='utf-8') as f:
        slist = json.load(f)
    return slist

def jiema_csv(l):
    with open(l, mode='r', encoding='utf-8') as f:
        scsv = csv.reader(f)
        for  row in scsv:
            print(', '.join(row))


def main():
    input_str = input('请输入（1）PM2.5（2）CO的监测值为：')
    str_list = input_str.split(' ')
    pm_str = float(str_list[0])
    co_str = float(str_list[1])
    param_list = []
    param_list.append(pm_str)
    param_list.append(co_str)

    #计算
    aqi = cal_aqi(param_list)

    print('空气质量指数为：{}'.format(aqi))

    list1 = jiema_json('beijing_aqi.json')
    list2 = jiema_json('shanghai_aqi.json')
    clist = list1+list2
    clist.sort(key=lambda city: city['aqi'])
    top5 = clist[:5]
    f = open('top5_aqi.json', mode='w', encoding='utf-8')
    json.dump(top5, f, ensure_ascii=False)
    f.close()

    lines=[]
    lines.append(list(clist[0].keys()))
    for city in clist:
        lines.append(list(city.values()))

    f2=open('aqi.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(f2)
    for line in lines:
        writer.writerow(line)
    f2.close()

    filepath=input('请输入文件名：')
    filename,fileext=os.path.split(filepath)
    if fileext == '.json':
        jiema_json(filepath)
    elif fileext == '.csv':
        jiema_csv(filepath)
    else:
        pass

if __name__ == '__main__':
    main()