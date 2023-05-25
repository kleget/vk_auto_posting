from importt import *

########## берем 100 постов из группы 'domain' ##########
def take_100_posts(domain, count_post, access_token):
    time.sleep(1)
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                "access_token": access_token,
                                "v": v,
                                "domain": domain,
                                "count": count_post
                            }).json()['response']['items']
    data = response[::-1]
    j = 0
    while j < len(data):
        if len(data[j]['text']) == 0 or data[j]['text'] == None or 'text' not in data[j]:  # ТЕКСТА НЕТ
            del data[j]
        else:
            j += 1
    return data

########## Проверяем наличие ключевых слов ##########
def key_words_filter(data, hatf):
    if hatf[0] != 'empty':
        for i in hatf[0]:
            if i in (data['text']).lower():
                return True
        return False
    else:
        return True

########## Проверяем наличие запретных слов ##########
def bed_words_filter(data, hatf):
    if hatf[1] != 'empty':
        for i in hatf[1]:
            if i in (data['text']).lower():
                return False
        return True
    else:
        return True

########## ВЫБИРАЕМ ПОСТЫ(К+Т, К) И ВОЗВРАЩАЕМ ИХ ЧЕРЕЗ POSTS ##########
def filter(data, hatf):# проверяем наличие фотографии в отсеянных постах #2{
    posts = []
    i = 0
    while i < len(data):
        # TEXT
        pos = []
        if "text" in data[i] and len(data[i]['text']) >= 1:
            try:
                if key_words_filter(data[i], hatf) == bed_words_filter(data[i], hatf) == True:
                    pos.append(data[i]['text'])
                else:
                    i += 1
                    continue
            except:
                i += 1
                continue
        else:
            i += 1
            continue

        # IMG
        if 'attachments' in data[i]:
            try:
                if len(data[i]['attachments']) >= 1:
                    for h in range(len(data[i]['attachments'])):
                        if data[i]['attachments'][h]['type'] in ['video' or 'audio' or 'doc' or 'poll']:
                            i += 1
                            continue
                        if data[i]['attachments'][h]['type'] == 'photo':
                            try:
                                ind = sort_size(data[i]['attachments'][h]['photo']['sizes'])
                                pos.append(data[i]['attachments'][h]['photo']['sizes'][ind]['url'])
                                i += 1
                                break
                            except:
                                pos.append('nonono')
                                i += 1
                                break
                        else:
                            pos.append('nonono')
                            i += 1
                            break
                else:
                    pos.append('nonono')
                    i += 1
                    break
            except:
                pos.append('nonono')
                i += 1
                break
        else:
            pos.append('nonono')
            i += 1
            break
        if len(pos) == 2:
            posts.append('%&*'.join(pos))
        else:
            continue
    return posts

########## ВЫБИРАЕТ НАИБОЛЬШИЙ РАЗМЕР КАРТИНКИ ##########
def sort_size(data):
    spisok = []
    for i in range(len(data)): 
        spisok.append(data[i]['height'])
    return spisok.index(max(spisok))

##########  ##########
def poster(answ, group_id,  hatf):
    ho = True
    h = 0
    while ho == True and h < len(answ):
        h = random.randint(0, len(answ) - 1)
        t = answ[h]
        t = t.split('%&*')
        t1 = t[0] # тект
        t2 = t[1] # картинка
        hashteg = hatf[3]
        # p = True
        if t1 != '***': #есть текст есть\нет картинки
            if hashteg != 'empty': # есть указанные хэштеги, значит удалям старые из поста и добавляем новые
                glavnaya(f"{t1}\n\n{hashteg}", t2, group_id, hatf[4], hatf[2])
                ho = False
                break
            else: # нет указынных хэштегов, значит мы просто удалям их из поста и ничего нового не добавляем
                glavnaya(t1, t2, group_id, hatf[4], hatf[2])
        h += 1

##########  ##########
def main():
    # try:
        while True:
            num = parsing_google_sheets_1()
            for w in range(0, num):
                open('params.txt', 'w').close()
                hatf = parsing_google_sheets_2(w)
                if hatf == "STOP":
                    continue
                print(f"-------- https://vk.com/{hatf[2]} --------")
                c = open('params.txt', 'r', encoding='utf-8')
                params = c.readlines()
                c.close()
                data_f = take_100_posts(hatf[2], int(hatf[5]), hatf[4])  # ПОСТЫ ИЗ ОСНОВЫ
                poposts = []
                for z in range(len(params)):
                    pppp = params[z]
                    pppp = re.sub("['|[|]|\\n|]", "", pppp).split(' ')
                    count_post = int(pppp[0])
                    domain = pppp[1]
                    group_id = int(pppp[2])
                    if z+1 != len(params):
                        print(domain, end=', ')
                    else:
                        print(domain)
                    data = take_100_posts(domain, count_post, hatf[4])# ПОСТЫ ИЗ ДОНОРОВ
                    i = 0
                    o = filter(data, hatf) #ПОСТЫ, В КОТОРЫХ ЕСТЬ ТЕКСТ
                    if o != None and len(o) >= 1:
                        poposts += o
                        i += 1

                answ = []
                for post in poposts:
                    similarity_found = False
                    post_split = post.split('%&*')
                    ww = deleting_hashtag(post_split[0]).lower()
                    # print(data_f)
                    if data_f is not None:
                        for datas in data_f:
                            rr = deleting_hashtag(datas['text']).lower()
                            similarity = difflib.SequenceMatcher(None, rr, ww).ratio() * 100 #На сколько процентов текст из основы совпадает с текстом из донора
                            if similarity > 25:
                                similarity_found = True
                                break
                    if similarity_found == False:
                        answ.append(f"{deleting_hashtag(post_split[0])}%&*{post_split[1]}")

                if len(answ) > 0:
                    poster(answ, group_id=group_id, hatf=hatf)
                    poposts.clear()
                    answ.clear()
                else:
                    print('________NO POST________\n\n')

        ########## ОТПРАВЛЯЕТ СКРИПТ В СОН ##########
            po = random.randint(110*60, 140*60)
            kl = str(datetime.now())[11:13]
            if int(kl) == 00 or int(kl) == 1:
                print("SLEEP   ", datetime.now())
                time.sleep(9 * 60 * 60)
            else:
                timi(po)
                time.sleep(po)
    # except:
    #     print('Ошибка в main()')
    #     time.sleep(sleep_time_on_error)
    #     main()

def deleting_hashtag(text):
    text = text.replace('\n', ' ')
    text = text.split(' ')
    text = text[::-1]
    i = 0
    while i in range(len(text)):
        if len(text[i]) != 0:
            if text[i][0] == '#':
                del text[i]
            else:
                i += 1
        else:
            del text[i]
    return " ".join(text[::-1])

########## СЧИТАЕТ ВРЕМЯ ##########
def timi(po):
    e = str(datetime.now())[11:16].split(':')
    e1 = int(e[0])
    e2 = int(e[1])
    if po >= 3600:
        k = int((po - 3600) / 60)
        if e2 + k >= 60:
            print(f"{e1 + 2}:{e2 + k - 60} ({po/60} min)")
        else:
            print(f"{e1 + 1}:{e2 + k} ({po/60} min)")
    else:
        k = int(po / 60)
        if e2 + k >= 60:
            print(f"{e1 + 1}:{e2 + k - 60} ({po/60} min)")
        else:
            print(f"{e1}:{e2 + k} ({po/60} min)")

if __name__ == "__main__":
    main()
