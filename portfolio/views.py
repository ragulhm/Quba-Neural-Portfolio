from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Project, SkillCategory, BlogPost, BlogCategory
from .forms import ContactForm
from .github_api import GitHubAPI
from .medium_api import MediumAPI
from .ai_utils import AstralOracle

def index(request):
    projects = Project.objects.all()
    
    # Structure skills data for the template
    categories = SkillCategory.objects.all().prefetch_related('skills')
    skills = []
    for category in categories:
        skills.append({
            "title": category.title,
            "icon": category.icon,
            "gradient": category.gradient,
            "items": [skill.name for skill in category.skills.all()]
        })

    # Latest blog posts
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]

    # Fetch GitHub Activity
    github_api = GitHubAPI()
    github_activities = github_api.get_recent_activity()

    # Fetch Medium Articles
    medium_api = MediumAPI('ragul.mr3391')
    medium_articles = medium_api.get_recent_articles()

    context = {
        'projects': projects,
        'skills': skills,
        'form': ContactForm(),
        'latest_posts': latest_posts,
        'github_activities': github_activities,
        'medium_articles': medium_articles
    }
    return render(request, 'portfolio/index.html', context)

def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been sent.'})
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    categories = BlogCategory.objects.all()
    return render(request, 'portfolio/blog_list.html', {'posts': posts, 'categories': categories})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'portfolio/blog_detail.html', {'post': post})

def ai_query(request):
    if request.method == 'POST':
        user_question = request.POST.get('question')
        if not user_question:
            return JsonResponse({'status': 'error', 'message': 'Say something...'}, status=400)
            
        oracle = AstralOracle()
        answer = oracle.query(user_question)
        return JsonResponse({'status': 'success', 'answer': answer})
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
