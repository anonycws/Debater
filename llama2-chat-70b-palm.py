import json
import openai
from poe_api_wrapper import PoeApi

POE_TOKEN = "9Op65dtYxqkTAorhNVs5nA%3D%3D"
# POE_TOKEN = "g4xFoKwbUYg39r-U9eaZtg%3D%3D"
poe_client = PoeApi(POE_TOKEN)


def poe_reply(text, bot, chatId=None):
    for chunk in poe_client.send_message(bot, text, chatId=chatId, timeout=120):
        pass
    return chunk


def generate_prompt(topic, t_pos, t_neg):
    pos_role1 = "You are a senior debater with strong dialectical ability. Now, you are participating in a debate competition on the topic of \"ZZZ\". You are the positive side; that is, you support \"XXX\". Next, please have a debate with the negative side who supports \"YYY\". The following are the rules of the competition:" \
              "\n1. Make a statement. Please explain your standpoint, requiring clear and sufficient arguments and a thorough analysis of your opinion about the \"XXX\"." \
              "\n2. Free debate. You and your opponent (negative side) each have three free debates. You can ask your opponent  (negative side) questions and answer his questions. Requirements: (1) You need to answer the question that the negative side asked if he asks questions. (2) Please make sure to introduce your arguments and opinions clearly. (3) Question the opinions of the negative side while strengthening your own." \
              "\n3. Summarize the statement. Question the opinions of the negative side while strengthening your own."
    neg_role1 = "You are a senior debater with strong dialectical ability. Now, you are participating in a debate competition on the topic of \"ZZZ\". You are the negative side; that is, you support \"YYY\". Next, please have a debate with the positive side who supports \"XXX\". The following are the rules of the competition:" \
              "\n1. Make a statement. Please explain your standpoint, requiring clear and sufficient arguments and a thorough analysis of your opinion about the \"YYY\"." \
              "\n2. Free debate. You and your opponent (negative side) each have three free debates. You can ask your opponent  (positive side) questions and answer his questions. Requirements: (1) You need to answer the question that the positive side asked if he asks questions. (2) Please make sure to introduce your arguments and opinions clearly. (3) Question the opinions of the positive side while strengthening your own." \
              "\n3. Summarize the statement. Question the opinions of the positive side while strengthening your own."
    pos_role = pos_role1.replace("ZZZ", topic).replace("XXX", t_pos).replace("YYY", t_neg)
    neg_role = neg_role1.replace("ZZZ", topic).replace("XXX", t_pos).replace("YYY", t_neg)

    pt_state = "\n\nFirst, please make a statement to explain your standpoint in less than 150 words."

    pos_pt_f1 = "First-round free debate. \nThe following text is the opponent's standpoint statement: \"TTTTT\". Next, please introduce your arguments and opinions, question the opponent's views, and answer their questions. Limit your response to 150 words."
    neg_pt_f1 = "First-round free debate. \nThe following text is the opponent's standpoint statement: \"TTTTT\". The opponent's first free debate is \"LLLLL\". Next, please introduce your arguments and opinions, question the opponent's views, and answer their questions. Limit your response to 150 words."

    pt_f2 = "Second-round free debate. \nThe following text is the opponent's free debate: \"TTTTT\". Next, please introduce your arguments and opinions, question the opponent's views, and answer their questions. Limit your response to 150 words."
    pt_f3 = "Third-round free debate. \nThe following text is the opponent's free debate: \"TTTTT\". Next, please introduce your arguments and opinions, question the opponent's views, and answer their questions. Limit your response to 150 words."

    pt_summ = "The following text is the opponent's standpoint statement: \"TTT\". \n\nSummarize the statement. Question the opinions of the opponent side while strengthening your own. Limit your response to 150 words."

    return pos_role,neg_role, pt_state,pos_pt_f1,neg_pt_f1,pt_f2,pt_f3,pt_summ

