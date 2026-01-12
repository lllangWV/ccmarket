# The Inference Loop

The core of every coding agent is a simple loop that:
1. Sends messages to the LLM
2. Checks for tool calls
3. Executes tools
4. Feeds results back

## Complete Go Implementation

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "os"
)

const ANTHROPIC_API = "https://api.anthropic.com/v1/messages"

type Message struct {
    Role    string      `json:"role"`
    Content interface{} `json:"content"`
}

type ToolUse struct {
    Type  string                 `json:"type"`
    ID    string                 `json:"id"`
    Name  string                 `json:"name"`
    Input map[string]interface{} `json:"input"`
}

type ToolResult struct {
    Type      string `json:"type"`
    ToolUseID string `json:"tool_use_id"`
    Content   string `json:"content"`
}

type Response struct {
    Content  []json.RawMessage `json:"content"`
    StopReason string          `json:"stop_reason"`
}

func callClaude(messages []Message, tools []map[string]interface{}) (*Response, error) {
    payload := map[string]interface{}{
        "model":      "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "messages":   messages,
        "tools":      tools,
    }

    body, _ := json.Marshal(payload)
    req, _ := http.NewRequest("POST", ANTHROPIC_API, bytes.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("x-api-key", os.Getenv("ANTHROPIC_API_KEY"))
    req.Header.Set("anthropic-version", "2023-06-01")

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    respBody, _ := io.ReadAll(resp.Body)
    var response Response
    json.Unmarshal(respBody, &response)
    return &response, nil
}

func runAgent(userMessage string, tools map[string]ToolDefinition) string {
    // Build tool definitions for API
    var apiTools []map[string]interface{}
    for _, tool := range tools {
        apiTools = append(apiTools, map[string]interface{}{
            "name":         tool.Name,
            "description":  tool.Description,
            "input_schema": tool.InputSchema,
        })
    }

    messages := []Message{{Role: "user", Content: userMessage}}

    for {
        response, err := callClaude(messages, apiTools)
        if err != nil {
            return fmt.Sprintf("Error: %v", err)
        }

        // Check if we're done (no tool use)
        if response.StopReason == "end_turn" {
            return extractTextContent(response.Content)
        }

        // Process response content
        var assistantContent []interface{}
        var toolResults []ToolResult

        for _, block := range response.Content {
            var content map[string]interface{}
            json.Unmarshal(block, &content)

            if content["type"] == "text" {
                assistantContent = append(assistantContent, content)
            } else if content["type"] == "tool_use" {
                var toolUse ToolUse
                json.Unmarshal(block, &toolUse)
                assistantContent = append(assistantContent, toolUse)

                // Execute the tool
                tool := tools[toolUse.Name]
                result, err := tool.Function(toolUse.Input)
                if err != nil {
                    result = fmt.Sprintf("Error: %v", err)
                }

                toolResults = append(toolResults, ToolResult{
                    Type:      "tool_result",
                    ToolUseID: toolUse.ID,
                    Content:   result,
                })
            }
        }

        // Add assistant message with tool uses
        messages = append(messages, Message{
            Role:    "assistant",
            Content: assistantContent,
        })

        // Add tool results
        if len(toolResults) > 0 {
            var resultsContent []interface{}
            for _, r := range toolResults {
                resultsContent = append(resultsContent, r)
            }
            messages = append(messages, Message{
                Role:    "user",
                Content: resultsContent,
            })
        }

        // If no tool calls, we're done
        if response.StopReason != "tool_use" {
            return extractTextContent(response.Content)
        }
    }
}

func extractTextContent(content []json.RawMessage) string {
    var result string
    for _, block := range content {
        var c map[string]interface{}
        json.Unmarshal(block, &c)
        if c["type"] == "text" {
            result += c["text"].(string)
        }
    }
    return result
}
```

## Loop Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              APPEND TO MESSAGES                         │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              CALL LLM (with tools)                      │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              CHECK STOP REASON                          │
├─────────────────────┴───────────────────────────────────┤
│  stop_reason == "end_turn"  │  stop_reason == "tool_use"│
│            │                │            │              │
│            ▼                │            ▼              │
│     RETURN RESPONSE         │    EXECUTE TOOLS          │
│                             │            │              │
│                             │            ▼              │
│                             │    APPEND RESULTS         │
│                             │            │              │
│                             │            ▼              │
│                             │    LOOP BACK TO CALL LLM  │
└─────────────────────────────────────────────────────────┘
```

## Key Implementation Details

### Stop Reasons

- `end_turn`: Model finished, return response
- `tool_use`: Model wants to use tools, execute and continue
- `max_tokens`: Hit token limit, may need to continue

### Message Format

User messages contain either text or tool results:
```json
{"role": "user", "content": "Your message"}
{"role": "user", "content": [{"type": "tool_result", "tool_use_id": "xxx", "content": "result"}]}
```

Assistant messages contain text and/or tool uses:
```json
{"role": "assistant", "content": [
    {"type": "text", "text": "I'll read that file..."},
    {"type": "tool_use", "id": "xxx", "name": "read_file", "input": {"path": "foo.txt"}}
]}
```

### Error Handling

Always return tool errors as results, don't crash:
```go
result, err := tool.Function(input)
if err != nil {
    result = fmt.Sprintf("Error: %v", err)
}
```

The model can then decide how to handle the error.

## Python Implementation

```python
import anthropic

client = anthropic.Anthropic()

def run_agent(user_message: str, tools: list[dict]) -> str:
    messages = [{"role": "user", "content": user_message}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=messages,
            tools=tools
        )
        
        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if b.type == "text")
        
        # Add assistant response
        messages.append({"role": "assistant", "content": response.content})
        
        # Execute tools and collect results
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            break
    
    return "".join(b.text for b in response.content if b.type == "text")
```
