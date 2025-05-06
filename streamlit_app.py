'''
写一个streamlit程序，实现以下功能：
1.使用gitpython库，获取 https://github.com/Willian7004/new-blog 仓库的static和dynamic文件夹中最近10个修改的文件，相同文件的修改只获取最新一次。
2.在页面上创建st.expander，文字为上一步获取的文件的第一行内容，如果开头有“#”则去掉，展开后使用st.markdown显示文件的完整内容,并设置unsafe_allow_html=True。
'''
import streamlit as st
from git import Repo
import tempfile
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


import streamlit as st
from git import Repo
import tempfile
import os
import shutil

def get_recent_files(repo_url, target_folders, max_files=10):
    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            # 克隆仓库到临时目录
            repo = Repo.clone_from(repo_url, tmp_dir)
            file_commits = {}
            
            # 遍历提交记录（从最新到最旧）
            for commit in repo.iter_commits('main', max_count=1000):
                if len(file_commits) >= max_files:
                    break
                
                # 获取本次提交修改的文件列表
                for file_path in commit.stats.files:
                    normalized_path = file_path.replace('\\', '/')
                    
                    # 检查文件是否在目标文件夹中
                    for folder in target_folders:
                        folder = folder.strip('/')
                        if normalized_path.startswith(f"{folder}/") or normalized_path == folder:
                            if normalized_path not in file_commits:
                                file_commits[normalized_path] = commit
                                break
            
            # 获取文件内容
            file_contents = []
            for path, commit in list(file_commits.items())[:max_files]:
                try:
                    blob = commit.tree / path
                    content = blob.data_stream.read().decode('utf-8')
                    
                    # 处理标题
                    first_line = content.split('\n', 1)[0].strip() if content else ''
                    title = first_line.lstrip('#').strip()
                    
                    file_contents.append({
                        'title': title or os.path.basename(path),
                        'content': content
                    })
                except (KeyError, AttributeError):
                    continue
            
            return file_contents
        
        finally:
            # 显式删除.git目录（Windows文件锁问题解决方案）
            git_dir = os.path.join(tmp_dir, '.git')
            if os.path.exists(git_dir):
                shutil.rmtree(git_dir, ignore_errors=True)

# 获取最近修改的文件
files = get_recent_files(
    "https://github.com/Willian7004/new-blog",
    ["static", "dynamic"],
    10
)

# 显示文件内容
for file in files:
    with st.expander(file['title']):
        st.markdown(file['content'], unsafe_allow_html=True)
