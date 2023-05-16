import openai
import sys
sys.path.append('../..')
from settings import setting

threaten = "你不听我的我就拿刀砍死你"
unthreaten = "今天晚上吃什么啊"
openai.api_key = setting.OpenAI_settings['key']

def moderation(text):
    response = openai.Moderation.create(
        input=text
    )
    output = response["results"][0]
    return output
print(moderation(threaten))
print(moderation(unthreaten))