import os
import numpy as np
import time as time
import cv2

# DEF COLOR_SCHEMES
def_attach_color_scheme = [0, 0, 250]
def_detach_color_scheme = [250, 0, 0]


class DynamicsEncoder:
    """
    Duplicates the original video, encoding every pixel that exhibits a dynamic with the appropriate color (red=detachment, blue=detachment)
    """
    def __init__(self, attachment_thresold: float = 0, detachment_thresold: float = 0, attach_color_scheme=None, detach_color_scheme=None):
        """
        :param color_scheme1:
        :param color_scheme2:
        :param attachment_thresold:
        :param detachment_thresold:
        """
        if attach_color_scheme is None:
            self.attach_color_scheme = def_attach_color_scheme
        if detach_color_scheme is None:
            self.detach_color_scheme = def_detach_color_scheme
        self.attach_threshold = attachment_thresold
        self.detach_threshold = detachment_thresold

    def color_by_scheme(self, buf: np.ndarray, dynamics: np.ndarray):
        """
        encodes the color in a given frame (buf)
        :param buf:
        :param dynamics:
        :return:
        """
        # encode detach
        buf = np.where(dynamics > self.detach_threshold*2, self.detach_color_scheme, buf)

        # encode attach
        buf = np.where(dynamics < self.attach_threshold*2, self.attach_color_scheme, buf)
        return buf

    def manipulate_frame(self, buf: np.ndarray, **kwargs):
        """
        colors are [Blue,Green,Red]
        :param buf:
        :return:
        """
        if kwargs.get('limit') is not None:
            limit = kwargs.get('limit')
        else:
            limit = -9

        dynamics = buf[0] - buf[1]

        # attach encoding
        buf[0] = self.color_by_scheme(buf[0], dynamics)
        # detach encoding
        buf[0] = self.color_by_scheme(buf[0], dynamics)

        return buf

    def manipulate_video(self, video_path: str, manipulated_video_path, condition, **kwargs):
        """
        condition is a function type object that receives pixel
        dynamic value (current_value-next_frame_value),current pixel time, current intensity.
        :param condition:
        :return:
        """
        file_name = video_path.split(os.sep)[-1]
        video_cap = cv2.VideoCapture("{0}".format(video_path))
        # get video meta data
        final_frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video_cap.get(cv2.CAP_PROP_FPS)
        frames_in_memory = 2
        # video writer to AVI
        out = cv2.VideoWriter(
            "{0}{1}{2}".format(manipulated_video_path, os.sep, file_name),
            cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

        buf = np.zeros((frames_in_memory, frame_height, frame_width, 3), np.dtype('int64'))
        ret = True

        fc = 0
        while fc < final_frame_count and ret:
            # loading the data according
            in_memory_frames_ctr = 0
            single_frame_start_time = time.time()
            while in_memory_frames_ctr < frames_in_memory:
                if np.sum(buf[frames_in_memory - 1]) > 0:
                    temp = buf[frames_in_memory - 1].copy()
                    # buf[FRAMES_IN_MEMORY-1] = np.zeros((frame_height, frame_width, 3))
                    buf = np.zeros((frames_in_memory, frame_height, frame_width, 3), np.dtype('int64'))
                    buf[0] = temp
                else:
                    ret, frame = video_cap.read()
                    buf[in_memory_frames_ctr] = frame
                    fc += 1
                in_memory_frames_ctr += 1
            buf = condition(buf, **kwargs)
            im = np.uint8(buf[0])
            out.write(im)
            # cv2.imshow("test", np.array(im, dtype=np.uint8))
            # new_video[fc-2] = buf[0]
            single_frame_end_time = time.time()
            print("frame No:{0} has been manipulated.took:{1:.2} seconds".format(fc - 2,
                                                                                 single_frame_end_time - single_frame_start_time))

        out.release()
        video_cap.release()

