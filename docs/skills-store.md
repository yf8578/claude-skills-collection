# 🏪 Skills Store - Interactive Browser

一个漂亮的终端 UI，让你可以浏览、搜索、安装 skills，就像使用应用商店一样！

## 🎯 功能特性

### ✨ 当前功能（v1.0）

- 📚 **浏览已安装的 Skills**
  - 查看所有已安装的 skills
  - 实时搜索和过滤
  - 查看详细信息（版本、描述、依赖等）

- 🔍 **智能搜索**
  - 按名称搜索
  - 按分类搜索
  - 按标签搜索
  - 按描述搜索

- 📊 **实时统计**
  - 已安装 skills 数量
  - 可用 skills 数量
  - 分类统计

- ⌨️ **便捷快捷键**
  - `↑/↓` 导航
  - `Enter` 或 `d` 查看详情
  - `i` 安装/重装
  - `/` 搜索
  - `r` 刷新
  - `?` 帮助
  - `q` 退出

- 🎨 **美观界面**
  - 斑马纹表格
  - 语法高亮
  - 实时状态更新
  - 进度显示

### 🚀 即将推出（v2.0）

- 🌐 **直接集成 ClawHub API**
  - 在 UI 内浏览 5,700+ skills
  - 点击即可安装
  - 查看评分和下载量

- 🔍 **GitHub 搜索集成**
  - 直接搜索 GitHub repos
  - 预览 README
  - 一键添加

- 🏷️ **高级过滤**
  - 按分类过滤
  - 按标签过滤
  - 按来源过滤

- 🔄 **自动更新检测**
  - 检测 skills 更新
  - 一键更新所有

## 🚀 快速开始

### 启动 Skills Store

```bash
cd ~/00zyf/AI/claude-skills-collection

# 方法 1：使用启动脚本（推荐）
./scripts/store.sh

# 方法 2：直接运行 Python
python3 scripts/skill-store.py
```

首次运行会自动安装依赖（textual, requests, rich）。

### 基本使用

1. **浏览已安装的 Skills**
   - 启动后默认显示 "Installed" 标签
   - 使用 `↑/↓` 方向键导航
   - 按 `Enter` 查看详细信息

2. **搜索 Skills**
   - 按 `/` 键激活搜索框
   - 输入关键词（名称、分类、标签等）
   - 实时过滤结果

3. **查看详情**
   - 选中 skill 后按 `Enter` 或 `d`
   - 查看完整描述、依赖、仓库链接等
   - 在详情页按 `i` 可以安装/重装

4. **安装 Skill**
   - 在列表中选中 skill
   - 按 `i` 键
   - 查看实时安装日志
   - 等待安装完成

5. **切换标签**
   - 按 `Tab` 切换标签
   - "Installed" - 已安装的 skills
   - "Discover" - 发现新 skills（指南）
   - "Help" - 完整帮助文档

## 🎨 界面预览

```
┌────────────────────────────────────────────────────────────────┐
│ Skills Store - Browse & Install Skills                         │
│ 📦 Total: 7 | ✅ Installed: 7 | 🌐 Available: 0                │
├────────────────────────────────────────────────────────────────┤
│ ┌─ Installed (7) ─┬─ Discover ─┬─ Help ─────────────────────┐ │
│ │                                                              │ │
│ │ Search: [________________________]                          │ │
│ │                                                              │ │
│ │ Name                 Version   Category    Description       │ │
│ │ ──────────────────────────────────────────────────────────  │ │
│ │ Citation Grabber     1.1.0     research    Fetch citations  │ │
│ │ PDF Skill            1.0.0     productivity PDF manipulation│ │
│ │ Word Document Skill  1.0.0     productivity Create Word...  │ │
│ │ PowerPoint Skill     1.0.0     productivity Create PPT...   │ │
│ │ Excel Skill          1.0.0     data        Excel sheets...  │ │
│ │ MCP Builder          1.0.0     development Create MCP...    │ │
│ │ Skill Creator        1.0.0     development Create skills... │ │
│ │                                                              │ │
│ └──────────────────────────────────────────────────────────────┘ │
│ ✓ Loaded 7 installed skills                                    │
├────────────────────────────────────────────────────────────────┤
│ q Quit | r Refresh | i Install | d Detail | / Search | ? Help │
└────────────────────────────────────────────────────────────────┘
```

## ⌨️ 快捷键参考

| 按键 | 功能 |
|------|------|
| `↑` / `k` | 上移 |
| `↓` / `j` | 下移 |
| `Enter` | 查看详情 |
| `d` | 查看详情 |
| `i` | 安装选中的 skill |
| `/` | 激活搜索框 |
| `r` | 刷新列表 |
| `Tab` | 切换标签 |
| `?` | 显示帮助 |
| `Esc` | 关闭弹窗 |
| `q` | 退出程序 |

