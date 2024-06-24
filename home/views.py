from django.shortcuts import render
from scraping.models import EuroMillionsResult
from predictions.models import Prediction, ShuffledPrediction, UploadImageModel
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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

    # Get the latest prediction date with non-null match_type
    latest_date = Prediction.objects.filter(
        match_type__isnull=False
    ).aggregate(latest_date=Max("prediction_date"))["latest_date"]

    # Fetch all predictions with the latest date and non-null match_type
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

    # Get the latest shuffled prediction date with non-null match_type
    latest_shuffled_date = ShuffledPrediction.objects.filter(
        match_type__isnull=False
    ).aggregate(latest_date=Max("prediction_date"))["latest_date"]

    # Fetch all shuffled predictions with the latest date and non-null match_type
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

from django.core.paginator import Paginator
from django.db.models import Sum

def alltime_winning_predictions_view(request):
    num_draws = request.GET.get('num_draws', '25')
    
    # Fetch all predictions that have a non-null match type, ordered by draw date
    alltime_winning_predictions = Prediction.objects.filter(
        match_type__isnull=False
    ).order_by("-draw_date")
    
    # Calculate the total winning amount for all records using an efficient database query
    total_winning_amount = alltime_winning_predictions.aggregate(
        total=Sum('win_amount')
    )['total'] or 0

    # Apply pagination if not showing 'all'
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
    A view to update the latest predictions with matching results against the latest EuroMillions draw.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A simple text response indicating whether the match results were updated or if
        the endpoint was accessed with a non-POST request.
    """

    if request.method == "POST":
        latest_result = EuroMillionsResult.objects.latest("id")
        latest_date = Prediction.objects.aggregate(
            latest_date=Max("prediction_date")
        )["latest_date"]
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
            common_lucky_numbers = (
                prediction_lucky_numbers & draw_lucky_numbers
            )

            # Determine the match type
            match_info = determine_match_type(
                len(common_numbers), len(common_lucky_numbers)
            )

            # Update the prediction instance
            if match_info:
                prediction.match_type = match_info
                prediction.winning_balls = format_numbers(common_numbers)
                prediction.winning_lucky_stars = format_numbers(
                    common_lucky_numbers
                )
                prediction.save()

        return HttpResponse(
            "Match results updated. Check the database for details."
        )
    else:
        return HttpResponse("This endpoint only accepts POST requests.")


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
    A view to update the latest shuffled predictions with matching results against the latest EuroMillions draw.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A simple text response indicating whether the match results were updated or if
        the endpoint was accessed with a non-POST request.
    """

    if request.method == "POST":
        latest_result = EuroMillionsResult.objects.latest("id")
        latest_date = ShuffledPrediction.objects.aggregate(
            latest_date=Max("prediction_date")
        )["latest_date"]
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
            common_lucky_numbers = (
                prediction_lucky_numbers & draw_lucky_numbers
            )

            # Determine the match type
            match_info = determine_match_type(
                len(common_numbers), len(common_lucky_numbers)
            )

            # Update the prediction instance
            if match_info:
                prediction.match_type = match_info
                prediction.winning_balls = format_numbers(common_numbers)
                prediction.winning_lucky_stars = format_numbers(
                    common_lucky_numbers
                )
                prediction.save()

        return HttpResponse(
            "Match results updated. Check the database for details."
        )
    else:
        return HttpResponse("This endpoint only accepts POST requests.")


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
