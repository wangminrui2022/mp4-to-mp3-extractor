import os
import sys
import subprocess
import venv
from pathlib import Path

# 获取当前脚本所在目录和 Skill 根目录
SCRIPT_PATH = Path(__file__).resolve()
SKILL_ROOT = SCRIPT_PATH.parent.parent
VENV_DIR = SKILL_ROOT / "venv"

def setup_venv():
    """检查并确保在虚拟环境中运行"""
    # 确定虚拟环境中的 Python 解释器路径
    if os.name == "nt":  # Windows
        venv_python = VENV_DIR / "Scripts" / "python.exe"
    else:  # Linux/macOS
        venv_python = VENV_DIR / "bin" / "python"

    # 1. 检查当前是否已经在该虚拟环境下运行
    if sys.executable.lower() == str(venv_python).lower():
        return # 已在虚拟环境中，直接返回继续执行业务逻辑

    # 2. 如果虚拟环境文件夹不存在，则创建它
    if not VENV_DIR.exists():
        print(f"正在创建 Python 虚拟环境: {VENV_DIR}...")
        venv.create(VENV_DIR, with_pip=True)
        print("虚拟环境创建成功。")

    # 3. 使用虚拟环境中的 Python 重新运行当前脚本
    # sys.argv 包含了传递给脚本的所有参数
    print("切换至虚拟环境运行...")
    result = subprocess.run([str(venv_python), str(SCRIPT_PATH)] + sys.argv[1:])
    sys.exit(result.returncode)

def extract_audio(src_dir, dest_dir):
    """核心业务逻辑：提取音频"""
    src_path = Path(src_dir).resolve()
    dest_path = Path(dest_dir).resolve()

    if not src_path.is_dir():
        print(f"错误: 源目录 '{src_dir}' 不存在。")
        sys.exit(1)

    mp4_files = list(src_path.rglob("*.mp4"))
    if not mp4_files:
        print("未找到 .mp4 文件。")
        sys.exit(0)

    print(f"开始处理 {len(mp4_files)} 个文件...")

    for mp4_file in mp4_files:
        rel_path = mp4_file.relative_to(src_path)
        out_file = dest_path / rel_path.with_suffix(".mp3")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = ["ffmpeg", "-y", "-i", str(mp4_file), "-vn", "-b:a", "192k", str(out_file)]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"\n任务完成！音频已提取至: {dest_path}")

if __name__ == "__main__":
    # 第一步：先处理虚拟环境逻辑
    setup_venv()
    
    # 第二步：执行真正的业务逻辑
    if len(sys.argv) < 3:
        print("用法: python extract.py <源目录> <目标目录>")
        sys.exit(1)
        
    extract_audio(sys.argv[1], sys.argv[2])