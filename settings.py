"""
Django Oscar 电商项目配置文件
=====================================

这个文件是整个项目的"控制面板"，就像产品的功能开关和参数设置。
每个配置项都决定了系统的一个方面如何运作。

作为一个产品经理，你可以把这个文件理解为：
- 系统的"产品需求文档"（哪些功能启用）
- 运维的"部署指南"（数据库、缓存、文件存储等）
- 业务逻辑的"配置层"（语言、时区、业务规则等）

本文档将帮助你理解每个配置块的业务含义。
"""

import os
import environ
import oscar

# ========================================
# 第一部分：环境变量配置
# ========================================
# 环境变量是一种"外部配置"机制，允许在不修改代码的情况下改变系统行为
# 比如：开发环境和生产环境使用不同的数据库连接

env = environ.Env()

# 路径辅助函数：创建一个函数，用于生成项目内的相对路径
# location("db.sqlite") 会返回 "项目根目录/db.sqlite" 的完整路径
location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)
###等价写法
###def location(x):
###    return os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

# ========================================
# 第二部分：核心配置（最重要！）
# ========================================

# 【开发模式开关】
# DEBUG = True  表示"开发者模式"：
#   ✅ 显示详细错误页面（方便调试）
#   ✅ 启用模板调试功能
#   ✅ 静态文件由 Django 自动处理
#
# DEBUG = False 表示"生产模式"：
#   ✅ 隐藏错误细节（安全）
#   ✅ 性能优化
#   ✅ 需要配合 Web 服务器（如 Nginx）处理静态文件
DEBUG = env.bool('DEBUG', default=True)

# 【允许访问的域名列表】
# 这是安全措施，防止"域名劫持"攻击
# 只有列表中的域名能访问网站
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# 【邮件配置】
# 邮件前缀：所有系统邮件的主题都会以这个开头
# 例如："[Oscar sandbox] 您的订单已确认"
EMAIL_SUBJECT_PREFIX = '[Oscar sandbox] '

# 邮件发送方式：这里配置为"控制台输出"
# 生产环境会改为真实的 SMTP 服务器
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ========================================
# 第三部分：数据库配置
# ========================================
# 数据库是系统的"数据中心"，所有业务数据都存储在这里
# 支持多种数据库：SQLite（轻量级）、MySQL、PostgreSQL（企业级）

DATABASES = {
    'default': {
        # 数据库引擎：默认使用 SQLite（轻量级，适合学习和开发）
        # 生产环境可以改为 'django.db.backends.mysql' 或 'postgresql'
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
###等价写法
###        'ENGINE': env.str('DATABASE_ENGINE', default='django.db.backends.sqlite3'),


        # 数据库文件位置：db.sqlite 文件存储在哪里
        'NAME': os.environ.get('DATABASE_NAME', location('db.sqlite')),

        # 以下是 MySQL/PostgreSQL 的连接参数（SQLite 不需要）
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', None),
        'HOST': os.environ.get('DATABASE_HOST', None),
        'PORT': os.environ.get('DATABASE_PORT', None),

        # 【重要】原子请求：确保每个 HTTP 请求要么完全成功，要么完全回滚
        # 防止数据不一致（比如：订单创建成功但库存扣减失败）
        'ATOMIC_REQUESTS': True
    }
}

# ========================================
# 第四部分：缓存配置
# ========================================
# 缓存是"临时存储区"，用于加速频繁访问的数据
# 例如：热门商品列表、用户Session等

CACHES = {
    'default': env.cache(default='locmemcache://'),
}

# locmemcache = 本地内存缓存，最简单的缓存方式
# 生产环境可以改为 Redis（内存数据库）或 Memcached（专业缓存）
# CACHES = {
#     'default': env.cache(
#         default='redis://127.0.0.1:6379/1',  # 默认Redis地址
#         # 环境变量示例：redis://:mypassword@192.168.1.100:6379/1
#     )
# }
# CACHES = {
#     'default': env.cache(
#         default='memcached://127.0.0.1:11211',  # 默认值
#         # 环境变量 KEY 为 CACHE_URL，示例值：memcached://192.168.1.100:11211
#     )
# }

