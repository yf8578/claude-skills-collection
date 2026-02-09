# 🚀 如何使用 Skills Collection

**5 分钟快速上手指南**

---

## 📍 你现在的位置

```bash
cd ~/00zyf/AI/claude-skills-collection
pwd
# 输出：/Users/zhangyifan/00zyf/AI/claude-skills-collection
```

---

## 🎯 三种使用方式

### 方式 1️⃣：图形化界面（最简单）⭐

**启动 Skills Store**：

```bash
cd ~/00zyf/AI/claude-skills-collection
./scripts/store.sh
```

**你会看到**：
```
┌─────────────────────────────────────────┐
│ 🏪 Skills Store                         │
│ 📦 Total: 7 | ✅ Installed: 7          │
├─────────────────────────────────────────┤
│ [Installed] [Discover] [Help]           │
│                                         │
│ ✅ Citation Grabber  1.1.0             │
│ ✅ PDF Skill         1.0.0             │
│ ✅ Word Document     1.0.0             │
│ ...                                     │
└─────────────────────────────────────────┘
```

**基本操作**：
- `↑/↓` - 上下移动
- `Enter` - 查看详情
- `/` - 搜索
- `i` - 安装/重装
- `?` - 帮助
- `q` - 退出

**首次使用会自动安装依赖**（textual, requests, rich）。

---

### 方式 2️⃣：命令行（最快速）⚡

#### 查看已安装的 Skills

```bash
cd ~/00zyf/AI/claude-skills-collection
./scripts/list.sh
```

输出：
```
📚 Available Skills

  Citation Grabber (1.1.0)
    📁 citation-grabber
    📝 Fetch scientific paper citations...
    🏷️  research | Status: stable

  PDF Skill (1.0.0)
    📁 pdf
    📝 PDF manipulation...

Total skills: 7
```

#### 添加新 Skill

```bash
# 从 ClawHub（5,700+ skills）
./scripts/add-skill.sh clawhub:skill-name

# 从 GitHub
./scripts/add-skill.sh github:username/repo

# 从本地目录
./scripts/add-skill.sh /path/to/skill
```

**例如**，添加一个搜索 skill：
```bash
./scripts/add-skill.sh clawhub:search

# 自动完成：
# ✅ 下载到 collection
# ✅ 注册到 registry.json
# ✅ 安装到所有平台
# ✅ Git 提交
```

#### 查看 Skill 状态

```bash
./scripts/status.sh pdf

# 输出：
# Skill: pdf
# ✅ Installed in Claude Code
# ✅ Installed in Codex
# ✅ Installed in Gemini CLI
# ✅ Installed in Antigravity
```

---

### 方式 3️⃣：直接在 AI 工具中使用

**你的 skills 已经安装到**：
- ✅ Claude Code (`~/.claude/skills/`)
- ✅ Codex (`~/.codex/skills/`)
- ✅ Gemini CLI (`~/.gemini/tools/`)
- ✅ Antigravity (`~/.antigravity/extensions/`)

**在 Claude Code 中使用**：

重启 Claude Code 后，运行：
```bash
/skills
# 或
/skill-list
```

你应该看到 7 个 skills。

**使用 citation-grabber**：
```bash
cd ~/.claude/skills/citation-grabber
python3 citation.py "Attention Is All You Need"
```

**使用 pdf skill**：
在 Claude Code 中直接说：
> "帮我处理这个 PDF 文件"

Claude 会自动使用 pdf skill。

---

## 🎬 完整示例：添加一个新 Skill

### 场景：我想添加一个 JSON 格式化工具

```bash
# 1. 进入项目目录
cd ~/00zyf/AI/claude-skills-collection

# 2. 搜索可用的 skills（可选）
# 方法 A：用 clawhub CLI
clawhub search json

# 方法 B：用我们的 API 工具
python3 scripts/clawhub-api.py

# 3. 添加 skill（一键完成）
./scripts/add-skill.sh clawhub:json-formatter

# 输出：
# 🎯 Adding skill to collection...
# 📦 Downloading from ClawHub: json-formatter
# 📋 Copying to collection
# ✅ Skill added to collection!
# 📝 Registering in registry.json...
# 🚀 Installing to all platforms...
#    ✅ Claude Code
#    ✅ Codex
#    ✅ Gemini CLI
#    ✅ Antigravity
# 📦 Committing to git...
# ✨ Successfully added skill: json-formatter

# 4. 查看（可选）
./scripts/list.sh
# 现在有 8 个 skills 了

# 5. 在 Skills Store 中查看（可选）
./scripts/store.sh
# 按 r 刷新，看到新 skill

# 6. 推送到 GitHub（可选）
git push

# 完成！🎉
```

---

## 🔍 浏览 ClawHub Skills

### 方法 1：使用 API 工具

```bash
cd ~/00zyf/AI/claude-skills-collection
python3 scripts/clawhub-api.py

# 输出：
# 🧪 Testing ClawHub API Client
#
# 1️⃣ Listing all skills...
#    Found 24 skills (showing first 10):
#    - NanoBazaar (nanobazaar)
#    - Uniswap V4 (uniswap-v4)
#    ...
```

### 方法 2：直接访问网站

浏览器打开：https://clawhub.ai

---

## 📊 管理你的 Skills

### 查看所有 Skills

```bash
./scripts/list.sh
```

### 查看详细信息

```bash
# 命令行
./scripts/status.sh citation-grabber

# 或在 Skills Store 中
./scripts/store.sh
# 选中 skill，按 Enter
```

