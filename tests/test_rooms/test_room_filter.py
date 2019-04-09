import sys
import os

from tests.base import BaseTestCase, CommonTestCases
from fixtures.room.filter_room_fixtures import (
    filter_rooms_by_capacity,
    filter_rooms_by_capacity_response,
    filter_rooms_by_location,
    filter_rooms_by_location_response,
    filter_rooms_by_location_capacity,
    filter_rooms_by_location_capacity_response
)

sys.path.append(os.getcwd())


class RoomsFilter(BaseTestCase):

    def test_filter_room_by_capacity(self):
        CommonTestCases.user_token_assert_equal(
            self,
            filter_rooms_by_capacity,
            filter_rooms_by_capacity_response
        )

    def test_filter_room_by_location(self):
        CommonTestCases.user_token_assert_equal(
            self,
            filter_rooms_by_location,
            filter_rooms_by_location_response
        )

    def test_filter_room_by_location_capacity(self):
        CommonTestCases.user_token_assert_equal(
            self,
            filter_rooms_by_location_capacity,
            filter_rooms_by_location_capacity_response
        )