# ========================================
# 第五部分：时间和语言配置（国际化）
# ========================================
# 这部分决定了网站如何显示时间和语言

# 【时区配置】
# USE_TZ = True 表示启用时区支持
USE_TZ = True

# TIME_ZONE = 'Asia/Shanghai' 设定网站使用的时区
# 为什么用上海时间？因为我们在中国🇨🇳
# 系统中所有时间都会基于这个时区显示
TIME_ZONE = 'Asia/Shanghai'

# 【语言配置】
# LANGUAGE_CODE 决定网站的默认语言
# 'zh-hans' = 简体中文（Simplified Chinese）
# 'en-gb' = 英式英语（Django默认）
LANGUAGE_CODE = 'zh-hans'

# LANGUAGES 列出网站支持的所有语言
# Django Oscar 支持 20+ 种语言，包括：
# 中文、日语、韩语、英语、法语、德语、西班牙语等
# 这些语言的文件已经预置好了，只需要启用即可
LANGUAGES = (
    ('ar', gettext_noop('Arabic')),
    ('ca', gettext_noop('Catalan')),
    ('cs', gettext_noop('Czech')),
    ('da', gettext_noop('Danish')),
    ('de', gettext_noop('German')),
    ('en-gb', gettext_noop('British English')),
    ('el', gettext_noop('Greek')),
    ('es', gettext_noop('Spanish')),
    ('fi', gettext_noop('Finnish')),
    ('fr', gettext_noop('French')),
    ('it', gettext_noop('Italian')),
    ('ko', gettext_noop('Korean')),
    ('nl', gettext_noop('Dutch')),
    ('pl', gettext_noop('Polish')),
    ('pt', gettext_noop('Portuguese')),
    ('pt-br', gettext_noop('Brazilian Portuguese')),
    ('ro', gettext_noop('Romanian')),
    ('ru', gettext_noop('Russian')),
    ('sk', gettext_noop('Slovak')),
    ('uk', gettext_noop('Ukrainian')),
    ('zh-cn', gettext_noop('Simplified Chinese')),
)

# SITE_ID = 1
# Django "Sites" 框架的设置，用于多站点管理
# 本项目只有一个站点，所以 ID = 1

# 【国际化开关】
# USE_I18N = True 启用国际化系统
# 即使只用一种语言，也建议保持开启，因为某些功能依赖它
USE_I18N = True

# USE_L10N = True 启用本地化格式
# 自动根据语言格式化日期、数字、货币等
# 例如：中文用"2023年12月31日"，英文用"Dec 31, 2023"
USE_L10N = True

# ========================================
# 第六部分：文件存储配置（媒体和静态文件）
# ========================================
# 这一部分管理网站的所有"文件"：
# - 媒体文件：用户上传的内容（商品图片、用户头像等）
# - 静态文件：网站自己的资源（CSS、JS、图片等）

# 【媒体文件配置】（用户上传的文件）

# MEDIA_ROOT = 媒体文件的物理存储路径
# 所有用户上传的文件都会保存在这个目录下
# 实际路径：C:\Users\jeffr\Documents\GitHub\python-django-oscar-sandbox\public\media
MEDIA_ROOT = location("public/media")

# MEDIA_URL = 媒体文件的访问 URL
# 用户访问 http://localhost:8000/media/products/image.jpg 时
# Django 会从 MEDIA_ROOT 目录读取文件并返回
MEDIA_URL = '/media/'

# 【静态文件配置】（网站自己的资源）

# STATIC_URL = 静态文件的访问 URL
# 类似于 MEDIA_URL，但用于 CSS、JavaScript 等文件
STATIC_URL = '/static/'

# STATIC_ROOT = 静态文件在生产环境的物理存储路径
# 为什么需要单独的路径？
# 因为开发环境和生产环境的静态文件管理方式不同
STATIC_ROOT = location('public/static')

# STATICFILES_DIRS = 额外存放静态文件的目录
# 除了 Django 应用自带的静态文件，这些目录也会被包含
STATICFILES_DIRS = (
    location('static/'),
)

