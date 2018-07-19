import numpy as np
from scipy.spatial.distance import euclidean
from operator import itemgetter


class TrackingPeople:
    MAX_PEOPLE = 2
    MAX_POINTS = 10
    DIST_THRESHOLD = 25.0

    def __init__(self):
        self.people = dict()
        for person_id in range(self.MAX_PEOPLE):
            self.people[person_id] = {'cur_pos': 0, 'positions': [None] * self.MAX_POINTS}

    def find_closest_person(self, center, hsv):
        mean_hsv = np.mean(hsv)
        distances = dict()
        for person_id, attributes in self.people.items():
            # checks if the previous tracked position is valid
            if attributes['positions'][(attributes['cur_pos'] - 1) % self.MAX_POINTS]:
                distances[person_id] = euclidean(center, attributes['positions'][(attributes['cur_pos'] - 1) % self.MAX_POINTS])
            else:
                distances[person_id] = attributes['positions'][(attributes['cur_pos'] - 1) % self.MAX_POINTS]

        filtered = dict(filter(lambda item: item[1] is not None, distances.items()))
        untracked = dict(filter(lambda item: item[1] is None, distances.items()))

        # print filtered

        if len(filtered) > 0:
            min_dist_id, min_dist = min(distances.items(), key=itemgetter(1))

            if min_dist < self.DIST_THRESHOLD:
                print 'TRACKING'
            elif len(untracked) > 0:
                print 'FREE SPOTS'
                min_dist_id = untracked.keys()[0]
            else:
                print 'NO FREE SPOTS'
                min_dist_id = -1
        else:
            print 'FIRST SPOT'
            min_dist_id = untracked.keys()[0]

        if min_dist_id != -1:
            self.people[min_dist_id]['positions'][self.people[min_dist_id]['cur_pos']] = center
            self.people[min_dist_id]['cur_pos'] = (self.people[min_dist_id]['cur_pos'] + 1) % self.MAX_POINTS
