import datetime
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-0ss2^y3uguv$3u(jg*ndf*gut7by)7ixp-(6w!#ry!!b^$mg32"
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = datetime.timedelta(days=30)  # 令牌有效时间
# JWT_REFRESH_DELTA = datetime.timedelta(days=30)         # 刷新令牌的有效时间
JWT_REFRESH_DELTA = datetime.timedelta(days=3)  # 剩余3天时刷新令牌
DEBUG = True

ALLOWED_HOSTS = [
    "http://localhost:5173",
    "127.0.0.1:5173",
    "localhost"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ebook',
        'USER': 'ebook',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    #"django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangoProject.model.VerifyToken.VerifyToken",
    'djangoProject.model.DecodeToken.DecodeToken',  # 如果请求中附加了正确的token将会解码并附加到request中
    'djangoProject.model.JWTRefreshMiddleware.JWTRefreshMiddleware',  # 先检查是否即将过期，过期刷新
    'djangoProject.model.JWTGenerateMiddleware.JWTGenerateMiddleware',  # 通过/login/接口来生成token并返回，该接口会自动拦截,
]
# 跨域允许列表
CORS_ALLOWED_ORIGINS = [
    "http://localhost:10000",  # 添加这个地址
    "http://127.0.0.1:10000",  # 或者这个
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]
# 跨域允许列表
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:10000",
    "http://127.0.0.1:10000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]
ROOT_URLCONF = "djangoProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangoProject.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