# 【文件查找器配置】
# Django 如何找到静态文件的位置
STATICFILES_FINDERS = (
    # 方式1：文件系统查找器 - 在 STATICFILES_DIRS 中查找
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 方式2：应用目录查找器 - 在各个 App 的 static/ 目录中查找
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# 【存储后端配置】
# 定义文件存储的方式和策略
STORAGES = {
    # 默认存储：用户上传的文件
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        # FileSystemStorage = 简单文件系统存储
        # 生产环境可以改为云存储（如 AWS S3、阿里云 OSS）
    },
    # 静态文件存储：优化过的静态文件管理
    "staticfiles": {
        "BACKEND": 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        # CompressedManifestStaticFilesStorage = 压缩 + 版本哈希
        # 好处：文件变更时自动生成新的URL，强制浏览器刷新缓存
    },
}

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 【主键字段类型】
# Django 4.0+ 的新默认值，使用更大的整数作为主键
# 避免未来数据量增长时主键溢出

# ========================================
# 第七部分：安全配置
# ========================================

# 【密钥】
# SECRET_KEY 是 Django 的"签名密钥"，用于：
# - CSRF 保护（防止跨站请求伪造）
# - Session 加密
# - 密码哈希
# ⚠️ 生产环境必须改成复杂的随机字符串！
SECRET_KEY = env.str('SECRET_KEY', default='UajFCuyjDKmWHe29neauXzHi9eZoRXr6RMbT5JyAdPiACBP6Cra2')

# ========================================
# 第八部分：模板系统配置（重点！）
# ========================================
# 模板 = HTML + 模板语法（Django Template Language）
# 模板系统决定"如何渲染网页"

TEMPLATES = [
    {
        # 模板引擎：Django 默认的模板引擎
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 【模板搜索路径】
        # Django 会按照这个列表的顺序搜索模板文件
        # 先找 templates/ 目录，找不到再去 App 的 templates/ 目录
        'DIRS': [
            location('templates'),  # 项目根目录的 templates/
        ],

        # 【模板加载器】
        # 定义 Django 如何查找和加载模板文件
        'OPTIONS': {
            'loaders': [
                # 加载器1：文件系统加载器 - 在 DIRS 中查找
                'django.template.loaders.filesystem.Loader',
                # 加载器2：应用目录加载器 - 在各个 App/templates/ 中查找
                'django.template.loaders.app_directories.Loader',
            ],

            # 【上下文处理器】（重要概念！）
            # 上下文处理器会在"每个请求"时自动添加一些变量到模板
            # 类似于"全局变量"或"公共数据"
            # 所有模板都能直接使用这些变量，不需要手动传递

            'context_processors': [
                # Django 内置的上下文处理器：
                'django.contrib.auth.context_processors.auth',  # 用户认证信息
                'django.template.context_processors.request',     # HTTP 请求对象
                'django.template.context_processors.debug',       # 调试信息
                'django.template.context_processors.i18n',        # 国际化变量
                'django.template.context_processors.media',      # MEDIA_URL
                'django.template.context_processors.static',      # STATIC_URL
                'django.contrib.messages.context_processors.messages',  # 消息框架

                # Oscar 特定的上下文处理器（每个都是功能模块）：
                'oscar.apps.search.context_processors.search_form',  # 🔍 搜索框
                'oscar.apps.communication.notifications.context_processors.notifications',  # 🔔 通知
                'oscar.apps.checkout.context_processors.checkout',    # 🛒 结账流程
                'oscar.core.context_processors.metadata',             # 📋 网站元数据（标题、描述等）
            ],

            # 是否启用模板调试
            'debug': DEBUG,
        }
    }
]

# 【理解上下文处理器】
# ========================================
# 上下文处理器是 Django 的"自动注入"机制
#
# 举例说明：
# 假设你在 context_processors 中添加了：
#   'myapp.context_processors.site_name'
# 而这个处理器返回：{'site_name': '我的电商网站'}
#
# 那么在任何一个模板中，你都可以直接使用：
#   {{ site_name }}  -> 输出 "我的电商网站"
#
# 不需要每个视图函数都手动传递这个变量！
# ========================================

# ========================================
# 第九部分：中间件配置（请求处理管道）
# ========================================
# 中间件 = "请求处理管道"中的一个个处理环节
# 每个 HTTP 请求都会依次经过这些中间件的处理

# 【处理顺序很重要！】从上到下执行

