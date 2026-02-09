# 🎬 Skills Store 快速演示

## 体验新功能！

你现在有两种方式管理 skills：

### 方式 1️⃣：图形化界面（新！）🏪

```bash
cd ~/00zyf/AI/claude-skills-collection
./scripts/store.sh
```

**体验**：
- 📱 类似应用商店的界面
- 🔍 实时搜索
- 📊 详细信息展示
- ⌨️ 快捷键操作

### 方式 2️⃣：命令行（快速）⚡

```bash
cd ~/00zyf/AI/claude-skills-collection

# 快速添加 skill
./scripts/add-skill.sh clawhub:skill-name

# 查看所有 skills
./scripts/list.sh
```

---

## 🎯 两种方式配合使用

### 典型工作流：

```bash
# 1. 发现新 skill（命令行）
clawhub search markdown

# 2. 快速添加（命令行）
./scripts/add-skill.sh clawhub:markdown-to-pdf

# 3. 浏览管理（图形界面）
./scripts/store.sh
# - 按 r 刷新查看新 skill
# - 按 Enter 查看详细信息
# - 按 / 搜索其他 skills
```

---

## 📸 界面预览

启动后你会看到：

```
┌─────────────────────────────────────────────────┐
│ 🏪 Skills Store - Browse & Install Skills      │
│ 📦 Total: 7 | ✅ Installed: 7                   │
├─────────────────────────────────────────────────┤
│ ┌─ Installed ─┬─ Discover ─┬─ Help ─┐          │
│ │ Search: [___________________]       │          │
│ │                                     │          │
│ │ ✅ Citation Grabber    1.1.0        │          │
│ │ ✅ PDF Skill           1.0.0        │          │
│ │ ✅ Word Document       1.0.0        │          │
│ │ ...                                 │          │
│ └─────────────────────────────────────┘          │
│ Press ? for help                                │
└─────────────────────────────────────────────────┘
```

---

## ⌨️ 常用快捷键

| 按键 | 功能 |
|------|------|
| `↑/↓` | 上下导航 |
| `Enter` | 查看详情 |
| `/` | 搜索 |
| `i` | 安装 |
| `r` | 刷新 |
| `?` | 帮助 |
| `q` | 退出 |

---

## 🚀 立即尝试

### 步骤 1: 安装依赖（仅首次）

```bash
pip3 install textual requests rich
```

或者直接运行，会自动安装：

```bash
./scripts/store.sh
```

### 步骤 2: 启动 Skills Store

```bash
cd ~/00zyf/AI/claude-skills-collection
./scripts/store.sh
```

### 步骤 3: 探索功能

1. 查看已安装的 7 个 skills
2. 按 `/` 尝试搜索 "pdf"
3. 选中一个 skill，按 `Enter` 查看详情
4. 按 `Tab` 切换到 "Help" 查看完整文档
5. 按 `q` 退出

---

## 💡 功能对比

| 功能 | 命令行 | Skills Store |
|------|--------|--------------|
| **浏览 skills** | `./scripts/list.sh` | ✨ 交互式表格 |
| **搜索** | `grep` 输出 | ✨ 实时过滤 |
| **查看详情** | 读文件 | ✨ 弹窗展示 |
| **安装** | `./scripts/add-skill.sh` | ✨ 一键安装 + 进度 |
| **速度** | ⚡ 极快 | 📱 直观 |
| **适合场景** | 自动化、脚本 | 浏览、探索 |

**结论**: 两者互补，按需选择！

---

## 🎓 学习更多

- **完整文档**: [docs/skills-store.md](./docs/skills-store.md)
- **使用指南**: [USAGE_GUIDE.md](./USAGE_GUIDE.md)
- **主文档**: [README.md](./README.md)

---

## 🔮 即将推出

v2.0 将直接集成 ClawHub API，让你可以在 Skills Store 内：
- 浏览 5,700+ skills
- 查看评分和下载量
- 点击即可安装

敬请期待！

---

**开始探索你的 Skills Collection 吧！** 🎉
