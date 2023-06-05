from favs.models import Thing, Fav, Comment
from favs.forms import CreateForm,CommentForm
from django.views import View
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from favs.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.contrib.humanize.templatetags.humanize import naturaltime

class ThingListView(OwnerListView):
    model = Thing
    template_name = "favs/list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            query.add(Q(tags__name__in=[strval]), Q.OR)
            thing_list = Thing.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :
            thing_list = Thing.objects.all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in thing_list:
            obj.natural_updated = naturaltime(obj.updated_at)
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_things.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'thing_list' : thing_list, 'search': strval, 'favorites':favorites}
        return render(request, self.template_name, ctx)

class ThingDetailView(OwnerDetailView):
    model = Thing
    template_name = "favs/detail.html"
    def get(self,request,pk):
        x=Thing.objects.get(id=pk)
        comments=Comment.objects.filter(thing=x).order_by('-updated_at')
        comment_form=CommentForm()
        ctx={'thing':x,'comments':comments,'comment_form':comment_form}
        return render(request,self.template_name,ctx)

class ThingCreateView(LoginRequiredMixin, View):
    template_name = 'favs/form.html'
    success_url = reverse_lazy('thing:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form':form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx={'form':form}
            return render(request,self.template_name,ctx)

        thing = form.save(commit=False)
        thing.owner = self.request.user
        thing.save()
        return redirect(self.success_url)

class ThingUpdateView(LoginRequiredMixin, View):
    template_name = 'favs/form.html'
    success_url = reverse_lazy('thing:all')

    def get(self, request, pk):
        thing=get_object_or_404(Thing, id=pk, owner=self.request.user)
        form=CreateForm(instance=thing)
        ctx={'form':form}
        return render(request, self.template_name,ctx)

    def post(self,request,pk=None):
        thing = get_object_or_404(Thing, id=pk, owner=self.request.user)
        form=CreateForm(request.POST, request.FILES or None, instance=thing)

        if not form.is_valid():
            ctx={'form':form}
            return render(request,self.template_name, ctx)

        thing = form.save(commit=False)
        thing.save()
        return redirect(self.success_url)

class ThingDeleteView(OwnerDeleteView):
    model = Thing
    template_name = "favs/delete.html"

class CommentCreateView(View,LoginRequiredMixin):
    def post(self,request,pk):
        f=get_object_or_404(Thing, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, thing=f)
        comment.save()
        return redirect(reverse('favs:thing_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "favs/comment_delete.html"

    def get_success_url(self):
        thing = self.object.thing
        return reverse('thing:detail', args=[thing.id])

def stream_file(request, pk):
    thing = get_object_or_404(Thing, id=pk)
    response = HttpResponse()
    response['Content-Type'] = thing.content_type
    response['Content-Length'] = len(thing.picture)
    response.write(thing.picture)
    return response

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Thing, id=pk)
        favorites = Fav(user=request.user, thing=t)
        try:
            favorites.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Thing, id=pk)
        try:
            favorites = Fav.objects.get(user=request.user, thing=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()

