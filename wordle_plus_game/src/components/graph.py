import pygame

class LineGraph:
    def __init__(self, width=800, height=600):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Score vs. Time for Different Difficulty Levels")
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        
    def create_graph(self, data):
        # Organizing data by difficulty levels
        difficulty_levels = {}
        for entry in data:
            difficulty = entry['Difficulty']
            if difficulty not in difficulty_levels:
                difficulty_levels[difficulty] = {'Score': [], 'Time': []}
            difficulty_levels[difficulty]['Score'].append(entry['Score'])
            difficulty_levels[difficulty]['Time'].append(entry['Time'])

        self.screen.fill((255, 255, 255))
        
        # graph dimensions and position
        graph_origin = (100, 500)  # Bottom-left corner of the graph
        graph_width = 600
        graph_height = 400
        
        # axes
        pygame.draw.line(self.screen, (0, 0, 0), graph_origin, (graph_origin[0] + graph_width, graph_origin[1]), 2)
        pygame.draw.line(self.screen, (0, 0, 0), graph_origin, (graph_origin[0], graph_origin[1] - graph_height), 2)
        
        # axis labels
        self.draw_text('Time', graph_origin[0] + graph_width // 2, graph_origin[1] + 20)
        self.draw_text('Score', graph_origin[0] - 50, graph_origin[1] - graph_height // 2, rotate=True)

        def find_tick_label(data, num_ticks):
            currMax = 0
            for entry in data:
                if entry['Time'] > currMax:
                    currMax = entry['Time']
            return currMax / num_ticks

        # tick marks and labels for x-axis (Time)
        x_ticks = 5  # x-axis ticks num
        for i in range(x_ticks + 1):
            x = graph_origin[0] + i * (graph_width / x_ticks)
            pygame.draw.line(self.screen, (0, 0, 0), (x, graph_origin[1]), (x, graph_origin[1] + 5), 2)
            tick_label = f"{int(i * find_tick_label(data, x_ticks))}"
            self.draw_text(tick_label, x - 10, graph_origin[1] + 10)
        
        # tick marks and labels for y-axis (Score)
        y_ticks = 5  # y-axis ticks num
        for i in range(y_ticks + 1):
            y = graph_origin[1] - i * (graph_height / y_ticks)
            pygame.draw.line(self.screen, (0, 0, 0), (graph_origin[0] - 5, y), (graph_origin[0], y), 2)
            tick_label = f"{int(i * find_tick_label(data, y_ticks))}"
            self.draw_text(tick_label, graph_origin[0] - 35, y - 10)

        # line graphs
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]  # color list
        color_index = 0
        
        for difficulty, values in difficulty_levels.items():
            time_values = values['Time']
            score_values = values['Score']
            
            # Normalize data for the graph dimensions
            max_time = max(max(time_values), 1)  
            max_score = max(max(score_values), 1)
            
            points = []
            for i in range(len(time_values)):
                x = graph_origin[0] + (time_values[i] / max_time) * graph_width
                y = graph_origin[1] - (score_values[i] / max_score) * graph_height
                points.append((x, y))
            
            # Draw lines if 2+ points
            if len(points) > 1:
                pygame.draw.lines(self.screen, colors[color_index % len(colors)], False, points, 2)
            elif len(points) == 1:  # if only 1 point, draw small circle
                pygame.draw.circle(self.screen, colors[color_index % len(colors)], points[0], 5)

            # Add label for each difficulty level
            self.draw_text(difficulty, graph_origin[0] + graph_width + 10, 20 + color_index * 30, color=colors[color_index % len(colors)])

            color_index += 1
        
        pygame.display.flip()  # Update the display

    def draw_text(self, text, x, y, rotate=False, color=(0, 0, 0)):
        text_surface = self.font.render(text, True, color)
        if rotate:
            text_surface = pygame.transform.rotate(text_surface, 90)
        self.screen.blit(text_surface, (x, y))