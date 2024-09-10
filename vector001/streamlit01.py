import streamlit as st
import pandas as pd
import numpy as np

st.title('我的第一个Streamlit应用')

# 创建一些示例数据
df = pd.DataFrame({
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 40],
    '城市': ['北京', '上海', '广州', '深圳']
})

# 显示数据框
st.write(df)

# 添加一个图表
st.line_chart(np.random.randn(20, 3))