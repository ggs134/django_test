from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .models import Info
from .models import BitcoinAddress
from .forms import PostForm

import keyUtils

# Create your views here.
def post_list(request):
	# posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	posts = Post.objects.order_by('published_date')
	addresses = BitcoinAddress.objects.all()
	return render(request, 'blog/post_list.html', {'posts': posts, 'addresses': addresses})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
	if request.method == "POST":
        		form = PostForm(request.POST)
        		if form.is_valid():
        			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
            		return redirect('blog.views.post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def site_info(request):
	infos = Info.objects.order_by('text')
	return render(request, 'blog/info.html', {'infos': infos})

def address_new(request):
	if request.method == "POST":
		priv_key = keyUtils.makePrivKey()
		wif = keyUtils.privateKeyToWif(priv_key)
		addr = keyUtils.keyToAddr(priv_key)
		addressObj = BitcoinAddress(address=addr, priv_key=priv_key, priv_wif=wif)
		addressObj.save()
		return redirect('blog.views.post_list')
	else:
		return render(request, 'blog/post_list.html',{})
	return render(request, 'blog/post_list.html',{})