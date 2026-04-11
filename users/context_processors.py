from blog.models import Tag # Model Tag nằm ở app blog

def global_data(request):
    # Lấy tất cả thể loại để hiện ở menu Header
    return {
        'all_tags': Tag.objects.all(),
    }