if __name__ == '__main__':
    pos_name, neg_name = "llama-2-chat-70b", "palm"
    
    data = {
        "education": {
            "topics": ["Does the traditional classroom address contemporary society’s needs?",
              "Should college education be compulsory?",
              "Should sexual education be mandatory?",
              "Should public colleges offer free tuition?",
              "Is it appropriate to judge heroes by success or failure?",
              "Is prosperity conducive to people's growth?",
              "Is love happier than being loved?",
              "Are generalists better off than specialists?"],
            "t_poses": ["Traditional classrooms can meet the needs of contemporary society",
               "College education should be compulsory",
               "Sexual education should be mandatory",
               "Public colleges should offer free tuition",
               "It is advisable to judge heroes by success or failure",
               "Prosperity is conducive to people growth",
               "Love is happier than being loved",
               "Generalists are better off than specialists"],
            "t_negs": ["Traditional classrooms cannot meet the needs of contemporary society",
              "College education should not be compulsory",
              "Sexual education should not be mandatory",
              "Public colleges should not offer free tuition",
              "It is not advisable to judge heroes by success or failure",
              "Adversity is conducive to people growth",
              "Being loved is happier than love",
              "Specialists are better off than generalists"],
            "file_names": ["traditional_classroom",
                  "college_education",
                  "sexual_education",
                  "free_tuition",
                  "judge_heroes",
                  "adversity",
                  "loved",
                  "generalists_specialists"]
		},
        "social": {
            "topics": ["Is cloning ethically acceptable?",
              "Is it ethical to have an abortion in the early stages of pregnancy?",
              "Should euthanasia be legalized?",
              "Is animal testing justified?",
              "Should the death penalty be taken away completely?",
              "Does the maintenance of social order mainly rely on law or morality?",
              "Is drug legalization a good idea?",
              "Should the number of private cars be limited?"],
            "t_poses": ["Cloning ethically is acceptable",
               "It is ethical to have an abortion in the early stages of pregnancy",
               "Euthanasia should be legalized",
               "Animal testing is justified",
               "The death penalty should be taken away completely",
               "The maintenance of social order mainly relies on the law",
               "Drug legalization is a good idea",
               "The number of private cars should be limited."],
            "t_negs": ["Cloning ethically is not acceptable",
              "It is not ethical to have an abortion in the early stages of pregnancy",
              "Euthanasia should not be legalized",
              "Animal testing is not justified",
              "The death penalty should not be taken away completely",
              "The maintenance of social order mainly relies on morality",
              "Drug legalization is not a good idea",
              "The number of private cars should not be limited."],
            "file_names": ["cloning",
                  "abort_pregnancy",
                  "euthanasia",
                  "animal_testing",
                  "death_penalty",
                  "social_order",
                  "drug_legalization",
                  "private_car"]
		},
        "fun filled": {
            "topics": ["Can personal interests and group interests be balanced?",
              "Should euthanasia be legalized?",
              "Is love selfish or selfless?",
              "Do fairy tales affect children’s perception of reality?",
              "Do women need more care than men?",
              "Is the popularity of short videos a manifestation of spiritual and cultural richness or lack?",
              "Is IQ more important than EQ, or is EQ more important than IQ?",
              "Which is more important, fighting ignorance or poverty?"],
            "t_poses": ["Personal interests and group interests can be balanced",
               "Euthanasia should be legalized",
               "love is selfish",
               "Fairy tales affect children's perception of reality",
               "Women need more care than men",
               "The popularity of short videos is a manifestation of spiritual and cultural richness",
               "IQ is more important than EQ",
               "Fighting ignorance is more important than fighting poverty"],
            "t_negs": ["Personal interests and group interests cannot be balanced",
              "Euthanasia should not be legalized",
              "love is selfless",
              "Fairy tales do not affect children's perception of reality",
              "Men need more care than women",
              "The popularity of short videos is a manifestation of spiritual and cultural lack",
              "EQ is more important than IQ",
              "Fighting poverty is more important than fighting stupidity"],
            "file_names": ["personal_group_interests",
                  "Euthanasia",
                  "love_selfish_selfless",
                  "fairy_tales",
                  "more_care",
                  "short_videos",
                  "EQ_IQ",
                  "fighting_ignorance_poverty"]
		},
        "family": {
            "topics": ["Should children use smartphones without parental supervision?",
              "Should parents decide which career their children will pursue?",
              "Is it ethically permissible for parents to  pick the genders of their future children?",
              "Is parental support essential for the future success of children?",
              "Should we send parents to nursing homes?",
              "Which is more important, career or family?",
              "Should there be privacy between husband and wife?",
              "Does the generation gap mainly come from parents or children?"],
            "t_poses": ["Children can use smartphones without parental supervision",
               "Parents should decide which career their children will pursue",
               "It is ethically permissible for parents to pick the genders of their future children",
               "Parental support is critical to a child's future success",
               "We should send parents to nursing homes.",
               "Career is more important than family",
               "Husband and wife should have privacy",
               "The generation gap mainly comes from parents"],
            "t_negs": ["Children cannot use smartphones without parental supervision",
              "Parents should not decide which career their children will pursue",
              "It is not ethically permissible for parents to pick the genders of their future children",
              "Parental support is not critical to a child's future success",
              "We should not send parents to nursing homes.",
              "Family is more important than career",
              "Husband and wife should be no privacy",
              "The generation gap mainly comes from children"],
            "file_names": ["children_samrtphones",
                  "decide_career_child",
                  "pick_gender",
                  "parental_support",
                  "nursing_home",
                  "family_career_important",
                  "husband_wife_privacy",
                  "generation_gap"]
		},
        "leisure": {
            "topics": ["Is leisure time essential for workplace effectiveness?",
              "Women spend their leisure time differently than men.",
              "Is a summer vacation better than a winter vacation?",
              "Has technology changed the way young people spend their leisure time?",
              "Playing video games during leisure time: pros and cons.",
              "Is it necessary to stop Spanish bullfighting?",
              "Should the establishment of lofty ideals follow personal hobbies or the trend of social development?",
              "Should workplace dating be banned?"],
            "t_poses": ["Leisure time is essential for workplace effectiveness",
               "Women spend their leisure time differently than men",
               "Summer vacation is better than winter vacation",
               "Technology has changed the way young people spend their leisure time",
               "Playing video games in your spare time is beneficial",
               "Spanish bullfighting needs to stop",
               "the establishment of lofty ideals should follow personal hobbies",
               "workplace dating should be banned"],
            "t_negs": ["Leisure time is not essential for workplace effectiveness",
              "Women spend their leisure time in the same way as men",
              "Summer vacation is no better than winter vacation",
              "Technology has not changed the way young people spend their leisure time",
              "Playing video games in your spare time is not beneficial",
              "Spanish bullfighting doesn't have to stop",
              "the establishment of lofty ideals should follow the trend of social development",
              "workplace dating should not be banned"],
            "file_names": ["leisure_time_essential",
                  "women_leisure_time",
                  "summer_vacation",
                  "technology_leisure",
                  "playing_video_games",
                  "spanish_bullfighting",
                  "establishment_lofty_ideals",
                  "workplace_dating"]
		},
        "environment": {
            "topics": ["Should we ban plastic bags and packaging?",
              "Should we ban zoos?",
              "Should all people become vegetarian?",
              "Should urban stray cats be culled?",
              "Can economic development and environmental protection go hand in hand?",
              "Should we limit setting off fireworks?",
              "Does a low-carbon life rely more on technological innovation or conceptual change?",
              "Is tourism beneficial to the environment?"],
            "t_poses": ["Plastic bags and packaging should be banned totally",
               "Zoos should be banned totally",
               "All people should become vegetarian",
               "Urban stray cats should be culled",
               "Economic development and environmental protection can go hand in hand.",
               "We should limit setting off fireworks",
               "The low-carbon life relies more on technological innovation",
               "Tourism is beneficial to the environment"],
            "t_negs": ["Plastic bags and packaging should not be banned",
              "Zoos should not be banned",
              "All people should not become vegetarians",
              "Urban stray cats should not be culled",
              "Economic development and environmental protection can not go hand in hand.",
              "We should not limit setting off fireworks",
              "The low-carbon life relies more on conceptual change",
              "Tourism is not beneficial to the environment"],
            "file_names": ["plastic_bags",
                  "ban_zoos",
                  "vegetarians",
                  "urban_stray_cats",
                  "economic_development",
                  "fireworks",
                  "low-carbon",
                  "tourism"]
		}
	}
    
    data_name_list = ["education", "social", "fun filled", "family", "leisure", "environment"]
    for domain in data_name_list:
        if domain in ["education", "social", "fun filled", "family", "leisure"]:
            continue
        print("\n\n\n\nstart domain: " + domain + "\n\n\n")
        topics = data.get(domain).get("topics")
        t_poses = data.get(domain).get("t_poses")
        t_negs = data.get(domain).get("t_negs")
        file_names = data.get(domain).get("file_names")

        for index in range(len(topics)): 
            if domain == 'environment' and index in [0,1,2,3,4,5,6]:
                continue
            pos_db_list = []
            neg_db_list = []

            topic = topics[index]
            t_pos = t_poses[index]
            t_neg = t_negs[index]
            print("topic: " + topic)
            print("t_pos: " + t_pos)
            print("t_neg: " + t_neg)
            pos_role, neg_role, pt_state, pos_pt_f1, neg_pt_f1, pt_f2, pt_f3, pt_summ = generate_prompt(topic, t_pos, t_neg)

            print('1._______________________________________')
            print("##### llama2-chat-70b")
            pos_deb1_chunk = poe_reply(pos_role + pt_state, "Llama-2-70b")
            pos_chatId = pos_deb1_chunk["chatId"]
            pos_deb1 = pos_deb1_chunk["text"]
            print(pos_deb1)

            print("##### palm")
            neg_deb1_chunk = poe_reply(neg_role + pt_state, "Google-PaLM")
            neg_chatId = neg_deb1_chunk["chatId"]
            neg_deb1 = neg_deb1_chunk["text"]
            print(neg_deb1)

            pos_db_list.append(pos_deb1)
            neg_db_list.append(neg_deb1)

            print('2._______________________________________')
            print("##### llama2-chat-70b")
            m2_pos = pos_pt_f1.replace('TTTTT', neg_deb1)  # pos, first-free-debate; with neg-statement
            pos_deb2 = poe_reply(m2_pos, "Llama-2-70b", chatId=pos_chatId)["text"]
            print(pos_deb2)

            print("##### palm")
            m2_neg = neg_pt_f1.replace('TTTTT', pos_deb1).replace('LLLLL', pos_deb2)  # neg, first-free-debate; with neg-statement; with pos-db1
            neg_deb2 = poe_reply(m2_neg, "Google-PaLM", chatId=neg_chatId)["text"]
            print(neg_deb2)
            pos_db_list.append(pos_deb2)
            neg_db_list.append(neg_deb2)

            print('3._______________________________________')
            print("##### llama2-chat-70b")
            m3_pos = pt_f2.replace('TTTTT', neg_deb2)
            pos_deb3 = poe_reply(m3_pos, "Llama-2-70b", chatId=pos_chatId)["text"]
            print(pos_deb3)

            print("##### palm")
            m3_neg = pt_f2.replace('TTTTT', pos_deb3)
            neg_deb3 = poe_reply(m3_neg, "Google-PaLM", chatId=neg_chatId)["text"]
            print(neg_deb3)

            pos_db_list.append(pos_deb3)
            neg_db_list.append(neg_deb3)

            print('4._______________________________________')
            print("##### llama2-chat-70b")
            m4_pos = pt_f3.replace('TTTTT', neg_deb3)
            pos_deb4 = poe_reply(m4_pos, "Llama-2-70b", chatId=pos_chatId)["text"]
            print(pos_deb4)

            print("##### palm")
            m4_neg = pt_f3.replace('TTTTT', pos_deb4)
            neg_deb4 = poe_reply(m4_neg, "Google-PaLM", chatId=neg_chatId)["text"]
            print(neg_deb4)

            pos_db_list.append(pos_deb4)
            neg_db_list.append(neg_deb4)

            print('6._______________________________________')
            print("##### llama2-chat-70b")
            m5_pos = pt_summ.replace("TTT", neg_deb4)
            pos_deb5 = poe_reply(m5_pos, "Llama-2-70b", chatId=pos_chatId)["text"]
            print(pos_deb5)

            print("##### palm")
            m5_neg = pt_summ.replace("TTT", pos_deb5)
            neg_deb5 = poe_reply(m5_neg, "Google-PaLM", chatId=neg_chatId)["text"]
            print(neg_deb5)

            pos_db_list.append(pos_deb5)
            neg_db_list.append(neg_deb5)

            db_dic = {}
            db_dic['pos'] = []
            db_dic['neg'] = []
            db_dic['pos'] = pos_db_list
            db_dic['neg'] = neg_db_list
            db_dic['pos_db'] = pos_name
            db_dic['neg_db'] = neg_name
            db_dic['domain'] = domain
            db_dic["topic"] = topic

            print('file_names[index]: ',file_names[index])
            with open('results-70b-palm/'+pos_name + "_" + neg_name + "_" + domain + "_" + file_names[index] + "_db2.json", "w") as wfile:
                json.dump(db_dic, wfile, indent=4)
            
            poe_client.delete_chat("Llama-2-70b", chatId=pos_chatId)
            poe_client.delete_chat("Google-PaLM", chatId=neg_chatId)