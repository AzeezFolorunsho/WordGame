import pygame
import sys
from wordle_plus_game.src.core.score_tracking import ScoreTracking
from wordle_plus_game.src.components.text import Text

class ScoreBoard:
    """
    Class to display the scoreboard with top scores and games played for a specific game mode.
    """

    def __init__(self, settings, game_mode):
        self.settings = settings
        self.game_mode = game_mode
        self.init_pygame()

        # Initialize the ScoreTracking object
        self.score_tracking = ScoreTracking()

        # Load top scores and games played for the specified game mode
        self.top_scores = self.load_top_scores_and_games_played()

    def init_pygame(self):
        """
        Initializes Pygame and sets up the screen.
        """
        self.screen_width = self.settings.get("General", "Screen Dimensions", {}).get("width", 1280)
        self.screen_height = self.settings.get("General", "Screen Dimensions", {}).get("height", 720)
        self.bg_color = self.settings.get("General", "Background Color", "#FFFFFF")

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Wordle Plus Scoreboard")
        self.screen.fill(self.bg_color)

        # Fonts
        self.title_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 50)
        self.font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 30)
        self.label_font = pygame.font.Font("wordle_plus_game/assets/FreeSansBold.otf", 25)

    def load_top_scores_and_games_played(self):
        """
        Loads the top scores and counts the games played for each difficulty level for the specified game mode.

        Returns:
            dict: A dictionary with difficulty levels as keys and tuples of (top score, games played) as values.
        """
        top_scores = {
            "Easy": (0, 0),
            "Normal": (0, 0),
            "Hard": (0, 0),
            "Ultra Hard": (0, 0)
        }

        # Load the top scores from the "Top Scores" sheet
        all_top_scores = self.score_tracking.load_scores('Top Scores')

        # Process the top scores for the specified game mode
        for score in all_top_scores:
            if score['Game mode'] == self.game_mode:
                difficulty = score['Difficulty']
                top_score = score['Score']

                if difficulty in top_scores:
                    if top_scores[difficulty][0] < top_score:
                        top_scores[difficulty] = (top_score, top_scores[difficulty][1])

        # Load game history to count the number of games played
        game_history = self.score_tracking.load_scores(self.game_mode)

        # Count games played for each difficulty level
        for game in game_history:
            difficulty = game['Difficulty']
            if difficulty in top_scores:
                top_scores[difficulty] = (
                    top_scores[difficulty][0],
                    top_scores[difficulty][1] + 1
                )

        return top_scores

    def display_scores(self):
        """
        Displays the top scores and games played for the game mode on the Pygame screen.
        """
        self.screen.fill(self.bg_color)

        # Display Game Mode Title
        title_text = f"{self.game_mode} Scoreboard"
        title = Text(title_text, self.title_font, 20, 20, text_color=(0, 0, 0))
        title.draw(self.screen)

        y_offset = 150
        box_width = 200
        box_height = 50
        label_y_offset = y_offset - 30

        for difficulty, (top_score, games_played) in self.top_scores.items():
            # Display Difficulty Level on the Left
            difficulty_text = Text(difficulty, self.font, 20, y_offset, text_color=(0, 0, 0))
            difficulty_text.draw(self.screen)

            # Draw Background Rectangles for Games Played and Top Score
            games_played_rect = pygame.Rect(400, y_offset, box_width, box_height)
            top_score_rect = pygame.Rect(650, y_offset, box_width, box_height)

            pygame.draw.rect(self.screen, (200, 200, 200), games_played_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), top_score_rect)

            # Label for Games Played and Top Score
            games_played_label = Text("Games Played", self.label_font, 400, label_y_offset, text_color=(0, 0, 0))
            top_score_label = Text("Top Score", self.label_font, 650, label_y_offset, text_color=(0, 0, 0))
            games_played_label.draw(self.screen)
            top_score_label.draw(self.screen)

            # Display the values for Games Played and Top Score inside the rectangles, centered
            games_played_text = Text(str(games_played), self.font, 400 + box_width / 2, y_offset + box_height / 2, text_color=(0, 0, 0), center=True)
            top_score_text = Text(str(top_score), self.font, 650 + box_width / 2, y_offset + box_height / 2, text_color=(0, 0, 0), center=True)
            games_played_text.draw(self.screen)
            top_score_text.draw(self.screen)

            # Increment y_offset for the next difficulty level
            y_offset += box_height + 40
            label_y_offset += box_height + 40

        pygame.display.flip()

    def run(self):
        """
        Runs the scoreboard display loop.
        """
        running = True
        while running:
            self.display_scores()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.update()