MIDDLEWARE = [
    # 1. 安全中间件
    'django.middleware.security.SecurityMiddleware',  # 安全相关的HTTP头

    # 2. 静态文件服务（WhiteNoise）
    # 生产环境中自动压缩和缓存静态文件
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # 3. 会话管理
    # 追踪用户访问状态（登录状态、购物车内容等）
    'django.contrib.sessions.middleware.SessionMiddleware',

    # 4. CSRF 保护
    # 防止跨站请求伪造攻击
    'django.middleware.csrf.CsrfViewMiddleware',

    # 5. X-Frame-Options
    # 防止网站被嵌入到 iframe 中（防止点击劫持）
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 6. 用户认证
    # 识别当前访问的用户是谁
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # 7. 消息框架
    # 用于显示一次性通知（如"登录成功"、"商品已添加到购物车"）
    'django.contrib.messages.middleware.MessageMiddleware',

    # 8. 静态页面
    # 自动处理简单的静态页面（如"关于我们"、"使用条款"）
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # 9. 语言处理
    # 根据用户偏好或URL自动切换语言
    'django.middleware.locale.LocaleMiddleware',

    # 10. 条件请求
    # 支持 HTTP 缓存（Last-Modified、ETag）
    'django.middleware.http.ConditionalGetMiddleware',

    # 11. 通用中间件
    # URL规范化、404处理等
    'django.middleware.common.CommonMiddleware',

    # 12. Oscar 购物车中间件 ⭐重要！
    # 确保每个请求都有一个购物车对象
    # 这个中间件会自动为匿名用户创建购物车
    # 即使不登录，用户也可以添加商品到购物车
    'oscar.apps.basket.middleware.BasketMiddleware',
]

# 【中间件处理流程图】
# ========================================
#
#   浏览器发送请求
#          ↓
#   SecurityMiddleware（安全检查）
#          ↓
#   WhiteNoiseMiddleware（静态文件）
#          ↓
#   SessionMiddleware（开启会话）
#          ↓
#   ... 其他中间件 ...
#          ↓
#   BasketMiddleware（加载购物车）⭐
#          ↓
#   视图函数处理请求
#          ↓
#   返回响应（反向经过各中间件）
#
# ========================================

# ROOT_URLCONF = 'urls'
# URL 路由配置：定义 URL 路径如何映射到视图函数
# 'urls' 指的是 urls.py 文件

# ========================================
# 第十部分：日志配置
# ========================================
# 日志 = 系统运行记录，用于：
# - 调试问题
# - 监控运行状态
# - 追踪错误

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    # 日志格式
    'formatters': {
        # 详细格式：包含时间、级别、模块名、消息
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
        # 简单格式：只有时间和消息
        'simple': {
            'format': '[%(asctime)s] %(message)s'
        },
    },

    # 根日志记录器配置
    'root': {
        'level': 'DEBUG',  # 记录所有 DEBUG 级别及以上的日志
        'handlers': ['console'],  # 输出到控制台
    },

    # 处理器配置（决定日志输出到哪里）
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',  # 不输出任何日志
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 输出到控制台/终端
            'formatter': 'simple'
        },
    },

    # 各个模块的日志配置
    'loggers': {
        # Oscar 框架日志
        'oscar': {
            'level': 'DEBUG',
            'propagate': True,  # 同时输出到父日志记录器
        },

        # Oscar 商品导入日志
        'oscar.catalogue.import': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },

        # Oscar 告警日志（静默）
        'oscar.alerts': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': False,
        },

        # Django 框架日志
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },

        # Django 请求日志（只记录错误）
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },

        # Django 数据库日志（只记录警告）
        'django.db.backends': {
            'level': 'WARNING',
            'propagate': True,
        },

        # Django 安全日志（静默）
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },

        # 第三方库：sorl-thumbnail（图片处理）
        'sorl.thumbnail': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

# ========================================
# 第十一部分：应用配置（核心！）
# ========================================
# INSTALLED_APPS = 启用的功能模块列表
# 这就像产品的"功能开关"，启用哪些模块就有哪些功能

