import chess
import numpy as np


class Util:

    @staticmethod
    def convert_to_bitmap_additional(board):

        result_dict = {
            "1-0": 1,
            "0-1": -1,
            "1/2-1/2": 0,
            "*": 0
        }

        result = result_dict[board.result()]

        turn_coeff = (2 * int(board.turn) - 1)
        piece_id = [1, 2, 3, 4, 5, 6]
        color_id = [True, False]

        encoding = []

        for color in color_id:
            for piece in piece_id:
                for i in range(64):
                    p = board.piece_at(i)

                    if p is None:
                        encoding.append(0)
                        continue

                    if p.piece_type == piece and p.color == color:
                        encoding.append(1)
                    else:
                        encoding.append(0)

        for color in color_id:
            for i in range(64):
                attacked = board.is_attacked_by(color, i)
                if attacked:
                    encoding.append((2 * int(color) - 1))
                else:
                    encoding.append(0)

        encoding.append(result)
        encoding.append(turn_coeff)

        for color in color_id:
            encoding.append((2 * int(color) - 1) * (int(board.has_kingside_castling_rights(color))))
            encoding.append((2 * int(color) - 1) * (int(board.has_queenside_castling_rights(color))))

        encoding.append(turn_coeff * int(board.is_check()))
        encoding.append(turn_coeff * int(board.has_legal_en_passant()))

        return np.array(encoding).astype(np.byte)

    @staticmethod
    def convert_to_bitmap(board):

        bitmap = []

        piece_id = [1, 2, 3, 4, 5, 6]
        color_id = [True, False]

        for color in color_id:
            for piece in piece_id:
                for i in range(64):
                    p = board.piece_at(i)

                    if p is None:
                        bitmap.append(0)
                        continue

                    if p.piece_type == piece and p.color == color:
                        bitmap.append(1)
                    else:
                        bitmap.append(0)

        for color in color_id:
            bitmap.append(int(board.has_kingside_castling_rights(color)))
            bitmap.append(int(board.has_queenside_castling_rights(color)))

        return np.array(bitmap).reshape(1, -1)
