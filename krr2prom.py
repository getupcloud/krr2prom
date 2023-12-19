#!/usr/bin/env python

import json
import sys

def number_or_none(value):
    try:
        return int(value) if value is not None else None
    except:
        return None


def add_metric(data, name, labels, value):
    v = number_or_none(value)
    if v is not None:
        data[name]['samples'].append({
            'labels': labels,
            'value': v
        })

def read_json(f):
    data = json.loads(f.read())
    result = {
        'krr_allocations_requests_cpu': {
            'help': 'The number of cpu milicores requested by this container detected by KRR.',
            'type': 'gauge',
            'samples': []
        },
        'krr_allocations_requests_memory': {
            'help': 'The number of memory bytes requested by this container detected by KRR.',
            'type': 'gauge',
            'samples': []
        },
        'krr_allocations_limits_cpu': {
            'help': 'The maximum number of cpu milicores requested by this container detected by KRR.',
            'type': 'gauge',
            'samples': []
        },
        'krr_allocations_limits_memory': {
            'help': 'The maximum number of memory bytes requested by this container detected by KRR.',
            'type': 'gauge',
            'samples': []
        },
        'krr_recommended_requests_cpu': {
            'help': 'The KRR recommended number of cpu milicores to this container.',
            'type': 'gauge',
            'samples': []
        },
        'krr_recommended_requests_memory': {
            'help': 'The KRR recommended number of memory bytes to this container.',
            'type': 'gauge',
            'samples': []
        },
        'krr_recommended_limits_cpu': {
            'help': 'The KRR recommended maximum number of cpu milicores to this container.',
            'type': 'gauge',
            'samples': []
        },
        'krr_recommended_limits_memory': {
            'help': 'The KRR recommended maximum number of memory bytes to this container.',
            'type': 'gauge',
            'samples': []
        },
    }

    for scan in data['scans']:
        obj, rec = scan['object'], scan['recommended']
        alloc = obj['allocations']

        kind      = obj['kind']
        namespace = obj['namespace']
        name      = obj['name']
        container = obj['container']

        if kind in ["Deployment", "DaemonSet", "StatefulSet"]:
            labels = f'kind="{kind}", name="{name}", container="{container}", namespace="{namespace}"'
            add_metric(result, 'krr_allocations_requests_cpu',    labels, alloc['requests']['cpu'])
            add_metric(result, 'krr_allocations_requests_memory', labels, alloc['requests']['memory'])
            add_metric(result, 'krr_allocations_limits_cpu',      labels, alloc['limits']['cpu'])
            add_metric(result, 'krr_allocations_limits_memory',   labels, alloc['limits']['memory'])
            add_metric(result, 'krr_recommended_requests_cpu',    labels, rec['requests']['cpu']['value'])
            add_metric(result, 'krr_recommended_requests_memory', labels, rec['requests']['memory']['value'])
            add_metric(result, 'krr_recommended_limits_cpu',      labels, rec['limits']['cpu']['value'])
            add_metric(result, 'krr_recommended_limits_memory',   labels, rec['limits']['memory']['value'])

    return result

if __name__ == '__main__':
    f_in = sys.stdin
    f_out = sys.stdout

    if len(sys.argv) > 1:
        f_in = open(sys.argv[1], 'r')

    result = read_json(f_in)

    if len(sys.argv) > 2:
        f_out = open(sys.argv[2], 'w')

    for name in sorted(result.keys()):
        metric = result[name]
        samples = metric['samples']
        print(f'# HELP {name} {metric["help"]}', file=f_out)
        print(f'# TYPE {name} {metric["type"]}', file=f_out)
        for sample in samples:
            print(f'{name}{{{sample["labels"]}}} {sample["value"]}', file=f_out)
