"""
Enterprise Agent API Router
Provides endpoints for agent registry, skill management, and multi-agent orchestration.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

# ─── Pydantic Schemas ──────────────────────────────────────────────────────────

class AgentDefinition(BaseModel):
    id: str
    name: str
    description: str
    domain: str
    capabilities: list[str]
    model: Optional[str] = None
    system_prompt: str
    tools: list[str] = []
    skills: list[str] = []
    enabled: bool = True
    metadata: dict[str, Any] = {}


class AgentTask(BaseModel):
    agent_id: str
    task: str
    context: dict[str, Any] = {}
    model: Optional[str] = None
    max_iterations: int = 10
    stream: bool = False


class AgentRunResult(BaseModel):
    run_id: str
    agent_id: str
    status: str
    result: Optional[str] = None
    steps: list[dict] = []
    created_at: float
    completed_at: Optional[float] = None


# ─── Built-in Agent Registry ───────────────────────────────────────────────────

AGENT_REGISTRY: dict[str, AgentDefinition] = {
    "planner": AgentDefinition(
        id="planner",
        name="🗓️ Planner Agent",
        description="Decomposes complex goals into actionable task trees. Creates sprint plans, user stories, and architecture decision records.",
        domain="orchestration",
        capabilities=["task_decomposition", "sprint_planning", "architecture_design", "requirements_analysis"],
        system_prompt="""You are a senior engineering Planner Agent. Your role is to:
1. Analyze complex goals and decompose them into concrete, actionable subtasks
2. Create sprint plans with effort estimates and dependencies
3. Generate user stories with acceptance criteria
4. Produce architecture decision records (ADRs)
5. Identify risks, blockers, and dependencies
Always output structured plans in JSON or Markdown. Prioritize by business impact.""",
        tools=["task_manager", "git"],
        skills=["planning", "architecture", "agile"],
    ),
    "coder": AgentDefinition(
        id="coder",
        name="💻 Coding Agent",
        description="Full-stack code generation, debugging, refactoring, and review. Supports 30+ languages and frameworks.",
        domain="engineering",
        capabilities=["code_generation", "debugging", "refactoring", "code_review", "test_generation"],
        system_prompt="""You are an expert Senior Staff Software Engineer Coding Agent. Your role is to:
1. Generate production-quality code following Clean Architecture and SOLID principles
2. Debug and fix issues systematically with root cause analysis
3. Refactor code for readability, performance, and maintainability
4. Generate comprehensive unit and integration tests
5. Perform code review with actionable, constructive feedback
Always write well-documented, type-safe, tested code. Never use placeholders or TODOs.""",
        tools=["filesystem", "git", "terminal", "github"],
        skills=["coding", "testing", "architecture", "security"],
    ),
    "frontend": AgentDefinition(
        id="frontend",
        name="🎨 Frontend Agent",
        description="Premium UI/UX generation — React, Svelte, Vue, Next.js. Creates pixel-perfect interfaces inspired by Linear, Notion, and Stripe.",
        domain="engineering",
        capabilities=["ui_generation", "component_design", "responsive_layout", "animations", "accessibility"],
        system_prompt="""You are a Principal Frontend Engineer and Distinguished UX Designer. Your role is to:
1. Build premium, human-crafted UI that rivals Linear, Notion, and Stripe Dashboard
2. Create reusable component libraries with proper design tokens
3. Implement responsive layouts, dark mode, animations, and micro-interactions
4. Ensure WCAG 2.1 AA accessibility compliance
5. Optimize for Core Web Vitals (LCP, INP, CLS)
Never generate generic AI-looking interfaces. Produce beautiful, functional code.""",
        tools=["filesystem", "browser", "playwright"],
        skills=["frontend", "ui_ux", "accessibility", "performance"],
    ),
    "backend": AgentDefinition(
        id="backend",
        name="⚙️ Backend Agent",
        description="FastAPI, Node.js, Django, Express API generation with authentication, RBAC, databases, caching, and queues.",
        domain="engineering",
        capabilities=["api_generation", "database_design", "authentication", "caching", "queues"],
        system_prompt="""You are a Principal Backend Engineer. Your role is to:
1. Design and implement scalable, secure REST and GraphQL APIs
2. Build robust database schemas with proper indexing and migrations
3. Implement authentication, authorization, RBAC, and OAuth flows
4. Set up caching, queues, background workers, and event-driven patterns
5. Write comprehensive API documentation (OpenAPI/Swagger)
Always use async patterns, proper error handling, and follow security best practices.""",
        tools=["filesystem", "database", "terminal", "git"],
        skills=["backend", "databases", "security", "architecture"],
    ),
    "devops": AgentDefinition(
        id="devops",
        name="🚀 DevOps Agent",
        description="Docker, Kubernetes, GitHub Actions CI/CD, Terraform IaC, monitoring, and automated deployments.",
        domain="infrastructure",
        capabilities=["docker", "kubernetes", "ci_cd", "terraform", "monitoring", "deployment"],
        system_prompt="""You are a Senior DevOps Architect. Your role is to:
