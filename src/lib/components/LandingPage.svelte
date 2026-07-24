<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';

	// ── State ──────────────────────────────────────────────────────
	let prompt = '';
	let selectedModel = 'claude-sonnet-4-5';
	let showModelDropdown = false;
	let inputFocused = false;
	let mouseX = 0;
	let mouseY = 0;
	let heroRef: HTMLElement;
	let textareaRef: HTMLTextAreaElement;

	// Models
	const models = [
		{ id: 'gpt-4o', name: 'GPT-4o', provider: 'OpenAI', color: '#10a37f' },
		{ id: 'claude-sonnet-4-5', name: 'Claude Sonnet 4.5', provider: 'Anthropic', color: '#d97706' },
		{ id: 'gemini-2.0-flash', name: 'Gemini 2.0 Flash', provider: 'Google', color: '#4285f4' },
		{ id: 'deepseek-chat', name: 'DeepSeek V3', provider: 'DeepSeek', color: '#7c3aed' },
		{ id: 'llama-3.3-70b', name: 'Llama 3.3 70B', provider: 'Groq', color: '#0284c7' },
		{ id: 'grok-3', name: 'Grok 3', provider: 'xAI', color: '#1a1a2e' }
	];

	// Prompt starters
	const starters = [
		{ label: 'Build a full-stack SaaS', icon: '⚡' },
		{ label: 'Debug my codebase', icon: '🐛' },
		{ label: 'Research & write a report', icon: '🔬' },
		{ label: 'Create a marketing strategy', icon: '📈' }
	];

	// Capabilities bento
	const capabilities = [
		{
			title: '12 Specialized Agents',
			desc: 'Planner, Coder, DevOps, Security, Research, Browser, and more — each with a deep system prompt and tool access.',
			tag: 'Agents',
			size: 'large'
		},
		{
			title: '18 AI Providers',
			desc: 'OpenAI, Anthropic, Gemini, Groq, DeepSeek, Ollama, OpenCode, OpenHands, Firecrawl, Composio and more.',
			tag: 'Models',
			size: 'small'
		},
		{
			title: '35+ Skills',
			desc: 'Code generation, RAG pipelines, agent orchestration, MCP integration, web scraping, CI/CD, and more.',
			tag: 'Skills',
			size: 'small'
		},
		{
			title: 'Autonomous Browser Agent',
			desc: 'Playwright-powered browser automation that navigates, fills forms, extracts data, and tests UI automatically.',
			tag: 'Automation',
			size: 'medium'
		},
		{
			title: 'RAG & Knowledge Base',
			desc: 'Upload PDFs, codebases, and docs. Get AI answers backed by your own knowledge with precise citations.',
			tag: 'Enterprise RAG',
			size: 'medium'
		},
		{
			title: 'Built-in Code Interpreter',
			desc: 'Execute Python safely in a WASM sandbox. Plot charts, analyze data, and export results.',
			tag: 'WASM',
			size: 'small'
		}
	];

	// Integrations
	const integrations = [
		{ name: 'OpenAI', logo: '⬛', color: '#000' },
		{ name: 'Anthropic', logo: '🟠', color: '#d97706' },
		{ name: 'Google', logo: '🔵', color: '#4285f4' },
		{ name: 'Groq', logo: '⚡', color: '#f59e0b' },
		{ name: 'Ollama', logo: '🦙', color: '#6366f1' },
		{ name: 'Firecrawl', logo: '🔥', color: '#ef4444' },
		{ name: 'Composio', logo: '🔧', color: '#06b6d4' },
		{ name: 'OpenHands', logo: '🙌', color: '#8b5cf6' },
		{ name: 'GitHub', logo: '⬤', color: '#24292e' },
		{ name: 'Slack', logo: '💬', color: '#4a154b' },
		{ name: 'Notion', logo: '📄', color: '#37352f' },
		{ name: 'Linear', logo: '⧫', color: '#5e6ad2' }
	];

	// Use cases
	const useCases = [
		{
			title: 'For Developers',
			desc: 'Generate, refactor, debug, and deploy code across 30+ languages. Autonomous coding agents that write, test, and commit.',
			cta: 'Start Coding',
			icon: '💻'
		},
		{
			title: 'For Research Teams',
			desc: 'Web research, literature review, competitor analysis, and structured report generation powered by Firecrawl.',
			cta: 'Start Research',
			icon: '🔬'
		},
		{
			title: 'For Enterprises',
			desc: 'Role-based access, private deployments, audit logs, SSO, SCIM, and multi-tenant workspace support.',
			cta: 'Contact Sales',
			icon: '🏢'
		}
	];

	// ── Handlers ──────────────────────────────────────────────────────
	function handleMouseMove(e: MouseEvent) {
		mouseX = e.clientX;
		mouseY = e.clientY;
	}

	function autoResize() {
		if (textareaRef) {
			textareaRef.style.height = 'auto';
			textareaRef.style.height = Math.min(textareaRef.scrollHeight, 200) + 'px';
		}
	}

	async function handleSubmit() {
		if (!prompt.trim()) return;
		const encoded = encodeURIComponent(prompt.trim());
		await goto(`/auth?prompt=${encoded}`);
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			handleSubmit();
		}
	}

	function handleStarterClick(label: string) {
		prompt = label;
		handleSubmit();
	}

	function getModelColor() {
		return models.find((m) => m.id === selectedModel)?.color ?? '#111';
	}

	function getModelName() {
		return models.find((m) => m.id === selectedModel)?.name ?? selectedModel;
	}

	onMount(() => {
		window.addEventListener('mousemove', handleMouseMove);
		return () => window.removeEventListener('mousemove', handleMouseMove);
	});