INSTALLED_APPS = [
    # ========================================
    # Django 内置应用（基础功能）
    # ========================================

    'django.contrib.admin',  # 管理后台
    'django.contrib.auth',    # 用户认证系统
    'django.contrib.contenttypes',  # 内容类型框架
    'django.contrib.sessions',  # 会话管理
    'django.contrib.messages',  # 消息框架
    'django.contrib.staticfiles',  # 静态文件管理
    'django.contrib.sites',  # 多站点管理
    'django.contrib.flatpages',  # 静态页面

    # ========================================
    # Oscar 核心应用（电商核心功能）
    # ========================================
    # Oscar 使用模块化设计，每个功能都是独立的应用

    'oscar.config.Shop',  # Oscar 主配置（必须）

    # 📊 分析模块：用户行为分析、销售数据统计
    'oscar.apps.analytics.apps.AnalyticsConfig',

    # 🛒 结账模块：订单确认、支付流程、地址填写
    'oscar.apps.checkout.apps.CheckoutConfig',

    # 📍 地址模块：收货地址管理
    'oscar.apps.address.apps.AddressConfig',

    # 🚚 配送模块：运费计算、配送方式
    'oscar.apps.shipping.apps.ShippingConfig',

    # 📦 商品目录模块：商品展示、分类、搜索
    'oscar.apps.catalogue.apps.CatalogueConfig',

    # ⭐ 商品评论模块：用户评价、评分
    'oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig',

    # 📧 通信模块：邮件、短信通知
    'oscar.apps.communication.apps.CommunicationConfig',

    # 🤝 合作伙伴模块：供应商、多供应商市场
    'oscar.apps.partner.apps.PartnerConfig',

    # 🛍️ 购物车模块：购物车管理、商品增删改
    'oscar.apps.basket.apps.BasketConfig',

    # 💳 支付模块：支付方式、支付网关集成
    'oscar.apps.payment.apps.PaymentConfig',

    # 🎁 促销模块：优惠券、折扣活动、满减
    'oscar.apps.offer.apps.OfferConfig',

    # 📋 订单模块：订单管理、订单历史
    'oscar.apps.order.apps.OrderConfig',

    # 👤 客户模块：用户账户、收货地址、订单历史
    'oscar.apps.customer.apps.CustomerConfig',

    # 🔍 搜索模块：商品搜索（基于 Whoosh）
    'oscar.apps.search.apps.SearchConfig',

    # 🎟️ 优惠券模块：优惠券管理、使用规则
    'oscar.apps.voucher.apps.VoucherConfig',

    # ❤️ 愿望清单模块：收藏商品
    'oscar.apps.wishlists.apps.WishlistsConfig',

    # ========================================
    # Oscar 管理后台模块（商家后台）
    # ========================================
    # 商家可以通过这些模块管理网站的各个部分

    'oscar.apps.dashboard.apps.DashboardConfig',  # 管理后台主入口

    # 📈 报表模块：销售报表、统计数据
    'oscar.apps.dashboard.reports.apps.ReportsDashboardConfig',

    # 👥 用户管理：查看用户、管理会员
    'oscar.apps.dashboard.users.apps.UsersDashboardConfig',

    # 📦 订单管理：处理订单、发货、退款
    'oscar.apps.dashboard.orders.apps.OrdersDashboardConfig',

    # 📦 商品管理：添加商品、编辑商品、管理分类
    'oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig',

    # 🎁 促销管理：创建优惠券、设置折扣
    'oscar.apps.dashboard.offers.apps.OffersDashboardConfig',

    # 🤝 合作伙伴管理：管理供应商
    'oscar.apps.dashboard.partners.apps.PartnersDashboardConfig',

    # 📄 页面管理：编辑静态页面
    'oscar.apps.dashboard.pages.apps.PagesDashboardConfig',

    # 📋 商品系列管理：创建和管理商品系列
    'oscar.apps.dashboard.ranges.apps.RangesDashboardConfig',

    # ⭐ 评论管理：审核用户评论
    'oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig',

    # 🎟️ 优惠券管理：管理优惠券
    'oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig',

    # 📧 通信管理：发送邮件、查看通知
    'oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig',

    # 🚚 配送管理：配置配送方式
    'oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig',

    # ========================================
    # 第三方依赖库
    # ========================================

    'widget_tweaks',  # 表单美化工具
    'haystack',  # 搜索引擎框架（支持多种搜索引擎）
    'treebeard',  # 树形结构数据（如商品分类树）
    'sorl.thumbnail',  # 图片缩略图生成
    'easy_thumbnails',  # 另一个图片处理库
    'django_tables2',  # 表格显示组件（用于管理后台）

    # ========================================
    # 其他 Django 应用
    # ========================================

    'django.contrib.sitemaps',  # 网站地图生成
]

