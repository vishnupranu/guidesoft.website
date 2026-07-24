<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';

	// ── State ──────────────────────────────────────────────────────
	let prompt = '';
	let selectedModel = 'GPT-4o';
	let showModelDropdown = false;
	let inputFocused = false;
	let activeTab = 'all';
	let billingAnnual = false;
	let activeFaq = -1;
	let scrollY = 0;

	// Models available
	const models = [
		{ id: 'GPT-4o', name: 'GPT-4o', provider: 'OpenAI', icon: '⚡', color: '#10a37f' },
		{ id: 'Claude-3.5', name: 'Claude 3.5 Sonnet', provider: 'Anthropic', icon: '🧠', color: '#d97706' },
		{ id: 'Gemini-1.5', name: 'Gemini 1.5 Pro', provider: 'Google', icon: '✨', color: '#2563eb' },
		{ id: 'DeepSeek-V3', name: 'DeepSeek V3', provider: 'DeepSeek', icon: '🚀', color: '#7c3aed' },
		{ id: 'Llama-3.3', name: 'Llama 3.3 70B', provider: 'Meta', icon: '🦙', color: '#0284c7' }
	];

	// Starters
	const starters = [
		{ label: 'Summarize 50-page PDF report', icon: '📄', model: 'GPT-4o' },
		{ label: 'Build a Next.js + Tailwind web app', icon: '💻', model: 'Claude 3.5 Sonnet' },
		{ label: 'Analyze Q3 revenue trends with Python', icon: '📊', model: 'DeepSeek V3' },
		{ label: 'Translate technical spec to Spanish', icon: '🌐', model: 'Gemini 1.5 Pro' }
	];

	// Typing animation
	const typingSentences = [
		"Welcome to GUIDESOFT.WEB — your personal AI workplace.",
		"Connect GPT-4o, Claude 3.5, Gemini, Llama 3, and DeepSeek in one place.",
		"Upload PDFs, docs, and code to chat with your knowledge base.",
		"Run autonomous AI agents, vision tools, and local models securely."
	];
	let sentenceIdx = 0;
	let charIdx = 0;
	let isDeleting = false;
	let typingText = '';
	let typingTimer: ReturnType<typeof setTimeout>;

	function typeEffect() {
		const currentSentence = typingSentences[sentenceIdx];
		if (!isDeleting) {
			typingText = currentSentence.slice(0, charIdx + 1);
			charIdx++;
			if (charIdx === currentSentence.length) {
				isDeleting = true;
				typingTimer = setTimeout(typeEffect, 2200);
				return;
			}
		} else {
			typingText = currentSentence.slice(0, charIdx - 1);
			charIdx--;
			if (charIdx === 0) {
				isDeleting = false;
				sentenceIdx = (sentenceIdx + 1) % typingSentences.length;
				typingTimer = setTimeout(typeEffect, 400);
				return;
			}
		}
		typingTimer = setTimeout(typeEffect, isDeleting ? 25 : 45);
	}

	// Agents showcase
	const agents = [
		{ name: 'Senior Developer', avatar: '👨‍💻', desc: 'Writes clean, tested code in React, Python, Go & Rust', tag: 'Coding', stars: '4.9k' },
		{ name: 'Data Analyst', avatar: '📈', desc: 'Analyzes CSVs, generates charts and SQL queries instantly', tag: 'Analytics', stars: '3.8k' },
		{ name: 'Research Scholar', avatar: '🔬', desc: 'Performs deep web searches & summarizes academic papers', tag: 'Research', stars: '5.2k' },
		{ name: 'Product Manager', avatar: '🚀', desc: 'Drafts PRDs, user stories, and roadmap documentation', tag: 'Productivity', stars: '4.1k' }
	];

	// Features Bento Grid
	const bentoItems = [
		{
			title: 'Multi-Model Switcher',
			desc: 'Switch seamlessly between OpenAI, Anthropic, Google, and local Ollama models in the same chat thread.',
			icon: '🔮',
			badge: 'All-in-One'
		},
		{
			title: 'Knowledge Base (RAG)',
			desc: 'Upload documents, codebase repos, and PDFs. Get accurate answers backed by precise citations.',
			icon: '📚',
			badge: 'Enterprise RAG'
		},
		{
			title: 'Code Interpreter & Sandbox',
			desc: 'Execute Python code safely in Pyodide WASM sandbox. Plot charts and export clean datasets.',
			icon: '⚡',
			badge: 'WASM Powered'
		},
		{
			title: 'Autonomous Agents & Tools',
			desc: 'Equip AI with web browsing, search tools, multi-agent orchestration, and custom API calls.',
			icon: '🤖',
			badge: 'Agentic Workflow'
		},
		{
			title: 'Voice & Vision Multimodal',
			desc: 'Speak naturally with real-time TTS/STT and upload screenshots or diagrams for vision analysis.',
			icon: '🎙️',
			badge: 'Real-Time Voice'
		},
		{
			title: '100% Privacy & Self-Hostable',
			desc: 'Deploy locally via Docker. Zero external data tracking — full control of your keys and data.',
			icon: '🛡️',
			badge: 'Open Source'
		}
	];

	// Testimonials
	const testimonials = [
		{ name: 'Elena Rostova', role: 'CTO, AI Scale', quote: 'GUIDESOFT replaced 4 different subscription tools for our team. The LobeHub UI combined with local model support is world-class.', avatar: 'ER' },
		{ name: 'David Kim', role: 'Staff Engineer, DevWorks', quote: 'The speed of model switching and the rich markdown/artifacts viewer makes coding 3x faster every single day.', avatar: 'DK' },
		{ name: 'Sarah Jenkins', role: 'Research Lead, OpenData', quote: 'Having RAG document chat with zero setup saved our lab hundreds of hours in paper synthesis.', avatar: 'SJ' }
	];

	// FAQs
	const faqs = [
		{ q: 'What is GUIDESOFT.WEB?', a: 'GUIDESOFT.WEB is an open-source, modern AI workspace inspired by LobeHub. It brings together top AI models, knowledge management, and AI agents into one interface.' },
		{ q: 'Can I self-host GUIDESOFT on my own server?', a: 'Yes! GUIDESOFT is fully open source and containerized with Docker. You can deploy it on local hardware or any cloud provider in under 2 minutes.' },
		{ q: 'How does model pricing work?', a: 'You can use your own API keys for OpenAI, Anthropic, Google, or DeepSeek — or run 100% free offline models using Ollama and local LLMs.' },
		{ q: 'Is my data secure?', a: 'Yes. All data remains stored in your local browser storage or self-hosted database. We do not track or store your conversations.' }
	];

	function handleSend() {
		if (!prompt.trim()) return;
		const encodedPrompt = encodeURIComponent(prompt.trim());
		goto(`/auth?next=chat&prompt=${encodedPrompt}&model=${selectedModel}`);
	}

	function handleStarterClick(starterPrompt: string, modelId: string) {
		prompt = starterPrompt;
		selectedModel = modelId;
		handleSend();
	}

	function observeReveal() {
		const io = new IntersectionObserver((entries) => {
			entries.forEach((entry) => {
				if (entry.isIntersecting) {
					entry.target.classList.add('revealed');
					io.unobserve(entry.target);
				}
			});
		}, { threshold: 0.1 });
		document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
	}

	onMount(() => {
		typeEffect();
		setTimeout(observeReveal, 100);
	});

	onDestroy(() => {
		clearTimeout(typingTimer);
	});
