import os
import json

# 支持的图片扩展名（不区分大小写）
SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}

def is_image_file(filename):
    """检查文件是否是支持的图片格式"""
    return os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS

def generate_index_json(image_files):
    """生成index.json文件内容"""
    return {"0": sorted(image_files)}

def generate_info_json(image_files, category_name, icon_file):
    """生成info.json文件内容"""
    return {
        "name": category_name,
        "icon": icon_file,
        "items": sorted(image_files)
    }

def process_directory(category_path, overwrite=False):
    """处理单个目录"""
    # 获取目录中所有支持的图片文件
    image_files = [
        f for f in os.listdir(category_path) 
        if is_image_file(f) and os.path.isfile(os.path.join(category_path, f))
    ]
    
    if not image_files:
        print(f'警告: 目录 {category_path} 中没有支持的图片文件')
        return False
    
    # 文件路径
    index_path = os.path.join(category_path, 'index.json')
    info_path = os.path.join(category_path, 'info.json')
    
    # 如果不覆盖且文件已存在，则跳过
    if not overwrite and (os.path.exists(index_path) or os.path.exists(info_path)):
        print(f'已跳过目录(文件已存在): {category_path}')
        return False
    
    # 选择第一个存在的图片文件作为icon
    icon_file = next(
        (f for f in image_files if os.path.exists(os.path.join(category_path, f))), 
        image_files[0]
    )
    
    try:
        # 生成index.json（保持原始字符）
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(generate_index_json(image_files), f, ensure_ascii=False, indent=2)
        
        # 生成info.json（强制Unicode转义）
        with open(info_path, 'w', encoding='ascii') as f:
            json.dump(
                generate_info_json(image_files, os.path.basename(category_path), icon_file),
                f,
                ensure_ascii=True,
                indent=2
            )
        
        print(f'成功处理目录: {category_path}')
        print(f'  发现 {len(image_files)} 个图片文件')
        print(f'  使用图标: {icon_file}')
        return True
        
    except Exception as e:
        print(f'处理目录 {category_path} 时出错: {str(e)}')
        return False

def main():
    print("=== Waline 表情包JSON生成器 ===")
    print("将遍历emoji目录并生成index.json和info.json")
    
    # 询问是否覆盖已存在文件
    overwrite = False
    while True:
        choice = input("是否重新生成所有已存在的JSON文件？(y/n): ").lower()
        if choice == 'y':
            overwrite = True
            break
        elif choice == 'n':
            break
        print("请输入 y 或 n")
    
    root_dir = 'emoji'
    if not os.path.exists(root_dir):
        print(f"错误: 目录 {root_dir} 不存在")
        return
    
    processed = 0
    skipped = 0
    errors = 0
    
    print("\n开始处理目录...")
    for category in os.listdir(root_dir):
        category_path = os.path.join(root_dir, category)
        if os.path.isdir(category_path):
            if process_directory(category_path, overwrite):
                processed += 1
            else:
                skipped += 1
    
    print("\n=== 处理完成 ===")
    print(f"已处理目录: {processed}")
    print(f"已跳过目录: {skipped}")
    print(f"错误目录: {errors}")

if __name__ == '__main__':
    main()