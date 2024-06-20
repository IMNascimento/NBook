from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def home(request):
    books = Book.objects.all()
    return render(request, 'catalog/home.html', {'books': books})

def index(request):
    user = request.user
    books = Book.objects.all()
    data_books = []
    for book in books:
        data_books.append(
            {
                'book': book,
                "commented": book.user_commented(user) if user.is_authenticated else False,
                "liked": book.user_liked(user) if user.is_authenticated else False,
                "comments": Comment.objects.filter(book=book)
            }
        )
    return render(request, 'catalog/index.html', {'books': data_books})

@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    like, created = Like.objects.get_or_create(user=request.user, book=book)
    if not created:
        like.delete()
    return redirect('index')

@login_required
def comment_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, book=book, content=content)
    return redirect('index')


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro cadastrado com sucesso!')
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'catalog/add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livro editado com sucesso!')
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/edit_book.html', {'form': form})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Livro deletado com sucesso!')
        return redirect('home')
    return render(request, 'catalog/delete_book.html', {'book': book})