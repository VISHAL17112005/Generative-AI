import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime

import os
os.environ["GRPC_VERBOSITY"] = "NONE"

load_dotenv()  # make sure GOOGLE_API_KEY is in your .env file

def call_gemini(prompt):
    # configure the client with your API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("models/gemini-2.5-flash")
    
    # Get model info only once at the start
    try:
        model_info = next(m for m in genai.list_models() if m.name == "models/gemini-2.5-flash")
        
        print("\n" + "="*50)
        print("Model Information:")
        print(f"Name: {model_info.name}")
        print(f"Display Name: {model_info.display_name}")
        print(f"Description: {model_info.description}")
        print(f"Generation Methods: {', '.join(model_info.supported_generation_methods)}")
        print("="*50 + "\n")
    except StopIteration:
        print("Model information not available")

    response = model.generate_content(prompt)
    
    # Get detailed token usage
    usage = response.usage_metadata
    prompt_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count
    reported_total = usage.total_token_count
    calculated_total = prompt_tokens + output_tokens
    
    print("\n" + "-"*50)
    print("Token Usage Statistics:")
    print(f"Your Prompt Tokens: {prompt_tokens}")
    print(f"Response Tokens: {output_tokens}")
    print(f"Visible Tokens (Prompt + Response): {calculated_total}")
    print(f"System & Internal Tokens: {reported_total - calculated_total}")
    print(f"Total Tokens Charged: {reported_total}")
    print("-"*50 + "\n")
    
    return response.text

def context_combine_prompt(context_from_logs: str, topic: str, response_style: str = "Comprehensive", include_sources: bool = True) -> str:
    """
    Create a prompt that combines context from logs with a question.

    Args:
        context_from_logs (str): The context content from scraped logs.
        topic (str): The question or topic to ask about.
        response_style (str): Style of response (Comprehensive, Concise, Technical, Beginner-friendly).
        include_sources (bool): Whether to include source references.

    Returns:
        str: The combined prompt for the LLM.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Add debugging information
    context_length = len(context_from_logs)
    print(f"\n🔍 CONTEXT ANALYSIS:")
    print(f"   📏 Context length: {context_length} characters")
    print(f"   💰 Estimated tokens: ~{context_length // 4} tokens")
    print(f"   📊 Optimization status: {'✅ OPTIMIZED' if context_length <= 7500 else '⚠️  LARGE CONTEXT'}")
    print(f"   📄 Context preview: {context_from_logs[:200]}...")
    
    # Style-specific instructions
    style_instructions = {
        "Comprehensive": "Provide a thorough, well-structured answer with extensive details, examples, and explanations.",
        "Concise": "Provide a clear, focused answer that covers the key points without unnecessary detail.",
        "Technical": "Provide a detailed, technical answer with specific terminology and in-depth explanations.",
        "Beginner-friendly": "Provide a clear, easy-to-understand answer with simple explanations and examples."
    }
    
    source_instruction = "Include source references and citations where appropriate." if include_sources else "Focus on the content without extensive source citations."
    
    prompt = f"""You are a helpful research assistant. Based on the following context information (retrieved on {current_date}), please provide a {response_style.lower()} answer to the user's question.

CONTEXT INFORMATION:
{context_from_logs}

INSTRUCTIONS:
- {style_instructions[response_style]}
- Base your answer ONLY on the context provided above
- If the context contains multiple sources or perspectives, synthesize them coherently
- Use clear headings and formatting to organize your response
- {source_instruction}
- Do not make up information that is not present in the context
- If the context is insufficient to fully answer the question, explain what information is available and what might be missing

QUESTION: {topic}

Please provide a {response_style.lower()} answer:"""
    
    return prompt




