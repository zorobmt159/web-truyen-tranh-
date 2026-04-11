import os
import django
import requests
import time
from datetime import datetime
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from blog.models import Comic, Chapter, Tag

def get_cover(title):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
        res = requests.get(url, timeout=10).json()
        if 'data' in res and res['data'] and res['data'][0]['images']['jpg']:
            return res['data'][0]['images']['jpg']['image_url']
        return "https://picsum.photos/300/400"
    except:
        return "https://picsum.photos/300/400"

def run_seed():
    print("---↓ Đang nạp dữ liệu truyện lên Render ---")
    if Comic.objects.exists():
        print("✅ Dữ liệu đã tồn tại, bỏ qua bước này.")
        return

    comics_data = [
        {"title": "One Piece", "description": "Hành trình tìm kiếm kho báu.", "tags": ["Phiêu lưu", "Hành động"]},
        {"title": "Naruto", "description": "Hành trình trở thành Hokage.", "tags": ["Ninja", "Hành động"]},
        # ... (Bạn có thể copy đủ 20 bộ truyện vào đây)
        {"title": "Vinland Saga", "description": "Sử thi Viking.", "tags": ["Lịch sử", "Hành động"]}
    ]

    for i, data in enumerate(comics_data):
        tag_objs = [Tag.objects.get_or_create(name=t)[0] for t in data['tags']]
        comic = Comic.objects.create(
            title=data['title'],
            description=data['description'],
            views=1000 + i * 10,
            likes=500 + i * 5
        )
        comic.tags.set(tag_objs)
        
        # Nạp 3 chapter mẫu
        for chap_num in range(1, 4):
            Chapter.objects.create(comic=comic, chapter_number=chap_num, title=f"Chương {chap_num}")

        # Tải ảnh bìa
        try:
            img_url = get_cover(data['title'])
            resp = requests.get(img_url, timeout=10)
            if resp.status_code == 200:
                fname = f"{data['title'].replace(' ', '_')}.jpg"
                comic.cover_image.save(fname, SimpleUploadedFile(fname, resp.content), save=True)
                print(f"✅ Đã xong: {data['title']}")
        except:
            print(f"❌ Lỗi ảnh: {data['title']}")
        time.sleep(1)

if __name__ == "__main__":
    run_seed()
