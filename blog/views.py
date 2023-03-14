from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm, CreatePostForm, PostUpdateForm
from django.contrib import messages
from .forms import BookingForm
from .models import Booking
import datetime
from dateutil import parser

# =======================
from django.core.paginator import Paginator
# ======================


def about_page(request):
    """
    This view renders to the user the about page.
    """
    return render(request, 'about.html')


# @login_required()
# def usersblog_page(request):
#     """
#     This view renders to the user the about page.
#     """
#     posts = Post.objects.all()
#     return render(request, 'usersblog.html', {'posts':posts})

# ======================================
@login_required()
def usersblog_page(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, 'usersblog.html', context)
# ====================================================
    
# @login_required()
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('usersblog')
    else:
        form = CreatePostForm()
    context = {
        'form': form
    }
    return render(request, 'create-post.html', context)


def usersblog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)
    new_comment = None
    comment_form = CommentForm(data=request.POST)
    if request.method == 'POST':
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()
    context = {
        'post': post,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }

    return render(request, 'usersblog_detail.html', context)


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.info(request, "The post have been updated")
            return redirect('usersblog')
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'edit_post.html', context)


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.info(request, "The post have been deleted")
        return redirect('usersblog')
    context = {
        'post': post,
    }
    return render(request, 'delete_post.html', context)


def pricing_page(request):
    """
    This view renders to the user the about page.
    """
    return render(request, 'pricing.html')

def contact_page(request):
    """
    This view renders to the user the about page.
    """
    return render(request, 'contact.html')


def contact_page(request):
    """
    This view renders to the user the about page.
    """
    return render(request, 'contact.html')


def services(request):
    """
    This view renders to the user the services page.
    """
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


def booknow(request):
    """The view for the booking page. If user is logged in it renders the
    booknow.html, otherwise it redirects user to the login page or signup page.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        date = datetime.datetime.strptime(str(request.POST['date']), '%Y-%m-%d')
        time = datetime.datetime.strptime(str(request.POST['time']), '%H:%M')
        time = request.POST['time']
        if Booking.objects.filter(date=date, time=time).exists():
            messages.error(request, "The time is already booked, please select another time")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if form.is_valid():
            booking_form = form.save(commit=False)
            booking_form.user = request.user
            booking_form.save()
            return redirect('bookings')
        else:
            messages.error(request, "Please enter correct data")
            return render(request, 'booknow.html', {'form': form})
    form = BookingForm()
    return render(request, 'booknow.html', {'form': form})


def bookings(request):
    """This view checks if user is logged in and renders the
    bookings.html page which shows user bookings and otherwise
    it redirects to the signup page
    """
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
        context = {
           'bookings': bookings
        }
        return render(request, 'bookings.html', context)
    else:
        return redirect('../accounts/signup')


def change_booking(request, booking_id):
    """The view that renders the change_booking page where the user can
    update a current booking.
    """
    record = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=record)
        date = datetime.datetime.strptime(str(request.POST['date']), '%Y-%m-%d')
        time = datetime.datetime.strptime(str(request.POST['time']), '%H:%M')
        time = request.POST['time']
        if Booking.objects.filter(date=date, time=time).exists():
            messages.error(request, "The time is already booked, please select another time")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if form.is_valid():
            form.save()
            messages.success(request, 'You succesfully updated your booking.')
            return redirect('bookings')
        else:
            return render(request, 'change-booking.html', {'form': form})
    form = BookingForm(instance=record)
    context = {'form': form, 'record': record}
    return render(request, 'change-booking.html', context)


def delete_booking(request, booking_id):
    """
    Function enables user to delete a booking record
    """
    record = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        form = BookingForm(request.POST, instance=record)
        if record.delete():
            messages.success(request, 'Your booking has been deleted.')
            return redirect('bookings')
    form = BookingForm(instance=record)
    context = {
        'form': form, 'record': record}
    return render(request, 'delete-booking.html', context)


# class PostList(generic.ListView):
#     model = Post
#     queryset = Post.objects.filter(status=1).order_by("-created_on")
#     template_name = "index.html"
#     paginate_by = 4

# ============================================================
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "usersblog.html"
    paginate_by = 4
# ===========================================================


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
