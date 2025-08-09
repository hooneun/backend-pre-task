# Django 앱 설정을 위한 모듈을 가져옵니다
from django.apps import AppConfig


# contacts 앱의 설정을 정의하는 클래스
class ContactsConfig(AppConfig):
    """
    contacts Django 앱의 구성 설정 클래스
    Django 프로젝트가 시작될 때 이 앱이 로드되는 방식을 정의합니다
    """

    # 기본 자동 필드 유형: BigAutoField 사용 (기본키로 64bit 정수 사용)
    # Django 3.2 이상에서 권장되는 설정
    default_auto_field = "django.db.models.BigAutoField"

    # 어플리케이션의 이름 (대상 앱의 Python 모듈 경로)
    # Django가 이 앱을 찾고 로드할 때 사용하는 경로
    name = "api.contacts"
