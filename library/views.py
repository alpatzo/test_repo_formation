from datetime import date, datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from library.utils import promo
from .models import Book
from .serializers import BookSerializer
from django.db.models import Sum
@csrf_exempt
@require_http_methods(['GET'])
def get_all_books(request):
    """GET: get all books"""
    books = Book.objects.all()
    print({"book type":books})
    serializer_for_books = BookSerializer(books, many=True) # default many=False
    # print({"serializer_for_books":serializer_for_books})
    # first format of total price
    # total_price = 0
    # for book in books:
    #     total_price+=book.price
    # the second format of total price
    total_price = books.aggregate(total=Sum('price'))['total'] or 0
    return JsonResponse({
        "books": serializer_for_books.data,
        "count": len(serializer_for_books.data),
        'total price':total_price
    })

@csrf_exempt
@require_http_methods(['GET'])
def get_book(request,pk):
    """GET: get a single book"""
    try:
        book = Book.objects.get(id=pk)
        limite_date = date(2019,12,31)
        if book.published_date > limite_date:

            serializer_for_book = BookSerializer(book)
            return JsonResponse({
                "book":serializer_for_book.data,
                "success":True
            })
        else:
            return JsonResponse({
                "error": "book published before 31/12/20219",
                "success":False
            })
    except Book.DoesNotExist:
        return JsonResponse({
            "error":"book not found",
            "success":False
        })

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_book(request, book_id):
    """DELETE: remove a book"""
    try:
        book = Book.objects.get(id = book_id)
        book.delete()
        return JsonResponse({
            "message":"book deleted successfully",
            "success":True
        })
    except Book.DoesNotExist:
        return JsonResponse({
            "error": "book not found",
            "success":False
        },status=404)

@csrf_exempt
@require_http_methods(['POST'])
def create_book(request):
    """POST: create book"""
    json_data = json.loads(request.body)
    promo_date = date(2019,12,31)
    print({"type promo_date":type(promo_date)})
    print({"type json_data['published_date']": type(json_data['published_date'])})
    date_book = datetime.strptime(json_data['published_date'], "%Y-%m-%d").date()
    print({"date_book":date_book})
    print({"type date_book":type(date_book)})
    price_book = json_data['price']
    if date_book < promo_date:
        price_book = promo(price_book)
        json_data['price']=price_book
    serializer = BookSerializer(data=json_data)
    if serializer.is_valid():
        book = serializer.save()
        book_data = BookSerializer(book).data
        return JsonResponse({
            "message":"book created successfully",
            "book":book_data,
            "success":True
        })
    else:
        return JsonResponse({
            "error":serializer.errors,
            "success":False
        })
    
@csrf_exempt
@require_http_methods(['PUT','PATCH'])
def update_book(request):
    json_data = json.loads(request.body)
    try:
        book = Book.objects.get(id=json_data['id'])
    except Book.DoesNotExist:
        JsonResponse({
            "error":"book not found"
        })
    serializer = BookSerializer(book, data=json_data)
    if serializer.is_valid():
        book = serializer.save()
        book_data = BookSerializer(book).data
        return JsonResponse({
            "message":"book updated successfully",
            "book":book_data
        })
    return JsonResponse({
        "error":serializer.errors
    })