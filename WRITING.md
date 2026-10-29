# 博客使用说明

博客地址：https://lea-32.github.io

## 第一次发布

进入仓库 Settings → Pages：
- Source：Deploy from a branch
- Branch：main
- 文件夹：/(root)
- 点击 Save，等待 Actions 中的 pages build and deployment 成功。

## 新增文章

1. 点击 Add file → Create new file。
2. 文件名填写 _posts/YYYY-MM-DD-english-title.md，日期替换为实际发布日期。
3. 复制 _drafts/note-template.md 中的内容，修改标题、分类和正文。
4. 点击 Commit changes，提交至 main。
5. 等待自动发布后打开博客查看。

顶部两组 --- 之间是 YAML 配置。缩进请用空格。
文章日期不要晚于当前日期，否则默认不会显示。

## 修改现有文章

打开 _posts 中的文章 → 点击编辑按钮 → 修改 → Commit changes。

## 图片

在仓库中创建 assets/images 文件夹并上传图片，正文使用：

![图片说明]({{ '/assets/images/example.png' | relative_url }})

将 example.png 替换为真实文件名，注意大小写。

## 草稿

_drafts 中的文件不会在正常发布时显示。准备好后复制到 _posts，
并按 YYYY-MM-DD-english-title.md 命名。

## 个性化

- 博客名称、描述、作者：修改 _config.yml。
- 首页介绍：修改 index.md。
- 关于页面：修改 about.md。
- 颜色、字号与间距：修改 assets/main.scss。
- 归档页会自动汇总文章。

## 发布失败

打开仓库 Actions → 失败的运行 → 查看报错。
优先检查 YAML 缩进、文件名日期以及 Liquid 模板语法。

公开仓库只保存准备公开的内容。

