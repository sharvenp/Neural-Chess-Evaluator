
import chess
import json
import time
import csv
import numpy as np
import pandas as pd

def process_data(data_path):
    print("Loading dataset...")

    data = pd.read_csv(data_path, nrows=1000000)
    fens = data["FEN"]
    evals = data["Evaluation"]
    print("Loaded dataset.")
    print("Processing dataset")

    start_time = time.time()
    count = 0

    x = []
    y = []

    for i in range(fens.size):

        try:
            processed_eval = str(evals[i])

            if ("#" in processed_eval): # Checkmate evaluation
                processed_eval = evals[i]
                processed_eval = processed_eval.replace("#", "")

                if (int(processed_eval) == 0):
                    processed_eval = 2 # Mate in 0 has score 2
                else:
                    processed_eval = 1 + (1 / int(processed_eval)) 
            else:
                processed_eval = int(evals[i])

            x.append(encode_board(fens[i]))
            y.append(processed_eval/1000)
            count += 1

            if count % 1000 == 0:
                print(f"Progress: {count} / {fens.size}")

        except Exception as e:
            print(f"Error processing: {e} \nFEN:{fens[i]}\nEval:{evals[i]}")

    print(f"Processed {count} examples.")
    print(f"Took {time.time() - start_time} seconds.")
    print("Writing processed dataset...")
    
    x = np.array(x).astype(np.byte)
    y = np.array(y)
    
    print(f"X shape: {x.shape} Y shape: {y.shape}")
    with open('../dataset/processed_X.npy', 'wb') as f:
        np.save(f, x)
    with open('../dataset/processed_Y.npy', 'wb') as f:
        np.save(f, y)

    print("Done.")

def encode_board(fen):

    result_dict = {
        "1-0": 1,
        "0-1": -1,
        "1/2-1/2": 0,
        "*": 0        
    }

    board = chess.Board(fen)
    result = result_dict[board.result()]
    
    turn_coeff = (2*int(board.turn) - 1)
    piece_id = [1, 2, 3, 4, 5, 6]
    color_id = [True, False]

    encoding = []

    for color in color_id:
        for piece in piece_id:
            feature = []
            for i in range(64):
                p = board.piece_at(i)
        
                if p is None:
                    feature.append(0)
                    continue

                if p.piece_type == piece and p.color == color:
                    feature.append(1)
                else:
                    feature.append(0)

            encoding.append(np.array(feature).reshape(8,8))


    for color in color_id:
        feature = []
        for i in range(64):
            attacked = board.is_attacked_by(color, i)
            if attacked:
                feature.append((2 * int(color) - 1))
            else:
                feature.append(0)

        encoding.append(np.array(feature).reshape(8,8))

    info_feature = [result]
    info_feature.append(turn_coeff)

    for color in color_id:
        info_feature.append((2*int(color) - 1) * (int(board.has_kingside_castling_rights(color))))
        info_feature.append((2*int(color) - 1) * (int(board.has_queenside_castling_rights(color))))
    
    info_feature.append(turn_coeff * int(board.is_check()))
    info_feature.append(turn_coeff * int(board.has_legal_en_passant()))

    for j in range(64 - len(info_feature)):
        info_feature.append(0)

    encoding.append(np.array(info_feature).reshape(8,8))
    encoding = np.array(encoding).astype(np.byte)

    return encoding

if __name__ == "__main__":
    process_data('../dataset/chessData.csv')