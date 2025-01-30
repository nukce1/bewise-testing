#!/bin/bash

set -e

echo "Init topics ..."

/opt/bitnami/kafka/bin/kafka-topics.sh --create --if-not-exists --topic applications-created --replication-factor=1 --partitions=3 --bootstrap-server kafka-host:9091

echo "Topic created successfully."

