from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re  # Import the regular expressions module

class Command(BaseCommand):
    help = 'Scrape EuroMillions results'

    def handle(self, *args, **kwargs):
        url = 'https://www.lottery.ie/accessible-results'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the section for EuroMillions results
        euromillions_section = soup.find('h3', string=lambda text: 'EuroMillions Results' in text)
        
        # Extract the date text using regex to remove unwanted text
        results_date = euromillions_section.get_text().strip()
        results_date = re.sub(r'EuroMillions Results\s*for\s*', '', results_date)  # Regex to remove the unwanted prefix

        # Parse and format the date
        date_object = datetime.strptime(results_date, '%a %d %B %Y')
        formatted_date = date_object.strftime('%Y-%m-%d')

        # Extract the winning numbers and lucky stars
        draw_results = euromillions_section.find_next_sibling('div', class_='draw-results')
        winning_numbers_section = draw_results.find('div', class_='winning-numbers')
        lucky_stars_section = draw_results.find('div', class_='luckystars')

        winning_numbers = [li.get_text() for li in winning_numbers_section.find_all('li')]
        lucky_stars = [li.get_text() for li in lucky_stars_section.find_all('li')]

        # Output results
        self.stdout.write(f"Date: {formatted_date}")
        self.stdout.write(f"Winning Numbers: {winning_numbers}")
        self.stdout.write(f"Lucky Stars: {lucky_stars}")
