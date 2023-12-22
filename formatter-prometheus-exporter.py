#!/usr/bin/env python3

import sys
from threading import Thread, Event
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from robusta_krr.api import formatters
from robusta_krr.api.models import Result
from krr2prom import robusta_krr, collect_metrics


@formatters.register(display_name='prometheus-exporter', rich_console=False)
def prometheus_exporter_formatter(result: Result) -> str:
    collect_metrics(result)
    return 'Done metrics'


def krr_runner(scan_frequency, stop_event):
    print("START KRR THREAD")
    cycle = 0
    while stop_event.wait(1):
        if cycle > 0 and cycle < scan_frequency:
            cycle += 1
            continue

        print(f"START KRR-{cycle}")
        t = Thread(target=robusta_krr.run)
        t.start()
        t.join()
        print(f"END KRR-{cycle}")
        cycle = 1

    print("STOP KRR THREAD")

# Run it as `python3 ./formatter-prometheus-exporter.py simple --formater prometheus-exporter`
if __name__ == "__main__":
    scan_frequency = int(os.environ.get('SCAN_FREQUENCY', 600))
    metrics_port = int(os.environ.get('METRICS_PORT', 8080))

    app = Flask(__name__)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })

    stop_event = Event()
    krr_thread = Thread(target=krr_runner, args=(stop_event,), daemon=False)
    krr_thread.start()

    print("START FLASK")
    app.run(host='0.0.0.0', port=metrics_port)
    print("STOP FLASK")
    stop_event.set()
    print("JOIN KRR THREAD")
    krr_thread.join()
    print("EXIT")
    sys.exit(0)
