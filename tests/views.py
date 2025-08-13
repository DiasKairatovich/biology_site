from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def teacher_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_teacher())(view_func)
def test_list(request):
    return render(request, 'tests/test_list.html')

def test_detail(request, test_id):
    return render(request, 'tests/test_detail.html', {'test_id': test_id})

def start_test(request, test_id):
    return render(request, 'tests/start_test.html', {'test_id': test_id})

def submit_test(request, test_id):
    return render(request, 'tests/submit_test.html', {'test_id': test_id})
