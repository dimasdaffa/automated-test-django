# 1. Imports from Third-Party Libraries (Django, Ninja, JWT)
from django.contrib.auth.models import User
from ninja import NinjaAPI, Router, Schema, File, Form, UploadedFile
from ninja.responses import Response
from ninja.pagination import paginate, PageNumberPagination
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth
from ninja_simple_jwt.auth.views.api import mobile_auth_router

# 2. Imports from Your Local Application (lms_core)
# (Impor ini disiapkan untuk endpoint LMS yang akan dibuat nanti)
from lms_core.models import Course, CourseMember, CourseContent, Comment
from lms_core.schema import (
    CourseSchemaOut, 
    CourseMemberOut, 
    CourseSchemaIn,
    CourseContentMini, 
    CourseContentFull,
    CourseCommentOut, 
    CourseCommentIn
)

# 3. API Initialization and Authentication
# Inisialisasi API utama cukup sekali saja dalam satu file.
api = NinjaAPI(
    title="LMS Core API",
    version="v1",
    description="API for Learning Management System"
)

# Inisialisasi skema autentikasi untuk digunakan pada endpoint yang butuh proteksi.
# Nama variabel diubah menjadi snake_case (api_auth) sesuai konvensi PEP 8.
api_auth = HttpJwtAuth()

# 4. Routers Definition
# Definisikan router utama untuk endpoint aplikasi Anda.
# Endpoint "hello" akan dimasukkan ke dalam router ini.
router = Router()

# 5. Schema and Endpoint Definitions
# Definisikan schema yang dibutuhkan oleh endpoint di bawah.
class HelloResponse(Schema):
    """Schema for the /hello endpoint response."""
    msg: str

@router.get("/hello", response=HelloResponse, summary="Simple endpoint to test API")
def hello(request):
    """
    Returns a simple "Hello World" message.
    """
    return {"msg": "Hello World"}

# Anda bisa menambahkan endpoint lain untuk LMS di sini, menggunakan router yang sama.
# Contoh:
# @router.get("/courses", response=list[CourseSchemaOut], auth=api_auth)
# def list_courses(request):
#     return Course.objects.all()


# 6. Register All Routers to the Main API
# Tambahkan router-router yang sudah dibuat ke instance API utama.
# Router untuk autentikasi (login, refresh, etc.) dari simple_jwt.
api.add_router("/auth/", mobile_auth_router, tags=["Authentication"])

# Router utama aplikasi Anda.
api.add_router("/", router, tags=["Main Endpoints"])