# 添加外部 Skills 完整指南

这个 collection 的主要用途就是**管理来自各种来源的 skills**！

## 🎯 核心概念

**claude-skills-collection 是你的 Skills 管理中心**

就像：
- 📦 npm 管理 JavaScript 包
- 🐍 pip 管理 Python 包
- 🍺 Homebrew 管理 macOS 软件

**claude-skills-collection 管理你的 AI Skills**

---

## 📥 从各种来源添加 Skills

### 1️⃣ 从 ClawHub（5,705+ skills）

```bash
# 第一步：搜索你想要的 skill
clawhub search pdf

# 输出示例：
# pdf-analyzer    - Extract and analyze PDF documents
# pdf-to-text     - Convert PDF to text
# pdf-merger      - Merge multiple PDFs

# 第二步：下载到临时目录
cd /tmp
clawhub install pdf-analyzer

# 第三步：找到下载位置（通常在 ~/.openclaw/skills/）
ls ~/.openclaw/skills/

# 第四步：复制到你的 collection
cp -r ~/.openclaw/skills/pdf-analyzer ~/00zyf/AI/claude-skills-collection/

# 第五步：注册并安装到所有平台
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh pdf-analyzer
./scripts/install-universal.sh pdf-analyzer

# 完成！现在这个 skill 在你所有 AI 工具中都可用了
```

---

### 2️⃣ 从 GitHub/社区

```bash
# 第一步：找到你想要的 skill（例如从 awesome-claude-skills）
# https://github.com/travisvn/awesome-claude-skills

# 第二步：克隆到临时目录
cd /tmp
git clone https://github.com/someone/awesome-skill.git

# 第三步：移动到你的 collection
mv awesome-skill ~/00zyf/AI/claude-skills-collection/

# 第四步：检查是否有 SKILL.md
cd ~/00zyf/AI/claude-skills-collection/awesome-skill
ls -la

# 如果没有 SKILL.md，创建一个
if [ ! -f "SKILL.md" ]; then
    cat > SKILL.md << 'EOF'
---
name: awesome-skill
description: Brief description from README
version: 1.0.0
usage: awesome-skill [options]
---

See README.md for details.
EOF
fi

# 第五步：注册并安装
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh awesome-skill
./scripts/install-universal.sh awesome-skill
```

---

### 3️⃣ 从 Anthropic 官方仓库

```bash
# 第一步：克隆官方仓库
cd /tmp
git clone https://github.com/anthropics/skills.git

# 第二步：浏览可用的 skills
cd skills
ls -d */

# 第三步：选择并复制到你的 collection
cp -r document-analyzer ~/00zyf/AI/claude-skills-collection/

# 第四步：注册并安装
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh document-analyzer
./scripts/install-universal.sh document-analyzer
```

---

### 4️⃣ 手动下载的 Skills

```bash
# 假设你从网上下载了一个 skill 压缩包

# 第一步：解压到你的 collection
cd ~/Downloads
unzip cool-skill.zip
mv cool-skill ~/00zyf/AI/claude-skills-collection/

# 第二步：进入 collection
cd ~/00zyf/AI/claude-skills-collection

# 第三步：检查 skill 结构
cd cool-skill
ls

# 确保有这些文件：
# - SKILL.md（必需）
# - 主程序文件（.py, .sh 等）
# - requirements.txt（如果有依赖）

# 第四步：注册并安装
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh cool-skill
./scripts/install-universal.sh cool-skill
```

---

### 5️⃣ 自己创建的 Skills

```bash
cd ~/00zyf/AI/claude-skills-collection

# 使用模板快速创建
./scripts/create-skill.sh my-custom-tool productivity

# 编辑并实现功能
cd my-custom-tool
# ... 编写代码 ...

# 注册并安装
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh my-custom-tool
./scripts/install-universal.sh my-custom-tool
```

---

## 🔧 完整工作流示例

### 场景：添加 3 个不同来源的 skills

```bash
# 准备工作
cd ~/00zyf/AI/claude-skills-collection

# ──────────────────────────────────────
# Skill 1: 从 ClawHub 下载 pdf-analyzer
# ──────────────────────────────────────
clawhub search pdf
clawhub install pdf-analyzer
cp -r ~/.openclaw/skills/pdf-analyzer .
./scripts/register.sh pdf-analyzer
./scripts/install-universal.sh pdf-analyzer

# ──────────────────────────────────────
# Skill 2: 从 GitHub 克隆 code-reviewer
# ──────────────────────────────────────
cd /tmp
git clone https://github.com/user/code-reviewer.git
mv code-reviewer ~/00zyf/AI/claude-skills-collection/
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh code-reviewer
./scripts/install-universal.sh code-reviewer

# ──────────────────────────────────────
# Skill 3: 自己创建 data-visualizer
# ──────────────────────────────────────
./scripts/create-skill.sh data-visualizer data
cd data-visualizer
# ... 实现功能 ...
cd ..
./scripts/register.sh data-visualizer
./scripts/install-universal.sh data-visualizer

# ──────────────────────────────────────
# 查看所有 skills
# ──────────────────────────────────────
./scripts/list.sh

# 输出：
# 📚 Available Skills
#
#   citation-grabber (1.1.0)
#   📁 citation-grabber
#   📝 Fetch scientific paper citations...
#
#   pdf-analyzer (1.0.0)
#   📁 pdf-analyzer
#   📝 Extract and analyze PDF documents...
#
#   code-reviewer (2.1.0)
#   📁 code-reviewer
#   📝 Automated code review and suggestions...
#
#   data-visualizer (0.1.0)
#   📁 data-visualizer
#   📝 Generate charts from data...
#
# Total skills: 4
```

