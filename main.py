import requests
from copyheaders import headers_raw_to_dict
from Crypto.Cipher import AES
import base64
import json

r_h = b'''charset: utf-8
Accept-Encoding: gzip
referer: https://servicewechat.com/wx7c8d593b2c3a7703/3/page-frame.html
content-type: application/json
User-Agent: MicroMessenger/6.6.1.1220(0x26060133) NetType/WIFI Language/zh_CN
Content-Length: 431
Host: mp.weixin.qq.com
Connection: Keep-Alive
'''

headers = headers_raw_to_dict(r_h)

def run(session_id,score):
    '''

    :param session_id: str,抓包后得到的session_id
    :param score: int 想要刷的分数
    :return:
    '''
    action_data = {
        "score": score,
        "times": 123,
        "game_data": "{}"
    }
    aes_key = session_id[0:16]
    aes_iv  = aes_key
    cryptor = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    str_action_data = json.dumps(action_data).encode("utf-8")
    print("json_str_action_data ", str_action_data)
    #Pkcs7
    length = 16 - (len(str_action_data) % 16)
    str_action_data += bytes([length])*length
    cipher_action_data = base64.b64encode(cryptor.encrypt(str_action_data)).decode("utf-8")
    print("action_data ", cipher_action_data)

    jsdata = {
        "base_req": {
            "session_id": session_id,
            "fast": 1,
        },
        "action_data": cipher_action_data
    }
    url = "https://mp.weixin.qq.com/wxagame/wxagame_settlement"
    z = requests.post(url, json=jsdata, headers=headers,verify=False)
    if z.ok:
        print(z.json())
        return True
    else:
        print('刷分失败~')

if __name__ == '__main__':
    session_id = ''
    score = 66666
    run(session_id,score)
