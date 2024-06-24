from django.shortcuts import render, redirect
from scraping.models import EuroMillionsResult
from predictions.models import Prediction, ShuffledPrediction, UploadImageModel
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from datetime import datetime
from django.contrib import messages


def get_image_url(name):
    image = UploadImageModel.objects.filter(name=name).values("image").first()
    return image["image"] if image else None


def index(request):
    """
    A view to return the index page with the latest draw results and latest winning predictions.

    This view fetches the latest EuroMillions draw result from the database. It also identifies the
    latest prediction date where predictions have a non-null match type and fetches all predictions
    for that date. Additionally, it fetches all winning predictions. The context containing the latest
    draw result, latest predictions, and winning predictions is then passed to the 'index.html' template
    for rendering.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'index.html' template with the context containing latest_result,
        latest_predictions, and winning_predictions.
    """

    try:
        latest_result = EuroMillionsResult.objects.latest("id")
    except EuroMillionsResult.DoesNotExist:
        latest_result = None

    # Calculate total winning amounts
    total_winning_amount_predictions = Prediction.objects.filter(
        win_amount__isnull=False
    ).aggregate(Sum('win_amount'))['win_amount__sum'] or 0

    total_winning_amount_shuffled = ShuffledPrediction.objects.filter(
        win_amount__isnull=False
    ).aggregate(Sum('win_amount'))['win_amount__sum'] or 0

    # Combine total winning amounts
    total_combined_winning_amount = total_winning_amount_predictions + total_winning_amount_shuffled

    latest_date = Prediction.objects.filter(
        match_type__isnull=False
    ).aggregate(latest_date=Max("prediction_date"))["latest_date"]

    if latest_date:
        latest_predictions = Prediction.objects.filter(
            prediction_date=latest_date, match_type__isnull=False
        )
    else:
        latest_predictions = []

    alltime_winning_predictions = Prediction.objects.filter(
        match_type__isnull=False
    ).order_by("-draw_date")

    # Fetch images for the latest result balls and stars
    if latest_result:
        ball_1_image = get_image_url(f"{latest_result.ball_1:02}")
        ball_2_image = get_image_url(f"{latest_result.ball_2:02}")
        ball_3_image = get_image_url(f"{latest_result.ball_3:02}")
        ball_4_image = get_image_url(f"{latest_result.ball_4:02}")
        ball_5_image = get_image_url(f"{latest_result.ball_5:02}")

        star_1_image = get_image_url(f"star{latest_result.lucky_star_1}")
        star_2_image = get_image_url(f"star{latest_result.lucky_star_2}")
    else:
        ball_1_image = ball_2_image = ball_3_image = ball_4_image = (
            ball_5_image
        ) = None
        star_1_image = star_2_image = None

    predictions_with_images = []
    for prediction in latest_predictions:
        winning_balls_list = (
            [int(ball) for ball in prediction.winning_balls.split(",")]
            if prediction.winning_balls
            else []
        )
        winning_stars_list = (
            [int(star) for star in prediction.winning_lucky_stars.split(",")]
            if prediction.winning_lucky_stars
            else []
        )

        pred_ball_1_image = get_image_url(
            f"green{prediction.pred_ball_1:02}"
            if prediction.pred_ball_1 in winning_balls_list
            else f"{prediction.pred_ball_1:02}"
        )
        pred_ball_2_image = get_image_url(
            f"green{prediction.pred_ball_2:02}"
            if prediction.pred_ball_2 in winning_balls_list
            else f"{prediction.pred_ball_2:02}"
        )
        pred_ball_3_image = get_image_url(
            f"green{prediction.pred_ball_3:02}"
            if prediction.pred_ball_3 in winning_balls_list
            else f"{prediction.pred_ball_3:02}"
        )
        pred_ball_4_image = get_image_url(
            f"green{prediction.pred_ball_4:02}"
            if prediction.pred_ball_4 in winning_balls_list
            else f"{prediction.pred_ball_4:02}"
        )
        pred_ball_5_image = get_image_url(
            f"green{prediction.pred_ball_5:02}"
            if prediction.pred_ball_5 in winning_balls_list
            else f"{prediction.pred_ball_5:02}"
        )

        pred_lucky_1_image = get_image_url(
            f"greenstar{prediction.pred_lucky_1}"
            if prediction.pred_lucky_1 in winning_stars_list
            else f"star{prediction.pred_lucky_1}"
        )
        pred_lucky_2_image = get_image_url(
            f"greenstar{prediction.pred_lucky_2}"
            if prediction.pred_lucky_2 in winning_stars_list
            else f"star{prediction.pred_lucky_2}"
        )

        predictions_with_images.append(
            {
                "prediction": prediction,
                "pred_ball_1_image": pred_ball_1_image,
                "pred_ball_2_image": pred_ball_2_image,
                "pred_ball_3_image": pred_ball_3_image,
                "pred_ball_4_image": pred_ball_4_image,
                "pred_ball_5_image": pred_ball_5_image,
                "pred_lucky_1_image": pred_lucky_1_image,
                "pred_lucky_2_image": pred_lucky_2_image,
            }
        )

    latest_shuffled_date = ShuffledPrediction.objects.filter(
        match_type__isnull=False
    ).aggregate(latest_date=Max("prediction_date"))["latest_date"]

    if latest_shuffled_date:
        latest_shuffled_predictions = ShuffledPrediction.objects.filter(
            prediction_date=latest_shuffled_date, match_type__isnull=False
        )
    else:
        latest_shuffled_predictions = []

    alltime_winning_shuffled_predictions = ShuffledPrediction.objects.filter(
        match_type__isnull=False
    ).order_by("-draw_date")

    shuffled_predictions_with_images = []
    for prediction in latest_shuffled_predictions:
        winning_balls_list = (
            [int(ball) for ball in prediction.winning_balls.split(",")]
            if prediction.winning_balls
            else []
        )
        winning_stars_list = (
            [int(star) for star in prediction.winning_lucky_stars.split(",")]
            if prediction.winning_lucky_stars
            else []
        )

        pred_ball_1_image = get_image_url(
            f"green{prediction.pred_ball_1:02}"
            if prediction.pred_ball_1 in winning_balls_list
            else f"{prediction.pred_ball_1:02}"
        )
        pred_ball_2_image = get_image_url(
            f"green{prediction.pred_ball_2:02}"
            if prediction.pred_ball_2 in winning_balls_list
            else f"{prediction.pred_ball_2:02}"
        )
        pred_ball_3_image = get_image_url(
            f"green{prediction.pred_ball_3:02}"
            if prediction.pred_ball_3 in winning_balls_list
            else f"{prediction.pred_ball_3:02}"
        )
        pred_ball_4_image = get_image_url(
            f"green{prediction.pred_ball_4:02}"
            if prediction.pred_ball_4 in winning_balls_list
            else f"{prediction.pred_ball_4:02}"
        )
        pred_ball_5_image = get_image_url(
            f"green{prediction.pred_ball_5:02}"
            if prediction.pred_ball_5 in winning_balls_list
            else f"{prediction.pred_ball_5:02}"
        )

        pred_lucky_1_image = get_image_url(
            f"greenstar{prediction.pred_lucky_1}"
            if prediction.pred_lucky_1 in winning_stars_list
            else f"star{prediction.pred_lucky_1}"
        )
        pred_lucky_2_image = get_image_url(
            f"greenstar{prediction.pred_lucky_2}"
            if prediction.pred_lucky_2 in winning_stars_list
            else f"star{prediction.pred_lucky_2}"
        )

        shuffled_predictions_with_images.append(
            {
                "prediction": prediction,
                "pred_ball_1_image": pred_ball_1_image,
                "pred_ball_2_image": pred_ball_2_image,
                "pred_ball_3_image": pred_ball_3_image,
                "pred_ball_4_image": pred_ball_4_image,
                "pred_ball_5_image": pred_ball_5_image,
                "pred_lucky_1_image": pred_lucky_1_image,
                "pred_lucky_2_image": pred_lucky_2_image,
            }
        )

    context = {
        "latest_result": latest_result,
        "latest_predictions": latest_predictions,
        "alltime_winning_predictions": alltime_winning_predictions,
        "ball_1_image": ball_1_image,
        "ball_2_image": ball_2_image,
        "ball_3_image": ball_3_image,
        "ball_4_image": ball_4_image,
        "ball_5_image": ball_5_image,
        "star_1_image": star_1_image,
        "star_2_image": star_2_image,
        "predictions_with_images": predictions_with_images,
        "latest_shuffled_predictions": latest_shuffled_predictions,
        "alltime_winning_shuffled_predictions": alltime_winning_shuffled_predictions,
        "shuffled_predictions_with_images": shuffled_predictions_with_images,
        "total_combined_winning_amount": total_combined_winning_amount,
    }

    return render(request, "home/index.html", context)

