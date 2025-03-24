## Unleash the Power of LangGraph with MCP: Math & Database Examples!

🚀 Ready to take your LangGraph skills to the next level? In this tutorial, we'll dive deep into connecting LangGraph to external services using the powerful `langchain-mcp-adapter`!

We'll walk you through the best way to use MCP with two practical examples:

1️⃣ **Math Server Integration:** Learn how to build a LangGraph that performs arithmetic operations by interacting with a custom math server through MCP. We'll show you how to define your API, create the MCP configuration, and seamlessly integrate it into your LangGraph workflow.

2️⃣ **Neon Database Connection:** Discover how to connect LangGraph to a Neon database using MCP. We'll demonstrate how to query and manipulate data in your Neon DB directly from your LangGraph, opening up a world of possibilities for data-driven applications.

This repo covers:

* Understanding the `langchain-mcp-adapter` and its benefits.
* Setting up and configuring MCP for custom APIs and databases.
* Creating LangGraph flows that interact with external services.
* Practical examples with a math server and Neon DB.
* Step-by-step code walkthroughs and explanations.

*URL FOR THE POSTMAN: (Send Request Via Post Method And Remove the Brackets) * 
```pyton
http://localhost:8123/threads/{your_thread_id}/runs/stream
```

*Body Format For The POSTMAN: (Remove The Brackets) * 
```pyton
{
  "assistant_id": "(your-assistant_id)",
  "input": {
  "messages": [
    {
      "content": "{your_message}",
      "type": "human"
    }
  ]
  },
  "metadata": {},
  "config": {
      "recursion_limit": 50
  },
  "stream_mode": [
    "values"
  ],
  "feedback_keys": [
    ""
  ],
  "stream_subgraphs": false,
  "on_completion": "delete",
  "on_disconnect": "cancel",
  "after_seconds": 1
}
```
