import os
import sys
import subprocess
import venv
import logging
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

def setup_venv():
    """检查并确保在虚拟环境中运行"""
    if os.name == "nt":
        venv_python = VENV_DIR / "Scripts" / "python.exe"
    else:
        venv_python = VENV_DIR / "bin" / "python"

    if sys.executable.lower() == str(venv_python).lower():
        return 

    if not VENV_DIR.exists():
        logger.info(f"未检测到虚拟环境，正在创建: {VENV_DIR}")
        venv.create(VENV_DIR, with_pip=True)
        logger.info("虚拟环境创建成功。")

    logger.info("正在切换至虚拟环境上下文...")
    # 使用虚拟环境执行时，日志会继续记录
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