# -*- coding:utf-8 -*-

from math import modf
from lxml import etree
from json import dumps as dp
import timeout_decorator
import requests as req
import excuate
import time


types = {0: [""],
         1: ["火", [220, 55, 35]], 2: ["水", [45, 127, 240]], 3: ["草", [103, 191, 64]],
         4: ["电", [245, 180, 38]], 5: ["普通", [152, 143, 126]], 6: ["格斗", [141, 61, 43]],
         7: ["飞行", [134, 149, 237]], 8: ["虫", [153, 174, 25]], 9: ["毒", [159, 64, 143]],
         10: ["岩石", [170, 144, 70]], 11: ["地面", [197, 163, 71]], 12: ["钢", [152, 151, 178]],
         13: ["冰", [74, 189, 216]], 14: ["超能", [244, 86, 142]], 15: ["恶", [93, 70, 56]],
         16: ["幽灵", [77, 74, 160]], 17: ["龙", [100, 69, 217]], 18: ["妖精", [250, 127, 172]]
         }

eggs = ["", "怪兽", "水中1", "昆虫", "飞行", "陆上", "妖精", "植物", "人形",
        "水中3", "矿物", "不定性", "水中2", "百变怪", "飞龙", "未发现"]


@timeout_decorator.timeout(60)
def get_info(url):
    html = req.get(url)
    et = etree.HTML(html.text)
    script = et.xpath('//script/text()')
    with open('look.txt', 'w', encoding='utf-8') as f:
        script = script[0][1:].strip(' ')
        left = script.find("nat_id")
        right = script.find("galar_form")
        script = script[left - 2:right - 2] + '}'
        f.write(script)
    null = 'null'
    script = eval(script)

    dic = {
        '伽勒尔编号': script['galar_id'],
        '阿罗拉编号': script['alola_id'],
        '属性': [types[script['type']][0], types[script['type_b']][0]],
        '分类': script['category'] + '宝可梦',
        '中文名': script['name_zh'],
        '英文名': script['name_en'],
        '特性': [script['abilitya'], script['abilityb'], script['abilityc']],
        '捕获率': script['capture_rate'],
        '蛋组': [eggs[script['egg_group']], eggs[script['egg_group_b']]],
        '孵化周期': script['egg_cycle'],
        '种族值': {
            'HP': script['bs_hp'], '攻击': script['bs_atk'],
            '防御': script['bs_def'], '特攻': script['bs_spatk'],
            '特防': script['bs_spdef'], '速度': script['bs_spd']
        },
        '初始形态': {
            int(script['devolution']['nat_id']): script['devolution']['name']
        },
        '进化': {},
        '日文名': script['name_jp']
    }

    if script['type_b'] == 0:
        dic['属性'].pop()
    if script['egg_group_b'] == 0:
        dic['蛋组'].pop()

    while True:
        if not bool(script['evolve_chain']):    # 说明没有进化形态，直接跳出循环
            break
        if not bool(script['evolve_chain'][0]['chain']):    # 说明有且至少有一种[平级的]进化形态，没有再进一步的形态，把这一种及与其平级的宝可梦收下来
            x = {}
            for i in range(len(script['evolve_chain'])):
                if not bool(x.get(float(script['evolve_chain'][i]['approach']['0']) + 0.001)):  # 查询结果为空才能继续添加键值对
                    x = {float(script['evolve_chain'][i]['approach']['0']) + 0.001: [script['evolve_chain'][i]['approach']['name'],
                                                                                     script['evolve_chain'][i]['approach']['text']]}
                    dic['进化'].update(x)
                else:
                    x = {script['evolve_chain'][i]['approach']['0'] + 0.011: [script['evolve_chain'][i]['approach']['name'],
                                                                              script['evolve_chain'][i]['approach']['text']]}
                    dic['进化'].update(x)
            break
        else:   # 说明还有进化态，重复上面的部分代码，即获取下一级所有的形态，然后再获取下下一级所有的形态
            x = {}
            for i in range(len(script['evolve_chain'])):
                if not bool(x.get(float(script['evolve_chain'][i]['approach']['0']) + 0.001)):
                    # 查询结果为空才能继续添加键值对，非空情况下键加0.01表示有第二种进化方式
                    x = {float(script['evolve_chain'][i]['approach']['0']) + 0.001: [script['evolve_chain'][i]['approach']['name'],
                                                                              script['evolve_chain'][i]['approach']['text']]}
                    dic['进化'].update(x)
                else:
                    x = {script['evolve_chain'][i]['approach']['0'] + 0.011: [
                        script['evolve_chain'][i]['approach']['name'],
                        script['evolve_chain'][i]['approach']['text']]}
                    dic['进化'].update(x)
                for i in range(len(script['evolve_chain'][0]['chain'])):
                    x = {script['evolve_chain'][0]['chain'][i]['approach']['0'] + 0.002: [
                             script['evolve_chain'][0]['chain'][i]['approach']['name'],
                             script['evolve_chain'][0]['chain'][i]['approach']['text']]}
                    dic['进化'].update(x)
            break

    if bool(dic['进化']):  # 在进化词条非空的情况下进行二次筛选
        id_001 = script['nat_id'] + 0.001
        id_011 = script['nat_id'] + 0.011
        id_002 = script['nat_id'] + 0.002
        level_2 = []
        level_2_1 = []
        level_3 = []
        y = {}
        l_id = list(dic['进化'].keys())
        for i in l_id:
            point_r, point_l = modf(i)
            point_r = round(point_r, 3)
            if point_r == 0.001:
                level_2.append(i)
            elif point_r == 0.011:
                level_2_1.append(i)
            else:
                level_3.append(i)
        if id_001 not in l_id and id_002 not in l_id and id_011 not in l_id:    # 初始形态
            for i in level_2:
                y[round(i)] = dic['进化'][i]
            if bool(level_2_1):
                for i in range(len(level_2_1)):
                    y[round(level_2_1[i])].append(dic['进化'][level_2_1[i]][1])
        elif id_001 in l_id:    # 二阶/最终形态
            if bool(level_3):
                for i in level_3:
                    y[round(i)] = dic['进化'][i]
            else:
                pass
        elif id_002 in l_id:    # 最终形态
            pass
        dic['进化'] = y

    return dic


