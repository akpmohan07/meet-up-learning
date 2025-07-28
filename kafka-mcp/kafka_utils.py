#!/usr/bin/env python3
"""
Kafka Utilities - Core Kafka operations and management functionality
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import (
    InvalidPartitionsError,
    InvalidReplicationFactorError,
    KafkaError,
    TopicAlreadyExistsError,
    UnknownTopicOrPartitionError,
)

# Configure logging
logger = logging.getLogger("kafka-utils")


class KafkaManager:
    """Manages Kafka connections and operations"""

    def __init__(self, config_file: str):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.admin_client = None
        self.producer = None

    def _load_config(self) -> Dict[str, Any]:
        """Load Kafka configuration from properties file"""
        config = {}
        try:
            with open(self.config_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            key, value = line.split("=", 1)
                            config[key.strip()] = value.strip()
            logger.info(f"Loaded Kafka config from {self.config_file}")
            return config
        except Exception as e:
            logger.error(f"Failed to load config file {self.config_file}: {e}")
            raise

    def _get_admin_client(self) -> KafkaAdminClient:
        """Get or create Kafka admin client"""
        if self.admin_client is None:
            self.admin_client = KafkaAdminClient(
                bootstrap_servers=self.config.get(
                    "bootstrap.servers", "localhost:9092"
                ),
                client_id=self.config.get("client.id", "kafka-mcp-server"),
                **{
                    k: v
                    for k, v in self.config.items()
                    if k not in ["bootstrap.servers", "client.id"]
                },
            )
        return self.admin_client

    def _get_producer(self) -> KafkaProducer:
        """Get or create Kafka producer"""
        if self.producer is None:
            self.producer = KafkaProducer(
                bootstrap_servers=self.config.get(
                    "bootstrap.servers", "localhost:9092"
                ),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                **{
                    k: v
                    for k, v in self.config.items()
                    if k not in ["bootstrap.servers", "client.id"]
                },
            )
        return self.producer

    def list_topics(self) -> List[Dict[str, Any]]:
        """List all topics in the Kafka cluster"""
        try:
            admin = self._get_admin_client()
            metadata = admin.describe_topics()

            if metadata is None:
                return []
            topics = []
            for topic_metadata in metadata:
                topics.append(
                    {
                        "name": topic_metadata.get("topic"),
                        "partitions": len(topic_metadata.get("partitions")),
                        "replication_factor": (
                            len(topic_metadata.get("partitions")[0].get("replicas"))
                            if topic_metadata.get("partitions")
                            else 0
                        ),
                    }
                )

            return sorted(topics, key=lambda x: x["name"])
        except Exception as e:
            logger.error(f"Failed to list topics: {e}")
            raise

    def create_topic(
        self,
        name: str,
        num_partitions: int = 1,
        replication_factor: int = 1,
        config: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Create a new topic"""
        if num_partitions < 1:
            return {
                "status": "error",
                "message": "Number of partitions must be at least 1.",
            }

        if replication_factor < 1 and replication_factor != -1:
            return {
                "status": "error",
                "message": "Replication factor must be at least 1 or -1 for default.",
            }
        try:
            admin = self._get_admin_client()

            topic = NewTopic(
                name=name,
                num_partitions=num_partitions,
                replication_factor=replication_factor,
                topic_configs=config or {},
            )

            response = admin.create_topics([topic])
            logger.info(f"Create Topics response: {response}")

            return {
                "status": "success",
                "message": f"Topic '{name}' created successfully",
                "topic": {
                    "name": name,
                    "partitions": num_partitions,
                    "replication_factor": replication_factor,
                },
            }

        except TopicAlreadyExistsError:
            return {
                "status": "error",
                "message": f"Topic '{name}' already exists",
            }
        except InvalidReplicationFactorError:
            return {
                "status": "error",
                "message": "Invalid replication factor. It must be at least 1 or -1 for default.",
            }
        except InvalidPartitionsError:
            return {
                "status": "error",
                "message": "Invalid number of partitions. It must be a positive integer.",
            }
        except KafkaError as e:
            logger.error(f"Kafka error while creating topic '{name}': {e}")
            return {
                "status": "error",
                "message": f"Kafka error: {str(e)}",
            }
        except Exception as e:
            logger.exception(f"Unexpected error while creating topic {name}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
            }

    def delete_topic(self, name: str) -> Dict[str, Any]:
        """Delete a topic"""
        try:
            admin = self._get_admin_client()
            response = admin.delete_topics([name])
            logger.info(f"Delete Topic response: {response}")

            return {
                "status": "success",
                "message": f"Topic '{name}' deleted successfully",
            }

        except UnknownTopicOrPartitionError:
            return {
                "status": "error",
                "message": f"Topic '{name}' does not exist or already deleted.",
            }
        except KafkaError as e:
            logger.error(f"Kafka error while deleting topic '{name}': {e}")
            return {
                "status": "error",
                "message": f"Kafka error: {str(e)}",
            }

        except Exception as e:
            logger.error(f"Failed to start topic deletion for '{name}': {e}")
            return {
                "status": "error",
                "message": f"Failed to initiate topic deletion: {str(e)}",
            }

    def get_topic_info(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a specific topic"""
        try:
            admin = self._get_admin_client()
            metadata = admin.describe_topics([name])

            logger.info(metadata)
            if metadata is None:
                return {"status": "error", "message": f"Topic '{name}' not found"}

            topic_metadata = metadata[0]
            partitions_info = []

            for partition in topic_metadata.get("partitions"):
                partitions_info.append(
                    {
                        "partition_id": partition.get("partition"),
                        "leader": partition.get("leader"),
                        "replicas": partition.get("replicas"),
                        "isr": partition.get("isr"),
                    }
                )

            return {
                "status": "success",
                "topic": {
                    "name": name,
                    "partitions": partitions_info,
                    "partition_count": len(partitions_info),
                    "replication_factor": (
                        len(partitions_info[0]["replicas"]) if partitions_info else 0
                    ),
                },
            }
        except Exception as e:
            logger.error(f"Failed to get topic info for {name}: {e}")
            return {
                "status": "error",
                "message": f"Failed to get topic info for '{name}': {str(e)}",
            }

    def send_message(
        self, topic: str, message: Optional[Any], key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a message to a Kafka topic"""
        try:
            producer = self._get_producer()
            future = producer.send(
                topic, value=message, key=key.encode("utf-8") if key else None
            )
            record_metadata = future.get(timeout=10)

            return {
                "status": "success",
                "message": f"Message sent to topic '{topic}'",
                "metadata": {
                    "topic": record_metadata.topic,
                    "partition": record_metadata.partition,
                    "offset": record_metadata.offset,
                },
            }
        except Exception as e:
            logger.error(f"Failed to send message to topic '{topic}': {e}")
            return {"status": "error", "message": f"Failed to send message: {str(e)}"}

    def close(self):
        """Close all connections"""
        if self.admin_client:
            self.admin_client.close()
        if self.producer:
            self.producer.close()
