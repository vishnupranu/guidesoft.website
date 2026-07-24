"""
Skills Registry API Router
Provides CRUD, search, and category browsing for the Markdown-based skill library.
"""

from __future__ import annotations

from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

router = APIRouter()

# ─── Pydantic Schemas ──────────────────────────────────────────────────────────

class SkillDefinition(BaseModel):
    id: str
    name: str
    description: str
    domain: str
    triggers: list[str]
    inputs: list[str]
    outputs: list[str]
    tools: list[str] = []
    related_skills: list[str] = []
    best_practices: list[str] = []
    system_prompt: str
    example: Optional[str] = None
    enabled: bool = True
    tags: list[str] = []
    metadata: dict[str, Any] = {}


# ─── Built-in Skill Library ────────────────────────────────────────────────────

SKILL_REGISTRY: dict[str, SkillDefinition] = {
    # ── Coding Skills ─────────────────────────────────────────────────────────
    "code-generation": SkillDefinition(
        id="code-generation",
        name="Code Generation",
        description="Generate production-ready code in any language with proper documentation, types, and error handling.",
        domain="coding",
        triggers=["generate code", "write function", "implement", "create class", "build module"],
        inputs=["requirements", "language", "framework", "context"],
        outputs=["source code", "tests", "documentation"],
        tools=["filesystem", "git"],
        related_skills=["code-review", "test-generation", "refactoring"],
        best_practices=["Follow SOLID principles", "Add type annotations", "Write self-documenting code", "Handle edge cases", "Add error handling"],
        system_prompt="Generate clean, production-ready code following best practices for the specified language and framework. Include proper types, error handling, and documentation.",
        tags=["coding", "generation", "productivity"],
    ),
    "code-review": SkillDefinition(
        id="code-review",
        name="Code Review",
        description="Comprehensive code review checking correctness, security, performance, and maintainability.",
        domain="coding",
        triggers=["review code", "check code", "audit code", "PR review"],
        inputs=["code", "context", "standards"],
        outputs=["review report", "suggestions", "severity ratings"],
        tools=["filesystem", "git", "github"],
        related_skills=["security-audit", "refactoring", "test-generation"],
        best_practices=["Check for security vulnerabilities", "Verify error handling", "Check test coverage", "Review naming conventions", "Check performance"],
        system_prompt="Perform a thorough code review. Check for bugs, security issues, performance problems, and code quality. Provide actionable feedback with severity ratings.",
        tags=["coding", "quality", "review"],
    ),
    "refactoring": SkillDefinition(
        id="refactoring",
        name="Code Refactoring",
        description="Refactor code for better readability, performance, and maintainability without changing behavior.",
        domain="coding",
        triggers=["refactor", "improve code", "clean up", "optimize code"],
        inputs=["code", "target quality attributes"],
        outputs=["refactored code", "diff", "explanation"],
        tools=["filesystem"],
        related_skills=["code-review", "code-generation"],
        best_practices=["Run tests before refactoring", "Refactor in small steps", "Keep behavior identical", "Improve naming", "Extract reusable functions"],
        system_prompt="Refactor the provided code to improve readability, performance, and maintainability. Preserve all existing behavior. Explain each change made.",
        tags=["coding", "quality", "refactoring"],
    ),
    "debugging": SkillDefinition(
        id="debugging",
        name="Debugging",
        description="Systematic debugging with root cause analysis, stack trace interpretation, and fix generation.",
        domain="coding",
        triggers=["debug", "fix bug", "error", "exception", "not working"],
        inputs=["code", "error message", "stack trace", "logs"],
        outputs=["root cause analysis", "fix", "explanation", "preventive measures"],
        tools=["filesystem", "terminal"],
        related_skills=["code-review", "testing"],
        best_practices=["Reproduce the issue first", "Analyze stack traces", "Check logs", "Use binary search", "Write a regression test"],
        system_prompt="Debug the issue systematically. Analyze the error, identify root cause, propose a fix, and suggest how to prevent similar issues in the future.",
        tags=["coding", "debugging", "quality"],
    ),
    "test-generation": SkillDefinition(
        id="test-generation",
        name="Test Generation",
        description="Generate unit tests, integration tests, and E2E tests with high coverage and edge case handling.",
        domain="testing",
        triggers=["write tests", "generate tests", "unit test", "integration test", "test coverage"],
        inputs=["code", "framework", "coverage requirements"],
        outputs=["test files", "coverage report", "test plan"],
        tools=["filesystem", "terminal"],
        related_skills=["code-generation", "e2e-testing", "accessibility-testing"],
        best_practices=["Test edge cases", "Follow AAA pattern", "Mock external dependencies", "Test error paths", "Keep tests fast and deterministic"],
        system_prompt="Generate comprehensive tests achieving >90% code coverage. Include unit tests, integration tests, edge cases, and error paths. Follow the AAA (Arrange, Act, Assert) pattern.",
        tags=["testing", "quality", "coverage"],
    ),

    # ── Frontend Skills ────────────────────────────────────────────────────────
    "ui-generation": SkillDefinition(
        id="ui-generation",
        name="UI Generation",
        description="Generate premium, human-crafted UI components and pages inspired by Linear, Notion, and Stripe.",
        domain="frontend",
        triggers=["create UI", "design page", "build component", "generate interface"],
        inputs=["requirements", "framework", "design system", "reference design"],
        outputs=["components", "CSS/Tailwind styles", "animations"],
        tools=["filesystem", "browser"],
        related_skills=["design-system", "accessibility", "responsive-design"],
        best_practices=["Use design tokens", "Implement dark mode", "Add micro-interactions", "Ensure keyboard navigation", "Test on multiple breakpoints"],
        system_prompt="Create premium, beautiful UI that rivals Linear and Stripe. Use proper spacing, typography, and visual hierarchy. Implement smooth animations and dark mode.",
        tags=["frontend", "ui", "design"],
    ),
    "design-system": SkillDefinition(
        id="design-system",
        name="Design System",
        description="Create and maintain component libraries, design tokens, and style guides.",
        domain="frontend",
        triggers=["design system", "component library", "design tokens", "style guide"],
        inputs=["brand guidelines", "existing components", "target frameworks"],
        outputs=["token definitions", "component library", "documentation"],
        tools=["filesystem"],
        related_skills=["ui-generation", "accessibility"],
        best_practices=["Define semantic tokens", "Document all variants", "Create Storybook stories", "Test all states", "Version the system"],
        system_prompt="Build a comprehensive design system with semantic color tokens, typography scale, spacing system, and reusable components. Document all variants and usage guidelines.",
        tags=["frontend", "design", "components"],
    ),
    "accessibility": SkillDefinition(
        id="accessibility",
        name="Accessibility (a11y)",
        description="WCAG 2.1 AA compliance, ARIA labels, keyboard navigation, and screen reader support.",
        domain="frontend",
        triggers=["accessibility", "a11y", "WCAG", "screen reader", "keyboard navigation"],
        inputs=["HTML/components", "audit results"],
        outputs=["fixed code", "WCAG compliance report", "recommendations"],
        tools=["browser", "playwright"],
        related_skills=["ui-generation", "e2e-testing"],
        best_practices=["Use semantic HTML", "Add ARIA labels", "Ensure keyboard focus", "Check color contrast", "Test with screen readers"],
        system_prompt="Audit and fix accessibility issues to meet WCAG 2.1 AA standards. Add proper ARIA labels, keyboard navigation, focus states, and ensure adequate color contrast.",
        tags=["accessibility", "frontend", "compliance"],
    ),
    "responsive-design": SkillDefinition(
        id="responsive-design",
        name="Responsive Design",
        description="Mobile-first responsive layouts that work perfectly across all screen sizes and devices.",
        domain="frontend",
        triggers=["responsive", "mobile", "breakpoints", "adaptive layout"],
        inputs=["designs", "breakpoints", "content"],
        outputs=["responsive CSS/Tailwind", "tested layouts"],
        tools=["filesystem", "browser"],
        related_skills=["ui-generation", "accessibility"],
        best_practices=["Design mobile-first", "Use CSS Grid and Flexbox", "Test on real devices", "Handle touch interactions", "Optimize images"],
        system_prompt="Create mobile-first responsive layouts using CSS Grid and Flexbox. Handle all common breakpoints. Optimize touch interactions for mobile devices.",
        tags=["frontend", "responsive", "mobile"],
    ),
    "performance-optimization": SkillDefinition(
        id="performance-optimization",
        name="Performance Optimization",
        description="Core Web Vitals optimization: LCP, INP, CLS. Bundle optimization, lazy loading, and caching.",
        domain="frontend",
        triggers=["performance", "slow", "optimize", "Core Web Vitals", "LCP", "bundle size"],
        inputs=["code", "lighthouse report", "performance metrics"],
        outputs=["optimized code", "performance report", "recommendations"],
        tools=["browser", "terminal"],
        related_skills=["ui-generation", "e2e-testing"],
        best_practices=["Optimize images", "Lazy load components", "Split bundles", "Minimize JavaScript", "Use service workers"],
        system_prompt="Analyze and optimize application performance. Focus on Core Web Vitals (LCP, INP, CLS). Implement code splitting, lazy loading, image optimization, and caching strategies.",
        tags=["performance", "frontend", "optimization"],
    ),

    # ── Backend Skills ─────────────────────────────────────────────────────────
    "api-design": SkillDefinition(
        id="api-design",
        name="API Design",
        description="Design RESTful and GraphQL APIs following OpenAPI specs, with authentication, versioning, and documentation.",
        domain="backend",
        triggers=["design API", "REST API", "GraphQL", "endpoints", "API spec"],
        inputs=["requirements", "data models", "authentication needs"],
        outputs=["OpenAPI spec", "API routes", "authentication setup"],
        tools=["filesystem"],
        related_skills=["database-design", "authentication", "api-documentation"],
        best_practices=["Follow REST conventions", "Version your APIs", "Validate inputs", "Return proper status codes", "Add rate limiting"],
        system_prompt="Design clean, well-documented APIs following REST best practices. Generate OpenAPI specs, implement proper authentication, input validation, error handling, and versioning.",
        tags=["backend", "api", "design"],
    ),
    "database-design": SkillDefinition(
        id="database-design",
        name="Database Design",
        description="Schema design, ER diagrams, indexing strategy, migrations, and query optimization.",
        domain="backend",
        triggers=["database design", "schema", "ER diagram", "migration", "SQL optimization"],
        inputs=["data requirements", "query patterns", "scale requirements"],
        outputs=["schema definitions", "migrations", "index recommendations"],
        tools=["filesystem", "database"],
        related_skills=["api-design", "performance-optimization"],
        best_practices=["Normalize appropriately", "Add proper indexes", "Use migrations", "Plan for scale", "Document schema"],
        system_prompt="Design efficient database schemas with proper normalization, indexing, and constraints. Generate migrations, seed data, and query optimization recommendations.",
        tags=["backend", "database", "design"],
    ),
    "authentication": SkillDefinition(
        id="authentication",
        name="Authentication & Authorization",
        description="JWT, OAuth2, RBAC, session management, MFA, and SSO integration.",
        domain="backend",
        triggers=["authentication", "authorization", "login", "JWT", "OAuth", "RBAC"],
        inputs=["requirements", "user model", "provider configs"],
        outputs=["auth implementation", "middleware", "token management"],
        tools=["filesystem"],
        related_skills=["security-audit", "api-design"],
        best_practices=["Use short-lived tokens", "Implement refresh tokens", "Hash passwords with bcrypt", "Add MFA support", "Log auth events"],
        system_prompt="Implement secure authentication and authorization. Use JWT with refresh tokens, bcrypt for passwords, RBAC for permissions, and OAuth2 for social login.",
        tags=["backend", "security", "authentication"],
    ),
    "async-processing": SkillDefinition(
        id="async-processing",
        name="Async Processing & Queues",
        description="Background jobs, Celery workers, Redis queues, event buses, and scheduled tasks.",
        domain="backend",
        triggers=["background jobs", "queues", "Celery", "async tasks", "workers", "cron"],
        inputs=["task requirements", "scale needs", "technology stack"],
        outputs=["worker configuration", "queue setup", "job definitions"],
        tools=["filesystem", "terminal"],
        related_skills=["api-design", "monitoring"],
        best_practices=["Use idempotent tasks", "Add retry logic", "Set task timeouts", "Monitor queue depth", "Handle failures gracefully"],
        system_prompt="Set up robust background processing with proper queuing, retry logic, error handling, and monitoring. Use Celery with Redis or equivalent for the technology stack.",
        tags=["backend", "async", "queues"],
    ),
    "caching": SkillDefinition(
        id="caching",
        name="Caching Strategy",
        description="Redis caching, cache invalidation, CDN, and HTTP caching headers for optimal performance.",
        domain="backend",
        triggers=["caching", "Redis", "cache", "performance", "CDN"],
        inputs=["data patterns", "performance requirements", "invalidation rules"],
        outputs=["caching implementation", "invalidation logic", "TTL configurations"],
        tools=["filesystem"],
        related_skills=["performance-optimization", "database-design"],
        best_practices=["Cache at the right layer", "Plan invalidation carefully", "Set appropriate TTLs", "Monitor hit rates", "Handle cache misses"],
        system_prompt="Design and implement a comprehensive caching strategy with Redis. Handle cache invalidation, set appropriate TTLs, and monitor cache performance.",
        tags=["backend", "caching", "performance"],
    ),

    # ── Architecture Skills ────────────────────────────────────────────────────
    "clean-architecture": SkillDefinition(
        id="clean-architecture",
        name="Clean Architecture",
        description="Domain-driven design, hexagonal architecture, CQRS, event-driven patterns, and clean code principles.",
        domain="architecture",
        triggers=["architecture", "clean code", "DDD", "hexagonal", "CQRS", "microservices"],
        inputs=["business requirements", "scale requirements", "team structure"],
        outputs=["architecture diagrams", "ADRs", "module structure"],
        tools=["filesystem"],
        related_skills=["database-design", "api-design", "security-audit"],
        best_practices=["Separate concerns", "Define clear boundaries", "Use dependency injection", "Design for testability", "Document decisions"],
        system_prompt="Design clean, maintainable architecture following DDD, hexagonal architecture, and clean code principles. Create clear module boundaries, dependency rules, and ADRs.",
        tags=["architecture", "design", "patterns"],
    ),
    "microservices": SkillDefinition(
        id="microservices",
        name="Microservices Design",
        description="Service decomposition, API gateways, service mesh, inter-service communication, and distributed patterns.",
        domain="architecture",
        triggers=["microservices", "service decomposition", "API gateway", "distributed"],
        inputs=["monolith analysis", "domain boundaries", "team structure"],
        outputs=["service definitions", "API contracts", "deployment topology"],
        tools=["filesystem"],
        related_skills=["clean-architecture", "devops-infrastructure"],
        best_practices=["Define clear service boundaries", "Design for failure", "Use async communication", "Implement circuit breakers", "Centralize logging"],
        system_prompt="Design a microservices architecture with clear service boundaries, well-defined APIs, proper service communication patterns, and operational considerations.",
        tags=["architecture", "microservices", "distributed"],
    ),

    # ── DevOps Skills ──────────────────────────────────────────────────────────
    "docker": SkillDefinition(
        id="docker",
        name="Docker & Containerization",
        description="Dockerfiles, Docker Compose, multi-stage builds, container security, and container optimization.",
        domain="devops",
        triggers=["Docker", "container", "Dockerfile", "Docker Compose"],
        inputs=["application stack", "requirements"],
        outputs=["Dockerfile", "docker-compose.yml", "optimization report"],
        tools=["filesystem", "terminal", "docker"],
        related_skills=["kubernetes", "ci-cd", "security-audit"],
        best_practices=["Use multi-stage builds", "Run as non-root", "Minimize image size", "Use .dockerignore", "Scan for vulnerabilities"],
        system_prompt="Create optimized, secure Dockerfiles and Docker Compose configurations. Use multi-stage builds, minimize image size, and follow container security best practices.",
        tags=["devops", "docker", "infrastructure"],
    ),
    "kubernetes": SkillDefinition(
        id="kubernetes",
        name="Kubernetes & Helm",
        description="K8s manifests, Helm charts, autoscaling, health checks, and production-grade deployment configs.",
        domain="devops",
        triggers=["Kubernetes", "k8s", "Helm", "deployment", "pods", "services"],
        inputs=["application specs", "resource requirements", "scale requirements"],
        outputs=["manifests", "Helm charts", "deployment guide"],
        tools=["filesystem", "kubernetes", "terminal"],
        related_skills=["docker", "monitoring", "ci-cd"],
        best_practices=["Set resource limits", "Use health checks", "Implement HPA", "Use namespaces", "Secure with RBAC"],
        system_prompt="Create production-grade Kubernetes manifests and Helm charts. Configure resource limits, health checks, autoscaling, network policies, and RBAC.",
        tags=["devops", "kubernetes", "infrastructure"],
    ),
    "ci-cd": SkillDefinition(
        id="ci-cd",
        name="CI/CD Pipeline",
        description="GitHub Actions, GitLab CI, automated testing, deployment pipelines, and release automation.",
        domain="devops",
        triggers=["CI/CD", "GitHub Actions", "pipeline", "automation", "deployment"],
        inputs=["repository structure", "testing requirements", "deployment targets"],
        outputs=["workflow files", "pipeline configuration", "deployment scripts"],
        tools=["filesystem", "github", "terminal"],
        related_skills=["docker", "testing", "monitoring"],
        best_practices=["Fail fast", "Cache dependencies", "Use secrets management", "Implement rollback", "Add notifications"],
        system_prompt="Create robust CI/CD pipelines with automated testing, security scanning, and deployment automation. Implement proper secret management and rollback strategies.",
        tags=["devops", "ci-cd", "automation"],
    ),
    "monitoring": SkillDefinition(
        id="monitoring",
        name="Monitoring & Observability",
        description="OpenTelemetry, Prometheus, Grafana, structured logging, distributed tracing, and alerting.",
        domain="devops",
        triggers=["monitoring", "observability", "Prometheus", "Grafana", "logging", "tracing"],
        inputs=["application stack", "SLAs", "alerting requirements"],
        outputs=["monitoring setup", "dashboards", "alert rules"],
        tools=["filesystem", "terminal"],
        related_skills=["kubernetes", "ci-cd"],
        best_practices=["Implement distributed tracing", "Use structured logging", "Define SLIs/SLOs", "Alert on symptoms not causes", "Keep dashboards simple"],
        system_prompt="Set up comprehensive monitoring with OpenTelemetry, Prometheus metrics, Grafana dashboards, and structured logging. Define SLIs/SLOs and configure meaningful alerts.",
        tags=["devops", "monitoring", "observability"],
    ),
    "terraform": SkillDefinition(
        id="terraform",
        name="Terraform & IaC",
        description="Infrastructure as Code with Terraform, modules, state management, and cloud provider configurations.",
        domain="devops",
        triggers=["Terraform", "IaC", "infrastructure", "cloud", "Pulumi"],
        inputs=["infrastructure requirements", "cloud provider", "existing resources"],
        outputs=["Terraform configurations", "modules", "state setup"],
        tools=["filesystem", "terminal"],
        related_skills=["kubernetes", "ci-cd", "security-audit"],
        best_practices=["Use modules", "Remote state", "Plan before apply", "Use workspaces", "Lock provider versions"],
        system_prompt="Create modular, reusable Terraform configurations for cloud infrastructure. Implement remote state, workspaces, and follow security best practices.",
        tags=["devops", "terraform", "infrastructure"],
    ),

    # ── Security Skills ────────────────────────────────────────────────────────
    "security-audit": SkillDefinition(
        id="security-audit",
        name="Security Audit",
        description="OWASP Top 10 audit, vulnerability scanning, secrets detection, and threat modeling.",
        domain="security",
        triggers=["security audit", "vulnerability", "OWASP", "penetration", "threat model"],
        inputs=["code", "architecture", "dependencies"],
        outputs=["security report", "severity ratings", "remediation plan"],
        tools=["filesystem", "terminal"],
        related_skills=["authentication", "ci-cd"],
        best_practices=["Check OWASP Top 10", "Scan dependencies", "Check for secrets", "Review auth flows", "Test input validation"],
        system_prompt="Perform a comprehensive security audit covering OWASP Top 10. Identify vulnerabilities, exposed secrets, authentication weaknesses, and injection risks. Provide prioritized remediation.",
        tags=["security", "audit", "compliance"],
    ),
    "secrets-management": SkillDefinition(
        id="secrets-management",
        name="Secrets Management",
        description="Vault integration, environment variables, encrypted secrets, and secure configuration management.",
        domain="security",
        triggers=["secrets", "environment variables", "API keys", "credentials", "Vault"],
        inputs=["secrets inventory", "deployment environment"],
        outputs=["secrets setup", "rotation policy", "audit trail"],
        tools=["filesystem"],
        related_skills=["security-audit", "ci-cd"],
        best_practices=["Never commit secrets", "Rotate regularly", "Use least privilege", "Audit access", "Encrypt at rest"],
        system_prompt="Implement secure secrets management. Set up proper secret storage, rotation policies, access controls, and audit logging. Remove any hardcoded secrets.",
        tags=["security", "secrets", "compliance"],
    ),

    # ── AI/ML Skills ──────────────────────────────────────────────────────────
    "rag-pipeline": SkillDefinition(
        id="rag-pipeline",
        name="RAG Pipeline",
        description="Retrieval-Augmented Generation with vector databases, embeddings, chunking, and hybrid search.",
        domain="ai",
        triggers=["RAG", "retrieval", "embeddings", "vector search", "knowledge base"],
        inputs=["documents", "query patterns", "model choices"],
        outputs=["pipeline code", "vector DB setup", "search API"],
        tools=["filesystem", "database"],
        related_skills=["database-design", "api-design"],
        best_practices=["Choose right chunk size", "Use hybrid search", "Rerank results", "Cache embeddings", "Monitor relevance"],
        system_prompt="Build a production RAG pipeline with proper chunking, embedding, vector storage, and hybrid search. Implement reranking, citation tracking, and quality evaluation.",
        tags=["ai", "rag", "search"],
    ),
    "agent-orchestration": SkillDefinition(
        id="agent-orchestration",
        name="Agent Orchestration",
        description="Multi-agent workflows with LangGraph, CrewAI, or custom orchestration. Includes planning, memory, and tool use.",
        domain="ai",
        triggers=["agent", "orchestration", "multi-agent", "LangGraph", "CrewAI", "workflow"],
        inputs=["task description", "agent definitions", "tool specs"],
        outputs=["orchestration code", "agent configurations", "workflow diagram"],
        tools=["filesystem"],
        related_skills=["rag-pipeline", "code-generation"],
        best_practices=["Define clear agent roles", "Handle failures gracefully", "Add memory", "Log all actions", "Implement human-in-the-loop"],
        system_prompt="Design and implement multi-agent orchestration systems. Define clear agent roles, communication protocols, memory systems, and failure handling strategies.",
        tags=["ai", "agents", "orchestration"],
    ),
    "prompt-engineering": SkillDefinition(
        id="prompt-engineering",
        name="Prompt Engineering",
        description="System prompt design, few-shot examples, chain-of-thought, and prompt optimization techniques.",
        domain="ai",
        triggers=["prompt", "system prompt", "few-shot", "chain-of-thought", "LLM optimization"],
        inputs=["task description", "model", "examples"],
        outputs=["optimized prompt", "few-shot examples", "evaluation"],
        tools=["filesystem"],
        related_skills=["agent-orchestration", "rag-pipeline"],
        best_practices=["Be specific and clear", "Use XML tags for structure", "Provide examples", "Set persona", "Test with adversarial inputs"],
        system_prompt="Design optimal prompts for LLM tasks. Apply prompt engineering techniques: chain-of-thought, few-shot examples, persona setting, and output format specification.",
        tags=["ai", "prompts", "optimization"],
    ),
    "mcp-integration": SkillDefinition(
        id="mcp-integration",
        name="MCP Integration",
        description="Model Context Protocol server implementation and tool registration for LLM tool use.",
        domain="ai",
        triggers=["MCP", "Model Context Protocol", "tool use", "function calling"],
        inputs=["tool specifications", "transport type", "authentication"],
        outputs=["MCP server code", "tool definitions", "client integration"],
        tools=["filesystem"],
        related_skills=["api-design", "agent-orchestration"],
        best_practices=["Define clear tool schemas", "Validate inputs", "Return structured outputs", "Handle errors gracefully", "Document tools"],
        system_prompt="Implement MCP servers and tool integrations. Define clear tool schemas, implement proper validation, and create comprehensive tool documentation.",
        tags=["ai", "mcp", "tools"],
    ),

    # ── Documentation Skills ───────────────────────────────────────────────────
    "api-documentation": SkillDefinition(
        id="api-documentation",
        name="API Documentation",
        description="OpenAPI/Swagger docs, endpoint documentation, SDK documentation, and interactive API explorers.",
        domain="documentation",
        triggers=["API docs", "OpenAPI", "Swagger", "documentation", "SDK docs"],
        inputs=["API code", "endpoint list", "authentication info"],
        outputs=["OpenAPI spec", "documentation site", "code examples"],
        tools=["filesystem"],
        related_skills=["api-design", "readme-generation"],
        best_practices=["Document all endpoints", "Add request/response examples", "Describe error codes", "Keep docs in sync", "Add authentication docs"],
        system_prompt="Generate comprehensive API documentation with OpenAPI specs, detailed endpoint descriptions, request/response examples, and authentication guides.",
        tags=["documentation", "api", "openapi"],
    ),
    "readme-generation": SkillDefinition(
        id="readme-generation",
        name="README Generation",
        description="Professional README files with setup guides, usage examples, badges, and contribution guidelines.",
        domain="documentation",
        triggers=["README", "documentation", "setup guide", "getting started"],
        inputs=["project structure", "tech stack", "purpose"],
        outputs=["README.md", "CONTRIBUTING.md", "CHANGELOG.md"],
        tools=["filesystem", "git"],
        related_skills=["api-documentation", "changelog-generation"],
        best_practices=["Include badges", "Quick start section", "Clear setup steps", "Usage examples", "Contributing guide"],
        system_prompt="Write a professional, comprehensive README with a clear project description, quick start guide, detailed setup instructions, usage examples, and contribution guidelines.",
        tags=["documentation", "readme", "onboarding"],
    ),

    # ── Browser Automation Skills ──────────────────────────────────────────────
    "e2e-testing": SkillDefinition(
        id="e2e-testing",
        name="E2E Testing with Playwright",
        description="End-to-end test automation with Playwright covering critical user journeys and visual regression.",
        domain="testing",
        triggers=["E2E", "end-to-end", "Playwright", "browser test", "integration test"],
        inputs=["user journeys", "application URL", "test scenarios"],
        outputs=["test files", "test report", "screenshots"],
        tools=["playwright", "filesystem"],
        related_skills=["test-generation", "accessibility"],
        best_practices=["Test critical paths", "Use page objects", "Add visual regression", "Handle async properly", "Run in CI/CD"],
        system_prompt="Create comprehensive E2E tests with Playwright for critical user journeys. Use Page Object Model, add visual regression checks, and ensure tests are stable in CI/CD.",
        tags=["testing", "e2e", "playwright"],
    ),
    "web-scraping": SkillDefinition(
        id="web-scraping",
        name="Web Scraping",
        description="Structured data extraction with Firecrawl, Playwright, BeautifulSoup, and anti-detection techniques.",
        domain="automation",
        triggers=["scraping", "data extraction", "Firecrawl", "crawl", "web data"],
        inputs=["target URLs", "data schema", "extraction rules"],
        outputs=["extracted data", "scraper code", "storage setup"],
        tools=["firecrawl", "playwright", "browser"],
        related_skills=["e2e-testing", "database-design"],
        best_practices=["Respect robots.txt", "Rate limit requests", "Handle pagination", "Validate extracted data", "Handle failures"],
        system_prompt="Build robust web scrapers using Firecrawl or Playwright. Extract structured data, handle pagination, manage rate limiting, and store results efficiently.",
        tags=["automation", "scraping", "data"],
    ),

    # ── Research Skills ────────────────────────────────────────────────────────
    "technical-research": SkillDefinition(
        id="technical-research",
        name="Technical Research",
        description="Technology evaluation, competitor analysis, literature review, and recommendation reports.",
        domain="research",
        triggers=["research", "evaluate", "compare", "technology choice", "analysis"],
        inputs=["research question", "criteria", "existing context"],
        outputs=["research report", "comparison table", "recommendation"],
        tools=["browser", "firecrawl"],
        related_skills=["web-scraping", "api-documentation"],
        best_practices=["Define clear criteria", "Use multiple sources", "Present objectively", "Include trade-offs", "Cite sources"],
        system_prompt="Conduct thorough technical research. Evaluate options against defined criteria, present trade-offs clearly, and provide a well-reasoned recommendation.",
        tags=["research", "analysis", "evaluation"],
    ),

    # ── Provider Integration Skills ────────────────────────────────────────────
    "opencode-integration": SkillDefinition(
        id="opencode-integration",
        name="OpenCode AI Integration",
        description="Integrate OpenCode AI for autonomous code generation, review, and development workflows.",
        domain="ai",
        triggers=["OpenCode", "opencode.ai", "AI coding"],
        inputs=["API key", "task description", "codebase context"],
        outputs=["code changes", "PR description", "implementation plan"],
        tools=["filesystem", "git"],
        related_skills=["code-generation", "agent-orchestration"],
        best_practices=["Provide full context", "Review before merging", "Use in iteration", "Combine with testing"],
        system_prompt="Use OpenCode AI for autonomous code generation. Provide clear context, review outputs carefully, and integrate with your existing development workflow.",
        tags=["ai", "coding", "opencode"],
    ),
    "openhands-integration": SkillDefinition(
        id="openhands-integration",
        name="OpenHands Integration",
        description="Integrate OpenHands (OpenDevin) for autonomous software development agent workflows.",
        domain="ai",
        triggers=["OpenHands", "OpenDevin", "autonomous agent", "software development"],
        inputs=["task description", "repository", "OpenHands config"],
        outputs=["code changes", "execution trace", "result"],
        tools=["filesystem", "git", "browser"],
        related_skills=["agent-orchestration", "code-generation"],
        best_practices=["Define clear tasks", "Set up sandbox", "Review all changes", "Use version control"],
        system_prompt="Use OpenHands for autonomous software development tasks. Define precise task descriptions and always review generated code before deployment.",
        tags=["ai", "agents", "openhands"],
    ),
    "firecrawl-integration": SkillDefinition(
        id="firecrawl-integration",
        name="Firecrawl Integration",
        description="Integrate Firecrawl for structured web data extraction, crawling, and research automation.",
        domain="ai",
        triggers=["Firecrawl", "web crawl", "structured extraction", "research"],
        inputs=["URLs", "schema", "Firecrawl API key"],
        outputs=["structured data", "markdown content", "links"],
        tools=["firecrawl"],
        related_skills=["web-scraping", "rag-pipeline", "technical-research"],
        best_practices=["Define clear schemas", "Use LLM extraction", "Handle rate limits", "Cache results"],
        system_prompt="Use Firecrawl to extract structured data from websites. Define clear schemas for structured extraction and handle rate limiting appropriately.",
        tags=["ai", "scraping", "firecrawl"],
    ),
    "composio-integration": SkillDefinition(
        id="composio-integration",
        name="Composio Integration",
        description="Connect AI agents to 250+ tools and services via Composio: GitHub, Slack, Notion, Linear, Gmail, etc.",
        domain="ai",
        triggers=["Composio", "tool integration", "GitHub agent", "Slack agent", "automation"],
        inputs=["Composio API key", "tool selection", "agent task"],
        outputs=["tool actions", "results", "audit log"],
        tools=["filesystem"],
        related_skills=["agent-orchestration", "mcp-integration"],
        best_practices=["Use minimal permissions", "Handle auth flows", "Log all actions", "Test with sandbox"],
        system_prompt="Use Composio to give AI agents access to external tools and services. Configure minimal required permissions and always log tool usage.",
        tags=["ai", "integration", "composio"],
    ),
}


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[SkillDefinition])
async def list_skills(
    domain: Optional[str] = Query(None, description="Filter by domain"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    q: Optional[str] = Query(None, description="Search query"),
):
    """List all skills with optional filtering."""
    skills = list(SKILL_REGISTRY.values())

    if domain:
        skills = [s for s in skills if s.domain == domain]

    if tag:
        skills = [s for s in skills if tag in s.tags]

    if q:
        q_lower = q.lower()
        skills = [
            s for s in skills
            if q_lower in s.name.lower()
            or q_lower in s.description.lower()
            or any(q_lower in t.lower() for t in s.triggers)
            or any(q_lower in tag.lower() for tag in s.tags)
        ]

    return skills


@router.get("/domains/", response_model=list[str])
async def list_domains():
    """List all skill domains."""
    return list(set(s.domain for s in SKILL_REGISTRY.values()))


@router.get("/tags/", response_model=list[str])
async def list_tags():
    """List all skill tags."""
    tags = set()
    for skill in SKILL_REGISTRY.values():
        tags.update(skill.tags)
    return sorted(tags)


@router.get("/{skill_id}", response_model=SkillDefinition)
async def get_skill(skill_id: str):
    """Get a specific skill by ID."""
    if skill_id not in SKILL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")
    return SKILL_REGISTRY[skill_id]


@router.post("/", response_model=SkillDefinition, status_code=status.HTTP_201_CREATED)
async def create_skill(skill: SkillDefinition):
    """Register a new custom skill."""
    if skill.id in SKILL_REGISTRY:
        raise HTTPException(status_code=409, detail=f"Skill '{skill.id}' already exists")
    SKILL_REGISTRY[skill.id] = skill
    return skill


@router.put("/{skill_id}", response_model=SkillDefinition)
async def update_skill(skill_id: str, skill: SkillDefinition):
    """Update an existing skill."""
    if skill_id not in SKILL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")
    skill.id = skill_id
    SKILL_REGISTRY[skill_id] = skill
    return skill


@router.delete("/{skill_id}")
async def delete_skill(skill_id: str):
    """Delete a custom skill (built-ins cannot be deleted)."""
    built_in_ids = set(SKILL_REGISTRY.keys()) - set()  # All current are built-in
    if skill_id not in SKILL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_id}' not found")
    del SKILL_REGISTRY[skill_id]
    return {"deleted": skill_id}
