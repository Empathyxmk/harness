#!/usr/bin/env python3
# file path: batch_run.py

import json
import os
import subprocess
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import threading

def read_projects_summary(file_path):
    """读取projects_summary.jsonl文件"""
    projects = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    project = json.loads(line.strip())
                    projects.append(project)
        print(f"📋 Loaded {len(projects)} projects from {file_path}")
        return projects
    except Exception as e:
        print(f"❌ Failed to read {file_path}: {e}")
        return []

def group_by_translation_pairs(projects):
    """按翻译对（源语言→目标语言）分组项目"""
    translation_pairs = defaultdict(list)
    
    for project in projects:
        source_lang = project.get('source_language', '')
        target_lang = project.get('target_language', '')
        
        if source_lang and target_lang:
            pair_key = f"{source_lang}→{target_lang}"
            translation_pairs[pair_key].append(project)
    
    return translation_pairs

def select_projects_to_run(translation_pairs, max_per_pair=5):
    """为每个翻译对选择前N个项目"""
    selected_projects = []
    
    for pair_key, projects in translation_pairs.items():
        # 按项目名称排序以确保一致性
        sorted_projects = sorted(projects, key=lambda x: x.get('project_name', ''))
        
        # 选择前max_per_pair个项目
        selected = sorted_projects[:max_per_pair]
        selected_projects.extend(selected)
        
        print(f"📦 {pair_key}: Selected {len(selected)} out of {len(projects)} projects")
        for project in selected:
            print(f"   - {project.get('project_name', 'Unknown')}")
    
    return selected_projects

def run_single_translation(args):
    """运行单个翻译任务 - 用于多进程"""
    project, base_dir, max_iterations, process_id = args
    
    project_name = project.get('project_name', '')
    source_language = project.get('source_language', '')
    target_language = project.get('target_language', '')
    
    print(f"🚀 [P{process_id:02d}] Starting: {project_name} ({source_language} → {target_language})")
    
    # 构建命令
    cmd = [
        'python', '-m', 'RepoTransAgent.run',
        '--project_name', project_name,
        '--source_language', source_language,
        '--target_language', target_language,
        '--max_iterations', str(max_iterations)
    ]
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 执行命令
        result = subprocess.run(
            cmd,
            cwd=base_dir,
            capture_output=True,
            text=True,
            timeout=1800  # 10分钟超时
        )
        
        # 计算执行时间
        execution_time = time.time() - start_time
        
        # 判断结果
        if result.returncode == 0:
            status = "✅ SUCCESS"
        elif result.returncode == 1:
            status = "❌ FAILED"
        elif result.returncode == 2:
            status = "⏱️ TIMEOUT"
        elif result.returncode == 3:
            status = "🛑 INTERRUPTED"
        else:
            status = f"❌ ERROR (code: {result.returncode})"
        
        print(f"[P{process_id:02d}] {status} - {project_name} - {execution_time:.1f}s")
        
        return {
            'project_name': project_name,
            'source_language': source_language,
            'target_language': target_language,
            'status': status,
            'return_code': result.returncode,
            'execution_time': execution_time,
            'process_id': process_id,
            'stdout': result.stdout[-2000:],  # 只保留最后2000字符
            'stderr': result.stderr[-2000:]   # 只保留最后2000字符
        }
        
    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        print(f"[P{process_id:02d}] ⏱️ TIMEOUT - {project_name} - {execution_time:.1f}s")
        
        return {
            'project_name': project_name,
            'source_language': source_language,
            'target_language': target_language,
            'status': "⏱️ TIMEOUT",
            'return_code': -1,
            'execution_time': execution_time,
            'process_id': process_id,
            'stdout': '',
            'stderr': 'Process timed out after 30 minutes'
        }
        
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"[P{process_id:02d}] 💥 EXCEPTION - {project_name} - {str(e)}")
        
        return {
            'project_name': project_name,
            'source_language': source_language,
            'target_language': target_language,
            'status': f"💥 EXCEPTION: {str(e)}",
            'return_code': -2,
            'execution_time': execution_time,
            'process_id': process_id,
            'stdout': '',
            'stderr': str(e)
        }

class ProgressTracker:
    """进度跟踪器"""
    def __init__(self, total_tasks):
        self.total_tasks = total_tasks
        self.completed_tasks = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.results = []
    
    def update(self, result):
        with self.lock:
            self.completed_tasks += 1
            self.results.append(result)
            
            elapsed = time.time() - self.start_time
            if self.completed_tasks > 0:
                avg_time = elapsed / self.completed_tasks
                estimated_remaining = (self.total_tasks - self.completed_tasks) * avg_time
                
                success_count = len([r for r in self.results if r['return_code'] == 0])
                
                print(f"📊 Progress: {self.completed_tasks}/{self.total_tasks} "
                      f"({self.completed_tasks/self.total_tasks*100:.1f}%) - "
                      f"Success: {success_count}/{self.completed_tasks} - "
                      f"ETA: {estimated_remaining/60:.1f}min")

