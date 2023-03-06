from whitebox.cron_tasks.shared import change_timestamp
from datetime import datetime


class TestNodes:
    def test_round_timestamp(self):
        timestamp = datetime(2023, 3, 7, 15, 34, 23)
        start_time = datetime(2023, 3, 6)

        assert change_timestamp(timestamp, start_time, 15, "T") == datetime(
            2023, 3, 7, 15, 45
        )
        assert change_timestamp(timestamp, start_time, 5, "H") == datetime(
            2023, 3, 7, 16, 0
        )
        assert change_timestamp(timestamp, start_time, 2, "D") == datetime(2023, 3, 8)
        assert change_timestamp(timestamp, start_time, 1, "W") == datetime(2023, 3, 13)
