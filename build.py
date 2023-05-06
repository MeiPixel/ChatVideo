import argparse
import os
import tiktoken
import pandas as pd
import openai
import json
import os
import re

# os.environ['http_proxy'] = 'http://127.0.0.1:1080'
# os.environ['https_proxy'] = 'http://127.0.0.1:1080'

tokenizer = tiktoken.get_encoding("cl100k_base")


def get_result(text):
    response = openai.ChatCompletion.create(

        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"""
以下是视频录音转录，转录文件的格式为```[id]  内容 ``` 
请把以下转录文件按照知识点分割成不同的部分，并给出范围和摘要：
-------转录---------   
{text}
-------------------
按照以下json格式输出:
```[{{"knowledge":str,"start_id":int,"end_id":int,"summary":str}},
    {{"knowledge":str,"start_id":int,"end_id":int,"summary":str}}]```
"""},
        ]
    )

    try:
        res_json = eval(response["choices"][0]["message"]['content'].replace('，', ','))
        return res_json
    except:
        ...
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": f'''输出以下文本的json部分，确保输出的只有正确的json,不要有代码框。
```{response["choices"][0]["message"]['content'].replace('，', ',')}```
json部分是:
'''}]
    )
    answer = response["choices"][0]["message"]['content']

    return eval(answer)


def summary(file_path):
    for file in os.listdir(file_path):
        if file.endswith('.md') and file != 'autocut.md':
            texts = ''
            n_token = 0
            info = []
            with open(os.path.join(file_path, file), encoding='utf8') as f:
                for i in f:
                    if i.startswith('-'):
                        text = i.split(' ', 3)[-1]
                        text = re.sub('\[(\d+),(.*?)]', r'[\1]', text)
                        n_token += len(tokenizer.encode(text))
                        texts += text
                        if n_token > 2500:
                            info.extend(get_result(texts))
                            texts = ''
                            n_token = 0
                info.extend(get_result(texts))

            json.dump(info, open(os.path.join(file_path, f"{re.sub('.md$', '', file)}.json"), 'w'))


# def call_autocut(video_path):
#     cmd = ['autocut', '-d', video_path]
#     subprocess.call(cmd)


def Embedding(x):
    return openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding']


def vectorization(file_path):
    full_name = {}
    for file in os.listdir(file_path):
        name, ext = os.path.splitext(file)
        if ext in [".mp4", ".mov", ".mkv", ".avi", ".flv", ".f4v", ".webm"]:
            full_name[name] = file
    all_data = []
    for file in os.listdir(file_path):
        if file.endswith('.json'):
            data = pd.DataFrame(json.load(open(os.path.join(file_path, file))))
            file_name = re.sub('.json$', '', file)
            data['text'] = '知识点：' + data['knowledge'] + ' ' + '摘要：' + data['summary']
            data['embeddings'] = data['text'].apply(Embedding)
            data['video_name'] = full_name[file_name]
            all_data.append(data)
    pd.concat(all_data).to_csv('./data/data.csv', index=0)


def build(video_path):
    # call_autocut(video_path)
    summary(video_path)
    vectorization(video_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, help='文件目录')
    parser.add_argument('-api_key', type=str, help='openai api key')
    args = parser.parse_args()
    path = args.path
    openai.api_key = args.key
    build(path)
