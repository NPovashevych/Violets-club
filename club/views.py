from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    MemberSearchForm,
    VioletSearchForm,
    MemberCreationForm, VioletForm, MemberUpdateForm,
)

from club.models import Member, Status, Violet, Variety, Post


def index(request: HttpRequest) -> HttpResponse:
    num_members = Member.objects.count()
    num_violets = Violet.objects.count()
    num_varieties = Variety.objects.count()
    num_statuses_beginner = Member.objects.filter(status__name="beginner").count()
    num_statuses_professional = Member.objects.filter(status__name="professional").count()
    num_statuses_amateur = Member.objects.filter(status__name="amateur").count()
    members_with_violets_count = Member.objects.annotate(num_violets=Count("violets"))
    member_with_max_violets = members_with_violets_count.order_by('-num_violets').first()
    name_of_member_with_max_violets = member_with_max_violets.username
    num_violets_of_member_with_max_violets = member_with_max_violets.num_violets
    posts = Post.objects.all()
    day_number = date.today().day
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_members": num_members,
        "num_violets": num_violets,
        "num_varieties": num_varieties,
        "num_statuses_beginner": num_statuses_beginner,
        "num_statuses_professional": num_statuses_professional,
        "num_statuses_amateur": num_statuses_amateur,
        "num_violets_of_member_with_max_violets": num_violets_of_member_with_max_violets,
        "name_of_member_with_max_violets": name_of_member_with_max_violets,
        "posts": posts,
        "day_number": day_number,
        "num_visits": num_visits + 1,
    }
    return render(request, "club/index.html", context=context)


class StatusListView(generic.ListView):
    model = Status
    template_name = "club/status_list.html"
    queryset = Status.objects.order_by("name")


class VarietyListView(generic.ListView):
    model = Variety
    template_name = "club/variety_list.html"
    context_object_name = "variety_list"
    paginate_by = 10


class VarietyCreateView(LoginRequiredMixin, generic.CreateView):
    model = Variety
    fields = "__all__"
    template_name = "club/variety_create.html"
    success_url = reverse_lazy("club:variety-list")


class VarietyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Variety
    fields = "__all__"
    template_name = "club/variety_create.html"
    success_url = reverse_lazy("club:variety-list")


class VarietyDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Variety
    template_name = "club/variety_delete.html"
    success_url = reverse_lazy("club:variety-list")


class MemberListView(generic.ListView):
    model = Member
    template_name = "club/member_list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = MemberSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class MemberDetailView(generic.DetailView):
    model = Member
    template_name = "club/member_detail.html"
    queryset = Member.objects.prefetch_related("violets__variety")


class MemberCreateView(LoginRequiredMixin, generic.CreateView):
    model = Member
    form_class = MemberCreationForm


class MemberUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Member
    form_class = MemberUpdateForm
    success_url = reverse_lazy("club:member-list")


class MemberDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Member
    success_url = reverse_lazy("club:member-list")


class VioletListView(generic.ListView):
    model = Violet
    template_name = "club/violet_list.html"
    queryset = Violet.objects.select_related("variety")
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VioletListView, self).get_context_data(**kwargs)
        sort = self.request.GET.get("sort", "")
        context["search_form"] = VioletSearchForm(initial={"sort": sort})
        return context

    def get_queryset(self):
        queryset = Violet.objects.all().select_related("variety")
        sort = self.request.GET.get("sort")
        if sort:
            return queryset.filter(sort__icontains=sort)
        return queryset


class VioletDetailView(generic.DetailView):
    model = Violet
    template_name = "club/violet_detail.html"


class VioletCreateView(LoginRequiredMixin, generic.CreateView):
    model = Violet
    template_name = "club/violet_create.html"
    success_url = reverse_lazy("club:violet-list")
    form_class = VioletForm


class VioletUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Violet
    form_class = VioletForm
    template_name = "club/violet_create.html"
    success_url = reverse_lazy("club:violet-list")


class VioletDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Violet
    template_name = "club/violet_delete.html"
    success_url = reverse_lazy("club:violet-list")


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = "__all__"
    template_name = "club/post_create_form.html"
    success_url = reverse_lazy("club:index")


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = "__all__"
    template_name = "club/post_create_form.html"
    success_url = reverse_lazy("club:index")


class AssignVioletView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        violet = get_object_or_404(Violet, pk=pk)
        if request.user in violet.member.all():
            violet.member.remove(request.user)
        else:
            violet.member.add(request.user)
        return redirect("club:violet-detail", pk=violet.id)
