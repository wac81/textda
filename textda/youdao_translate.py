import json

import requests
import os
import time
import random


print('WARNING: you need know, I would do my best for this translate web working, but it was allowed only 1000 times one hour.')

def translate(word):
    '''
    request youdao web
    :param word:
    :return:
    '''
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "false"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        return response.text
    else:
        print("youdao web request failed!")
        # 相应失败就返回空
        return None

def get_reuslt(repsonse):
    # 通过 json.loads 把返回的结果加载成 json 格式
    # try:
    result = json.loads(repsonse)
    return result['translateResult'][0][0]['tgt']

def read_text_src(text_src, delimiter):
    if isinstance(text_src, str):
        with open(text_src, 'r') as f:
            text_src = [line.split(delimiter) for line in f]
    elif not isinstance(text_src, list):
        raise TypeError('text_src should be list or str')
    return text_src

def translate_batch(file_path, batch_num=30, reWrite=True, suffix='_youdao'):
    '''

    :param file_path: src file path
    :param batch_num: default 30
    :param reWrite: default True. means you can rewrite file , False means you can append data after this file.
    :param suffix: new file suffix
    :return:
    '''

    texts = read_text_src(file_path, delimiter='\t')
    with open(file_path + suffix, 'w' if reWrite else 'a') as f:
        for i in range(0, len(texts), batch_num):  #批量翻译
            text = texts[i:i+batch_num]
            text_batch = ''
            text_tag = []
            for t in text:
                f.write(t[0] + '\t' + t[1].strip() + '\n')
                # if t[0] != 'neu':
                #     continue
                text_batch += t[1]
                text_tag.append(t[0])
            print(text)

            if text_batch == '':
                continue
            #批量翻译
            #先翻译成英文
            list_trans = translate(text_batch)
            if list_trans is not None and json.loads(list_trans)['errorCode'] == 0:
                text_batch = ''
                for t in json.loads(list_trans)['translateResult']:
                    text_batch += t[0]['tgt'] + '\n'

                #英文--》中文
                chinese_trans = translate(text_batch.strip('\n'))
                if chinese_trans is not None:
                    ct = json.loads(chinese_trans)
                    if 'translateResult' in ct.keys():
                        for i, t in enumerate(json.loads(chinese_trans)['translateResult']):
                            print(t[0]['tgt'])
                            if t[0]['tgt'] is None:
                                continue
                            f.write(text_tag[i] + '\t' + t[0]['tgt'] + '\n')
            else:
                print('error: requests many times')
                continue

            # time.sleep(random.random() * 5)
            time.sleep(3)   #一小时允许1000次，每秒允许0.27次，间隔睡眠时间定在3秒

if __name__ == '__main__':

    dir = './data'

    translate_batch(os.path.join(dir, 'insurance_train'), batch_num=30)