def get_total_winning_amount(predictions):
    """
    Sums the winning amounts from a queryset of predictions.

    Args:
        predictions: A queryset of Prediction objects.

    Returns:
        int: The total winning amount.
    """
    return sum(prediction.win_amount for prediction in predictions if prediction.win_amount)

def alltime_winning_predictions_view(request):
    """
    Serves as the view for displaying all-time winning predictions with pagination.

    This view fetches all predictions from the database that have a non-null match type,
    indicating that they are winning predictions. It calculates the total winning amount from
    all such predictions and allows viewing these predictions in a paginated format.
    If accessed via an AJAX request, it returns only the HTML for the predictions list,
    suitable for dynamic page updates.

    Args:
        request (HttpRequest): The HTTP request object, which can contain a GET parameter
        'num_draws' specifying the number of predictions to display per page (defaults to 25).
        This can also handle AJAX requests for dynamic pagination without reloading the page.

    Returns:
        HttpResponse: Renders the 'alltime.html' template with the paginated winning predictions
        and the total winning amount, or a JsonResponse containing HTML content if it's an AJAX request.

    """
    num_draws = request.GET.get('num_draws', '25')
    
    alltime_winning_predictions = Prediction.objects.filter(
        match_type__isnull=False
    ).order_by("-draw_date")
    
    total_winning_amount = alltime_winning_predictions.aggregate(
        total=Sum('win_amount')
    )['total'] or 0

    if num_draws != 'all':
        paginator = Paginator(alltime_winning_predictions, 25)
        page_number = request.GET.get('page', 1)
        alltime_winning_predictions = paginator.get_page(page_number)
    
    predictions_with_images = []
    for prediction in alltime_winning_predictions:
        winning_balls_list = (
            [int(ball) for ball in prediction.winning_balls.split(",")]
            if prediction.winning_balls
            else []
        )
        winning_stars_list = (
            [int(star) for star in prediction.winning_lucky_stars.split(",")]
            if prediction.winning_lucky_stars
            else []
        )

        pred_ball_1_image = get_image_url(
            f"green{prediction.pred_ball_1:02}"
            if prediction.pred_ball_1 in winning_balls_list
            else f"{prediction.pred_ball_1:02}"
        )
        pred_ball_2_image = get_image_url(
            f"green{prediction.pred_ball_2:02}"
            if prediction.pred_ball_2 in winning_balls_list
            else f"{prediction.pred_ball_2:02}"
        )
        pred_ball_3_image = get_image_url(
            f"green{prediction.pred_ball_3:02}"
            if prediction.pred_ball_3 in winning_balls_list
            else f"{prediction.pred_ball_3:02}"
        )
        pred_ball_4_image = get_image_url(
            f"green{prediction.pred_ball_4:02}"
            if prediction.pred_ball_4 in winning_balls_list
            else f"{prediction.pred_ball_4:02}"
        )
        pred_ball_5_image = get_image_url(
            f"green{prediction.pred_ball_5:02}"
            if prediction.pred_ball_5 in winning_balls_list
            else f"{prediction.pred_ball_5:02}"
        )

        pred_lucky_1_image = get_image_url(
            f"greenstar{prediction.pred_lucky_1}"
            if prediction.pred_lucky_1 in winning_stars_list
            else f"star{prediction.pred_lucky_1}"
        )
        pred_lucky_2_image = get_image_url(
            f"greenstar{prediction.pred_lucky_2}"
            if prediction.pred_lucky_2 in winning_stars_list
            else f"star{prediction.pred_lucky_2}"
        )

        predictions_with_images.append(
            {
                "prediction": prediction,
                "pred_ball_1_image": pred_ball_1_image,
                "pred_ball_2_image": pred_ball_2_image,
                "pred_ball_3_image": pred_ball_3_image,
                "pred_ball_4_image": pred_ball_4_image,
                "pred_ball_5_image": pred_ball_5_image,
                "pred_lucky_1_image": pred_lucky_1_image,
                "pred_lucky_2_image": pred_lucky_2_image,
            }
        )

    context = {
        "alltime_winning_predictions": predictions_with_images,
        "total_winning_amount": total_winning_amount,
    }

    return render(request, "home/alltime.html", context)


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('partial_predictions_list.html', context, request)
        return JsonResponse({'html': html})

    return render(request, "home/alltime.html", context)


