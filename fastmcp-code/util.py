import inspect
import jsonschema

def convert_to_openai_tools(tools):
    openai_tools = []
    for t in tools:
        func = getattr(t, "fn", None)
        params = {"type": "object", "properties": {}}

        if func:
            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                params["properties"][name] = {"type": "string"}  # naive default
            required = [
                name for name, p in sig.parameters.items()
                if p.default == inspect._empty
            ]
            if required:
                params["required"] = required

        openai_tools.append({
            "type": "function",
            "name": str(t.key),
            "description": str(t.description or ""),
            "parameters": params,
        })
    return openai_tools
