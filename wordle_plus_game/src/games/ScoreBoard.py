import pygame
import sys
from wordle_plus_game.src.core.score_tracking import ScoreTracking
from wordle_plus_game.src.components.text import Text
from wordle_plus_game.src.components.scrollable_table import ScrollableTable

class ScoreBoard:
    """
    Class to display the scoreboard with top scores and game history for a specific game mode.
    """

    def __init__(self, settings, game_mode):
        self.settings = settings
        self.game_mode = game_mode
        self.init_pygame()
        self.load_data()
        self.create_ui_elements()

    def init_pygame(self):
        """
        Initializes Pygame and sets up the screen.
        """
        pygame.init()

        # Screen dimensions and settings
        self.screen_width = self.settings.get("General", "Screen Dimensions", {}).get("width", 1280)
        self.screen_height = self.settings.get("General", "Screen Dimensions", {}).get("height", 720)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption(f"{self.game_mode} Scoreboard")
        self.bg_color = pygame.Color(self.settings.get("General", "Background Color", "#FFFFFF"))
        self.screen.fill(self.bg_color)

        # Font sizes based on screen width
        self.title_font = pygame.font.Font(None, int(self.screen_width * 0.04))
        self.font = pygame.font.Font(None, int(self.screen_width * 0.025))
        self.label_font = pygame.font.Font(None, int(self.screen_width * 0.022))

        # Margins and spacing
        self.margin = int(self.screen_width * 0.05)
        self.spacing = int(self.screen_height * 0.02)

    def load_data(self):
        """
        Loads the necessary data for the scoreboard.
        """
        self.score_tracking = ScoreTracking()

        # Load top scores and games played
        self.top_scores = self.load_top_scores_and_games_played()

        # Load game history
        self.game_history = self.load_game_history()

    def load_top_scores_and_games_played(self):
        """
        Loads the top scores and counts the games played for each difficulty level.
        """
        difficulties = ["Easy", "Normal", "Hard", "Ultra Hard"]
        top_scores = {difficulty: {'top_score': 0, 'games_played': 0} for difficulty in difficulties}

        # Load all scores
        all_scores = self.score_tracking.load_scores('Top Scores')
        game_history = self.score_tracking.load_scores(self.game_mode)

        for score in all_scores:
            if score['Game mode'] == self.game_mode and score['Difficulty'] in top_scores:
                current_top = top_scores[score['Difficulty']]['top_score']
                if score['Score'] > current_top:
                    top_scores[score['Difficulty']]['top_score'] = score['Score']

        for game in game_history:
            if game['Difficulty'] in top_scores:
                top_scores[game['Difficulty']]['games_played'] += 1

        return top_scores

    def load_game_history(self):
        """
        Loads game history data.
        """
        history_data = self.score_tracking.load_scores(self.game_mode)
        game_history = [["Difficulty", "Score", "Time"]]

        for game in history_data:
            game_history.append([game['Difficulty'], game['Score'], game['Time']])

        return game_history

    def create_ui_elements(self):
        """
        Creates and positions all UI elements.
        """
        # Title
        title_text = f"{self.game_mode} Scoreboard"
        self.title = Text(
            title_text,
            self.title_font,
            self.screen_width / 2,  # x position
            self.margin,  # y position
            text_color=(0, 0, 0),
            center=True
        )

        # Top Scores Section
        self.top_scores_section = []
        section_start_y = self.margin + self.title_font.get_height() + self.spacing

        label_width = self.screen_width * 0.2
        box_width = self.screen_width * 0.15

        for index, (difficulty, scores) in enumerate(self.top_scores.items()):
            row_y = section_start_y + index * (self.font.get_height() + self.spacing * 2)

            difficulty_text = Text(
                difficulty,
                self.font,
                self.margin,  # x position
                row_y,  # y position
                text_color=(0, 0, 0)
            )

            games_played_x = self.screen_width - self.margin - 2 * box_width - self.spacing
            top_score_x = self.screen_width - self.margin - box_width

            games_played_box = pygame.Rect(games_played_x, row_y, box_width, self.font.get_height() + self.spacing)
            top_score_box = pygame.Rect(top_score_x, row_y, box_width, self.font.get_height() + self.spacing)

            games_played_text = Text(
                str(scores['games_played']),
                self.font,
                games_played_box.centerx,  # x position
                games_played_box.centery,  # y position
                text_color=(0, 0, 0),
                center=True
            )

            top_score_text = Text(
                str(scores['top_score']),
                self.font,
                top_score_box.centerx,  # x position
                top_score_box.centery,  # y position
                text_color=(0, 0, 0),
                center=True
            )

            self.top_scores_section.append({
                'difficulty_text': difficulty_text,
                'games_played_box': games_played_box,
                'games_played_text': games_played_text,
                'top_score_box': top_score_box,
                'top_score_text': top_score_text
            })

        # Scrollable Table
        table_y = section_start_y + len(self.top_scores) * (self.font.get_height() + self.spacing * 2) + self.spacing
        table_height = self.screen_height - table_y - self.margin
        table_width = self.screen_width - 2 * self.margin

        # Since game_history is a list, pass it directly
        self.scrollable_table = ScrollableTable(
            surface=self.screen,
            position=(self.margin, table_y),
            size=(table_width, table_height),
            headers=self.game_history[0],  # First row is the header
            data=self.game_history[1:],    # The rest are data rows
            font=self.font,
            row_height=self.font.get_height() + self.spacing
        )

    def draw(self):
        """
        Draws all UI elements onto the screen.
        """
        self.screen.fill(self.bg_color)
        self.title.draw(self.screen)

        for section in self.top_scores_section:
            section['difficulty_text'].draw(self.screen)
            pygame.draw.rect(self.screen, (220, 220, 220), section['games_played_box'])
            pygame.draw.rect(self.screen, (0, 0, 0), section['games_played_box'], 2)
            section['games_played_text'].draw(self.screen)

            pygame.draw.rect(self.screen, (220, 220, 220), section['top_score_box'])
            pygame.draw.rect(self.screen, (0, 0, 0), section['top_score_box'], 2)
            section['top_score_text'].draw(self.screen)

        self.scrollable_table.draw()
        pygame.display.flip()

    def run(self):
        """
        Runs the scoreboard display loop.
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen_width, self.screen_height = event.size
                    self.init_pygame()
                    self.create_ui_elements()
                else:
                    self.scrollable_table.handle_event(event)
            clock.tick(60)

        pygame.quit()
        sys.exit()
