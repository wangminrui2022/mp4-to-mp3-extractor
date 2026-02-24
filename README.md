# 🎵 OpenClaw Skill: MP4 to MP3 Extractor

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://github.com/openclaw/openclaw)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

这是一个为 [OpenClaw](https://github.com/openclaw/openclaw) 量身定制的本地自动化 Skill。它能批量扫描指定目录及其子目录下的 `.mp4` 视频文件，并利用 `ffmpeg` 高效提取出 `.mp3` 音频。

最核心的亮点是：它不仅能**完美保留原始的文件夹多级层级结构**，还具备**自引导（Self-bootstrapping）能力**，能够全自动创建和管理 Python 虚拟环境，实现真正的“开箱即用”。

---

## ✨ 核心特性

* **📂 完美的结构保持**：自动将源目录的多级子文件夹原样映射到目标目录，文件再多也不会乱。
* **🤖 自动化虚拟环境 (venv)**：
  * 首次运行时，脚本会自动检测并执行 `python -m venv venv`。
  * 智能兼容 Windows (`Scripts/python.exe`) 与 Linux/macOS (`bin/python`) 环境路径。
  * 零侵入性，绝不污染你的全局 Python 环境。
* **⚡ 高效无损提取**：直接调用系统原生的 `ffmpeg` 进行处理，默认输出 192kbps 的高质量音频。
* **🧠 深度集成 OpenClaw**：通过精心编写的 `SKILL.md`，Agent 能够精准理解意图并自动推断缺省的目标路径。

---

## 🛠️ 前置要求

在运行此 Skill 之前，请确保宿主机（运行 OpenClaw 的机器）已安装以下系统级依赖：

1. **Python 3.8 或更高版本**
2. **FFmpeg**: 必须将其添加到系统的环境变量 (PATH) 中。
   * *验证方法：在终端中输入 `ffmpeg -version` 和 `python --version`，若能正常输出版本号即可。*

---

## 🚀 安装指南

将本仓库克隆到你的 OpenClaw 工作区的 `skills/` 目录下即可：

```bash
# 进入你的 OpenClaw skills 目录
cd ~/.openclaw/skills  # 视你的实际安装路径而定

# 克隆本仓库
git clone [https://github.com/你的用户名/mp4-to-mp3-extractor.git](https://github.com/你的用户名/mp4-to-mp3-extractor.git)

# 重启你的 OpenClaw Agent 让其重新加载 Skill 索引