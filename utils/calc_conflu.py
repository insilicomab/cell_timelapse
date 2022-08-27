from turtle import width
import pandas as pd
import numpy as np
import cv2


def calc_conflu(filename, output):

    # read video
    cap = cv2.VideoCapture(f'./input/movie/raw/{filename}')

    # config
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    writer = cv2.VideoWriter(
        f'./output/movie/{output}.mp4',
        fourcc,
        fps,
        (width, height)
    )

    # kernel_size
    KERNEL_SIZE = 15

    # calculated confluency list
    conflu_list = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        """
        make a video
        """

        # gray scale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # binarization using Otsu's method
        _, th = cv2.threshold(frame_gray, 0, 255,
                              cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # configure the kernel
        kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

        # morphological transformation(Dilation)
        th_dilation = cv2.dilate(th, kernel, iterations=1)

        # contour extraction
        contours, hierarchy = cv2.findContours(th_dilation,
                                               cv2.RETR_LIST,
                                               cv2.CHAIN_APPROX_NONE)

        # draw the contours on the source image
        img_contour = cv2.drawContours(
            frame.copy(), contours, -1, (0, 255, 0), 2)

        writer.write(img_contour)

        """
        calc_confluency
        """

        # total number of pixels
        whole_area = th_dilation.size

        # number of zero area pixels
        white_area = cv2.countNonZero(th_dilation)

        # calculate confluency
        confluency = int(white_area / whole_area * 100)

        # append to list
        conflu_list.append(confluency)

    # make dataframe
    df = pd.DataFrame(conflu_list, columns=['confluency'])
    df['frame'] = df.index
    df.set_index('frame', inplace=True)
    df.to_csv(f'./output/csv/{output}.csv')

    writer.release()

    return conflu_list