# ========================================
# 第十二部分：认证配置
# ========================================

# 【认证后端】
# 认证后端决定"如何验证用户身份"
# Oscar 自定义后端：允许用户使用"邮箱"登录
# Django 默认后端：使用"用户名"登录
AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',  # 邮箱登录 ⭐
    'django.contrib.auth.backends.ModelBackend',  # 用户名登录（备用）
)

# 【密码验证规则】
AUTH_PASSWORD_VALIDATORS = [
    # 最少9个字符
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    # 检查常见密码
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

# 【登录后跳转】
# 用户登录成功后跳转到哪个页面
LOGIN_REDIRECT_URL = '/'

# 【URL 末尾斜杠】
# True = 自动添加斜杠
# /products 会自动变成 /products/
APPEND_SLASH = True

# ========================================
# 第十三部分：消息框架配置
# ========================================

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    # 将错误消息标记为"danger"级别（Bootstrap样式）
    messages.ERROR: 'danger'
}

# ========================================
# 第十四部分：搜索引擎配置（重要！）
# ========================================

# 【搜索信号处理器】
# RealtimeSignalProcessor = 实时索引
# 商品添加/修改时会自动更新搜索索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 【Whoosh 搜索引擎配置】
# Whoosh 是一个纯 Python 实现的全文搜索引擎
# 适合中小型项目，简单易部署

HAYSTACK_CONNECTIONS = {
    'default': {
        # 搜索引擎引擎：Whoosh
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',

        # 索引文件存储路径
        'PATH': location('whoosh_index'),

        # 是否包含拼写检查
        'INCLUDE_SPELLING': True,
    },
}

# 【搜索引擎对比】
# ========================================
# 项目当前配置：Whoosh（轻量级，适合开发/学习）
# - ✅ 纯Python实现，无需额外安装
# - ✅ 配置简单
# - ⚠️ 性能有限，不适合大规模数据
#
# 生产环境推荐：Solr 或 Elasticsearch
# - ✅ 高性能，支持海量数据
# - ✅ 分布式部署
# - ✅ 高级搜索功能（分面搜索、高亮等）
# ========================================

# 【Solr 配置示例】（已注释，仅供参考）
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#         'URL': 'http://127.0.0.1:8983/solr/sandbox',
#         'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores',
#         'INCLUDE_SPELLING': True,
#     }
# }

# ========================================
# 第十五部分：调试工具配置
# ========================================

# 【允许访问调试工具的IP地址】
# Django Debug Toolbar 会在这些IP显示调试信息
INTERNAL_IPS = ['127.0.0.1', '::1']

# ========================================
# 第十六部分：Oscar 特定配置
# ========================================
# 这些配置覆盖 Oscar 的默认行为

from oscar.defaults import *

# 【商店配置】
# 网站标语
OSCAR_SHOP_TAGLINE = 'Sandbox'

# 【最近浏览商品】
# 记录用户最近浏览的20个商品
OSCAR_RECENTLY_VIEWED_PRODUCTS = 20

# 【允许匿名结账】
# True = 用户可以不登录就下单（先填写地址，再注册账号）
# False = 必须先登录才能下单
OSCAR_ALLOW_ANON_CHECKOUT = True

# ========================================
# 第十七部分：订单流程配置
# ========================================

# 【订单初始状态】
# 新订单创建时的状态
OSCAR_INITIAL_ORDER_STATUS = 'Pending'  # 待处理

# 订单中每个商品的初始状态
OSCAR_INITIAL_LINE_STATUS = 'Pending'

# 【订单状态流转规则】
# 定义订单可以从哪个状态转换到哪个状态
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),  # 待处理 → 处理中/已取消
    'Being processed': ('Complete', 'Cancelled',),  # 处理中 → 已完成/已取消
    'Cancelled': (),  # 已取消（不能转换到其他状态）
    'Complete': (),  # 已完成（不能转换到其他状态）
}

