# Kafka MCP Server Workshop

In this guide, we will go through various flows and show you the fastest and easiest way to get started with building a Kafka MCP Server.

## What is MCP (Model Context Protocol)?

The Model Context Protocol (MCP) is an open protocol that enables secure connections between host applications (like Claude Desktop) and external data sources and tools. MCP allows AI assistants to:

- Access real-time data from external systems
- Execute operations on behalf of users
- Provide contextual information from various sources

Learn more about [MCP Protocol](https://modelcontextprotocol.io/).

## What You Will Learn

* How to set up a Kafka development environment using Docker
* How to build an MCP server using FastMCP framework
* How to implement Kafka operations as MCP tools (connect, list topics, create/delete topics, produce messages)
* How to integrate your MCP server with Claude Desktop

## What You Will Build

* A complete MCP server that provides Kafka operations as tools for AI assistants
* Integration with Claude Desktop for natural language Kafka operations

## Prerequisites

* Python 3.10 or higher
* Docker and Docker Compose
* A code editor (VS Code recommended)
* Basic understanding of Python and Kafka concepts

---

## Setup Environment and Load Data

### Step 1: Clone and Setup the Project

In a new terminal, run the following statements to set up your environment. This will:

* Clone the repository and navigate to the project directory
* Create a Python virtual environment
* Install required dependencies

```bash
# Clone the repository
git clone https://github.com/Daminivenkateswaralu/kafka-mcp.git
cd kafka-mcp

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start Kafka Development Environment

* Open the docker application

```bash
# Start Kafka using Docker Compose
docker compose up -d

# Verify Kafka is running
docker compose ps
```

This will start a single Kafka broker accessible at `localhost:9092`.

**Important**: If you use different configuration, be sure to update the `kafka.properties` file accordingly.

---

## Initialize MCP Server

Let's start by setting up the basic MCP server structure. We'll use the skeleton file `server_skeleton.py` as our starting point.

### Step 4: Import Kafka Utilities

First, uncomment and update the import statement in your `server_skeleton.py`:

```python
# TODO: Import kafka utilities
from kafka_utils import KafkaManager
```

### Step 5: Initialize the FastMCP Server

Add the following code to initialize the MCP server. Replace the TODO comment:

```python
# TODO: Initialize the MCP server
mcp = FastMCP("Kafka MCP Server", lifespan=kafka_lifespan)
```

### Step 6: Update Context Cleanup

In the `kafka_lifespan` function, add proper cleanup code:

```python
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
```

### Step 7: Add Server Startup Code

Update the main section at the bottom of the file:

```python
if __name__ == "__main__":
    # TODO: Run the server
    logger.info("Starting Kafka MCP Server...")
    mcp.run()
```

---

## Connect to Kafka

Now let's implement the connection functionality using the FastMCP framework.

### Step 8: Implement Kafka Connection Tool

Replace the `# TODO: Implement kafka_initialize_connection tool` comment with:

```python
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
```

### Step 9: Test the Connection

Run the MCP server in development mode:

```bash
mcp dev server_skeleton.py
```

### How to Start the MCP Inspector

1. **Open the MCP Inspector site** in your browser.
2. **Configure the session token**:
   - Copy the session token displayed in your terminal after running the server.
   - Paste this token into the "Session Token" field in the site's configuration.
3. **Set up the command to run your server**:
   - In the "Command" field, enter: `python`
   - In the "Arguments" field, enter: `server_skeleton.py`


This opens the **MCP Inspector**. Test your connection tool by running:

```json
{
  "name": "kafka_initialize_connection",
  "arguments": {
    "config_file": "kafka.properties"
  }
}
```

You should see: `"Successfully connected to Kafka using config file: kafka.properties"`

---

## List Topics

Using the FastMCP framework, we'll add the ability to list Kafka topics.

### Step 10: Implement Topic Listing

Replace the `# TODO: Implement kafka_list_topics tool` comment with:

```python
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
```

### Step 11: Test Topic Listing

In the MCP Inspector, first connect to Kafka, then list topics:

```json
{
  "name": "kafka_list_topics",
  "arguments": {}
}
```

---

## Create Topic

Now let's add topic creation functionality.

### Step 12: Implement Topic Creation

Replace the `# TODO: Implement kafka_create_topic tool` comment with:

```python
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
```

### Step 13: Test Topic Creation

Create a test topic:

```json
{
  "name": "kafka_create_topic",
  "arguments": {
    "name": "user-events",
    "partitions": 3,
    "replication_factor": 1
  }
}
```

Then list topics again to verify it was created.

---

## Delete Topic

Let's add the ability to delete topics.

### Step 14: Implement Topic Deletion

Replace the `# TODO: Implement kafka_delete_topic tool` comment with:

```python
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
```

---

## Get Topic Information

Add detailed topic inspection capability.

### Step 15: Implement Topic Information

Replace the `# TODO: Implement kafka_get_topic_info tool` comment with:

```python
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
```

### Step 16: Test Topic Information

Get details about your test topic:

```json
{
  "name": "kafka_get_topic_info",
  "arguments": {
    "name": "user-events"
  }
}
```

---

## Send Messages

Finally, let's implement message production.

### Step 17: Implement Message Sending

Replace the `# TODO: Implement kafka_send_message tool` comment with:

```python
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
```

### Step 18: Test Message Sending

Send a test message:

```json
{
  "name": "kafka_send_message",
  "arguments": {
    "topic": "user-events",
    "message": {
      "user_id": 123,
      "action": "login",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    "key": "user-123"
  }
}
```

---

## Integration with Claude Desktop

### Step 19: Configure Claude Desktop

To connect your MCP server with Claude Desktop, open the settings and update your `claude_desktop_config.json` file. Add your MCP server configuration under the `mcpServers` section as shown below:

```json
{
  "mcpServers": {
    "kafka": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["/path/to/your/server_skeleton.py"]
    }
  }
}
```

### Step 20: Test Natural Language Operations

Try these example interactions with Claude:

1. **Connect to Kafka**:
   ```
   "Initialize connection to Kafka using the kafka.properties file"
   ```

2. **List Topics**:
   ```
   "Show me all topics in the Kafka cluster"
   ```

3. **Create a Topic**:
   ```
   "Create a topic called 'orders' with 5 partitions"
   ```

4. **Send Messages**:
   ```
   "Send a message to the orders topic with this data: {'order_id': 'ORD-001', 'amount': 99.99}"
   ```

---

## Testing and Validation

### Sample Test Scenarios

Create these test topics and messages to verify your implementation:

#### Create Topics

```json
// Basic topic
{
  "name": "kafka_create_topic",
  "arguments": {
    "name": "test-topic",
    "partitions": 1,
    "replication_factor": 1
  }
}

// Topic with custom configuration
{
  "name": "kafka_create_topic",
  "arguments": {
    "name": "orders",
    "partitions": 5,
    "replication_factor": 1,
    "config": {
      "retention.ms": "604800000"
    }
  }
}
```

#### Send Sample Messages

```json
// User event message
{
  "name": "kafka_send_message",
  "arguments": {
    "topic": "user-events",
    "message": {
      "user_id": 12345,
      "event_type": "login",
      "timestamp": "2024-01-15T10:30:00Z",
      "ip_address": "192.168.1.100"
    }
  }
}

// Order message
{
  "name": "kafka_send_message",
  "arguments": {
    "topic": "orders",
    "message": {
      "order_id": "ORD-2024-001",
      "customer_id": 67890,
      "items": [
        {"product_id": "PROD-123", "quantity": 2, "price": 29.99}
      ],
      "total_amount": 59.98,
      "status": "pending"
    }
  }
}
```

---

## Troubleshooting

### Common Issues

1. **Connection Failed**: 
   - Verify Docker Compose is running: `docker compose ps`
   - Check Kafka logs: `docker compose logs kafka`
   - Verify `kafka.properties` configuration

2. **MCP Inspector Not Working**: 
   - Ensure you're running `mcp dev server_skeleton.py` from the correct directory
   - Check Python virtual environment is activated
   - Verify all dependencies are installed

3. **Import Errors**:
   - Make sure `kafka_utils.py` is in the same directory
   - Verify kafka-python is installed: `pip install kafka-python`

4. **Tool Execution Errors**:
   - Always connect to Kafka first using `kafka_initialize_connection`
   - Check server logs for detailed error messages
   - Verify Kafka cluster is healthy

### Debugging Tips

1. **Use Logging**: The server logs provide detailed information about operations
2. **Test Incrementally**: Test each tool individually in the MCP Inspector

---

## Conclusion

Congratulations! You've successfully completed the Kafka MCP Server workshop.

### What You've Accomplished

* Built a complete MCP server for Kafka operations
* Implemented core Kafka functionality (connect, list, create, delete, inspect, send)
* Integrated natural language Kafka management with Claude Desktop
* Created a foundation for further Kafka tooling extensions

### Next Steps

* **Add Consumer Functionality**: Implement message consumption tools
* **Error Handling**: Add more robust error handling and validation
* **Security**: Add authentication and authorization for production use
* **Monitoring**: Add health checks and metrics
* **Documentation**: Create user guides for your specific use cases

### Related Resources

* [MCP Protocol Documentation](https://modelcontextprotocol.io/)
* [FastMCP Framework](https://github.com/modelcontextprotocol/python-sdk)
* [Kafka Documentation](https://kafka.apache.org/documentation/)
* [kafka-python Library](https://kafka-python.readthedocs.io/)

---

**Happy Coding!** 🚀 