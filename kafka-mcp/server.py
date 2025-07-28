#!/usr/bin/env python3
"""
Kafka MCP Server - A Model Context Protocol server for Kafka operations using FastMCP
"""

import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context, FastMCP

from kafka_utils import (
    KafkaManager,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka-mcp-server")


@dataclass
class KafkaContext:
    """Application context holding Kafka manager"""

    kafka_manager: Optional[KafkaManager] = None


# Create the FastMCP server with lifespan management
@asynccontextmanager
async def kafka_lifespan(server: FastMCP) -> AsyncIterator[KafkaContext]:
    """Manage Kafka connections lifecycle"""
    context = KafkaContext()
    try:
        yield context
    finally:
        if context.kafka_manager:
            context.kafka_manager.close()


# Initialize the MCP server
mcp = FastMCP("Kafka MCP Server", lifespan=kafka_lifespan)


@mcp.tool()
def kafka_initialize_connection(config_file: str, ctx: Context) -> str:
    """Connect to Kafka using a properties file"""
    try:
        kafka_manager = KafkaManager(config_file)
        # Store in the lifespan context
        ctx.request_context.lifespan_context.kafka_manager = kafka_manager
        return f"Successfully connected to Kafka using config file: {config_file}"
    except Exception as e:
        return f"Failed to connect to Kafka: {str(e)}"


@mcp.tool()
def kafka_list_topics(ctx: Context) -> str:
    """List all topics in the Kafka cluster"""
    kafka_manager = ctx.request_context.lifespan_context.kafka_manager
    if not kafka_manager:
        return "Error: Not connected to Kafka. Please use kafka_initialize_connection first."

    try:
        topics = kafka_manager.list_topics()
        if topics:
            topics_info = []
            for topic in topics:
                topics_info.append(
                    f"• {topic['name']} (partitions: {topic['partitions']}, replication: {topic['replication_factor']})"
                )
            return f"Topics in Kafka cluster:\n" + "\n".join(topics_info)
        else:
            return "No topics found in the Kafka cluster."
    except Exception as e:
        return f"Error listing topics: {str(e)}"


@mcp.tool()
def kafka_create_topic(
    name: str,
    partitions: int = 1,
    replication_factor: int = 1,
    config: Optional[Dict[str, str]] = None,
    ctx: Context = None,
) -> str:
    """Create a new Kafka topic"""
    kafka_manager = ctx.request_context.lifespan_context.kafka_manager
    if not kafka_manager:
        return "Error: Not connected to Kafka. Please use kafka_initialize_connection first."

    try:
        result = kafka_manager.create_topic(
            name, partitions, replication_factor, config
        )
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error creating topic: {str(e)}"


@mcp.tool()
def kafka_delete_topic(name: str, ctx: Context) -> str:
    """Delete a Kafka topic"""
    kafka_manager = ctx.request_context.lifespan_context.kafka_manager
    if not kafka_manager:
        return "Error: Not connected to Kafka. Please use kafka_initialize_connection first."

    try:
        result = kafka_manager.delete_topic(name)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error deleting topic: {str(e)}"


@mcp.tool()
def kafka_get_topic_info(name: str, ctx: Context) -> str:
    """Get detailed information about a specific topic"""
    kafka_manager = ctx.request_context.lifespan_context.kafka_manager
    if not kafka_manager:
        return "Error: Not connected to Kafka. Please use kafka_initialize_connection first."

    try:
        result = kafka_manager.get_topic_info(name)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting topic info: {str(e)}"


@mcp.tool()
def kafka_send_message(
    topic: str,
    message: Optional[Any] = None,
    key: Optional[str] = None,
    ctx: Context = None,
) -> str:
    """Send a message to a Kafka topic"""
    if message is None:
        return "Error: 'message' must be provided."

    kafka_manager = ctx.request_context.lifespan_context.kafka_manager
    if not kafka_manager:
        return "Error: Not connected to Kafka. Please use kafka_initialize_connection first."

    try:
        result = kafka_manager.send_message(topic, message, key)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error sending message: {str(e)}"

if __name__ == "__main__":
    # Run the server
    mcp.run()
