from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import forms
from . import models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()

    context = {'tickets': tickets,
               'reviews': reviews}
    return render(request, 'reviews/home.html', context)


def ticket_create(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # form is valid save ticket in DB
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            # go back to home page
            return redirect('home')

    else:
        form = forms.TicketForm()

    context = {'form': form}
    return render(request, 'reviews/ticket_create.html', context)


def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            # form is valid save ticket in DB
            form.save()
            # go back to home page
            return redirect('home')

    context = {'form': form}
    return render(request, 'reviews/ticket_edit.html', context)


def review_without_ticket_create(request):
    """ create a ticket AND a review at the same time"""
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            # all form are valid save ticket anr review in DB
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            # go back to home page
            return redirect('home')

    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    context = {'ticket_form': ticket_form,
               'review_form': review_form
               }
    return render(request, 'reviews/review_without_ticket_create.html',
                  context)


def review_with_ticket_create(request, ticket_id):
    """ create a review from a ticket"""
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            # save review in DB
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            # go back to home page
            return redirect('home')

    else:
        review_form = forms.ReviewForm()

    context = {'ticket': ticket,
               'review_form': review_form
               }
    return render(request, 'reviews/review_with_ticket_create.html',
                  context)


def review_edit(request, review_id):
    """ edit a review"""
    review = get_object_or_404(models.Review, id=review_id)
    review_form = forms.ReviewForm(instance=review)
    ticket = get_object_or_404(models.Ticket, id=review.ticket.id)

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            # save review in DB
            review_form.save()
            # go back to home page
            return redirect('home')

    context = {'ticket': ticket,
               'review_form': review_form
               }
    return render(request, 'reviews/review_edit.html',
                  context)


def follow_user(request):
    """ add a followed user"""
    followed_by = request.user.followed_by.all()
    following = request.user.following.all()
    if request.method == 'POST':
        form = forms.FollowUserForm(request.POST)
        if form.is_valid():
            # save review in DB
            user_follows = form.save(commit=False)
            user_follows.user = request.user
            user_follows = form.save()
            # go back to home page
            return redirect('follow_user')
    else:
        form = forms.FollowUserForm()

    context = {'form': form,
               'following': following,
               'followed_by': followed_by
               }
    return render(request, 'reviews/follow_user.html',
                  context)


def unfollow_user(request, follow_id):
    relationship = models.UserFollows.objects.get(id=follow_id)

    if request.method == 'POST':
        relationship.delete()
        return redirect('follow_user')

    context = {'relationship': relationship}
    return render(request,
                  'reviews/follow_delete.html',
                  context)
