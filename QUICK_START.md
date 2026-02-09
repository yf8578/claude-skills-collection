# ⚡ 5 分钟快速上手

## 📍 你现在在这里

```
/Users/zhangyifan/00zyf/AI/claude-skills-collection/
```

这是你的 **Skills 管理中心**！

---

## 🎯 这个项目有什么用？

想象一下：

### ❌ 没有 Collection 之前

```bash
# 你从 ClawHub 下载了一个 skill
clawhub install pdf-tool

# 只在 OpenClaw 可用，其他工具要重新安装：
cp xxx ~/.claude/skills/      # 给 Claude Code 装一次
cp xxx ~/.codex/skills/        # 给 Codex 装一次
cp xxx ~/.gemini/tools/        # 给 Gemini 装一次
# ... 太麻烦了！
```

### ✅ 有 Collection 之后

```bash
# 下载任何 skill，放到这里
cp -r downloaded-skill ~/00zyf/AI/claude-skills-collection/

# 一条命令，安装到所有 AI 工具
./scripts/install-universal.sh downloaded-skill

# ✓ Claude Code  ✓ Codex  ✓ Gemini CLI  ✓ Antigravity  ✓ OpenClaw
# 全部搞定！
```

---

## 🚀 马上试试

### 1. 查看现有 skills

```bash
cd ~/00zyf/AI/claude-skills-collection
./scripts/list.sh
```

### 2. 安装 citation-grabber 到所有平台

```bash
./scripts/install-universal.sh citation-grabber

# 会自动检测你的：
# - Claude Code？安装！
# - Gemini CLI？安装！
# - Codex？安装！
# - Antigravity？安装！
```

### 3. 测试一下

```bash
# 直接运行（不需要安装到任何工具）
cd citation-grabber
python3 citation.py "Attention Is All You Need"

# 或者在 Claude Code 中使用：
# （会自动加载，因为已经安装了）
```

---

## 📥 添加新的 Skills（3 种方法）

### 方法 1：从 ClawHub 下载（推荐）

```bash
# 1. 搜索
clawhub search pdf

# 2. 安装到临时位置
clawhub install pdf-analyzer

# 3. 复制到 collection
cp -r ~/.openclaw/skills/pdf-analyzer ~/00zyf/AI/claude-skills-collection/

# 4. 一键安装到所有平台
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh pdf-analyzer
./scripts/install-universal.sh pdf-analyzer

# ✅ 完成！现在所有 AI 工具都能用了
```

### 方法 2：从 GitHub 克隆

```bash
# 找到一个好的 skill，比如从 awesome-claude-skills

# 1. 克隆
cd /tmp
git clone https://github.com/someone/cool-skill.git

# 2. 移动到 collection
mv cool-skill ~/00zyf/AI/claude-skills-collection/

# 3. 注册并安装到所有平台
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh cool-skill
./scripts/install-universal.sh cool-skill
```

### 方法 3：自己创建

```bash
cd ~/00zyf/AI/claude-skills-collection

# 使用模板创建
./scripts/create-skill.sh my-tool productivity

# 实现功能
cd my-tool
# 编写代码...

# 注册并安装
cd ..
./scripts/register.sh my-tool
./scripts/install-universal.sh my-tool
```

---

## 📊 常用命令

```bash
cd ~/00zyf/AI/claude-skills-collection

# 列出所有 skills
./scripts/list.sh

# 安装单个 skill 到所有平台
./scripts/install-universal.sh <skill-name>

# 检查安装状态
./scripts/status.sh <skill-name>

# 创建新 skill
./scripts/create-skill.sh <name> <category>

# 注册 skill
./scripts/register.sh <skill-name>

# 卸载 skill
./scripts/uninstall.sh <skill-name>
```

---

## 🌍 跨平台支持

你的系统上有多个 AI 工具？没问题！

```bash
./scripts/install-universal.sh skill-name
```

这个命令会自动：
- ✅ 检测 Claude Code → 安装到 `~/.claude/skills/`
- ✅ 检测 Gemini CLI → 安装到 `~/.gemini/tools/`
- ✅ 检测 Codex → 安装到 `~/.codex/skills/`
- ✅ 检测 Antigravity → 安装到 `~/.antigravity/extensions/`
- ✅ 检测 OpenClaw → 通过 `clawhub sync`

**一次安装，处处可用！**

---

## 💡 实际案例

### 场景：我想要一个 PDF 处理工具

```bash
# 1. 搜索 ClawHub
clawhub search pdf

# 2. 找到 pdf-analyzer，下载
clawhub install pdf-analyzer

# 3. 添加到 collection
cp -r ~/.openclaw/skills/pdf-analyzer ~/00zyf/AI/claude-skills-collection/

# 4. 一键安装到所有工具
cd ~/00zyf/AI/claude-skills-collection
./scripts/register.sh pdf-analyzer
./scripts/install-universal.sh pdf-analyzer

# 5. 测试
cd pdf-analyzer
python3 main.py test.pdf

# 6. 现在可以在任何 AI 工具中使用了！
```

---

## 📖 下一步

1. **推送到 GitHub**（备份）
   - 见 `SETUP.md`

2. **浏览更多 skills**
   - [ClawHub](https://clawhub.ai/) - 5,705+ skills
   - [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)

3. **深入学习**
   - 📘 [快速开始指南](docs/getting-started.md)
   - 🌍 [跨平台配置](docs/cross-platform-guide.md)
   - 📥 [添加外部 Skills](docs/add-external-skills.md)

---

## ❓ 最常见问题

**Q: 这个和直接用 clawhub install 有什么区别？**
A: `clawhub` 只能装到 OpenClaw，这个能一次装到**所有**工具！

**Q: 我能添加从任何地方下载的 skills 吗？**
A: **可以！** 从 GitHub、ClawHub、Anthropic、社区等任何来源。

**Q: Skills 之间会冲突吗？**
A: 不会。每个 skill 是独立的目录。

**Q: 我能分享我的 collection 吗？**
A: 可以！推送到 GitHub，其他人就能克隆使用。

---

## ✅ 总结

**claude-skills-collection 让你：**

1. ✅ 统一管理所有 skills（无论来源）
2. ✅ 一键安装到多个 AI 工具
3. ✅ 方便添加、删除、更新
4. ✅ 完整记录（registry.json）
5. ✅ 可以备份和分享

**核心流程：**

```
下载 skill → 放到 collection → 一键安装到所有工具 → 开始使用
```

---

开始建立你的 Skills 库吧！🚀

有问题？查看文档或提 issue。
