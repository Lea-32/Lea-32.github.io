# 博客访问与管理

- 公开网站：https://lea-32.github.io/
- 管理仓库：https://github.com/Lea-32/Lea-32.github.io
- 笔记目录：https://github.com/Lea-32/Lea-32.github.io/tree/main/_notes
- 发布状态：https://github.com/Lea-32/Lea-32.github.io/actions

读者访问网站无需登录；编辑仓库需要登录有写入权限的 GitHub 账号。博客当前没有独立后台。

## 在浏览器新增文章

进入仓库的 _notes 目录 → Add file → Create new file，文件名如 python-basics.md。
使用以下模板（文件名和 permalink 使用唯一的英文名称）：

```markdown
---
layout: note
title: "Python 学习笔记"
description: "整理 Python 基础语法与练习。"
permalink: /notes/python-basics/
tags: [Python, 编程]
---

## 学习目标

这里写正文。
```

点击 Commit changes，选择提交到 main。等待 Actions 中 pages build and deployment 完成。
首页、归档和搜索索引会自动加入这篇笔记。本网站用 _notes 集合管理笔记，不要求日期文件名。

## 修改、删除文章

进入 _notes → 打开文件 → 点击铅笔编辑 → Commit changes。
删除时使用文件页面菜单中的 Delete file 并提交。直接删除 _notes 中的发布副本即可；
如果以后重新导出整个 Vault，源文件仍会再次生成，需要同时调整导出范围。
可从 GitHub 文件历史中找到以前的版本并恢复。

## 图片

在仓库 assets/notes 目录点击 Add file → Upload files，上传图片并提交。
正文使用标准 Markdown，例如：

```markdown
![图片说明](/assets/notes/example.png)
```

图片路径和大小写必须与上传文件一致。浏览器手动上传不能自动转换 Obsidian 的 ![[图片]]。

## 从 Obsidian 更新

原始 Vault：E:\Agent-Learning\Agent-Learning
本地网站目录：E:\codex\Projects\lea-blog

本次提供的 import_obsidian.py 用于本机转换：

```powershell
python E:\codex\Projects\lea-blog\import_obsidian.py E:\Agent-Learning\Agent-Learning
```

脚本只修改本地网站副本，生成 _notes、assets/notes 与 import-report.json；不自动推送到 GitHub，
也不会修改 Vault。依赖 Python 与 Pillow。当前脚本会导出 Vault 内全部非隐藏 Markdown 笔记，
这是本次“全部笔记可公开”的范围；新增私人笔记前应先收窄导出范围。

转换后检查 import-report.json，再将 _notes 中的文章和 assets/notes 中的图片上传到仓库对应目录。
也可以请 Codex 在检查后更新上传。常规正文、代码、双括号图片与链接、高亮和提示块会转换；
Dataview、复杂插件、块引用或其他特殊语法需要进一步适配。

脚本现在会读取 Vault 笔记顶部的 YAML 属性，并保留发布副本中已有的分类、简介和标签；
同名字段以 Vault 为准。依赖 Python、Pillow、PyYAML。

## 内容分类

每篇笔记使用一个主要分类 category，并可添加多个 tags。

| category 值 | 页面名称 |
| --- | --- |
| papers | 论文精读 |
| stacks | 技术栈学习 |
| algorithms | 算法与数据结构 |
| projects | 项目实践 |
| notes | 随记（默认） |

在 Obsidian 或仓库文章顶部这样填写：

```yaml
---
title: "一篇论文的精读笔记"
category: papers
description: "研究问题、核心方法与实验结果的梳理。"
tags: [大模型, 论文精读]
---
```

直接在 GitHub 新建笔记时，还需保留 layout: note 和唯一的 permalink。
分类页、首页筛选、数量和搜索会在发布后自动更新。新增分类需同步修改
_data/categories.yml、分类入口页面，以及 import_obsidian.py 的 allowed 集合。

## 修改外观

- 标题、简介、作者：_config.yml。
- 个人介绍：about.md。
- 顶部导航与页脚：_layouts/default.html。
- 页面布局、卡片、配色和深色模式：assets/apple.scss。
- 分类名称与介绍：_data/categories.yml。
- 长文目录和公式：_layouts/note.html。

每次提交到 main 后自动发布。发布失败时打开 Actions 中对应任务查看报错。
