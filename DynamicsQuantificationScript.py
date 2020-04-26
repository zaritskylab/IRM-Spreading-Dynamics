import os
from math import factorial
import numpy as np
import pandas as pd
import cv2 as cv
import matplotlib.pyplot as plt


class DynamicsQuantification:
    """
    Quantifies the attachment & detachment events in a given video.
    auto-calculates the background threshold if not given the threshold argument (see help & readme)
    FIRST 10 FRAMES OF IMAGERY MUST BE ONLY BACKGROUND, no visible platelets.
    """

    def __init__(self, file_path, **kwargs):
        def get_background_threshold(file_path: str):
            """
            FIRST 10 FRAMES MUST BE ONLY BACKGROUND
            reads 10 first frames, calculates average and standard deviation of background noise.
            :param video_cap:
            :return:
            """
            vid_cap = cv.VideoCapture(file_path)
            frame_width = int(vid_cap.get(cv.CAP_PROP_FRAME_WIDTH))
            frame_height = int(vid_cap.get(cv.CAP_PROP_FRAME_HEIGHT))
            detachment_events = list()
            attachment_events = list()
            ret, current_frame = vid_cap.read()
            next_frame = None
            frame_ctr = 0
            while frame_ctr < 9 and ret:
                if next_frame is None:
                    ret, next_frame = vid_cap.read()

                dynamics_matrix = next_frame.astype(float)[:, :, 0] - current_frame.astype(float)[:, :, 0]
                detachment_events = detachment_events + [x for x in dynamics_matrix[dynamics_matrix < 0]]
                attachment_events = attachment_events + [x for x in dynamics_matrix[dynamics_matrix > 0]]
                ret, current_frame = vid_cap.read()
                ret, next_frame = vid_cap.read()

                frame_ctr += 1

            detachment_events = np.array(detachment_events)
            attachment_events = np.array(attachment_events)
            attach_threshold = np.average(detachment_events) - np.std(detachment_events)
            detach_threshold = np.average(attachment_events) + np.std(attachment_events)

            return attach_threshold, detach_threshold

        print(kwargs)

        if kwargs.get('-time_scale') is not None:
            self.seconds_per_frame = kwargs.get('-time_scale')
        else:
            self.seconds_per_frame = 5.0

        self.file_path = file_path

        if kwargs.get('-threshold_for_events') is not None:
            self.attach_threshold, self.detach_threshold = kwargs.get('-threshold_for_events')
        else:
            # obtain automatic threshold
            self.attach_threshold, self.detach_threshold = get_background_threshold(file_path)

        if kwargs.get('-filter') is not None:
            self.smoothing_enabled = (True, 11) if kwargs.get('-filter') == 'True' or \
                                                   kwargs.get('-filter') is True else (False, 1)
        else:
            self.smoothing_enabled = (True, 11)

    def get_fraction_of_event(self, dynamics_matrix: np.ndarray):
        detachment_event = dynamics_matrix[dynamics_matrix >= self.detach_threshold]
        attachment_event = dynamics_matrix[dynamics_matrix < self.attach_threshold]

        return len(attachment_event) / (len(detachment_event) + len(attachment_event)) if len(
                attachment_event) > 0 else 0, \
                len(detachment_event) / (len(detachment_event) + len(attachment_event)) if len(attachment_event) > 0 \
                else 0

    def count_dynamics_events(self, video_path: str):
        # reading the file
        video_cap = cv.VideoCapture(video_path)
        final_frame_count = int(video_cap.get(cv.CAP_PROP_FRAME_COUNT))
        frame_width = int(video_cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_cap.get(cv.CAP_PROP_FRAME_HEIGHT))

        distribution_for_detachment_event_about_time = np.ndarray((final_frame_count - 1), dtype=float)
        distribution_for_attachment_event_about_time = np.ndarray((final_frame_count - 1), dtype=float)

        ret = True
        fc = 0
        first_frame = None
        while fc < final_frame_count - 1 and ret:
            if first_frame is None:
                ret, first_frame = video_cap.read()
                ret, second_frame = video_cap.read()
            else:
                ret, second_frame = video_cap.read()
            dynamics_matrix = second_frame.astype(float)[:, :, 0] - first_frame.astype(float)[:, :, 0]
            distribution_for_attachment_event_about_time[fc], distribution_for_detachment_event_about_time[fc] = self.get_fraction_of_event(dynamics_matrix)
            first_frame = second_frame.copy()
            fc += 1

        if self.smoothing_enabled[0]:
            return self.savitzky_golay_smoother(distribution_for_attachment_event_about_time,
                                                window_size=self.smoothing_enabled[1],
                                                order=3), \
                   self.savitzky_golay_smoother(distribution_for_detachment_event_about_time,
                                                window_size=self.smoothing_enabled[1],
                                                order=3)
        else:
            return distribution_for_attachment_event_about_time, distribution_for_detachment_event_about_time

    def savitzky_golay_smoother(self, y, window_size=5, order=3, derivative=0, rate=1):
        order_range = range(order + 1)
        half_window = (window_size - 1) // 2
        b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
        m = np.linalg.pinv(b).A[derivative] * rate ** derivative * factorial(derivative)

        firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
        lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
        y = np.concatenate((firstvals, y, lastvals))
        return np.convolve(m[::-1], y, mode='valid')

    def obtain_dynamics(self):
        """
        creates & saves the figure and signal numpy arrays to the results folder.
        :return:
        """
        file_name = self.file_path.split(os.sep)[-1][:-4]
        file_path_folder = os.sep.join(self.file_path.split(os.sep)[:-1])
        path_for_results = "{0}{1}Results".format(file_path_folder, os.sep)

        attachment_dynamics, detachment_dynamics = self.count_dynamics_events(self.file_path)
        # saving numpy arrays
        np.save("{0}{1}DynamicsNumpyArrays{1}{2}_attachment_signal_numpyArray".format(path_for_results, os.sep, file_name), attachment_dynamics)
        np.save("{0}{1}DynamicsNumpyArrays{1}{2}_detachment_signal_numpyArray".format(path_for_results, os.sep, file_name), detachment_dynamics)
        t = ["{}".format(int(frame_num*self.seconds_per_frame)) for frame_num in range(0, len(attachment_dynamics))]
        fig, ax = plt.subplots()
        ax.plot(t, attachment_dynamics)
        ax.plot(t, detachment_dynamics)
        ax.set_xlabel("time (sec)", fontsize=4)
        ax.set_ylabel("Attachment/detachment fraction", fontsize=4)

        for k, label in enumerate(ax.xaxis.get_ticklabels()[::]):
            if k % 10 == 0:
                label.set_visible(True)
            else:
                label.set_visible(False)

        plt.setp(ax, ylim=(0, 1))
        plt.tight_layout()
        fig.savefig("{0}{1}DynamicsPlots{1}{2}_dynamicsSignalPlot.png".format(path_for_results, os.sep, file_name), dpi=300, bbox_inches="tight")
        return self.attach_threshold, self.detach_threshold


