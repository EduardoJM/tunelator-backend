import os
from io import BytesIO
from PIL import Image
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from authentication.models import User
from content.models import SocialContent

class SocialContentAPITestCase(APITestCase):
    url = reverse('content:SocialContent-list')

    def setUp(self):
        self.email = 'example@example.com.br'
        self.password = 'any password'
        self.first_name = 'First'
        self.last_name = 'Last'
        self.first_user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )

        self.access = str(AccessToken.for_user(self.first_user))
        self.bearer = "Bearer %s" % self.access
    
    def temporary_image(self):
        bts = BytesIO()
        img = Image.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile("test.jpg", bts.getvalue())

    def test_list_content_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        
        response = self.client.get(self.url)

        self.assertEqual(401, response.status_code)
        self.assertTrue("detail" in response.json())

    def test_list_content_without_any_content(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.bearer)

        response = self.client.get(self.url)

        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue("count" in data)
        self.assertTrue("next" in data)
        self.assertTrue("previous" in data)
        self.assertTrue("results" in data)
        self.assertEqual(0, data["count"])
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])
        self.assertEqual([], data["results"])

    def create_content(self, title, link, desc, image=None):
        return SocialContent.objects.create(
            title=title,
            link=link,
            description=desc,
            image=image
        )

    def test_list_content_order(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.bearer)

        content1 = self.create_content("first title", "https://www.google.com/", "any text")
        content2 = self.create_content("second title", "https://www.google.com/", "any text")
        content3 = self.create_content("last title", "https://www.google.com/", "any text")

        id1 = content1.pk
        id2 = content2.pk
        id3 = content3.pk

        response = self.client.get(self.url)

        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue("count" in data)
        self.assertTrue("results" in data)
        self.assertEqual(3, data["count"])

        ids = [x["id"] for x in data["results"]]
        self.assertEqual(ids[0], id3)
        self.assertEqual(ids[1], id2)
        self.assertEqual(ids[2], id1)

        content1.delete()
        content2.delete()
        content3.delete()

    def test_list_content_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.bearer)

        content = self.create_content("first title", "https://www.google.com/", "any text", self.temporary_image())

        response = self.client.get(self.url)

        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue("count" in data)
        self.assertTrue("results" in data)
        self.assertEqual(1, data["count"])

        item = data["results"][0]
        self.assertEqual(item["title"], content.title)
        self.assertEqual(item["link"], content.link)
        self.assertEqual(item["description"], content.description)
        self.assertTrue(str(item["image"]).endswith(content.image.url))

        try:
            os.remove(content.image.path)
        except Exception:
            pass
        content.delete()

    def test_list_limit_pagination(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.bearer)

        content1 = self.create_content("first title", "https://www.google.com/", "any text")
        content2 = self.create_content("second title", "https://www.google.com/", "any text")
        content3 = self.create_content("last title", "https://www.google.com/", "any text")
        content4 = self.create_content("ha title", "https://www.google.com/", "any text")
        id1 = content1.pk
        id2 = content2.pk
        id3 = content3.pk
        id4 = content4.pk

        response = self.client.get(self.url, { 'limit': 2 })

        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue("count" in data)
        self.assertTrue("results" in data)
        self.assertEqual(4, data["count"])
        self.assertEqual(2, len(data["results"]))

        ids = [x["id"] for x in data["results"]]
        self.assertEqual(ids[0], id4)
        self.assertEqual(ids[1], id3)

        response = self.client.get(self.url, { 'limit': 2, 'offset': 2 })

        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue("count" in data)
        self.assertTrue("results" in data)
        self.assertEqual(4, data["count"])
        self.assertEqual(2, len(data["results"]))

        ids = [x["id"] for x in data["results"]]
        self.assertEqual(ids[0], id2)
        self.assertEqual(ids[1], id1)

        content1.delete()
        content2.delete()
        content3.delete()
        content4.delete()
