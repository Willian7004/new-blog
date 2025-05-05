'''
写一个streamlit程序，实现以下功能：
1.读取当前目录下dynamic文件夹中的所有.md文件，根据文件名在侧边栏创建单选按钮
2.选中文件后在页面上使用st.markdown显示对应的文件内容,并设置unsafe_allow_html=True
'''
import streamlit as st
import os
from pathlib import Path
with st.expander("页面说明"):
    st.title("动态文章")
    st.write("本页面展示内容根据相应话题动态调整的文章，在侧边栏选择文章，文章内容在下方显示。文章主要包括我使用一些软硬件的体验，相比之前的blog缩减了一些不常更新的话题。")
def read_md_file(file_path):
    """读取Markdown文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    
    # 检查dynamic文件夹是否存在
    dynamic_dir = Path("dynamic")
    if not dynamic_dir.exists():
        st.error("当前目录下未找到dynamic文件夹！")
        return
    
    # 获取所有.md文件
    md_files = list(dynamic_dir.glob("*.md"))
    
    if not md_files:
        st.warning("dynamic文件夹中没有找到任何.md文件！")
        return
    
    # 在侧边栏创建单选按钮
    selected_file = st.sidebar.radio(
        "选择文章",
        md_files,
        format_func=lambda x: x.stem  # 只显示文件名（不含扩展名）
    )
    
    # 读取并显示选中的文件内容
    if selected_file:
        content = read_md_file(selected_file)
        st.markdown(content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()