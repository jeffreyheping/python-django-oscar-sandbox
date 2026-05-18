# Django Oscar Sandbox 完整搭建计划

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

## 实施步骤

### 步骤 1：创建项目目录

**操作**：
```bash
cd C:\Users\jeffr\.qclaw\workspace
mkdir python-django-oscar-sandbox
cd python-django-oscar-sandbox
```

### 步骤 2：使用 Git Sparse Checkout 获取 sandbox 目录

**操作**：
```bash
git init
git remote add origin https://github.com/django-oscar/django-oscar.git
git config core.sparseCheckout true
echo "sandbox" > .git/info/sparse-checkout
git pull origin master
```

**缘由**：使用 Git Sparse Checkout 只获取 sandbox 目录，避免下载整个仓库

### 步骤 3：将 sandbox 内容移到根目录

**操作**：
```bash
mv sandbox/* .
mv sandbox/.[!.]* . 2>/dev/null || true
rmdir sandbox
```

**缘由**：简化项目结构，不需要额外的 sandbox 子目录

### 步骤 4：安装 Python 依赖

**操作**：
```bash
pip install django-oscar[sorl-thumbnail]
```

**缘由**：
- `[sorl-thumbnail]` 表示同时安装图片处理依赖
- 安装后 `import oscar` 就可以正常工作

### 步骤 5：创建数据库并迁移

**操作**：
```bash
python manage.py migrate
```

**缘由**：Oscar 的数据库迁移会自动执行

### 步骤 6：加载测试数据

**操作**：
```bash
python manage.py loaddata fixtures/auth.json
python manage.py oscar_populate_countries --initial-only
```

**缘由**：
- auth.json 包含测试用户
- 国家数据是结账流程必需的

### 步骤 7：创建管理员账户

**操作**：
```bash
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF
```

**缘由**：方便登录管理后台

### 步骤 8：收集静态文件

**操作**：
```bash
python manage.py collectstatic
```

**缘由**：Django 需要集中所有静态文件

### 步骤 9：验证并启动

**操作**：
```bash
python manage.py runserver
```

---

## 完整命令汇总

```bash
# 1. 创建目录
cd C:\Users\jeffr\.qclaw\workspace
mkdir python-django-oscar-sandbox
cd python-django-oscar-sandbox

# 2. 初始化 Git 并获取 sandbox
git init
git remote add origin https://github.com/django-oscar/django-oscar.git
git config core.sparseCheckout true
echo "sandbox" > .git/info/sparse-checkout
git pull origin master

# 3. 移动内容到根目录
mv sandbox/* .
mv sandbox/.[!.]* . 2>/dev/null || true
rmdir sandbox

# 4. 安装依赖
pip install django-oscar[sorl-thumbnail]

# 5. 数据库设置
python manage.py migrate

# 6. 加载测试数据
python manage.py loaddata fixtures/auth.json
python manage.py oscar_populate_countries --initial-only

# 7. 创建管理员
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

# 8. 收集静态文件
python manage.py collectstatic

# 9. 启动服务器
python manage.py runserver
```

---

## 预期结果

- 项目目录：`C:\Users\jeffr\.qclaw\workspace\python-django-oscar-sandbox`
- 访问地址：http://127.0.0.1:8000/zh-cn/
- 管理后台：http://127.0.0.1:8000/zh-cn/dashboard/
- 登录信息：用户名 `admin`，密码 `admin`

---

## 关键点

✅ **完全不需要 Oscar 源码** - sandbox 项目通过 pip 安装的包就能完美运行
✅ **最简化** - 只获取必要的文件
✅ **清晰易懂** - 每步都有缘由说明
