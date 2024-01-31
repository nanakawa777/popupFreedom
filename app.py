import base64
import time

import pandas as pd
import requests

from compare import semantic_search

SCOPE = {
    "企业": "1",
    "地区": "2",
    "全流程": "00",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "http://taxcontroller.yunzhangfang.com/v_rule/pending",
    "Cookie": "session=249c36bb-00e8-427e-89b9-db433632a9d1.NCsUiOvJ7j8tZtQeaP3TMIP1meM; jobnumber=E02691; remember_token=\"\346\235\216\346\263\275\346\255\243|fd9f8c54bcfeb8ec2becc4f2cfad2590c5d807fcc6814ccaeacf3ea090c50c4831848984a97887ddf893620611805caee0601d76c75d4bbef9f4ed9c4ed39528\"",
}


def get_pending(dqbm: str = "0", limit: str = "100"):
    """获取待处理的弹框，默认获取全国，前100条"""
    response = requests.get("http://taxcontroller.yunzhangfang.com/v_rule/pending_json?page=1&matchkey=",
                            headers=headers,
                            params={"dqbm": dqbm, "limit": limit}
                            )

    # status_code attribute returns the HTTP status code that was sent with the response.
    # print("Response Status Code: " + str(response.status_code))

    # You can use the json() method to get the JSON from the response.
    # print("JSON response: " + str(response.json()))

    return response.json()


def get_publish_rule(rule_id):
    response = requests.get(
        url="http://taxcontroller.yunzhangfang.com/v_rule/publishedrule_json?page=1&limit=20&dqbm=0&matchkey=&matchresult=&bxls=&matchscope=",
        headers=headers,
        params={"rule_id": rule_id}
    )
    return response.json()


def push_new_rule(rule: dict):
    """推送新的规则"""
    # url = "http://taxcontroller.yunzhangfang.com/v_rule/initial_rule_submit_json"
    # response = requests.post(url, headers=headers, json=rule)
    print(f"新增规则：{rule}")


def run():
    while True:
        pending_jsond = get_pending()
        for data in pending_jsond.get("data", []):
            content = data.get("content", "")
            if content == "":
                continue

            print(f"当前处理弹框文本：{content}")
            rule_id = semantic_search(content)
            if rule_id:
                rule = get_publish_rule(rule_id)["data"][0]
                print(f"套用规则：{rule}")
                new_rule = {
                    'matchtype': rule['matchtype'],
                    'matchkey': rule['matchkey'],
                    'matchresult': rule['matchresult'],
                    'codematch': rule['codematch'],
                    'initruleid': data["id"],
                    'rulename': rule['name'],
                    'matchscope': SCOPE.get(rule['scope'], "01"),  # 默认为01，具体场景
                    'resulttype': rule['resulttype'],
                    'matchscopevalue': f"{data['dqmc']}-{data['rwlx']}-{data['bslx']}-{data['step']}",
                }
                push_new_rule(new_rule)

        time.sleep(180)


run()
