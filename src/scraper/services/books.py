import asyncio
import aiohttp
from parsel.selector import Selector


async def get_books_from_page(href: str) -> list[dict]:
    """
    Get books from a specific category and page.
    Args:
        book_category (str): The category of books to scrape.
        page (int): The page number to scrape.
    Returns:
        list[dict]: A list of dictionaries containing book data.
    """

    # target_url = f"https://www.estantevirtual.com.br/{book_category}?page={page}"
    target_url = f"https://www.estantevirtual.com.br/{href}"
    async with aiohttp.ClientSession() as session:
        async with session.get(target_url) as response:
            html = await response.text()
            selector = Selector(text=html)

            last_page = selector.css(".pagination__page::text").getall()[-1].strip()

            books = selector.css("#product-item")
            get_book_data_tasks = [get_book_data(book) for book in books]

            books_data = await asyncio.gather(*get_book_data_tasks)
            return books_data, int(last_page)


async def get_book_data(book_selector: Selector) -> dict:
    """
    Extract book data from the book selector.
    Args:
        book_selector (Selector): The selector for the book element.
    Returns:
        dict: A dictionary containing book data.
    """

    img_url = book_selector.css("img::attr(data-src)").get().strip()
    title = book_selector.css("h2.product-item__title::text").get().strip()
    author = book_selector.css(".product-item__author::text").get().strip()

    return {
        "img_url": img_url,
        "title": title,
        "author": author,
    }


async def get_all_categories() -> list[str]:
    """
    Get all book categories from Estante Virtual.
    Returns:
        list[str]: A list of book categories.
    """

    target_url = "https://www.estantevirtual.com.br/categoria"
    async with aiohttp.ClientSession() as session:
        async with session.get(target_url) as response:
            html = await response.text()
            selector = Selector(text=html)

            categories = selector.css(".estantes-list a::attr(href)").getall()

            return [category.replace("/", "") for category in categories]