def latest_predictions_with_matches(request):
    """
    A view to update the latest predictions with matching results against the latest EuroMillions draw,
    ensuring that updates are only performed if the prediction date matches today's date.

    Args:
        request: The HTTP request object.

    Returns:
        redirect: Redirects to the previous page with appropriate messages depending on the action outcome.
    """

    if request.method == "POST":
        latest_date_query = Prediction.objects.aggregate(
            latest_date=Max("prediction_date")
        )
        latest_date_str = latest_date_query["latest_date"]

        # Convert latest_date from string to date object
        latest_date = datetime.strptime(latest_date_str, "%Y/%m/%d").date()

        # Check if latest_date is today's date
        if latest_date != datetime.today().date():
            messages.error(request, "Winning predicted patterns already checked!")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        latest_result = EuroMillionsResult.objects.latest("id")
        latest_predictions = Prediction.objects.filter(
            prediction_date=latest_date
        )

        for prediction in latest_predictions:
            prediction_numbers = {
                prediction.pred_ball_1,
                prediction.pred_ball_2,
                prediction.pred_ball_3,
                prediction.pred_ball_4,
                prediction.pred_ball_5,
            }
            draw_numbers = {
                latest_result.ball_1,
                latest_result.ball_2,
                latest_result.ball_3,
                latest_result.ball_4,
                latest_result.ball_5,
            }
            prediction_lucky_numbers = {
                prediction.pred_lucky_1,
                prediction.pred_lucky_2,
            }
            draw_lucky_numbers = {
                latest_result.lucky_star_1,
                latest_result.lucky_star_2,
            }

            common_numbers = prediction_numbers & draw_numbers
            common_lucky_numbers = prediction_lucky_numbers & draw_lucky_numbers

            # Determine the match type
            match_info = determine_match_type(
                len(common_numbers), len(common_lucky_numbers)
            )

            # Update the prediction instance
            if match_info:
                prediction.match_type = match_info
                prediction.winning_balls = format_numbers(common_numbers)
                prediction.winning_lucky_stars = format_numbers(common_lucky_numbers)
                prediction.save()

        messages.success(request, "Match results updated. Check the homepage for details.")
    else:
        messages.error(request, "This endpoint only accepts POST requests.")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))