def get_1():
    url = 'https://www.pokedex.app/zh/pokemon-{}'
    for i in range(1, 2):
        flag = True
        while flag:
            try:
                d = get_info(url.format(i))
                tx_0 = dp(d['特性'][0], ensure_ascii=False)
                tx_1 = dp(d['特性'][1], ensure_ascii=False)
                tx_2 = dp(d['特性'][2], ensure_ascii=False)
                jh = dp(d['进化'], ensure_ascii=False)
                zzz = dp(d['种族值'], ensure_ascii=False)
                csxt = dp(d['初始形态'], ensure_ascii=False)
                sql = '''INSERT INTO base_pkm(全国编号,伽勒尔编号,阿罗拉编号,属性,中文名,分类,特性1,特性2,隐藏特性,捕获率,
                                              蛋组,孵化周期,日文名,英文名,进化,种族值,初始形态) 
                        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')'''
                excuate.cal_pym(sql % (i, d['伽勒尔编号'], d['阿罗拉编号'], ','.join(d['属性']), d['中文名'], d['分类'],
                                       tx_0, tx_1, tx_2, d['捕获率'], ','.join(d['蛋组']),
                                       d['孵化周期'], d['日文名'], d['英文名'], jh, zzz, csxt))
                print('太好了！成功收服了编号为{}的「{}」！'.format(i, d['中文名']))
                flag = False
                time.sleep(1)
            except Exception as e:
                print('捕捉失败呜呜呜，再扔个精灵球试试')
                flag = True
                print(e)
                time.sleep(1)


if __name__ == '__main__':
    t_start = time.time()

    get_1()

    t_stop = time.time()
    print('用时：{:.2f}分钟'.format((t_stop - t_start) / 60.0))
