import json

from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import CharField, Value, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from . import forms
from . import models

NUMBER_OF_ITEMS_BY_PAGE = 5


@login_required
def home(request):
    """ view for the homepage
        get the 3 most recents items (review and ticket) from all sources
        and the 3 most recents itmes from the user feed
        Send it for display
    """
    # get user feed tickets and reviews
    user_tickets = models.Ticket.objects.filter(
        Q(user__in=request.user.following.values("followed_user")) |
        Q(user=request.user)
    )
    user_tickets = user_tickets.annotate(
        content_type=Value('TICKET', CharField()))

    user_reviews = models.Review.objects.filter(
        Q(user__in=request.user.following.values("followed_user")) |
        Q(user=request.user) |
        Q(ticket__in=models.Ticket.objects.filter(user=request.user))
    )
    user_reviews = user_reviews.annotate(
        content_type=Value('REVIEW', CharField()))

    # merge the reviews and tickets and select the 3 most recent
    user_feed = sorted(
        chain(user_tickets, user_reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )[:3]

    # get general feed tickets and reviews
    general_tickets = models.Ticket.objects.all()
    general_tickets = general_tickets.annotate(
        content_type=Value('TICKET', CharField()))

    general_reviews = models.Review.objects.all()
    general_reviews = general_reviews.annotate(
        content_type=Value('REVIEW', CharField()))

    # merge the reviews and tickets and select the 3 most recent
    general_feed = sorted(
        chain(general_tickets, general_reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )[:3]

    context = {'user_feed': user_feed,
               'general_feed': general_feed}
    return render(request, 'reviews/home.html', context)


@login_required
def feed(request):
    """ view for the feed page
        get the items (review and ticket) from the user
        and from the users it follows
        sort them in decreasing time send them for display
    """
    tickets = models.Ticket.objects.filter(
        Q(user__in=request.user.following.values("followed_user")) |
        Q(user=request.user)
    )
    tickets = tickets.annotate(
        content_type=Value('TICKET', CharField()))

    reviews = models.Review.objects.filter(
        Q(user__in=request.user.following.values("followed_user")) |
        Q(user=request.user) |
        Q(ticket__in=models.Ticket.objects.filter(user=request.user))
    )
    reviews = reviews.annotate(
        content_type=Value('REVIEW', CharField()))

    feed = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )

    # Pagination handling
    paginator = Paginator(feed, NUMBER_OF_ITEMS_BY_PAGE)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'reviews/feed.html', context)


@login_required
def posts(request):
    """ view for the posts page
        get the items (review and ticket) from the user
        sort them in decreasing time send them for display
    """
    tickets = models.Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = models.Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    # Pagination handling
    paginator = Paginator(posts, NUMBER_OF_ITEMS_BY_PAGE)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'reviews/posts.html', context)


@login_required
def ticket_create(request):
    """ view for the ticket creation page """
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # form is valid save ticket in DB
            ticket = form.save(commit=False)
            # add the user to the ticket
            ticket.user = request.user
            ticket.save()

            next = request.POST.get('next', '/')
            # go to previous page
            return redirect(next)
    else:
        form = forms.TicketForm()

    context = {'form': form}
    return render(request, 'reviews/ticket_create.html', context)


@login_required
def ticket_edit(request, ticket_id):
    """ view for the ticket edition page
    retrieve the ticket and display it then save the changes
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            # form is valid save ticket in DB
            form.save()

            next = request.POST.get('next', '/')
            # go to previous page
            return redirect(next)

    context = {'form': form}
    return render(request, 'reviews/ticket_edit.html', context)


@login_required
@csrf_exempt
def ticket_delete(request):
    """ view for the ticket deletion page
    retrieve the ticket and display it then delete it when confirmed
    """
    if request.method == 'POST':
        body_json = json.loads(request.body)
        ticket_id = body_json['item']
        ticket = models.Ticket.objects.get(id=ticket_id)
        ticket.delete()
        return JsonResponse({'success': 'yes'})


@login_required
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

            next = request.POST.get('next', '/')
            # go to previous page
            return redirect(next)
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    context = {'ticket_form': ticket_form,
               'review_form': review_form
               }
    return render(request, 'reviews/review_without_ticket_create.html',
                  context)


@login_required
def review_with_ticket_create(request, ticket_id):
    """ create a review from a ticket"""

    # get the ticket data for dispaly
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            # save review in DB
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            next = request.POST.get('next', '/')
            # go to previous page
            return redirect(next)
    else:
        review_form = forms.ReviewForm()

    context = {'ticket': ticket,
               'review_form': review_form
               }
    return render(request, 'reviews/review_with_ticket_create.html',
                  context)


@login_required
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

            next = request.POST.get('next', '/')
            # go to previous page
            return redirect(next)

    context = {'ticket': ticket,
               'review_form': review_form
               }
    return render(request, 'reviews/review_edit.html',
                  context)


@login_required
@csrf_exempt
def review_delete(request):

    if request.method == 'POST':
        body_json = json.loads(request.body)
        review_id = body_json['item']
        review = models.Review.objects.get(id=review_id)
        review.delete()
        return JsonResponse({'success': 'yes'})


@login_required
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


@login_required
@csrf_exempt
def unfollow_user(request):
    """ delete a follow relationship """

    print("view: unfollow_user")
    if request.method == 'POST':
        body_json = json.loads(request.body)
        print("RPOST:", body_json)
        follow_id = body_json['relation']
        relationship = models.UserFollows.objects.get(id=follow_id)
        relationship.delete()
        return JsonResponse({'success': 'yes'})
