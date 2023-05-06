import openai
import argparse
from utils.Player import play_video
# os.environ['http_proxy'] = 'http://127.0.0.1:1080'
# os.environ['https_proxy'] = 'http://127.0.0.1:1080'

from utils.Recall import create_context
from utils.Regenerate import get_result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, help='文件目录')
    parser.add_argument('-api_key', type=str, help='openai api key')
    args = parser.parse_args()
    path = args.path
    openai.api_key = args.key

    question = input('请输入想要学习的内容：')
    recall_text,info = create_context(question)
    knowledge = get_result(recall_text,question)
    Effective = []
    for i in knowledge:
        if i['Effective'] =='yes':
            Effective.append(info[i['id']-1])
    for i in Effective:
        play_video(path,i)