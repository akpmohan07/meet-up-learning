#!/usr/bin/env python3
"""
Kafka MCP Server Skeleton - Workshop Template
A Model Context Protocol server for Kafka operations using FastMCP

This is a skeleton template for the Kafka MCP Server workshop.
Participants will implement the missing functionality step by step.
"""

import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context, FastMCP

# TODO: Import kafka utilities
from kafka_utils import KafkaManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kafka-mcp-server")


@dataclass
class KafkaContext:
    """Application context holding Kafka manager"""
    kafka_manager: Optional['KafkaManager'] = None


# TODO: Create the FastMCP server with lifespan management
@asynccontextmanager
async def kafka_lifespan(server: FastMCP) -> AsyncIterator[KafkaContext]:
    """Manage Kafka connections lifecycle"""
    context = KafkaContext()
    try:
        logger.info("Starting Kafka MCP Server...")
        yield context
    finally:
        logger.info("Shutting down Kafka MCP Server...")
        # TODO: Add cleanup code here
        if context.kafka_manager:
            context.kafka_manager.close()


# TODO: Initialize the MCP server
mcp = FastMCP("Kafka MCP Server", lifespan=kafka_lifespan)

# TODO: Implement kafka_initialize_connection tool
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

# TODO: Implement kafka_list_topics tool


# TODO: Implement kafka_create_topic tool
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


# TODO: Implement kafka_delete_topic tool


# TODO: Implement kafka_get_topic_info tool


# TODO: Implement kafka_send_message tool


if __name__ == "__main__":
    # TODO: Run the server
    logger.info("Starting Kafka MCP Server...")
    mcp.run()