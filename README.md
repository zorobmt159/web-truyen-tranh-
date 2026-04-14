# 📚 Web Truyện Tranh Online

> Ứng dụng web đọc và quản lý truyện tranh được xây dựng bằng Django

---

## 🚀 Demo

👉 (https://web-truyen-tranh-71qx.onrender.com/)

---

## 🎯 Tính năng

* 📖 Đọc truyện tranh trực tuyến
* ❤️ Theo dõi (follow) truyện yêu thích
* 🔍 Tìm kiếm theo thể loại (tags)
* 🔥 Xem truyện hot & bảng xếp hạng
* 👤 Đăng ký / đăng nhập người dùng
* 💎 Hệ thống gói dịch vụ (Free / Pro / Premium)
* 🖼️ Upload & quản lý ảnh bìa

---

## 🛠️ Công nghệ sử dụng

| Thành phần | Công nghệ             |
| ---------- | --------------------- |
| Backend    | Django 4.x, Python 3  |
| Database   | SQLite (dev)          |
| Frontend   | HTML, CSS, JavaScript |
| Static     | WhiteNoise            |
| Deploy     | Heroku                |
| Media      | Django ImageField     |

---

## ⚙️ Cài đặt

### 1. Clone project

```bash
git clone https://github.com/your-username/web-truyen-tranh.git
cd web-truyen-tranh
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux / Mac
```

### 3. Cài thư viện

```bash
pip install -r requirements.txt
```

### 4. Migrate database

```bash
python manage.py migrate
```

### 5. Tạo tài khoản admin

```bash
python manage.py createsuperuser
```

### 6. Chạy server

```bash
python manage.py runserver
```

👉 Truy cập: http://127.0.0.1:8000/

---

## 🗄️ Thiết kế database

### Các model chính

* **Comic**

  * title
  * description
  * cover_image
  * tags
  * views

* **Chapter**

  * comic (FK)
  * title
  * nội dung / ảnh
  * created_at

* **Tag**

  * name

* **User**

  * loại tài khoản
  * danh sách truyện theo dõi

---

## 🧠 Kiến trúc

```
Django (MVC Pattern)

Models     → Database
Views      → Xử lý logic
Templates  → Giao diện
```

---

## 📦 Triển khai (Deploy)

Sử dụng Heroku:

```bash
git push heroku main
```

Lưu ý:

* DEBUG = False
* Cấu hình ALLOWED_HOSTS
* Có file Procfile

---

## 🖼️ Hình ảnh

👉 

---

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh. Hãy tạo issue trước khi gửi pull request lớn.

---

## 📄 License

MIT License
