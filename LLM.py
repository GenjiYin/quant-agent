import re
import pandas as pd
from openai import OpenAI
from prompt import table_to_query, gen_prompt
from tools import data, tool_map
deepseek_api = 'sk-09b2df08a3b2499189b7087b4a5ba98e'

# os.environ['TAVILY_API_KEY'] = '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'

def parser(result, parse_info='Action'):
    if parse_info == 'Action':
        pattern = r"Action:\s*(.*?)(?=\n\n|Action_input:)"
        action_match = re.search(pattern, result, re.DOTALL)
        return action_match.group(1).strip()
    
    elif parse_info == 'Action_input':
        pattern = r"Action_input:\s*(.*?)(?=\n\n|Observation:)"
        action_match = re.search(pattern, result, re.DOTALL)
        return action_match.group(1).strip()

def call_llm(query):
    """
    :params table: 传入你要分析的新闻数据, 这个数据是DataFrame类型的
    :params query: 想让模型为你构造的因子
    """
    max_try = 10          # 需要循环执行大模型
    table = table_to_query(data)         # 将数据转化为提示词
    client = OpenAI(api_key=deepseek_api, base_url="https://api.deepseek.com").chat.completions.create
    history_chat = ''
    
    step = 1
    
    for _ in range(max_try):
        # try:
        system_prompt, prompt = gen_prompt(table, query, history_chat=history_chat)
        # print(prompt)
        messages=[
            {"role": "system", "content": system_prompt}, 
        ]
        messages.append({'role': 'user', 'content': prompt})
        response = client(
            model="deepseek-chat", 
            messages=messages, 
            stream=False
        )
        result = response.choices[0].message.content
        # print(result)
        
        if 'Final_answer' in result:
            return result
        
        # 执行动作
        action_name = parser(result, parse_info='Action')
        action_params = eval(parser(result, parse_info='Action_input'))
        print(f'step_{step} 执行动作: {action_name}, 动作参数: {action_params}')
        step+=1
        param1, param2 = list(action_params.values())
        output_df = tool_map[action_name](param1, param2)
        output_df.to_csv('./output.csv', index=False)
        observation = list(output_df.columns)
        
        # 我们替换掉之前的Observation
        pattern = r"(Observation:\s*)(.*)(?=\n|$)"
        history_chat = history_chat + r'\n\n' +re.sub(pattern, r"\1" + '新表包含的字段有: '+str(observation), result, flags=re.DOTALL)
        # print(history_chat)
        table = observation
        
        # except Exception as err:
        #     print('模型加载失败 {}'.format(err))
        #     return {}

if __name__ == '__main__':
    # print(call_llm('先计算滞后一期收盘价, 再用收盘价减去滞后收盘价'))
    # print(call_llm('先计算滞后一期收盘价, 再用收盘价除以滞后收盘价'))    # 存在问题, 算到除法时停不下来
    print(call_llm('先计算滞后一期收盘价, 再计算滞后收盘价的五日均值'))