from flask import Flask, render_template, url_for, request
import random
import copy
import itertools

app = Flask(__name__)

# お客様の好みを保存するクラス
class Preference:
    def __init__(self, shape = None, feeling = None, words = None, flower = None):
        self.shape = shape
        self.feeling = feeling
        self.words = words
        self.flower = flower
    # 表示用関数
    def __str__(self):
        return f"形：{self.shape} キモチ：{self.feeling} 言葉：{self.words} 商品：{self.flower}"

# カタチと値段
shape_value = {
    "one": 1000,
    "s-bouquet": 3000,
    "m-bouquet": 5000,
    "l-bouquet": 10000,
    "cup": 2000,
    "driedflower": 3000,
    "giftflower": 10000,
    "a-wineflower": 15000,
    "b-wineflower": 20000,
}

# キモチと言葉
feeling_words = {
    "love": ["いつも感謝しています",
               "あなたに愛を誓います",
               "深く尊敬しています",
               "たくさんの愛をあなたにおくります"],
    "celebration": ["輝かしい未来に、おめでとう！",
                    "親愛なる友人へ、おめでとう！",
                    "魅力あふれるあなたへ、おめでとう！",
                    "夢への一歩、おめでとう！"],
    "thanks": ["いつも感謝しています",
               "あなたのサポートへ感謝します"],
    "business": ["あなたのさらなる前進を祈っています",
             "あなたに新たな出会いやさくさんの絆が生まれますように",
             "成功して輝き続ける未来が待っていますように",
             "挑戦し続けるあなたを応援します"],
}

# 花言葉
flower_lang = {
    "red_gerbera": [200, "赤いガーベラ", "「常に前進」・「チャレンジ」という花言葉を持っており挑戦する", "red"],
    "red_dahlia": [600, "赤いダリア", "「華麗」・「栄華」という花言葉を持っており輝き続ける", "red"],
    "pink_dahlia": [600, "ピンクやオレンジダリア", "「優雅」・「気品」・「栄華」・「威厳」という花言葉を持っており輝き続ける", "red"],
    "orange_rose": [400, "オレンジの薔薇", "「絆」・「信頼」・「健やか」という花言葉を持っており新たな出会いや絆が生まれるような", "yellow"],
    "gypsophila": [600, "かすみ草", "「感謝」という花言葉を持っており感謝を伝えたい", "green"],
    "pink_gerbera": [200, "ピンクのガーベラ", "「感謝」・「神秘」・「熱愛」・「崇高美」という花言葉をもっており感謝を伝えたい", "red"],
    "white_dahlia": [600, "白いダリア", "「感謝」・「豊かな愛情」という花言葉を持っており感謝を伝えたい", "blue"],
    "lily": [800, "ユリ", "「純粋」という花言葉を持っており感謝を伝えたい", "red"],
    "red_rose": [400, "赤い薔薇", "「愛情」・「美」・「情熱」・「ロマンス」という花言葉を持っており愛を伝えたい", "red"],
    "white_rose": [400, "白い薔薇", "「純潔」・「深い尊敬」という花言葉を持っており尊敬している", "blue"],
    "pink_rose": [400, "ピンクの薔薇", "「上品」・「感謝」・「幸福」・「愛の誓い」という花言葉を持っており感謝を伝えたい", "red"],
    "pink_astilbe": [300, "ピンクのアスチルベ", "「恋の訪れ」・「自由」・「落ち着いた明るさ」という花言葉を持っており愛を伝えたい", "red"],
    "pink_anthurium": [600, "ピンクのアンスリウム", "「飾らない美しさ」という花言葉を持っており尊敬している", "red"],
    "oncidium": [700, "オンシジウム", "「可憐」・「一緒に踊って」という花言葉を持っており愛を伝えたい", "yellow"],
    "orange_strelitzia": [800, "オレンジ色のストレリチア", "「寛容」・「輝かしい未来」という花言葉を持っており祝福を伝えたい", "yellow"],
    "yellow_rose": [400, "黄色の薔薇", "「友情」・「思いやり」・「幸福」・「温かさ」という花言葉を持っており祝福を伝えたい", "yellow"],
    "purple_lisianthus": [800, "紫色のトルコキキョウ", "「希望」という花言葉を持っており祝福を伝えたい", "red"],
}

