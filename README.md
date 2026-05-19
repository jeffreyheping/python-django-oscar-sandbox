
# Django Oscar Sandbox 学习项目

## 项目的前世今生

### 前世：Django Oscar 的起源

**Django Oscar** 是一个成熟的开源电商框架，由英国的 Tangent Snowball 公司（现在的 The Hut Group）开发，用于驱动其内部电商平台。

- **诞生背景**：为了解决电商开发中重复性高、扩展性弱的问题，Django Oscar 被设计为模块化、可扩展的电商框架
- **核心哲学**："没有两个电商是相同的"，因此 Oscar 提供灵活的架构，允许深度定制而无需修改核心代码

### 今生：这个 Sandbox 项目的由来

这个项目是 **Django Oscar 官方的 Sandbox 沙箱示例** 的独立版本，故事是这样的：

1. **原始仓库结构**：Django Oscar 在其 GitHub 仓库中包含两个部分：
   - `src/oscar/` - Oscar 核心库代码
   - `sandbox/` - 演示项目，展示如何使用 Oscar

2. **问题**：直接克隆整个 Oscar 仓库太庞大，对于只想学习 Oscar 的人来说不需要核心源码

3. **解决方案**：使用 Git 稀疏检出（Sparse Checkout）只提取 `sandbox/` 目录的内容

4. **结果**：就是你现在看到的这个项目！

---

## 为什么这个项目是独立的？

✅ **不需要 Oscar 源码** - 通过 pip 安装 `django-oscar` 包即可运行  
✅ **轻量级** - 只包含学习和使用 Oscar 必需的文件  
✅ **可部署** - 可以独立部署到任何服务器

---

## 项目历史（本仓库的由来）

这个仓库的创建步骤：

```bash
# 1. 初始化 git
git init
git remote add origin https://github.com/django-oscar/django-oscar.git

# 2. 配置稀疏检出，只获取 sandbox 目录
git config core.sparseCheckout true
echo "sandbox" &gt; .git/info/sparse-checkout

# 3. 拉取代码
git pull origin master

# 4. 把 sandbox 内容移到根目录
mv sandbox/* .
mv sandbox/.[!.]* .
rmdir sandbox
```

---

## 项目自定义内容

相比官方 Sandbox，这个项目做了少量定制：

| 修改 | 位置 | 说明 |
|-----|------|------|
| 时区设置 | [settings.py](file:///c:/Users/jeffr/Documents/GitHub/python-django-oscar-sandbox/settings.py#L43) | 改为 `Asia/Shanghai` |
| 语言设置 | [settings.py](file:///c:/Users/jeffr/Documents/GitHub/python-django-oscar-sandbox/settings.py#L50) | 改为 `zh-hans` |
| 占位图片 | [public/media/image_not_found.jpg](file:///c:/Users/jeffr/Documents/GitHub/python-django-oscar-sandbox/public/media/image_not_found.jpg) | 确保此文件存在 |

---

## 快速开始

### 环境要求

- Python 3.8+
- Django 4.2+

### 安装依赖

```bash
pip install django-oscar[sorl-thumbnail]
```

### 启动项目

```bash
# 数据库迁移（如果需要）
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

### 访问地址

- 前台商店：http://127.0.0.1:8000/zh-cn/
- 管理后台：http://127.0.0.1:8000/zh-cn/dashboard/
- Django Admin：http://127.0.0.1:8000/admin/

### 默认账号

- 用户名：`admin`
- 密码：`admin`

---

## 更多文档

| 文档 | 内容 |
|------|------|
| [原始 README](README.original.rst) | Oscar 官方的沙箱说明 |
| [项目说明](项目说明.md) | ⭐ 详细的搭建和操作手册（推荐阅读） |
| [搭建指南](.trae/documents/django-oscar-sandbox搭建指南.md) | 快速搭建指南 |
| [完整步骤](.trae/documents/django-oscar-sandbox完整搭建步骤.md) | 从零开始的完整步骤 |
| [实施计划](.trae/documents/实施计划.md) | 项目实施计划 |

---

## 关于 Django Oscar

| 项目 | 链接 |
|------|------|
| 官方网站 | https://django-oscar.readthedocs.io/ |
| GitHub 仓库 | https://github.com/django-oscar/django-oscar |
| 官方演示 | https://latest.oscarcommerce.com/ |

---

## 学习路线建议

作为产品经理，学习 Oscar 可以按照以下顺序：

1. **体验前台** - 作为用户逛商店，了解电商流程
2. **体验后台** - 作为商家管理商品、订单、促销
3. **理解模块** - 了解各个 Oscar App 的职责
4. **深入流程** - 理解购物车、结账、订单处理等核心流程
5. **查看数据** - 通过 Django Admin 理解数据模型关系

祝学习愉快！
