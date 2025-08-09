# Django의 URL 라우팅 기능들을 가져옵니다
from django.urls import path, include  # URL 패턴 정의와 하위 URL 포함 기능

# Django REST Framework의 자동 URL 라우터를 가져옵니다
from rest_framework.routers import DefaultRouter  # ViewSet을 위한 자동 URL 생성기

# 현재 앱의 뷰들을 가져옵니다
from . import views

# DRF 라우터 인스턴스 생성
# DefaultRouter: ViewSet에 대해 자동으로 CRUD URL들을 생성해주는 라우터
router = DefaultRouter()

# 라벨 ViewSet을 "labels" URL 패턴에 등록
# 자동으로 다음 URL들이 생성됨:
# GET    /labels/          -> 라벨 목록 조회
# POST   /labels/          -> 새 라벨 생성
# GET    /labels/{id}/     -> 특정 라벨 조회
# PUT    /labels/{id}/     -> 특정 라벨 전체 수정
# PATCH  /labels/{id}/     -> 특정 라벨 부분 수정
# DELETE /labels/{id}/     -> 특정 라벨 삭제
# GET    /labels/stats/    -> 라벨 통계 (ViewSet의 커스텀 액션)
# GET    /labels/{id}/contacts/ -> 특정 라벨의 연락처 목록
router.register("labels", views.LabelViewSet)

# 연락처 ViewSet을 "contacts" URL 패턴에 등록
# 자동으로 다음 URL들이 생성됨:
# GET    /contacts/        -> 연락처 목록 조회 (페이지네이션, 필터링, 검색 지원)
# POST   /contacts/        -> 새 연락처 생성
# GET    /contacts/{id}/   -> 특정 연락처 상세 조회
# PUT    /contacts/{id}/   -> 특정 연락처 전체 수정
# PATCH  /contacts/{id}/   -> 특정 연락처 부분 수정
# DELETE /contacts/{id}/   -> 특정 연락처 삭제
# GET    /contacts/birthdays_this_month/  -> 이번 달 생일인 연락처들
# GET    /contacts/statistics/            -> 연락처 통계 정보
# POST   /contacts/{id}/add_labels/       -> 연락처에 라벨 추가
# POST   /contacts/{id}/remove_labels/    -> 연락처에서 라벨 제거
router.register("", views.ContactViewSet)

# 어플리케이션의 URL 패턴 리스트
# router.urls: 위에서 등록한 ViewSet들로 자동 생성된 모든 URL들
# path("", include(...)): 빈 경로에 라우터 URL들을 포함 (예: /api/contacts/...)
urlpatterns = [path("", include(router.urls))]