---

## 📊 目录结构（添加多个 skills 后）

```
claude-skills-collection/
├── citation-grabber/        ← 你自己的（独立仓库引用）
├── pdf-analyzer/            ← 从 ClawHub 下载
├── code-reviewer/           ← 从 GitHub 克隆
├── anthropic-summarizer/    ← 从 Anthropic 官方
├── data-visualizer/         ← 自己创建
├── image-processor/         ← 社区下载
├── web-scraper/            ← 手动添加
│
├── docs/                    ← 文档
├── scripts/                 ← 管理工具
└── registry.json            ← 所有 skills 的注册表
```

**关键点：** 无论 skill 来自哪里，都统一管理！

---

## 🎯 为什么要用 Collection 管理？

### ❌ 不用 Collection 的问题

```bash
# Skill 散落在各处
~/.claude/skills/skill1
~/.codex/skills/skill2
~/Downloads/skill3
~/Projects/skill4

# 每次要安装到新工具，都要手动复制
cp -r skill1 ~/.claude/skills/
cp -r skill1 ~/.codex/skills/
cp -r skill1 ~/.gemini/tools/
# ... 太麻烦了！

# 不知道安装了哪些
# 难以更新
# 没有统一的记录
```

### ✅ 用 Collection 的优势

```bash
# 所有 skills 在一个地方
~/00zyf/AI/claude-skills-collection/

# 一条命令安装到所有工具
./scripts/install-universal.sh skill-name

# 随时查看所有 skills
./scripts/list.sh

# 统一管理
./scripts/status.sh skill-name
./scripts/uninstall.sh skill-name
./scripts/register.sh skill-name

# 有完整的记录（registry.json）
```

---

## 🚀 实际使用示例

### 我想要一个 PDF 处理工具

```bash
# 1. 搜索
clawhub search pdf

# 2. 下载并添加到 collection
cd /tmp && clawhub install pdf-processor
cp -r ~/.openclaw/skills/pdf-processor ~/00zyf/AI/claude-skills-collection/

# 3. 注册并安装到所有平台
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh pdf-processor
./scripts/install-universal.sh pdf-processor

# 4. 现在可以在任何 AI 工具中使用了
# - Claude Code 中：直接调用
# - Gemini CLI 中：自动可用
# - Codex 中：已加载
```

### 我想创建自己的工具

```bash
cd ~/00zyf/AI/claude-skills-collection

# 1. 创建
./scripts/create-skill.sh email-sender productivity

# 2. 实现功能
cd email-sender
# 编写代码...

# 3. 注册并安装
cd ..
./scripts/register.sh email-sender
./scripts/install-universal.sh email-sender

# 4. 发布到 GitHub（可选）
cd email-sender
git init
git remote add origin https://github.com/yf8578/email-sender.git
git push -u origin main
```

---

## 💡 最佳实践

### 1. 保持 Collection 整洁

```bash
# 定期检查 skills
./scripts/list.sh

# 移除不需要的
./scripts/uninstall.sh unused-skill
rm -rf unused-skill
```

### 2. 备份你的 Collection

```bash
# 整个 collection 就是一个 Git 仓库
cd ~/00zyf/AI/claude-skills-collection
git add .
git commit -m "Add new skills"
git push
```

### 3. 文档化你的 Skills

在 `registry.json` 中维护完整信息：
- 来源
- 用途
- 版本
- 依赖

### 4. 定期更新

```bash
# 检查 ClawHub 上的更新
clawhub update pdf-analyzer

# 从 GitHub 拉取最新版本
cd /tmp
git clone https://github.com/user/skill.git
cp -r skill ~/00zyf/AI/claude-skills-collection/
```

---

## ❓ 常见问题

### Q: 所有下载的 skills 都兼容吗？

A: 大部分兼容，但需要检查：
- 是否有 SKILL.md 文件
- 依赖是否满足
- 是否需要特定平台功能

### Q: 如何知道 skill 的质量？

A: 检查这些指标：
- GitHub stars/ClawHub 下载量
- 文档完整性
- 更新频率
- 社区评价

### Q: 能自动更新 skills 吗？

A: 目前需要手动更新。未来可以添加 `update-all.sh` 脚本。

### Q: 如何分享我的 collection？

A:
```bash
# 推送到 GitHub
cd ~/00zyf/AI/claude-skills-collection
git push

# 其他人可以克隆
git clone https://github.com/yf8578/claude-skills-collection.git
```

---

## 🎓 总结

**claude-skills-collection 是你的私人 Skills 市场**

- ✅ 统一管理所有来源的 skills
- ✅ 一键安装到多个 AI 工具
- ✅ 完整的版本和依赖记录
- ✅ 便捷的管理脚本
- ✅ 可以分享和备份

**核心工作流：**

```bash
# 发现 skill
clawhub search xxx

# 添加到 collection
cp -r skill-source ~/00zyf/AI/claude-skills-collection/

# 注册并安装到所有平台
./scripts/register.sh skill-name
./scripts/install-universal.sh skill-name

# 开始使用！
```

---

现在开始建立你的 Skills 库吧！🚀
