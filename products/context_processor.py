"""module calling the form to search a product"""

from products.forms import SearchProduct


def search_form(request):

    """calls the search method of product
    returns the search form"""

    return {"search_form":  SearchProduct()}
