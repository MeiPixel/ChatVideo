import openai
import pandas as pd

data = pd.read_csv('../data/data.csv')


def get_result(text, question):
    messages = [
        {"role": "system", "content": f"""
以下文档每行是一条内容：
---文档---
{text}
---------
用户的问题：```{question}```
逐条判断否是用户要学习的内容：
写出判断结果：
--判断结果示例--
用户要学习的内容是：知识点xxx，知识点xxx，知识点xxx
----------
将判断结果输出为json格式：
---格式---
[{{"id":int,"Effective":"yes/no"}},{{"id":int,"Effective":"yes/no"}}]
---------
请输出以下内容：
结果：你的判断结果
json：将整理的json用代码格式输出
"""},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = response["choices"][0]["message"]['content'].replace('：', ':')
    try:
        res_json = eval(answer.split('json:')[-1])
        return res_json
    except:
        ...
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": f'''输出以下文本的json部分，确保输出的只有正确的json,不要有代码框。
    ```{answer}```
    json部分是:
    '''}]
    )
    res_json = eval(response["choices"][0]["message"]['content'])

    return res_json
