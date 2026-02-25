#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: MP4 to MP3 Extractor for OpenClaw
Author: 王岷瑞/https://github.com/wangminrui2022
License: MIT License
Description: 批量将指定目录下的 .mp4 视频文件提取为 .mp3 音频文件，保持原文件夹结构。
             具备自动创建虚拟环境和日志循环管理功能。
"""
import os
import sys
import subprocess
import venv
import logging
import shutil
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# --- 基础路径配置 ---
SCRIPT_PATH = Path(__file__).resolve()
SKILL_ROOT = SCRIPT_PATH.parent.parent
VENV_DIR = SKILL_ROOT / "venv"
LOG_DIR = SKILL_ROOT / "logs"

# --- 日志系统初始化 ---
def setup_logger():
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / "skill_execution.log"

    logger = logging.getLogger("OpenClawExtractor")
    logger.setLevel(logging.INFO)

    # 防止重复添加 Handler
    if not logger.handlers:
        # 1. 格式化器: 包含时间、日志级别、具体信息
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # 2. 文件 Handler: 按天(D)滚动，间隔1天，保留最近3个备份(backupCount=3)
        file_handler = TimedRotatingFileHandler(
            log_file, when="D", interval=1, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 3. 控制台 Handler: 让 OpenClaw 的终端也能看到信息
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()

def get_python_cmd():
    """动态获取当前系统可用的 Python 命令"""
    for cmd in ["python3", "python"]:
        if shutil.which(cmd):
            return cmd
    return sys.executable # 如果都找不到，回退到当前运行的解释器

def setup_venv():
    """检查并确保在虚拟环境中运行"""
    # 1. 确定虚拟环境内部的 Python 路径
    if os.name == "nt":
        venv_python = VENV_DIR / "Scripts" / "python.exe"
    else:
        venv_python = VENV_DIR / "bin" / "python"

    # 2. 如果已经在虚拟环境中，直接返回
    if sys.executable.lower() == str(venv_python).lower():
        return 

    # 3. 如果没在虚拟环境，先检查是否存在，不存在则创建
    if not VENV_DIR.exists():
        logger.info(f"正在创建虚拟环境...")
        # 动态获取系统 Python 命令来创建 venv
        base_python = get_python_cmd()
        subprocess.run([base_python, "-m", "venv", str(VENV_DIR)], check=True)
        logger.info("虚拟环境创建成功。")

    # 4. 切换到虚拟环境 Python 执行
    logger.info("切换至虚拟环境上下文...")
    result = subprocess.run([str(venv_python), str(SCRIPT_PATH)] + sys.argv[1:])
    sys.exit(result.returncode)

def extract_audio(src_dir, dest_dir):
    """提取音频核心逻辑"""
    src_path = Path(src_dir).resolve()
    dest_path = Path(dest_dir).resolve()

    logger.info(f"--- 开始任务: 从 {src_path} 提取音频 ---")

    if not src_path.is_dir():
        logger.error(f"源目录不存在: {src_path}")
        sys.exit(1)

    mp4_files = list(src_path.rglob("*.mp4"))
    if not mp4_files:
        logger.warning("扫描完成：未发现任何 .mp4 文件。")
        sys.exit(0)

    logger.info(f"扫描完成，发现 {len(mp4_files)} 个视频文件。目标路径: {dest_path}")

    success = 0
    fail = 0

    for mp4_file in mp4_files:
        rel_path = mp4_file.relative_to(src_path)
        out_file = dest_path / rel_path.with_suffix(".mp3")
        
        logger.info(f"正在处理: {rel_path}")
        
        try:
            out_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 执行 ffmpeg
            cmd = [
                "ffmpeg", "-y", "-i", str(mp4_file),
                "-vn", "-b:a", "192k", str(out_file)
            ]
            
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode == 0:
                logger.info(f"成功提取: {out_file.name}")
                success += 1
            else:
                logger.error(f"FFmpeg 报错 ({mp4_file.name}): {process.stderr.strip()}")
                fail += 1
                
        except Exception as e:
            logger.error(f"系统错误 ({mp4_file.name}): {str(e)}")
            fail += 1

    logger.info(f"--- 任务结束: 成功 {success}, 失败 {fail} ---")
    print(f"\n[结果反馈] 成功: {success} | 失败: {fail}")

if __name__ == "__main__":
    setup_venv()
    
    if len(sys.argv) < 3:
        logger.error("参数不足。用法: python extract.py <源目录> <目标目录>")
        sys.exit(1)
        
    extract_audio(sys.argv[1], sys.argv[2])