def determine_match_type(num_common_numbers, num_common_lucky_numbers):
    match_cases = {
        (5, 2): "Match 5 + 2",
        (5, 0): "Match 5",
        (4, 2): "Match 4 + 2",
        (4, 1): "Match 4 + 1",
        (4, 0): "Match 4",
        (3, 2): "Match 3 + 2",
        (3, 1): "Match 3 + 1",
        (3, 0): "Match 3",
        (2, 2): "Match 2 + 2",
        (2, 1): "Match 2 + 1",
        (2, 0): "Match 2",
        (1, 2): "Match 1 + 2",
    }
    return match_cases.get((num_common_numbers, num_common_lucky_numbers))


def format_numbers(numbers):
    """Format a set of numbers as a comma-separated string, without extra commas for single numbers."""
    numbers_list = list(numbers)
    return ", ".join(map(str, numbers_list))


def latest_shuffled_predictions_with_matches(request):
    """
    A view to update the latest shuffled predictions with matching results against the latest EuroMillions draw,
    ensuring updates are only made if the prediction date is today.

    Args:
        request: The HTTP request object.

    Returns:
        redirect: Redirects to the previous page with appropriate messages depending on the action outcome.
    """

    if request.method == "POST":
        latest_date_query = ShuffledPrediction.objects.aggregate(
            latest_date=Max("prediction_date")
        )
        latest_date_str = latest_date_query["latest_date"]

        # Convert latest_date from string to date object
        latest_date = datetime.strptime(latest_date_str, "%Y/%m/%d").date()

        # Check if latest_date is today's date
        if latest_date != datetime.today().date():
            messages.error(request, "Winning predicted combinations already checked!")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        latest_result = EuroMillionsResult.objects.latest("id")
        latest_predictions = ShuffledPrediction.objects.filter(
            prediction_date=latest_date
        )

        for prediction in latest_predictions:
            prediction_numbers = {
                prediction.pred_ball_1,
                prediction.pred_ball_2,
                prediction.pred_ball_3,
                prediction.pred_ball_4,
                prediction.pred_ball_5,
            }
            draw_numbers = {
                latest_result.ball_1,
                latest_result.ball_2,
                latest_result.ball_3,
                latest_result.ball_4,
                latest_result.ball_5,
            }
            prediction_lucky_numbers = {
                prediction.pred_lucky_1,
                prediction.pred_lucky_2,
            }
            draw_lucky_numbers = {
                latest_result.lucky_star_1,
                latest_result.lucky_star_2,
            }

            common_numbers = prediction_numbers & draw_numbers
            common_lucky_numbers = prediction_lucky_numbers & draw_lucky_numbers

            # Determine the match type
            match_info = determine_match_type(
                len(common_numbers), len(common_lucky_numbers)
            )

            # Update the prediction instance
            if match_info:
                prediction.match_type = match_info
                prediction.winning_balls = format_numbers(common_numbers)
                prediction.winning_lucky_stars = format_numbers(common_lucky_numbers)
                prediction.save()

        messages.success(request, "Match results updated. Check the database for details.")
    else:
        messages.error(request, "This endpoint only accepts POST requests.")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def determine_match_type(num_common_numbers, num_common_lucky_numbers):
    match_cases = {
        (5, 2): "Match 5 + 2",
        (5, 0): "Match 5",
        (4, 2): "Match 4 + 2",
        (4, 1): "Match 4 + 1",
        (4, 0): "Match 4",
        (3, 2): "Match 3 + 2",
        (3, 1): "Match 3 + 1",
        (3, 0): "Match 3",
        (2, 2): "Match 2 + 2",
        (2, 1): "Match 2 + 1",
        (2, 0): "Match 2",
        (1, 2): "Match 1 + 2",
    }
    return match_cases.get((num_common_numbers, num_common_lucky_numbers))

