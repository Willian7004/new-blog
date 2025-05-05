# New Blog

### 项目说明

##### 创建原因
此前我创建过博客类项目，存在两个问题：\
1.pages部分的文章需要持续更新，文章较多导致维护困难；由于使用streamlit页面而非markdown，难以在GitHub上直接查看。\
2.杂谈部分的文章通常不更新，由于只占一个页面，曝光度下降；由于按发布顺序命名，难以按日期等方式组织文章。\
3.gallery系列项目由于注重内容的系统性，需要大量时间来创建一个页面，改为文章形式更适合展示具体创意。

继续使用Streamlit的原因如下：\
1.Streamlit方便部署多项目，在容量占用较大的Gallery等项目的部署上相比GitHub Pages有一定优势。\
2.Streamlit使用Python，方便编写更多功能。语法简洁的特性无论是亲自编写或使用LLM辅助编写都有优势。\
3.Streamlit的UI框架比较优秀，在web技术栈中更优秀的框架较少。\
4.结合GitHub action，把更改发送到release可以实现RSS。其中首页使用只显示更改的文件名的名称版本用于展示更新情况，另外提供显示更改内容的版本用于订阅。

##### 项目结构
Streamlit程序：\
1.主页包含项目说明和最近更新的内容。\
2.“静态文章”部分可选月份，按发布日期显示文章。\
3.“动态文章”部分直接选择具体的文章，文章为相应主题的最新内容。

目录结构：\
1.“静态文章”部分在static文件夹并按月份创建子文件夹，“动态文章”部分在dynamic文件夹。在仓库内可以直接按这一目录阅读。\
2.streamlit_app.py和pages文件夹为程序，开头用多行注释记录使用LLM辅助创建相应文件的提示词。\
3.files文件夹与文章文件夹对应的部分用于保存文章引用的媒体文件，files内的xlsx文件夹用于把xlsx表格转换为markdown表格以便填入文章。

##### 其它说明
1.本项目已部署到Streamlit Cloud，域名为https://willian7004-new-blog.streamlit.app/ \
2.域名选择上，之前由于GitHub命名笔误，使用了纠正后的名称，本项目改为使用实际的GitHub名称作为开头。\
3.旧仓库的杂谈文章和Gallery等内容不同步到本仓库，可在原仓库查看。

### 本地部署

##### 使用python部署
1.安装依赖
```bash
pip install -r requirements.txt
```
2.运行应用
```
streamlit run streamlit_app.py
```

##### 使用docker部署
1.创建docker
```bash
docker build . -t new-homepage
```
2.运行docker
```bash
docker run -p 8501:8501 new-homepage
```