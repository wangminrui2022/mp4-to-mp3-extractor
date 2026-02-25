# 🎵 OpenClaw Skills: MP4 to MP3 Extractor

[![OpenClaw Skills](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://github.com/openclaw/openclaw)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-orange.svg)](https://ffmpeg.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

这是一个为 [OpenClaw](https://github.com/openclaw/openclaw) 量身定制的本地自动化 Skills。它能批量扫描指定目录及其子目录下的 `.mp4` 视频文件，并利用 `ffmpeg` 高效提取出 `.mp3` 音频。

最核心的亮点是：它不仅能**完美保留原始的文件夹多级层级结构**，还具备**自引导（Self-bootstrapping）能力**，能够全自动创建和管理 Python 虚拟环境，实现真正的“开箱即用”。

---

## ✨ 核心特性

* **📂 完美的结构保持**：自动将源目录的多级子文件夹原样映射到目标目录，文件再多也不会乱。
* **🤖 自动化虚拟环境 (venv)**：
  * 首次运行时，脚本会自动检测并执行 `python -m venv venv`。
  * 智能兼容 Windows (`Scripts/python.exe`) 与 Linux/macOS (`bin/python`) 环境路径。
  * 零侵入性，绝不污染你的全局 Python 环境。
* **⚡ 高效无损提取**：直接调用系统原生的 `ffmpeg` 进行处理，默认输出 192kbps 的高质量音频。
* **📝 工业级日志审计**：
  * **全流程记录**：从环境创建、文件扫描到每一个转换细节，均有据可查。
  * **自动循环清理**：采用滚动日志技术，**仅保留最近 3 天的记录**，防止磁盘爆满。
* **🧠 深度集成 OpenClaw**：通过精心编写的 `SKILL.md`，Agent 能够精准理解意图并自动推断缺省的目标路径。

---

## 🛠️ 前置要求

在运行此 Skills 之前，请确保宿主机（运行 OpenClaw 的机器）已安装以下系统级依赖：

1. **Python 3.8 或更高版本**
插件安装之后显示blocked，是没有找python，需要建立到标准路径的软链接，终端输入以下命令：
**/usr/local/python312/bin/python3是python安装目录。*
sudo ln -s /usr/local/python312/bin/python3 /usr/local/python312/bin/python
sudo ln -s /usr/local/python312/bin/python3 /usr/bin/python

2. **FFmpeg**: 必须将其添加到系统的环境变量 (PATH) 中。
   * *验证方法：在终端中输入 `ffmpeg -version` 和 `python --version`，若能正常输出版本号即可。*

---

## 🚀 安装指南

将本仓库克隆到你的 OpenClaw 工作区的 `skills/` 目录下即可：

```bash
# 进入你的 OpenClaw skills 目录
cd /opt/openclaw-2026.2.14  # 视你的实际安装路径而定

# 安装skills
npx skills add https://github.com/wangminrui2022/mp4-to-mp3-extractor
选项：
Installation scope 选择 Global
Installation method 选择 Copy to all agents (Independent copies for each agent)

# 安装完成在以下两个目录可以看到该技能
ls ~/.openclaw/skills/mp4-to-mp3-extractor/
ls /home/admin/.agents/skills/mp4-to-mp3-extractor/

#现在你可以在聊天界面里直接对你的 Agent 说：
请严格使用 skills 列表中的「mp4-to-mp3-extractor」技能完成以下任务：
1. 递归遍历源目录 /home/admin/Videos/Tutorials 下所有 .mp4 文件（包括所有子文件夹）。
2. 对每个找到的 .mp4 文件，使用 mp4-to-mp3-extractor 技能提取音频，转换为 .mp3 文件。
3. 输出路径为 /home/admin/Audio/Tutorials，并完全保持原有的文件夹结构（例如：源文件在 Videos/Tutorials/xxx/yyy/abc.mp4，则输出必须是 Audio/Tutorials/xxx/yyy/abc.mp3）。
4. 如果目标子目录不存在，请自动创建。
5. mp3 文件名必须与原 mp4 文件名完全一致，仅将扩展名改为 .mp3。
6. 批量处理所有文件，完成后告诉我总共转换了多少个文件以及是否全部成功。