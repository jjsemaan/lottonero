from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from scraping.models import EuroMillionsResult

"""
    A Django management command to scrape the latest EuroMillions results
    from the official lottery website. This command extracts the draw date,
    winning numbers, and lucky stars from the EuroMillions section of the
    lottery results page and writes them to the db.

    Attributes:
        help (str): Provides a brief description of the command's
        purpose, which is accessible through the command-line interface.

    Methods:
        handle(*args, **kwargs): The main entry point for the command.
                                 It performs the scraping, parsing,
                                 and output of the EuroMillions results.

    Command to run this code from the terminal:
        python manage.py scrape_euromillions

    """


class Command(BaseCommand):
    help = "Scrape EuroMillions results"

    def handle(self, *args, **kwargs):
        url = "https://www.lottery.ie/accessible-results"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        euromillions_section = soup.find(
            "h3", string=lambda text: "EuroMillions Results" in text
        )

        # Extract the date text using regex to remove unwanted text
        results_date = euromillions_section.get_text().strip()
        results_date = re.sub(
            r"EuroMillions Results\s*for\s*", "", results_date
        )

        date_object = datetime.strptime(results_date, "%a %d %B %Y")
        formatted_date = date_object.strftime("%Y/%m/%d")

        if EuroMillionsResult.objects.filter(
            draw_date=formatted_date
        ).exists():
            self.stdout.write(
                f"Results for {formatted_date} have already been scraped."
            )
            return

        draw_results = euromillions_section.find_next_sibling(
            "div", class_="draw-results"
        )
        winning_numbers_section = draw_results.find(
            "div", class_="winning-numbers"
        )
        lucky_stars_section = draw_results.find("div", class_="luckystars")

        winning_numbers = [
            int(li.get_text()) for li in winning_numbers_section.find_all("li")
        ]
        lucky_stars = [
            int(li.get_text()) for li in lucky_stars_section.find_all("li")
        ]

        jackpot_details = draw_results.find("div", class_="jackpot").get_text(
            strip=True
        )
        prize_breakdown_paragraph = draw_results.find("p").get_text(strip=True)

        result = EuroMillionsResult(
            draw_date=formatted_date,
            ball_1=winning_numbers[0],
            ball_2=winning_numbers[1],
            ball_3=winning_numbers[2],
            ball_4=winning_numbers[3],
            ball_5=winning_numbers[4],
            lucky_star_1=lucky_stars[0],
            lucky_star_2=lucky_stars[1],
            jackpot=jackpot_details,
            prize_breakdown=prize_breakdown_paragraph,
        )
        result.save()

        self.stdout.write(f"Date: {formatted_date}")
        self.stdout.write(f"Winning Numbers: {winning_numbers}")
        self.stdout.write(f"Lucky Stars: {lucky_stars}")
        self.stdout.write(f"Jackpot Details: {jackpot_details}")
        self.stdout.write(f"Prize Breakdown: {prize_breakdown_paragraph}")

        self.stdout.write("Results successfully saved to the database.")