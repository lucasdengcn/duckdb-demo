import streamlit as st

if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter():
    st.session_state.count += 1

st.button('点击增加计数', on_click=increment_counter)

st.write('计数器:', st.session_state.count)