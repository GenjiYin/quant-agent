import pandas as pd

data = pd.read_csv('./data.csv')

def m_avg(column_name, N):
    def f(df):
        df[f'm_avg_{column_name}_{N}'] = df[column_name].rolling(N).mean()
        return df
    global data
    data = data.groupby('instrument').apply(f).reset_index(drop=True)
    return data

def m_lag(column_name, N):
    def f(df):
        df[f'm_lag_{column_name}_{N}'] = df[column_name].shift(N)
        return df
    global data
    data = data.groupby('instrument').apply(f).reset_index(drop=True)
    return data

def sub(factor1, factor2):
    global data
    data[f'{factor1}-{factor2}'] = data[factor1] - data[factor2]
    return data

def divide(factor1, factor2):
    global data
    data[f'{factor1}/{factor2}'] = data[factor1] / data[factor2]
    return data

tool_info = """
[
    {
        'name': m_avg, 
        'description': 对某一个指标计算多日移动平均值, 
        'args': {
            'column_name' : 需要计算移动平均的对象(指标), 
            'N': 需要计算N日移动平均, 
        }
    }, 
    {
        'name': m_lag, 
        'description': '计算某一指标的滞后数据', 
        'args': {
            'column_name': 被滞后计算的对象(指标), 
            'N': 滞后N期
        }
    }, 
    {
        'name': sub, 
        'description': '计算两个因子的减法', 
        'args': {
            'factor1': 被减数因子， 
            'factor2': 减数因子
        }
    },
    {
        'name': divide, 
        'description': '计算两个因子的除法', 
        'args': {
            'factor1': 被除数因子, 
            'factor2': 除数因子
        }
    }
]
"""

tool_map = {
    'm_avg': m_avg, 
    'm_lag': m_lag, 
    'sub': sub, 
    'divide': divide
}


if __name__ == '__main__':
    print(data)
    print(sub('close', 'open'))
    print(data)