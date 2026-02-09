# 设置指南

你的 Claude Skills Collection 已经准备就绪！现在需要将它推送到 GitHub。

## 📦 当前状态

✅ 所有文件已创建完成
✅ Git 仓库已初始化
✅ 已创建初始 commit
⏳ 需要创建 GitHub 仓库并推送

## 🚀 推送到 GitHub

### 第一步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`claude-skills-collection`
3. 描述：`Personal monorepo of Claude AI skills with cross-platform support`
4. 选择 **Public**（公开）
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 第二步：推送代码

在终端运行：

```bash
cd ~/claude-skills-collection

# 已经配置好了 remote，直接推送
git push -u origin main
```

### 第三步：验证

访问你的仓库页面：https://github.com/yf8578/claude-skills-collection

你应该能看到：
- ✅ 17 个文件
- ✅ 完整的 README
- ✅ Scripts 和文档目录

## 🎯 现在如何使用？

### 选项 A：安装到 Claude Code

```bash
cd ~/claude-skills-collection
./scripts/install.sh citation-grabber
```

### 选项 B：跨平台安装（推荐）

```bash
cd ~/claude-skills-collection
./scripts/install-universal.sh citation-grabber
```

这个脚本会自动检测你的系统上有哪些 AI CLI 工具：
- ✅ Claude Code
- ✅ OpenClaw/ClawHub
- ✅ Codex
- ✅ Gemini CLI
- ✅ Google Antigravity

然后将 skill 安装到所有检测到的工具中！

### 选项 C：直接运行（不安装）

```bash
cd ~/claude-skills-collection/citation-grabber
pip3 install -r requirements.txt

# 获取论文引用
python3 citation.py "Attention Is All You Need"
```

## 📚 下载新的 Skills

### 方法 1：添加到这个 Collection

```bash
# 创建新 skill
cd ~/claude-skills-collection
./scripts/create-skill.sh my-new-skill research

# 编辑 skill
cd my-new-skill
# 实现你的功能...

# 注册
./scripts/register.sh my-new-skill

# 安装到所有平台
./scripts/install-universal.sh my-new-skill
```

### 方法 2：从其他来源下载

#### 从 ClawHub 下载（OpenClaw）

```bash
# 搜索 skills
clawhub search pdf

# 安装
clawhub install pdf-analyzer

# 查看已安装
clawhub list
```

#### 从 Anthropic Skills Repository

```bash
# 克隆官方 skills 仓库
git clone https://github.com/anthropics/skills.git
cd skills

# 复制想要的 skill 到你的 collection
cp -r some-skill ~/claude-skills-collection/

# 注册并安装
cd ~/claude-skills-collection
./scripts/register.sh some-skill
./scripts/install-universal.sh some-skill
```

#### 从社区获取

浏览这些资源：
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [ClawHub Registry](https://clawhub.ai/) - 5,705+ skills
- [Skills Marketplace](https://skillsmp.com/)

```bash
# 下载社区 skill
git clone https://github.com/someone/cool-skill.git
cd cool-skill

# 复制到你的 collection
cp -r . ~/claude-skills-collection/cool-skill/

# 注册并安装
cd ~/claude-skills-collection
./scripts/register.sh cool-skill
./scripts/install-universal.sh cool-skill
```

## 🔍 检查安装状态

```bash
# 列出所有 skills
./scripts/list.sh

# 检查特定 skill 的安装状态
./scripts/status.sh citation-grabber
```

## 🌍 跨平台使用

你提到你有多个工具：
- Claude Code
- Gemini CLI
- Google Antigravity
- Codex

好消息！`install-universal.sh` 会自动检测并为所有工具安装 skills。

查看详细的跨平台配置指南：
```bash
cat docs/cross-platform-guide.md
```

## 💡 常用操作

```bash
# 列出所有 skills
./scripts/list.sh

# 安装单个 skill
./scripts/install.sh citation-grabber

# 跨平台安装
./scripts/install-universal.sh citation-grabber

# 卸载 skill
./scripts/uninstall.sh citation-grabber

# 检查状态
./scripts/status.sh citation-grabber

# 创建新 skill
./scripts/create-skill.sh my-skill research
```

## 🎓 学习资源

- [快速开始](./docs/getting-started.md)
- [跨平台配置](./docs/cross-platform-guide.md)
- [主 README](./README.md)

## ❓ 常见问题

### Q: Skills 在不同工具间通用吗？

A: **基本通用**！
- ✅ SKILL.md 格式是通用标准
- ✅ Python/Bash 脚本可以在所有平台运行
- ⚠️ 某些元数据字段是平台特定的
- ⚠️ 安装路径和方法不同

查看 `docs/cross-platform-guide.md` 了解详情。

### Q: 如何更新 skills？

目前需要手动更新。未来会添加 `update.sh` 脚本。

### Q: 可以发布我的 skills 吗？

可以！
1. 确保代码质量
2. 添加完整文档
3. 发布到 GitHub
4. 提交到 ClawHub（如果用 OpenClaw）
5. 提交 PR 到 awesome-claude-skills

### Q: 我的平台不在列表中怎么办？

1. 检查平台是否支持 SKILL.md 标准
2. 手动复制 skill 文件到平台的 skills 目录
3. 参考平台文档进行配置
4. 欢迎分享你的经验！更新 `docs/cross-platform-guide.md`

## 🎉 完成！

你现在有了：
- ✅ 专业的 skills collection 仓库
- ✅ 完整的管理工具
- ✅ 跨平台支持
- ✅ 详细文档
- ✅ 一个可用的 skill（citation-grabber）

开始创建你的 skills 吧！🚀

---

需要帮助？查看文档或在 GitHub 上提 issue。
