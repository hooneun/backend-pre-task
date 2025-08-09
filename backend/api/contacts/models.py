# Django의 유효성 검사 도구를 가져옵니다
from django.core.validators import RegexValidator
# Django의 데이터베이스 모델링 도구를 가져옵니다
from django.db import models


# 라벨 모델 정의 - 연락처를 분류하기 위한 태그 역할
class Label(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="라벨명",
        help_text="연락처 분류용 라벨명 (예: 가족, 친구, 회사)",
    )
    color_validator = RegexValidator(
        regex=r"^#[0-9A-Fa-f]{6}$", message="색상은 #FFFFFF 형식이어야 합니다."
    )
    color = models.CharField(
        max_length=7,
        default="#007bff",
        verbose_name="색상",
        help_text="라벨 색상 (HEX 코드, 예: #FF0000",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        db_table = "contract_label"
        verbose_name = "라벨"
        verbose_name_plural = verbose_name
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="이름", help_text="연락처 이름 (필수)"
    )
    email = models.EmailField(
        blank=True, null=True, verbose_name="이메일", help_text="이메일 주소 (옵션)"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="전화번호",
        help_text="전화번호 (옵션)",
    )
    company = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="회사",
        help_text="소속 회사명 (옵션)",
    )
    position = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="직책",
        help_text="회사 내 직책 (옵션)",
    )
    memo = models.TextField(
        blank=True, null=True, verbose_name="메모", help_text="연락처 메모 (옵션)"
    )
    profile_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="프로필 사진",
        help_text="프로필 사진 URL (옵션)",
    )
    address = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="주소",
        help_text="주소 (옵션)",
    )
    birthday = models.DateField(
        blank=True, null=True, verbose_name="생일", help_text="생년월일 (옵션)"
    )
    website = models.URLField(
        blank=True, null=True, verbose_name="웹사이트", help_text="웹사이트 URL (옵션)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    # 관계
    labels = models.ManyToManyField(
        Label, blank=True, verbose_name="라벨", help_text="연락처 연결 라벨"
    )

    class Meta:
        db_table = "contracts_contact"
        verbose_name = "연락처"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"], name="idx_contact_name"),
            models.Index(fields=["email"], name="idx_contact_email"),
            models.Index(fields=["phone"], name="idx_contact_phone"),
            models.Index(fields=["created_at"], name="idx_contact_created_at"),
        ]

    def __str__(self):
        return self.name

    @property
    def company_with_position(self):
        if self.company and self.position:
            return f"{self.company} ({self.position})"
        elif self.company:
            return f"{self.company}"
        elif self.position:
            return f"{self.position}"
        return ""