## 🔧 安装依赖

Skills Store 需要以下 Python 库：

```bash
pip3 install textual requests rich
```

或使用 requirements 文件：

```bash
pip3 install -r requirements-browser.txt
```

首次运行 `./scripts/store.sh` 时会自动安装。

## 📊 工作流集成

### 与命令行工具配合

Skills Store 是 **可视化前端**，与命令行工具无缝集成：

```bash
# 使用 Skills Store 浏览和查看详情
./scripts/store.sh

# 使用命令行快速安装（如果你知道 skill 名称）
./scripts/add-skill.sh clawhub:pdf-analyzer

# 使用命令行查看状态
./scripts/list.sh
./scripts/status.sh pdf

# 然后回到 Skills Store 刷新查看
```

### 典型工作流

1. **发现阶段**：
   ```bash
   # 在外部搜索 skills
   clawhub search markdown
   ```

2. **浏览阶段**：
   ```bash
   # 启动 Skills Store 查看已安装的
   ./scripts/store.sh
   ```

3. **安装阶段**：
   ```bash
   # 方法 A：在 Skills Store 内安装（如果已在列表中）
   # 方法 B：命令行快速安装
   ./scripts/add-skill.sh clawhub:markdown-to-pdf
   ```

4. **管理阶段**：
   ```bash
   # 回到 Skills Store 刷新，查看新安装的 skill
   # 按 r 键刷新
   ```

## 🎯 使用场景

### 场景 1：查看我有哪些 Skills

```bash
./scripts/store.sh
# 启动后即可看到所有已安装的 skills
# 使用搜索快速找到想要的
```

### 场景 2：了解 Skill 的详细信息

```bash
# 1. 启动 Skills Store
./scripts/store.sh

# 2. 选中感兴趣的 skill
# 3. 按 Enter 查看详情
# 4. 查看描述、依赖、仓库链接等
```

### 场景 3：重新安装损坏的 Skill

```bash
# 1. 在 Skills Store 中找到该 skill
# 2. 按 i 键重新安装
# 3. 查看安装日志确认成功
```

### 场景 4：按分类查找 Skills

```bash
# 1. 启动 Skills Store
# 2. 按 / 激活搜索
# 3. 输入分类名如 "productivity"
# 4. 查看所有该分类的 skills
```

## 🔮 未来功能（路线图）

### v2.0 - ClawHub 集成
- [ ] 直接在 UI 内浏览 ClawHub 的 5,700+ skills
- [ ] 查看每个 skill 的：
  - 下载量
  - 评分
  - 最后更新时间
  - 作者信息
- [ ] 点击即可安装

### v3.0 - GitHub 集成
- [ ] 搜索 GitHub repos
- [ ] 预览 README
- [ ] 查看 stars、forks、issues
- [ ] 一键添加到 collection

### v4.0 - 高级功能
- [ ] Skill 更新检测
- [ ] 批量安装/更新
- [ ] 依赖关系可视化
- [ ] 使用统计
- [ ] 自定义分类
- [ ] 导入/导出 skill 列表

## 🐛 故障排除

### 问题 1: 无法启动 - 缺少依赖

```bash
# 错误信息：
❌ Missing dependencies!

# 解决方案：
pip3 install textual requests rich
```

### 问题 2: 界面显示异常

```bash
# 确保终端支持 256 色
echo $TERM  # 应该是 xterm-256color 或类似

# 如果不是，设置：
export TERM=xterm-256color
```

### 问题 3: 安装失败

```bash
# Skills Store 内的安装实际上调用 add-skill.sh
# 如果失败，可以在命令行手动运行：
./scripts/add-skill.sh clawhub:skill-name

# 查看详细错误信息
```

## 🎓 最佳实践

1. **定期刷新**
   - 添加新 skills 后，在 Skills Store 中按 `r` 刷新

2. **使用搜索**
   - 当 skills 很多时，用搜索快速定位

3. **查看详情**
   - 安装前先查看详情，了解依赖和功能

4. **结合使用**
   - Skills Store 用于浏览和管理
   - 命令行用于快速安装和自动化

## 📚 相关文档

- [USAGE_GUIDE.md](../USAGE_GUIDE.md) - 完整使用指南
- [README.md](../README.md) - 项目主文档
- [add-external-skills.md](./add-external-skills.md) - 添加外部 skills

## 💡 提示

- Skills Store 是 **只读浏览器**（目前）
- 实际的安装、更新操作通过脚本完成
- 所有更改都会自动同步到 registry.json
- 刷新列表（按 `r`）可以看到最新状态

---

**享受愉快的 Skills 浏览体验！** 🎉

如有问题或建议，欢迎在 GitHub 提 Issue：
https://github.com/yf8578/claude-skills-collection/issues
