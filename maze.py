"""Implementation of the Maze ADT using a 2-D array."""

from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols) -> None:
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self) -> int:
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self) -> int:
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col) -> None:
        """Fills the indicated cell with a "wall" marker."""
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col) -> None:
        """Sets the starting cell position."""
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col) -> None:
        """Sets the exit cell position."""
        assert 0 <= row < self.num_rows() and \
               0 <= col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self) -> bool:
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        path = Stack()
        path.push(self._start_cell)

        current_position = self._start_cell
        row = current_position.row
        col = current_position.col

        modifiers = ((-1, 0), (0, 1), (1, 0), (0, -1))

        while not (
                self._exit_found(row, col)
                or path.is_empty()
        ):
            move_found = False

            for row_mod, col_mod in modifiers:
                if move_found:
                    break
                if (
                        self._valid_move(row + row_mod, col + col_mod)
                        and self._maze_cells[row + row_mod, col + col_mod]
                        != self.MAZE_WALL
                        and self._maze_cells[row + row_mod, col + col_mod]
                        != self.TRIED_TOKEN
                        and self._maze_cells[row + row_mod, col + col_mod]
                        != self.PATH_TOKEN
                ):
                    self._mark_path(row, col)
                    path.push(current_position)

                    current_position = _CellPosition(row + row_mod, col + col_mod)
                    row = current_position.row
                    col = current_position.col

                    move_found = True

            if not move_found:
                self._mark_tried(row, col)

                current_position = path.pop()

                row = current_position.row
                col = current_position.col

        if path.is_empty():
            self._mark_tried(row, col)
            return False

        self._mark_path(row, col)
        return True

    def reset(self) -> None:
        """Resets the maze by removing all "path" and "tried" tokens."""
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if self._maze_cells[row, col] in \
                        {self.PATH_TOKEN, self.TRIED_TOKEN}:
                    self._maze_cells[row, col] = None

        return self

    def __str__(self) -> str:
        """Returns a text-based representation of the maze."""
        representation = ""

        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                if self._maze_cells[row, col]:
                    representation += self._maze_cells[row, col] + " "
                else:
                    representation += "_ "
            representation += "\n"

        return representation[:-1]

    def _valid_move(self, row, col) -> bool:
        """Returns True if the given cell position is a valid move."""
        return (
                0 <= row < self.num_rows()
                and 0 <= col < self.num_cols()
                and self._maze_cells[row, col] is None
        )

    def _exit_found(self, row, col) -> bool:
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col) -> None:
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col) -> None:
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition:
    """Private storage class for holding a cell position."""

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
