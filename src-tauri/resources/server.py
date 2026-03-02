import os
import json
import uvicorn
from typing import List, Optional, Union, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI(title="LiteLLM OpenAI-Compatible Server")

class ChatCompletionMessage(BaseModel):
    role: str
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatCompletionMessage]
    stream: Optional[bool] = False
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    response_format: Optional[Dict[str, Any]] = None

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completions endpoint.
    Uses LiteLLM to handle the actual LLM call.
    Validated with Pydantic for type safety.
    """
    try:
        # Convert Pydantic model to dict, excluding unset fields to let LiteLLM use its defaults
        body = request.model_dump(exclude_unset=True)
        
        if body.get("stream"):
            async def event_generator():
                # acompletion returns an async generator when stream=True
                response = await litellm.acompletion(**body)
                async for chunk in response:
                    # chunk is a litellm.utils.CustomStreamWrapper or ModelResponse
                    # which is compatible with OpenAI's ChatCompletionChunk
                    if hasattr(chunk, "model_dump_json"):
                        content = chunk.model_dump_json()
                    else:
                        content = json.dumps(chunk)
                    yield f"data: {content}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(event_generator(), media_type="text/event-stream")
        else:
            response = await litellm.acompletion(**body)
            # response is a ModelResponse, compatible with OpenAI's ChatCompletion
            return response

    except Exception as e:
        print(f"Error in chat_completions: {e}")
        # Improve error reporting by returning LiteLLM's specific error if possible
        status_code = getattr(e, "status_code", 500)
        raise HTTPException(status_code=status_code, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

def run(port=18888):
    print(f"Starting OpenAI-compatible server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    port = int(os.environ.get("SERVER_PORT", 18888))
    run(port=port)

