"""
AWS implementation of the CPDL
Authors: Diana Mendes, Samuel Pedro & Jason Bolito
"""

import awscam

from .base import CaptureProcessDisplayLoop


class AwsCaptureProcessDisplayLoop(CaptureProcessDisplayLoop):
    # def __capture_new_frame(self) -> np.ndarray:
    def _capture_new_frame(self):
        success, frame = awscam.getLastFrame()
        if not success:
            raise Exception('DEEP LENS ERROR: Failed to get frame from the stream')

        return frame
