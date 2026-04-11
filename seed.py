import os
import django
import asyncio
import requests
import time
from datetime import datetime
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from asgiref.sync import sync_to_async

# --- Setup môi trường Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from blog.models import Comic, Chapter, Tag

# --- Hàm hỗ trợ lấy ảnh bìa ---
def get_cover(title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
        res = requests.get(url, timeout=10).json()
        if 'data' in res and res['data'] and res['data'][0]['images']['jpg']:
            return res['data'][0]['images']['jpg']['image_url']
        return "https://picsum.photos/300/400"
    except Exception as e:
        return "https://picsum.photos/300/400"

# --- Hàm xử lý Database đồng bộ ---
def sync_db_operations(data, index):
    tag_objs = []
    for tag_name in data['tags']:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        tag_objs.append(tag)

    comic = Comic.objects.create(
        title=data['title'],
        description=data['description'],
        views=1000 + index * 10,
        likes=500 + index * 5,
        updated_at=datetime.now()
    )
    comic.tags.set(tag_objs)

    for chap_num in range(1, 4):
        Chapter.objects.create(
            comic=comic,
            chapter_number=chap_num,
            title=f"Chương {chap_num}"
        )
    return comic

# --- Hàm chính ---
async def run_seed():
    print("---↓ Đang khởi tạo dữ liệu truyện ---")
    
    # Nếu đã có truyện rồi thì không nạp nữa để tránh trùng lặp
    count = await sync_to_async(Comic.objects.count)()
    if count > 0:
        print(f"✅ Đã có {count} truyện, bỏ qua nạp dữ liệu.")
        return

    comics_data = [
        {"title": "One Piece", "description": "Hành trình tìm kiếm kho báu huyền thoại.", "tags": ["Phiêu lưu", "Hành động"]},
        {"title": "Naruto", "description": "Hành trình trở thành Hokage của cậu bé ninja.", "tags": ["Ninja", "Hành động"]},
        {"title": "Bleach", "description": "Cuộc chiến của các Tử thần.", "tags": ["Siêu nhiên", "Hành động"]},
        {"title": "Dragon Ball", "description": "Bảy viên ngọc rồng và những trận chiến vũ trụ.", "tags": ["Chiến đấu", "Phiêu lưu"]},
        {"title": "Attack on Titan", "description": "Cuộc chiến sinh tồn trước người khổng lồ.", "tags": ["Hành động", "Kinh dị"]},
        {"title": "Jujutsu Kaisen", "description": "Chiến đấu với những lời nguyền độc ác.", "tags": ["Siêu nhiên", "Hành động"]},
        {"title": "My Hero Academia", "description": "Thế giới của những siêu anh hùng.", "tags": ["Siêu anh hùng", "Học đường"]},
        {"title": "Chainsaw Man", "description": "Thợ săn quỷ với sức mạnh quỷ cưa.", "tags": ["Kinh dị", "Hành động"]},
        {"title": "Spy x Family", "description": "Gia đình giả tưởng của điệp viên và sát thủ.", "tags": ["Hài hước", "Hành động"]},
        {"title": "Demon Slayer", "description": "Kiếm sĩ diệt quỷ cứu em gái.", "tags": ["Siêu nhiên", "Hành động"]},
        {"title": "Tokyo Revengers", "description": "Du hành thời gian thay đổi số phận băng đảng.", "tags": ["Hành động", "Du hành"]},
        {"title": "Death Note", "description": "Cuốn sổ tử thần và cuộc đấu trí đỉnh cao.", "tags": ["Tâm lý", "Siêu nhiên"]},
        {"title": "Fullmetal Alchemist", "description": "Anh em giả kim thuật sư tìm lại cơ thể.", "tags": ["Giả tưởng", "Phiêu lưu"]},
        {"title": "Hunter x Hunter", "description": "Kỳ thi thợ săn và những chuyến phiêu lưu.", "tags": ["Phiêu lưu", "Hành động"]},
        {"title": "Black Clover", "description": "Cậu bé không phép thuật muốn làm Vua pháp sư.", "tags": ["Giả tưởng", "Phép thuật"]},
        {"title": "Blue Lock", "description": "Dự án đào tạo tiền đạo số 1 thế giới.", "tags": ["Thể thao", "Bóng đá"]},
        {"title": "Haikyuu!!", "description": "Đam mê bóng chuyền bất tận.", "tags": ["Thể thao", "Học đường"]},
        {"title": "Sword Art Online", "description": "Mắc kẹt trong thế giới game thực tế ảo.", "tags": ["Game", "Hành động"]},
        {"title": "One Punch Man", "description": "Anh hùng đấm phát chết luôn.", "tags": ["Hài hước", "Hành động"]},
        {"title": "Vinland Saga", "description": "Sử thi về những chiến binh Viking.", "tags": ["Lịch sử", "Hành động"]}
    ]

    headers = {"User-Agent": "Mozilla/5.0"}

    for i, data in enumerate(comics_data):
        comic = await sync_to_async(sync_db_operations)(data, i)
        title = data['title']
        try:
            image_url = get_cover(title)
            print(f"📡 Đang nạp: {title}")
            response = requests.get(image_url, headers=headers, timeout=10)
            if response.status_code == 200:
                img_temp = BytesIO(response.content)
                file_name = f"{title.replace(' ', '_')}.jpg"
                img_file = SimpleUploadedFile(file_name, img_temp.read(), content_type="image/jpeg")
                await sync_to_async(comic.cover_image.save)(file_name, img_file, save=True)
                print(f"✅ Xong: {title}")
        except Exception as e:
            print(f"⚠️ Lỗi ảnh {title}: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(run_seed())
