import cv2
import random
from skimage.measure import compare_ssim as ssim


class BoundingBox:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.area = (xmax - xmin) * (ymax - ymin)

    def intersection_area(self, bbox):
        dx = min(self.xmax, bbox.xmin) - max(self.xmin, bbox.xmin)
        if dx <= 0:
            return 0

        dy = min(self.ymax, bbox.ymax) - max(self.ymin, bbox.ymin)
        if dy <= 0:
            return 0

        return dx * dy

    def intersection_over_union_area(self, bbox):
        intersection = self.intersection_area(bbox)
        union = self.area + bbox.area - intersection

        return 0 if union == 0 else intersection / union


class IdentifiedPerson:
    def __init__(self, positions, feature, colour, timestamps):
        self.positions = positions
        self.feature = feature
        self.colour = colour
        self.timestamps = timestamps

    """
    def __init__(self, positions, feature, colour, frame_width):
        self.positions = positions
        self.feature = feature
        self.colour = colour
        self.state = None
        self.update_state(frame_width)

    def compute_relative_position(self, position_idx, frame_width):
        x, y = self.positions[position_idx]

        if x < float(frame_width / 2.0):
            return 0
        else:
            return 1

    def update_state(self, frame_width):
        if not self.state:
            self.state = self.compute_relative_position(-1, frame_width)
        elif self.state != self.compute_relative_position(-1, frame_width):
            self.state = 1 - self.state
    """


class Feature:
    def __init__(self, frame, center, timestamp, bbox, parent_width, parent_height):
        self.frame = frame
        self.resized_frame = cv2.resize(frame, (50, 50))
        self.last_position = center
        self.timestamp = timestamp
        self.bbox = bbox
        self.parent_width = parent_width
        self.parent_height = parent_height


TOLERANCE = 0.0001
IMAGE_SIMILARITY_WEIGHT = 0.7
IOU_WEIGHT = 0.0
POSITION_SIMILARITY_WEIGHT = 1 - IMAGE_SIMILARITY_WEIGHT


class TrackingPeople:
    MAX_EFFECTIVE_SIMILARITY = IOU_WEIGHT + IMAGE_SIMILARITY_WEIGHT

    DIFF_THRESHOLD = 0.1 * MAX_EFFECTIVE_SIMILARITY

    def __init__(self):
        self.people = list()

    @staticmethod
    def diff_between_features(previous_feature, current_feature):
        if current_feature.frame.size == 0:
            return 0

        last_x, last_y = previous_feature.last_position
        cur_x, cur_y = current_feature.last_position

        pos_similarity = -float(abs(last_x - cur_x) + abs(last_y - cur_y)) / (
                current_feature.parent_width + current_feature.parent_height)

        # norm_factor = / float(
        #     abs(last_x) + abs(last_y) + abs(last_x) + abs(last_y))
        # print "pos similarity: {}".format(pos_similarity)

        image_similarity = ssim(previous_feature.resized_frame,
                                current_feature.resized_frame,
                                multichannel=True)

        # print "pf last position: {}".format(previous_feature.last_position)
        # print "cf last position: {}".format(current_feature.last_position)
        return POSITION_SIMILARITY_WEIGHT * pos_similarity + IMAGE_SIMILARITY_WEIGHT * image_similarity + \
               IOU_WEIGHT * current_feature.bbox.intersection_over_union_area(previous_feature.bbox)

    def find_closest_person_v2(self, frame, center, timestamp, bbox, frame_shape):
        current_feature = Feature(frame, center, timestamp, bbox, frame_shape[1], frame_shape[0])

        if len(self.people) > 0:
            candidate_person, candidate_person_similarity = max(
                ((person, self.diff_between_features(person.feature, current_feature)) for person in self.people),
                key=lambda (_, diff): diff)

            if candidate_person_similarity > self.DIFF_THRESHOLD:
                if len(candidate_person.positions) > 5:
                    del (candidate_person.positions[0])
                candidate_person.positions.append(center)
                candidate_person.feature.last_position = center
                candidate_person.timestamps.append(timestamp)
            else:
                self.people.append(IdentifiedPerson([center], current_feature, random.sample(range(0, 255), 3), [timestamp]))
        else:
            self.people.append(IdentifiedPerson([center], current_feature, random.sample(range(0, 255), 3), [timestamp]))
