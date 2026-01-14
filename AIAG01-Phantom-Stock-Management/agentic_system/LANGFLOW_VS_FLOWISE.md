# 🎯 Quick Reference: Langflow vs Flowise

## Side-by-Side Comparison

---

## Installation

| Platform | Command |
|----------|---------|
| **Langflow** | `pip install langflow` |
| **Flowise** | `npm install -g flowise` |

---

## Starting the Platform

| Platform | Command | URL |
|----------|---------|-----|
| **Langflow** | `langflow run` | http://localhost:7860 |
| **Flowise** | `npx flowise start` | http://localhost:3000 |

---

## Node Types

### Langflow
- **Agent:** Conversational Agent
- **Tool:** Custom Tool (Python)
- **Data Source:** API Request
- **Output:** Text Output

### Flowise
- **Agent:** Conversational Agent
- **Tool:** Custom Tool (JavaScript)
- **Data Source:** API Chain
- **Output:** Final Output

---

## Tool Language

| Platform | Language | Example |
|----------|----------|---------|
| **Langflow** | Python | `def validate_data(data):` |
| **Flowise** | JavaScript | `async function validateData(data) {` |

---

## Agent Configuration

### Langflow
```
Agent Node → System Message → Add Tool → Python Code
```

### Flowise
```
Agent Node → System Message → Add Tool → JavaScript Code
```

---

## Connection Method

### Langflow
- Drag from output handle
- Drop on input handle
- Automatic type checking

### Flowise
- Click output port
- Drag to input port
- Visual connection line

---

## Testing

### Langflow
1. Click "Run" button
2. View output in node
3. Check logs tab

### Flowise
1. Click "Test" button
2. Enter test input
3. View chat response

---

## Export/Import

### Langflow
- Export: JSON file
- Import: Upload JSON
- Format: Langflow-specific

### Flowise
- Export: JSON file
- Import: Upload JSON
- Format: Flowise-specific

---

## API Deployment

### Langflow
```
Endpoint: http://localhost:7860/api/v1/run/{flow_id}
Method: POST
```

### Flowise
```
Endpoint: http://localhost:3000/api/v1/prediction/{chatflow_id}
Method: POST
```

---

## Visual Flow

### Langflow
```
[Node] → [Node] → [Node]
  ↓        ↓        ↓
Output   Output   Output
```

### Flowise
```
[Node] → [Node] → [Node]
         ↓
      [Output]
```

---

## Memory Support

### Langflow
- Buffer Memory
- Conversation Buffer Memory
- Add to each agent

### Flowise
- Buffer Memory
- Conversation Buffer Memory
- Connect to agents

---

## Pros and Cons

### Langflow

**Pros:**
- ✅ Python-based (familiar for data scientists)
- ✅ Rich Python ecosystem
- ✅ Better for ML/AI workflows
- ✅ More agent types

**Cons:**
- ❌ Requires Python knowledge
- ❌ Slower startup
- ❌ Less polished UI

### Flowise

**Pros:**
- ✅ JavaScript-based (familiar for web devs)
- ✅ Faster startup
- ✅ Cleaner UI
- ✅ Better for web integration

**Cons:**
- ❌ Requires JavaScript knowledge
- ❌ Fewer agent types
- ❌ Less ML/AI support

---

## Which to Choose?

### Choose Langflow if:
- You're comfortable with Python
- You need ML/AI capabilities
- You want more agent types
- You're building data science workflows

### Choose Flowise if:
- You're comfortable with JavaScript
- You need web integration
- You want a cleaner UI
- You're building chatbots

---

## Agent Pipeline in Both

### Langflow
```python
# Monitoring Agent Tool
def validate_data(inventory_data):
    # Python code here
    return result

# Validation Agent Tool
def calculate_deviations(processed_data):
    # Python code here
    return result
```

### Flowise
```javascript
// Monitoring Agent Tool
async function validateData(inventoryData) {
    // JavaScript code here
    return result;
}

// Validation Agent Tool
async function calculateDeviations(processedData) {
    // JavaScript code here
    return result;
}
```

---

## Integration with Backend

### Both Platforms
```
Backend API (http://localhost:8000)
         ↓
   Langflow/Flowise
         ↓
    Dashboard
```

---

## Quick Setup Comparison

| Step | Langflow | Flowise |
|------|----------|---------|
| 1. Install | `pip install langflow` | `npm install -g flowise` |
| 2. Start | `langflow run` | `npx flowise start` |
| 3. Open | http://localhost:7860 | http://localhost:3000 |
| 4. Create | New Flow | New Chatflow |
| 5. Add Agents | 4 Agent nodes | 4 Agent nodes |
| 6. Add Tools | Python functions | JavaScript functions |
| 7. Connect | Drag & drop | Click & drag |
| 8. Test | Run button | Test button |
| 9. Deploy | Get API endpoint | Get API endpoint |

---

## Tool Code Comparison

### Monitoring Agent

**Langflow (Python):**
```python
def validate_data(inventory_data):
    anomalies = []
    for record in inventory_data:
        if record["reported_stock"] < 0:
            anomalies.append(record)
    return {"anomalies": anomalies}
```

**Flowise (JavaScript):**
```javascript
async function validateData(inventoryData) {
    const anomalies = [];
    for (const record of inventoryData) {
        if (record.reported_stock < 0) {
            anomalies.push(record);
        }
    }
    return JSON.stringify({anomalies});
}
```

---

## Final Recommendation

### For AIAG01 Project:

**Use Langflow if:**
- Your team knows Python
- You want to extend with ML models
- You need complex data processing

**Use Flowise if:**
- Your team knows JavaScript
- You want faster setup
- You need web-first integration

**Both work equally well for the phantom stock detection system!**

---

## 📚 Resources

### Langflow
- Docs: https://docs.langflow.org
- GitHub: https://github.com/logspace-ai/langflow
- Guide: `LANGFLOW_INTEGRATION.md`

### Flowise
- Docs: https://docs.flowiseai.com
- GitHub: https://github.com/FlowiseAI/Flowise
- Guide: `FLOWISE_INTEGRATION.md`

---

## ✅ Summary

Both platforms support:
- ✅ 4 autonomous agents
- ✅ Custom tools per agent
- ✅ Visual pipeline
- ✅ API deployment
- ✅ Easy testing

**Choose based on your team's language preference!**
