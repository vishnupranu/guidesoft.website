"""
Multi-Provider AI Router
Provides unified API for routing to OpenCode AI, OpenHands, Firecrawl, 
Composio, Anthropic, Groq, Together AI, DeepSeek, Mistral, and others.
"""

from __future__ import annotations

import os
from typing import Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


# ─── Pydantic Schemas ──────────────────────────────────────────────────────────

class ProviderInfo(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    base_url: str
    models: list[str]
    capabilities: list[str]
    status: str  # "configured", "available", "unconfigured"
    api_key_env: Optional[str] = None
    docs_url: Optional[str] = None


class ProviderTestResult(BaseModel):
    provider_id: str
    success: bool
    message: str
    latency_ms: Optional[float] = None


# ─── Provider Registry ─────────────────────────────────────────────────────────

def _check_key(env_var: str) -> str:
    """Return 'configured' if env var is set, 'unconfigured' otherwise."""
    return "configured" if os.environ.get(env_var) else "unconfigured"


def get_providers() -> list[ProviderInfo]:
    return [
        ProviderInfo(
            id="openai",
            name="OpenAI",
            description="GPT-4o, GPT-4-turbo, GPT-4o-mini, o1, o1-mini, o3 models.",
            icon="🟢",
            base_url="https://api.openai.com/v1",
            models=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "o1", "o1-mini", "o3-mini", "gpt-3.5-turbo"],
            capabilities=["chat", "completion", "vision", "function_calling", "streaming", "embeddings"],
            status=_check_key("OPENAI_API_KEY"),
            api_key_env="OPENAI_API_KEY",
            docs_url="https://platform.openai.com/docs",
        ),
        ProviderInfo(
            id="anthropic",
            name="Anthropic Claude",
            description="Claude 4 Opus, Claude 3.7 Sonnet, Claude 3.5 Haiku — best for coding and reasoning.",
            icon="🟠",
            base_url="https://api.anthropic.com",
            models=["claude-opus-4-5", "claude-sonnet-4-5", "claude-haiku-4-5", "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"],
            capabilities=["chat", "completion", "vision", "function_calling", "streaming", "artifacts"],
            status=_check_key("ANTHROPIC_API_KEY"),
            api_key_env="ANTHROPIC_API_KEY",
            docs_url="https://docs.anthropic.com",
        ),
        ProviderInfo(
            id="google",
            name="Google Gemini",
            description="Gemini 2.0 Flash, Gemini 2.5 Pro — multimodal AI with large context windows.",
            icon="🔵",
            base_url="https://generativelanguage.googleapis.com",
            models=["gemini-2.0-flash", "gemini-2.5-pro", "gemini-2.0-flash-thinking", "gemini-1.5-pro"],
            capabilities=["chat", "completion", "vision", "function_calling", "streaming", "embeddings", "grounding"],
            status=_check_key("GOOGLE_API_KEY"),
            api_key_env="GOOGLE_API_KEY",
            docs_url="https://ai.google.dev",
        ),
        ProviderInfo(
            id="groq",
            name="Groq",
            description="Ultra-fast inference — Llama 3.3 70B, Mixtral, Gemma. Best for low-latency applications.",
            icon="⚡",
            base_url="https://api.groq.com/openai/v1",
            models=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
            capabilities=["chat", "completion", "streaming", "function_calling"],
            status=_check_key("GROQ_API_KEY"),
            api_key_env="GROQ_API_KEY",
            docs_url="https://console.groq.com/docs",
        ),
        ProviderInfo(
            id="deepseek",
            name="DeepSeek",
            description="DeepSeek V3 and R1 — high performance at low cost. Best for coding and math.",
            icon="🌊",
            base_url="https://api.deepseek.com/v1",
            models=["deepseek-chat", "deepseek-reasoner", "deepseek-coder"],
            capabilities=["chat", "completion", "streaming", "function_calling", "reasoning"],
            status=_check_key("DEEPSEEK_API_KEY"),
            api_key_env="DEEPSEEK_API_KEY",
            docs_url="https://platform.deepseek.com/docs",
        ),
        ProviderInfo(
            id="together",
            name="Together AI",
            description="Open-source models at scale — Llama, Mistral, Qwen, CodeLlama, and more.",
            icon="🤝",
            base_url="https://api.together.xyz/v1",
            models=["meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", "mistralai/Mixtral-8x7B-Instruct-v0.1", "Qwen/Qwen2.5-72B-Instruct-Turbo"],
            capabilities=["chat", "completion", "streaming", "fine_tuning"],
            status=_check_key("TOGETHER_API_KEY"),
            api_key_env="TOGETHER_API_KEY",
            docs_url="https://docs.together.ai",
        ),
        ProviderInfo(
            id="mistral",
            name="Mistral AI",
            description="Mistral Large, Mixtral, Mistral 7B — efficient European AI models.",
            icon="🌪️",
            base_url="https://api.mistral.ai/v1",
            models=["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest", "open-mixtral-8x22b"],
            capabilities=["chat", "completion", "streaming", "function_calling", "embeddings"],
            status=_check_key("MISTRAL_API_KEY"),
            api_key_env="MISTRAL_API_KEY",
            docs_url="https://docs.mistral.ai",
        ),
        ProviderInfo(
            id="openrouter",
            name="OpenRouter",
            description="Access 200+ models from one API — GPT-4o, Claude, Gemini, Llama, and more.",
            icon="🛣️",
            base_url="https://openrouter.ai/api/v1",
            models=["anthropic/claude-3.5-sonnet", "openai/gpt-4o", "google/gemini-2.0-flash", "meta-llama/llama-3.3-70b-instruct"],
            capabilities=["chat", "completion", "streaming", "vision", "function_calling"],
            status=_check_key("OPENROUTER_API_KEY"),
            api_key_env="OPENROUTER_API_KEY",
            docs_url="https://openrouter.ai/docs",
        ),
        ProviderInfo(
            id="perplexity",
            name="Perplexity AI",
            description="Online LLMs with real-time web search — Sonar, Sonar Pro models.",
            icon="🔍",
            base_url="https://api.perplexity.ai",
            models=["sonar", "sonar-pro", "sonar-reasoning", "sonar-reasoning-pro"],
            capabilities=["chat", "completion", "streaming", "web_search", "citations"],
            status=_check_key("PERPLEXITY_API_KEY"),
            api_key_env="PERPLEXITY_API_KEY",
            docs_url="https://docs.perplexity.ai",
        ),
        ProviderInfo(
            id="ollama",
            name="Ollama",
            description="Local open-source models — Llama, Mistral, CodeLlama, Phi, Gemma, and more.",
            icon="🦙",
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            models=["llama3.2", "mistral", "codellama", "phi4", "gemma2", "deepseek-r1", "qwen2.5-coder"],
            capabilities=["chat", "completion", "streaming", "function_calling", "embeddings", "vision"],
            status="configured" if os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434") else "unconfigured",
            api_key_env=None,
            docs_url="https://ollama.ai",
        ),
        ProviderInfo(
            id="opencode",
            name="OpenCode AI",
            description="Autonomous AI coding agent — reviews, generates, and commits production code.",
            icon="🤖",
            base_url=os.environ.get("OPENCODE_API_URL", "https://api.opencode.ai"),
            models=["opencode-v1"],
            capabilities=["code_generation", "code_review", "git_commits", "autonomous_coding"],
            status=_check_key("OPENCODE_API_KEY"),
            api_key_env="OPENCODE_API_KEY",
            docs_url="https://opencode.ai",
        ),
        ProviderInfo(
            id="openhands",
            name="OpenHands",
            description="Autonomous software development agent — writes, tests, and deploys code autonomously.",
            icon="🙌",
            base_url=os.environ.get("OPENHANDS_URL", "http://localhost:3000"),
            models=["openhands-v1"],
            capabilities=["autonomous_coding", "testing", "debugging", "deployment"],
            status="configured" if os.environ.get("OPENHANDS_URL") else "unconfigured",
            api_key_env="OPENHANDS_API_KEY",
            docs_url="https://docs.all-hands.dev",
        ),
        ProviderInfo(
            id="firecrawl",
            name="Firecrawl",
            description="Web scraping and data extraction API — crawl any website into clean structured data.",
            icon="🔥",
            base_url="https://api.firecrawl.dev",
            models=["firecrawl-v1"],
            capabilities=["web_scraping", "crawling", "structured_extraction", "llm_extraction"],
            status=_check_key("FIRECRAWL_API_KEY"),
            api_key_env="FIRECRAWL_API_KEY",
            docs_url="https://docs.firecrawl.dev",
        ),
        ProviderInfo(
            id="composio",
            name="Composio",
            description="250+ tool integrations for AI agents — GitHub, Slack, Notion, Linear, Gmail, and more.",
            icon="🔧",
            base_url="https://backend.composio.dev/api",
            models=["composio-v1"],
            capabilities=["github", "slack", "notion", "linear", "gmail", "google_calendar", "jira", "tool_execution"],
            status=_check_key("COMPOSIO_API_KEY"),
            api_key_env="COMPOSIO_API_KEY",
            docs_url="https://docs.composio.dev",
        ),
        ProviderInfo(
            id="claude-code",
            name="Claude Code (Anthropic CLI)",
            description="Anthropic's official CLI coding agent — agentic coding with filesystem and git access.",
            icon="🧑‍💻",
            base_url="https://api.anthropic.com",
            models=["claude-opus-4-5", "claude-sonnet-4-5"],
            capabilities=["agentic_coding", "filesystem", "git", "bash", "mcp"],
            status=_check_key("ANTHROPIC_API_KEY"),
            api_key_env="ANTHROPIC_API_KEY",
            docs_url="https://docs.anthropic.com/claude-code",
        ),
        ProviderInfo(
            id="azure-openai",
            name="Azure OpenAI",
            description="OpenAI models deployed on Microsoft Azure — enterprise compliance and private endpoints.",
            icon="☁️",
            base_url=os.environ.get("AZURE_OPENAI_BASE_URL", "https://your-resource.openai.azure.com"),
            models=["gpt-4o", "gpt-4-turbo", "gpt-35-turbo"],
            capabilities=["chat", "completion", "streaming", "function_calling", "embeddings"],
            status=_check_key("AZURE_OPENAI_API_KEY"),
            api_key_env="AZURE_OPENAI_API_KEY",
            docs_url="https://learn.microsoft.com/azure/ai-services/openai",
        ),
        ProviderInfo(
            id="cohere",
            name="Cohere",
            description="Command R+ and Command models — RAG-optimized with grounding and citations.",
            icon="🌐",
            base_url="https://api.cohere.com/v2",
            models=["command-r-plus", "command-r", "command-a-03-2025"],
            capabilities=["chat", "completion", "streaming", "embeddings", "rerank", "web_search"],
            status=_check_key("COHERE_API_KEY"),
            api_key_env="COHERE_API_KEY",
            docs_url="https://docs.cohere.com",
        ),
        ProviderInfo(
            id="xai",
            name="xAI Grok",
            description="Grok 2 and Grok 3 — real-time information with X/Twitter integration.",
            icon="✖️",
            base_url="https://api.x.ai/v1",
            models=["grok-3", "grok-3-mini", "grok-2-1212", "grok-2-vision-1212"],
            capabilities=["chat", "completion", "streaming", "vision", "real_time_info"],
            status=_check_key("XAI_API_KEY"),
            api_key_env="XAI_API_KEY",
            docs_url="https://docs.x.ai",
        ),
    ]


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[ProviderInfo])
async def list_providers():
    """List all AI providers with their status."""
    return get_providers()


@router.get("/{provider_id}", response_model=ProviderInfo)
async def get_provider(provider_id: str):
    """Get details of a specific provider."""
    providers = {p.id: p for p in get_providers()}
    if provider_id not in providers:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_id}' not found")
    return providers[provider_id]


@router.get("/{provider_id}/models", response_model=list[str])
async def get_provider_models(provider_id: str):
    """Get models available for a specific provider."""
    providers = {p.id: p for p in get_providers()}
    if provider_id not in providers:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_id}' not found")
    return providers[provider_id].models


@router.get("/configured/", response_model=list[ProviderInfo])
async def get_configured_providers():
    """List only providers that have been configured with API keys."""
    return [p for p in get_providers() if p.status == "configured"]


@router.get("/models/all", response_model=dict[str, list[str]])
async def get_all_models():
    """Get all models across all configured providers."""
    result = {}
    for provider in get_providers():
        if provider.status == "configured":
            result[provider.id] = provider.models
    return result
