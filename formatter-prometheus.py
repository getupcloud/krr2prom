#!/usr/bin/env python3

import time
from prometheus_client import generate_latest
from robusta_krr.api import formatters
from robusta_krr.api.models import Result
from krr2prom import robusta_krr, collect_metrics

@formatters.register(display_name='prometheus', rich_console=False)
def prometheus_formatter(result: Result) -> str:
    collect_metrics(result)
    return generate_latest()

# Run it as `python3 ./formatter-prometheus.py simple --formater prometheus`
if __name__ == "__main__":
    robusta_krr.run()
    print("Sleeping forever...")
    while True
        time.sleep(100)
