from django.core.management.base import BaseCommand

from analytics.services.team_strength_service import calculate_team_strengths


class Command(BaseCommand):

    help = "Calculate team attack and defence strengths"

    def handle(self, *args, **kwargs):

        calculate_team_strengths()

        self.stdout.write(
            self.style.SUCCESS(
                "Team strengths calculated successfully"
            )
        )