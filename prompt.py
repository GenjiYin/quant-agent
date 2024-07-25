import pandas as pd
from tools import tool_info

def table_to_query(data):
    """
    将数据转化为字典
    """
    columns = list(data.columns)
    query = {}
    for c in columns:
        query[c] = list(data[c])
    return query

table_type = """
{
    '指标名1': [指标值1, 指标值2, 指标值3, 指标值4, ...], 
    '指标名2': [指标值1, 指标值2, 指标值3, 指标值4, ...], 
    '指标名3': [指标值1, 指标值2, 指标值3, 指标值4, ...], 
    ......
}
"""

constraints = [
    'Thoughts, Action, Action_input, Observation同时出现为一轮推理', 
    '你给出动作之后无法调用动作, 必须要求用户在Observation后面输入执行动作之后的结果才能进行新的一轮推理, 这个Observation通常是我指定类型的表格', 
    '禁止出现与上一轮动作和动作参数一样的决策'
]

user_prompt = """
现在我会传入一个数据表, 他的格式如下: 
{table_type}

我传入的表格为:
{table}

请根据以下内容为我加工一个量化因子: 
{query}

提出问题后你必须采用以下字典格式来回复: 
Thoughts: 构建因子的思路
Action: 返回你选择的动作工具名称
Action_input: 使用动作工具必须的参数
Observation: 将参数传入动作后的返回值

或者当你发现了最终答案后你可以按照以下格式回复: 
Thoughts: 我为你找到了最优解
Final_answer: (问题解决后按顺序描述一下你运行的动作以及参数)

你可以选择的动作工具:
{tools}

以往的推理记录能够为你提供帮助: 
{history_chat}

有如下限制: 
{constraints}
"""

def gen_prompt(table, query, history_chat='暂无推理记录'):
    system_prompt = '你是一个量化投研大师, 请协助我挖掘量化因子. '
    prompt = user_prompt.format(
        table_type=table_type, 
        table=table, 
        query=query, 
        tools=tool_info, 
        history_chat=history_chat, 
        constraints=constraints
    )
    return system_prompt, prompt

if __name__ == '__main__':
    data = pd.read_csv('./data.csv')
    # print(table_to_query(data))
    print(gen_prompt(table_to_query(data), '生成五日移动平均因子'))