</script>

<svelte:window bind:scrollY />

<div class="lobe-landing">

	<!-- ══════════════════════════════════════════════════
	     HEADER / NAV
	════════════════════════════════════════════════════ -->
	<header class="header" class:scrolled={scrollY > 30}>
		<div class="header-container">
			<a href="/" class="brand-logo">
				<div class="brand-icon">G</div>
				<span class="brand-name">GUIDESOFT<span class="brand-accent">.WEB</span></span>
				<span class="brand-tag">v2.5</span>
			</a>

			<nav class="nav-links">
				<a href="#features" class="nav-item">Features</a>
				<a href="#models" class="nav-item">Models</a>
				<a href="#agents" class="nav-item">Agents</a>
				<a href="#pricing" class="nav-item">Pricing</a>
				<a href="#faq" class="nav-item">FAQ</a>
			</nav>

			<div class="nav-right">
				<a href="https://github.com/vishnupranu/guidesoft.website" target="_blank" class="gh-star-btn">
					<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
					<span>Star</span>
					<span class="star-count">1.4k</span>
				</a>
				<a href="/auth" class="btn-secondary">Sign In</a>
				<a href="/auth?mode=signup" class="btn-gradient">Get Started</a>
			</div>
		</div>
	</header>

	<!-- ══════════════════════════════════════════════════
	     HERO SECTION (LOBEHUB CHAT INTERFACE)
	════════════════════════════════════════════════════ -->
	<section class="hero-section">
		<div class="hero-background-gradient"></div>
		<div class="hero-grid-overlay"></div>

		<div class="hero-container">
			<!-- Announcement Badge -->
			<div class="hero-badge">
				<span class="badge-sparkle">✦</span>
				<span>Introducing GUIDESOFT.WEB 2.5 with DeepSeek V3 &amp; Ant Design X</span>
				<span class="badge-arrow">→</span>
			</div>

			<!-- Title & Typewriter -->
			<h1 class="hero-title">
				Shape the Future of Work<br />
				<span class="gradient-text">with GUIDESOFT AI</span>
			</h1>

			<!-- Typewriter Container -->
			<div class="typewriter-box">
				<span class="typing-content">{typingText}</span><span class="type-cursor">|</span>
			</div>

			<!-- LobeHub-Style Chat Input Container -->
			<div class="lobe-input-card" class:focused={inputFocused}>
				<!-- Input Top Bar (Model Selector & Controls) -->
				<div class="input-header">
					<div class="model-picker-wrap">
						<button
							class="model-picker-trigger"
							on:click={() => (showModelDropdown = !showModelDropdown)}
						>
							<span class="model-picker-icon">{models.find(m => m.id === selectedModel)?.icon}</span>
							<span class="model-picker-name">{models.find(m => m.id === selectedModel)?.name}</span>
							<span class="model-picker-badge">{models.find(m => m.id === selectedModel)?.provider}</span>
							<span class="dropdown-arrow">▾</span>
						</button>

						{#if showModelDropdown}
							<div class="model-dropdown-menu">
								<div class="menu-title">Select Active Model</div>
								{#each models as m}
									<button
										class="dropdown-item"
										class:selected={selectedModel === m.id}
										on:click={() => { selectedModel = m.id; showModelDropdown = false; }}
									>
										<span class="m-icon">{m.icon}</span>
										<div class="m-info">
											<div class="m-name">{m.name}</div>
											<div class="m-provider">{m.provider}</div>
										</div>
										{#if selectedModel === m.id}<span class="m-check">✓</span>{/if}
									</button>
								{/each}
							</div>
						{/if}
					</div>

					<div class="input-actions-top">
						<button class="icon-tool-btn" title="Agent Mode">🤖 <span class="tool-label">Agent Mode</span></button>
						<button class="icon-tool-btn" title="Attach Document/PDF">📎 <span class="tool-label">Attach File</span></button>
					</div>
				</div>

				<!-- Main Input Area -->
				<div class="input-body">
					<textarea
						bind:value={prompt}
						on:focus={() => (inputFocused = true)}
						on:blur={() => (inputFocused = false)}
						on:keydown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
						placeholder="Ask GUIDESOFT anything, generate code, or upload documents…"
						class="lobe-textarea"
						rows="3"
					></textarea>
				</div>

				<!-- Input Footer & Send Button -->
				<div class="input-footer">
					<div class="input-footer-left">
						<span class="privacy-badge">🔒 100% Private &amp; Encrypted</span>
						<span class="shortcut-hint">Press <strong>Enter ↵</strong> to send</span>
					</div>

					<button class="send-btn" on:click={handleSend} disabled={!prompt.trim()}>
						<span>Send Message</span>
						<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
					</button>
				</div>
			</div>

			<!-- Quick Starter Prompts -->
			<div class="starters-row">
				<span class="starters-label">Try asking:</span>
				{#each starters as s}
					<button class="starter-chip" on:click={() => handleStarterClick(s.label, s.model)}>
						<span class="starter-icon">{s.icon}</span>
						<span class="starter-text">{s.label}</span>
					</button>
				{/each}
			</div>

			<!-- Platform Stats -->
			<div class="stats-strip">
				<div class="stat-box"><strong>50,000+</strong><span>Active Developers</span></div>
				<div class="stat-sep"></div>
				<div class="stat-box"><strong>12+</strong><span>LLM Providers</span></div>
				<div class="stat-sep"></div>
				<div class="stat-box"><strong>99.9%</strong><span>Uptime SLA</span></div>
				<div class="stat-sep"></div>
				<div class="stat-box"><strong>100%</strong><span>Open Source</span></div>
			</div>
		</div>
	</section>

	<!-- ══════════════════════════════════════════════════
	     SUPPORTED MODELS MATRIX
	════════════════════════════════════════════════════ -->
	<section class="models-section reveal" id="models">
		<div class="section-container">
			<div class="section-badge center">MODEL MATRIX</div>
			<h2 class="section-title center">One Interface, All World-Class AI Models</h2>
			<p class="section-subtitle center">Connect your API keys or run completely offline with Ollama.</p>

			<div class="models-grid">
				{#each [
					{ name: 'OpenAI GPT-4o', desc: 'Flagship multimodal model for complex reasoning and vision.', badge: 'GPT-4o', color: '#10a37f' },
					{ name: 'Anthropic Claude 3.5', desc: 'Industry-leading coding, instruction following, and analysis.', badge: 'Claude 3.5', color: '#d97706' },
					{ name: 'Google Gemini 1.5 Pro', desc: '1M token context window for massive codebase analysis.', badge: 'Gemini Pro', color: '#2563eb' },
					{ name: 'DeepSeek V3 / R1', desc: 'Open-weights reasoning powerhouse with high cost efficiency.', badge: 'DeepSeek', color: '#7c3aed' },
					{ name: 'Meta Llama 3.3 70B', desc: 'State-of-the-art open source model for self-hosted privacy.', badge: 'Llama 3.3', color: '#0284c7' },
					{ name: 'Ollama & Local LLMs', desc: 'Run Llama, Mistral, and Qwen offline on your local GPU.', badge: 'Local GPU', color: '#059669' }
				] as m}
					<div class="model-card" style="--accent: {m.color}">
						<div class="model-card-top">
							<span class="m-badge" style="background: {m.color}20; color: {m.color}; border: 1px solid {m.color}40">{m.badge}</span>
							<span class="m-dot" style="background: {m.color}"></span>
						</div>
						<h3 class="m-title">{m.name}</h3>
						<p class="m-desc">{m.desc}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ══════════════════════════════════════════════════
	     BENTO GRID FEATURES
	════════════════════════════════════════════════════ -->
	<section class="bento-section reveal" id="features">
		<div class="section-container">
			<div class="section-badge center">PLATFORM FEATURES</div>
			<h2 class="section-title center">Engineered for Maximum AI Productivity</h2>
			<p class="section-subtitle center">Built with modern UI standards, smooth animations, and clean ergonomics.</p>

			<div class="bento-grid">
				{#each bentoItems as item, i}
					<div class="bento-card" style="animation-delay: {i * 70}ms">
						<div class="bento-header">
							<span class="bento-icon">{item.icon}</span>
							<span class="bento-tag">{item.badge}</span>
						</div>
						<h3 class="bento-title">{item.title}</h3>
						<p class="bento-desc">{item.desc}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ══════════════════════════════════════════════════
	     AGENT MARKETPLACE / DISCOVER
	════════════════════════════════════════════════════ -->
	<section class="agents-section reveal" id="agents">
		<div class="section-container">
			<div class="section-badge center">AI AGENT MARKETPLACE</div>
			<h2 class="section-title center">Pre-Built AI Agents for Every Role</h2>
			<p class="section-subtitle center">Deploy specialized assistants with tailored prompt instructions and toolsets.</p>

			<div class="agents-grid">
				{#each agents as agent}
					<div class="agent-card">
						<div class="agent-avatar">{agent.avatar}</div>
						<div class="agent-content">
							<div class="agent-top">
								<h3 class="agent-name">{agent.name}</h3>
								<span class="agent-tag">{agent.tag}</span>
							</div>
							<p class="agent-desc">{agent.desc}</p>
							<div class="agent-bottom">
								<span class="agent-stars">⭐ {agent.stars} uses</span>
								<a href="/auth?mode=signup" class="agent-use-btn">Use Agent →</a>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ══════════════════════════════════════════════════
	     PRICING SECTION
	════════════════════════════════════════════════════ -->
	<section class="pricing-section reveal" id="pricing">
		<div class="section-container">
			<div class="section-badge center">PRICING</div>
			<h2 class="section-title center">Transparent Pricing for Everyone</h2>

			<div class="billing-switcher">
				<span class:active={!billingAnnual}>Monthly</span>
				<button class="switch-toggle" class:annual={billingAnnual} on:click={() => (billingAnnual = !billingAnnual)}>
					<span class="switch-ball"></span>
				</button>
				<span class:active={billingAnnual}>Annual <span class="discount-badge">Save 30%</span></span>
			</div>

			<div class="pricing-cards-grid">
				<!-- Community / Free -->
				<div class="price-card">
					<div class="price-title">Community</div>
					<div class="price-desc">Self-Hosted &amp; Open Source</div>
					<div class="price-amount"><span class="val">$0</span><span class="unit">/forever</span></div>
					<ul class="price-features">
						<li>✓ 100% Open Source</li>
						<li>✓ Unlimited Local Ollama Chat</li>
						<li>✓ Self-host via Docker</li>
						<li>✓ Knowledge RAG Support</li>
						<li>✓ Community Discord</li>
					</ul>
					<a href="https://github.com/vishnupranu/guidesoft.website" target="_blank" class="price-btn">Deploy Yourself</a>
				</div>

				<!-- Pro -->
				<div class="price-card popular">
					<div class="popular-ribbon">Most Popular</div>
					<div class="price-title">Pro Cloud</div>
					<div class="price-desc">For Individuals &amp; Power Users</div>
					<div class="price-amount">
						<span class="val">{billingAnnual ? '$14' : '$20'}</span>
						<span class="unit">/month</span>
					</div>
					<ul class="price-features">
						<li>✓ Unlimited Hosted Model Access</li>
						<li>✓ GPT-4o, Claude 3.5 &amp; Gemini Pro</li>
						<li>✓ Unlimited Document Knowledge Bases</li>
						<li>✓ Pyodide Code Interpreter</li>
						<li>✓ Priority Fast Response SLA</li>
					</ul>
					<a href="/auth?mode=signup&plan=pro" class="price-btn primary">Start Free Trial</a>
				</div>

				<!-- Enterprise -->
				<div class="price-card">
					<div class="price-title">Enterprise</div>
					<div class="price-desc">For Organizations at Scale</div>
					<div class="price-amount"><span class="val">Custom</span></div>
					<ul class="price-features">
						<li>✓ Private Cloud / On-Premise VPC</li>
						<li>✓ Single Sign-On (SSO / SAML)</li>
						<li>✓ Custom Agent Development</li>
						<li>✓ SOC 2 &amp; HIPAA Compliance</li>
						<li>✓ 24/7 Dedicated Support</li>
					</ul>
					<a href="/auth?mode=signup&plan=enterprise" class="price-btn">Contact Sales</a>
				</div>
			</div>
		</div>
	</section>

	<!-- ══════════════════════════════════════════════════
	     FAQ SECTION
	════════════════════════════════════════════════════ -->
	<section class="faq-section reveal" id="faq">
		<div class="section-container" style="max-width: 800px">
			<div class="section-badge center">FAQ</div>
			<h2 class="section-title center">Frequently Asked Questions</h2>

			<div class="faq-accordion">
				{#each faqs as item, i}
					<div class="faq-card" class:open={activeFaq === i}>
						<button class="faq-header-btn" on:click={() => (activeFaq = activeFaq === i ? -1 : i)}>
							<span class="faq-question-text">{item.q}</span>
							<span class="faq-icon">{activeFaq === i ? '−' : '+'}</span>
						</button>
						{#if activeFaq === i}
							<div class="faq-body-text">{item.a}</div>
						{/if}
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ══════════════════════════════════════════════════
	     FOOTER
	════════════════════════════════════════════════════ -->
	<footer class="footer">
		<div class="footer-container">
			<div class="footer-grid">
				<div class="footer-brand-col">
					<div class="brand-logo">
						<div class="brand-icon">G</div>
						<span class="brand-name">GUIDESOFT<span class="brand-accent">.WEB</span></span>
					</div>
					<p class="footer-desc">
						The Open-Source AI Workspace.<br />
						Empowering developers, teams, and enterprises with world-class AI models.
					</p>
					<div class="footer-social-row">
						<a href="https://github.com/vishnupranu/guidesoft.website" target="_blank" class="social-chip">GitHub</a>
						<span class="social-chip">Discord</span>
						<span class="social-chip">Twitter / X</span>
					</div>
				</div>

				<div class="footer-col">
					<div class="footer-col-head">Product</div>
					<a href="#features" class="footer-link">Features</a>
					<a href="#models" class="footer-link">Models</a>
					<a href="#agents" class="footer-link">Agent Market</a>
					<a href="#pricing" class="footer-link">Pricing</a>
				</div>

				<div class="footer-col">
					<div class="footer-col-head">Developers</div>
					<a href="/auth" class="footer-link">API Docs</a>
					<a href="https://github.com/vishnupranu/guidesoft.website" target="_blank" class="footer-link">GitHub Repo</a>
					<a href="#" class="footer-link">Self-Host Guide</a>
					<a href="#" class="footer-link">Docker Hub</a>
				</div>

				<div class="footer-col">
					<div class="footer-col-head">Legal</div>
					<a href="#" class="footer-link">Privacy Policy</a>
					<a href="#" class="footer-link">Terms of Service</a>
					<a href="#" class="footer-link">Security Policy</a>
				</div>
			</div>

			<div class="footer-bottom-bar">
				<span>© 2024 GUIDESOFT.WEB. All rights reserved.</span>
				<span>Powered by Ant Design X &amp; SvelteKit</span>
			</div>
		</div>
	</footer>

</div>

<style>
	:global(body) {
		margin: 0; padding: 0;
		background: #09090b;
		color: #f4f4f5;
		font-family: 'Inter', system-ui, -apple-system, sans-serif;
		overflow-x: hidden;
	}
	:global(*) { box-sizing: border-box; }
	:global(a) { text-decoration: none; }

	.lobe-landing { width: 100%; position: relative; }

	/* ── Header ── */
	.header {
		position: fixed; top: 0; left: 0; right: 0; z-index: 100;
		padding: 16px 32px;
		transition: background 0.3s, backdrop-filter 0.3s, border-bottom 0.3s;
	}
	.header.scrolled {
		background: rgba(9, 9, 11, 0.85);
		backdrop-filter: blur(16px);
		border-bottom: 1px solid rgba(255, 255, 255, 0.08);
	}
	.header-container {
		max-width: 1240px; margin: 0 auto;
		display: flex; align-items: center; justify-content: space-between;
	}
	.brand-logo {
		display: flex; align-items: center; gap: 10px;
		color: #fff; font-size: 16px; font-weight: 700;
	}
	.brand-icon {
		width: 32px; height: 32px; border-radius: 8px;
		background: linear-gradient(135deg, #10b981, #059669);
		display: flex; align-items: center; justify-content: center;
		color: #fff; font-weight: 800; font-size: 16px;
	}
	.brand-name { font-family: 'Syne', sans-serif; }
	.brand-accent { color: #10b981; }
	.brand-tag {
		background: rgba(16, 185, 129, 0.15); color: #34d399;
		padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: 600;
	}

	.nav-links { display: flex; gap: 8px; }
	.nav-item {
		color: #a1a1aa; padding: 6px 14px; border-radius: 6px;
		font-size: 14px; font-weight: 500; transition: color 0.2s;
	}
	.nav-item:hover { color: #fff; background: rgba(255, 255, 255, 0.05); }

	.nav-right { display: flex; align-items: center; gap: 10px; }
	.gh-star-btn {
		display: inline-flex; align-items: center; gap: 6px;
		padding: 7px 12px; border-radius: 8px;
		background: rgba(255, 255, 255, 0.06);
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: #e4e4e7; font-size: 13px; font-weight: 500;
		transition: border-color 0.2s;
	}
	.gh-star-btn:hover { border-color: rgba(255, 255, 255, 0.25); color: #fff; }
	.star-count {
		background: rgba(255, 255, 255, 0.1); padding: 1px 6px;
		border-radius: 4px; font-size: 11px; color: #a1a1aa;
	}

	.btn-secondary {
		padding: 8px 16px; border-radius: 8px; color: #e4e4e7;
		font-size: 14px; font-weight: 500; transition: color 0.2s;
	}
	.btn-secondary:hover { color: #fff; }
	.btn-gradient {
		padding: 9px 18px; border-radius: 8px;
		background: linear-gradient(135deg, #10b981, #059669);
		color: #fff; font-size: 14px; font-weight: 600;
		transition: opacity 0.2s, transform 0.2s;
	}
	.btn-gradient:hover { opacity: 0.92; transform: translateY(-1px); }

	/* ── Hero Section ── */
	.hero-section {
		position: relative; min-height: 100vh;
		padding: 140px 24px 80px;
		display: flex; align-items: center; justify-content: center;
		overflow: hidden;
	}
	.hero-background-gradient {
		position: absolute; top: -100px; left: 50%; transform: translateX(-50%);
		width: 900px; height: 500px; border-radius: 50%;
		background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, rgba(37, 99, 235, 0.08) 50%, transparent 80%);
		filter: blur(80px); pointer-events: none;
	}
	.hero-grid-overlay {
		position: absolute; inset: 0; pointer-events: none;
		background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
		                  linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
		background-size: 40px 40px;
		mask-image: radial-gradient(circle at 50% 30%, black 30%, transparent 75%);
	}

	.hero-container {
		position: relative; z-index: 10;
		max-width: 880px; margin: 0 auto; text-align: center;
	}

	.hero-badge {
		display: inline-flex; align-items: center; gap: 8px;
		padding: 6px 16px; border-radius: 100px;
		background: rgba(16, 185, 129, 0.1);
		border: 1px solid rgba(16, 185, 129, 0.25);
		color: #34d399; font-size: 13px; font-weight: 500;
		margin-bottom: 24px;
	}

	.hero-title {
		font-family: 'Syne', sans-serif;
		font-size: clamp(38px, 6vw, 68px);
		font-weight: 800; line-height: 1.1; color: #fff;
		margin: 0 0 20px;
	}
	.gradient-text {
		background: linear-gradient(135deg, #34d399 0%, #60a5fa 50%, #a78bfa 100%);
		-webkit-background-clip: text; -webkit-text-fill-color: transparent;
	}

	.typewriter-box {
		font-size: 18px; color: #a1a1aa; min-height: 28px;
		margin-bottom: 36px;
	}
	.typing-content { color: #34d399; font-weight: 500; }
	.type-cursor { color: #10b981; animation: blink 1s infinite; }
	@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0;} }

	/* ── LobeHub Style Input Card ── */
	.lobe-input-card {
		background: rgba(24, 24, 27, 0.75);
		border: 1.5px solid rgba(255, 255, 255, 0.12);
		border-radius: 20px;
		backdrop-filter: blur(20px);
		box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), 0 0 30px rgba(16, 185, 129, 0.08);
		padding: 14px 18px;
		text-align: left; transition: border-color 0.2s, box-shadow 0.2s;
	}
	.lobe-input-card.focused {
		border-color: rgba(16, 185, 129, 0.6);
		box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.12), 0 20px 60px rgba(0, 0, 0, 0.5);
	}

	.input-header {
		display: flex; align-items: center; justify-content: space-between;
		margin-bottom: 10px;
	}
	.model-picker-wrap { position: relative; }
	.model-picker-trigger {
		display: flex; align-items: center; gap: 8px;
		padding: 6px 12px; border-radius: 8px;
		background: rgba(255, 255, 255, 0.06);
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: #fff; font-size: 13px; font-weight: 500;
		cursor: pointer; transition: background 0.2s;
	}
	.model-picker-trigger:hover { background: rgba(255, 255, 255, 0.1); }
	.model-picker-badge {
		background: rgba(16, 185, 129, 0.2); color: #34d399;
		padding: 2px 6px; border-radius: 4px; font-size: 11px;
	}

	.model-dropdown-menu {
		position: absolute; top: 110%; left: 0; z-index: 50;
		width: 260px; background: #18181b;
		border: 1px solid rgba(255, 255, 255, 0.15);
		border-radius: 12px; padding: 8px;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
	}
	.menu-title { font-size: 11px; color: #71717a; padding: 4px 8px; text-transform: uppercase; }
	.dropdown-item {
		width: 100%; display: flex; align-items: center; gap: 10px;
		padding: 8px 10px; border-radius: 6px; background: none;
		border: none; color: #e4e4e7; text-align: left;
		cursor: pointer; transition: background 0.2s;
	}
	.dropdown-item:hover, .dropdown-item.selected { background: rgba(255, 255, 255, 0.08); }
	.m-name { font-size: 13px; font-weight: 500; color: #fff; }
	.m-provider { font-size: 11px; color: #71717a; }

	.input-actions-top { display: flex; gap: 6px; }
	.icon-tool-btn {
		display: flex; align-items: center; gap: 5px;
		padding: 5px 10px; border-radius: 6px;
		background: rgba(255, 255, 255, 0.04);
		border: 1px solid rgba(255, 255, 255, 0.08);
		color: #a1a1aa; font-size: 12px; cursor: pointer;
	}
	.icon-tool-btn:hover { color: #fff; background: rgba(255, 255, 255, 0.08); }

	.input-body { margin-bottom: 10px; }
	.lobe-textarea {
		width: 100%; background: none; border: none; outline: none;
		color: #fff; font-size: 15px; font-family: inherit;
		resize: none; line-height: 1.5;
	}
	.lobe-textarea::placeholder { color: #71717a; }

	.input-footer {
		display: flex; align-items: center; justify-content: space-between;
		padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.06);
	}
	.input-footer-left { font-size: 12px; color: #71717a; display: flex; gap: 16px; }
	.privacy-badge { color: #10b981; }

	.send-btn {
		display: flex; align-items: center; gap: 8px;
		padding: 9px 18px; border-radius: 10px;
		background: linear-gradient(135deg, #10b981, #059669);
		color: #fff; font-size: 13px; font-weight: 600;
		border: none; cursor: pointer; transition: opacity 0.2s;
	}
	.send-btn:disabled { opacity: 0.4; cursor: not-allowed; }

	/* Starters */
	.starters-row {
		display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
		margin: 20px 0 40px; justify-content: center;
	}
	.starters-label { font-size: 12px; color: #71717a; }
	.starter-chip {
		display: flex; align-items: center; gap: 6px;
		padding: 6px 12px; border-radius: 100px;
		background: rgba(255, 255, 255, 0.04);
		border: 1px solid rgba(255, 255, 255, 0.08);
		color: #d4d4d8; font-size: 12px; cursor: pointer;
		transition: all 0.2s;
	}
	.starter-chip:hover {
		background: rgba(16, 185, 129, 0.12);
		border-color: rgba(16, 185, 129, 0.3); color: #34d399;
	}

	/* Stats Strip */
	.stats-strip {
		display: flex; align-items: center; justify-content: center;
		gap: 28px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.06);
	}
	.stat-box { display: flex; flex-direction: column; }
	.stat-box strong { font-size: 20px; font-weight: 700; color: #fff; }
	.stat-box span { font-size: 11px; color: #71717a; text-transform: uppercase; letter-spacing: 1px; }
	.stat-sep { width: 1px; height: 28px; background: rgba(255, 255, 255, 0.08); }

	/* ── Shared Sections ── */
	.section-container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
	.section-badge {
		font-size: 11px; font-weight: 700; letter-spacing: 2px; color: #10b981;
		margin-bottom: 12px; text-transform: uppercase;
	}
	.center { text-align: center; }
	.section-title {
		font-family: 'Syne', sans-serif; font-size: clamp(28px, 4vw, 44px);
		font-weight: 700; color: #fff; margin: 0 0 14px;
	}
	.section-subtitle {
		font-size: 16px; color: #a1a1aa; margin: 0 auto 50px; max-width: 580px;
	}

	.reveal { opacity: 0; transform: translateY(28px); transition: opacity 0.7s ease, transform 0.7s ease; }
	:global(.revealed) { opacity: 1 !important; transform: none !important; }

	/* ── Models Matrix ── */
	.models-section { padding: 100px 0; background: rgba(255, 255, 255, 0.01); }
	.models-grid {
		display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
		gap: 20px;
	}
	.model-card {
		padding: 24px; border-radius: 16px;
		background: rgba(24, 24, 27, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.08);
		transition: transform 0.2s, border-color 0.2s;
	}
	.model-card:hover {
		transform: translateY(-4px); border-color: var(--accent);
	}
	.model-card-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
	.m-badge { padding: 3px 10px; border-radius: 100px; font-size: 12px; font-weight: 600; }
	.m-dot { width: 8px; height: 8px; border-radius: 50%; }
	.m-title { font-size: 18px; font-weight: 600; color: #fff; margin: 0 0 8px; }
	.m-desc { font-size: 14px; color: #a1a1aa; line-height: 1.5; margin: 0; }

	/* ── Bento Grid ── */
	.bento-section { padding: 100px 0; }
	.bento-grid {
		display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;
	}
	.bento-card {
		padding: 28px; border-radius: 18px;
		background: rgba(24, 24, 27, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.08);
		transition: all 0.2s;
	}
	.bento-card:hover { border-color: rgba(16, 185, 129, 0.4); transform: translateY(-3px); }
	.bento-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
	.bento-icon { font-size: 28px; }
	.bento-tag {
		background: rgba(16, 185, 129, 0.12); color: #34d399;
		padding: 3px 9px; border-radius: 6px; font-size: 11px; font-weight: 600;
	}
	.bento-title { font-size: 18px; font-weight: 600; color: #fff; margin: 0 0 8px; }
	.bento-desc { font-size: 14px; color: #a1a1aa; line-height: 1.6; margin: 0; }

	/* ── Agent Marketplace ── */
	.agents-section { padding: 100px 0; background: rgba(16, 185, 129, 0.02); }
	.agents-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
	.agent-card {
		display: flex; gap: 16px; padding: 22px; border-radius: 16px;
		background: rgba(24, 24, 27, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
	}
	.agent-avatar { font-size: 36px; }
	.agent-content { flex: 1; }
	.agent-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
	.agent-name { font-size: 16px; font-weight: 600; color: #fff; margin: 0; }
	.agent-tag { background: rgba(255,255,255,0.06); color: #a1a1aa; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
	.agent-desc { font-size: 13px; color: #71717a; margin: 0 0 14px; }
	.agent-bottom { display: flex; justify-content: space-between; align-items: center; font-size: 12px; }
	.agent-stars { color: #a1a1aa; }
	.agent-use-btn { color: #34d399; font-weight: 600; }

	/* ── Pricing ── */
	.pricing-section { padding: 100px 0; }
	.billing-switcher { display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 48px; font-size: 14px; color: #a1a1aa; }
	.billing-switcher span.active { color: #fff; font-weight: 600; }
	.switch-toggle {
		width: 44px; height: 24px; border-radius: 100px; background: rgba(255,255,255,0.1);
		border: none; cursor: pointer; position: relative;
	}
	.switch-toggle.annual { background: #10b981; }
	.switch-ball {
		position: absolute; top: 2px; left: 2px; width: 20px; height: 20px;
		border-radius: 50%; background: #fff; transition: transform 0.2s;
	}
	.switch-toggle.annual .switch-ball { transform: translateX(20px); }
	.discount-badge { background: rgba(52,211,153,0.15); color: #34d399; padding: 2px 8px; border-radius: 100px; font-size: 11px; }

	.pricing-cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
	.price-card {
		position: relative; padding: 36px 28px; border-radius: 20px;
		background: rgba(24, 24, 27, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
		display: flex; flex-direction: column;
	}
	.price-card.popular {
		border-color: rgba(16, 185, 129, 0.5);
		box-shadow: 0 0 40px rgba(16, 185, 129, 0.15);
	}
	.popular-ribbon {
		position: absolute; top: -12px; left: 50%; transform: translateX(-50%);
		background: linear-gradient(135deg, #10b981, #059669); color: #fff;
		padding: 3px 14px; border-radius: 100px; font-size: 11px; font-weight: 600;
	}
	.price-title { font-size: 20px; font-weight: 700; color: #fff; margin-bottom: 4px; }
	.price-desc { font-size: 13px; color: #71717a; margin-bottom: 24px; }
	.price-amount { margin-bottom: 28px; }
	.price-amount .val { font-family: 'Syne', sans-serif; font-size: 38px; font-weight: 800; color: #fff; }
	.price-amount .unit { font-size: 13px; color: #71717a; margin-left: 4px; }
	.price-features { list-style: none; padding: 0; margin: 0 0 32px; display: flex; flex-direction: column; gap: 12px; flex: 1; }
	.price-features li { font-size: 14px; color: #a1a1aa; }
	.price-btn {
		display: flex; align-items: center; justify-content: center; padding: 12px;
		border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); color: #e4e4e7;
		font-size: 14px; font-weight: 600; transition: all 0.2s;
	}
	.price-btn:hover { border-color: rgba(16,185,129,0.4); color: #34d399; }
	.price-btn.primary { background: linear-gradient(135deg, #10b981, #059669); border: none; color: #fff; }

	/* ── FAQ ── */
	.faq-section { padding: 100px 0; }
	.faq-accordion { display: flex; flex-direction: column; gap: 10px; }
	.faq-card { border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; overflow: hidden; }
	.faq-header-btn {
		width: 100%; display: flex; justify-content: space-between; align-items: center;
		padding: 20px 24px; background: none; border: none; color: #fff;
		font-size: 16px; font-weight: 500; cursor: pointer; text-align: left;
	}
	.faq-body-text { padding: 0 24px 20px; color: #a1a1aa; font-size: 14px; line-height: 1.6; }

	/* ── Footer ── */
	.footer { padding: 60px 0 40px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: #000; }
	.footer-container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
	.footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
	.footer-desc { font-size: 13px; color: #71717a; line-height: 1.6; margin: 12px 0 20px; }
	.footer-social-row { display: flex; gap: 8px; }
	.social-chip {
		padding: 4px 10px; border-radius: 6px; background: rgba(255,255,255,0.04);
		border: 1px solid rgba(255,255,255,0.08); color: #a1a1aa; font-size: 12px;
	}
	.footer-col { display: flex; flex-direction: column; gap: 10px; }
	.footer-col-head { font-size: 12px; font-weight: 600; color: #fff; text-transform: uppercase; margin-bottom: 6px; }
	.footer-link { font-size: 13px; color: #71717a; transition: color 0.2s; }
	.footer-link:hover { color: #fff; }
	.footer-bottom-bar {
		display: flex; justify-content: space-between; font-size: 12px; color: #52525b;
		padding-top: 24px; border-top: 1px solid rgba(255, 255, 255, 0.06);
	}

	@media (max-width: 900px) {
		.bento-grid, .pricing-cards-grid, .agents-grid { grid-template-columns: 1fr; }
		.footer-grid { grid-template-columns: 1fr 1fr; }
		.nav-links { display: none; }
	}
</style>
