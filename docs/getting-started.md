# 快速开始指南

本指南帮助你快速上手 Claude Skills Collection。

## 📥 第一步：获取仓库

```bash
git clone https://github.com/yf8578/claude-skills-collection.git
cd claude-skills-collection
```

## 🎯 第二步：选择你的使用方式

### 方式 A: 我使用 Claude Code

```bash
# 安装单个 skill
./scripts/install.sh citation-grabber

# 或安装所有 skills
./scripts/install-all.sh

# 重启 Claude Code 即可使用
```

安装后，Claude 会自动加载这些 skills。

### 方式 B: 我使用 OpenClaw

```bash
# 如果 skill 已发布到 ClawHub
clawhub install citation-grabber

# 或本地安装
clawhub sync --local ./citation-grabber
```

### 方式 C: 我使用多个工具

查看 [跨平台配置指南](./cross-platform-guide.md) 了解如何在多个 AI CLI 工具中使用相同的 skills。

### 方式 D: 我只想直接运行脚本

```bash
# 每个 skill 都可以独立运行
cd citation-grabber
pip install -r requirements.txt
python3 citation.py "Attention Is All You Need"
```

## 🔍 第三步：查看可用的 Skills

```bash
# 列出所有 skills
./scripts/list.sh

# 查看某个 skill 的状态
./scripts/status.sh citation-grabber
```

## 🎨 第四步：创建你自己的 Skill

```bash
# 使用模板创建新 skill
./scripts/create-skill.sh my-awesome-skill research

# 编辑 skill 文件
cd my-awesome-skill
nano SKILL.md
nano main.py

# 注册到 registry
./scripts/register.sh my-awesome-skill

# 测试
python3 main.py --help
```

## 📚 常用命令速查

| 命令 | 用途 |
|------|------|
| `./scripts/list.sh` | 列出所有 skills |
| `./scripts/install.sh <name>` | 安装指定 skill |
| `./scripts/status.sh <name>` | 检查 skill 状态 |
| `./scripts/create-skill.sh <name>` | 创建新 skill |
| `./scripts/uninstall.sh <name>` | 卸载 skill |

## 💡 示例：使用 Citation Grabber

```bash
# 安装
./scripts/install.sh citation-grabber

# 使用 - 搜索论文
python3 citation-grabber/citation.py "Attention Is All You Need"

# 批量处理
echo "Deep Learning" > papers.txt
echo "BERT" >> papers.txt
python3 citation-grabber/citation.py papers.txt -o refs.bib
```

## 🆘 遇到问题？

1. **Skill 无法加载**
   - 检查是否正确安装：`./scripts/status.sh <skill-name>`
   - 查看错误日志
   - 尝试重新安装

2. **依赖问题**
   - 手动安装：`pip install -r <skill>/requirements.txt`
   - 使用虚拟环境隔离依赖

3. **跨平台问题**
   - 参考 [跨平台配置指南](./cross-platform-guide.md)

## 📖 下一步

- 阅读 [创建 Skills 指南](./creating-skills.md)
- 查看 [跨平台兼容性](./cross-platform-guide.md)
- 浏览现有 skills 学习最佳实践

---

祝使用愉快！🚀
