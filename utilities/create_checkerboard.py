import numpy as np
import matplotlib.pyplot as plt
import cv2

def create_checkerboard(num_w, num_h, n, pad=0):
    board = np.zeros((num_h*n, num_w*n), dtype=np.uint8)
    for i in range(num_h):
        for j in range(num_w):
            if (i%2 != 0) and (j%2 != 0):
                continue
            if (i%2 != 1) and (j%2 != 1):
                continue
            board[i*n:(i*n)+n, j*n:(j*n)+n] = 255
    if pad != 0:
        board = np.pad(board, pad, constant_values=127)
    return board

if __name__ == "__main__":
    board = create_checkerboard(10, 10, 500, pad=100)
    cv2.imwrite('checkerboard.png', board)
    cv2.imshow("checkerboard", board)
    cv2.waitKey(0)
    cv2.destroyAllWindows()