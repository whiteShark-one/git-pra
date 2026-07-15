import re
import json
import os

def parse_oxford_3000(input_file, output_file):
    word_dict = {}
    
    print("🔄 正在读取并解析文件，请稍候...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                # 兼容制表符(\t)或多个空格分隔
                parts = re.split(r'\t|\s{2,}', line, maxsplit=1)
                if len(parts) < 2:
                    # 降级尝试：用单个空格分割（防止格式不严谨）
                    parts = line.split(' ', maxsplit=1)
                    if len(parts) < 2:
                        continue
                
                eng_part = parts[0].strip()
                chn_part = parts[1].strip()
                
                # 处理英文部分：兼容逗号分隔（如 "a, an" -> ["a", "an"]）
                eng_words = [w.strip() for w in eng_part.split(',') if w.strip()]
                
                if not eng_words or not chn_part:
                    continue
                
                # 构建字典：中文释义 -> [英文单词列表]
                if chn_part not in word_dict:
                    word_dict[chn_part] = []
                
                for w in eng_words:
                    if w not in word_dict[chn_part]:
                        word_dict[chn_part].append(w)
                        
    except FileNotFoundError:
        print(f"❌ 找不到文件: {input_file}")
        print("💡 请确保《牛津3000词_完整版_中英文版.txt》与此 Python 脚本在同一目录下。")
        return

    # 为了让生成的代码更美观，按英文单词首字母对字典进行排序
    sorted_dict = {}
    sorted_keys = sorted(word_dict.keys(), key=lambda k: word_dict[k][0].lower())
    for k in sorted_keys:
        sorted_dict[k] = word_dict[k]

    # 转换为 JS 对象格式字符串
    js_dict_str = json.dumps(sorted_dict, ensure_ascii=False, indent=2)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("// 牛津3000词完整版数据 (由 Python 脚本自动生成)\n")
        f.write("const demoDict = ")
        f.write(js_dict_str)
        f.write(";\n")
        
    print("-" * 50)
    print(f"✅ 转换成功！共提取 {len(sorted_dict)} 个独立中文词条。")
    print(f"📁 数据已保存至: {os.path.abspath(output_file)}")
    print("-" * 50)
    print("💡 下一步操作：")
    print("1. 打开生成的 dict_data.js 文件")
    print("2. 复制全部内容 (Ctrl+A -> Ctrl+C)")
    print("3. 替换 HTML 代码中的 const demoDict = { ... };")

if __name__ == "__main__":
    input_filename = "牛津3000词_完整版_中英文版.txt"
    output_filename = "dict_data.js"
    
    parse_oxford_3000(input_filename, output_filename)
    
    input("\n按回车键退出程序...")