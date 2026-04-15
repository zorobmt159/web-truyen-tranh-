import os
import django
import requests
import time

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

# Django setup (PHẢI ĐỨNG TRƯỚC IMPORT MODEL)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from blog.models import Comic, Chapter, Tag


# =========================
# ADMIN AUTO CREATE
# =========================
def create_admin():
    User = get_user_model()

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="123"
        )
        print("✅ Admin created")
    else:
        print("⚠️ Admin already exists")


# =========================
# GET COVER IMAGE
# =========================
def get_cover(title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
        res = requests.get(url, timeout=10).json()

        if res.get("data"):
            return res["data"][0]["images"]["jpg"]["image_url"]

    except Exception as e:
        print(f"⚠️ API error: {e}")

    return None


# =========================
# SEED DATA
# =========================
def run():
    Chapter.objects.all().delete()
    Comic.objects.all().delete()
    Tag.objects.all().delete()

    comics_data = [
        {"title": "One Piece", "description": "Hành trình tìm kho báu.", "tags": ["Phiêu lưu", "Hành động"]},
        {"title": "Naruto", "description": "Ninja trở thành Hokage.", "tags": ["Ninja", "Hành động"]},
        {"title": "Bleach", "description": "Cuộc chiến Tử thần.", "tags": ["Siêu nhiên", "Hành động"]},
        {"title": "Dragon Ball", "description": "Ngọc rồng vũ trụ.", "tags": ["Chiến đấu", "Phiêu lưu"]},
        {"title": "Attack on Titan", "description": "Chiến đấu người khổng lồ.", "tags": ["Hành động", "Kinh dị"]},
        {"title": "Jujutsu Kaisen", "description": "Lời nguyền.", "tags": ["Siêu nhiên", "Hành động"]},
        {"title": "My Hero Academia", "description": "Siêu anh hùng.", "tags": ["Siêu anh hùng", "Học đường"]},
        {"title": "Chainsaw Man", "description": "Thợ săn quỷ.", "tags": ["Kinh dị", "Hành động"]},
        {"title": "Spy x Family", "description": "Gia đình gián điệp.", "tags": ["Hài hước", "Hành động"]},
        {"title": "Demon Slayer", "description": "Diệt quỷ.", "tags": ["Siêu nhiên", "Hành động"]},
        {"title": "Tokyo Revengers", "description": "Du hành thời gian.", "tags": ["Hành động", "Du hành"]},
        {"title": "Death Note", "description": "Cuốn sổ tử thần.", "tags": ["Tâm lý", "Siêu nhiên"]},
        {"title": "Hunter x Hunter", "description": "Thợ săn.", "tags": ["Phiêu lưu", "Hành động"]},
        {"title": "Black Clover", "description": "Ma pháp sư.", "tags": ["Giả tưởng", "Phép thuật"]},
        {"title": "Blue Lock", "description": "Bóng đá.", "tags": ["Thể thao", "Bóng đá"]},
        {"title": "Haikyuu!!", "description": "Bóng chuyền.", "tags": ["Thể thao", "Học đường"]},
        {"title": "Sword Art Online", "description": "Game sinh tồn.", "tags": ["Game", "Hành động"]},
        {"title": "One Punch Man", "description": "Đấm phát chết.", "tags": ["Hài hước", "Hành động"]},
        {"title": "Vinland Saga", "description": "Viking.", "tags": ["Lịch sử", "Hành động"]},
    ]

    headers = {"User-Agent": "Mozilla/5.0"}

    for data in comics_data:

        # TAGS
        tag_objs = []
        for t in data["tags"]:
            tag, _ = Tag.objects.get_or_create(name=t)
            tag_objs.append(tag)

        # COMIC
        comic = Comic.objects.create(
            title=data["title"],
            description=data["description"],
        )
        comic.tags.set(tag_objs)

        # CHAPTERS
        for n in range(1, 4):
            Chapter.objects.create(
                comic=comic,
                chapter_number=n,
                title=f"Chương {n}"
            )

        # COVER IMAGE
        try:
            print(f"📡 {data['title']}")

            image_url = get_cover(data["title"])

            if image_url:
                img_data = requests.get(image_url, headers=headers, timeout=10).content

                filename = f"{data['title'].replace(' ', '_')}.jpg"

                img_file = SimpleUploadedFile(
                    filename,
                    img_data,
                    content_type="image/jpeg"
                )

                comic.cover_image.save(filename, img_file, save=True)

                print(f"✅ {data['title']}")

        except Exception as e:
            print(f"⚠️ {data['title']}: {e}")

        time.sleep(1)

    print(f"\n🎉 DONE: {Comic.objects.count()} comics created")


# RUN
run()
create_admin()
