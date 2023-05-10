from requests import get
from parsel import Selector
from tomd import Tomd
from re import sub


def get_www(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70"
    }
    html = get(url=url, headers=head).text
    return html


def chose_selector(url):
    support_web = {
        "juejin.cn": (".article-title", ".article-content"),
        "linux.cn": ("#article_titl", "#ct > div > article > div.d"),
        "toutiao.com": ("#root > div.article-detail-container > div.main > div:nth-child(1) > div > div > div > div > h1", "#article-content"),
        "cnblogs.com": ('#cb_post_title_url > span', '#cnblogs_post_body'),
        "weixin.qq.com": ('.rich_media_title', '.rich_media_content'),
        "zhuanlan.zhihu.com": ('#root > div > main > div > article > header > h1',
                               '#root > div > main > div > article > div.Post-RichTextContainer'),
        "zhihu.com/question/": ('.QuestionHeader-title', '.RichContent-inner'),
        "csdn.net/": ('.title-article', 'article'),

    }
    for tag, value in support_web.items():
        if tag in url:
            return value
    # 找不到
    raise ModuleNotFoundError("该网站不在支持列表里")

def replacestr(text:str,replace__str:dict)-> str:
    for k,v in replace__str.items():
        print(f"{k}\t{v}")
        text = text.replace(k,v)
    return text

def get_md(url):
    kv = chose_selector(url)
    html = get_www(url)

    page = Selector(html)

    title_chose = kv[0]
    title = page.css(title_chose + "::text").get()  # 原始标题
    # print('移除标题里面所有不支持的字符（windown文件名要求）', end=' ==> ')
    for x in ' \/:*?？"<>|\n':
        title = title.replace(x, "")

    arctl_chose = kv[1]

    arctl = page.css(arctl_chose).get()  # 网页原文
    arctl = replacestr(arctl, replace__str)

    arctl = sub("(<img.*?>)", "<p>\\1</p>", arctl)  # 图片需要<p> 包围才能在md中展现



    md_txt = Tomd(arctl).markdown


    return title + ".md",md_txt


removestr = [" ","|","\\"]# 需要移除的字符
replace__str = {
    "&nbsp;":" ",
    "&lt;":"<",
    "&gt;":">",
    "&amp;":"& ",
    "&quot;":'"',
    "&apos;":"'",
}


