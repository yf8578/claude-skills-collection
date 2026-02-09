# Skills Collection 使用指南

## 📚 目录

1. [管理功能](#管理功能)
2. [添加新 Skills](#添加新-skills)
3. [日常使用](#日常使用)
4. [完整工作流](#完整工作流)

---

## 管理功能

你的 Skills Collection 提供以下管理工具：

### 📦 Skills 管理

| 脚本 | 功能 | 用法 |
|------|------|------|
| **add-skill.sh** ⭐ | 添加新 skill（自动化） | `./scripts/add-skill.sh clawhub:pdf-analyzer` |
| **list.sh** | 查看所有 skills | `./scripts/list.sh` |
| **status.sh** | 检查 skill 安装状态 | `./scripts/status.sh pdf` |
| **register.sh** | 注册 skill 到 registry.json | `./scripts/register.sh skill-name` |
| **create-skill.sh** | 从模板创建新 skill | `./scripts/create-skill.sh my-skill` |

### 🚀 安装/卸载

| 脚本 | 功能 | 用法 |
|------|------|------|
| **install-universal-link.sh** ⭐ | 安装到所有平台（软链接） | `./scripts/install-universal-link.sh pdf` |
| **install-universal.sh** | 安装到所有平台（复制） | `./scripts/install-universal.sh pdf` |
| **install-all-link.sh** | 批量安装所有 skills（软链接） | `./scripts/install-all-link.sh` |
| **install-all.sh** | 批量安装所有 skills（复制） | `./scripts/install-all.sh` |
| **install.sh** | 仅安装到 Claude Code | `./scripts/install.sh pdf` |
| **uninstall.sh** | 卸载 skill | `./scripts/uninstall.sh pdf` |

---

## 添加新 Skills

### 🎯 核心概念

**你的 Collection 是单一数据源**

```
❌ 错误流程（绕过 collection）：
clawhub install pdf-analyzer
   ↓
~/.openclaw/skills/pdf-analyzer  ← 只在这里，collection 没用了

✅ 正确流程（通过 collection 管理）：
clawhub install pdf-analyzer
   ↓
~/00zyf/AI/claude-skills-collection/pdf-analyzer  ← Collection（单一数据源）
   ↓
自动安装到所有平台
```

---

### ⭐ 方法 1: 自动化脚本（推荐）

使用 `add-skill.sh` **一键添加**新 skills：

#### 从 ClawHub 添加

```bash
cd ~/00zyf/AI/claude-skills-collection

# 添加 skill（自动下载、注册、安装、提交）
./scripts/add-skill.sh clawhub:pdf-analyzer

# 完成！skill 已添加到 collection 并安装到所有平台
```

#### 从 GitHub 添加

```bash
./scripts/add-skill.sh github:username/skill-name

# 例如：
./scripts/add-skill.sh github:travisvn/some-awesome-skill
```

#### 从本地目录添加

```bash
./scripts/add-skill.sh local:/path/to/skill

# 或直接用路径（自动检测）
./scripts/add-skill.sh /tmp/my-skill
./scripts/add-skill.sh ~/Downloads/cool-skill
```

#### 可选参数

```bash
# 使用复制而非软链接
./scripts/add-skill.sh clawhub:pdf-analyzer --copy

# 只添加到 collection，不安装
./scripts/add-skill.sh github:user/skill --no-install

# 不自动 git commit
./scripts/add-skill.sh clawhub:skill --no-commit
```

---

### 方法 2: 手动添加（了解细节）

如果你想了解背后的步骤：

```bash
# 1. 下载 skill 到临时位置
clawhub install pdf-analyzer
# 或
git clone https://github.com/user/skill.git /tmp/skill

# 2. 复制到 collection
cp -r ~/.openclaw/skills/pdf-analyzer ~/00zyf/AI/claude-skills-collection/

# 3. 注册到 registry
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh pdf-analyzer

# 4. 安装到所有平台（软链接）
./scripts/install-universal-link.sh pdf-analyzer

# 5. Git 提交
git add pdf-analyzer registry.json
git commit -m "feat: Add pdf-analyzer skill"
git push
```

**建议**：直接用 `add-skill.sh`，它自动完成所有步骤！

---

## 日常使用

### 查看已安装的 Skills

```bash
cd ~/00zyf/AI/claude-skills-collection

# 列出所有 skills
./scripts/list.sh

# 检查某个 skill 的安装状态
./scripts/status.sh pdf
```

### 更新 Skill

因为使用了软链接，更新超简单：

```bash
# 在 collection 中修改
cd ~/00zyf/AI/claude-skills-collection/pdf
nano SKILL.md
# 或修改任何文件

# 保存后，所有平台自动更新！✨
# Codex、Gemini CLI、Antigravity 立即看到变化
# Claude Code 需要重启
```

### 从 Collection 重新安装

```bash
# 如果某个平台的 skill 损坏了，重新安装：
./scripts/install-universal-link.sh pdf

# 或者重新安装所有 skills：
./scripts/install-all-link.sh
```

### 删除 Skill

```bash
# 从所有平台卸载
./scripts/uninstall.sh pdf-analyzer

# 从 collection 删除
rm -rf pdf-analyzer

# 更新 registry.json（手动编辑删除条目）
nano registry.json

# 提交
git add -A
git commit -m "Remove pdf-analyzer skill"
```

---

## 完整工作流

### 场景 1: 发现并添加新 Skill

```bash
# 1. 搜索 ClawHub（5,700+ skills）
clawhub search markdown

# 输出：
# markdown-to-pdf    - Convert Markdown to PDF
# markdown-linter    - Lint markdown files
# ...

# 2. 添加你想要的 skill
cd ~/00zyf/AI/claude-skills-collection
./scripts/add-skill.sh clawhub:markdown-to-pdf

# 3. 自动完成：
#    ✅ 下载到 collection
#    ✅ 注册到 registry.json
#    ✅ 安装到所有平台（软链接）
#    ✅ Git 提交

# 4. 推送到 GitHub
git push

# 完成！现在在 Claude Code、Codex、Gemini CLI、Antigravity 都可以用了
```

### 场景 2: 从 GitHub 添加开源 Skill

```bash
# 1. 在 GitHub 上找到一个 skill
# 例如：https://github.com/awesome-user/sql-formatter

# 2. 一行命令添加
cd ~/00zyf/AI/claude-skills-collection
./scripts/add-skill.sh github:awesome-user/sql-formatter

# 3. 推送
git push

# 完成！
```

### 场景 3: 自己开发 Skill

```bash
cd ~/00zyf/AI/claude-skills-collection

# 1. 创建新 skill
./scripts/create-skill.sh my-awesome-skill --category development

# 2. 编辑实现
cd my-awesome-skill
nano SKILL.md          # 编写文档
nano main.py           # 编写代码
nano requirements.txt  # 添加依赖

# 3. 测试
python main.py

# 4. 注册并安装
cd ..
./scripts/register.sh my-awesome-skill
./scripts/install-universal-link.sh my-awesome-skill

# 5. 提交
git add my-awesome-skill registry.json
git commit -m "feat: Add my-awesome-skill"
git push

# 6. 分享给其他人！
# 他们可以：
# git clone https://github.com/yf8578/claude-skills-collection.git
# cd claude-skills-collection
# ./scripts/install-all-link.sh
```

---

## 🎯 关键优势

### 为什么要通过 Collection 管理？

#### ❌ 不使用 Collection（传统方式）

```bash
# 分散在各处，难以管理
~/.claude/skills/skill1/
~/.codex/skills/skill2/
~/.gemini/tools/skill3/
~/Downloads/skill4/

# 问题：
- 不知道哪些 skills 来自哪里
- 更新一个 skill 要复制到 N 个地方
- 没有版本控制
- 无法分享给别人
- 重装系统后全丢了
```

#### ✅ 使用 Collection（推荐方式）

```bash
# 单一数据源
~/00zyf/AI/claude-skills-collection/
  ├── skill1/
  ├── skill2/
  ├── skill3/
  └── skill4/

# 其他平台都是软链接
~/.claude/skills/skill1 → collection/skill1
~/.codex/skills/skill1 → collection/skill1
~/.gemini/tools/skill1 → collection/skill1

# 优势：
✅ 所有 skills 集中管理
✅ 修改一处，处处生效
✅ Git 版本控制
✅ 可以推送到 GitHub
✅ 其他人可以 clone 你的 collection
✅ 重装系统只需 git clone + install-all-link.sh
```

---

## 📊 实际示例

### 示例：添加 3 个新 Skills

```bash
cd ~/00zyf/AI/claude-skills-collection

# 1. 从 ClawHub 添加
./scripts/add-skill.sh clawhub:json-formatter
# ✅ Added json-formatter (downloaded, registered, installed, committed)

# 2. 从 GitHub 添加
./scripts/add-skill.sh github:travisvn/code-reviewer
# ✅ Added code-reviewer (cloned, registered, installed, committed)

# 3. 从本地添加（你自己开发的）
./scripts/add-skill.sh ~/Projects/my-custom-skill
# ✅ Added my-custom-skill (copied, registered, installed, committed)

# 4. 查看所有 skills
./scripts/list.sh
# 输出：
# 📚 Available Skills
#   1. citation-grabber (1.1.0)
#   2. pdf (1.0.0)
#   ...
#   8. json-formatter (1.0.0)  ← 新增
#   9. code-reviewer (1.0.0)   ← 新增
#  10. my-custom-skill (1.0.0) ← 新增
#
# Total: 10 skills

# 5. 推送到 GitHub
git push

# 完成！现在你有 10 个 skills，全部：
# - 在 collection 中（单一数据源）
# - 安装到 4 个平台
# - 版本控制
# - 备份到 GitHub
```

---

## 🎓 最佳实践

### ✅ 推荐做法

1. **总是通过 collection 添加 skills**
   ```bash
   # 好 ✅
   ./scripts/add-skill.sh clawhub:skill-name

   # 不好 ❌
   clawhub install skill-name  # 直接安装，绕过了 collection
   ```

2. **使用软链接（默认）**
   - 节省 60-80% 磁盘空间
   - 自动同步更新
   - 除非遇到兼容性问题

3. **定期推送到 GitHub**
   ```bash
   cd ~/00zyf/AI/claude-skills-collection
   git add .
   git commit -m "Update skills"
   git push
   ```

4. **给 skills 分类**
   - 编辑 registry.json 设置正确的 category
   - 便于查找和管理

### 🔄 定期维护

```bash
# 每周/每月做一次
cd ~/00zyf/AI/claude-skills-collection

# 1. 检查所有 skills
./scripts/list.sh

# 2. 更新过时的 skills（手动检查源仓库）
cd skill-name
git pull  # 如果是 git 管理的
# 或重新下载

# 3. 提交变更
git add -A
git commit -m "Update skills"
git push
```

---

## 💡 常见问题

### Q: 如果我直接用 `clawhub install` 会怎样？

A: Skill 会被安装到 `~/.openclaw/skills/`，但**不在你的 collection 中**，失去了：
- 版本控制
- 跨平台同步
- 单一数据源管理

**解决方法**：用 `./scripts/add-skill.sh clawhub:skill-name` 代替。

### Q: Collection 会被删除吗？

A: 不会！它是你的技能管理中心，会一直保留。你添加的每个 skill 都进入这里。

### Q: 软链接和复制有什么区别？

A:
- **软链接**：省空间，自动同步，推荐
- **复制**：完全独立，占用更多空间，用于兼容性问题

详见：[docs/symlink-vs-copy.md](./docs/symlink-vs-copy.md)

### Q: 如何分享我的 Skills Collection？

A:
```bash
# 1. 推送到 GitHub
git push

# 2. 告诉别人 clone
git clone https://github.com/yf8578/claude-skills-collection.git
cd claude-skills-collection
./scripts/install-all-link.sh

# 完成！他们得到了你的所有 skills
```

---

## 🚀 快速命令参考

```bash
# 切换到 collection 目录
cd ~/00zyf/AI/claude-skills-collection

# 添加新 skill
./scripts/add-skill.sh clawhub:skill-name      # 从 ClawHub
./scripts/add-skill.sh github:user/repo        # 从 GitHub
./scripts/add-skill.sh /path/to/skill          # 从本地

# 查看和管理
./scripts/list.sh                              # 列出所有 skills
./scripts/status.sh skill-name                 # 检查状态
./scripts/create-skill.sh new-skill            # 创建新 skill

# 安装
./scripts/install-universal-link.sh skill-name # 安装单个（软链接）
./scripts/install-all-link.sh                  # 安装所有（软链接）

# Git 操作
git add . && git commit -m "Update" && git push

# 更新 skill（软链接模式）
cd skill-name && nano file.py  # 修改后自动同步
```

---

**你的 Skills Collection 现在是一个强大的管理工具！** 🎉

所有新 skills 都会进入 collection，统一管理，版本控制，跨平台同步。