# 【订单状态级联】
# 当订单状态改变时，商品行状态如何跟着变化
OSCAR_ORDER_STATUS_CASCADE = {
    'Being processed': 'Being processed',  # 处理中 → 处理中
    'Cancelled': 'Cancelled',  # 取消 → 取消
    'Complete': 'Shipped',  # 完成 → 已发货
}

# ========================================
# 第十八部分：图片处理配置（sorl-thumbnail）
# ========================================

# 【缩略图调试】
# 与 DEBUG 保持一致
THUMBNAIL_DEBUG = DEBUG

# 【缩略图键前缀】
# 用于在缓存中区分不同项目的缩略图
THUMBNAIL_KEY_PREFIX = 'oscar-sandbox'

# 【缩略图元数据存储】
# KVStore = Key-Value Store（键值存储）
# 存储缩略图的元数据（尺寸、格式、原始图片路径等）
# cached_db_kvstore = 缓存在内存 + 存储在数据库
# 这就是之前你问的"KVStore"！
THUMBNAIL_KVSTORE = env(
    'THUMBNAIL_KVSTORE',
    default='sorl.thumbnail.kvstores.cached_db_kvstore.KVStore')

# 【Redis 配置】（可选，生产环境使用）
# 如果使用 Redis 存储缩略图元数据，配置在这里
THUMBNAIL_REDIS_URL = env('THUMBNAIL_REDIS_URL', default=None)

# 【easy-thumbnails 配置】
# 另一个图片处理库的默认存储设置
THUMBNAIL_DEFAULT_STORAGE_ALIAS = "default"

# 【会话序列化】
# 会话数据如何存储和传输
# JSON 序列化更安全（防止注入攻击）
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# ========================================
# 第十九部分：安全配置
# ========================================

# 【HTTPS 重定向】
# True = 所有HTTP请求都重定向到HTTPS
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

# 【HSTS 配置】
# HTTP Strict Transport Security
# 告诉浏览器只能通过HTTPS访问
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)

# 【防止内容类型嗅探】
SECURE_CONTENT_TYPE_NOSNIFF = True

# 【XSS 过滤器】
# 启用浏览器 XSS 保护
SECURE_BROWSER_XSS_FILTER = True

# ========================================
# 第二十部分：本地配置覆盖
# ========================================
# 允许创建 local_settings.py 来覆盖上述配置
# 这样可以在不修改主配置文件的情况下调整设置
# 常用于：
# - 本地开发环境的特殊配置
# - 生产环境的敏感信息（如数据库密码）

try:
    from settings_local import *
except ImportError:
    pass

# ========================================
# 配置总结
# ========================================
#
# 这个 settings.py 文件可以分为以下几个部分：
#
# 1️⃣ 环境基础（1-15行）
#    - 导入必要的库
#    - 设置路径辅助函数
#
# 2️⃣ 核心配置（11-29行）
#    - DEBUG 模式
#    - 允许的域名
#    - 数据库连接
#
# 3️⃣ 国际化（36-87行）
#    - 时区和语言
#    - 多语言支持
#
# 4️⃣ 文件系统（89-115行）
#    - 媒体文件（用户上传）
#    - 静态文件（CSS、JS）
#
# 5️⃣ 模板系统（124-153行）
#    - 模板搜索路径
#    - 上下文处理器（全局变量）
#
# 6️⃣ 中间件（155-173行）
#    - 请求处理管道
#    - 安全、会话、认证
#
# 7️⃣ 日志（183-257行）
#    - 日志格式和输出
#    - 各模块日志级别
#
# 8️⃣ 应用模块（260-311行）
#    - Django 内置应用
#    - Oscar 核心应用
#    - Oscar 管理后台
#    - 第三方库
#
# 9️⃣ 认证和支付（313-353行）
#    - 认证后端
#    - 密码规则
#    - 搜索引擎配置
#
# 🔟 Oscar 特定配置（372-428行）
#    - 商店配置
#    - 订单流程
#    - 图片处理
#    - 安全设置
#
# ========================================
