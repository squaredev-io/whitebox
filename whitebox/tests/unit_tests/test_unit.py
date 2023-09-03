from whitebox.cron_tasks.shared import change_timestamp
from datetime import datetime, timezone


class TestNodes:
    def test_round_timestamp(self):
        timestamp = datetime(2023, 3, 7, 15, 34, 23, tzinfo=timezone.utc)
        start_time = datetime(2023, 3, 6, tzinfo=timezone.utc)

        assert change_timestamp(timestamp, start_time, 15, "T") == datetime(
            2023, 3, 7, 15, 45, tzinfo=timezone.utc
        )
        assert change_timestamp(timestamp, start_time, 5, "H") == datetime(
            2023, 3, 7, 16, 0, tzinfo=timezone.utc
        )
        assert change_timestamp(timestamp, start_time, 2, "D") == datetime(
            2023, 3, 8, tzinfo=timezone.utc
        )
        assert change_timestamp(timestamp, start_time, 1, "W") == datetime(
            2023, 3, 13, tzinfo=timezone.utc
        )
