from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ArticleForm, CommentForm
from webapp.models import Article, Comment


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'create.html', context={
                'form': form
            })


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        form = ArticleForm(data={
            'title': article.title,
            'text': article.text,
            'author': article.author
        })
        return render(request, 'update.html', context={
            'form': form,
            'article': article
        })

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            article.save()

            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'update.html', context={
                'form': form,
                'article': article
            })


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        return render(request, 'delete.html', context={
            'article': article
        })

    def post(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        article.delete()
        return redirect('index')


class CommentIndexView(TemplateView):
    template_name = 'comment/comment_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.order_by('-created_at')
        return context


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
        form = CommentForm(initial={
            'article': article.title,
            'author': 'Anonym'
        })
        return render(request, 'comment/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=form.cleaned_data['article']
            )
            return redirect('article_view', pk=comment.article.pk)
        else:
            return render(request, 'comment/create.html', context={
                'form': form
            })


class CommentUpdateView(View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        form = CommentForm(data={
            'article': comment.article,
            'text': comment.text,
            'author': comment.author
        })
        return render(request, 'comment/update.html', context={
            'form': form,
            'comment': comment
        })

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        if form.is_valid():
            comment.article = form.cleaned_data['article']
            comment.text = form.cleaned_data['text']
            comment.author = form.cleaned_data['author']
            comment.save()

            return redirect('comment')
        else:
            return render(request, 'comment/update.html', context={
                'form': form,
                'comment': comment
            })


class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        return render(request, 'comment/delete.html', context={
            'comment': comment
        })

    def post(self, request, *args, **kwargs):
        comment_pk = kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
        return redirect('comment')