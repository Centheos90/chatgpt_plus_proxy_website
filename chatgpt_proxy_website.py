# -*- coding: utf-8 -*-
'''
第一作者：cooolr
第二作者：chatgpt
日期：2023-02-22
'''

import os
import requests
from hashlib import md5
from urllib.parse import unquote
from flask import Flask, request, redirect, send_file, Response, stream_with_context
from werkzeug.routing import BaseConverter

proxies = {"https": ""}

# 定义Cookie参数
# 需要在cookie获取以下三个参数，_puid为plus会员专属，没它不行
_puid = "769dc1b0-6c0e-449b-ad2f-14b2ccd52360"
cf_clearance = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..HWEnkgtPXdoC8Y3x.LWWvu8bTb4ptT6eXwaFo3sjlUsirdCzpMLCGzvUE0TIjMmGK7UiPvAhh2gkdzvJQ4v-8uM2YQrQjND01cWUm01dAEcWebnCq4teAuNUkTiCmM4XKN2UrJ5mJcWc8Tm7QUbxUsobPzK74GnBtTqtJUFXhlBrqjCcIUmkz3edRNeYesRHoh3WMP_t95zSwT-IVcUAWsOK5SJAvEp0-zdtGEgzPeKx-_hL2wRffltL43dvQok-HE0dEYIdDdUQeCcyy75nvi6g37JPinyKiiXHmqB__y8wuBcR2aMi_a2fAeIU5WOSAETvVZzEV_nhGxvHHySqnYbHoOtA10x60s2kcL5u0xhNhXQVJf3xiNC7AMLeiu1tyX1kZnWB5e1CDop7tx-MiHP7xUMI23DUfDhnnvtN4eRXQkNrvsdJH0xf7ga8awAhwpsjM0_7f3m8qfZlDEqoRga0sCfl3VF5chhAdUVWZuKK5VLJxh8u9S_Yp5kp_WB-veQnE2SMSSGL054YN3uRNBj_ZA5UBjkqv3-aDBbHkURkPRVMCx8CldNnihqPP-m-fw3tdsCprB6YZyDJP4vUf8-yUKvS19KB8de7Fwsy6E2_YXzjSK1m4b5ZRTijYp4664uJN4f0Llt1xElc3sw22X4Yl8F2Hni4EEWf73deJhCEdqup-OtJwmP55MMmUg9Bk9eBvw9giDP_nRKoFfyf_1qufRF-6hhlokWFnfVVhnLWRui6IgvNCTd83kUAMrcsUjkQXvzFhqt_mk5CJbs3mK1E3XCVs4OvhAC-fGXrXpQlXCc1_Ji77sepF1I9v1sDcrssRv54jSEINpuj5XU343-bEfj4zuvhd1R98FX_V7iAWBBHk32mr11PSrCEn2GWx10S6u_StoD6kv3hYpM3ur1zFZ_2EkaLnYgB-bPsjMROuT7KAxLlq9a7H-F7qEbAVv4Bw_md8FBS8DmMw7i8q6RJcdz3SWXsLu3HnGg7sLBQZToscxVapB-uP0SfOBPjo2As9K8e8m30DyarEupa8Gw0KFGkiGtu4Koe871Zn84eM5DDM-oz-TIFqqDng60OOwjWvXmOg2eGMT3fnInNJBm8EwLK7XVeIrTHlgW9SwnaN_ibAD0MpaQISc0TkEQWSpgd7RRsLASYUZ61QULdNk9SnWi8rWVEQm_MsSyYML6MylFHX6pW4tRbup9TMUqBzh6W283ShqnfBijNTDkcThX6FUVtt8Wqs3QbOvHUd8Pw3b9aPtgkKfpg1wZdMBT1w6NWcbPrlNeaxOfgcfomBojKdzUyNOBwckkh13ggUKOKRCoLlczPRj7Mg2Ax6txVADivyMHA_AI3rtq7TtxdqVWZoDqDT3zhLN9U7lUB4yo6SLDF3sqwzPrGR5m3BSindJh-WlrqKFdSrW07KfRNTCxFHv6F-2ZMOBNRHgYW6GAfkYx7YvjCoErpHD71Qc3xwHH3kalxVbQ0XOvpxFQ9BsA8la_5v7E7pjzYsicMaQ1_-e8dRxADjW-Ajt_2z5Q59Fm-Z-2sNR6p3kTU3bjlpADrraoqhueUBugbHmYMd1U7YKpwFPG1HtPxQ1hSUZieX9pYDWmrqiznmWLecCFrpmURgJMY_emFIInHUD830mA9dCYAQGEFxSM5CRl9YIoM_dAG-tpImnIm4-WOjpQuNuiNt9mlpAjJa0Tc115VUOQrCagzxlvgfH_XxgQLecS5HVMtlssVdSLfl7dBPpVPwhCiK_8KnEFgOBZ08ivc6QGaxglH_dQD5a8VpCEkmNZjT2Vhffo4aDa0xCQdzoD_Z0Lj1mYrjXqqJTFW74fhdvt_r2cVFO2GLM8Mn1JVjzSN-EAWsErQM0cOg9CzLnyHvRvvVyKcz11Wy9g2rc7AAzRROMUDCfBhlxnkpoQBmKK2EihLOIgNijvJJSLq4KV_4ogfxxgQd98tF4ikMKDbEeANOQXYsHlIutGRRHbknC8ZIidY8r-VT9vynaByRZPllN-uA-kNFKnvkQnCZIs6e8vKG8qJaIesyG5TQFuCTZCAyjZDldug8Xm9bXgGKh8_GN7Ls_MnVvcrFaeHsPGR9n_c2xpuduSyrh9olA38c-sweFuvDBclUSR_iBmtehkwZm0gHl7EePTia4sqwAj29UKmZAy6WLBDJ163KhX8cnFEvJgUm7WH1-DxF_zT69uHDyLTKT_cL1USu9XPg-WOfZNbGHWFOFLw9n3TL0oOAuwTmt_rMibFhRpUumOKvKKlmv9axZsdhF6cnUaltYdy3-lekh8Ty0aG8SeI4BhrhL_vbl1KcuFBuEXXLNv4nGYu5tBgyEVbXgOxhH62H4fVg3jF2rmAoR9llV2XOcPYHxDQ-PpJC1MviXh1OACOW2WwzRZxm2VLX5Kin6hmEqMKqylNAk3YiDnHjAiu_YtjdSrhr_Y8KPUZf2X9IwhohfXM0lLyhyDayVoHS08N5aq4uzeTMRrDXm00N-ufAvGxuF1GVqcVQ2zn-ey3h28br26QHRjKEujnTkqZF1ybmSOVWNiIP8A7zqarvHBlu4Tz0TV5KeUlkmX9TOVXIOvgsFaeUTdVmheucIFhrnZsTwHLMGHNIoH8Hiem7tmxcpibQqp8yoWu7oz8ozxiT-CuMwDiVsNEql-52EpJj_3H9pP0PUbjauFQRkZhJL_b5ZZpLdZHHyhc_9jhmR5tVdGBKeeEgvJ9QxWBnnDWADvZ6L1-wY5wGg716EvYiyF1mYav44DONZuHAGMHH4OCCEHj4aaZ-XEdNMp6TJfyTd6V2d4FwsjXYfm0LPoEFrmv-AdFPovAC-gYgol6Q29YQQITXQgLBaUELqOTF7gOtDLQNd7HroZqn05MVYtSrL2otvUQVUW8RvgH-1GogB4PipJtlIV5Jy_1nwNr6tBug15I5koxBXsGIPDysyQKBqhnrQx-hOe6MrzKtbq1BgwPjlxq0yQE40Nli5TtfZo9Eh1vI5K3Wmm89I2IAIbzR3h_RCWEjXdabJoDWwB5TiKvBg1YkTJxVbaOB1RP0DWb-6ji930Ets2MP3FOHKBl_JpYWfvuzMiW9G7QjrG9rfKjffxrTG4wC27tZBIRLm8iS7J0RGPmMyyBA02rX0c7ejIf2YQZrsnOxkusXDrzv5DZz3ahiOIBh4H5hCG3-fTa94UK1y4kO58ubig.-L_bRgAQTzpa_gqdcLrHfQ"
session_token = "https%3A%2F%2Fchatgpt.com%2F"

