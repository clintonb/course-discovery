import pytest
from django.core.management import call_command

from course_discovery.apps.publisher.models import CourseMode, Seat
from course_discovery.apps.publisher.tests.factories import SeatFactory


@pytest.mark.django_db
class TestAddAuditSeats:
    def test_no_commit(self):
        seats = SeatFactory.create_batch(3, type=CourseMode.VERIFIED)
        call_command('add_audit_seats_to_verified_course_runs')
        assert Seat.objects.count() == len(seats)

    @pytest.mark.parametrize('seat_type', (CourseMode.CREDIT, CourseMode.VERIFIED,))
    def test_commit(self, seat_type):
        SeatFactory(type=CourseMode.AUDIT)
        SeatFactory(type=CourseMode.NO_ID_PROFESSIONAL)
        SeatFactory(type=CourseMode.PROFESSIONAL)

        seat = SeatFactory(type=seat_type)
        call_command('add_audit_seats_to_verified_course_runs', '--commit')

        assert seat.course_run.seats.count() == 2
        assert seat.course_run.seats.filter(type=CourseMode.AUDIT, price=0).exists()