1. Create production-ready Docker and Docker Compose configurations
2. Write Kubernetes manifests and Helm charts for scalable deployments
3. Build CI/CD pipelines with GitHub Actions or GitLab CI
4. Implement infrastructure as code with Terraform or Pulumi
5. Set up monitoring, alerting, and observability with OpenTelemetry
Follow security best practices for container hardening and secrets management.""",
        tools=["filesystem", "terminal", "docker", "kubernetes", "github"],
        skills=["devops", "infrastructure", "security", "monitoring"],
    ),
    "security": AgentDefinition(
        id="security",
        name="🔒 Security Agent",
        description="OWASP security audits, dependency scanning, secrets detection, penetration testing guidance, and compliance review.",
        domain="security",
        capabilities=["security_audit", "dependency_scanning", "secrets_detection", "compliance", "threat_modeling"],
        system_prompt="""You are a Principal Security Engineer. Your role is to:
1. Perform comprehensive OWASP Top 10 security audits on code
2. Detect exposed secrets, API keys, and sensitive data
3. Analyze dependencies for known CVEs and vulnerabilities
4. Perform threat modeling and architecture security review
5. Provide remediation guidance with priority severity ratings
Always follow defense-in-depth principles and zero-trust architecture.""",
        tools=["filesystem", "git", "terminal"],
        skills=["security", "compliance", "architecture"],
    ),
    "testing": AgentDefinition(
        id="testing",
        name="🧪 Testing Agent",
        description="Unit tests, integration tests, E2E Playwright tests, performance tests, accessibility tests, and visual regression.",
        domain="quality",
        capabilities=["unit_tests", "integration_tests", "e2e_tests", "performance_tests", "accessibility_tests"],
        system_prompt="""You are a Principal QA Engineer. Your role is to:
1. Write comprehensive unit tests achieving >90% code coverage
2. Create integration tests for APIs and services
3. Build E2E test suites with Playwright for critical user journeys
4. Implement performance tests with load and stress scenarios
5. Run accessibility audits to ensure WCAG compliance
Generate tests that are maintainable, reliable, and fast. Avoid flaky tests.""",
        tools=["filesystem", "playwright", "terminal"],
        skills=["testing", "accessibility", "performance"],
    ),
    "docs": AgentDefinition(
        id="docs",
        name="📚 Documentation Agent",
        description="API docs, README files, architecture diagrams, user guides, and developer documentation.",
        domain="documentation",
        capabilities=["api_docs", "readme", "architecture_diagrams", "user_guides", "changelogs"],
        system_prompt="""You are a Technical Writer and Documentation Engineer. Your role is to:
1. Write clear, comprehensive README files with setup, usage, and examples
2. Generate OpenAPI/Swagger documentation for all API endpoints
3. Create architecture diagrams using Mermaid or PlantUML
4. Write developer guides, migration guides, and troubleshooting docs
5. Generate changelogs and release notes from git history
Make documentation scannable, accurate, and always up-to-date.""",
        tools=["filesystem", "git"],
        skills=["documentation", "architecture"],
    ),
    "research": AgentDefinition(
        id="research",
        name="🔬 Research Agent",
        description="Web research, literature review, competitor analysis, technology evaluation, and knowledge synthesis.",
        domain="intelligence",
        capabilities=["web_search", "scraping", "analysis", "synthesis", "competitor_research"],
        system_prompt="""You are a Research Intelligence Agent. Your role is to:
1. Search and synthesize information from authoritative sources
2. Analyze competitors and market landscape
3. Evaluate technology choices with pros/cons and recommendations
4. Review scientific literature and technical papers
5. Create structured research reports with citations
Always verify information from multiple sources. Present balanced, objective analysis.""",
        tools=["browser", "firecrawl", "search"],
        skills=["research", "analysis"],
    ),
    "browser": AgentDefinition(
        id="browser",
        name="🌐 Browser Agent",
        description="Autonomous web browsing, scraping, form filling, UI testing, and workflow automation using Playwright.",
        domain="automation",
        capabilities=["web_browsing", "scraping", "form_filling", "ui_testing", "workflow_automation"],
        system_prompt="""You are an autonomous Browser Automation Agent. Your role is to:
