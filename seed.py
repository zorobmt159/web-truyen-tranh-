%%writefile seed.py
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from blog.models import Comic, Chapter, Tag

def run():
    if Comic.objects.count() > 0:
        print("✅ Đã có data, bỏ qua.")
        return

    data = [
        ("One Piece",           "Hành trình tìm kho báu.",              ["Phiêu lưu","Hành động"],     1200, 800),
        ("Naruto",              "Hành trình trở thành Hokage.",         ["Ninja","Hành động"],          1100, 750),
        ("Attack on Titan",     "Sinh tồn trước người khổng lồ.",       ["Hành động","Kinh dị"],        1300, 900),
        ("Jujutsu Kaisen",      "Chiến đấu với lời nguyền.",            ["Siêu nhiên","Hành động"],     1250, 870),
        ("Demon Slayer",        "Kiếm sĩ diệt quỷ cứu em gái.",        ["Siêu nhiên","Hành động"],     1180, 820),
        ("One Punch Man",       "Anh hùng đấm phát chết luôn.",         ["Hài hước","Hành động"],       1350, 950),
        ("Death Note",          "Cuốn sổ tử thần đấu trí đỉnh cao.",   ["Tâm lý","Siêu nhiên"],        1050, 730),
        ("Chainsaw Man",        "Thợ săn quỷ với sức mạnh quỷ cưa.",   ["Kinh dị","Hành động"],        1150, 780),
        ("Spy x Family",        "Gia đình giả tưởng điệp viên sát thủ.",["Hài hước","Hành động"],      980,  690),
        ("Blue Lock",           "Dự án đào tạo tiền đạo số 1 TG.",     ["Thể thao","Bóng đá"],         1400, 960),
        ("Haikyuu!!",           "Đam mê bóng chuyền bất tận.",          ["Thể thao","Học đường"],       890,  610),
        ("Vinland Saga",        "Sử thi về chiến binh Viking.",         ["Lịch sử","Hành động"],        1190, 810),
        ("Hunter x Hunter",     "Kỳ thi thợ săn phiêu lưu.",           ["Phiêu lưu","Hành động"],      970,  660),
        ("Fullmetal Alchemist", "Anh em giả kim tìm lại cơ thể.",      ["Giả tưởng","Phiêu lưu"],      920,  620),
        ("Dragon Ball",         "Bảy viên ngọc rồng vũ trụ.",          ["Chiến đấu","Phiêu lưu"],      950,  650),
        ("Bleach",              "Cuộc chiến của các Tử thần.",          ["Siêu nhiên","Hành động"],     900,  600),
        ("My Hero Academia",    "Thế giới siêu anh hùng.",             ["Siêu anh hùng","Học đường"],  1000, 700),
        ("Tokyo Revengers",     "Du hành thời gian đổi số phận.",      ["Hành động","Du hành"],        870,  580),
        ("Sword Art Online",    "Mắc kẹt trong thế giới game.",        ["Game","Hành động"],           840,  560),
        ("Black Clover",        "Cậu bé không phép muốn làm Vua.",     ["Giả tưởng","Phép thuật"],     810,  540),
    ]

    for i, (title, desc, tags, views, likes) in enumerate(data):
        tag_objs = []
        for t in tags:
            tag, _ = Tag.objects.get_or_create(name=t)
            tag_objs.append(tag)

        comic = Comic.objects.create(
            title=title, description=desc,
            views=views, likes=likes
        )
        comic.tags.set(tag_objs)

        for n in range(1, 6):
            Chapter.objects.create(
                comic=comic,
                chapter_number=n,
                title=f"Chương {n}"
            )
        print(f"✅ {title}")

    print(f"\n🎉 Đã tạo {Comic.objects.count()} bộ truyện!")

run()
