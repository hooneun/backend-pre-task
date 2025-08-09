# Django REST Framework의 페이지네이션 기능을 가져옵니다
from rest_framework.pagination import PageNumberPagination  # 페이지 번호 기반 페이지네이션
from rest_framework.response import Response  # API 응답 객체


# 커스텀 페이지네이션 클래스
class CustomPageNumberPagination(PageNumberPagination):
    """
    연락처 목록 조회를 위한 커스텀 페이지네이션 클래스
    기본 PageNumberPagination을 상속받아 프로젝트에 맞게 커스터마이즈
    페이지별로 데이터를 나누어 전송하여 성능을 향상시킵니다
    """
    
    # 한 페이지당 기본 아이템 개수 (20개)
    page_size = 20
    
    # 클라이언트가 페이지 크기를 변경할 때 사용할 쿼리 파라미터 이름
    # 예: ?page_size=50 -> 한 페이지에 50개 아이템 표시
    page_size_query_param = "page_size"
    
    # 한 페이지에 표시할 수 있는 최대 아이템 개수 (서버 보호를 위한 제한)
    max_page_size = 100

    # 페이지네이션된 응답을 생성하는 메소드 (DRF 기본 형식을 커스텀)
    def get_paginated_response(self, data):
        """
        페이지네이션 메타데이터를 포함한 전용 응답 형식 생성
        기본 DRF 형식 대신 더 상세한 페이지 정보를 제공
        """
        return Response(
            {
                # 페이지네이션 전용 섹션에 모든 메타데이터를 그룹화
                "pagination": {
                    # 전체 아이템 개수 (모든 페이지를 통합한 총 개수)
                    "count": self.page.paginator.count,
                    
                    # 전체 페이지 수
                    "page_count": self.page.paginator.num_pages,
                    
                    # 현재 페이지의 아이템 개수 (마지막 페이지는 기본 크기보다 적을 수 있음)
                    "page_size": self.page_size,
                    
                    # 현재 페이지 번호 (1부터 시작)
                    "current_page": self.page.number,
                    
                    # 다음 페이지 URL (마지막 페이지인 경우 null)
                    "next": self.get_next_link(),
                    
                    # 이전 페이지 URL (첫 번째 페이지인 경우 null)
                    "previous": self.get_previous_link(),
                },
                
                # 실제 데이터 내용 (연락처 목록)
                "results": data,
            }
        )