# 请求头
headers = {
    'authority': 'chat.openai.com',
    'accept': 'text/event-stream',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': f'cf_clearance={cf_clearance}; __Secure-next-auth.session-token={session_token}; _puid={_puid}',
    'dnt': '1',
    'origin': 'https://chat.openai.com',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

def get_authorization():
    """获取 accessToken"""
    url = "https://chat.openai.com/api/auth/session"
    r = requests.get(url, headers=headers, proxies=proxies)
    authorization = r.json()["accessToken"]
    return "Bearer "+authorization

# 获取 accessToken 并设置到 headers 中
headers["authorization"] = get_authorization()

# 定义 Flask 应用程序
app = Flask(__name__)

# 自定义正则表达式转换器
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

# 注册正则表达式转换器
app.url_map.converters['regex'] = RegexConverter

# 将 cookie 存储到字典中
cookie_dict = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in headers["cookie"].split("; ")}

# 创建存储资源的目录
resource_dir = './resource'
os.makedirs(resource_dir, exist_ok=True)

# 处理所有的 HTTP 请求方法
@app.route('/<path:uri>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'TRACE', 'CONNECT', 'PATCH'])
def index(uri):
    param = '&'.join([f'{i}={j}' for i,j in request.args.items()])
    url = f"https://chat.openai.com/{uri}?{param}" if param else f"https://chat.openai.com/{uri}"

    # 如果请求的是静态资源，优先从本地获取，否则从远程获取
    if any(x in url for x in ('.jpg', '.png', '.ico', '.woff', '.otf', '.css')):
        ext = url.split('.')[-1]
        filename = md5(url.encode('utf-8')).hexdigest()
        filepath = os.path.join(resource_dir, f'{filename}.{ext}')
        if os.path.isfile(filepath):
            # 如果本地存在该静态资源，则返回该资源
            return send_file(filepath)
        else:
            # 否则，从远程获取资源并保存到本地，再返回该资源
            r = requests.get(url, headers=headers, cookies=cookie_dict)
            with open(filepath, 'wb') as f:
                f.write(r.content)
            return send_file(filepath)
    elif 'conversation' in url:
        # 如果请求的是实时对话，则使用流式处理响应，提高效率
        r = requests.request(request.method, url, headers=headers, cookies=cookie_dict, data=request.data, proxies=proxies, stream=True)
        response = Response(stream_with_context(r.iter_content(chunk_size=1024)))
        response.headers['content-type'] = r.headers.get('content-type')
        return response
    else:
        # 对于其他请求，则使用常规方式处理
        r = requests.request(request.method, url, headers=headers, cookies=cookie_dict, data=request.data, proxies=proxies)
        return r.content.replace(b'https://chat.openai.com', b'http://127.0.0.1:8011')

if __name__ == "__main__":
    app.run(port=8011, threaded=True)
    # 在浏览器打开: http://127.0.0.1:8011/chat
