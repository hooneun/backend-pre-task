# Django REST Framework의 시리얼라이저 기능들을 가져옵니다
from rest_framework import serializers  # 기본 시리얼라이저 클래스들
from rest_framework.fields import MultipleChoiceField  # 다중 선택 필드

# 현재 앱의 데이터베이스 모델들을 가져옵니다
from .models import Label, Contact  # 라벨과 연락처 모델


# 커스텀 필드 클래스: 체크박스 형태의 다중 선택을 위한 필드
class CheckboxSelectMultipleField(MultipleChoiceField):
    """
    체크박스 형태의 다중 선택 필드
    Django REST Framework의 브라우저 API에서 라벨을 체크박스로 표시하기 위해 사용
    """

    def __init__(self, *args, **kwargs):
        # HTML 템플릿을 체크박스 형태로 설정
        kwargs["style"] = {"base_template": "checkbox_multiple.html"}
        # 부모 클래스(MultipleChoiceField)의 초기화 메소드 호출
        super().__init__(*args, **kwargs)


# 라벨 모델용 시리얼라이저 클래스
class LabelSerializer(serializers.ModelSerializer):
    """
    라벨 데이터를 JSON으로 변환하거나 JSON을 라벨 모델로 변환하는 시리얼라이저
    ModelSerializer: Django 모델을 기반으로 자동으로 필드를 생성해주는 시리얼라이저
    """

    class Meta:
        model = Label  # 이 시리얼라이저가 다룰 모델
        # JSON에 포함될 필드들 (API 응답/요청에서 사용됨)
        fields = ["id", "name", "color", "created_at", "updated_at"]
        # 읽기 전용 필드들 (API 요청 시 수정할 수 없고, 응답에만 포함됨)
        read_only_fields = ["id", "created_at", "updated_at"]


