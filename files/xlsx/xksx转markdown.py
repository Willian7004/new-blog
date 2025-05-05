'''
写一个python程序，使用openpyxl把当前目录下所有xlsx文件转换为markdown表格，只转换第一个表，在当前目录下保存为同名的md文件。
'''
import openpyxl
import glob
import os

def convert_excel_to_markdown(excel_file):
    # 加载Excel工作簿
    wb = openpyxl.load_workbook(excel_file, data_only=True)
    sheet = wb.worksheets[0]  # 获取第一个工作表
    
    # 读取所有数据行
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return  # 跳过空工作表
    
    # 处理单元格内容并转义特殊字符
    processed_rows = []
    for row in rows:
        cleaned_row = [
            str(cell).replace("|", "\\|").replace("\n", " ") 
            if cell is not None else ""
            for cell in row
        ]
        processed_rows.append(cleaned_row)
    
    # 统一列数（以第一行为准）
    num_columns = len(processed_rows[0]) if processed_rows else 0
    adjusted_rows = []
    for row in processed_rows:
        adjusted_row = row[:num_columns] + [""] * (num_columns - len(row))
        adjusted_rows.append(adjusted_row[:num_columns])
    
    # 生成Markdown表格
    header = "| " + " | ".join(adjusted_rows[0]) + " |"
    separator = "| " + " | ".join(["---"] * num_columns) + " |"
    data_rows = [
        "| " + " | ".join(row) + " |"
        for row in adjusted_rows[1:]
    ]
    
    markdown_content = "\n".join([header, separator] + data_rows)
    
    # 保存Markdown文件
    base_name = os.path.splitext(excel_file)[0]
    md_filename = f"{base_name}.md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)

if __name__ == "__main__":
    # 处理当前目录下所有xlsx文件
    for excel_file in glob.glob("*.xlsx"):
        convert_excel_to_markdown(excel_file)
        print(f"转换完成：{excel_file} -> {os.path.splitext(excel_file)[0]}.md")