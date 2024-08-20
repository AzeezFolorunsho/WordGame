import pygame
from wordle_plus_game.src.core.score_tracking import ScoreTracking
from wordle_plus_game.src.components.text import Text

class ScoreBoard:
    """
    Class to display the scoreboard with top scores and game history.
    """

    def __init__(self, settings):
        self.settings = settings
        self.init_pygame()

        # Initialize the ScoreTracking object
        self.score_tracking = ScoreTracking()

        # Load data from the Excel sheets
        self.game_history = self.score_tracking.load_scores('Classic')
        self.top_scores = self.score_tracking.load_scores('Top Scores')

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

    def display_scores(self):
        """
        Displays the scores on the Pygame screen.
        """
        self.screen.fill(self.bg_color)

        # Display Title
        title = Text("Wordle Plus Scoreboard", self.title_font, 20, 20, text_color=(0, 0, 0))
        title.draw(self.screen)

        # Display Top Scores
        top_scores_title = Text("Top Scores", self.font, 20, 100, text_color=(0, 0, 0))
        top_scores_title.draw(self.screen)
        y_offset = 150
        for score in self.top_scores:
            score_text = f"Game Mode: {score['Game mode']} | Difficulty: {score['Difficulty']} | Score: {score['Score']} | Time: {score['Time']}"
            score_line = Text(score_text, self.font, 20, y_offset, text_color=(0, 0, 0))
            score_line.draw(self.screen)
            y_offset += 40

        # Display Game History
        game_history_title = Text("Game History", self.font, 20, y_offset + 40, text_color=(0, 0, 0))
        game_history_title.draw(self.screen)
        y_offset += 80
        for game in self.game_history:
            game_text = f"Difficulty: {game['Difficulty']} | Score: {game['Score']} | Time: {game['Time']}"
            game_line = Text(game_text, self.font, 20, y_offset, text_color=(0, 0, 0))
            game_line.draw(self.screen)
            y_offset += 40

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
