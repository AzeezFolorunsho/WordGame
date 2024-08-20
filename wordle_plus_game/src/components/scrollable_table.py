import pygame

class ScrollableTable:
    """
    A class for creating and displaying a scrollable table in Pygame.

    Attributes:
        surface (pygame.Surface): The surface where the table will be drawn.
        position (tuple): The (x, y) position of the table.
        size (tuple): The (width, height) of the table.
        headers (list): List of column headers.
        data (list): List of data rows.
        font (pygame.font.Font): Font used for rendering text.
        row_height (int): Height of each table row.
        scroll_offset (int): Current vertical scroll offset.
    """

    def __init__(self, surface, position, size, headers, data, font, row_height):
        self.surface = surface
        self.x, self.y = position
        self.width, self.height = size
        self.headers = headers
        self.data = data
        self.font = font
        self.row_height = row_height
        self.scroll_offset = 0

        # Calculate column widths equally
        self.num_columns = len(headers)
        self.column_width = self.width // self.num_columns

        # Create a surface for the table content
        self.content_height = self.row_height * (len(self.data) + 1)  # +1 for headers
        self.content_surface = pygame.Surface((self.width, self.content_height))
        self.content_surface.fill((240, 240, 240))  # Light gray background

        self.draw_table_content()

    def draw_table_content(self):
        """
        Draws the content of the table on the off-screen surface.
        """
        # Draw headers
        for i, header in enumerate(self.headers):
            header_text = self.font.render(str(header), True, (0, 0, 0))
            header_rect = header_text.get_rect(center=(
                self.column_width * i + self.column_width / 2,
                self.row_height / 2
            ))
            self.content_surface.blit(header_text, header_rect)

            # Draw header separator
            pygame.draw.rect(
                self.content_surface,
                (200, 200, 200),
                pygame.Rect(self.column_width * i, 0, self.column_width, self.row_height),
                1
            )

        # Draw rows
        for row_index, row in enumerate(self.data):
            y_position = self.row_height * (row_index + 1)
            for col_index, item in enumerate(row):
                cell_text = self.font.render(str(item), True, (0, 0, 0))
                cell_rect = cell_text.get_rect(center=(
                    self.column_width * col_index + self.column_width / 2,
                    y_position + self.row_height / 2
                ))
                self.content_surface.blit(cell_text, cell_rect)

                # Draw cell separator
                pygame.draw.rect(
                    self.content_surface,
                    (200, 200, 200),
                    pygame.Rect(
                        self.column_width * col_index,
                        y_position,
                        self.column_width,
                        self.row_height
                    ),
                    1
                )

    def draw(self):
        """
        Draws the visible part of the table on the main surface.
        """
        # Create a clipping rect
        clip_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface.set_clip(clip_rect)

        # Blit the content surface with current scroll offset
        self.surface.blit(self.content_surface, (self.x, self.y - self.scroll_offset))

        # Reset clip
        self.surface.set_clip(None)

        # Draw border around the table
        pygame.draw.rect(self.surface, (0, 0, 0), clip_rect, 2)

    def scroll(self, direction):
        """
        Scrolls the table content up or down.

        Args:
            direction (int): The scroll direction (-1 for up, 1 for down).
        """
        max_scroll = max(0, self.content_height - self.height)
        new_scroll_y = self.scroll_offset + direction * self.row_height

        if 0 <= new_scroll_y <= max_scroll:
            self.scroll_offset = new_scroll_y

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
