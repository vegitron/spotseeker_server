from django.utils import unittest
import datetime
from spotseeker_server.models import Spot, SpotAvailableHours

class SpotHoursModelTest(unittest.TestCase):
    def test_startMatchesEnd(self):
        spot = Spot.objects.create(name = 'testing hours')
        try:
            hours = SpotAvailableHours.objects.create(day = "m", spot = spot, start_time = "01:30", end_time = "01:30")
        except Exception as e:
            self.assertEquals(e[0], "Invalid time range - start time must be before end time", "Got an error trying to save a time range with no time in it")

    def test_startAfterEnd(self):
        spot = Spot.objects.create(name = 'testing hours')
        try:
            hours = SpotAvailableHours.objects.create(day = "m", spot = spot, start_time = "01:40", end_time = "01:30")
        except Exception as e:
            self.assertEquals(e[0], "Invalid time range - start time must be before end time", "Got an error trying to save a time range with no time in it")

    def test_properRange(self):
        spot = Spot.objects.create(name = 'testing hours')
        hours = SpotAvailableHours.objects.create(day = "m", spot = spot, start_time = "01:30", end_time = "01:40")

        self.assertEquals(hours.start_time,  datetime.time(1, 30), "ok")
        self.assertEquals(hours.end_time,  datetime.time(1, 40), "ok")
        self.assertEquals(hours.day,  "m", "ok")

    def test_missingStart(self):
        spot = Spot.objects.create(name = 'testing hours')
        has_error = False
        try:
            hours = SpotAvailableHours.objects.create(spot = spot, day="m", end_time = "01:30")
        except:
            has_error = True

        self.assertEquals(has_error, True, "Doesn't allow hours to be stored without a start time")

    def test_missingEnd(self):
        spot = Spot.objects.create(name = 'testing hours')
        has_error = False
        try:
            hours = SpotAvailableHours.objects.create(spot = spot, day="m", start_time = "01:30")
        except:
            has_error = True

        self.assertEquals(has_error, True, "Doesn't allow hours to be stored without an end time")

    def test_missingHours(self):
        spot = Spot.objects.create(name = 'testing hours')
        has_error = False
        try:
            hours = SpotAvailableHours.objects.create(spot = spot, day="m")
        except:
            has_error = True

        self.assertEquals(has_error, True, "Doesn't allow hours to be stored without hours")

    def test_missingDay(self):
        spot = Spot.objects.create(name = 'testing hours')
        has_error = False
        try:
            hours = SpotAvailableHours.objects.create(spot = spot, start_time="01:30", end_time="02:30")
        except:
            has_error = True

        self.assertEquals(has_error, True, "Doesn't allow hours to be stored without a day")

    def test_invalidDay(self):
        spot = Spot.objects.create(name = 'testing hours')
        has_error = False
        try:
            hours = SpotAvailableHours.objects.create(spot = spot, day="Fail_day", start_time="01:30", end_time="02:30")
        except Exception as e:
            has_error = True

        self.assertEquals(has_error, True, "Doesn't allow hours to be stored with an invalid day")

