# import xlrd
import pandas as pd
import openai
import os
import json
import ast
def chatGPT35(msg_list):
    # import openai
    openai.api_key = "API_KEYH"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=msg_list
    )

    chat = ''
    for choice in response.choices:
        chat += choice.message.content
    print('ChatGPT: ', chat)

    return chat

def clean(string):
    # str2 = string.replace('\n\n', ' ').strip()
    str2 = string.replace('\n', ' ').strip()
    str2 = str2.replace('  ', ' ').strip()
    str2 = str2.replace('  ', ' ').strip()
    return str2

def read_eval_datas(folder, pre_pos_name, pre_neg_name):
    task_prompt, debating_prompt, dm_topics = eval_prompt()
    files = os.listdir(folder)
    # files = files[:5]

    debater_pairs = []
    count_eval = 0
    data_name_list = ["education", "social", "fun filled", "family", "leisure", "environment"]
    # dabate_pair = 'Claude_ChatGPT'
    # dabate_pair = 'GPT4_ChatGPT'
    data_dics = []
    for file in files:
        print('file: ',file)
        if file =='.DS_Store':
            continue
        fpath = folder + '/'+ file
        data_dic = json.load(open(fpath, 'r'))
        debater1s = [clean(x) for x in data_dic["pos"] ]
        debater2s = [clean(x) for x in data_dic["neg"] ]
        pos_name = data_dic["pos_db"]
        neg_name = data_dic["neg_db"]
        domain = data_dic["domain"]
        if pos_name==pre_pos_name and neg_name ==pre_neg_name:
            len_pos = [len(x.split()) for x in data_dic["pos"] ]
            len_neg = [len(x.split()) for x in data_dic["neg"] ]
            print('len_pos: ',len_pos)
            print('len_neg: ', len_neg)
            total_len1 = sum(len_pos) + sum(len_neg)
            print('total_len1: ', total_len1)
            total_len = sum([len(x.split()) for x in data_dic["pos"] ] + [len(x.split()) for x in data_dic["neg"] ])
            # print('total_len: ', sum(total_len))

            # if total_len <2200:
            print()
            print('file: ', file)
            print('total_len: ', total_len)
            # print('data_dic: ',data_dic)
            pos_db = data_dic["pos_db"]
            neg_db = data_dic["neg_db"]
            domain = data_dic["domain"]
            topic = data_dic["topic"]
            d1, d2, d3, d4, d5 = debater1s
            c1, c2, c3, c4, c5 = debater2s
            # print('d1: ', d1)

            count_eval +=1

            debating = debating_prompt.replace('X1X1X1',d1).replace('X2X2X2',d2).replace('X3X3X3',d3).replace('X4X4X4',d4).replace('X5X5X5',d5).replace('Y1Y1Y1',c1).replace('Y2Y2Y2',c2).replace('Y3Y3Y3',c3).replace('Y4Y4Y4',c4).replace('Y5Y5Y5',c5)
            # print('debating: ', debating)
            debater_pairs.append(debating)

            print('count_eval: ', count_eval)

            topics = dm_topics.get(domain).get("topics")
            t_poss  = dm_topics.get(domain).get("t_poses")
            t_negs = dm_topics.get(domain).get("t_negs")
            topic_idx = topics.index(topic)
            t_pos = t_poss[topic_idx]
            t_neg = t_negs[topic_idx]
            print('------------------------------------------------------------')
            print('topic: ', topic)
            print('t_pos: ', t_pos)
            print('t_neg: ', t_neg)
            task_intro = task_prompt.replace('XXXXX', topic).replace('YYYYY', t_pos).replace('ZZZZZ', t_neg)

            msg_list = [
                {"role": "system", "content": task_intro},
                {"role": "user", "content": debating},
            ]
            print('**********************************')
            print('msg_list: ', msg_list)
            eval_res = chatGPT35(msg_list)
            print('eval_res: ',eval_res)
            data_dic['eval'] =eval_res

            data_dics.append(data_dic)

            with open('eval_results/' + pos_name + "_" + neg_name + "_" + domain  + "111.json", "w") as wfile:
                json.dump(data_dics, wfile, indent=4)
             # break


    # return task_prompt, debater_pairs


def read_eval(folder, file):
    # files = os.listdir(folder)
    fpath = folder + '/' +file
    clean_datas = []
    datas = json.load(open(fpath, 'r'))
    for idx,data in enumerate(datas):
        print('idx: ',idx)
        pos_name = data["pos_db"]
        neg_name = data["neg_db"]
        domain = data["domain"]

        eval_res = data["eval"].split('Explanation')[0]
        if 'Note: ' in eval_res:
            eval_res = data["eval"].split('Note: ')[0]

        eval_res = eval_res.replace('\n', ' ').strip()
        eval_res = ast.literal_eval(eval_res)
        print('eval_res: ',eval_res)
        data["eval"] = eval_res
        clean_datas.append(data)

    write_name = folder + '/'+ file.split('.json')[0] + '_dic.json'
    with open(write_name, "w") as wfile:
        json.dump(clean_datas, wfile, indent=4)









if __name__ == '__main__':
    # folder ='./datas/'
    folder = './results'
    pre_pos_name = 'ChatGPT'
    pre_neg_name = 'GPT4'
    # read_eval_datas(folder,pre_pos_name,pre_neg_name)

    pre_pos_name = 'ChatGPT'
    pre_neg_name = 'Claude'
    # read_eval_datas(folder,pre_pos_name,pre_neg_name)


    # # eval --> dic
    # folder = 'eval_results'
    # file = 'GPT4_ChatGPT.json'
    # read_eval(folder, file)
    #
    # folder = 'eval_results'
    # file = 'Claude_ChatGPT.json'
    # read_eval(folder, file)

    # folder = 'eval_results'
    # file = 'ChatGPT_GPT4.json'
    # read_eval(folder, file)

    folder = 'eval_results'
    file = 'ChatGPT_Claude.json'
    read_eval(folder, file)

