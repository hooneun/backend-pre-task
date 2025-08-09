from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import LabelSerializer, ContactSerializer

from .models import Label, Contact


class LabelModelTests(TestCase):
    def test_create_label(self):
        label = Label.objects.create(name="친구", color="#ff0000")

        self.assertEqual(label.name, "친구")
        self.assertEqual(label.color, "#ff0000")
        self.assertTrue(label.created_at)
        self.assertTrue(label.updated_at)

    def test_label_str_representation(self):
        label = Label(name="가족")
        self.assertEqual(str(label), label.name)

    def test_unique_label_name(self):
        Label.objects.create(name="친구", color="#ff0000")

        with self.assertRaises(Exception):
            Label.objects.create(name="친구", color="#ff0000")


class ContactModelTest(TestCase):
    """연락처 모델 테스트"""

    def setUp(self):
        """테스트 데이터 준비"""
        self.label1 = Label.objects.create(name="가족", color="#FF0000")
        self.label2 = Label.objects.create(name="친구", color="#00FF00")

    def test_create_contact(self):
        """연락처 생성 테스트"""
        contact = Contact.objects.create(
            name="홍길동", email="hong@example.com", phone="010-1234-5678"
        )

        self.assertEqual(contact.name, "홍길동")
        self.assertEqual(contact.email, "hong@example.com")
        self.assertEqual(contact.phone, "010-1234-5678")

    def test_contact_with_labels(self):
        """라벨이 있는 연락처 테스트"""
        contact = Contact.objects.create(name="김철수")
        contact.labels.add(self.label1, self.label2)

        self.assertEqual(contact.labels.count(), 2)
        self.assertIn(self.label1, contact.labels.all())
        self.assertIn(self.label2, contact.labels.all())

    def test_company_with_position_property(self):
        """회사-직책 속성 테스트"""
        contact = Contact.objects.create(
            name="이영희", company="ABC회사", position="개발자"
        )

        self.assertEqual(contact.company_with_position, "ABC회사 (개발자)")

        # 회사만 있는 경우
        contact.position = None
        self.assertEqual(contact.company_with_position, "ABC회사")

        # 둘 다 없는 경우
        contact.company = None
        self.assertEqual(contact.company_with_position, "")


class LabelSerializerTest(APITestCase):
    """라벨 시리얼라이저 테스트"""

    def test_valid_label_serialization(self):
        """유효한 라벨 직렬화 테스트"""
        label = Label.objects.create(name="회사", color="#0000FF")
        serializer = LabelSerializer(label)

        expected_data = {
            "id": label.id,
            "name": "회사",
            "color": "#0000FF",
            "created_at": label.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": label.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

        self.assertEqual(serializer.data, expected_data)

    def test_label_deserialization(self):
        """라벨 역직렬화 테스트"""
        data = {"name": "새 라벨", "color": "#FFFF00"}

        serializer = LabelSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        label = serializer.save()
        self.assertEqual(label.name, "새 라벨")
        self.assertEqual(label.color, "#FFFF00")

    def test_invalid_color_validation(self):
        """잘못된 색상 코드 검증 테스트"""
        data = {"name": "테스트 라벨", "color": "invalid-color"}

        serializer = LabelSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("color", serializer.errors)


class ContactSerializerTest(APITestCase):
    """연락처 시리얼라이저 테스트"""

    def setUp(self):
        self.label1 = Label.objects.create(name="가족", color="#FF0000")
        self.label2 = Label.objects.create(name="친구", color="#00FF00")

    def test_contact_with_labels_serialization(self):
        """라벨이 있는 연락처 직렬화 테스트"""
        contact = Contact.objects.create(name="홍길동")
        contact.labels.add(self.label1)

        serializer = ContactSerializer(contact)
        data = serializer.data

        self.assertEqual(data["name"], "홍길동")
        self.assertEqual(len(data["labels"]), 1)
        self.assertEqual(data["labels"][0]["name"], "가족")

    def test_contact_creation_with_labels(self):
        """라벨과 함께 연락처 생성 테스트"""
        data = {
            "name": "김철수",
            "email": "kim@example.com",
            "label_ids": [self.label1.id, self.label2.id],
        }

        serializer = ContactSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        contact = serializer.save()
        self.assertEqual(contact.name, "김철수")
        self.assertEqual(contact.labels.count(), 2)


class LabelAPITest(APITestCase):
    """라벨 API 테스트"""

    def setUp(self):
        self.client = APIClient()
        self.label_data = {"name": "테스트 라벨", "color": "#FF0000"}

    def test_create_label(self):
        """라벨 생성 API 테스트"""
        url = reverse("label-list")
        response = self.client.post(url, self.label_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 1)
        self.assertEqual(Label.objects.get().name, "테스트 라벨")

    def test_get_label_list(self):
        """라벨 목록 조회 API 테스트"""
        Label.objects.create(name="라벨1", color="#FF0000")
        Label.objects.create(name="라벨2", color="#00FF00")

        url = reverse("label-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 응답 데이터 구조 확인 (페이지네이션이 적용된 경우)
        if isinstance(response.data, dict) and 'results' in response.data:
            label_names = [label['name'] for label in response.data['results']]
        else:
            label_names = [label['name'] for label in response.data]
        
        self.assertIn("라벨1", label_names)
        self.assertIn("라벨2", label_names)

    def test_get_label_detail(self):
        """라벨 상세 조회 API 테스트"""
        label = Label.objects.create(name="테스트", color="#FF0000")

        url = reverse("label-detail", kwargs={"pk": label.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "테스트")

    def test_update_label(self):
        """라벨 수정 API 테스트"""
        label = Label.objects.create(name="원본", color="#FF0000")

        url = reverse("label-detail", kwargs={"pk": label.id})
        updated_data = {"name": "수정됨", "color": "#00FF00"}
        response = self.client.put(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        label.refresh_from_db()
        self.assertEqual(label.name, "수정됨")

    def test_delete_label(self):
        """라벨 삭제 API 테스트"""
        label = Label.objects.create(name="삭제할 라벨", color="#FF0000")

        url = reverse("label-detail", kwargs={"pk": label.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Label.objects.count(), 0)


class ContactAPITest(APITestCase):
    """연락처 API 테스트"""

    def setUp(self):
        self.client = APIClient()
        self.label = Label.objects.create(name="친구", color="#FF0000")
        self.contact_data = {
            "name": "홍길동",
            "email": "hong@example.com",
            "phone": "010-1234-5678",
            "label_ids": [self.label.id],
        }

    def test_create_contact(self):
        """연락처 생성 API 테스트"""
        url = reverse("contact-list")
        response = self.client.post(url, self.contact_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)

        contact = Contact.objects.get()
        self.assertEqual(contact.name, "홍길동")
        self.assertEqual(contact.labels.count(), 1)

    def test_search_contacts(self):
        """연락처 검색 API 테스트"""
        Contact.objects.create(name="홍길동", email="hong@example.com")
        Contact.objects.create(name="김철수", email="kim@example.com")

        url = reverse("contact-list")
        response = self.client.get(url, {"search": "홍길동"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "홍길동")

    def test_filter_contacts_by_label(self):
        """라벨로 연락처 필터링 테스트"""
        contact1 = Contact.objects.create(name="홍길동")
        contact1.labels.add(self.label)

        contact2 = Contact.objects.create(name="김철수")

        url = reverse("contact-list")
        response = self.client.get(url, {"labels": self.label.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "홍길동")
