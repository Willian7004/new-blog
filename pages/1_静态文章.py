'''
写一个streamlit程序，实现以下功能：
1.读取当前目录下static文件夹中有多个包含.md文件的文件夹，文件夹命名包含年、月（例如2025年5月对应的文件夹命名为202505），文件命名依次包含年、月、日和序号（例如2025年5月5日第一篇名称为2025050501）。.md文件内容第一行为标题。
2.在页面第一行创建下拉菜单、输入框和复选框。下拉菜单用于选择月份对应的文件夹，较新的排在前面，第一个选项为“全部”，用于选择所有文件夹。在输入框输入文字筛选标题包含特定关键词的文件，通过空格输入多个关键词以筛选同时包含所有关键词的文件。复选框文字为“全文搜索”，选中后搜索文件全文。
3.在侧边栏创建单选按钮文字为文件标题，用于选中对应文件。新的文件显示在上方。在每个日期的文件上方添加一个文字为对应日期的选项，用于选中相应日期的所有文件。
4.选中文件后在页面上使用st.markdown显示对应的文件内容（包括标题）,并设置unsafe_allow_html=True。
'''
import os
import re
import streamlit as st
with st.expander("页面说明"):
    st.title("静态文章")
    st.write("本页面展示通常不持续更新的文章。可以选择特定月份，并在选项中添加了日期显示用于以便选择特定日期的文章。文章题材不限。大部分为新的内容，也会适当整理之前的博客项目的文章。在一些文章中会添加媒体内容。")
def get_month_folders(static_dir='static'):
    """获取并排序月份文件夹"""
    folders = []
    for name in os.listdir(static_dir):
        path = os.path.join(static_dir, name)
        if os.path.isdir(path) and re.match(r'^\d{6}$', name):
            try:
                year = int(name[:4])
                month = int(name[4:6])
                folders.append((name, year, month))
            except:
                continue
    folders.sort(key=lambda x: (-x[1], -x[2]))
    return [f[0] for f in folders]

def parse_filename(filename):
    """解析文件名"""
    match = re.match(r'^(\d{8})(\d{2})\.md$', filename)
    if match:
        try:
            date_str = match.group(1)
            year = int(date_str[:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])
            seq = int(match.group(2))
            return year, month, day, seq
        except:
            return None
    return None

def get_file_info(file_path):
    """获取文件信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            title = f.readline().strip()
        filename = os.path.basename(file_path)
        parsed = parse_filename(filename)
        if not parsed or not title:
            return None
        year, month, day, seq = parsed
        return {
            'path': file_path,
            'title': title,
            'year': year,
            'month': month,
            'day': day,
            'seq': seq,
            'date_key': f"{year:04d}{month:02d}{day:02d}"
        }
    except:
        return None

def get_all_files(month_folders, static_dir='static'):
    """获取所有文件信息"""
    all_files = []
    for folder in month_folders:
        folder_path = os.path.join(static_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        for filename in os.listdir(folder_path):
            if filename.endswith('.md'):
                file_path = os.path.join(folder_path, filename)
                file_info = get_file_info(file_path)
                if file_info:
                    all_files.append(file_info)
    all_files.sort(key=lambda x: (-x['year'], -x['month'], -x['day'], -x['seq']))
    return all_files

def filter_files(files, keywords, search_full):
    """过滤文件"""
    if not keywords:
        return files
    
    filtered = []
    for file in files:
        content = None
        if search_full:
            try:
                with open(file['path'], 'r', encoding='utf-8') as f:
                    content = f.read().lower()
            except:
                continue
        
        target = content if search_full else file['title'].lower()
        if all(kw.lower() in target for kw in keywords):
            filtered.append(file)
    return filtered

def prepare_sidebar_options(files):
    """准备侧边栏选项"""
    date_groups = {}
    for file in files:
        key = file['date_key']
        if key not in date_groups:
            date_groups[key] = []
        date_groups[key].append(file)
    
    options = []
    for date_key in sorted(date_groups.keys(), reverse=True):
        # 添加日期选项
        date_str = f"{date_key[:4]}年{int(date_key[4:6])}月{int(date_key[6:8])}日"
        options.append(('📅 ' + date_str, f'DATE:{date_key}'))
        # 添加文件选项
        for file in date_groups[date_key]:
            options.append((file['title'], file['path']))
    return options

def main():

    # 读取月份文件夹
    month_folders = ['全部'] + get_month_folders()
    
    # 页面顶部控件
    col1, col2, col3 = st.columns([2, 4, 1],vertical_alignment='bottom')
    with col1:
        selected_month = st.selectbox('选择月份', month_folders)
    with col2:
        search_text = st.text_input('搜索关键词（空格分隔多个关键词）')
    with col3:
        full_search = st.checkbox('全文搜索')
    
    # 获取需要处理的月份
    process_folders = month_folders[1:] if selected_month == '全部' else [selected_month]
    
    # 获取并过滤文件
    all_files = get_all_files(process_folders)
    keywords = search_text.strip().split()
    filtered_files = filter_files(all_files, keywords, full_search)
    
    # 侧边栏
    selected_file = None
    if filtered_files:
        sidebar_options = prepare_sidebar_options(filtered_files)
        selected = st.sidebar.radio("选择文件", [opt[1] for opt in sidebar_options],
                                  format_func=lambda x: next(opt[0] for opt in sidebar_options if opt[1] == x))
        
        if selected.startswith('DATE:'):
            date_key = selected.split(':')[1]
            selected_files = [f for f in filtered_files if f['date_key'] == date_key]
            if selected_files:
                selected_file = selected_files[0]['path']
        else:
            selected_file = selected
    else:
        st.sidebar.write("没有找到匹配的文件")

    # 显示内容
    if selected_file and os.path.exists(selected_file):
        with open(selected_file, 'r', encoding='utf-8') as f:
            content = f.read()
        st.markdown(content, unsafe_allow_html=True)

if __name__ == '__main__':
    main()