import json
import os
from collections import defaultdict
from statistics import mean

def analyze_projects_summary():
    """
    分析projects_summary.jsonl文件，统计翻译语言对数量和覆盖率信息
    """
    
    # 检查文件是否存在
    if not os.path.exists('projects_summary.jsonl'):
        print("错误：当前目录下未找到projects_summary.jsonl文件")
        return
    
    # 存储数据的字典
    translation_pairs = defaultdict(int)  # 语言对计数
    coverage_data = defaultdict(lambda: {'line': [], 'branch': []})  # 覆盖率数据
    project_names = defaultdict(list)  # 存储每个语言对的项目名称
    
    # 读取和解析JSONL文件
    with open('projects_summary.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                
                # 获取源语言和目标语言
                source_lang = data.get('source_language', '')
                target_lang = data.get('target_language', '')
                
                if source_lang and target_lang:
                    # 统计翻译语言对
                    pair = f"{source_lang} → {target_lang}"
                    translation_pairs[pair] += 1
                    
                    # 存储项目名称
                    project_name = data.get('project_name', '')
                    project_names[pair].append(project_name)
                    
                    # 统计覆盖率信息
                    coverage = data.get('coverage', {})
                    if coverage and isinstance(coverage, dict):
                        if 'line' in coverage:
                            coverage_data[pair]['line'].append(coverage['line'])
                        if 'branch' in coverage:
                            coverage_data[pair]['branch'].append(coverage['branch'])
                
            except json.JSONDecodeError:
                continue
    
    # 打印统计表格
    print("=" * 80)
    print("翻译语言对统计表（包含覆盖率信息）")
    print("=" * 80)
    print(f"{'Translation Pair':<25} {'Count':<8} {'Line Coverage':<15} {'Branch Coverage':<15}")
    print("-" * 70)
    
    total_count = 0
    all_line_coverage = []
    all_branch_coverage = []
    
    for pair in sorted(translation_pairs.keys()):
        count = translation_pairs[pair]
        total_count += count
        
        # 计算平均覆盖率
        line_coverage = coverage_data[pair]['line']
        branch_coverage = coverage_data[pair]['branch']
        
        avg_line = mean(line_coverage) if line_coverage else 0
        avg_branch = mean(branch_coverage) if branch_coverage else 0
        
        all_line_coverage.extend(line_coverage)
        all_branch_coverage.extend(branch_coverage)
        
        print(f"{pair:<25} {count:<8} {avg_line:<15.2f} {avg_branch:<15.2f}")
    
    # 打印总计行
    overall_line = mean(all_line_coverage) if all_line_coverage else 0
    overall_branch = mean(all_branch_coverage) if all_branch_coverage else 0
    
    print("-" * 70)
    print(f"{'Total':<25} {total_count:<8} {overall_line:<15.2f} {overall_branch:<15.2f}")
    
    # 检查Python → Rust缺少的项目
    print("\n" + "=" * 80)
    print("检查Python → Rust缺少的项目")
    print("=" * 80)
    
    python_projects = set(project_names.get("Python → C++", []))
    rust_projects = set(project_names.get("Python → Rust", []))
    
    missing_projects = python_projects - rust_projects
    
    if missing_projects:
        print(f"Python → Rust缺少的项目 ({len(missing_projects)}个):")
        for project in sorted(missing_projects):
            print(f"  - {project}")
    else:
        print("没有缺少的项目")
        
    print(f"\nPython → C++项目数: {len(python_projects)}")
    print(f"Python → Rust项目数: {len(rust_projects)}")

if __name__ == "__main__":
    analyze_projects_summary()