# 花とpreferenceの対応
all_items = [key for key in flower_lang.keys()]
love_flowers = [["pink_rose"], ["red_rose"], ["white_rose", "pink_anthurium"], ["pink_astilbe", "oncidium"]]
celebration_flowers = [["orange_strelitzia"], ["yellow_rose"], ["yellow_rose"], ["purple_lisianthus"]]
thanks_flowers = [["gypsophila", "pink_gerbera", "white_dahlia", "lily"], ["gypsophila", "pink_gerbera", "white_dahlia", "lily"]]
business_flowers = [["red_gerbera"], ["orange_rose"], ["red_dahlia", "pink_dahlia"], ["red_gerbera"]]

love_reasonable = ["pink_rose", "red_rose", "white_rose", "pink_astilbe"]
celebration_reasonable = ["yellow_rose", "yellow_rose", "yellow_rose", "yellow_rose"]
thanks_reasonable = ["pink_gerbera", "pink_gerbera", "pink_gerbera", "pink_gerbera"]
business_reasonable = ["red_gerbera", "orange_rose", "orange_rose", "red_gerbera"]
reasonable_items = ["red_gerbera", "orange_rose", "pink_gerbera", "red_rose",
                    "white_rose", "pink_rose", "pink_astilbe", "yellow_rose"]

# トップページ
@app.route("/", methods=["GET"])
def index():
    return render_template("top.html")

# 大分類
@app.route("/major_div", methods=["GET"])
def select_div():
    return render_template("major_div.html")

# カタチを選ぶページ
@app.route("/select_shape", methods=["GET"])
def select_shape():
    return render_template("select_shape.html")

# 感情を選ぶページ
@app.route("/select_feeling/<shape>", methods=["GET"])
def select_feeling(shape):
    preference = Preference(shape=shape)
    value = shape_value[shape]
    if "bouquet" in shape:
        img_name = "image/shape/bouquet.png"
    elif "wineflower" in shape:
        img_name = "image/shape/wineflower.png"
    else:
        img_name = "image/shape/" + shape + ".png"
    return render_template("select_feeling.html", preference=preference, value=value, img_name=img_name)

# 言葉を選ぶページ
@app.route("/select_words/<shape>/<feeling>", methods=["GET"])
def select_words(shape, feeling):
    preference = Preference(shape=shape, feeling=feeling)
    words_list = feeling_words[feeling]
    return render_template("select_words.html", preference=preference, words_list=words_list, length=len(words_list))

# 花を選ぶページ
@app.route("/select_flower/<shape>/<feeling>/<int:words>", methods=["GET"])
def select_flower(shape, feeling, words):
    preference = Preference(shape=shape, feeling=feeling, words=words)
    feeling_word = feeling_words[feeling][words]
    if (shape == "one") or (shape == "s-bouquet") or (shape == "cup") or (shape == "driedflower"):
        recommend_items = []
        if feeling=="love":
            recommend_items.append(love_reasonable[words])
        elif feeling=="celebration":
            recommend_items.append(celebration_reasonable[words])
        elif feeling=="thanks":
            recommend_items.append(thanks_reasonable[words])
        else:
            recommend_items.append(business_reasonable[words])
        rest_items = random.sample(list(filter(lambda x: x not in recommend_items, reasonable_items)) , 2)
    else:
        if feeling=="love":
            recommend_items = copy.copy(love_flowers[words])
        elif feeling=="celebration":
            recommend_items = copy.copy(celebration_flowers[words])
        elif feeling=="thanks":
            recommend_items = random.sample(thanks_flowers[words] , 2)
        else:        
            recommend_items = copy.copy(business_flowers[words])
        rest_items = random.sample(list(filter(lambda x: x not in recommend_items, all_items)) , 3 - len(recommend_items))

    merchandise = []
    for name in recommend_items:
        merchandise.append([name, "image/merchandise/"+name+".webp", flower_lang[name][1], "この花には"+flower_lang[name][2]+"人へピッタリな花になっています", flower_lang[name][3]+"-color"])
    for name in rest_items:
        merchandise.append([name, "image/merchandise/"+name+".webp", flower_lang[name][1], "この花には"+flower_lang[name][2]+"人へピッタリな花になっています", flower_lang[name][3]+"-color"])


    return render_template("select_flower.html", preference=preference, feeling_word=feeling_word, \
                           merchandise=merchandise, recommend_nums=len(recommend_items))

