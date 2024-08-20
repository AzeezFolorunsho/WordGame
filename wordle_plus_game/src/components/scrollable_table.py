import pygame

class ScrollableTable:
    """
    A class for creating and displaying a scrollable table in Pygame.

    Attributes:
        screen (pygame.Surface): The Pygame screen surface where the table will be displayed.
        font (pygame.font.Font): The font used to render the table text.
        x (int): The x-coordinate of the top-left corner of the table.
        y (int): The y-coordinate of the top-left corner of the table.
        width (int): The width of the table.
        height (int): The height of the table (visible area).
        row_height (int): The height of each row in the table.
        data (list of list): The data to be displayed in the table.
        scroll_y (int): The current scroll position.
        max_visible_rows (int): The maximum number of rows that can be displayed without scrolling.
    """

    def __init__(self, screen, font, x, y, width, height, row_height, data):
        self.screen = screen
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.row_height = row_height
        self.data = data

        self.scroll_y = 0
        self.max_visible_rows = height // row_height

    def draw(self):
        """
        Draws the scrollable table on the Pygame screen.
        """
        # Calculate the visible rows
        start_row = self.scroll_y // self.row_height
        end_row = start_row + self.max_visible_rows

        # Draw visible rows
        for i, row_data in enumerate(self.data[start_row:end_row]):
            row_y = self.y + i * self.row_height
            self.draw_row(row_data, row_y)

        # Draw the border for the table
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

    def draw_row(self, row_data, row_y):
        """
        Draws a single row of data on the screen.

        Args:
            row_data (list): The data for the row to be drawn.
            row_y (int): The y-coordinate of the row.
        """
        col_width = self.width // len(row_data)

        for i, cell_data in enumerate(row_data):
            cell_x = self.x + i * col_width
            cell_rect = pygame.Rect(cell_x, row_y, col_width, self.row_height)
            pygame.draw.rect(self.screen, (200, 200, 200), cell_rect)
            pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 1)

            cell_text = self.font.render(str(cell_data), True, (0, 0, 0))
            cell_text_rect = cell_text.get_rect(center=cell_rect.center)
            self.screen.blit(cell_text, cell_text_rect)

    def scroll(self, direction):
        """
        Scrolls the table content up or down.

        Args:
            direction (int): The scroll direction (-1 for up, 1 for down).
        """
        max_scroll = max(0, len(self.data) * self.row_height - self.height)
        new_scroll_y = self.scroll_y + direction * self.row_height

        if 0 <= new_scroll_y <= max_scroll:
            self.scroll_y = new_scroll_y

    def handle_event(self, event):
        """
        Handles Pygame events for scrolling.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll(-1)
            elif event.button == 5:  # Scroll down
                self.scroll(1)