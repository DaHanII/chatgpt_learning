import openai
import settings.setting as setting

# 获取访问open ai的密钥
openai.api_key = setting.OpenAI_settings['key']
class Conversation:
    def __init__(self, prompt, num_of_round):
        self.prompt = prompt
        self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({"role": "system", "content": self.prompt})

    def ask(self, question):
        try:
            self.messages.append({"role": "user", "content": question})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                temperature=0.5,
                max_tokens=2048,
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        message = response["choices"][0]["message"]["content"]
        num_of_tokens = response['usage']['total_tokens']
        self.messages.append({"role": "assistant", "content": message})

        if len(self.messages) > self.num_of_round*2 + 1:
            del self.messages[1:3]  #Remove the first round conversation left.
        return message, num_of_tokens


prompt = """你是一个中国厨师，用中文回答做菜的问题。你的回答需要满足以下要求:
1. 你的回答必须是中文
2. 回答限制在100个字以内"""
question1 = "你是谁？"
question2 = "请问鱼香肉丝怎么做？"
question3 = "那蚝油牛肉呢？"

conv = Conversation(prompt, 3)
questions = [question1, question2, question3]
for question in questions:
    answer, num_of_tokens = conv.ask(question)
    print("询问 {%s} 消耗的token数量是 : %d" % (question, num_of_tokens))

# 方式2
import tiktoken
encoding = tiktoken.get_encoding("cl100k_base")

conv2 = Conversation(prompt, 3)
question1 = "你是谁？"
answer1, num_of_tokens = conv2.ask(question1)
print("总共消耗的token数量是 : %d" % (num_of_tokens))

prompt_count = len(encoding.encode(prompt))
question1_count = len(encoding.encode(question1))
answer1_count = len(encoding.encode(answer1))
total_count = prompt_count + question1_count + answer1_count
print("Prompt消耗 %d Token, 问题消耗 %d Token，回答消耗 %d Token，总共消耗 %d Token" % (prompt_count, question1_count, answer1_count, total_count))