from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def bid_statistics(request):
    context = {
        'statistics_data':
            [
                {"label": "accepted", "value": 540},
                {"label": "paid", "value": 120},
                {"label": "rejected", "value": 200}
            ]
    }
    return render(request, 'home/statistics.html', context)
