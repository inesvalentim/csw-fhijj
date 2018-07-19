# import numpy as np
import cv2
import random
from skimage.measure import compare_ssim as ssim


class IdentifiedPerson:
    def __init__(self, positions, feature, colour):
        self.positions = positions
        self.feature = feature
        self.colour = colour
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
    def __init__(self, frame, center, timestamp):
        self.frame = frame
        self.resized_frame = cv2.resize(frame, (50, 50))
        self.last_position = center
        self.timestamp = timestamp


TOLERANCE = 0.0001
IMAGE_SIMILARITY_WEIGHT = 0.7
POSITION_SIMILARITY_WEIGHT = 1 - IMAGE_SIMILARITY_WEIGHT


class TrackingPeople:
    MAX_EFFECTIVE_SIMILARITY = POSITION_SIMILARITY_WEIGHT

    DIFF_THRESHOLD = 0.1 * MAX_EFFECTIVE_SIMILARITY

    def __init__(self):
        self.people = list()

    @staticmethod
    def diff_between_features(previous_feature, current_feature):
        if current_feature.frame.size == 0:
            return 0

        last_x, last_y = previous_feature.last_position
        cur_x, cur_y = current_feature.last_position

        pos_similarity = -float(abs(last_x - cur_x) + abs(last_y - cur_y)) / float(
            abs(last_x) + abs(last_y) + abs(last_x) + abs(last_y))
        # print "pos similarity: {}".format(pos_similarity)

        image_similarity = ssim(previous_feature.resized_frame,
                                current_feature.resized_frame,
                                multichannel=True)

        # print "pf last position: {}".format(previous_feature.last_position)
        # print "cf last position: {}".format(current_feature.last_position)
        return POSITION_SIMILARITY_WEIGHT * pos_similarity + IMAGE_SIMILARITY_WEIGHT * image_similarity

    """
    @staticmethod
    def diff_between_frames(previous, current):
        if current.size == 0:
            return 0
        else:
            previous = cv2.resize(previous, (50, 50))
            current = cv2.resize(current, (50, 50))

        return ssim(previous, current, multichannel=True)

    def find_closest_person(self, frame, center, timestamp):
        if len(self.people) > 0:
            differences = map(lambda x: self.diff_between_frames(x["hue_frame"], frame), self.people)
            print differences
            min_idx = np.argmax(differences)

            if differences[min_idx] > self.DIFF_THRESHOLD:
                if len(self.people[min_idx]['positions']) == 5:
                    self.people[min_idx]['positions'].pop(0)
                self.people[min_idx]['positions'].append(center)
                self.people[min_idx]['latest_timestamp'] = timestamp
            else:
                self.people.append({'color': random.sample(range(0, 255), 3),
                                    'hue_frame': frame, 'positions': [center], 'latest_timestamp': timestamp})
        else:
            self.people.append({'color': random.sample(range(0, 255), 3),
                                'hue_frame': frame, 'positions': [center], 'latest_timestamp': timestamp})
    """

    def find_closest_person_v2(self, frame, center, timestamp):
        # def find_closest_person_v2(self, frame, center, timestamp, og_frame_width):
        current_feature = Feature(frame, center, timestamp)

        if len(self.people) > 0:
            candidate_person, candidate_person_similarity = max(
                ((person, self.diff_between_features(person.feature, current_feature)) for person in self.people),
                key=lambda (_, diff): diff)

            if candidate_person_similarity > self.DIFF_THRESHOLD:
                # if len(self.people[min_idx]['positions']) == 5:
                #     self.people[min_idx]['positions'].pop(0)
                candidate_person.positions.append(center)
                candidate_person.feature.last_position = center
                candidate_person.timestamp = timestamp
                # candidate_person.update_state(og_frame_width)
            else:
                self.people.append(IdentifiedPerson([center], current_feature, random.sample(range(0, 255), 3)))
                # self.people.append(IdentifiedPerson([center], current_feature,
                # random.sample(range(0, 255), 3)), og_frame_width)
        else:
            self.people.append(IdentifiedPerson([center], current_feature, random.sample(range(0, 255), 3)))
            # self.people.append(IdentifiedPerson([center], current_feature,
            # random.sample(range(0, 255), 3)), og_frame_width)
