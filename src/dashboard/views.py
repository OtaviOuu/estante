from django.shortcuts import render, redirect
from scraper.services.books import get_all_categories, get_books_from_page
import asyncio
from django.http import HttpResponseRedirect

# Create your views here.


async def home(request):
    """
    Render the home page.
    """

    categories = await get_all_categories()
    return render(request, "dashboard/home.html", {"categories": categories})


async def dashboard(request):
    """
    Render the dashboard page.
    """

    category = request.GET.get("category")
    page = request.GET.get("page") if request.GET.get("page") else 1
    if category:
        target_href = f"{category.replace("/", "")}?page={page}"
        books, last_page = await get_books_from_page(href=target_href)

        context = {
            "books": books,
            "last_page": range(1, last_page + 1),
            "actual_page": page,
            "category": category.replace("/", ""),
        }

        return render(request, "dashboard/board.html", context)

    return redirect("home")
