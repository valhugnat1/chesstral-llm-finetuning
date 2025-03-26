from mistral_inference.transformer import Transformer
from mistral_inference.generate import generate
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage, SystemMessage, AssistantMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
import time
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
import uuid

app = FastAPI(title="Mistral Local API")

# Initialize Mistral components
tokenizer = MistralTokenizer.from_file("/root/chesstral-llm-finetuning/mistral-finetune/mistral_model/tokenizer.model.v3")
model = Transformer.from_folder("/root/chesstral-llm-finetuning/mistral-finetune/mistral_model")
model.load_lora("/root/chesstral-llm-finetuning/mistral-finetune/runs/run2/checkpoints/checkpoint_000300/consolidated/lora.safetensors")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "mistral-finetune"
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 64
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None

@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    # try:

        messages = [UserMessage(content=message.content) for message in request.messages]
        print (messages)
        completion_request = ChatCompletionRequest(messages=messages)

        print (completion_request)
        
        # Generate tokens
        tokens = tokenizer.encode_chat_completion(completion_request).tokens
        print (tokens)
        out_tokens, _ = generate(
            [tokens], 
            model, 
            max_tokens=request.max_tokens, 
            temperature=request.temperature,
            eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id
        )
        
        # Decode response
        result = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
        
        # Calculate token usage (simplified)
        prompt_tokens = len(tokens)
        completion_tokens = len(out_tokens[0])
        total_tokens = prompt_tokens + completion_tokens
        
        # Format response
        return {
            "id": str(uuid.uuid4()),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": result
                },
                "index": 0,
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            }
        }
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Mistral Local API is running. Send requests to /chat/completions"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    