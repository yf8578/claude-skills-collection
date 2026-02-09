#!/usr/bin/env python3
"""
Simple Skills Browser - 简单的 Skills 浏览器
无需复杂依赖，直接显示本地和在线 skills
"""

import json
import sys
from pathlib import Path
from typing import List, Dict

# 尝试导入 requests，如果没有就提示
try:
    import requests
except ImportError:
    print("❌ 缺少 requests 库")
    print("安装方法：pip3 install requests")
    sys.exit(1)


COLLECTION_DIR = Path.home() / "00zyf" / "AI" / "claude-skills-collection"
REGISTRY_FILE = COLLECTION_DIR / "registry.json"
CLAWHUB_API = "https://clawhub.ai/api/v1/skills"


def load_local_skills() -> List[Dict]:
    """加载本地已安装的 skills"""
    if not REGISTRY_FILE.exists():
        return []

    with open(REGISTRY_FILE) as f:
        data = json.load(f)
        return data.get("skills", [])


def load_clawhub_skills() -> List[Dict]:
    """从 ClawHub 加载在线 skills"""
    try:
        response = requests.get(CLAWHUB_API, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except Exception as e:
        print(f"⚠️  无法连接 ClawHub: {e}")
        return []


def display_local_skills(skills: List[Dict]):
    """显示本地 skills"""
    print("\n" + "="*70)
    print("📦 已安装的 Skills")
    print("="*70 + "\n")

    if not skills:
        print("❌ 没有安装任何 skills")
        print("\n添加 skill：")
        print("  ./scripts/add-skill.sh clawhub:skill-name")
        return

    for i, skill in enumerate(skills, 1):
        name = skill.get('name', 'Unknown')
        version = skill.get('version', 'N/A')
        desc = skill.get('description', '')
        category = skill.get('category', 'N/A')
        source = skill.get('source', 'unknown')

        print(f"{i}. {name} (v{version})")
        print(f"   📁 {skill.get('id', 'N/A')}")
        print(f"   📝 {desc[:80]}..." if len(desc) > 80 else f"   📝 {desc}")
        print(f"   🏷️  {category} | 来源: {source}")
        print()

    print(f"总计: {len(skills)} 个 skills")
    print("\n查看详情：./scripts/status.sh <skill-name>")
    print("添加新的：./scripts/add-skill.sh clawhub:<skill-name>")


def display_clawhub_skills(skills: List[Dict]):
    """显示 ClawHub 在线 skills"""
    print("\n" + "="*70)
    print("🌐 ClawHub 可用的 Skills")
    print("="*70 + "\n")

    if not skills:
        print("❌ 无法获取 ClawHub skills")
        return

    for i, skill in enumerate(skills, 1):
        slug = skill.get('slug', 'unknown')
        name = skill.get('displayName', 'Unknown')
        summary = skill.get('summary', '')
        stats = skill.get('stats', {})
        tags = skill.get('tags', {})

        downloads = stats.get('downloads', 0)
        stars = stats.get('stars', 0)
        version = tags.get('latest', 'N/A')

        print(f"{i}. {name}")
        print(f"   🆔 {slug}")
        print(f"   📝 {summary[:80]}..." if summary and len(summary) > 80 else f"   📝 {summary or 'No description'}")
        print(f"   📊 ⭐ {stars} | 📥 {downloads} | v{version}")
        print()

    print(f"总计: {len(skills)} 个 skills")
    print("\n添加到你的 collection：")
    print("  ./scripts/add-skill.sh clawhub:<slug>")
    print("\n例如：")
    if skills:
        example_slug = skills[0].get('slug', 'example')
        print(f"  ./scripts/add-skill.sh clawhub:{example_slug}")


def search_skills(query: str, skills: List[Dict], skill_type: str = "local"):
    """搜索 skills"""
    query_lower = query.lower()
    matching = []

    for skill in skills:
        if skill_type == "local":
            name = skill.get('name', '').lower()
            desc = skill.get('description', '').lower()
            tags = ' '.join(skill.get('tags', [])).lower()
            category = skill.get('category', '').lower()

            if query_lower in name or query_lower in desc or query_lower in tags or query_lower in category:
                matching.append(skill)
        else:  # clawhub
            name = skill.get('displayName', '').lower()
            slug = skill.get('slug', '').lower()
            summary = skill.get('summary', '').lower() if skill.get('summary') else ''

            if query_lower in name or query_lower in slug or query_lower in summary:
                matching.append(skill)

    return matching


def interactive_menu():
    """交互式菜单"""
    print("\n" + "="*70)
    print("🏪 Skills Browser - 简单浏览器")
    print("="*70)
    print("\n选择操作：")
    print("  1. 查看已安装的 skills")
    print("  2. 浏览 ClawHub 在线 skills")
    print("  3. 搜索已安装的 skills")
    print("  4. 搜索 ClawHub skills")
    print("  5. 显示统计信息")
    print("  q. 退出")
    print()

    choice = input("请选择 (1-5/q): ").strip()
    return choice


def show_stats():
    """显示统计信息"""
    local = load_local_skills()

    print("\n" + "="*70)
    print("📊 统计信息")
    print("="*70 + "\n")

    print(f"已安装 skills: {len(local)}")

    # 按分类统计
    categories = {}
    for skill in local:
        cat = skill.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    print("\n按分类：")
    for cat, count in categories.items():
        print(f"  {cat}: {count}")

    # 按来源统计
    sources = {}
    for skill in local:
        src = skill.get('source', 'unknown')
        sources[src] = sources.get(src, 0) + 1

    print("\n按来源：")
    for src, count in sources.items():
        print(f"  {src}: {count}")

    print("\nClawHub 状态：正在检查...")
    clawhub = load_clawhub_skills()
    if clawhub:
        total_downloads = sum(s.get('stats', {}).get('downloads', 0) for s in clawhub)
        total_stars = sum(s.get('stats', {}).get('stars', 0) for s in clawhub)
        print(f"  可用 skills: {len(clawhub)}")
        print(f"  总下载量: {total_downloads}")
        print(f"  总星标: {total_stars}")


def main():
    """主程序"""
    import sys

    if len(sys.argv) > 1:
        # 命令行模式
        command = sys.argv[1]

        if command == "local":
            skills = load_local_skills()
            display_local_skills(skills)

        elif command == "clawhub":
            print("🔄 正在从 ClawHub 获取 skills...")
            skills = load_clawhub_skills()
            display_clawhub_skills(skills)

        elif command == "search":
            if len(sys.argv) < 3:
                print("用法: browse.py search <关键词>")
                return

            query = sys.argv[2]
            print(f"🔍 搜索本地 skills: {query}")
            local = load_local_skills()
            results = search_skills(query, local, "local")

            if results:
                display_local_skills(results)
            else:
                print(f"❌ 没有找到匹配 '{query}' 的 skills")

        elif command == "stats":
            show_stats()

        else:
            print(f"未知命令: {command}")
            print("\n用法:")
            print("  browse.py local      - 查看已安装的 skills")
            print("  browse.py clawhub    - 查看 ClawHub skills")
            print("  browse.py search <关键词> - 搜索 skills")
            print("  browse.py stats      - 显示统计信息")

    else:
        # 交互模式
        while True:
            choice = interactive_menu()

            if choice == '1':
                skills = load_local_skills()
                display_local_skills(skills)
                input("\n按 Enter 继续...")

            elif choice == '2':
                print("\n🔄 正在从 ClawHub 获取 skills...")
                skills = load_clawhub_skills()
                display_clawhub_skills(skills)
                input("\n按 Enter 继续...")

            elif choice == '3':
                query = input("\n🔍 输入搜索关键词: ").strip()
                local = load_local_skills()
                results = search_skills(query, local, "local")
                if results:
                    display_local_skills(results)
                else:
                    print(f"❌ 没有找到匹配 '{query}' 的 skills")
                input("\n按 Enter 继续...")

            elif choice == '4':
                query = input("\n🔍 输入搜索关键词: ").strip()
                print("🔄 正在从 ClawHub 搜索...")
                clawhub = load_clawhub_skills()
                results = search_skills(query, clawhub, "clawhub")
                if results:
                    display_clawhub_skills(results)
                else:
                    print(f"❌ 没有找到匹配 '{query}' 的 skills")
                input("\n按 Enter 继续...")

            elif choice == '5':
                show_stats()
                input("\n按 Enter 继续...")

            elif choice.lower() == 'q':
                print("\n👋 再见！")
                break

            else:
                print("\n❌ 无效选择，请重试")
                input("\n按 Enter 继续...")


if __name__ == "__main__":
    main()
