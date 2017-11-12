#!/usr/bin/env python

import argparse
import json
import logging
import os
import requests
import time

import paho.mqtt.client as mqtt

LOG = logging.getLogger(__name__)

current_weather_url = 'https://api.darksky.net/forecast/{api_key}/{location}'
params = {
    'exclude': 'minutely,hourly,daily,flags',
    'units': 'si',
}


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--api-key',
                   default=os.environ.get('FORECASTIO_API_KEY'))
    p.add_argument('--location',
                   default=os.environ.get('FORECASTIO_LOCATION'))
    p.add_argument('--interval', '-i',
                   default=os.environ.get('FORECASTIO_POLL_INTERVAL', 60),
                   type=int)
    p.add_argument('--topic',
                   default=os.environ.get('FORECASTIO_TOPIC_PREFIX', 'sensor'))
    p.add_argument('--mqtt-server', '-s',
                   default=os.environ.get('FORECASTIO_MQTT_SERVER'))

    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level='INFO')

    LOG.info('connecting to mqtt broker')
    mq = mqtt.Client()
    mq.loop_start()
    mq.connect(args.mqtt_server)

    url = current_weather_url.format(
        location=args.location,
        api_key=args.api_key)
    while True:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        topic = '{}/forecastio/{latitude},{longitude}'.format(
            args.topic, **data)
        sample = data['currently']
        for k in ['summary', 'icon']:
            del sample[k]

        sample['sensor_type'] = 'forecastio'

        LOG.info('sending on %s sample %s', topic, sample)
        mq.publish(topic, json.dumps(sample))

        time.sleep(args.interval)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