def run_parallel_translations(selected_projects, base_dir, max_iterations, num_processes=20):
    """并行运行翻译任务"""
    print(f"\n🚀 Starting parallel translation with {num_processes} processes...")
    print(f"   Total projects: {len(selected_projects)}")
    print(f"   Max iterations per project: {max_iterations}")
    print(f"   Timeout per project: 30 minutes")
    
    # 准备参数
    task_args = []
    for i, project in enumerate(selected_projects):
        task_args.append((project, base_dir, max_iterations, i + 1))
    
    # 初始化进度跟踪器
    tracker = ProgressTracker(len(selected_projects))
    
    # 开始并行执行
    results = []
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # 提交所有任务
        future_to_args = {executor.submit(run_single_translation, args): args for args in task_args}
        
        # 处理完成的任务
        for future in as_completed(future_to_args):
            try:
                result = future.result()
                results.append(result)
                tracker.update(result)
                
            except Exception as e:
                args = future_to_args[future]
                project = args[0]
                process_id = args[3]
                
                error_result = {
                    'project_name': project.get('project_name', ''),
                    'source_language': project.get('source_language', ''),
                    'target_language': project.get('target_language', ''),
                    'status': f"💥 EXECUTOR ERROR: {str(e)}",
                    'return_code': -3,
                    'execution_time': 0,
                    'process_id': process_id,
                    'stdout': '',
                    'stderr': str(e)
                }
                results.append(error_result)
                tracker.update(error_result)
                
                print(f"[P{process_id:02d}] 💥 EXECUTOR ERROR: {e}")
    
    total_time = time.time() - start_time
    print(f"\n🏁 Parallel execution completed in {total_time/60:.1f} minutes")
    
    return results

