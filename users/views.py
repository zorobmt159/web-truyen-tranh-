from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from blog.models import Comic, UserProfile, Subscription, Tag
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

VALID_COUPONS = {'WELCOME99': 99}  # code: % giảm

def get_sidebar_data():
    all_comics = Comic.objects.all()
    top_month = all_comics.order_by('-views')[:5]
    all_tags = Tag.objects.all().order_by('name')
    recent = all_comics.filter(updated_at__gte=timezone.now() - timedelta(days=7))
    top_week = sorted(recent, key=lambda c: c.views, reverse=True)[:5] or list(top_month)
    today_comics = all_comics.filter(updated_at__date=timezone.now().date())
    top_day = sorted(today_comics, key=lambda c: c.views, reverse=True)[:5] or list(top_week)
    return {'top_month': top_month, 'top_week': top_week, 'top_day': top_day, 'all_tags': all_tags}

# --- TRANG CHỦ ---
def home(request):
    show_coupon = False
    if request.user.is_authenticated and request.session.pop('show_coupon_popup', False):
        show_coupon = True
    comics = Comic.objects.all().order_by('-updated_at')
    ctx = {'comics': comics, 'show_coupon_popup': show_coupon}
    ctx.update(get_sidebar_data())
    return render(request, 'users/home.html', ctx)

# --- HOT ---
def hot_comics(request):
    ctx = {'comics': Comic.objects.all().order_by('-views')[:20]}
    ctx.update(get_sidebar_data())
    return render(request, 'users/hot_comics.html', ctx)

# --- XẾP HẠNG ---
def ranking(request):
    rank_type = request.GET.get('type', 'view')
    if rank_type == 'like':
        qs = Comic.objects.order_by('-likes')[:30]
    elif rank_type == 'chapter':
        qs = sorted(Comic.objects.all(), key=lambda c: c.chapters.count(), reverse=True)[:30]
    elif rank_type == 'month':
        qs = Comic.objects.order_by('-views')[:30]
    elif rank_type == 'week':
        since = timezone.now() - timedelta(days=7)
        qs = sorted(Comic.objects.filter(updated_at__gte=since), key=lambda c: c.views, reverse=True)[:30]
    else:
        qs = Comic.objects.order_by('-views')[:30]
    ctx = {'ranked_comics': qs, 'rank_type': rank_type}
    ctx.update(get_sidebar_data())
    return render(request, 'users/ranking.html', ctx)

# --- THỂ LOẠI ---
def genre_list(request, tag_name=None):
    tags = Tag.objects.all().order_by('name')
    comics = Comic.objects.all().order_by('-updated_at')
    selected_tag = None
    if tag_name:
        selected_tag = get_object_or_404(Tag, name=tag_name)
        comics = comics.filter(tags=selected_tag)
    ctx = {'tags': tags, 'comics': comics, 'selected_tag': selected_tag}
    ctx.update(get_sidebar_data())
    return render(request, 'users/the_loai.html', ctx)

# --- CHI TIẾT TRUYỆN ---
def comic_detail(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    comic.views += 1
    comic.save()
    chapters = comic.chapters.all().order_by('chapter_number')
    ctx = {'comic': comic, 'chapters': chapters}
    ctx.update(get_sidebar_data())
    return render(request, 'users/manga_detail.html', ctx)

# --- THEO DÕI ---
@login_required
def toggle_follow(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    if request.user in comic.followers.all():
        comic.followers.remove(request.user)
    else:
        comic.followers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def followed_comics(request):
    comics = request.user.followed_comics.all().order_by('-updated_at')
    ctx = {'comics': comics}
    ctx.update(get_sidebar_data())
    return render(request, 'users/followed_comics.html', ctx)

# --- TÌM KIẾM ---
def search_results(request):
    query = request.GET.get('q', '').strip()
    results = Comic.objects.filter(
        Q(title__icontains=query)|Q(description__icontains=query)|Q(tags__name__icontains=query)
    ).distinct().order_by('-created_at') if query else []
    ctx = {'query': query, 'results': results}
    ctx.update(get_sidebar_data())
    return render(request, 'users/search_results.html', ctx)

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    if query:
        comics = Comic.objects.filter(title__icontains=query)[:5]
        data = [{'pk': c.pk, 'title': c.title, 'cover_url': c.cover_image.url if c.cover_image else None, 'latest_chapter': c.latest_chapter_number or '?'} for c in comics]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

# --- USER ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            Subscription.objects.get_or_create(user=user)
            login(request, user)
            request.session['show_coupon_popup'] = True  # trigger popup
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    prof, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': prof})

@login_required
def pricing(request):
    sub, _ = Subscription.objects.get_or_create(user=request.user)
    prof, _ = UserProfile.objects.get_or_create(user=request.user)
    current_plan = sub.plan
    features = [
        {'name': 'Đọc truyện miễn phí',      'free': '✅', 'pro': '✅', 'premium': '✅'},
        {'name': 'Tìm kiếm không giới hạn',   'free': '✅', 'pro': '✅', 'premium': '✅'},
        {'name': 'Ẩn quảng cáo',              'free': '❌', 'pro': '✅', 'premium': '✅'},
        {'name': 'Đọc sớm chapter mới',       'free': '❌', 'pro': '✅', 'premium': '✅'},
        {'name': 'Bookmark không giới hạn',   'free': '❌', 'pro': '✅', 'premium': '✅'},
        {'name': 'Tải chapter offline',        'free': '❌', 'pro': '❌', 'premium': '✅'},
        {'name': 'Đọc trước 7 ngày',          'free': '❌', 'pro': '❌', 'premium': '✅'},
        {'name': 'Hỗ trợ ưu tiên 24/7',      'free': '❌', 'pro': '❌', 'premium': '✅'},
    ]
    ctx = {'current_plan': current_plan, 'features': features, 'subscription': sub}
    ctx.update(get_sidebar_data())
    return render(request, 'users/pricing.html', ctx)

@login_required
def checkout(request, plan):
    if plan not in ('pro', 'premium'):
        return redirect('pricing')
    price = 49000 if plan == 'pro' else 99000
    ctx = {'plan': plan, 'price': price}
    ctx.update(get_sidebar_data())
    return render(request, 'users/checkout.html', ctx)

@login_required
def confirm_payment(request):
    if request.method == 'POST':
        plan = request.POST.get('plan')
        coupon = request.POST.get('coupon', '').strip().upper()
        if plan in ('pro', 'premium'):
            sub, _ = Subscription.objects.get_or_create(user=request.user)
            prof, _ = UserProfile.objects.get_or_create(user=request.user)
            sub.plan = plan
            sub.started_at = timezone.now()
            sub.expires_at = timezone.now() + timedelta(days=30)
            sub.is_active = True
            sub.save()
            prof.plan = plan
            prof.plan_expires_at = sub.expires_at
            prof.save()
            messages.success(request, f'🎉 Nâng cấp {plan.upper()} thành công! Cảm ơn bạn.')
    return redirect('pricing')

@login_required
def cancel_subscription(request):
    sub, _ = Subscription.objects.get_or_create(user=request.user)
    prof, _ = UserProfile.objects.get_or_create(user=request.user)
    sub.plan = 'free'
    sub.is_active = False
    sub.expires_at = None
    sub.save()
    prof.plan = 'free'
    prof.plan_expires_at = None
    prof.save()
    messages.info(request, 'Đã hủy gia hạn. Tài khoản sẽ về Free sau kỳ hạn.')
    return redirect('pricing')

@require_POST
def dismiss_coupon(request):
    return JsonResponse({'ok': True})
