#!/usr/bin/env python3

import sys
from prometheus_client import Gauge
import robusta_krr


KRR_SCORE = Gauge(
    'krr_score',
    'KRR score values.',
    [
        'strategy_name', 'strategy_history_duration', 'strategy_timeframe_duration',
        'strategy_cpu_percentile', 'strategy_memory_buffer_percentage', 'strategy_points_required'
    ]
)

KRR_ALLOCATIONS_REQUESTS_CPU = Gauge(
    'krr_allocations_requests_cpu',
    'The number of cpu milicores requested by this container detected by KRR.',
    [ 'kind', 'name', 'container', 'namespace' ]
)

KRR_ALLOCATIONS_REQUESTS_MEMORY = Gauge(
    'krr_allocations_requests_memory',
    'The number of memory bytes requested by this container detected by KRR.',
    [ 'kind', 'name', 'container', 'namespace' ]
)

KRR_ALLOCATIONS_LIMITS_CPU = Gauge(
    'krr_allocations_limits_cpu',
    'The maximum number of cpu milicores requested by this container detected by KRR.',
    [ 'kind', 'name', 'container', 'namespace' ]
)

KRR_ALLOCATIONS_LIMITS_MEMORY = Gauge(
    'krr_allocations_limits_memory',
    'The maximum number of memory bytes requested by this container detected by KRR.',
    [ 'kind', 'name', 'container', 'namespace' ]
)

KRR_RECOMMENDED_REQUESTS_CPU = Gauge(
    'krr_recommended_requests_cpu',
    'The KRR recommended number of cpu milicores to this container.',
    [ 'kind', 'name', 'container', 'namespace', 'severity' ]
)

KRR_RECOMMENDED_REQUESTS_MEMORY = Gauge(
    'krr_recommended_requests_memory',
    'The KRR recommended number of memory bytes to this container.',
    [ 'kind', 'name', 'container', 'namespace', 'severity' ]
)

KRR_RECOMMENDED_LIMITS_CPU = Gauge(
    'krr_recommended_limits_cpu',
    'The KRR recommended maximum number of cpu milicores to this container.',
    [ 'kind', 'name', 'container', 'namespace', 'severity' ]
)

KRR_RECOMMENDED_LIMITS_MEMORY = Gauge(
    'krr_recommended_limits_memory',
    'The KRR recommended maximum number of memory bytes to this container.',
    [ 'kind', 'name', 'container', 'namespace', 'severity' ]
)


def set_metric(metric, value, *labels):
    try:
        metric.labels(*labels).set(float(value))
    except TypeError:
        pass


def collect_metrics(result):
    KRR_SCORE.labels(
        result.strategy.name,
        result.strategy.settings.get('history_duration', 0),
        result.strategy.settings.get('timeframe_duration', 0),
        result.strategy.settings.get('cpu_percentile', 0),
        result.strategy.settings.get('memory_buffer_percentage', 0),
        result.strategy.settings.get('points_required', 0),
    ).set(result.score)

    def severity(rec):
        return rec.severity.split('.')[-1]

    for scan in result.scans:
        obj, alloc, recom = scan.object, scan.object.allocations, scan.recommended

        kind      = obj.kind
        namespace = obj.namespace
        name      = obj.name
        container = obj.container

        if kind in ["Deployment", "DaemonSet", "StatefulSet"]:
            set_metric(KRR_ALLOCATIONS_REQUESTS_CPU,    alloc.requests['cpu'],      kind, name, container, namespace)
            set_metric(KRR_ALLOCATIONS_REQUESTS_MEMORY, alloc.requests['memory'],   kind, name, container, namespace)
            set_metric(KRR_ALLOCATIONS_LIMITS_CPU,      alloc.limits['cpu'],        kind, name, container, namespace)
            set_metric(KRR_ALLOCATIONS_LIMITS_MEMORY,   alloc.limits['memory'],     kind, name, container, namespace)
            set_metric(KRR_RECOMMENDED_REQUESTS_CPU,    recom.requests['cpu'],      kind, name, container, namespace, severity(rec.requests['cpu']))
            set_metric(KRR_RECOMMENDED_REQUESTS_MEMORY, recom.requests['memory'],   kind, name, container, namespace, severity(rec.requests['memory']))
            set_metric(KRR_RECOMMENDED_LIMITS_CPU,      recom.limits['cpu'],        kind, name, container, namespace, severity(rec.limits['cpu']))
            set_metric(KRR_RECOMMENDED_LIMITS_MEMORY,   recom.limits['memory'],     kind, name, container, namespace, severity(rec.limits['memory']))
