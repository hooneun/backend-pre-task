# django-filter 라이브러리를 가져옵니다 (고급 필터링 기능 제공)
import django_filters
# 현재 앱의 모델들을 가져옵니다
from .models import Contact, Label


# 연락처 모델용 커스텀 필터 클래스
class ContactFilter(django_filters.FilterSet):
    """
    연락처 모델에 대한 고급 필터링 기능을 제공하는 클래스
    Django REST Framework의 DjangoFilterBackend와 함께 사용되어 API에서 다양한 방식으로 연락처를 필터링할 수 있게 합니다
    """
    
    # 이름 필드 필터: 부분 일치 검색 (대소문자 무시)
    # icontains: case-insensitive contains (예: ?name=김 -> "김민수" 찾음)
    name = django_filters.CharFilter(lookup_expr="icontains")
    
    # 이메일 필드 필터: 부분 일치 검색
    # 예: ?email=gmail -> "test@gmail.com" 찾음
    email = django_filters.CharFilter(lookup_expr="icontains")
    
    # 회사명 필드 필터: 부분 일치 검색
    # 예: ?company=네이버 -> "네이버 주식회사" 찾음
    company = django_filters.CharFilter(lookup_expr="icontains")
    
    # 생성일 이후 필터: 지정한 날짜 이후에 생성된 연락처들만
    # gte: greater than or equal (이상)
    # 예: ?created_after=2024-01-01T00:00:00Z
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",        # 연락처 모델의 created_at 필드를 대상으로
        lookup_expr="gte"              # greater than or equal 조건
    )
    
    # 생성일 이전 필터: 지정한 날짜 이전에 생성된 연락처들만
    # lte: less than or equal (이하)
    # 예: ?created_before=2024-12-31T23:59:59Z
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",        # 연락처 모델의 created_at 필드를 대상으로
        lookup_expr="lte"               # less than or equal 조건
    )
    
    # 생일 월 필터: 특정 월에 생일인 연락처들만
    # birthday__month: birthday 필드의 월 부분만 추출 (예: 3월 -> 3)
    # 예: ?birthday_month=3 -> 3월에 생일인 사람들
    birthday_month = django_filters.NumberFilter(field_name="birthday__month")
    
    # 라벨 필터: 여러 라벨을 동시에 선택하여 필터링 가능
    # 예: ?labels=1&labels=2 -> ID가 1 또는 2인 라벨이 연결된 연락처들
    labels = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all())

    class Meta:
        model = Contact  # 이 필터가 적용될 모델
        
        # 기본 필터들: 간단한 필터링 옵션들 정의
        # 위에서 정의한 커스텀 필터 외에도 기본적인 필터링 옵션들 제공
        fields = {
            "name": ["exact", "icontains"],      # 정확히 일치 또는 부분 일치
            "email": ["exact", "icontains"],     # 예: ?name=김민수 (exact), ?name__icontains=김 (contains)
            "phone": ["exact", "icontains"],     # 전화번호 정확 일치 또는 부분 일치
            "company": ["exact", "icontains"],   # 회사명 정확 일치 또는 부분 일치
        }
