# 跨平台 Skills 配置指南

本指南说明如何在多个 AI CLI 工具中配置和使用相同的 skills。

## 🌍 支持的平台

| 平台 | SKILL.md 支持 | 自动安装 | 配置路径 |
|------|--------------|---------|----------|
| **Claude Code** | ✅ 完全支持 | ✅ 是 | `~/.claude/skills/` |
| **OpenClaw/ClawHub** | ✅ 完全支持 | ✅ 是 | 通过 clawhub 管理 |
| **Codex** | ⚠️ 部分支持 | ❌ 手动 | `~/.codex/skills/` |
| **Gemini CLI** | ⚠️ 实验性 | ❌ 手动 | 自定义路径 |
| **Google Antigravity** | ❓ 未知 | ❓ 未知 | 需调查 |

## 📋 通用性说明

### ✅ 完全通用的部分

1. **SKILL.md 基础结构**
   ```yaml
   ---
   name: skill-name
   description: What it does
   usage: how to use it
   ---
   ```
   这个基础结构被所有主流工具识别。

2. **脚本和代码**
   - Python 脚本（`.py`）
   - Bash 脚本（`.sh`）
   - 其他可执行文件

   这些文件在所有平台上都能直接运行。

### ⚠️ 平台特定的部分

1. **元数据字段**
   - Claude Code: 使用 `claude:` 命名空间
   - OpenClaw: 使用 `openclaw:` 命名空间
   - Codex: 使用 `codex:` 命名空间

2. **安装机制**
   - 每个工具有自己的安装路径和方法
   - 依赖管理方式不同

## 🔧 平台配置详解

### 1. Claude Code

**特点：**
- 官方支持 SKILL.md 标准
- 自动加载 `~/.claude/skills/` 中的 skills
- 支持插件市场

**安装方法：**

```bash
# 方法 1: 使用本项目的安装脚本
./scripts/install.sh citation-grabber

# 方法 2: 手动复制
cp -r citation-grabber ~/.claude/skills/

# 方法 3: 通过插件市场
/plugin install citation-grabber@claude-skills-collection
```

**SKILL.md 示例：**
```yaml
---
name: my-skill
metadata:
  claude:
    priority: high        # 优先级
    auto_install: true    # 自动安装依赖
    category: research    # 分类
---
```

---

### 2. OpenClaw / ClawHub

**特点：**
- 拥有公共技能注册表（5,705+ skills）
- CLI 命令管理：`clawhub`
- 内置安全扫描（VirusTotal）

**安装方法：**

```bash
# 方法 1: 从 ClawHub 安装（如果已发布）
clawhub install citation-grabber

# 方法 2: 本地安装
clawhub sync --local ./citation-grabber

# 方法 3: 发布到 ClawHub
clawhub publish ./citation-grabber
```

**SKILL.md 示例：**
```yaml
---
name: my-skill
metadata:
  openclaw:
    emoji: "📚"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["python3"]
      python: ">=3.8"
    install:
      - id: pip-deps
        kind: pip
        packages: ["requests>=2.25.0"]
---
```

**管理命令：**
```bash
clawhub list              # 列出已安装的 skills
clawhub update --all      # 更新所有 skills
clawhub search citation   # 搜索 skills
```

---

### 3. Codex (OpenAI)

**特点：**
- 支持 SKILL.md，但解析可能有差异
- 主要通过代码注释和文档理解功能

**安装方法：**

```bash
# Codex 通常需要手动配置
mkdir -p ~/.codex/skills
cp -r citation-grabber ~/.codex/skills/

# 或者在项目中直接引用
export CODEX_SKILLS_PATH=/path/to/claude-skills-collection
```

**SKILL.md 示例：**
```yaml
---
name: my-skill
metadata:
  codex:
    enabled: true
    runtime: python      # 运行时环境
    context_files:       # 需要加载的上下文文件
      - README.md
      - examples.md
---
```

---

### 4. Gemini CLI

**特点：**
- 较新的工具，skills 支持处于实验阶段
- 可能需要自定义配置

**安装方法：**

```bash
# Gemini CLI 目前主要通过环境变量配置
export GEMINI_TOOLS_PATH=/path/to/claude-skills-collection

# 或在配置文件中指定
# ~/.gemini/config.yaml
tools:
  paths:
    - /path/to/claude-skills-collection
```

**SKILL.md 示例：**
```yaml
---
name: my-skill
metadata:
  gemini:
    compatible: true
    runtime: python
    trigger_keywords:    # 触发关键词
      - "cite"
      - "citation"
      - "paper"
---
```