def alltime_winning_shuffled_predictions_view(request):
    """
    View function to display all-time winning shuffled predictions with their associated images.

    This view retrieves shuffled predictions from the database where each prediction has a non-null 
    match type and a winning amount greater than zero. It calculates the total winning amount across 
    all such predictions and supports pagination for displaying these records.

    Args:
        request (HttpRequest): The request object used to fetch the number of records (`num_draws`) to 
        display per page from GET parameters. Defaults to 25 records per page if not specified. If 
        'all' is specified, all records are displayed on one page.

    Returns:
        HttpResponse: Renders the 'alltime_shuffled.html' template with context containing:
            - alltime_winning_shuffled_predictions: A paginated list of predictions with additional data 
              for displaying associated images.
            - total_winning_amount: The sum of win amounts across all eligible shuffled predictions.
    """
    num_draws = request.GET.get('num_draws', '25')
    
    base_query = ShuffledPrediction.objects.filter(
        match_type__isnull=False,
        win_amount__isnull=False,
        win_amount__gt=0
    )
    
    total_winning_amount = base_query.aggregate(
        total=Sum('win_amount')
    )['total'] or 0

    alltime_winning_shuffled_predictions = base_query.order_by("-draw_date")

    if num_draws != 'all':
        paginator = Paginator(alltime_winning_shuffled_predictions, int(num_draws))
        page_number = request.GET.get('page', 1)
        alltime_winning_shuffled_predictions = paginator.get_page(page_number)
    
    shuffled_predictions_with_images = []
    for prediction in alltime_winning_shuffled_predictions:
        pred_ball_images = [get_image_url(f"green{getattr(prediction, f'pred_ball_{i}'):02}")
                            if getattr(prediction, f'pred_ball_{i}') in map(int, prediction.winning_balls.split(",") if prediction.winning_balls else [])
                            else get_image_url(f"{getattr(prediction, f'pred_ball_{i}'):02}")
                            for i in range(1, 6)]

        pred_lucky_images = [get_image_url(f"greenstar{getattr(prediction, f'pred_lucky_{i}')}")
                             if getattr(prediction, f'pred_lucky_{i}') in map(int, prediction.winning_lucky_stars.split(",") if prediction.winning_lucky_stars else [])
                             else get_image_url(f"star{getattr(prediction, f'pred_lucky_{i}')}")
                             for i in range(1, 3)]

        shuffled_predictions_with_images.append({
            "prediction": prediction,
            "pred_ball_images": pred_ball_images,
            "pred_lucky_images": pred_lucky_images,
        })

    context = {
        "alltime_winning_shuffled_predictions": shuffled_predictions_with_images,
        "total_winning_amount": total_winning_amount,
    }

    return render(request, "home/alltime_shuffled.html", context)