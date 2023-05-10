import os

import pywebio
from pywebio import config
from pywebio.input import file_upload, input_group, input
from pywebio.output import put_markdown, put_loading, put_text, clear, put_button, toast
from pywebio.session import download
import save_md

def check_age(age):
    if len(age) <= 1:
        return None
    support_url = ["juejin.cn", "linux.cn", "toutiao.com", "cnblogs.com", "weixin.qq.com", "zhuanlan.zhihu.com",
                   "zhihu.com/question", "csdn.net"]

    for x in support_url:
        if x in age:
            print(f"匹配到{x}")
            return None

        if x == support_url[-1]:
            msg12 = "\n".join(support_url)
            toast("目前只支持\n" + msg12, position='right', color='#2188ff', duration=10)
            return "不支持的url"

def sendmd():

    data = input_group("小功能", [
        file_upload(accept=".md", placeholder="上传md文件以展示", name="file"),
        input(placeholder="粘贴Url 将文章保存为markdown", name="down_url", validate=check_age),
    ])

    print(data)
    cank = filter(lambda y:y[1], data.items())

    atg = list(cank)
    tagss = atg[0][0]

    if tagss == "file":
        c = data["file"]
        md = c.get("content").decode("utf8")
        put_markdown(md)


    elif tagss == "down_url":# data["down_url"]:

        c = data["down_url"]
        file_name,fileinfo = save_md.get_md(c)

        put_text("由于存在防盗链，可能会导致图片预览失败，可以下载后本地用markdown编辑器打开")


        put_button('点我下载', lambda: download(file_name, bytes(fileinfo, encoding="utf-8")))

        put_markdown(fileinfo)



if __name__ == '__main__':
    config(title="JiaY", theme="yeti", description="yes")  # global configuration
    # start_server(sendmd, port=8000,cdn=False)
    pywebio.start_server(sendmd, port=8012, cdn=True)
