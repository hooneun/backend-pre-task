# Django REST Framework의 핵심 컴포넌트들을 가져옵니다
from rest_framework import viewsets, filters, status  # ViewSet, 필터, HTTP 상태코드
from rest_framework.decorators import api_view, action  # API 뷰 데코레이터, 커스텀 액션 데코레이터
from rest_framework.response import Response  # API 응답 객체
from rest_framework.request import Request   # API 요청 객체
from django_filters.rest_framework import DjangoFilterBackend  # 필터링 백엔드
from django.db.models import Q, Count  # Q: 복잡한 쿼리 조건, Count: 개수 집계 함수

# 현재 앱의 다른 모듈들을 가져옵니다
from .filters import ContactFilter      # 연락처 필터링 클래스
from .models import Label, Contact      # 데이터베이스 모델들
from .pagination import CustomPageNumberPagination  # 커스텀 페이지네이션
from .serializers import (              # 시리얼라이저들 (데이터 직렬화/역직렬화)
    LabelSerializer,                    # 라벨 기본 시리얼라이저
    ContactSerializer,                  # 연락처 상세 시리얼라이저
    ContactListSerializer,              # 연락처 목록용 간소화 시리얼라이저
    LabelStatsSerializer,               # 라벨 통계용 시리얼라이저
)


# API 테스트용 간단한 뷰 함수
# @api_view 데코레이터: 이 함수를 REST API 엔드포인트로 만들어줍니다
@api_view(["GET"])  # GET 방식의 HTTP 요청만 허용
def test_api(request: Request) -> Response:
    """
    API 연결 테스트용 엔드포인트
    GET /api/test/ 로 접근하면 사용 가능한 API 목록을 반환합니다
    """
    return Response(  # JSON 형태로 응답 반환
        {
            "message": "success",           # 성공 메시지
            "endpoints": {                  # 사용 가능한 API 엔드포인트들
                "contacts": "/api/contacts/",   # 연락처 관련 API
                "labels": "/api/labels/",       # 라벨 관련 API
            },
        }
    )


