import os, django, requests, time
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from blog.models import Comic, Chapter, Tag

def get_cover(title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
        res = requests.get(url, timeout=10).json()
        if res.get('data') and res['data'][0]['images']['jpg']:
            return res['data'][0]['images']['jpg']['image_url']
    except:
        pass
    return None

def run():
    if Comic.objects.count() > 0:
        print("✅ Đã có data, bỏ qua.")
        return

    # Xóa data cũ nếu có
    Chapter.objects.all().delete()
    Comic.objects.all().delete()
    Tag.objects.all().delete()

    comics_data = [
        {"title": "One Piece",           "description": "Hành trình tìm kiếm kho báu huyền thoại.",           "tags": ["Phiêu lưu","Hành động"]},
        {"title": "Naruto",              "description": "Hành trình trở thành Hokage của cậu bé ninja.",       "tags": ["Ninja","Hành động"]},
        {"title": "Bleach",              "description": "Cuộc chiến của các Tử thần.",                         "tags": ["Siêu nhiên","Hành động"]},
        {"title": "Dragon Ball",         "description": "Bảy viên ngọc rồng và những trận chiến vũ trụ.",      "tags": ["Chiến đấu","Phiêu lưu"]},
        {"title": "Attack on Titan",     "description": "Cuộc chiến sinh tồn trước người khổng lồ.",           "tags": ["Hành động","Kinh dị"]},
        {"title": "Jujutsu Kaisen",      "description": "Chiến đấu với những lời nguyền độc ác.",               "tags": ["Siêu nhiên","Hành động"]},
        {"title": "My Hero Academia",    "description": "Thế giới của những siêu anh hùng.",                   "tags": ["Siêu anh hùng","Học đường"]},
        {"title": "Chainsaw Man",        "description": "Thợ săn quỷ với sức mạnh quỷ cưa.",                   "tags": ["Kinh dị","Hành động"]},
        {"title": "Spy x Family",        "description": "Gia đình giả tưởng của điệp viên và sát thủ.",        "tags": ["Hài hước","Hành động"]},
        {"title": "Demon Slayer",        "description": "Kiếm sĩ diệt quỷ cứu em gái.",                        "tags": ["Siêu nhiên","Hành động"]},
        {"title": "Tokyo Revengers",     "description": "Du hành thời gian thay đổi số phận băng đảng.",       "tags": ["Hành động","Du hành"]},
        {"title": "Death Note",          "description": "Cuốn sổ tử thần và cuộc đấu trí đỉnh cao.",           "tags": ["Tâm lý","Siêu nhiên"]},
        {"title": "Fullmetal Alchemist", "description": "Anh em giả kim thuật sư tìm lại cơ thể.",             "tags": ["Giả tưởng","Phiêu lưu"]},
        {"title": "Hunter x Hunter",     "description": "Kỳ thi thợ săn và những chuyến phiêu lưu.",           "tags": ["Phiêu lưu","Hành động"]},
        {"title": "Black Clover",        "description": "Cậu bé không phép thuật muốn làm Vua pháp sư.",       "tags": ["Giả tưởng","Phép thuật"]},
        {"title": "Blue Lock",           "description": "Dự án đào tạo tiền đạo số 1 thế giới.",               "tags": ["Thể thao","Bóng đá"]},
        {"title": "Haikyuu!!",           "description": "Đam mê bóng chuyền bất tận.",                         "tags": ["Thể thao","Học đường"]},
        {"title": "Sword Art Online",    "description": "Mắc kẹt trong thế giới game thực tế ảo.",             "tags": ["Game","Hành động"]},
        {"title": "One Punch Man",       "description": "Anh hùng đấm phát chết luôn.",                        "tags": ["Hài hước","Hành động"]},
        {"title": "Vinland Saga",        "description": "Sử thi về những chiến binh Viking.",                   "tags": ["Lịch sử","Hành động"]},
    ]

    headers = {"User-Agent": "Mozilla/5.0"}

    for i, data in enumerate(comics_data):
        # Tạo tags
        tag_objs = []
        for tag_name in data['tags']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_objs.append(tag)

        # Tạo comic
        comic = Comic.objects.create(
            title=data['title'],
            description=data['description'],
            views=1000 + i * 10,
            likes=500 + i * 5,
        )
        comic.tags.set(tag_objs)

        # Tạo chapters
        for n in range(1, 4):
            Chapter.objects.create(comic=comic, chapter_number=n, title=f"Chương {n}")

        # Tải ảnh bìa từ Jikan
        try:
            image_url = get_cover(data['title'])
            print(f"📡 Đang tải ảnh: {data['title']}")
            if image_url:
                res = requests.get(image_url, headers=headers, timeout=10)
                if res.status_code == 200:
                    fname = f"{data['title'].replace(' ','_')}.jpg"
                    img_file = SimpleUploadedFile(fname, BytesIO(res.content).read(), content_type="image/jpeg")
                    comic.cover_image.save(fname, img_file, save=True)
                    print(f"✅ {data['title']}")
                else:
                    print(f"❌ Lỗi ảnh {data['title']}: {res.status_code}")
            else:
                print(f"⚠️ Không lấy được ảnh: {data['title']}")
        except Exception as e:
            print(f"⚠️ {data['title']}: {e}")

        time.sleep(1)  # Tránh Jikan rate limit

    print(f"\n✨ Xong! Đã tạo {Comic.objects.count()} bộ truyện.")

run()
