
import chess
import json
import time
import csv
import numpy as np

def process_data(data_path, save_file):
    print("Loading dataset...")

    processed_bitmaps = []
    processed_evals = []

    data = pd.read_csv(data_path, nrows=1000000)
    fens = data["FEN"]
    evals = data["Evaluation"]

    print("Loaded dataset.")
    print("Processing dataset")

    start_time = time.time()
    count = 0

    for i in range(fens.size):

        try:
            processed_eval = str(evals[i])

            if ("#" in processed_eval): # Checkmate evaluation
                processed_eval = evals[i]
                processed_eval = processed_eval.replace("#", "")

                if (int(processed_eval) == 0):
                    processed_eval = 200000000 # Mate in 0 has score 200000000
                else:
                    processed_eval = 100000000 / int(processed_eval) 
            else:
                processed_eval = int(evals[i])

            processed_bitmaps.append(convert_board_to_bitmap(fens[i]))
            processed_evals.append(processed_eval)
            count += 1

            if count % 1000 == 0:
                print(f"Progress: {count} / {fens.size}")

        except Exception as e:
            print(f"Error processing: {e} \nFEN:{fens[i]}\nEval:{evals[i]}")


    print(f"Processed {count} examples.")
    print(f"Took {time.time() - start_time} seconds.")
    print("Writing processed dataset...")

    save_data = {'Bitmap': processed_bitmaps, 'Evaluation': processed_evals}  
    df = pd.DataFrame(save_data)
    
    df.to_csv(save_file)

    print("Done.")


def convert_board_to_bitmap(fen):

    bitmap = ""
    board = chess.Board(fen)

    piece_id = [1, 2, 3, 4, 5, 6]
    color_id = [True, False]

    for color in color_id:
        for piece in piece_id:
            for i in range(64):
                p = board.piece_at(i)
                
                if p is None:
                    bitmap += "0"
                    continue

                if p.piece_type == piece and p.color == color:
                    bitmap += "1"
                else:
                    bitmap += "0"

    for color in color_id:
        bitmap += str(int(board.has_kingside_castling_rights(color)))
        bitmap += str(int(board.has_queenside_castling_rights(color)))

    return bitmap

def encode_board(fen):

    board = chess.Board(fen)

    piece_id = [1, 2, 3, 4, 5, 6]
    color_id = [True, False]

    encoding = []

    for i in range(64):
        p = board.piece_at(i)
        
        if p is None:
            encoding.append(0)
            continue

        encoding.append((2*int(p.color) - 1) * (p.piece_type/6))

    print(encoding)

    return np.array(encoding)

def reserialize_data(csv_file):
    dataset = []
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        
        i = 0
        for row in reader:
            dataset.append([BoardBitmapConverter.convertStringtoBitMap(row[1]), float(row[2])])
            i += 1

            if i % 1000 == 0:
                print(f"Processed: {i} lines.")


    np.save(f"../dataset/serialized_dataset.npy", dataset)
    print("Saved.")

if __name__ == "__main__":
    # process_data('../dataset/chessData.csv', "../dataset/processed_data.csv")
    # reserialize_data("../dataset/processed_data_1M.csv")
    encode_board("r1bqkbnr/1ppp1Qpp/p1n5/4p3/4P3/3B4/PPPP1PPP/RNB1K1NR b KQkq - 0 1")