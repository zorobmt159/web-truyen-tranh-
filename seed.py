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
# COVER MAP (NO API)
# =========================
COVER_MAP = {
    "One Punch Man": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw8B43Q0tVmm8hUYYbfgdbFS8sG8ujruWuyg&s",
    "Vinland Saga": "https://m.media-amazon.com/images/M/MV5BNDA3MGNmZTEtMzFiMy00ZmViLThhNmQtMjQ4ZDc5MDEyN2U1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    "Sword Art Online": "https://m.media-amazon.com/images/M/MV5BN2NhYzU2NDEtYzI1NS00MjgzLThjZGUtOTYyNGJkZjZmNDdjXkEyXkFqcGc@._V1_.jpg",
    "Haikyuu!!": "https://m.media-amazon.com/images/M/MV5BYjYxMWFlYTAtYTk0YS00NTMxLWJjNTQtM2E0NjdhYTRhNzE4XkEyXkFqcGc@._V1_.jpg",
    "Blue Lock": "https://upload.wikimedia.org/wikipedia/vi/0/07/Blue_Lock_vol_1.jpg",
    "Black Clover": "https://external-preview.redd.it/black-clover-spade-arc-key-visual-v0-zwXgqkt9a79-czOpiDPRN4M7RaR3qXmGH8ZNAjvvCcM.jpg?auto=webp&s=75b449bbfe125435f9a1ffd6c5a5440e9b98826b",
    "Hunter x Hunter": "https://www.arcsystemworks.fr/wp-content/uploads/2024/10/portrait_standard_hp-1024x1536.jpg",
    "Death Note": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-CjmZOwj-fCkdyXLhM-yv0xW01kZOivg12g&s",
    "Tokyo Revengers": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSntNz5HZEGzs2m_qot7iC0IrW0CQQ5e_IosQ&s",
    "Demon Slayer": "https://m.media-amazon.com/images/M/MV5BMWU1OGEwNmQtNGM3MS00YTYyLThhYmMtN2FjYzQzNzNmNTE0XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    "Spy x Family": "https://preview.redd.it/new-key-visual-for-spy-x-family-season-3-v0-avitygppitpe1.jpeg?width=640&crop=smart&auto=webp&s=77f0824a129766f41c233af21a35122a0f89c583",
    "Chainsaw Man": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvYewwgW0fGGvU0lzTCzh7S6AkYT1rKpiYrw&s",
    "My Hero Academia": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTro8eluwxHiX2UJOZlUcodWbnK16Vi3DAFFA&s",
    "Jujutsu Kaisen": "https://m.media-amazon.com/images/M/MV5BMjBlNTExMDAtMWZjZi00MDc5LWFkMjgtZDU0ZWQ5ODk3YWY5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    "Attack on Titan": "https://m.media-amazon.com/images/M/MV5BZjliODY5MzQtMmViZC00MTZmLWFhMWMtMjMwM2I3OGY1MTRiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
    "Dragon Ball": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJaBZ0z6wAuFBzFLV4aWxsWNhNOVrQ4jfQRQ&s",
    "Bleach": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQ2UB2qNjYSqYnTOi5iQw3Wn4hV0iW8zXRVg&s",
    "Naruto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiccwKj3fabqP1EGVJgaVGN4Bvaaxdy64fTg&s",
    "One Piece": "https://upload.wikimedia.org/wikipedia/vi/9/90/One_Piece%2C_Volume_61_Cover_%28Japanese%29.jpg",
}


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

    for i, data in enumerate(comics_data):

        # TAGS
        tag_objs = []
        for t in data["tags"]:
            tag, _ = Tag.objects.get_or_create(name=t)
            tag_objs.append(tag)

        # RANDOM FAKE STATS (views + likes)
        views = (i + 1) * 1234
        likes = (i + 1) * 321

        # COMIC
        comic = Comic.objects.create(
            title=data["title"],
            description=data["description"],
            views=views,
            likes=likes,
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

            image_url = COVER_MAP.get(data["title"])

            if image_url:
                img_data = requests.get(image_url, headers=headers, timeout=10).content

                filename = f"{data['title'].replace(' ', '_')}.jpg"

                img_file = SimpleUploadedFile(
                    filename,
                    img_data,
                    content_type="image/jpeg"
                )

                comic.cover_image.save(filename, img_file, save=True)

                print(f"✅ {data['title']} (views={views}, likes={likes})")
            else:
                print(f"⚠️ No cover found for {data['title']}")

        except Exception as e:
            print(f"⚠️ {data['title']}: {e}")

        time.sleep(1)

    print(f"\n🎉 DONE: {Comic.objects.count()} comics created")


# RUN
run()
create_admin()
