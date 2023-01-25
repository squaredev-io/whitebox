# Monitors and Alerts

## Monitors

You can create a monitor in whitebox so that alert are created automaticaly when some value is out of bounds. Here is an example:

```Python
from whitebox import Whitebox, MonitorStatus, MonitorMetrics, AlertSeverity

wb = Whitebox(host="127.0.0.1:8000", api_key="some_api_key")

model_monitor = wb.create_model_monitor(
    model_id="mock_model_id",
    name="test",
    status=MonitorStatus.active,
    metric=MonitorMetrics.accuracy,
    feature="feature1",
    lower_threshold=0.7,
    severity=AlertSeverity.high,
    email="jaclie.chan@somemail.io",
)
```

## Alerts

Once the metrics reports have been produced, the monitoring alert pipeline is triggered. This means that if you have created any model monitors for a specific metric, alerts will be created if certain criteria are met, based on the thresholds and the monitor types you have specified.