def save_results(results, output_file):
    """保存结果到文件"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存详细结果到JSON
    json_file = f"batch_results_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 保存简要报告到文本文件
    report_file = f"batch_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("PARALLEL BATCH TRANSLATION RESULTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Projects: {len(results)}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Execution Mode: Parallel (20 processes)\n\n")
        
        # 统计
        success_count = len([r for r in results if r['return_code'] == 0])
        failed_count = len([r for r in results if r['return_code'] == 1])
        timeout_count = len([r for r in results if r['return_code'] == 2])
        error_count = len([r for r in results if r['return_code'] not in [0, 1, 2]])
        
        f.write("SUMMARY:\n")
        f.write(f"✅ Success: {success_count} ({success_count/len(results)*100:.1f}%)\n")
        f.write(f"❌ Failed: {failed_count} ({failed_count/len(results)*100:.1f}%)\n")
        f.write(f"⏱️ Timeout: {timeout_count} ({timeout_count/len(results)*100:.1f}%)\n")
        f.write(f"💥 Error: {error_count} ({error_count/len(results)*100:.1f}%)\n\n")
        
        # 执行时间统计
        execution_times = [r['execution_time'] for r in results if r['execution_time'] > 0]
        if execution_times:
            f.write("EXECUTION TIME STATS:\n")
            f.write(f"Average: {sum(execution_times)/len(execution_times):.1f}s\n")
            f.write(f"Min: {min(execution_times):.1f}s\n")
            f.write(f"Max: {max(execution_times):.1f}s\n\n")
        
        # 按翻译对分组统计
        pairs_stats = defaultdict(list)
        for result in results:
            pair_key = f"{result['source_language']}→{result['target_language']}"
            pairs_stats[pair_key].append(result)
        
        f.write("BY TRANSLATION PAIR:\n")
        for pair_key, pair_results in pairs_stats.items():
            pair_success = len([r for r in pair_results if r['return_code'] == 0])
            f.write(f"{pair_key}: {pair_success}/{len(pair_results)} success ({pair_success/len(pair_results)*100:.1f}%)\n")
        
        f.write("\nDETAILED RESULTS:\n")
        f.write("-" * 80 + "\n")
        
        # 按完成时间排序
        sorted_results = sorted(results, key=lambda x: x.get('process_id', 0))
        
        for result in sorted_results:
            f.write(f"Project: {result['project_name']} [P{result.get('process_id', 0):02d}]\n")
            f.write(f"Translation: {result['source_language']} → {result['target_language']}\n")
            f.write(f"Status: {result['status']}\n")
            f.write(f"Time: {result['execution_time']:.1f}s\n")
            if result['stderr'] and result['stderr'] != 'Process timed out after 30 minutes':
                f.write(f"Error: {result['stderr'][:200]}...\n")
            f.write("-" * 40 + "\n")
    
    print(f"\n📊 Results saved to:")
    print(f"   📋 Detailed: {json_file}")
    print(f"   📄 Report: {report_file}")

def main():
    print("🤖 Parallel Batch Translation Runner")
    print("=" * 50)
    
    # 配置
    projects_summary_path = "/workspace/target_projects/projects_summary.jsonl"
    base_dir = "/workspace/methods"
    max_per_pair = 1000
    max_iterations = 20
    num_processes = 50
    
    # 检查路径
    if not os.path.exists(projects_summary_path):
        print(f"❌ projects_summary.jsonl not found at: {projects_summary_path}")
        sys.exit(1)
    
    if not os.path.exists(base_dir):
        print(f"❌ Base directory not found: {base_dir}")
        sys.exit(1)
    
    # 检查CPU核心数
    cpu_count = mp.cpu_count()
    print(f"💻 System CPU cores: {cpu_count}")
    if num_processes > cpu_count:
        print(f"⚠️ Warning: Using {num_processes} processes on {cpu_count} cores")
    
    # 读取项目
    projects = read_projects_summary(projects_summary_path)
    if not projects:
        print("❌ No projects found")
        sys.exit(1)
    
    # 按翻译对分组
    translation_pairs = group_by_translation_pairs(projects)
    print(f"\n📦 Found {len(translation_pairs)} translation pairs:")
    for pair_key, projects_list in translation_pairs.items():
        print(f"   {pair_key}: {len(projects_list)} projects")
    
    # 选择要运行的项目
    selected_projects = select_projects_to_run(translation_pairs, max_per_pair)
    # import pandas as pd
    # df = pd.DataFrame(selected_projects)
    # selected_projects = df.groupby(['source_language', 'target_language']).head(10).to_dict('records')
    # print(len(selected_projects))
    # exit()
    # 断点续传：过滤已完成项目
    completed = set()
    model_name = "claude-sonnet-4-20250514"
    logs_dir = Path(f"/workspace/methods/logs/{model_name.replace('/', '_')}")
    if logs_dir.exists():
        for log_dir in logs_dir.rglob("*/"):
            if (log_dir / "final_summary.txt").exists():
                # if 'Java_to_Python' not in log_dir.name:
                parts = log_dir.name.split('_')
                completed.add('_'.join(parts[:-2]))
                # with open(log_dir / "final_summary.txt", "r") as f:
                #     final_summary = f.read()
                # if ("Final Status: success" in final_summary):
                #     parts = log_dir.name.split('_')
                #     completed.add('_'.join(parts[:-2]))
    # print(completed)
    selected_projects = [p for p in selected_projects if f"{p['project_name']}_{p['source_language']}_to_{p['target_language']}" not in completed]
    selected_projects = selected_projects[::-1]
    # print(len(selected_projects))
    # exit()
    # selected_projects = [project for project in selected_projects if (project['target_language'] in ["Rust"]) and (project['source_language'] in ["Python"]) and (project['project_name'] in ["ramonhagenaars_jsons", "socialwifi_RouterOS-api"])]
    # print(len(selected_projects))
    # exit()
    print(f"\n🎯 Selected {len(selected_projects)} projects to run")
    
    # 确认运行
    print(f"\n⚡ Configuration:")
    print(f"   📊 Projects: {len(selected_projects)}")
    print(f"   🔄 Processes: {num_processes}")
    print(f"   🔁 Max iterations per project: {max_iterations}")
    print(f"   ⏱️ Timeout per project: 30 minutes")
    
    response = input(f"\n继续并行运行这 {len(selected_projects)} 个项目? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled by user")
        sys.exit(0)
    
    # 开始并行批量运行
    results = run_parallel_translations(selected_projects, base_dir, max_iterations, num_processes)
    
    # 保存结果
    save_results(results, "batch_results")
    
    # 显示最终统计
    success_count = len([r for r in results if r['return_code'] == 0])
    print(f"\n📊 Final Stats: {success_count}/{len(results)} projects succeeded ({success_count/len(results)*100:.1f}%)")
    
    # 显示各状态的项目数
    status_counts = defaultdict(int)
    for result in results:
        if result['return_code'] == 0:
            status_counts['Success'] += 1
        elif result['return_code'] == 1:
            status_counts['Failed'] += 1
        elif result['return_code'] == 2:
            status_counts['Timeout'] += 1
        else:
            status_counts['Error'] += 1
    
    print(f"📈 Breakdown:")
    for status, count in status_counts.items():
        print(f"   {status}: {count}")

if __name__ == "__main__":
    main()