# 内容確認ページ
@app.route("/confirmation/<shape>/<feeling>/<int:words>/<flower>", methods=["GET"])
def confirmation(shape, feeling, words, flower):
    preference = Preference(shape=shape, feeling=feeling, words=words, flower=flower)
    feeling_word = feeling_words[feeling][words]
    merchandise=[flower, "image/merchandise/"+flower+".webp", flower_lang[flower][1], "この花には"+flower_lang[flower][2]+"人へピッタリな花になっています", flower_lang[flower][3]+"-color"]
    return render_template("confirmation.html", preference=preference, feeling_word=feeling_word, merchandise=merchandise)

# お会計を選ぶページ
@app.route("/bill/<shape>/<feeling>/<int:words>/<flower>", methods=["GET"])
def bill(shape, feeling, words, flower):
    preference = Preference(shape=shape, feeling=feeling, words=words, flower=flower)
    return render_template("bill.html", preference=preference)

# 案内番号ページ
@app.route("/completion", methods=["GET"])
def completion():
    return render_template("completion.html")

# お任せ　感情を選ぶページ
@app.route("/select_feeling_uptoyou/", methods=["GET"])
def select_feeling_uptoyou():
    return render_template("/uptoyou/select_feeling_uptoyou.html")

# お任せ　花を選ぶページ
@app.route("/select_flower_uptoyou/<feeling>", methods=["GET"])
def select_flower_uptoyou(feeling):
    if feeling == "love":
        index = random.randint(0, len(feeling_words[feeling])-1)
        flower = love_reasonable[index]
        feeling_word = feeling_words[feeling][index]
    elif feeling == "thanks":
        index = random.randint(0, len(feeling_words[feeling])-1)
        flower = thanks_reasonable[index]
        feeling_word = feeling_words[feeling][index]
    elif feeling == "celebration":
        index = random.randint(0, len(feeling_words[feeling])-1)
        flower = celebration_reasonable[index]
        feeling_word = feeling_words[feeling][index]
    else:
        index = random.randint(0, len(feeling_words[feeling])-1)
        flower = business_reasonable[index]
        feeling_word = feeling_words[feeling][index]
    preference = Preference(feeling=feeling, words=index)
    
    merchandise=[flower, "image/merchandise/"+flower+".webp", flower_lang[flower][1], "この花には"+flower_lang[flower][2]+"人へピッタリな花になっています", flower_lang[flower][3]+"-color"]

    return render_template("/uptoyou/select_flower_uptoyou.html", feeling_word=feeling_word,\
                           merchandise=merchandise, preference=preference)

# お任せ　カタチを選ぶページ
@app.route("/select_shape/<feeling>/<int:words>/<flower>", methods=["GET"])
def select_shape_uptoyou(feeling, words, flower):
    preference = Preference(feeling=feeling, words=words, flower=flower)
    feeling_word = feeling_words[feeling][words]
    merchandise=[flower, "image/merchandise/"+flower+".webp", flower_lang[flower][1], "この花には"+flower_lang[flower][2]+"人へピッタリな花になっています", flower_lang[flower][3]+"-color"]
    return render_template("/uptoyou/select_shape_uptoyou.html", preference=preference, feeling_word=feeling_word,\
                           merchandise=merchandise)

# みんなの花束を参考にするページ ※名前は後で変える
@app.route("/reference1", methods=["GET"])
def reference1():
    return render_template("/reference/reference1.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)