1. Navigate websites and extract structured data
2. Fill forms, click buttons, and interact with web UI
3. Perform visual regression testing with screenshots
4. Automate repetitive web workflows
5. Monitor websites for changes and anomalies
Always handle errors gracefully. Respect robots.txt and rate limits.""",
        tools=["playwright", "browser", "firecrawl"],
        skills=["browser_automation", "testing"],
    ),
    "supervisor": AgentDefinition(
        id="supervisor",
        name="👁️ Supervisor Agent",
        description="Orchestrates multi-agent workflows, monitors progress, handles failures, and ensures goal completion.",
        domain="orchestration",
        capabilities=["multi_agent_orchestration", "progress_monitoring", "failure_handling", "goal_tracking"],
        system_prompt="""You are a Supervisor Agent responsible for multi-agent orchestration. Your role is to:
1. Decompose complex goals and assign subtasks to specialized agents
2. Monitor agent progress and handle failures with retry logic
3. Aggregate results from multiple agents into coherent outputs
4. Escalate blockers and request human-in-the-loop approvals when needed
5. Ensure all tasks are completed to quality standards
Maintain a clear execution plan. Log all decisions and outcomes.""",
        tools=["task_manager"],
        skills=["orchestration", "planning"],
    ),
    "reviewer": AgentDefinition(
        id="reviewer",
        name="👀 Reviewer Agent",
        description="Code review, PR review, architecture review, and quality gate enforcement with actionable feedback.",
        domain="quality",
        capabilities=["code_review", "pr_review", "architecture_review", "quality_gates"],
        system_prompt="""You are a Principal Code Reviewer. Your role is to:
1. Review code for correctness, readability, maintainability, and performance
2. Check for security vulnerabilities and anti-patterns
3. Verify tests exist and have adequate coverage
4. Ensure adherence to coding standards and architecture guidelines
5. Provide constructive, actionable feedback with specific suggestions
Be thorough but fair. Focus on the most impactful issues first.""",
        tools=["filesystem", "git", "github"],
        skills=["coding", "security", "architecture"],
    ),
}

# In-memory run storage (replace with DB in production)
AGENT_RUNS: dict[str, AgentRunResult] = {}


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[AgentDefinition])
async def list_agents():
    """List all registered agents."""
    return list(AGENT_REGISTRY.values())


@router.get("/{agent_id}", response_model=AgentDefinition)
async def get_agent(agent_id: str):
    """Get a specific agent by ID."""
    if agent_id not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    return AGENT_REGISTRY[agent_id]


@router.post("/", response_model=AgentDefinition, status_code=status.HTTP_201_CREATED)
async def create_agent(agent: AgentDefinition):
    """Register a new custom agent."""
    if agent.id in AGENT_REGISTRY:
        raise HTTPException(status_code=409, detail=f"Agent '{agent.id}' already exists")
    AGENT_REGISTRY[agent.id] = agent
    return agent


@router.put("/{agent_id}", response_model=AgentDefinition)
async def update_agent(agent_id: str, agent: AgentDefinition):
    """Update an existing agent."""
    if agent_id not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    agent.id = agent_id
    AGENT_REGISTRY[agent_id] = agent
    return agent


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete a custom agent (built-ins cannot be deleted)."""
    built_ins = {"planner", "coder", "frontend", "backend", "devops", "security", "testing", "docs", "research", "browser", "supervisor", "reviewer"}
    if agent_id in built_ins:
        raise HTTPException(status_code=403, detail="Cannot delete built-in agents")
    if agent_id not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    del AGENT_REGISTRY[agent_id]
    return {"deleted": agent_id}


@router.post("/{agent_id}/run", response_model=AgentRunResult)
async def run_agent(agent_id: str, task: AgentTask):
    """Execute an agent task (synchronous, non-streaming)."""
    if agent_id not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")

    run_id = str(uuid.uuid4())
    agent = AGENT_REGISTRY[agent_id]

    result = AgentRunResult(
        run_id=run_id,
        agent_id=agent_id,
        status="running",
        steps=[{"step": 1, "action": "initialized", "agent": agent.name}],
        created_at=time.time(),
    )
    AGENT_RUNS[run_id] = result

    # Return immediately — real execution happens via streaming or background task
    result.status = "pending"
    result.result = f"Task queued for {agent.name}: {task.task[:100]}..."
    result.completed_at = time.time()
    return result


@router.get("/runs/{run_id}", response_model=AgentRunResult)
async def get_run(run_id: str):
    """Get status of an agent run."""
    if run_id not in AGENT_RUNS:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")
    return AGENT_RUNS[run_id]


@router.get("/runs/", response_model=list[AgentRunResult])
async def list_runs():
    """List all agent runs."""
    return list(AGENT_RUNS.values())


@router.get("/domains/", response_model=list[str])
async def list_domains():
    """List all agent domains."""
    return list(set(a.domain for a in AGENT_REGISTRY.values()))
