# Django Oscar Sandbox 完整搭建文档

## 目标
在 `C:\Users\jeffr\.qclaw\workspace\python-django-oscar-sandbox` 目录下，从零开始搭建一个完整的 django-oscar sandbox 项目。

## 核心理解

**关键问题**：django-oscar 的 GitHub 仓库包含两部分：
1. **Oscar 核心源码** (`src/oscar/`) - 电商框架本身
2. **Sandbox 示例项目** (`sandbox/`) - 一个完整的电商网站示例

**解决方案**：
- 使用 `pip install django-oscar` 安装 Oscar 核心包（通过 PyPI）
- 只从 GitHub 获取 sandbox 项目文件夹（示例代码）
- 这样就不需要 Oscar 源码，只依赖 pip 安装的包

---

## 最简化的完整流程

### 方法一：完全不需要 Oscar 源码（推荐）

```bash
# 1. 创建目录
cd C:\Users\jeffr\.qclaw\workspace
mkdir python-django-oscar-sandbox
cd python-django-oscar-sandbox

# 2. 安装 Oscar（会自动获取所有依赖）
pip install django-oscar[sorl-thumbnail]

# 3. 从 GitHub 手动下载 sandbox 文件夹
# 访问：https://github.com/django-oscar/django-oscar/tree/master/sandbox
# 下载并解压到当前目录

# 4. 进入 sandbox 目录
cd sandbox

# 5. 创建数据库
python manage.py migrate

# 6. 加载测试数据（可选）
python manage.py loaddata fixtures/auth.json
python manage.py oscar_populate_countries --initial-only

# 7. 收集静态文件
python manage.py collectstatic

# 8. 启动服务器
python manage.py runserver
```

### 方法二：使用 Git Sparse Checkout（高级）

```bash
# 1. 创建目录并初始化
cd C:\Users\jeffr\.qclaw\workspace
mkdir python-django-oscar-sandbox
cd python-django-oscar-sandbox
git init

# 2. 添加远程仓库
git remote add origin https://github.com/django-oscar/django-oscar.git

# 3. 使用 Sparse Checkout 只获取 sandbox 目录
git config core.sparseCheckout true
echo "sandbox" > .git/info/sparse-checkout

# 4. 拉取代码
git pull origin master

# 5. 移动 sandbox 内容到根目录
mv sandbox/* .
mv sandbox/.* . 2>/dev/null || true
rmdir sandbox

# 6. 后续步骤同上
pip install django-oscar[sorl-thumbnail]
python manage.py migrate
python manage.py runserver
```

---

## 详细安装步骤说明

### 第一步：准备工作 - 创建项目目录

**操作**：
```bash
cd C:\Users\jeffr\.qclaw\workspace
mkdir python-django-oscar-sandbox
cd python-django-oscar-sandbox
```

**缘由**：
- 在工作区内创建一个独立的目录用于存放 sandbox 项目
- 保持项目结构整洁，与其他项目分离

---

### 第二步：安装依赖

**操作**：
```bash
pip install django-oscar[sorl-thumbnail]
```

**缘由**：
- `[sorl-thumbnail]` 表示同时安装图片处理依赖
- 这是官方推荐的最小依赖集
- 安装后，`import oscar` 就可以正常工作了

**完整依赖会自动安装**：
```txt
django>=4.2,<6.2
Pillow>=6.0
django-extra-views>=0.13
django-haystack>=3.0b1
django-treebeard>=4.7.0
Babel>=1.0
purl>=0.7
phonenumbers
django-phonenumber-field>=4.0.0
factory-boy>=3.3.1
django-tables2>=2.3
django-widget-tweaks>=1.4.1
sorl-thumbnail>=12.10.0
```

---

### 第三步：获取 Sandbox 文件夹

**方案 A：手动下载（最简单）**
1. 访问 https://github.com/django-oscar/django-oscar/tree/master/sandbox
2. 点击 "Download ZIP" 或使用 GitHub CLI
3. 解压到 `C:\Users\jeffr\.qclaw\workspace\python-django-oscar-sandbox`

**方案 B：使用 Git Sparse Checkout（推荐给开发者）**
```bash
git init
git remote add origin https://github.com/django-oscar/django-oscar.git
git config core.sparseCheckout true
echo "sandbox" > .git/info/sparse-checkout
git pull origin master

# 将 sandbox 内容移到根目录
mv sandbox/* .
mv sandbox/.[!.]* . 2>/dev/null || true
rmdir sandbox
```