</script>

<!-- Main Container -->
<div class="landing" on:mousemove={handleMouseMove} role="main">

	<!-- Subtle grid background -->
	<div class="grid-bg" aria-hidden="true"></div>

	<!-- ── HEADER ──────────────────────────────────────────────────── -->
	<header class="header">
		<div class="header-inner">
			<a href="/" class="logo">
				<div class="logo-mark">
					<svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path d="M14 2L26 22H2L14 2Z" fill="currentColor" />
					</svg>
				</div>
				<span class="logo-text">GUIDESOFT</span>
				<span class="logo-dot">.WEB</span>
			</a>

			<nav class="nav" aria-label="Main navigation">
				<a href="#capabilities" class="nav-link">Capabilities</a>
				<a href="#integrations" class="nav-link">Integrations</a>
				<a href="#usecases" class="nav-link">Use Cases</a>
				<a href="https://vision-thinking-excess-holding.trycloudflare.com/api/v1/agents/" target="_blank" rel="noopener" class="nav-link">API</a>
			</nav>

			<div class="header-actions">
				<a href="/auth" class="btn-ghost">Sign In</a>
				<a href="/auth?signup=true" class="btn-primary">Get Started</a>
			</div>
		</div>
	</header>

	<!-- ── HERO ──────────────────────────────────────────────────────── -->
	<section class="hero" bind:this={heroRef} aria-label="Hero section">

		<!-- Eyebrow -->
		<div class="eyebrow">
			<span class="eyebrow-dot"></span>
			<span>Enterprise AI Agent Operating System</span>
		</div>

		<!-- Main Headline — Antigravity/Codex style massive typography -->
		<h1 class="hero-headline">
			Experience liftoff<br />with the next-gen<br />
			<span class="headline-accent">agent platform</span>
		</h1>

		<p class="hero-sub">
			Orchestrate 12 specialized AI agents across 18 model providers.<br />
			One workspace for code, research, automation, and enterprise AI.
		</p>

		<!-- Prompt Input Box -->
		<div class="prompt-container" class:focused={inputFocused} id="hero-input-container">

			<!-- Model Selector -->
			<div class="model-selector-wrap">
				<button
					class="model-selector"
					style="--model-color: {getModelColor()}"
					on:click={() => (showModelDropdown = !showModelDropdown)}
					aria-label="Select AI model"
					aria-expanded={showModelDropdown}
				>
					<span class="model-dot" style="background:{getModelColor()}"></span>
					<span class="model-name">{getModelName()}</span>
					<svg class="model-caret" class:open={showModelDropdown} width="12" height="12" viewBox="0 0 12 12" fill="none">
						<path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
					</svg>
				</button>

				{#if showModelDropdown}
					<div class="model-dropdown" role="listbox" aria-label="AI models">
						{#each models as model}
							<button
								class="model-option"
								class:active={selectedModel === model.id}
								role="option"
								aria-selected={selectedModel === model.id}
								on:click={() => { selectedModel = model.id; showModelDropdown = false; }}
							>
								<span class="option-dot" style="background:{model.color}"></span>
								<span class="option-info">
									<span class="option-name">{model.name}</span>
									<span class="option-provider">{model.provider}</span>
								</span>
								{#if selectedModel === model.id}
									<svg class="option-check" width="14" height="14" viewBox="0 0 14 14" fill="none">
										<path d="M2 7l3.5 3.5L12 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									</svg>
								{/if}
							</button>
						{/each}
					</div>
				{/if}
			</div>

			<div class="input-area">
				<textarea
					bind:this={textareaRef}
					bind:value={prompt}
					on:focus={() => (inputFocused = true)}
					on:blur={() => (inputFocused = false)}
					on:input={autoResize}
					on:keydown={handleKeydown}
					placeholder="Ask anything, build anything, research anything..."
					rows="1"
					id="hero-prompt-input"
					aria-label="Enter your prompt"
				></textarea>
			</div>

			<button
				class="send-btn"
				class:active={prompt.trim().length > 0}
				on:click={handleSubmit}
				aria-label="Send prompt"
			>
				<svg width="18" height="18" viewBox="0 0 18 18" fill="none">
					<path d="M9 15V3M9 3L4 8M9 3l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
				</svg>
			</button>
		</div>

		<!-- Starter Chips -->
		<div class="starters" aria-label="Prompt suggestions">
			{#each starters as starter}
				<button class="starter-chip" on:click={() => handleStarterClick(starter.label)}>
					<span>{starter.icon}</span>
					<span>{starter.label}</span>
				</button>
			{/each}
		</div>

		<!-- CTA Buttons — Antigravity style (dark pill + ghost) -->
		<div class="hero-ctas">
			<a href="/auth?signup=true" class="cta-primary">
				<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="2" width="12" height="12" rx="2" fill="currentColor" opacity="0.2"/><path d="M8 4v8M4 8h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
				Get started free
			</a>
			<a href="#capabilities" class="cta-ghost">Explore capabilities</a>
		</div>

		<!-- Stats Row -->
		<div class="stats-row" aria-label="Platform statistics">
			<div class="stat">
				<span class="stat-num">18</span>
				<span class="stat-label">AI Providers</span>
			</div>
			<div class="stat-divider" aria-hidden="true"></div>
			<div class="stat">
				<span class="stat-num">12</span>
				<span class="stat-label">Specialized Agents</span>
			</div>
			<div class="stat-divider" aria-hidden="true"></div>
			<div class="stat">
				<span class="stat-num">35+</span>
				<span class="stat-label">Skill Definitions</span>
			</div>
			<div class="stat-divider" aria-hidden="true"></div>
			<div class="stat">
				<span class="stat-num">32</span>
				<span class="stat-label">Firecrawl Skills</span>
			</div>
		</div>
	</section>

	<!-- ── CAPABILITIES BENTO ──────────────────────────────────────── -->
	<section class="section" id="capabilities" aria-labelledby="cap-heading">
		<div class="section-inner">
			<div class="section-header">
				<p class="section-label">Capabilities</p>
				<h2 class="section-headline" id="cap-heading">
					Everything you need<br />to build with AI
				</h2>
			</div>

			<div class="bento-grid">
				{#each capabilities as item}
					<div class="bento-card bento-{item.size}">
						<span class="bento-tag">{item.tag}</span>
						<h3 class="bento-title">{item.title}</h3>
						<p class="bento-desc">{item.desc}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ── AGENTS SHOWCASE ────────────────────────────────────────── -->
	<section class="section section-dark" aria-labelledby="agents-heading">
		<div class="section-inner">
			<div class="section-header section-header-light">
				<p class="section-label-light">Agent Fleet</p>
				<h2 class="section-headline-light" id="agents-heading">
					Specialized agents for<br />every task
				</h2>
				<p class="section-sub-light">12 expert agents, each with deep system prompts, curated tool access, and domain-specific skills.</p>
			</div>

			<div class="agents-grid">
				{#each [
					{ id: 'planner', name: 'Planner', emoji: '🗓️', desc: 'Decomposes goals into sprint plans, task trees & ADRs', domain: 'Orchestration' },
					{ id: 'coder', name: 'Coder', emoji: '💻', desc: 'Production-grade code in 30+ languages with full test coverage', domain: 'Engineering' },
					{ id: 'frontend', name: 'Frontend', emoji: '🎨', desc: 'Premium UI rivaling Linear, Stripe & Notion with WCAG compliance', domain: 'Engineering' },
					{ id: 'backend', name: 'Backend', emoji: '⚙️', desc: 'FastAPI, GraphQL, database schemas, auth & async queues', domain: 'Engineering' },
					{ id: 'devops', name: 'DevOps', emoji: '🚀', desc: 'Docker, Kubernetes, Terraform IaC, GitHub Actions CI/CD', domain: 'Infrastructure' },
					{ id: 'security', name: 'Security', emoji: '🔒', desc: 'OWASP Top 10 audits, CVE scanning, threat modeling', domain: 'Security' },
					{ id: 'testing', name: 'Testing', emoji: '🧪', desc: 'Unit, integration & Playwright E2E with >90% coverage', domain: 'Quality' },
					{ id: 'research', name: 'Research', emoji: '🔬', desc: 'Deep web research, Firecrawl scraping, synthesis & citations', domain: 'Intelligence' },
					{ id: 'browser', name: 'Browser', emoji: '🌐', desc: 'Autonomous Playwright navigation, form filling & extraction', domain: 'Automation' },
					{ id: 'docs', name: 'Docs', emoji: '📚', desc: 'OpenAPI specs, README generation, Mermaid diagrams', domain: 'Documentation' },
					{ id: 'supervisor', name: 'Supervisor', emoji: '👁️', desc: 'Multi-agent orchestration with retry logic & progress tracking', domain: 'Orchestration' },
					{ id: 'reviewer', name: 'Reviewer', emoji: '👀', desc: 'Code quality gates, PR reviews & architectural feedback', domain: 'Quality' }
				] as agent}
					<div class="agent-card">
						<div class="agent-emoji">{agent.emoji}</div>
						<div class="agent-info">
							<span class="agent-domain">{agent.domain}</span>
							<h3 class="agent-name">{agent.name} Agent</h3>
							<p class="agent-desc">{agent.desc}</p>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ── INTEGRATIONS ────────────────────────────────────────────── -->
	<section class="section" id="integrations" aria-labelledby="int-heading">
		<div class="section-inner">
			<div class="section-header">
				<p class="section-label">Integrations</p>
				<h2 class="section-headline" id="int-heading">
					Connect everything<br />you already use
				</h2>
				<p class="section-sub">18 AI model providers, 250+ business tool integrations via Composio, plus Firecrawl and OpenHands.</p>
			</div>

			<div class="integrations-grid">
				{#each integrations as int}
					<div class="integration-card">
						<span class="int-icon">{int.logo}</span>
						<span class="int-name">{int.name}</span>
					</div>
				{/each}
			</div>

			<div class="integration-note">
				<span>+ OpenCode AI, OpenHands, Mistral, Together AI, Perplexity, Cohere, xAI Grok, Azure OpenAI and more</span>
			</div>
		</div>
	</section>

	<!-- ── USE CASES ──────────────────────────────────────────────── -->
	<section class="section" id="usecases" aria-labelledby="uc-heading">
		<div class="section-inner">
			<div class="section-header">
				<p class="section-label">Use Cases</p>
				<h2 class="section-headline" id="uc-heading">Built for every team</h2>
			</div>

			<div class="use-cases-grid">
				{#each useCases as uc}
					<div class="uc-card">
						<span class="uc-icon">{uc.icon}</span>
						<h3 class="uc-title">{uc.title}</h3>
						<p class="uc-desc">{uc.desc}</p>
						<button class="uc-cta" on:click={() => goto('/auth?signup=true')}>
							{uc.cta}
							<svg width="14" height="14" viewBox="0 0 14 14" fill="none">
								<path d="M3 7h8M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</button>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ── FINAL CTA ──────────────────────────────────────────────── -->
	<section class="section section-cta" aria-labelledby="cta-heading">
		<div class="section-inner cta-inner">
			<h2 class="cta-headline" id="cta-heading">
				Ready for liftoff?
			</h2>
			<p class="cta-sub">
				Join developers and teams using GUIDESOFT.WEB to<br />
				orchestrate AI agents, build products, and automate workflows.
			</p>
			<div class="cta-actions">
				<a href="/auth?signup=true" class="cta-primary large">Start for free</a>
				<a href="/auth" class="cta-ghost large">Sign in</a>
			</div>
		</div>
	</section>

	<!-- ── FOOTER ─────────────────────────────────────────────────── -->
	<footer class="footer" role="contentinfo">
		<div class="footer-inner">
			<div class="footer-logo">
				<div class="logo-mark small">
					<svg width="18" height="18" viewBox="0 0 28 28" fill="none">
						<path d="M14 2L26 22H2L14 2Z" fill="currentColor" />
					</svg>
				</div>
				<span>GUIDESOFT.WEB</span>
			</div>
			<div class="footer-links">
				<a href="https://vision-thinking-excess-holding.trycloudflare.com/docs" target="_blank" rel="noopener">API Docs</a>
				<a href="https://github.com/happies2013-design/open-webui" target="_blank" rel="noopener">GitHub</a>
				<a href="/auth" class="footer-link">Sign In</a>
			</div>
			<p class="footer-copy">© 2026 GUIDESOFT.WEB · Enterprise AI Agent OS</p>
		</div>
	</footer>
</div>

<!-- Click outside to close dropdown -->
{#if showModelDropdown}
	<div class="overlay" on:click={() => (showModelDropdown = false)} role="button" tabindex="-1" aria-label="Close model dropdown" on:keydown={() => {}}></div>
{/if}

<style>
	/* ── RESET & BASE ────────────────────────────────────────────────── */
	:global(body) {
		margin: 0;
		padding: 0;
		background: #fff;
		color: #0a0a0a;
		font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', system-ui, sans-serif;
		-webkit-font-smoothing: antialiased;
	}

	.landing {
		min-height: 100vh;
		background: #ffffff;
		position: relative;
		overflow-x: hidden;
	}

	/* Subtle dot grid background — like Codex / Antigravity */
	.grid-bg {
		position: fixed;
		inset: 0;
		background-image: radial-gradient(circle, #e4e4e7 1px, transparent 1px);
		background-size: 28px 28px;
		opacity: 0.45;
		pointer-events: none;
		z-index: 0;
	}

	/* ── HEADER ──────────────────────────────────────────────────────── */
	.header {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 100;
		background: rgba(255, 255, 255, 0.88);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border-bottom: 1px solid rgba(0, 0, 0, 0.06);
	}

	.header-inner {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 24px;
		height: 56px;
		display: flex;
		align-items: center;
		gap: 32px;
	}

	.logo {
		display: flex;
		align-items: center;
		gap: 8px;
		text-decoration: none;
		color: #0a0a0a;
		font-size: 15px;
		font-weight: 700;
		letter-spacing: -0.01em;
		flex-shrink: 0;
	}

	.logo-mark {
		display: flex;
		align-items: center;
		color: #0a0a0a;
	}

	.logo-mark.small {
		color: #666;
	}

	.logo-dot {
		color: #888;
		font-weight: 500;
	}

	.nav {
		display: flex;
		align-items: center;
		gap: 4px;
		flex: 1;
	}

	.nav-link {
		padding: 6px 12px;
		font-size: 14px;
		color: #555;
		text-decoration: none;
		border-radius: 8px;
		transition: all 0.15s;
		font-weight: 500;
	}

	.nav-link:hover {
		color: #0a0a0a;
		background: rgba(0, 0, 0, 0.04);
	}

	.header-actions {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-shrink: 0;
	}

	.btn-ghost {
		padding: 7px 16px;
		font-size: 14px;
		color: #444;
		text-decoration: none;
		border-radius: 9px;
		transition: all 0.15s;
		font-weight: 500;
	}

	.btn-ghost:hover {
		color: #0a0a0a;
		background: rgba(0, 0, 0, 0.04);
	}

	.btn-primary {
		padding: 7px 18px;
		font-size: 14px;
		font-weight: 600;
		color: #fff;
		background: #0a0a0a;
		border-radius: 9px;
		text-decoration: none;
		transition: all 0.15s;
		letter-spacing: -0.01em;
	}

	.btn-primary:hover {
		background: #222;
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0,0,0,0.15);
	}

	/* ── HERO ─────────────────────────────────────────────────────────── */
	.hero {
		position: relative;
		z-index: 1;
		padding-top: 140px;
		padding-bottom: 100px;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0;
		max-width: 900px;
		margin: 0 auto;
		padding-left: 24px;
		padding-right: 24px;
	}

	.eyebrow {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		padding: 6px 14px;
		background: rgba(0, 0, 0, 0.04);
		border: 1px solid rgba(0, 0, 0, 0.07);
		border-radius: 100px;
		font-size: 12.5px;
		font-weight: 500;
		color: #555;
		letter-spacing: 0.01em;
		margin-bottom: 32px;
	}

	.eyebrow-dot {
		width: 6px;
		height: 6px;
		background: #22c55e;
		border-radius: 50%;
		animation: pulse 2s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; transform: scale(1); }
		50% { opacity: 0.5; transform: scale(0.8); }
	}

	/* The hero headline — massive, bold, Antigravity/Codex inspired */
	.hero-headline {
		font-size: clamp(48px, 7vw, 88px);
		font-weight: 800;
		line-height: 1.05;
		letter-spacing: -0.04em;
		color: #0a0a0a;
		margin: 0 0 12px;
	}

	.headline-accent {
		background: linear-gradient(135deg, #0a0a0a 0%, #666 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.hero-sub {
		font-size: 18px;
		color: #666;
		line-height: 1.6;
		margin: 0 0 40px;
		max-width: 580px;
		font-weight: 400;
	}

	/* ── PROMPT INPUT ─────────────────────────────────────────────────── */
	.prompt-container {
		width: 100%;
		max-width: 680px;
		background: #fff;
		border: 1.5px solid #e4e4e7;
		border-radius: 16px;
		box-shadow: 0 4px 24px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
		transition: all 0.2s ease;
		overflow: visible;
		position: relative;
		padding: 14px 16px 12px;
		display: flex;
		flex-direction: column;
		gap: 10px;
		margin-bottom: 16px;
	}

	.prompt-container.focused {
		border-color: #0a0a0a;
		box-shadow: 0 0 0 3px rgba(0,0,0,0.06), 0 4px 24px rgba(0,0,0,0.08);
	}

	.model-selector-wrap {
		position: relative;
	}

	.model-selector {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 5px 10px;
		background: rgba(0,0,0,0.03);
		border: 1px solid rgba(0,0,0,0.07);
		border-radius: 8px;
		font-size: 12.5px;
		font-weight: 500;
		color: #444;
		cursor: pointer;
		transition: all 0.15s;
	}

	.model-selector:hover {
		background: rgba(0,0,0,0.06);
		border-color: rgba(0,0,0,0.12);
	}

	.model-dot {
		width: 7px;
		height: 7px;
		border-radius: 50%;
		flex-shrink: 0;
	}

	.model-caret {
		color: #888;
		transition: transform 0.15s;
	}

	.model-caret.open {
		transform: rotate(180deg);
	}

	.model-dropdown {
		position: absolute;
		top: calc(100% + 6px);
		left: 0;
		background: #fff;
		border: 1px solid #e4e4e7;
		border-radius: 12px;
		box-shadow: 0 8px 32px rgba(0,0,0,0.1);
		z-index: 200;
		min-width: 240px;
		overflow: hidden;
		padding: 6px;
	}

	.model-option {
		display: flex;
		align-items: center;
		gap: 10px;
		width: 100%;
		padding: 9px 12px;
		border: none;
		background: none;
		cursor: pointer;
		border-radius: 8px;
		transition: background 0.1s;
	}

	.model-option:hover, .model-option.active {
		background: rgba(0,0,0,0.04);
	}

	.option-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		flex-shrink: 0;
	}

	.option-info {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		flex: 1;
		gap: 1px;
	}

	.option-name {
		font-size: 13px;
		font-weight: 500;
		color: #111;
	}

	.option-provider {
		font-size: 11.5px;
		color: #888;
	}

	.option-check {
		color: #0a0a0a;
		flex-shrink: 0;
	}

	.input-area {
		flex: 1;
	}

	.input-area textarea {
		width: 100%;
		border: none;
		background: transparent;
		resize: none;
		font-size: 15px;
		color: #0a0a0a;
		line-height: 1.5;
		outline: none;
		font-family: inherit;
		min-height: 24px;
		max-height: 200px;
		overflow-y: auto;
		box-sizing: border-box;
		padding: 0;
		display: block;
	}

	.input-area textarea::placeholder {
		color: #aaa;
	}

	.send-btn {
		align-self: flex-end;
		width: 36px;
		height: 36px;
		border-radius: 10px;
		border: none;
		background: #e4e4e7;
		color: #888;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.15s;
		flex-shrink: 0;
	}

	.send-btn.active {
		background: #0a0a0a;
		color: #fff;
	}

	.send-btn.active:hover {
		background: #222;
		transform: translateY(-1px);
	}

	/* ── STARTERS ─────────────────────────────────────────────────────── */
	.starters {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		justify-content: center;
		margin-bottom: 36px;
	}

	.starter-chip {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 8px 14px;
		background: rgba(0,0,0,0.03);
		border: 1px solid rgba(0,0,0,0.07);
		border-radius: 100px;
		font-size: 13px;
		color: #555;
		cursor: pointer;
		transition: all 0.15s;
		font-weight: 500;
	}

	.starter-chip:hover {
		background: rgba(0,0,0,0.07);
		border-color: rgba(0,0,0,0.12);
		color: #0a0a0a;
		transform: translateY(-1px);
	}

	/* ── HERO CTAs ────────────────────────────────────────────────────── */
	.hero-ctas {
		display: flex;
		align-items: center;
		gap: 12px;
		margin-bottom: 56px;
	}

	.cta-primary {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		padding: 11px 22px;
		background: #0a0a0a;
		color: #fff;
		border-radius: 100px;
		font-size: 14px;
		font-weight: 600;
		text-decoration: none;
		transition: all 0.2s;
		letter-spacing: -0.01em;
		border: none;
		cursor: pointer;
	}

	.cta-primary:hover {
		background: #222;
		transform: translateY(-2px);
		box-shadow: 0 8px 24px rgba(0,0,0,0.15);
	}

	.cta-primary.large {
		padding: 14px 28px;
		font-size: 15px;
	}

	.cta-ghost {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		padding: 11px 22px;
		background: transparent;
		color: #555;
		border-radius: 100px;
		font-size: 14px;
		font-weight: 500;
		text-decoration: none;
		border: 1px solid #e4e4e7;
		transition: all 0.2s;
		cursor: pointer;
	}

	.cta-ghost:hover {
		color: #0a0a0a;
		border-color: #c4c4c7;
		background: rgba(0,0,0,0.03);
	}

	.cta-ghost.large {
		padding: 14px 28px;
		font-size: 15px;
	}

	/* ── STATS ────────────────────────────────────────────────────────── */
	.stats-row {
		display: flex;
		align-items: center;
		gap: 32px;
	}

	.stat {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 2px;
	}

	.stat-num {
		font-size: 28px;
		font-weight: 800;
		color: #0a0a0a;
		letter-spacing: -0.03em;
		line-height: 1;
	}

	.stat-label {
		font-size: 12px;
		color: #888;
		font-weight: 500;
	}

	.stat-divider {
		width: 1px;
		height: 32px;
		background: #e4e4e7;
	}

	/* ── SECTIONS ─────────────────────────────────────────────────────── */
	.section {
		position: relative;
		z-index: 1;
		padding: 100px 24px;
	}

	.section-dark {
		background: #0a0a0a;
	}

	.section-cta {
		background: #f9f9f9;
		border-top: 1px solid #e4e4e7;
	}

	.section-inner {
		max-width: 1140px;
		margin: 0 auto;
	}

	.section-header {
		text-align: center;
		margin-bottom: 64px;
	}

	.section-header-light {
		text-align: center;
		margin-bottom: 64px;
	}

	.section-label {
		display: inline-block;
		font-size: 12px;
		font-weight: 600;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #888;
		margin-bottom: 16px;
	}

	.section-label-light {
		display: inline-block;
		font-size: 12px;
		font-weight: 600;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #666;
		margin-bottom: 16px;
	}

	.section-headline {
		font-size: clamp(32px, 4vw, 52px);
		font-weight: 800;
		color: #0a0a0a;
		margin: 0 0 16px;
		letter-spacing: -0.03em;
		line-height: 1.1;
	}

	.section-headline-light {
		font-size: clamp(32px, 4vw, 52px);
		font-weight: 800;
		color: #fff;
		margin: 0 0 16px;
		letter-spacing: -0.03em;
		line-height: 1.1;
	}

	.section-sub {
		font-size: 16px;
		color: #666;
		max-width: 520px;
		margin: 0 auto;
		line-height: 1.6;
	}

	.section-sub-light {
		font-size: 16px;
		color: #888;
		max-width: 520px;
		margin: 0 auto;
		line-height: 1.6;
	}

	/* ── BENTO GRID ──────────────────────────────────────────────────── */
	.bento-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		grid-auto-rows: auto;
		gap: 16px;
	}

	.bento-card {
		background: #fff;
		border: 1px solid #e4e4e7;
		border-radius: 16px;
		padding: 28px;
		transition: all 0.2s;
		position: relative;
		overflow: hidden;
	}

	.bento-card::before {
		content: '';
		position: absolute;
		inset: 0;
		background: radial-gradient(400px at 50% -20%, rgba(0,0,0,0.02), transparent);
		pointer-events: none;
	}

	.bento-card:hover {
		border-color: #c4c4c7;
		transform: translateY(-2px);
		box-shadow: 0 8px 32px rgba(0,0,0,0.06);
	}

	.bento-large {
		grid-column: span 2;
		padding: 36px;
	}

	.bento-medium {
		grid-column: span 1;
	}

	.bento-small {
		grid-column: span 1;
	}

	.bento-tag {
		display: inline-block;
		font-size: 11px;
		font-weight: 600;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: #888;
		background: rgba(0,0,0,0.04);
		padding: 3px 8px;
		border-radius: 5px;
		margin-bottom: 14px;
	}

	.bento-title {
		font-size: 20px;
		font-weight: 700;
		color: #0a0a0a;
		margin: 0 0 10px;
		letter-spacing: -0.02em;
	}

	.bento-desc {
		font-size: 14px;
		color: #666;
		line-height: 1.65;
		margin: 0;
	}

	/* ── AGENTS GRID ─────────────────────────────────────────────────── */
	.agents-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 12px;
	}

	.agent-card {
		background: rgba(255,255,255,0.04);
		border: 1px solid rgba(255,255,255,0.08);
		border-radius: 14px;
		padding: 20px;
		transition: all 0.2s;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.agent-card:hover {
		background: rgba(255,255,255,0.07);
		border-color: rgba(255,255,255,0.15);
		transform: translateY(-2px);
	}

	.agent-emoji {
		font-size: 24px;
		line-height: 1;
	}

	.agent-info {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.agent-domain {
		font-size: 11px;
		font-weight: 600;
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: #666;
	}

	.agent-name {
		font-size: 15px;
		font-weight: 700;
		color: #fff;
		margin: 0;
		letter-spacing: -0.01em;
	}

	.agent-desc {
		font-size: 12.5px;
		color: #666;
		line-height: 1.55;
		margin: 0;
	}

	/* ── INTEGRATIONS ─────────────────────────────────────────────────── */
	.integrations-grid {
		display: grid;
		grid-template-columns: repeat(6, 1fr);
		gap: 12px;
		margin-bottom: 20px;
	}

	.integration-card {
		background: #fff;
		border: 1px solid #e4e4e7;
		border-radius: 12px;
		padding: 18px 14px;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 8px;
		transition: all 0.2s;
		text-decoration: none;
	}

	.integration-card:hover {
		border-color: #c4c4c7;
		transform: translateY(-2px);
		box-shadow: 0 4px 16px rgba(0,0,0,0.06);
	}

	.int-icon {
		font-size: 22px;
		line-height: 1;
	}

	.int-name {
		font-size: 12px;
		font-weight: 600;
		color: #555;
	}

	.integration-note {
		text-align: center;
		font-size: 13px;
		color: #aaa;
		padding: 12px 0;
	}

	/* ── USE CASES ────────────────────────────────────────────────────── */
	.use-cases-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 16px;
	}

	.uc-card {
		background: #fff;
		border: 1px solid #e4e4e7;
		border-radius: 16px;
		padding: 32px;
		display: flex;
		flex-direction: column;
		gap: 14px;
		transition: all 0.2s;
	}

	.uc-card:hover {
		border-color: #c4c4c7;
		transform: translateY(-2px);
		box-shadow: 0 8px 32px rgba(0,0,0,0.06);
	}

	.uc-icon {
		font-size: 28px;
		line-height: 1;
	}

	.uc-title {
		font-size: 20px;
		font-weight: 700;
		color: #0a0a0a;
		margin: 0;
		letter-spacing: -0.02em;
	}

	.uc-desc {
		font-size: 14px;
		color: #666;
		line-height: 1.65;
		margin: 0;
		flex: 1;
	}

	.uc-cta {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		font-size: 13.5px;
		font-weight: 600;
		color: #0a0a0a;
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		text-decoration: none;
		transition: gap 0.2s;
	}

	.uc-cta:hover {
		gap: 10px;
	}

	/* ── FINAL CTA ────────────────────────────────────────────────────── */
	.cta-inner {
		text-align: center;
		padding: 80px 0;
	}

	.cta-headline {
		font-size: clamp(40px, 5vw, 72px);
		font-weight: 800;
		color: #0a0a0a;
		letter-spacing: -0.04em;
		margin: 0 0 16px;
		line-height: 1.05;
	}

	.cta-sub {
		font-size: 17px;
		color: #666;
		line-height: 1.6;
		margin: 0 0 40px;
	}

	.cta-actions {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 12px;
	}

	/* ── FOOTER ───────────────────────────────────────────────────────── */
	.footer {
		background: #fff;
		border-top: 1px solid #e4e4e7;
		padding: 32px 24px;
		position: relative;
		z-index: 1;
	}

	.footer-inner {
		max-width: 1140px;
		margin: 0 auto;
		display: flex;
		align-items: center;
		justify-content: space-between;
		flex-wrap: wrap;
		gap: 16px;
	}

	.footer-logo {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 14px;
		font-weight: 700;
		color: #0a0a0a;
		letter-spacing: -0.01em;
	}

	.footer-links {
		display: flex;
		gap: 20px;
	}

	.footer-links a, .footer-link {
		font-size: 13.5px;
		color: #888;
		text-decoration: none;
		transition: color 0.15s;
	}

	.footer-links a:hover, .footer-link:hover {
		color: #0a0a0a;
	}

	.footer-copy {
		font-size: 12.5px;
		color: #bbb;
		margin: 0;
	}

	/* ── OVERLAY ──────────────────────────────────────────────────────── */
	.overlay {
		position: fixed;
		inset: 0;
		z-index: 150;
		background: transparent;
	}

	/* ── RESPONSIVE ───────────────────────────────────────────────────── */
	@media (max-width: 900px) {
		.nav { display: none; }
		.bento-grid { grid-template-columns: 1fr 1fr; }
		.bento-large { grid-column: span 2; }
		.agents-grid { grid-template-columns: repeat(2, 1fr); }
		.integrations-grid { grid-template-columns: repeat(3, 1fr); }
		.use-cases-grid { grid-template-columns: 1fr; }
	}

	@media (max-width: 600px) {
		.hero { padding-top: 100px; padding-bottom: 60px; }
		.hero-headline { font-size: 40px; }
		.bento-grid { grid-template-columns: 1fr; }
		.bento-large { grid-column: span 1; }
		.agents-grid { grid-template-columns: 1fr 1fr; }
		.integrations-grid { grid-template-columns: repeat(3, 1fr); }
		.stats-row { gap: 16px; }
		.stat-num { font-size: 22px; }
		.header-actions .btn-ghost { display: none; }
	}
</style>