# 연락처 모델용 상세 시리얼라이저 클래스 (생성/수정/조회용)
class ContactSerializer(serializers.ModelSerializer):
    """
    연락처의 모든 정보를 다루는 시리얼라이저
    생성, 수정, 상세 조회 시에 사용됩니다
    """

    # 모델의 @property 메소드를 읽기 전용 필드로 추가
    company_with_position = serializers.ReadOnlyField()

    # 연결된 라벨들을 중첩된 시리얼라이저로 표시 (읽기 전용)
    # many=True: 여러 개의 라벨 객체를 처리
    labels = LabelSerializer(many=True, read_only=True)

    # 라벨 연결을 위한 별도의 쓰기 전용 필드
    # 체크박스 형태로 여러 라벨을 선택할 수 있게 함
    label_ids = CheckboxSelectMultipleField(
        choices=[],  # 선택지는 __init__에서 동적으로 설정
        write_only=True,  # API 요청 시에만 사용, 응답에는 포함안됨
        required=False,  # 선택사항 (라벨을 안 선택해도 됨)
        help_text="연결할 라벨들의 ID 목록",
    )

    class Meta:
        model = Contact  # 이 시리얼라이저가 다룰 모델
        # API에서 사용할 모든 필드들 정의
        fields = [
            "id",  # 기본키 (자동생성)
            "name",  # 이름 (필수)
            "email",  # 이메일
            "phone",  # 전화번호
            "company",  # 회사명
            "position",  # 직책
            "memo",  # 메모
            "profile_url",  # 프로필 사진 URL
            "address",  # 주소
            "birthday",  # 생일
            "website",  # 웹사이트
            "labels",  # 연결된 라벨들 (읽기 전용, 중첩 객체)
            "label_ids",  # 라벨 ID 목록 (쓰기 전용)
            "company_with_position",  # 회사+직책 조합 (읽기 전용)
            "created_at",  # 생성일시
            "updated_at",  # 수정일시
        ]
        # 읽기 전용 필드들 (수정 불가)
        read_only_fields = ["id", "created_at", "updated_at"]

    # 시리얼라이저 초기화 메소드
    def __init__(self, *args, **kwargs):
        """
        시리얼라이저 인스턴스 생성 시 실행되는 초기화 메소드
        라벨 선택지를 동적으로 설정하기 위해 오버라이드
        """
        # 부모 클래스의 초기화 메소드 먼저 호출
        super().__init__(*args, **kwargs)

        # 데이터베이스에서 모든 라벨을 가져와서 선택지로 설정
        labels = Label.objects.all()
        # label_ids 필드의 choices를 동적으로 생성
        # 각 라벨의 ID를 값으로, "라벨명 (색상)" 형태를 표시명으로 사용
        self.fields["label_ids"].choices = [
            (label.id, f"{label.name} ({label.color})") for label in labels
        ]

    # 새 연락처 생성 메소드 (POST 요청 처리)
    def create(self, validated_data):
        """
        검증된 데이터로 새 연락처를 생성합니다
        라벨 연결 처리를 위해 커스텀 구현
        """
        # label_ids는 연락처 모델에 직접 저장할 수 없으므로 분리
        label_ids = validated_data.pop("label_ids", [])

        # MultipleChoiceField에서 받은 문자열 값들을 정수로 변환
        label_ids = [int(id) for id in label_ids] if label_ids else []

        # 라벨 정보를 제외한 나머지 데이터로 연락처 객체 생성
        # **validated_data: 딕셔너리를 키워드 인자로 전개
        contact = Contact.objects.create(**validated_data)

        # 라벨 ID가 제공된 경우 다대다 관계 설정
        if label_ids:
            # 해당 ID들의 라벨 객체들을 조회
            labels = Label.objects.filter(id__in=label_ids)
            # 다대다 관계 필드에 라벨들을 설정 (기존 것들은 교체됨)
            contact.labels.set(labels)

        return contact

    # 기존 연락처 수정 메소드 (PUT/PATCH 요청 처리)
    def update(self, instance, validated_data):
        """
        기존 연락처를 수정합니다
        라벨 연결 업데이트를 위해 커스텀 구현
        """
        # label_ids 데이터를 분리 (None이면 라벨을 수정하지 않음)
        label_ids = validated_data.pop("label_ids", None)

        # 문자열로 받은 ID들을 정수로 변환
        if label_ids is not None:
            label_ids = [int(id) for id in label_ids] if label_ids else []

        # 연락처의 일반 필드들을 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # instance.attr = value와 동일
        instance.save()  # 데이터베이스에 변경사항 저장

        # 라벨 ID가 제공된 경우에만 라벨 관계 업데이트
        if label_ids is not None:
            # 해당 ID들의 라벨 객체들 조회
            labels = Label.objects.filter(id__in=label_ids)
            # 기존 라벨 관계를 모두 지우고 새로운 라벨들로 설정
            instance.labels.set(labels)

        return instance


# 연락처 목록 조회용 간소화된 시리얼라이저 클래스
class ContactListSerializer(serializers.ModelSerializer):
    """
    연락처 목록용 간소화된 시리얼라이저
    목록 조회 시 필요한 핵심 정보만 포함하여 응답 속도를 향상시킵니다
    메모, 주소, 생일, 웹사이트 등 상세 정보는 제외
    """

    # 회사명과 직책을 조합한 읽기 전용 필드
    company_with_position = serializers.ReadOnlyField()

    # 연결된 라벨들을 중첩 객체로 표시
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        # 목록에서 표시할 핵심 필드들만 포함
        fields = [
            "id",  # 식별자
            "name",  # 이름
            "email",  # 이메일
            "phone",  # 전화번호
            "company",  # 회사명
            "position",  # 직책
            "profile_url",  # 프로필 사진
            "labels",  # 라벨들
            "company_with_position",  # 회사+직책 조합
        ]


# 라벨 통계 정보용 시리얼라이저 클래스
class LabelStatsSerializer(serializers.ModelSerializer):
    """
    라벨 통계 정보용 시리얼라이저
    각 라벨에 연결된 연락처 개수 정보를 포함합니다
    ViewSet의 stats 액션에서 사용됩니다
    """

    # annotate()로 추가된 가상 필드를 정수 필드로 정의
    # read_only=True: 계산된 값이므로 읽기 전용
    contact_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Label
        # 통계에 필요한 라벨 기본 정보 + 연락처 개수
        fields = ["id", "name", "color", "contact_count"]