**缘由**：
- GitHub 的 sandbox 文件夹包含了完整的示例项目
- 这个文件夹依赖 pip 安装的 django-oscar 包，不需要本地源码

---

### 第四步：创建数据库

**操作**：
```bash
cd sandbox
python manage.py migrate
```

**缘由**：
- Django 的 migration 系统会自动检测 Oscar 的数据库迁移
- SQLite 数据库（`db.sqlite`）会自动创建

---

### 第五步：加载测试数据

**操作**：
```bash
# 加载用户账户
python manage.py loaddata fixtures/auth.json

# 加载国家数据（结账必需）
python manage.py oscar_populate_countries --initial-only

# 加载产品数据（可选）
python manage.py oscar_import_catalogue fixtures/books.essential.csv fixtures/books.hacking.csv
```

**缘由**：
- 测试数据包含示例商品、用户、页面内容
- 让网站立即可以看到效果
- 国家数据是必需的，否则结账流程会失败

---

### 第六步：收集静态文件

**操作**：
```bash
python manage.py collectstatic
```

**缘由**：
- Django 需要将所有静态文件集中到 `STATIC_ROOT` 目录
- 包括 Oscar 核心、Django Admin、自定义应用的静态文件

---

### 第七步：创建管理员账户

**操作**：
```bash
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Admin user created!")
EOF
```

**缘由**：
- 方便登录管理后台
- 用户名和密码都是 `admin`

---

### 第八步：启动开发服务器

**操作**：
```bash
python manage.py runserver
```

**缘由**：
- Django 开发服务器
- 默认地址：http://127.0.0.1:8000

---

## 访问地址

- **前台网站**：http://127.0.0.1:8000/zh-cn/
- **管理后台**：http://127.0.0.1:8000/zh-cn/dashboard/
- **登录页面**：http://127.0.0.1:8000/zh-cn/accounts/login/

**登录信息**：
- 用户名：`admin`
- 密码：`admin`

---

## 完整命令汇总

```bash
# 一行命令创建并启动（不含测试数据）
cd C:\Users\jeffr\.qclaw\workspace
mkdir python-django-oscar-sandbox
cd python-django-oscar-sandbox
pip install django-oscar[sorl-thumbnail]
# [手动下载 sandbox 文件夹]
cd sandbox
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

---

## 常见问题解决

### 问题 1：找不到 Oscar 模块
```
ModuleNotFoundError: No module named 'oscar'
```
**解决**：
```bash
pip install django-oscar
```

### 问题 2：静态文件不显示
**解决**：
```bash
python manage.py collectstatic
```

### 问题 3：数据库错误
**解决**：
```bash
rm db.sqlite3
python manage.py migrate
```

### 问题 4：结账时报错"没有国家"
**解决**：
```bash
python manage.py oscar_populate_countries --initial-only
```

---

## 文件结构

搭建完成后应该有：
```
python-django-oscar-sandbox/
└── sandbox/
    ├── apps/
    │   ├── __init__.py
    │   ├── offers.py
    │   ├── sitemaps.py
    │   └── user/
    │       ├── __init__.py
    │       └── models.py
    ├── fixtures/
    │   ├── auth.json
    │   ├── books.essential.csv
    │   └── ...
    ├── public/
    │   ├── media/
    │   └── static/
    ├── static/
    │   └── robots.txt
    ├── __init__.py
    ├── db.sqlite3
    ├── manage.py
    ├── README.rst
    ├── settings.py
    ├── settings_postgres.py
    ├── settings_sphinx.py
    ├── test_migrations.sh
    ├── urls.py
    ├── uwsgi.ini
    └── wsgi.py
```

---

## 最佳实践

1. **始终使用虚拟环境**（可选但推荐）
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **保存依赖列表**（便于在其他机器重建）
   ```bash
   pip freeze > requirements.txt
   ```

3. **定期更新**
   ```bash
   pip install --upgrade django-oscar
   ```

---

## 总结

**最简单的方法只需要 4 步**：
1. `pip install django-oscar[sorl-thumbnail]`
2. 下载 sandbox 文件夹
3. `python manage.py migrate`
4. `python manage.py runserver`

**完全不需要 Oscar 源码！** sandbox 项目通过 pip 安装的包就能完美运行。
