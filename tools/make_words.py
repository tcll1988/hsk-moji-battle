# 使い方: python3 tools/make_words.py path/to/hsk1.json
#  hsk1.json = https://raw.githubusercontent.com/drkameleon/complete-hsk-vocabulary/main/wordlists/exclusive/old/1.json
#  出力: data/words.json, data/words.js（ゲームが読み込む）, words_check.csv（先生の確認用）
import json,csv,os
HERE=os.path.dirname(os.path.abspath(__file__)); APP=os.path.dirname(HERE)
src=json.load(open(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'hsk1.json'))
by={w['simplified']:w for w in src}
# (hanzi, chosen numeric reading from the source forms or None=first, Japanese gloss (AI-written))
G=[
("あいさつ・ひと",[("你",None,"あなた"),("我",None,"わたし"),("他",None,"彼"),("她",None,"彼女"),("我们",None,"わたしたち"),("人",None,"人"),("谢谢",None,"ありがとう"),("不客气",None,"どういたしまして"),("对不起",None,"ごめんなさい"),("没关系",None,"かまいません・大丈夫です"),("再见",None,"さようなら"),("喂","wei4","（電話で）もしもし"),("请",None,"どうぞ（～してください）"),("名字",None,"名前"),("叫","jiao4","（名前を）～という")]),
("かず",[("一",None,"1"),("二",None,"2"),("三","san1","3"),("四",None,"4"),("五",None,"5"),("六",None,"6"),("七",None,"7"),("八",None,"8"),("九",None,"9"),("十",None,"10"),("零",None,"ゼロ・0"),("几","ji3","いくつ（10未満）"),("多少","duo1 shao5","どのくらい・いくら（数量）"),("岁","sui4","～歳"),("个","ge4","～個（量詞）")]),
("かぞく・しごと",[("爸爸",None,"お父さん"),("妈妈",None,"お母さん"),("儿子",None,"息子"),("女儿",None,"娘"),("朋友",None,"友だち"),("老师",None,"先生（教師）"),("学生",None,"学生"),("同学",None,"クラスメート"),("医生",None,"医者"),("先生",None,"（男性への敬称）～さん"),("小姐",None,"（若い女性への敬称）～さん"),("谁",None,"だれ")]),
("じかん",[("今天",None,"今日"),("明天",None,"明日"),("昨天",None,"昨日"),("年","nian2","年"),("月",None,"月"),("日","ri4","日"),("星期",None,"週・曜日"),("上午",None,"午前"),("中午",None,"昼・正午"),("下午",None,"午後"),("现在",None,"今"),("时候",None,"とき"),("点",None,"～時"),("分钟",None,"～分間")]),
("たべもの・かいもの",[("吃","chi1","食べる"),("喝","he1","飲む"),("菜",None,"料理・おかず"),("茶",None,"お茶"),("米饭",None,"ごはん"),("水","shui3","水"),("水果",None,"果物"),("苹果",None,"りんご"),("杯子",None,"コップ"),("饭馆",None,"レストラン・食堂"),("钱","qian2","お金"),("块",None,"～元（お金の単位）"),("买",None,"買う")]),
("ばしょ・のりもの",[("北京",None,"北京"),("中国",None,"中国"),("学校",None,"学校"),("医院",None,"病院"),("商店",None,"店"),("火车站",None,"（鉄道の）駅"),("出租车",None,"タクシー"),("飞机",None,"飛行機"),("家","jia1","家・家庭"),("里","li3","～の中"),("前面",None,"前"),("后面",None,"後ろ"),("上","shang4","上"),("下",None,"下")]),
("うごき①",[("爱",None,"愛する・大好きだ"),("喜欢",None,"好きだ"),("想",None,"～したい・思う"),("看","kan4","見る・読む"),("看见",None,"見える・目に入る"),("听","ting1","聞く"),("说话",None,"話す"),("读","du2","（声に出して）読む"),("写",None,"書く"),("学习",None,"勉強する"),("工作",None,"仕事・働く"),("做",None,"する・作る"),("打电话",None,"電話をかける")]),
("うごき②",[("去",None,"行く"),("来",None,"来る"),("回","hui2","帰る・戻る"),("住",None,"住む・泊まる"),("在",None,"～にいる・ある"),("坐","zuo4","座る・（乗り物に）乗る"),("开",None,"開ける・運転する"),("睡觉",None,"寝る"),("下雨",None,"雨が降る"),("认识",None,"知り合う・知っている"),("会","hui4","（習って）できる"),("能","neng2","（能力・条件的に）できる"),("有",None,"持っている・ある"),("是","shi4","～である")]),
("もの・てんき",[("书","shu1","本"),("字",None,"字"),("东西","dong1 xi5","もの"),("衣服",None,"服"),("椅子",None,"いす"),("桌子",None,"机・テーブル"),("电脑",None,"パソコン"),("电视",None,"テレビ"),("电影",None,"映画"),("猫",None,"猫"),("狗",None,"犬"),("天气",None,"天気"),("热",None,"暑い・熱い"),("冷","leng3","寒い・冷たい")]),
("ようす",[("大","da4","大きい"),("小",None,"小さい"),("多",None,"多い"),("少","shao3","少ない"),("好","hao3","よい"),("高兴",None,"うれしい"),("漂亮",None,"きれいだ"),("很",None,"とても"),("太",None,"あまりにも・～すぎる"),("都","dou1","みんな・すべて"),("不",None,"～ない（否定）"),("没","mei2","～していない・ない"),("汉语",None,"中国語")]),
("ぎもん・ことば",[("什么",None,"なに"),("哪","na3","どれ・どの"),("那","na4","あれ・それ"),("这",None,"これ・この"),("怎么",None,"どうやって・なぜ"),("怎么样",None,"どうですか"),("呢","ne5","～は？（疑問）"),("吗","ma5","～か？（疑問）"),("的","de5","～の"),("了","le5","～した（完了）"),("和","he2","～と"),("些",None,"いくつか（量詞）"),("本","ben3","～冊（量詞）")]),
]
out=[];seen=set();rows=[]
for si,(name,ws) in enumerate(G):
  for h,num,ja in ws:
    w=by[h]; forms=w['forms']
    if num is None: f=forms[0]
    else:
      c=[f for f in forms if f['transcriptions']['numeric'].lower()==num]; assert c,(h,num,[f['transcriptions']['numeric'] for f in forms])
      c.sort(key=lambda f: f['transcriptions']['pinyin'][:1].isupper()); f=c[0]  # 固有名詞（姓など）の大文字形より普通の語を優先
    t=f['transcriptions']; seen.add(h)
    out.append(dict(h=h,py=t['pinyin'],num=t['numeric'].lower(),ja=ja,en=f['meanings'][0],s=si))
    alts=sorted({x['transcriptions']['pinyin'] for x in forms}-{t['pinyin']})
    rows.append([h,t['pinyin'],t['numeric'],ja,si+1,name,('出典の他の読み: '+' / '.join(alts)+' → 採用: '+t['pinyin']) if alts else '',"pinyin: complete-hsk-vocabulary (old HSK1, MIT); 日本語: AI作成・要確認"])
missing=set(by)-seen; assert not missing,missing
assert len(out)==150
data={"stages":[g[0] for g in G],"words":out}
json.dump(data,open(os.path.join(APP,'data','words.json'),'w'),ensure_ascii=False,indent=0)
open(os.path.join(APP,'data','words.js'),'w').write('/* 自動生成（tools/make_words.py）。単語を直すときはスクリプトを編集して再生成してください */\nwindow.HSK_DATA = '+json.dumps(data,ensure_ascii=False)+';\n')
with open(os.path.join(APP,'words_check.csv'),'w',newline='',encoding='utf-8-sig') as fp:
  wr=csv.writer(fp); wr.writerow(["漢字","ピンイン","数字ピンイン","日本語訳(AI作成・要確認)","ステージ","グループ","多音字メモ","出典"]); wr.writerows(rows)
print(len(out),[len(g[1]) for g in G])
