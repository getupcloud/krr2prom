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

def is_number(value):
    try:
        float(value) or int(value)
        return True
    except TypeError:
        return False

def collect_metrics(result):
    KRR_SCORE.labels(
        result.strategy.name,
        result.strategy.settings.get('history_duration', 0),
        result.strategy.settings.get('timeframe_duration', 0),
        result.strategy.settings.get('cpu_percentile', 0),
        result.strategy.settings.get('memory_buffer_percentage', 0),
        result.strategy.settings.get('points_required', 0),
    ).set(result.score)

    for scan in result.scans:
        obj, rec = scan.object, scan.recommended
        alloc = obj.allocations

        kind      = obj.kind
        namespace = obj.namespace
        name      = obj.name
        container = obj.container

        if kind in ["Deployment", "DaemonSet", "StatefulSet"]:
            if is_number(alloc.requests['cpu']): KRR_ALLOCATIONS_REQUESTS_CPU.labels(kind, name, container, namespace).set(alloc.requests['cpu'])
            if is_number(alloc.requests['memory']): KRR_ALLOCATIONS_REQUESTS_MEMORY.labels(kind, name, container, namespace).set(alloc.requests['memory'])
            if is_number(alloc.limits['cpu']): KRR_ALLOCATIONS_LIMITS_CPU.labels(kind, name, container, namespace).set(alloc.limits['cpu'])
            if is_number(alloc.limits['memory']): KRR_ALLOCATIONS_LIMITS_MEMORY.labels(kind, name, container, namespace).set(alloc.limits['memory'])

            if is_number(alloc.requests['cpu']): KRR_RECOMMENDED_REQUESTS_CPU.labels(kind, name, container, namespace, rec.requests['cpu'].severity).set(rec.requests['cpu'].value)
            if is_number(alloc.requests['memory']): KRR_RECOMMENDED_REQUESTS_MEMORY.labels(kind, name, container, namespace, rec.requests['memory'].severity).set(rec.requests['memory'].value)
            if is_number(alloc.limits['cpu']): KRR_RECOMMENDED_LIMITS_CPU.labels(kind, name, container, namespace, rec.limits['cpu'].severity).set(rec.limits['cpu'].value)
            if is_number(alloc.limits['memory']): KRR_RECOMMENDED_LIMITS_MEMORY.labels(kind, name, container, namespace, rec.limits['memory'].severity).set(rec.limits['memory'].value)