### 重新安装 Skill

```bash
# 命令行
./scripts/install-universal-link.sh pdf

# 或在 Skills Store 中
# 选中 skill，按 i
```

### 卸载 Skill

```bash
./scripts/uninstall.sh skill-name
```

### 更新 Skill

由于使用了软链接，更新超简单：

```bash
# 在 collection 中修改
cd ~/00zyf/AI/claude-skills-collection/pdf
nano SKILL.md

# 保存后，所有平台自动更新！✨
# (Claude Code 需要重启)
```

---

## 🎨 自定义和开发

### 创建新 Skill

```bash
cd ~/00zyf/AI/claude-skills-collection

# 1. 创建模板
./scripts/create-skill.sh my-awesome-skill --category development

# 2. 编辑
cd my-awesome-skill
nano SKILL.md     # 编写文档和元数据
nano main.py      # 编写代码
nano requirements.txt  # 添加依赖

# 3. 注册
cd ..
./scripts/register.sh my-awesome-skill

# 4. 安装到所有平台
./scripts/install-universal-link.sh my-awesome-skill

# 5. 测试
python3 my-awesome-skill/main.py

# 6. 提交
git add my-awesome-skill registry.json
git commit -m "feat: Add my-awesome-skill"
git push
```

---

## 💡 常用命令速查

```bash
# 进入项目目录
cd ~/00zyf/AI/claude-skills-collection

# 📱 启动图形界面
./scripts/store.sh

# 📦 添加 skill
./scripts/add-skill.sh clawhub:skill-name
./scripts/add-skill.sh github:user/repo
./scripts/add-skill.sh /path/to/skill

# 📋 查看
./scripts/list.sh                    # 列出所有
./scripts/status.sh skill-name       # 查看状态

# 🔧 管理
./scripts/install-universal-link.sh skill-name  # 重装
./scripts/uninstall.sh skill-name              # 卸载

# 🔍 浏览 ClawHub
python3 scripts/clawhub-api.py

# 📤 推送到 GitHub
git add . && git commit -m "Update" && git push
```

---

## 🆘 常见问题

### Q1: Skills Store 打不开？

**A**: 需要安装依赖：

```bash
pip3 install textual requests rich

# 或者运行启动脚本会自动安装
./scripts/store.sh
```

### Q2: Claude Code 看不到 skills？

**A**: 需要重启 Claude Code，然后运行：

```bash
/skills
```

### Q3: 添加 skill 失败？

**A**: 检查：
1. 网络连接正常
2. skill 名称正确
3. 查看详细错误信息

```bash
./scripts/add-skill.sh clawhub:skill-name 2>&1 | tee error.log
```

### Q4: 如何更新 collection 中的 skill？

**A**: 直接编辑源文件：

```bash
cd ~/00zyf/AI/claude-skills-collection/skill-name
# 修改文件
git add . && git commit -m "Update skill" && git push
```

由于使用软链接，其他平台自动更新（Claude Code 需重启）。

---

## 📚 完整文档

需要更多信息？查看这些文档：

1. **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - 完整项目总结
2. **[USAGE_GUIDE.md](./USAGE_GUIDE.md)** - 详细使用指南
3. **[QUICK_DEMO.md](./QUICK_DEMO.md)** - 快速演示
4. **[docs/skills-store.md](./docs/skills-store.md)** - Skills Store 完整指南
5. **[README.md](./README.md)** - 项目主文档

**在 Skills Store 中查看帮助**：
```bash
./scripts/store.sh
# 按 ? 查看帮助
# 或切换到 "Help" 标签
```

---

## 🎯 推荐工作流

### 日常使用

```bash
# 早上打开项目
cd ~/00zyf/AI/claude-skills-collection

# 启动 Skills Store 浏览
./scripts/store.sh

# 或快速查看列表
./scripts/list.sh
```

### 添加新 Skills

```bash
# 1. 浏览 ClawHub
clawhub search <keyword>
# 或
python3 scripts/clawhub-api.py

# 2. 添加想要的
./scripts/add-skill.sh clawhub:skill-name

# 3. 查看
./scripts/store.sh  # 按 r 刷新

# 4. 推送
git push
```

### 维护更新

```bash
# 每周/每月
cd ~/00zyf/AI/claude-skills-collection

# 查看所有 skills
./scripts/list.sh

# 更新需要的 skills（手动检查源仓库）
cd skill-name
# 更新文件

# 提交
cd ..
git add -A
git commit -m "Update skills"
git push
```

---

## 🌟 核心优势

使用 Skills Collection 的好处：

✅ **集中管理** - 所有 skills 在一个地方
✅ **跨平台** - 一次添加，4 个平台可用
✅ **节省空间** - 软链接节省 60-80%
✅ **自动同步** - 修改一处，处处生效
✅ **版本控制** - Git 完整历史
✅ **易于分享** - GitHub 公开仓库
✅ **双重界面** - CLI + TUI，各取所需

---

## 🚀 立即开始

```bash
# 1. 启动 Skills Store 体验
cd ~/00zyf/AI/claude-skills-collection
./scripts/store.sh

# 2. 添加一个新 skill 试试
./scripts/add-skill.sh clawhub:search

# 3. 查看所有 skills
./scripts/list.sh

# 完成！现在你已经会用了 🎉
```

---

**享受强大的 AI Skills 管理体验！** 🎊

有问题？查看完整文档或在 Skills Store 中按 `?` 查看帮助。
