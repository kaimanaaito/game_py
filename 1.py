#%%
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# ページ設定
st.set_page_config(
    page_title="行動経済学診断ツール", 
    layout="centered", 
    page_icon="🧠",
    initial_sidebar_state="expanded"
)
st.title("🧠 深層心理バイアス診断")

# カスタムスタイル
def local_css():
    st.markdown("""
    <style>
        .stProgress > div > div > div {
            background-color: #4B8BBE;
        }
        .st-bb {
            background-color: #F0F2F6;
        }
        .st-at {
            background-color: #306998;
        }
        div[data-testid="stExpander"] div[role="button"] p {
            font-size: 1.2rem;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
local_css()

# カスタムカラーパレット
colors = {
    "primary": "#4B8BBE",
    "secondary": "#306998",
    "accent": "#FFE873",
    "background": "#F0F2F6",
    "text": "#1A1A1A",
    "warning": "#FF6B6B",
    "success": "#4ECDC4"
}

# バイアスカテゴリ定義（拡張版）
BIAS_CATEGORIES = {
    "損失回避": {
        "desc": "損失を利益よりも大きく感じる傾向",
        "icon": "💸",
        "actions": [
            "投資判断では『現在の価値』だけに注目",
            "『損切りルール』を事前に設定",
            "損失を『学びのコスト』と再定義"
        ]
    },
    "サンクコスト": {
        "desc": "既に投資したコストに引きずられる傾向", 
        "icon": "⏳",
        "actions": [
            "意思決定時『これから得られるもの』だけを評価",
            "『沈没コスト』という用語を意識的に使用",
            "毎月サブスクの見直し日を設定"
        ]
    },
    "アンカリング": {
        "desc": "最初に提示された情報に影響される傾向",
        "icon": "⚓",
        "actions": [
            "重要な買い物では複数店舗を比較",
            "『最初に見た価格』をメモしない",
            "相場調査は匿名で行う"
        ]
    },
    "現在バイアス": {
        "desc": "現在の利益を未来の利益より重視する傾向",
        "icon": "⏱️",
        "actions": [
            "未来の自分に手紙を書く",
            "長期目標を可視化してデスクに掲示",
            "24時間ルール（衝動買いは1日待つ）"
        ]
    },
    "社会的証明": {
        "desc": "周囲の行動に影響される傾向",
        "icon": "👥",
        "actions": [
            "『自分だけの評価基準』を作成",
            "商品レビューは低評価から読む",
            "購買前に『本当に必要か』3回自問"
        ]
    },
    "確証バイアス": {
        "desc": "自己の信念を支持する情報ばかり集める傾向",
        "icon": "🔍",
        "actions": [
            "反対意見を意図的に探す習慣",
            "『悪魔の代弁者』役を設定",
            "意思決定前に反対理由を10個挙げる"
        ]
    },
    "フレーミング効果": {
        "desc": "表現方法で選択が変わる傾向",
        "icon": "🖼️",
        "actions": [
            "情報を複数の表現で見直す",
            "数値データを絶対値で確認",
            "逆フレーミングを練習する"
        ]
    },
    "希少性の原理": {
        "desc": "稀少なものに価値を感じる傾向",
        "icon": "🏆",
        "actions": [
            "『限定』表示を疑う習慣",
            "人工的希少性を見抜く",
            "需要と供給の関係を考える"
        ]
    },
    "返報性の原理": {
        "desc": "受けた恩義に報いたくなる傾向",
        "icon": "🔄",
        "actions": [
            "贈り物の意図を考える",
            "即時の返礼を避ける",
            "心理的負債を作らない"
        ]
    },
    "同調圧力": {
        "desc": "集団の意見に合わせようとする傾向",
        "icon": "👥",
        "actions": [
            "『みんな』の具体性を問う",
            "少数意見を積極的に探す",
            "匿名で意見を形成する"
        ]
    },
    "楽観バイアス": {
        "desc": "自分は平均より優れていると思う傾向",
        "icon": "😊",
        "actions": [
            "統計データと自己評価を比較",
            "最悪のシナリオを想定",
            "外部意見を取り入れる"
        ]
    },
    "後知恵バイアス": {
        "desc": "結果を知った後で予測可能だったと思い込む傾向",
        "icon": "🔮",
        "actions": [
            "意思決定理由を事前に記録",
            "不確実性を受け入れる",
            "複数シナリオを想定"
        ]
    },
    "代表性ヒューリスティック": {
        "desc": "典型例にあてはめて判断する傾向",
        "icon": "🎯",
        "actions": [
            "統計的基準率を確認",
            "固定観念を疑う",
            "個別事例の特殊性を考慮"
        ]
    },
    "可用性ヒューリスティック": {
        "desc": "思い出しやすい情報を重視する傾向",
        "icon": "💭",
        "actions": [
            "メディア情報の偏りを意識",
            "統計データを積極的に調べる",
            "個人的体験と全体傾向を区別"
        ]
    },
    "プロスペクト理論": {
        "desc": "確実な利益と不確実な利益を異なって評価する傾向",
        "icon": "🎲",
        "actions": [
            "期待値計算を習慣化",
            "リスクの本質を理解",
            "確率的思考を身につける"
        ]
    }
}

# 問題データ（大幅拡張）
categories = {
    "消費行動": [
        {
            "question": "【Q1】スマホ購入で悩んでいます。店員に『このモデルは今月だけ限定20%オフ、在庫残り5台』と言われました。どうしますか？",
            "options": ["即座に購入する", "一度帰って他店と比較する", "必要性を再検討する"],
            "correct": "必要性を再検討する",
            "bias": "希少性の原理",
            "explanation": "『限定』『残り僅か』は典型的な希少性演出です。本当に必要かどうかの判断が先決です。"
        },
        {
            "question": "【Q2】オンラインショッピングで2万円の商品をカートに入れました。送料800円を見て『あと1000円で送料無料』の表示が。どうしますか？",
            "options": ["送料無料まで追加購入する", "必要な商品のみ購入する", "購入を中止する"],
            "correct": "必要な商品のみ購入する",
            "bias": "アンカリング",
            "explanation": "『送料無料』に惑わされて不要な買い物をするのは、800円を節約するために1000円使う不合理な行動です。"
        },
        {
            "question": "【Q3】3年前に15万円で購入したブランドバッグ、今は3万円でしか売れません。使用頻度は年に2回程度。どうしますか？",
            "options": ["思い出があるので保管する", "損失を受け入れて売却する", "もう少し相場回復を待つ"],
            "correct": "損失を受け入れて売却する",
            "bias": "損失回避",
            "explanation": "既に価値は下がっており、使わないなら売却が合理的。『元の価格』に固執するのは損失回避バイアスです。"
        },
        {
            "question": "【Q4】カフェで友人が『みんなこのスイーツ頼んでるよ』と言いました。あなたは甘いものを控えているところです。どうしますか？",
            "options": ["周りに合わせてスイーツを注文", "自分の方針を貫く", "友人に影響されて迷いを感じる"],
            "correct": "自分の方針を貫く",
            "bias": "社会的証明",
            "explanation": "『みんな』という曖昧な多数派アピールに流されず、自分の目標を優先することが重要です。"
        },
        {
            "question": "【Q5】定期購読している雑誌（月1200円）、最近ほとんど読んでいません。年間契約なので解約すると違約金3000円。どうしますか？",
            "options": ["違約金を避けて継続する", "違約金を払って即解約する", "契約満了まで続ける"],
            "correct": "違約金を払って即解約する",
            "bias": "サンクコスト",
            "explanation": "読まない雑誌に毎月1200円払うより、3000円の違約金で止める方が長期的に合理的です。"
        },
        {
            "question": "【Q6】ECサイトでレビュー★4.8の商品と★4.2の商品で迷っています。★4.8は100件のレビュー、★4.2は5000件のレビューです。どちらを選びますか？",
            "options": ["★4.8の商品（100件）", "★4.2の商品（5000件）", "レビュー以外の要素で判断"],
            "correct": "★4.2の商品（5000件）",
            "bias": "代表性ヒューリスティック",
            "explanation": "サンプル数が大きい方が統計的に信頼性が高い。100件の★4.8は偏った評価の可能性があります。"
        },
        {
            "question": "【Q7】クレジットカードの年会費1万円、ポイント還元で年8000円相当獲得。『実質年会費2000円』という表現をどう捉えますか？",
            "options": ["お得だと感じる", "年会費1万円として考える", "ポイント使用の手間を考慮する"],
            "correct": "ポイント使用の手間を考慮する",
            "bias": "フレーミング効果",
            "explanation": "ポイントは現金ではなく、使用制限や有効期限があります。『実質』という表現に惑わされないことが重要です。"
        }
    ],
    "投資・貯蓄": [
        {
            "question": "【Q8】投資信託Aは過去5年で年率8%、投資信託Bは過去1年で年率15%。どちらに投資しますか？",
            "options": ["5年実績のA", "1年実績のB", "もっと長期データを調べる"],
            "correct": "もっと長期データを調べる",
            "bias": "可用性ヒューリスティック",
            "explanation": "直近の高い成績に目を奪われがちですが、長期の安定性の方が重要。より多くのデータが必要です。"
        },
        {
            "question": "【Q9】株式投資で30万円の含み損。『損切りすべき』という意見と『持ち続けるべき』という意見の両方をネットで見つけました。どうしますか？",
            "options": ["損切り意見を支持する記事をさらに探す", "持続意見を支持する記事をさらに探す", "両方の根拠を冷静に比較検討する"],
            "correct": "両方の根拠を冷静に比較検討する",
            "bias": "確証バイアス",
            "explanation": "自分の希望に沿う情報ばかり探すのは確証バイアス。反対意見も平等に検討することが重要です。"
        },
        {
            "question": "【Q10】『年利3%保証』の定期預金と『年利期待値5%（変動あり）』の投資商品、どちらを選びますか？",
            "options": ["確実な3%を選ぶ", "期待値5%にチャレンジ", "リスク許容度を詳しく検討する"],
            "correct": "リスク許容度を詳しく検討する",
            "bias": "プロスペクト理論",
            "explanation": "確実性を過大評価する傾向があります。自分のリスク許容度と投資期間を総合的に判断することが重要です。"
        },
        {
            "question": "【Q11】仮想通貨で投資額が半分に。友人は『今買い増しのチャンス』、別の友人は『早く逃げろ』と言います。どうしますか？",
            "options": ["友人の成功体験を信じて買い増し", "友人の警告を聞いて売却", "自分で情報収集して判断"],
            "correct": "自分で情報収集して判断",
            "bias": "社会的証明",
            "explanation": "投資判断を他人の意見で決めるのは危険。自分のリスク許容度と投資方針で判断すべきです。"
        },
        {
            "question": "【Q12】住宅ローンの繰上返済で悩んでいます。『金利1%だから投資の方が有利』という意見と『確実な1%リターン』という意見があります。どう考えますか？",
            "options": ["投資でより高いリターンを狙う", "確実な1%を取って繰上返済", "家計全体のバランスで判断"],
            "correct": "家計全体のバランスで判断",
            "bias": "フレーミング効果",
            "explanation": "『確実な1%』と『期待リターン3%』は同じではありません。リスクと安心感を総合的に判断が必要です。"
        }
    ],
    "人間関係": [
        {
            "question": "【Q13】職場の送別会の幹事に任命されました。予算は一人5000円。高級店Aは一人6000円、普通の店Bは一人4000円。どうしますか？",
            "options": ["高級店で印象良く（自腹1000円）", "予算内の普通の店にする", "参加者に予算超過を相談する"],
            "correct": "参加者に予算超過を相談する",
            "bias": "返報性の原理",
            "explanation": "『良い印象を与えたい』という心理で自腹を切るのは返報性の罠。透明性を保つことが重要です。"
        },
        {
            "question": "【Q14】SNSで『○○さんの投稿に感動しました』とコメントしたら、相手からも『いいね』が急に増えました。どう解釈しますか？",
            "options": ["相互関係が良好になった", "お返しの義務感かもしれない", "偶然の一致"],
            "correct": "お返しの義務感かもしれない",
            "bias": "返報性の原理",
            "explanation": "SNSでは返報性原理が強く働きます。相手の行動が義務感からか本心からかを冷静に判断することが大切です。"
        },
        {
            "question": "【Q15】部署の飲み会で『全員参加予定』と聞きました。あなたは家族との時間を大切にしたいのですが、どうしますか？",
            "options": ["空気を読んで参加する", "理由を説明して欠席する", "体調不良を理由に欠席する"],
            "correct": "理由を説明して欠席する",
            "bias": "同調圧力",
            "explanation": "『全員参加』という同調圧力に屈せず、自分の価値観を正直に伝えることが長期的に良い関係を築きます。"
        },
        {
            "question": "【Q16】マッチングアプリで知り合った人から高価なプレゼントをもらいました。まだ数回しか会っていません。どう対応しますか？",
            "options": ["嬉しく受け取る", "丁寧に断る", "同程度のお返しをする"],
            "correct": "丁寧に断る",
            "bias": "返報性の原理",
            "explanation": "関係性に不釣り合いな贈り物は相手に心理的負債を作らせる手法の可能性があります。"
        }
    ],
    "健康・生活": [
        {
            "question": "【Q17】健康診断で『要経過観察』。ネットで調べると『90%は問題なし』という情報と『早期発見が重要』という情報の両方を発見。どうしますか？",
            "options": ["90%を信じて様子見", "早期発見を重視して精密検査", "医師に詳しく相談する"],
            "correct": "医師に詳しく相談する",
            "bias": "確証バイアス",
            "explanation": "安心したい気持ちで楽観的情報に偏ったり、逆に不安で悲観的情報に偏るのは危険。専門家の判断が重要です。"
        },
        {
            "question": "【Q18】ジムの入会で『今だけ入会金無料、月会費3ヶ月半額』のキャンペーン。通常入会は来月から。どうしますか？",
            "options": ["キャンペーンを利用して即入会", "来月の通常入会を待つ", "本当に継続できるか検討する"],
            "correct": "本当に継続できるか検討する",
            "bias": "現在バイアス",
            "explanation": "『今だけ』という緊急性に惑わされず、継続的な利用可能性を冷静に評価することが重要です。"
        },
        {
            "question": "【Q19】新しいダイエット方法が話題です。『1ヶ月で5kg減』という成功例がSNSで多数投稿されています。どう判断しますか？",
            "options": ["成功例が多いので試してみる", "医学的根拠を調べる", "友人の体験談を聞く"],
            "correct": "医学的根拠を調べる",
            "bias": "可用性ヒューリスティック",
            "explanation": "SNSの成功例は目立ちやすいだけで、失敗例や健康被害は表に出にくい。科学的根拠の確認が必要です。"
        },
        {
            "question": "【Q20】睡眠改善アプリに月額980円課金中。3ヶ月使って効果を実感できません。どうしますか？",
            "options": ["もう少し続けてみる", "すぐに解約する", "無料の代替方法を探す"],
            "correct": "すぐに解約する",
            "bias": "サンクコスト",
            "explanation": "既に支払った金額に固執せず、効果のないサービスは早期に見切りをつけることが合理的です。"
        },
        {
            "question": "【Q21】コロナワクチンの副作用について、友人から『周りで重篤な副作用が3人もいた』と聞きました。どう考えますか？",
            "options": ["友人の体験を重視する", "統計データを確認する", "医師に相談する"],
            "correct": "統計データを確認する",
            "bias": "可用性ヒューリスティック",
            "explanation": "身近な体験談は印象に残りやすいですが、全体の統計と比較することで正しいリスク評価ができます。"
        }
    ],
    "仕事・キャリア": [
        {
            "question": "【Q22】転職活動中、A社は年収50万円アップ＋残業多め、B社は年収据え置き＋ワークライフバランス良好。どちらを選びますか？",
            "options": ["年収アップのA社", "バランス重視のB社", "長期的な価値で判断する"],
            "correct": "長期的な価値で判断する",
            "bias": "現在バイアス",
            "explanation": "目先の年収アップに惑わされず、健康、家族時間、スキルアップなどの長期的価値を総合判断することが重要です。"
        },
        {
            "question": "【Q23】新しいプロジェクトに6ヶ月間取り組んでいますが、成果が見えません。上司は継続を指示していますが、あなたはどうしますか？",
            "options": ["上司の指示に従い継続", "プロジェクトの見直しを提案", "密かに他の業務に集中する"],
            "correct": "プロジェクトの見直しを提案",
            "bias": "サンクコスト",
            "explanation": "既に投資した時間に固執せず、客観的にプロジェクトの価値を評価し直すことが重要です。"
        },
        {
            "question": "【Q24】資格取得のため通信講座に10万円支払い、テキストが届きました。しかし最近、その資格の市場価値が下がっていることを知りました。どうしますか？",
            "options": ["既に払ったので最後まで続ける", "損失を受け入れて中止する", "他の有用な資格に変更できないか確認する"],
            "correct": "他の有用な資格に変更できないか確認する",
            "bias": "サンクコスト",
            "explanation": "既に支払った費用に固執せず、現在の状況に最適な選択肢を探ることが合理的です。"
        },
        {
            "question": "【Q25】会社の業績発表で『前年比120%成長』と発表されました。しかし詳しく調べると、前年が異常に悪い年だったことが判明。どう評価しますか？",
            "options": ["120%成長を素直に評価", "異常年との比較なので割り引いて評価", "他社との比較も含めて総合評価"],
            "correct": "他社との比較も含めて総合評価",
            "bias": "アンカリング",
            "explanation": "前年という特定の基準点（アンカー）に固執せず、業界全体や長期トレンドと比較することが重要です。"
        }
    ],
    "教育・学習": [
        {
            "question": "【Q26】オンライン英会話を始めて3ヶ月、上達を実感できません。『3ヶ月で話せるようになる』という広告を信じて始めたのですが、どうしますか？",
            "options": ["広告が間違っていたと判断してやめる", "個人差があるのでもう少し続ける", "学習方法を見直す"],
            "correct": "学習方法を見直す",
            "bias": "楽観バイアス",
            "explanation": "『3ヶ月で話せる』という楽観的な期待に現実が追いつかないのは自然。方法論の見直しが建設的です。"
        },
        {
            "question": "【Q27】プログラミングスクールの広告で『卒業生の95%が転職成功』とありました。受講料は60万円。どう判断しますか？",
            "options": ["95%という数字を信頼して申し込む", "統計の詳細を確認する", "他のスクールと比較する"],
            "correct": "統計の詳細を確認する",
            "bias": "代表性ヒューリスティック",
            "explanation": "95%の定義（どの期間？どんな条件？）や母数を確認せずに判断するのは危険です。"
        },
        {
            "question": "【Q28】子供の塾選びで、A塾は『東大合格者100名』、B塾は『東大合格率20%』と宣伝しています。どちらを重視しますか？",
            "options": ["合格者数100名のA塾", "合格率20%のB塾", "両方の規模と実態を確認する"],
            "correct": "両方の規模と実態を確認する",
            "bias": "フレーミング効果",
            "explanation": "絶対数と割合では印象が変わります。A塾が1000人中100人、B塾が10人中2人の可能性もあります。"
        }
    ]
}

# グラデーションカラーマップ作成
def create_gradient_cmap():
    colors = ["#FF6B6B", "#FFE66D", "#4ECDC4"]
    return LinearSegmentedColormap.from_list("bias_gradient", colors)

# サイドバー設定
with st.sidebar:
    st.header("診断設定")
    category = st.selectbox(
        "診断カテゴリを選択：",
        list(categories.keys()),
        help="あなたが診断したい分野を選択してください"
    )
    
    st.markdown("---")
    st.markdown("### バイアス解説")
    selected_bias = st.selectbox(
        "事前に学びたいバイアス：",
        list(BIAS_CATEGORIES.keys()),
        format_func=lambda x: f"{BIAS_CATEGORIES[x]['icon']} {x}"
    )
    st.write(f"**{BIAS_CATEGORIES[selected_bias]['desc']}**")
    st.write("📌 対策例：")
    for action in BIAS_CATEGORIES[selected_bias]['actions']:
        st.caption(f"• {action}")

# メインコンテンツ
st.markdown(f"## 🔍 {category} の深層心理診断")
st.caption("日常生活に潜む不合理な判断パターンを発見しましょう")

# 診断実施
score = 0
bias_count = {bias: 0 for bias in BIAS_CATEGORIES}
user_answers = []
selected_questions = categories[category]

for i, q in enumerate(selected_questions):
    st.markdown(f"### {q['question']}")
    user_answer = st.radio(
        f"選択肢：",
        q['options'],
        key=f"q{i}",
        index=None,
        horizontal=True
    )
    
    if user_answer:
        user_answers.append({
            "question": q['question'],
            "user_choice": user_answer,
            "correct_choice": q['correct'],
            "bias": q['bias'],
            "explanation": q['explanation']
        })
        
        if user_answer == q['correct']:
            score += 1
        else:
            # バイアスが定義されていることを確認
            if q['bias'] in bias_count:
                bias_count[q['bias']] += 1
            else:
                st.warning(f"未定義のバイアスが検出されました: {q['bias']}")

# 診断結果の表示
if st.button("診断結果を表示", type="primary", use_container_width=True):
    if len(user_answers) < len(selected_questions):
        st.warning("⚠️ すべての質問に回答してから診断結果を表示してください。")
    else:
        st.markdown("---")
        
        # ヘッダー
        st.subheader("🔍 診断結果")
        col1, col2, col3 = st.columns([1,1,2])
        
        with col1:
            st.metric(
                "正解数", 
                f"{score}/{len(selected_questions)}",
                help="正解数が少ないほどバイアスの影響が強い"
            )
        
        with col2:
            ratio = score/len(selected_questions)
            st.metric(
                "正解率", 
                f"{int(ratio*100)}%",
                delta=f"{'+' if ratio > 0.5 else ''}{int((ratio-0.5)*100)}%",
                delta_color="inverse"
            )
        
        with col3:
            st.caption("※正解率50%が基準値（高いほど合理的）")
        
        # バイアス分布の可視化（検出されたバイアスのみ表示）
        detected_biases = {k: v for k, v in bias_count.items() if v > 0}
        
        if detected_biases:
            st.markdown("### 📊 あなたのバイアス強度マップ")
            biases = list(detected_biases.keys())
            counts = list(detected_biases.values())
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # グラデーションバー作成
            cmap = create_gradient_cmap()
            bar_colors = cmap(np.linspace(0, 1, len(biases)))
            
            bars = ax.barh(
                biases, 
                counts, 
                color=bar_colors, 
                edgecolor='white', 
                linewidth=2,
                height=0.6
            )
            
            # 3D効果追加
            for bar in bars:
                bar.set_hatch("///")
                bar.set_alpha(0.9)
            
            # デザイン調整
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(colors["text"])
            ax.spines['bottom'].set_color(colors["text"])
            
            ax.set_xlabel('バイアス検出回数', fontsize=12, color=colors["text"])
            ax.set_title('各バイアスの相対的強度', 
                        pad=20, fontsize=14, color=colors["text"], weight='bold')
            
            # バーラベル追加
            for i, (b, c) in enumerate(zip(biases, counts)):
                ax.text(
                    c + 0.1, 
                    i, 
                    f"{c}回",
                    va='center', 
                    color=colors["text"],
                    fontweight='bold'
                )
            
            # 日本語フォント対応
            plt.rcParams['font.family'] = ['DejaVu Sans', 'Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
            
            st.pyplot(fig)
        else:
            st.success("🎯 検出された強いバイアスはありませんでした！")
            st.balloons()
        
        # 総合評価
        st.markdown("### 📝 総合評価")
        ratio = score / len(selected_questions)
        
        if ratio >= 0.8:
            st.success(f"**🎖️ 優秀！ 深層心理バイアスに囚われない合理的思考ができています**")
            st.write("""
            - ✅ 感情より事実を重視する判断力
            - ✅ マーケティング手法を見抜く洞察力  
            - ✅ 統計的・論理的思考力
            - ✅ 長期的視点での意思決定能力
            """)
        elif ratio >= 0.6:
            st.info(f"**🧠 良好！ バイアスを意識しつつも、時々影響を受けています**")
            st.write("""
            - ⚠️ 特定の状況で感情的判断をしがち
            - ⚠️ 『お得』という表現に弱い傾向
            - ⚠️ 周囲の意見に影響されることがある
            - ✅ 基本的な論理的思考は身についている
            """)
        elif ratio >= 0.4:
            st.warning(f"**⚠️ 要注意！ 複数のバイアスの影響を受けています**")
            st.write("""
            - ❌ 広告文句や営業トークに弱い
            - ❌ 過去の選択に固執しがち  
            - ❌ 数字の表現方法に大きく影響される
            - ❌ 短期的な利益を過大評価する傾向
            """)
        else:
            st.error(f"**🚨 改善必要！ 強い心理的バイアスの影響下にあります**")
            st.write("""
            - 🔴 感情的な判断が論理的判断を上回っている
            - 🔴 『みんながやっている』という同調圧力に弱い
            - 🔴 数字よりも物語やイメージに強く影響される
            - 🔴 長期的視点よりも目先の利益を重視
            """)
        
        # 個別問題の詳細解説
        st.markdown("### 🔍 あなたの回答分析")
        
        correct_answers = [ans for ans in user_answers if ans['user_choice'] == ans['correct_choice']]
        incorrect_answers = [ans for ans in user_answers if ans['user_choice'] != ans['correct_choice']]
        
        if correct_answers:
            with st.expander(f"✅ 正解した問題 ({len(correct_answers)}件)", expanded=False):
                for ans in correct_answers:
                    st.write(f"**Q:** {ans['question']}")
                    st.write(f"**あなたの選択:** `{ans['user_choice']}` ✅")
                    st.write(f"**解説:** {ans['explanation']}")
                    st.write("---")
        
        if incorrect_answers:
            with st.expander(f"❌ バイアスが検出された問題 ({len(incorrect_answers)}件)", expanded=True):
                for ans in incorrect_answers:
                    st.write(f"**Q:** {ans['question']}")
                    st.write(f"**あなたの選択:** `{ans['user_choice']}` ❌")
                    st.write(f"**推奨回答:** `{ans['correct_choice']}`")
                    st.write(f"**検出バイアス:** {BIAS_CATEGORIES[ans['bias']]['icon']} {ans['bias']}")
                    st.write(f"**解説:** {ans['explanation']}")
                    st.write("---")
        
        # バイアス詳細解説と改善方法
        if detected_biases:
            st.markdown("### 🛠️ 個別バイアス対策法")
            for bias, count in detected_biases.items():
                with st.expander(f"{BIAS_CATEGORIES[bias]['icon']} **{bias}バイアス** (検出: {count}回)", expanded=True):
                    st.write(f"**{BIAS_CATEGORIES[bias]['desc']}**")
                    
                    # 具体的事例
                    st.markdown("##### 🧪 あなたの具体例:")
                    bias_examples = [ans for ans in user_answers if ans['bias'] == bias and ans['user_choice'] != ans['correct_choice']]
                    for ans in bias_examples:
                        st.write(f"- ✖️ {ans['question']}")
                        st.write(f"  → あなたの選択: `{ans['user_choice']}` (推奨: `{ans['correct_choice']}`)")
                        st.write(f"  💡 **なぜこうなったか**: {ans['explanation']}")
                        st.write("")
                    
                    # 改善アクション
                    st.markdown("##### 🎯 科学的改善方法:")
                    for i, action in enumerate(BIAS_CATEGORIES[bias]['actions']):
                        st.write(f"{i+1}. **{action}**")
                    
                    # 日常での実践方法
                    st.markdown("##### 📅 今日から始められる実践法:")
                    practice_tips = {
                        "損失回避": ["投資前に最大損失額を決める", "月1回ポートフォリオを見直す", "損失を『授業料』として記録する"],
                        "サンクコスト": ["意思決定時に『これまでのコスト』を考慮しない練習", "定期的なサブスクリプション見直し日を設定", "『やめる勇気』を評価する"],
                        "アンカリング": ["複数の情報源から価格を調べる習慣", "最初の価格を無視する練習", "相場観を養うため定期的に市場調査"],
                        "現在バイアス": ["未来の自分への手紙を書く", "長期目標を毎日見る場所に掲示", "衝動的な決断は24時間待つルール"],
                        "社会的証明": ["自分だけの判断基準リストを作る", "『みんな』の具体的な人数を確認する癖", "少数派の意見を意識的に探す"],
                        "確証バイアス": ["自分の意見に反対する記事を必ず1つ読む", "友人に『反対意見』を求める", "決断前に反対理由を3つ挙げる"],
                        "フレーミング効果": ["数値は必ず絶対値で確認", "複数の表現で同じ情報を見る", "％と実数の両方で確認する習慣"],
                        "希少性の原理": ["『限定』『残りわずか』を見たら一度立ち止まる", "人工的希少性を見抜く練習", "本当の需要と供給を調べる"],
                        "返報性の原理": ["贈り物の意図を考える習慣", "すぐにお返しせず時間を置く", "心理的な負債を作らないよう意識"],
                        "同調圧力": ["『みんな』の正体を具体的に確認", "匿名で自分の意見を整理する時間を作る", "少数派でいることに慣れる"],
                        "楽観バイアス": ["統計データと自分の予測を比較記録", "最悪シナリオを必ず想定", "第三者の意見を積極的に求める"],
                        "後知恵バイアス": ["予測を事前に記録する習慣", "結果を知る前の自分の考えを思い出す", "不確実性を受け入れる練習"],
                        "代表性ヒューリスティック": ["統計的基準率を調べる癖", "固定観念リストを作り定期見直し", "個別事例の特殊性を意識"],
                        "可用性ヒューリスティック": ["印象的な事例と統計データを区別", "メディアの偏りを意識する", "身近な体験と全体傾向を分けて考える"],
                        "プロスペクト理論": ["期待値計算を習慣化", "確実性と不確実性のリスクを比較", "確率的思考の訓練"]
                    }
                    
                    if bias in practice_tips:
                        for tip in practice_tips[bias]:
                            st.write(f"📌 {tip}")

        # 継続的改善のためのアドバイス
        st.markdown("### 🌟 継続的改善のために")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 短期目標（1ヶ月）")
            st.write("""
            - 重要な決断の前に10分考える時間を作る
            - 『なぜそう思うのか』を3回自問する習慣
            - 反対意見を1つは必ず探す
            - 数字は複数の表現で確認する
            """)
        
        with col2:
            st.markdown("#### 🎯 長期目標（3ヶ月）")
            st.write("""
            - 月1回この診断を受け直して進歩を確認
            - 意思決定日記をつけて振り返り
            - 友人・家族にバイアスチェックを依頼
            - 経済学・心理学の基礎知識を学習
            """)
        
        st.markdown("---")
        st.info("💡 **重要**: バイアスは完全に無くすものではありません。適切に認識し、重要な場面でコントロールすることが目標です。")
        st.caption("※本診断は継続的な自己認識向上を目的としています。定期的な受診で成長を実感してください。")