---

### 5. Google Antigravity

**状态：** 需要进一步调查

如果你有使用经验，请分享配置方法！

---

## 🎯 推荐的跨平台 SKILL.md 模板

为了最大化兼容性，推荐使用以下模板：

```yaml
---
name: skill-name
description: Brief description (universal)
version: 1.0.0
usage: skill-name [options]

# 通用元数据
metadata:
  category: research
  tags: ["tag1", "tag2"]
  author: your-name
  repository: https://github.com/user/repo

  # Claude Code 特定
  claude:
    priority: high
    auto_install: true

  # OpenClaw 特定
  openclaw:
    emoji: "📚"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["python3"]
    install:
      - id: pip-deps
        kind: pip
        packages: ["requests>=2.25.0"]

  # Codex 特定
  codex:
    enabled: true
    runtime: python

  # Gemini 特定
  gemini:
    compatible: true
    runtime: python
---

# Skill Name

[Universal documentation that works for all platforms]
```

## 📦 统一安装脚本

创建一个通用的安装脚本，自动检测平台：

```bash
#!/bin/bash
# install-universal.sh

SKILL_NAME=$1

# 检测 Claude Code
if [ -d "$HOME/.claude" ]; then
    echo "Installing for Claude Code..."
    cp -r "$SKILL_NAME" "$HOME/.claude/skills/"
fi

# 检测 OpenClaw
if command -v clawhub &> /dev/null; then
    echo "Installing for OpenClaw..."
    clawhub sync --local "./$SKILL_NAME"
fi

# 检测 Codex
if [ -d "$HOME/.codex" ]; then
    echo "Installing for Codex..."
    cp -r "$SKILL_NAME" "$HOME/.codex/skills/"
fi

# 检测 Gemini CLI
if command -v gemini &> /dev/null; then
    echo "Installing for Gemini CLI..."
    # 添加到 Gemini 配置
    # 实现取决于 Gemini CLI 的具体配置方式
fi

# 安装 Python 依赖
if [ -f "$SKILL_NAME/requirements.txt" ]; then
    pip3 install -r "$SKILL_NAME/requirements.txt"
fi

echo "✅ Installation complete!"
```

## 🔍 兼容性检查清单

在发布 skill 之前，检查以下项目：

- [ ] SKILL.md 包含基础字段（name, description, usage）
- [ ] 包含多个平台的元数据配置
- [ ] Python/Bash 脚本有正确的 shebang
- [ ] 依赖清单完整（requirements.txt）
- [ ] 文档说明了跨平台用法
- [ ] 在至少两个平台上测试过

## 💡 最佳实践

### 1. 使用命名空间

```yaml
metadata:
  claude:    # Claude Code 特定配置
  openclaw:  # OpenClaw 特定配置
  codex:     # Codex 特定配置
```

这样不同工具只会读取自己的配置，不会冲突。

### 2. 提供降级方案

如果某个平台不支持自动安装：

```yaml
metadata:
  openclaw:
    install:
      - id: auto-pip
        kind: pip
        packages: ["requests"]
  # 降级方案：手动安装说明
  manual_install: |
    For platforms without auto-install:
    pip install requests
```

### 3. 保持核心功能独立

不要让 skill 依赖特定平台的特性。核心逻辑应该是：

```python
# ✅ 好：平台无关
def fetch_citation(doi):
    import requests
    return requests.get(f"https://doi.org/{doi}")

# ❌ 避免：平台特定
def fetch_citation_claude(doi):
    from claude_helpers import fetch_url  # 仅 Claude 有
    return fetch_url(f"https://doi.org/{doi}")
```

## 🆘 故障排除

### Skill 在某个平台无法加载

1. 检查 SKILL.md 格式是否正确
2. 确认平台是否支持 SKILL.md
3. 查看平台的日志文件

### 依赖安装失败

```bash
# 手动安装依赖
pip3 install -r skill-name/requirements.txt

# 或使用虚拟环境
python3 -m venv skill-env
source skill-env/bin/activate
pip install -r requirements.txt
```

### 找不到 skill

不同平台的 skill 路径：
- Claude Code: `~/.claude/skills/`
- OpenClaw: `clawhub list` 查看
- Codex: `~/.codex/skills/` 或环境变量指定
- Gemini: 查看 `~/.gemini/config.yaml`

## 📚 参考资源

- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
- [ClawHub Registry](https://clawhub.ai/)
- [SKILL.md Standard](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)

## 🤝 贡献

如果你在其他平台成功配置了 skills，请分享你的经验！

---

最后更新：2026-02-09