# 라벨 관리를 위한 ViewSet 클래스
# ModelViewSet: Create, Read, Update, Delete 모든 기능을 자동으로 제공하는 클래스
class LabelViewSet(viewsets.ModelViewSet):
    """
    라벨 관리 ViewSet
    - GET /labels/: 모든 라벨 조회 (목록)
    - POST /labels/: 새 라벨 생성
    - GET /labels/{id}/: 특정 라벨 조회 (상세)
    - PUT /labels/{id}/: 특정 라벨 전체 수정
    - PATCH /labels/{id}/: 특정 라벨 부분 수정
    - DELETE /labels/{id}/: 특정 라벨 삭제
    """
    # 기본 쿼리셋: 모든 라벨을 대상으로 합니다
    queryset = Label.objects.all()
    # 사용할 시리얼라이저: 라벨 데이터를 JSON으로 변환/역변환
    serializer_class = LabelSerializer

    # 필터링, 검색, 정렬 기능을 위한 백엔드 설정
    filter_backends = [
        DjangoFilterBackend,    # 필드 기반 필터링 (예: ?name=가족)
        filters.SearchFilter,   # 텍스트 검색 (예: ?search=가족)
        filters.OrderingFilter, # 정렬 (예: ?ordering=name)
    ]
    # 검색 가능한 필드들: 라벨명으로만 검색 가능
    search_fields = ["name"]
    # 정렬 가능한 필드들: 이름과 생성일로 정렬 가능
    ordering_fields = ["name", "created_at"]
    # 기본 정렬 순서: 라벨명 오름차순
    ordering = ["name"]

    # 커스텀 액션: 라벨 통계 조회
    # @action 데코레이터: 기본 CRUD 외에 추가 기능을 만들 때 사용
    # detail=False: 개별 라벨이 아닌 전체 라벨에 대한 액션 (URL: /labels/stats/)
    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        라벨 통계 조회 API
        GET /labels/stats/
        각 라벨별로 연결된 연락처 개수를 포함한 통계 정보를 반환합니다
        """
        # annotate: 각 라벨에 연결된 연락처 개수를 계산해서 추가
        # Count("contacts"): contacts 필드(다대다 관계)의 개수를 셈
        labels_with_counts = Label.objects.annotate(
            contact_count=Count("contacts")  # contact_count라는 가상 필드 추가
        ).order_by("-contact_count")  # 연락처 개수가 많은 순으로 정렬

        # 통계용 시리얼라이저로 데이터 변환 (many=True: 여러 객체를 한번에 처리)
        serializer = LabelStatsSerializer(labels_with_counts, many=True)
        return Response(serializer.data)  # JSON 형태로 응답

    # 커스텀 액션: 특정 라벨에 연결된 연락처들 조회
    # detail=True: 특정 라벨에 대한 액션 (URL: /labels/{id}/contacts/)
    @action(detail=True, methods=["get"])
    def contacts(self, request, pk=None):
        """
        특정 라벨의 연락처 목록 조회 API
        GET /labels/{id}/contacts/
        선택한 라벨에 연결된 모든 연락처를 반환합니다
        """
        # get_object(): URL의 pk 값으로 해당 라벨 객체를 가져옴
        label = self.get_object()
        # 다대다 관계를 통해 이 라벨과 연결된 모든 연락처 조회
        contacts = label.contacts.all()

        # 목록용 시리얼라이저로 연락처 데이터 변환
        serializer = ContactListSerializer(contacts, many=True)
        return Response(serializer.data)


# 연락처 관리를 위한 ViewSet 클래스
class ContactViewSet(viewsets.ModelViewSet):
    """
    연락처 관리 ViewSet
    - GET /contacts/: 모든 연락처 조회 (목록, 페이지네이션)
    - POST /contacts/: 새 연락처 생성
    - GET /contacts/{id}/: 특정 연락처 조회 (상세)
    - PUT /contacts/{id}/: 특정 연락처 전체 수정
    - PATCH /contacts/{id}/: 특정 연락처 부분 수정
    - DELETE /contacts/{id}/: 특정 연락처 삭제
    """
    # 기본 쿼리셋 - prefetch_related로 라벨 정보도 함께 미리 가져와서 성능 최적화
    queryset = Contact.objects.prefetch_related("labels")

    # 필터링, 검색, 정렬 기능 설정
    filter_backends = [
        DjangoFilterBackend,    # 필드별 필터링
        filters.SearchFilter,   # 텍스트 검색
        filters.OrderingFilter, # 정렬
    ]
    # 간단한 필터링 가능한 필드들
    filterset_fields = ["labels", "company"]
    # 복잡한 필터링을 위한 커스텀 필터 클래스
    filterset_class = ContactFilter
    # 페이지네이션: 목록을 페이지별로 나누어 표시
    pagination_class = CustomPageNumberPagination
    # 검색 가능한 필드들: 이름, 이메일, 전화번호, 회사명에서 검색
    search_fields = ["name", "email", "phone", "company"]
    # 정렬 가능한 필드들
    ordering_fields = ["name", "email", "phone", "created_at"]
    # 기본 정렬: 최신 생성순
    ordering = ["-created_at"]

    # 액션에 따라 다른 시리얼라이저를 사용하는 메소드
    def get_serializer_class(self):
        """
        요청 타입에 따라 적절한 시리얼라이저 선택
        - list 액션 (목록 조회): 간소화된 ContactListSerializer 사용
        - 나머지 액션 (상세, 생성, 수정): 전체 정보가 포함된 ContactSerializer 사용
        """
        if self.action == "list":  # GET /contacts/ (목록)
            return ContactListSerializer  # 빠른 로딩을 위한 간소화 버전
        return ContactSerializer  # GET /contacts/{id}/, POST, PUT, PATCH (상세)

    # 동적 쿼리셋 생성 메소드: 요청 파라미터에 따라 다른 데이터를 반환
    def get_queryset(self):
        """
        요청 파라미터에 따라 필터링된 연락처 목록을 반환
        지원하는 파라미터:
        - has_email: true/false (이메일이 있는/없는 연락처만)
        - has_birthday: true/false (생일이 있는/없는 연락처만)
        """
        # 기본 쿼리셋 (라벨 정보 미리 로드)
        queryset = Contact.objects.prefetch_related("labels")

        # 이메일 유무로 필터링: ?has_email=true 또는 ?has_email=false
        has_email = self.request.query_params.get("has_email")
        if has_email is not None:
            if has_email.lower() == "true":
                # 이메일이 NULL이 아니고 빈 문자열도 아닌 연락처만
                queryset = queryset.filter(email__isnull=False).exclude(email="")
            else:
                # 이메일이 NULL이거나 빈 문자열인 연락처만 (Q 객체로 OR 조건)
                queryset = queryset.filter(Q(email__isnull=True) | Q(email=""))

        # 생일 유무로 필터링: ?has_birthday=true 또는 ?has_birthday=false
        has_birthday = self.request.query_params.get("has_birthday")
        if has_birthday is not None:
            if has_birthday.lower() == "true":
                # 생일이 NULL이 아닌 연락처만
                queryset = queryset.filter(birthday__isnull=False)
            else:
                # 생일이 NULL인 연락처만
                queryset = queryset.filter(birthday__isnull=True)

        return queryset

    # 커스텀 액션: 이번 달 생일인 연락처들 조회
    @action(detail=False, methods=["get"])
    def birthdays_this_month(self, request):
        """
        이번 달 생일인 연락처 목록 조회 API
        GET /contacts/birthdays_this_month/
        현재 달과 같은 월에 생일인 연락처들을 반환합니다
        """
        # datetime 모듈에서 현재 날짜/시간 가져오기
        from datetime import datetime

        now = datetime.now()  # 현재 날짜와 시간
        # birthday 필드의 월(month)이 현재 월과 같고, 생일이 NULL이 아닌 연락처들 조회
        contacts = Contact.objects.filter(
            birthday__month=now.month,      # 생일의 월이 현재 월과 같음
            birthday__isnull=False         # 생일이 NULL이 아님
        ).prefetch_related("labels")       # 라벨 정보도 함께 조회 (성능 최적화)

        # 목록용 시리얼라이저로 데이터 변환
        serializer = ContactListSerializer(contacts, many=True)
        return Response(serializer.data)

    # 커스텀 액션: 연락처 통계 정보 조회
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """
        연락처 통계 정보 조회 API
        GET /contacts/statistics/
        전체 연락처, 이메일/전화번호/생일 보유 연락처 수, 회사 수 등의 통계를 반환합니다
        """
        # 각종 통계 정보를 딕셔너리로 구성
        stats = {
            # 전체 연락처 수
            "total_contacts": Contact.objects.count(),
            
            # 이메일이 있는 연락처 수 (NULL이 아니고 빈 문자열도 아님)
            "with_email": Contact.objects.filter(email__isnull=False)
            .exclude(email="")
            .count(),
            
            # 전화번호가 있는 연락처 수
            "with_phone": Contact.objects.filter(phone__isnull=False)
            .exclude(phone="")
            .count(),
            
            # 생일이 등록된 연락처 수
            "with_birthday": Contact.objects.filter(birthday__isnull=False).count(),
            
            # 서로 다른 회사 수 (중복 제거)
            "companies": Contact.objects.filter(company__isnull=False)
            .exclude(company="")        # 회사가 있는 연락처만
            .values("company")          # 회사명만 선택
            .distinct()                # 중복 제거
            .count(),                  # 개수 세기
        }
        return Response(stats)  # JSON으로 통계 정보 반환

    # 커스텀 액션: 연락처에 라벨 추가
    @action(detail=True, methods=["post"])
    def add_labels(self, request, pk=None):
        """
        특정 연락처에 라벨 추가 API
        POST /contacts/{id}/add_labels/
        요청 본문: {"label_ids": [1, 2, 3]}
        지정한 라벨들을 연락처에 추가합니다 (기존 라벨은 유지)
        """
        # URL의 pk로 연락처 객체 가져오기
        contact = self.get_object()
        # 요청 데이터에서 라벨 ID 목록 추출
        label_ids = request.data.get("label_ids", [])

        # 라벨 ID가 제공되지 않은 경우 에러 응답
        if not label_ids:
            return Response(
                {"error": "label_ids가 필요합니다."}, 
                status=status.HTTP_400_BAD_REQUEST  # 400 Bad Request
            )

        # 제공된 ID들로 라벨 객체들 조회
        labels = Label.objects.filter(id__in=label_ids)
        # 다대다 관계에 라벨들 추가 (*labels: 리스트를 개별 인자로 전개)
        contact.labels.add(*labels)

        # 업데이트된 연락처 정보를 시리얼라이저로 변환해서 응답
        serializer = self.get_serializer(contact)
        return Response(serializer.data)

    # 커스텀 액션: 연락처에서 라벨 제거
    @action(detail=True, methods=["post"])
    def remove_labels(self, request, pk=None):
        """
        특정 연락처에서 라벨 제거 API
        POST /contacts/{id}/remove_labels/
        요청 본문: {"label_ids": [1, 2, 3]}
        지정한 라벨들을 연락처에서 제거합니다
        """
        # URL의 pk로 연락처 객체 가져오기
        contact = self.get_object()
        # 요청 데이터에서 라벨 ID 목록 추출
        label_ids = request.data.get("label_ids", [])

        # 라벨 ID가 제공되지 않은 경우 에러 응답
        if not label_ids:
            return Response(
                {"error": "label_ids가 필요합니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 제공된 ID들로 라벨 객체들 조회
        labels = Label.objects.filter(id__in=label_ids)
        # 다대다 관계에서 라벨들 제거
        contact.labels.remove(*labels)

        # 업데이트된 연락처 정보를 시리얼라이저로 변환해서 응답
        serializer = self.get_serializer(contact)
        return Response(serializer.data)
