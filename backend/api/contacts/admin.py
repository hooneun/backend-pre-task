# Django의 관리자 페이지 기능을 가져옵니다
from django.contrib import admin

# 현재 앱의 모델들을 가져옵니다
from api.contacts.models import Label, Contact


# 라벨 모델을 Django 관리자 페이지에 등록하고 설정하는 클래스
# @admin.register 데코레이터: Label 모델과 이 Admin 클래스를 자동으로 연결
@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    """
    라벨 모델의 Django 관리자 페이지 설정
    관리자가 웹 브라우저에서 라벨을 쉽게 관리할 수 있도록 UI를 구성합니다
    """

    # 목록 페이지에서 표시할 컬럼들 (테이블의 열 제목들)
    list_display = ["name", "color", "created_at"]

    # 오른쪽 사이드바에 표시할 필터들 (생성일로 필터링 가능)
    list_filter = ["created_at"]

    # 검색 기능을 위한 필드들 (라벨명으로 검색 가능)
    search_fields = ["name"]

    # 기본 정렬 순서 (라벨명 오름차순)
    ordering = ["name"]


# 연락처 모델을 Django 관리자 페이지에 등록하고 설정하는 클래스
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    연락처 모델의 Django 관리자 페이지 설정
    관리자가 웹 브라우저에서 연락처를 쉽게 관리할 수 있도록 UI를 구성합니다
    """

    # 목록 페이지에서 표시할 컬럼들 (각 연락처의 핵심 정보들을 테이블로 표시)
    list_display = [
        "name",  # 이름
        "email",  # 이메일
        "phone",  # 전화번호
        "company",  # 회사명
        "position",  # 직책
        "get_labels",  # 연결된 라벨들 (커스텀 메소드)
        "created_at",  # 생성일시
    ]

    # 오른쪽 사이드바 필터들 (라벨, 회사, 생성일로 필터링 가능)
    list_filter = ["labels", "company", "created_at"]

    # 검색 기능을 위한 필드들 (이름, 이메일, 전화번호, 회사명으로 검색 가능)
    search_fields = ["name", "email", "phone", "company"]

    # 다대다 관계 필드(labels)를 위한 가로형 선택 위젯
    # 라벨 선택 시 더 편리한 UI 제공 (양쪽 박스에서 드래그앤드롭으로 선택)
    filter_horizontal = ["labels"]

    # 기본 정렬 순서 (최신 생성순)
    ordering = ["-created_at"]

    # 상세 편집 페이지의 필드 그룹화 설정
    # 관련있는 필드들을 섹션별로 묶어서 더 직관적인 UI 제공
    fieldsets = (
        ("기본 정보", {"fields": ("name", "profile_url")}),  # 첫 번째 섹션: 필수 정보들
        (
            "연락 정보",
            {  # 두 번째 섹션: 연락 관련 정보들
                "fields": ("email", "phone", "address", "website")
            },
        ),
        (
            "회사 정보",
            {"fields": ("company", "position")},  # 세 번째 섹션: 직장 관련 정보들
        ),
        (
            "추가 정보",
            {"fields": ("birthday", "memo", "labels")},  # 네 번째 섹션: 부가 정보들
        ),
    )

    # 커스텀 메소드: 연락처의 라벨들을 관리자 목록에서 문자열로 표시
    def get_labels(self, obj):
        """
        연락처에 연결된 모든 라벨들을 쉼표로 구분된 문자열로 변환
        obj: 현재 연락처 객체 (Contact 인스턴스)
        반환값: "가족, 친구, 회사" 형태의 문자열
        """
        # obj.labels.all(): 이 연락처와 연결된 모든 라벨들을 조회
        # [label.name for label in ...]: 각 라벨의 이름만 추출하여 리스트 생성
        # ", ".join(...): 리스트의 요소들을 쉼표와 공백으로 연결한 문자열 생성
        return ", ".join([label.name for label in obj.labels.all()])

    # 관리자 페이지에서 이 메소드의 컬럼 제목을 "라벨"로 설정
    get_labels.short_description = "라벨"
