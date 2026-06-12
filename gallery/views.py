from django.shortcuts import render
from .models import NailDesign, Category, SavedDesign, DesignLike
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def gallery_list(request):

    query = request.GET.get('q')
    category = request.GET.get('category')

    designs = NailDesign.objects.all()
    categories = Category.objects.all()

    if query:
        designs = designs.filter(
            title__icontains=query
        )

    if category:
        designs = designs.filter(
            category__id=category
        )

    context = {
        'designs': designs,
        'categories': categories,
        'query': query,
        'selected_category': category
    }

    return render(
        request,
        'gallery/gallery_list.html',
        context
    )


def design_detail(request, pk):

    design = get_object_or_404(
        NailDesign,
        pk=pk
    )

    is_saved = False
    is_liked = False

    if request.user.is_authenticated:

        is_saved = SavedDesign.objects.filter(
            user=request.user,
            design=design
        ).exists()

        is_liked = DesignLike.objects.filter(
            user=request.user,
            design=design
        ).exists()

    return render(
        request,
        'gallery/design_detail.html',
        {
            'design': design,
            'is_saved': is_saved,
            'is_liked': is_liked,
        }
    )


@login_required
def like_design(request, pk):

    design = get_object_or_404(
        NailDesign,
        pk=pk
    )

    like = DesignLike.objects.filter(
        user=request.user,
        design=design
    )

    if like.exists():

        like.delete()

    else:

        DesignLike.objects.create(
            user=request.user,
            design=design
        )

    return redirect(
        'design_detail',
        pk=pk
    )

@login_required
def save_design(request, pk):
    design = get_object_or_404(
        NailDesign,
        pk=pk
    )

    SavedDesign.objects.get_or_create(
        user=request.user,
        design=design
    )

    return redirect('saved_designs')


@login_required
def saved_designs(request):
    saved = SavedDesign.objects.filter(
        user=request.user
    ).select_related(
        'design'
    )

    return render(
        request,
        'gallery/saved_designs.html',
        {
            'saved_designs': saved
        }
    )


@login_required
def unsave_design(request, pk):

    SavedDesign.objects.filter(
        user=request.user,
        design_id=pk
    ).delete()

    return redirect(
        'design_detail',
        pk=pk
    )