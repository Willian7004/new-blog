'''
写一个streamlit程序，实现以下功能：
1.使用gitpython库，获取 https://github.com/Willian7004/new-blog 仓库的static和dynamic文件夹中最近10个修改的文件，相同文件的修改只获取最新一次。
2.在页面上创建st.expander，文字为上一步获取的文件的第一行内容，如果开头有“#”则去掉，展开后使用st.markdown显示文件的完整内容,并设置unsafe_allow_html=True。按修改时间从新到旧的顺序显示。
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
st.sidebar.write("本页面显示项目说明和最近更新的内容。最近更新的内容包括创建和修改的文章，按修改时间从新到旧显示，可以直接展开全文。")

st.subheader("最近更新：",divider=True)

def get_file_contents(repo_path):
    repo = Repo(repo_path)
    files_dict = {}

    # 遍历所有提交并收集文件修改记录
    for commit in repo.iter_commits(all=True):
        # 获取差异比较
        if commit.parents:
            parent = commit.parents[0]
            diffs = parent.diff(commit)
        else:
            diffs = commit.diff(None)

        for diff in diffs:
            file_path = diff.b_path or diff.a_path
            if file_path and any(file_path.startswith(p) for p in ('static/', 'dynamic/')):
                if diff.change_type == 'D':  # 跳过已删除文件
                    continue
                
                # 更新文件记录（保留最新修改）
                if file_path not in files_dict or commit.committed_datetime > files_dict[file_path]['commit_time']:
                    files_dict[file_path] = {
                        'commit': commit,
                        'commit_time': commit.committed_datetime,
                        'file_path': file_path
                    }

    # 按修改时间排序并取前10个
    sorted_files = sorted(files_dict.values(), 
                        key=lambda x: x['commit_time'], 
                        reverse=True)[:10]

    # 提取文件内容
    file_contents = []
    for file_info in sorted_files:
        try:
            blob = file_info['commit'].tree / file_info['file_path']
            content = blob.data_stream.read().decode('utf-8')
            first_line = content.split('\n', 1)[0].strip()
            
            # 处理标题
            title = first_line.lstrip('#').strip() if first_line.startswith('#') else first_line
            
            file_contents.append({
                'title': title or file_info['file_path'],
                'content': content,
                'commit_time': file_info['commit_time']
            })
        except Exception as e:
            st.error(f"读取文件失败：{str(e)}")
            continue

    return file_contents

with tempfile.TemporaryDirectory() as temp_dir:
    try:
        # 克隆仓库
        repo_url = "https://github.com/Willian7004/new-blog"
        Repo.clone_from(repo_url, temp_dir)
        
        # 获取文件内容
        files = get_file_contents(temp_dir)
        
        # 显示结果
        if not files:
            st.warning("没有找到符合条件的文件")

        else:
            for file in files:
                with st.expander(file['title']):
                    st.markdown(file['content'], unsafe_allow_html=True)

    except Exception as e:
        st.error(f"操作失败：{str(e)}")
