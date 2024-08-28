import pygame

class LineGraph:
    def __init__(self, x, y, screen, width=500, height=400):
        """
        Initializes the LineGraph object with position, dimensions, and display screen.

        Args:
            x (int): The x-coordinate for the top-left corner of the graph area.
            y (int): The y-coordinate for the top-left corner of the graph area.
            width (int): The width of the graph area.
            height (int): The height of the graph area.
            screen (pygame.Surface): The Pygame surface where the graph will be drawn.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)

    def create_graph(self, data):
        """
        Draws a line graph based on the provided data.

        Args:
            data (list of dicts): A list of dictionaries containing 'Difficulty', 'Score', and 'Time' keys.
        """
        # Organizing data by difficulty levels
        difficulty_levels = self._organize_data_by_difficulty(data)

        # Graph dimensions and position
        graph_origin = (self.x + 50, self.y + self.height - 50)  # Bottom-left corner of the graph
        graph_width = self.width - 100  # Adjust graph width to fit within the designated area
        graph_height = self.height - 100  # Adjust graph height to fit within the designated area

        # Draw axes
        self._draw_axes(graph_origin, graph_width, graph_height)

        # Draw tick marks and labels for both axes
        self._draw_ticks_and_labels(graph_origin, graph_width, graph_height, data)

        # Draw line graphs for each difficulty level
        self._draw_line_graphs(graph_origin, graph_width, graph_height, difficulty_levels)

    def _organize_data_by_difficulty(self, data):
        """
        Organizes data into a dictionary grouped by difficulty level.

        Args:
            data (list of dicts): The data to be organized.

        Returns:
            dict: A dictionary with difficulty levels as keys and corresponding scores and times as values.
        """
        difficulty_levels = {}
        for entry in data:
            difficulty = entry['Difficulty']
            if difficulty not in difficulty_levels:
                difficulty_levels[difficulty] = {'Score': [], 'Time': []}
            difficulty_levels[difficulty]['Score'].append(entry['Score'])
            difficulty_levels[difficulty]['Time'].append(entry['Time'])
        return difficulty_levels

    def _draw_axes(self, graph_origin, graph_width, graph_height):
        """
        Draws the x and y axes on the graph.

        Args:
            graph_origin (tuple): The origin point (bottom-left corner) of the graph.
            graph_width (int): The width of the graph.
            graph_height (int): The height of the graph.
        """
        # X-axis
        pygame.draw.line(self.screen, (0, 0, 0), graph_origin, (graph_origin[0] + graph_width, graph_origin[1]), 2)
        # Y-axis
        pygame.draw.line(self.screen, (0, 0, 0), graph_origin, (graph_origin[0], graph_origin[1] - graph_height), 2)

        # Axis labels
        self.draw_text('Time', graph_origin[0] + graph_width // 2, graph_origin[1] + 20)
        self.draw_text('Score', graph_origin[0] - 50, graph_origin[1] - graph_height // 2, rotate=True)

    def _draw_ticks_and_labels(self, graph_origin, graph_width, graph_height, data):
        """
        Draws tick marks and labels for both x and y axes.

        Args:
            graph_origin (tuple): The origin point (bottom-left corner) of the graph.
            graph_width (int): The width of the graph.
            graph_height (int): The height of the graph.
            data (list of dicts): The data used to calculate tick mark labels.
        """
        x_ticks = 5  # Number of tick marks on the x-axis
        y_ticks = 5  # Number of tick marks on the y-axis

        max_time = max(entry['Time'] for entry in data)
        max_score = max(entry['Score'] for entry in data)

        # Draw x-axis tick marks and labels
        for i in range(x_ticks + 1):
            x = graph_origin[0] + i * (graph_width / x_ticks)
            pygame.draw.line(self.screen, (0, 0, 0), (x, graph_origin[1]), (x, graph_origin[1] + 5), 2)
            tick_label = f"{int(i * (max_time / x_ticks))}"
            self.draw_text(tick_label, x - 10, graph_origin[1] + 10)

        # Draw y-axis tick marks and labels
        for i in range(y_ticks + 1):
            y = graph_origin[1] - i * (graph_height / y_ticks)
            pygame.draw.line(self.screen, (0, 0, 0), (graph_origin[0] - 5, y), (graph_origin[0], y), 2)
            tick_label = f"{int(i * (max_score / y_ticks))}"
            self.draw_text(tick_label, graph_origin[0] - 35, y - 10)

    def _draw_line_graphs(self, graph_origin, graph_width, graph_height, difficulty_levels):
        """
        Draws line graphs for each difficulty level.

        Args:
            graph_origin (tuple): The origin point (bottom-left corner) of the graph.
            graph_width (int): The width of the graph.
            graph_height (int): The height of the graph.
            difficulty_levels (dict): A dictionary of difficulty levels and their corresponding data.
        """
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]  # Colors for each difficulty level
        color_index = 0

        for difficulty, values in difficulty_levels.items():
            time_values = values['Time']
            score_values = values['Score']

            max_time = max(max(time_values), 1)
            max_score = max(max(score_values), 1)

            points = [(graph_origin[0] + (time / max_time) * graph_width, 
                       graph_origin[1] - (score / max_score) * graph_height) 
                      for time, score in zip(time_values, score_values)]

            if len(points) > 1:
                pygame.draw.lines(self.screen, colors[color_index % len(colors)], False, points, 2)
            elif len(points) == 1:
                pygame.draw.circle(self.screen, colors[color_index % len(colors)], points[0], 5)

            self.draw_text(difficulty, graph_origin[0] + graph_width + 10, self.y + 20 + color_index * 30, color=colors[color_index % len(colors)])
            color_index += 1

    def draw_text(self, text, x, y, rotate=False, color=(0, 0, 0)):
        """
        Draws text on the screen at the specified coordinates.

        Args:
            text (str): The text to be displayed.
            x (int): The x-coordinate for the text.
            y (int): The y-coordinate for the text.
            rotate (bool): Whether to rotate the text by 90 degrees.
            color (tuple): The color of the text.
        """
        text_surface = self.font.render(text, True, color)
        if rotate:
            text_surface = pygame.transform.rotate(text_surface, 90)
        self.screen.blit(text_surface, (x, y))
