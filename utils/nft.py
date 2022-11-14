import json

with open('data/nft.json', 'r') as fp:
    js = json.load(fp)

async def get_categorys(start):
    end = start + 10
    categorys = []
    for index, category in enumerate(js):
        if index == end:
            break
        elif index >= start:
            categorys.append(category)
    return categorys

def get_category(category_index):
    paragraphs = []
    for index, category in enumerate(js):
        if index == category_index:
            for paragraph in js[category]:
                if js[category][paragraph]['is_sell']:
                    paragraphs.append(paragraph)
            return paragraphs, category

def sell_nft(category_index_need, paragraph_index_need):
    for category_index, category in enumerate(js):
        if category_index == category_index_need:
            for paragraph_index, paragraph in enumerate(js[category]):
                if paragraph_index == paragraph_index_need:
                    js[category][paragraph]['is_sell'] = not(js[category][paragraph]['is_sell'])
                    save_nft_js()
                    return True

def get_category_index(need_category):
    for index, category in enumerate(js):
        if category == need_category:
            return index

def buy_nft_js(category, paragraph, tg_id):
    js[category][paragraph]['is_sell'] = False
    js[category][paragraph]['buyer'] = tg_id
    save_nft_js()

def save_nft_js():
    with open('data/nft.json', 'w') as fp:
        json.dump(js, fp)


def get_paragraph_index(category, need_paragraph):
    for index, paragraph in enumerate(js[category]):
        if paragraph == need_paragraph:
            return index

def get_nft(need_category, need_paragraph):
    for category_index, category in enumerate(js):
        if category_index == need_category:
            for paragraph_index, paragraph in enumerate(js[category]):
                if need_paragraph == paragraph_index:
                    return js[category][paragraph], paragraph, category
    print('вышел')
