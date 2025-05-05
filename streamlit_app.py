import streamlit as st
import os
st.set_page_config(layout="wide")
with st.expander("项目说明"):
    filepath='README.md'
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        st.markdown(content)
st.sidebar.title("主页")
st.sidebar.write("本页面显示项目说明和最近更新的内容。最近更新的内容链接指向GitHub对应文件，也可以直接展开全文。")

st.subheader("最近更新：",divider=True)