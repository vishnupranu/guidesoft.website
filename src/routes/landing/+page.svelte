<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';

	// ─── State ───────────────────────────────────────────────────────
	let prompt = '';
	let promptFocused = false;
	let heroLoaded = false;
	let scrollY = 0;
	let activeUseCase = 0;
	let activeFaq = -1;
	let billingAnnual = false;
	let testimonialIdx = 0;
	let canvasEl: HTMLCanvasElement;
	let animId: number;
	let particles: { x: number; y: number; vx: number; vy: number; r: number; o: number }[] = [];

	const useCases = [
		{
			tab: 'Developers', icon: '⚡',
			headline: 'Ship AI features 10× faster',
			body: 'Connect any model, build custom pipelines, and integrate REST APIs with zero config. GUIDESOFT handles the infrastructure so you focus on the product.',
			bullets: ['OpenAI-compatible REST API', 'Function calling & tool use', 'Code interpreter & RAG', 'Local model support'],
			emoji: '⚙️'
		},
		{
			tab: 'Teams', icon: '👥',
			headline: 'Collaborate on AI without limits',
			body: 'Shared workspaces, version-controlled prompts, and real-time collab. Keep your entire team on the same page — and the same model.',
			bullets: ['Shared prompt library', 'Role-based access control', 'Team analytics dashboard', 'Real-time collaboration'],
			emoji: '🤝'
		},
		{
			tab: 'Enterprise', icon: '🏢',
			headline: 'Enterprise-grade AI, on your terms',
			body: 'Deploy on-premise or in your private cloud. SSO, audit logs, compliance controls, and 99.9% uptime SLA. Your data never leaves your infrastructure.',
			bullets: ['On-premise deployment', 'SSO & SAML', 'SOC 2 compliant', 'Dedicated support'],
			emoji: '🔒'
		}
	];

	const features = [
		{ icon: '🧠', title: 'Multi-Model AI', desc: 'GPT-4o, Claude, Gemini, Llama, Mistral — switch models mid-conversation.', accent: '#7c3aed' },
		{ icon: '📚', title: 'Knowledge RAG', desc: 'Upload PDFs, docs, websites. AI answers from your data with source citations.', accent: '#2563eb' },
		{ icon: '🤖', title: 'AI Agents', desc: 'Autonomous agents that browse the web, write code, and execute multi-step tasks.', accent: '#059669' },
		{ icon: '🎙️', title: 'Voice & Vision', desc: 'Talk to your AI with real-time voice. Analyze images, charts, and screenshots.', accent: '#dc2626' },
		{ icon: '🔧', title: 'Function Calling', desc: 'Connect AI to your APIs, databases, and external tools with built-in function calling.', accent: '#d97706' },
		{ icon: '🔒', title: 'Privacy First', desc: 'Deploy locally, keep data on-premise. Zero telemetry, full encryption at rest.', accent: '#7c3aed' }
	];

	const testimonials = [
		{ name: 'Priya Nair', role: 'CTO, FinSight', avatar: 'PN', quote: 'GUIDESOFT cut our AI integration time from months to days. The multi-model support is a game changer for our research team.', stars: 5 },
		{ name: 'Marcus Chen', role: 'Lead Engineer, Devstack', avatar: 'MC', quote: "The local deployment option was a dealbreaker for us in healthcare. We're HIPAA compliant and running GPT-4 class models on our own servers.", stars: 5 },
		{ name: 'Aisha Okonkwo', role: 'Product Lead, Nexara', avatar: 'AO', quote: "Best AI platform I've used. The RAG pipeline and knowledge base made our internal docs actually useful. Team loves it.", stars: 5 },
		{ name: 'Leo Martínez', role: 'Founder, Codewise', avatar: 'LM', quote: 'Went from zero to production AI in 2 hours. The API is clean, the docs are excellent, and support actually responds.', stars: 5 }
	];

	const faqs = [
		{ q: 'What AI models does GUIDESOFT support?', a: 'GUIDESOFT supports GPT-4o, GPT-4, Claude 3.5, Gemini Pro, Llama 3, Mistral, and any OpenAI-compatible model. You can connect your own model endpoints too.' },
		{ q: 'Can I run GUIDESOFT on my own servers?', a: 'Yes. GUIDESOFT is designed for self-hosting. Deploy via Docker in minutes on any cloud or on-premise. Your data never leaves your infrastructure.' },
		{ q: 'How does pricing work?', a: 'We offer a generous free tier, then pay-as-you-go Pro and Team plans. Enterprise contracts include volume discounts, dedicated SLA, and on-premise support.' },
		{ q: 'Is there an API?', a: 'Yes — a full OpenAI-compatible REST API. Drop it into any existing codebase that already uses OpenAI, with zero code changes.' },
		{ q: 'How secure is my data?', a: 'All data is encrypted at rest and in transit. We are SOC 2 Type II certified. With self-hosting, your data never touches our servers at all.' }
	];

	const logos = ['OpenAI', 'Anthropic', 'Google', 'Meta', 'Mistral', 'Ollama', 'HuggingFace', 'LangChain'];
	const integrations = ['🐍 Python', '⚡ Node.js', '🔷 TypeScript', '☁️ AWS', '🌊 GCP', '🔵 Azure', '🐳 Docker', '⎈ Kubernetes', '🔗 LangChain', '🦜 LlamaIndex', '📊 Slack', '📧 Gmail'];

	const typingPhrases = [
		'Summarize this 50-page report',
		'Build a data pipeline with AI',
		'Analyze my sales data trends',
		'Write production-ready code',
		'Search my knowledge base',
		'Create an AI agent workflow'
	];
	let typingText = '';
	let typingPhrase = 0;
	let typingChar = 0;
	let typingDir = 1;
	let typingTimer: ReturnType<typeof setTimeout>;

	function typeNext() {
		const phrase = typingPhrases[typingPhrase];
		if (typingDir === 1) {
			typingChar++;
			typingText = phrase.slice(0, typingChar);
			if (typingChar >= phrase.length) { typingDir = -1; typingTimer = setTimeout(typeNext, 1800); return; }
		} else {
			typingChar--;
			typingText = phrase.slice(0, typingChar);
			if (typingChar <= 0) { typingDir = 1; typingPhrase = (typingPhrase + 1) % typingPhrases.length; typingTimer = setTimeout(typeNext, 300); return; }
		}
		typingTimer = setTimeout(typeNext, typingDir === 1 ? 55 : 30);
	}

	function initParticles(canvas: HTMLCanvasElement) {
		canvas.width = window.innerWidth;
		canvas.height = window.innerHeight;
		particles = Array.from({ length: 55 }, () => ({
			x: Math.random() * canvas.width, y: Math.random() * canvas.height,
			vx: (Math.random() - 0.5) * 0.3, vy: (Math.random() - 0.5) * 0.3,
			r: Math.random() * 1.5 + 0.4, o: Math.random() * 0.4 + 0.08
		}));
	}

	function drawParticles() {
		if (!canvasEl) return;
		const ctx = canvasEl.getContext('2d')!;
		ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
		particles.forEach((p) => {
			p.x += p.vx; p.y += p.vy;
			if (p.x < 0) p.x = canvasEl.width; if (p.x > canvasEl.width) p.x = 0;
			if (p.y < 0) p.y = canvasEl.height; if (p.y > canvasEl.height) p.y = 0;
			ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
			ctx.fillStyle = `rgba(167,139,250,${p.o})`; ctx.fill();
		});
		for (let i = 0; i < particles.length; i++) {
			for (let j = i + 1; j < particles.length; j++) {
				const dx = particles[i].x - particles[j].x, dy = particles[i].y - particles[j].y;
				const d = Math.sqrt(dx * dx + dy * dy);
				if (d < 100) {
					ctx.beginPath(); ctx.moveTo(particles[i].x, particles[i].y); ctx.lineTo(particles[j].x, particles[j].y);
					ctx.strokeStyle = `rgba(124,58,237,${0.12 * (1 - d / 100)})`; ctx.lineWidth = 0.5; ctx.stroke();
				}
			}
		}
		animId = requestAnimationFrame(drawParticles);
	}

	function handlePromptSubmit() {
		if (!prompt.trim()) return;
		goto(`/auth?next=chat&prompt=${encodeURIComponent(prompt.trim())}`);
	}

	function observeReveal() {
		const io = new IntersectionObserver((entries) => {
			entries.forEach((e) => { if (e.isIntersecting) { (e.target as HTMLElement).classList.add('revealed'); io.unobserve(e.target); } });
		}, { threshold: 0.1 });
		document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
	}

	let testimonialTimer: ReturnType<typeof setInterval>;

	onMount(() => {
		heroLoaded = true;
		if (canvasEl) { initParticles(canvasEl); drawParticles(); }
		window.addEventListener('resize', () => { if (canvasEl) { canvasEl.width = window.innerWidth; canvasEl.height = window.innerHeight; initParticles(canvasEl); } });
		setTimeout(typeNext, 800);
		setTimeout(observeReveal, 100);
		testimonialTimer = setInterval(() => { testimonialIdx = (testimonialIdx + 1) % testimonials.length; }, 4500);
	});

	onDestroy(() => { cancelAnimationFrame(animId); clearTimeout(typingTimer); clearInterval(testimonialTimer); });
</script>

<svelte:head>
	<title>GUIDESOFT.WEB — The AI Platform for Everyone</title>
	<meta name="description" content="Build, automate and collaborate with AI. GUIDESOFT supports GPT-4, Claude, Gemini, Llama and more." />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@600;700;800&display=swap" rel="stylesheet" />
</svelte:head>

<svelte:window bind:scrollY />

<div class="landing">

	<!-- ══ HERO ══ -->
	<section class="hero" id="hero">
		<canvas class="hero-canvas" bind:this={canvasEl}></canvas>
		<div class="orb orb-1"></div>
		<div class="orb orb-2"></div>
		<div class="orb orb-3"></div>
		<div class="hero-grid"></div>

		<nav class="nav" class:nav-scrolled={scrollY > 40}>
			<div class="nav-inner">
				<a href="/landing" class="nav-logo">
					<div class="nav-logo-mark">G</div>
					<span class="nav-logo-text">GUIDESOFT<span class="nav-logo-dot">.WEB</span></span>
				</a>
				<div class="nav-links">
					<a href="#features" class="nav-link">Features</a>
					<a href="#how-it-works" class="nav-link">How it works</a>
					<a href="#pricing" class="nav-link">Pricing</a>
					<a href="#faq" class="nav-link">FAQ</a>
				</div>
				<div class="nav-actions">
					<a href="/auth" class="btn-ghost">Sign In</a>
					<a href="/auth?mode=signup" class="btn-primary-sm">Get Started</a>
				</div>
			</div>
		</nav>

		<div class="hero-content" class:loaded={heroLoaded}>
			<div class="hero-badge"><span class="badge-dot"></span>Now with GPT-4o, Claude 3.5 &amp; Gemini Pro</div>
			<h1 class="hero-heading">The AI Platform<br /><span class="gradient-text">Built for Everyone</span></h1>
			<p class="hero-sub">Build · Automate · Collaborate with AI.<br />Connect any model. Ship in minutes.</p>

			<div class="hero-prompt-wrap" class:focused={promptFocused}>
				<div class="prompt-icon">✦</div>
				<input
					bind:value={prompt}
					on:focus={() => (promptFocused = true)}
					on:blur={() => (promptFocused = false)}
					on:keydown={(e) => e.key === 'Enter' && handlePromptSubmit()}
					class="hero-prompt-input"
					placeholder={typingText || 'Ask anything or describe what you want to build…'}
					id="hero-prompt"
					autocomplete="off"
				/>
				<button class="prompt-submit" on:click={handlePromptSubmit} id="hero-prompt-submit">
					<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
				</button>
			</div>
			<p class="prompt-hint">Press Enter to get started — no account required to explore</p>

			<div class="hero-cta">
				<a href="/auth?mode=signup" class="btn-primary" id="hero-cta-signup">Get Started Free</a>
				<a href="#how-it-works" class="btn-outline" id="hero-cta-demo">See How It Works ↓</a>
			</div>

			<div class="hero-stats">
				<div class="stat"><strong>50K+</strong><span>Teams</span></div>
				<div class="stat-divider"></div>
				<div class="stat"><strong>12+</strong><span>AI Models</span></div>
				<div class="stat-divider"></div>
				<div class="stat"><strong>99.9%</strong><span>Uptime</span></div>
				<div class="stat-divider"></div>
				<div class="stat"><strong>∞</strong><span>Integrations</span></div>
			</div>
		</div>
		<div class="scroll-hint"><div class="scroll-dot"></div></div>
	</section>

	<!-- ══ TRUSTED BY ══ -->
	<section class="trusted">
		<p class="trusted-label">Trusted by teams at</p>
		<div class="ticker-wrap">
			<div class="ticker-track">
				{#each [...logos, ...logos] as logo}<div class="ticker-item">{logo}</div>{/each}
			</div>
		</div>
	</section>

	<!-- ══ WHAT IS GUIDESOFT ══ -->
	<section class="what-is reveal" id="about">
		<div class="container">
			<div class="what-grid">
				<div class="what-left">
					<div class="eyebrow">WHAT IS GUIDESOFT</div>
					<h2 class="sec-h">Your AI command center — everything in one place</h2>
					<p class="sec-p">GUIDESOFT is an open-source AI platform that brings together the world's best language models, knowledge management, and automation tools into a single, beautiful interface.</p>
					<p class="sec-p">Whether you're a solo developer, a growing team, or an enterprise — GUIDESOFT adapts to your workflow and scales with your ambitions.</p>
					<div class="pills">
						{#each ['Open Source', 'Self-Hostable', 'API-First', 'Privacy-Focused'] as p}
							<span class="pill">{p}</span>
						{/each}
					</div>
				</div>
				<div class="what-right">
					<div class="ui-mock">
						<div class="ui-mock-header">
							<div class="ui-dots"><span></span><span></span><span></span></div>
							<span class="ui-title-label">GUIDESOFT.WEB</span>
						</div>
						<div class="ui-mock-body">
							<div class="ui-msg user">What's the revenue trend for Q2 2024?</div>
							<div class="ui-msg bot">
								<div class="model-tag">GPT-4o</div>
								Based on your uploaded data, Q2 revenue grew <strong>34%</strong> YoY with strong performance in March and June...
								<div class="mini-chart">
									{#each [45, 60, 52, 80, 95] as h, i}
										<div class="mini-bar" class:hi={i === 4} style="height:{h}%"></div>
									{/each}
								</div>
							</div>
							<div class="ui-input"><span>Ask a follow-up...</span><span class="send">↑</span></div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- ══ FEATURES ══ -->
	<section class="features reveal" id="features">
		<div class="container">
			<div class="eyebrow center">CAPABILITIES</div>
			<h2 class="sec-h center">Everything you need to build with AI</h2>
			<p class="sec-p center" style="max-width:560px;margin:0 auto 48px;">Six core pillars that make GUIDESOFT the most complete AI platform available.</p>
			<div class="feat-grid">
				{#each features as f, i}
					<div class="feat-card" style="--a:{f.accent}; animation-delay:{i*80}ms">
						<div class="feat-icon">{f.icon}</div>
						<h3 class="feat-title">{f.title}</h3>
						<p class="feat-desc">{f.desc}</p>
						<div class="feat-glow"></div>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ══ HOW IT WORKS ══ -->
	<section class="how reveal" id="how-it-works">
		<div class="container">
			<div class="eyebrow center">HOW IT WORKS</div>
			<h2 class="sec-h center">From zero to AI-powered in minutes</h2>
			<div class="steps">
				<div class="step">
					<div class="step-num">01</div>
					<div class="step-icon">🔑</div>
					<h3 class="step-t">Connect your models</h3>
					<p class="step-d">Add your OpenAI, Anthropic, or Ollama key. Or use GUIDESOFT's built-in models. Zero config required.</p>
				</div>
				<div class="step-arr">→</div>
				<div class="step">
					<div class="step-num">02</div>
					<div class="step-icon">📁</div>
					<h3 class="step-t">Upload your knowledge</h3>
					<p class="step-d">Drop in PDFs, documents, websites, or databases. AI instantly searches and cites from your data.</p>
				</div>
				<div class="step-arr">→</div>
				<div class="step">
					<div class="step-num">03</div>
					<div class="step-icon">🚀</div>
					<h3 class="step-t">Build &amp; ship</h3>
					<p class="step-d">Create agents, automate workflows, embed in your app via API. Share with your team in one click.</p>
				</div>
			</div>
		</div>
	</section>

	<!-- ══ AI CAPABILITIES ══ -->
	<section class="caps reveal" id="capabilities">
		<div class="container">
			<div class="caps-grid">
				<div class="caps-left">
					<div class="eyebrow">AI CAPABILITIES</div>
					<h2 class="sec-h">The full spectrum of modern AI</h2>
					{#each [
						{ i: '💬', t: 'Chat & Conversation', d: 'Multi-turn conversations with memory, context windows up to 200K tokens' },
						{ i: '🔍', t: 'RAG & Search', d: 'Semantic search over your documents with source citations and confidence scores' },
						{ i: '🤖', t: 'Autonomous Agents', d: 'Multi-step task execution, web browsing, code running, API calling' },
						{ i: '🎙️', t: 'Voice & Vision', d: 'Real-time speech-to-text, image analysis and OCR' }
					] as cap}
						<div class="cap-row">
							<span class="cap-i">{cap.i}</span>
							<div><div class="cap-t">{cap.t}</div><div class="cap-d">{cap.d}</div></div>
						</div>
					{/each}
				</div>
				<div class="caps-right">
					<div class="models-box">
						<div class="models-lbl">Supported Models</div>
						<div class="models-wrap">
							{#each ['GPT-4o', 'Claude 3.5', 'Gemini Pro', 'Llama 3', 'Mistral', 'Phi-3', 'Qwen', 'Deepseek'] as m}
								<div class="model-chip">{m}</div>
							{/each}
						</div>
						<div class="models-note">+ Any OpenAI-compatible endpoint</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- ══ USE CASES ══ -->
	<section class="uc reveal" id="use-cases">
		<div class="container">
			<div class="eyebrow center">USE CASES</div>
			<h2 class="sec-h center">Built for how you work</h2>
			<div class="uc-tabs">
				{#each useCases as uc, i}
					<button class="uc-tab" class:active={activeUseCase === i} on:click={() => (activeUseCase = i)} id="uc-tab-{i}">{uc.icon} {uc.tab}</button>
				{/each}
			</div>
			<div class="uc-panel">
				<div class="uc-text">
					<h3 class="uc-h">{useCases[activeUseCase].headline}</h3>
					<p class="uc-p">{useCases[activeUseCase].body}</p>
					<ul class="uc-list">{#each useCases[activeUseCase].bullets as b}<li>✓ {b}</li>{/each}</ul>
					<a href="/auth?mode=signup" class="btn-primary">Start Building →</a>
				</div>
				<div class="uc-vis"><div class="uc-emoji">{useCases[activeUseCase].emoji}</div></div>
			</div>
		</div>
	</section>

	<!-- ══ INTEGRATIONS ══ -->
	<section class="integ reveal" id="integrations">
		<div class="container">
			<div class="eyebrow center">INTEGRATIONS</div>
			<h2 class="sec-h center">Works with your entire stack</h2>
			<div class="integ-grid">
				{#each integrations as ig}<div class="integ-chip">{ig}</div>{/each}
			</div>
			<p class="integ-note">Full OpenAI-compatible REST API — drop GUIDESOFT into any codebase with <strong>zero code changes</strong>.</p>
		</div>
	</section>

	<!-- ══ TESTIMONIALS ══ -->
	<section class="testi reveal" id="testimonials">
		<div class="container">
			<div class="eyebrow center">TESTIMONIALS</div>
			<h2 class="sec-h center">Loved by builders worldwide</h2>
			<div class="testi-carousel">
				{#each testimonials as t, i}
					<div class="testi-card" class:active={testimonialIdx === i} class:prev={testimonialIdx === (i + 1) % testimonials.length}>
						<div class="stars">{'★'.repeat(t.stars)}</div>
						<p class="t-q">"{t.quote}"</p>
						<div class="t-auth">
							<div class="t-av">{t.avatar}</div>
							<div><div class="t-name">{t.name}</div><div class="t-role">{t.role}</div></div>
						</div>
					</div>
				{/each}
			</div>
			<div class="testi-dots">
				{#each testimonials as _, i}
					<button class="tdot" class:active={testimonialIdx === i} on:click={() => (testimonialIdx = i)} id="tdot-{i}"></button>
				{/each}
			</div>
		</div>
	</section>

	<!-- ══ PRICING ══ -->
	<section class="pricing reveal" id="pricing">
		<div class="container">
			<div class="eyebrow center">PRICING</div>
			<h2 class="sec-h center">Start free. Scale as you grow.</h2>
			<div class="bill-toggle">
				<span class:on={!billingAnnual}>Monthly</span>
				<button class="toggle" class:annual={billingAnnual} on:click={() => (billingAnnual = !billingAnnual)} id="billing-toggle">
					<span class="thumb"></span>
				</button>
				<span class:on={billingAnnual}>Annual <span class="save">Save 30%</span></span>
			</div>
			<div class="plan-grid">
				<div class="plan">
					<div class="plan-name">Starter</div>
					<div class="plan-desc">For individuals exploring AI</div>
					<div class="plan-price"><span class="pa">$0</span><span class="pp">/mo</span></div>
					<ul class="plan-list">
						<li>✓ 100 messages/day</li><li>✓ GPT-3.5, Llama 3</li>
						<li>✓ 3 knowledge bases</li><li>✓ 1 GB storage</li><li>✓ Community support</li>
					</ul>
					<a href="/auth?mode=signup" class="plan-btn" id="plan-free">Get Started Free</a>
				</div>
				<div class="plan featured">
					<div class="plan-badge">Most Popular</div>
					<div class="plan-name">Pro</div>
					<div class="plan-desc">For power users and teams</div>
					<div class="plan-price"><span class="pa">{billingAnnual ? '$14' : '$20'}</span><span class="pp">/mo</span></div>
					<ul class="plan-list">
						<li>✓ Unlimited messages</li><li>✓ All models (GPT-4o, Claude)</li>
						<li>✓ Unlimited knowledge bases</li><li>✓ 100 GB storage</li>
						<li>✓ API access</li><li>✓ Priority support</li>
					</ul>
					<a href="/auth?mode=signup&plan=pro" class="plan-btn primary" id="plan-pro">Start Pro Trial</a>
				</div>
				<div class="plan">
					<div class="plan-name">Enterprise</div>
					<div class="plan-desc">For organizations at scale</div>
					<div class="plan-price"><span class="pa">Custom</span></div>
					<ul class="plan-list">
						<li>✓ Unlimited everything</li><li>✓ On-premise deployment</li>
						<li>✓ SSO &amp; SAML</li><li>✓ SOC 2 compliance</li>
						<li>✓ SLA guarantee</li><li>✓ Dedicated support</li>
					</ul>
					<a href="/auth?mode=signup&plan=enterprise" class="plan-btn" id="plan-enterprise">Contact Sales</a>
				</div>
			</div>
		</div>
	</section>

	<!-- ══ FAQ ══ -->
	<section class="faq reveal" id="faq">
		<div class="container" style="max-width:780px">
			<div class="eyebrow center">FAQ</div>
			<h2 class="sec-h center">Common questions</h2>
			<div class="faq-list">
				{#each faqs as f, i}
					<div class="faq-item" class:open={activeFaq === i}>
						<button class="faq-q" on:click={() => (activeFaq = activeFaq === i ? -1 : i)} id="faq-{i}">
							<span>{f.q}</span><span class="faq-ch">{activeFaq === i ? '−' : '+'}</span>
						</button>
						{#if activeFaq === i}<div class="faq-a">{f.a}</div>{/if}
					</div>
				{/each}
			</div>
		</div>
	</section>

	<!-- ══ CTA + FOOTER ══ -->
	<section class="cta-sec reveal" id="cta">
		<div class="container">
			<div class="cta-box">
				<div class="cta-orb"></div>
				<div class="eyebrow center" style="color:#a78bfa">GET STARTED</div>
				<h2 class="cta-h">Ready to build with AI?</h2>
				<p class="cta-sub">Join 50,000+ teams already using GUIDESOFT. Start free — no credit card required.</p>
				<div class="cta-btns">
					<a href="/auth?mode=signup" class="btn-primary large" id="cta-main">Start for Free →</a>
					<a href="/auth" class="btn-ghost-l" id="cta-signin">Sign In</a>
				</div>
			</div>
		</div>
	</section>

	<footer class="footer">
		<div class="container">
			<div class="foot-grid">
				<div class="foot-brand">
					<div class="foot-logo">
						<div class="nav-logo-mark sm">G</div>
						<span>GUIDESOFT<span class="nav-logo-dot">.WEB</span></span>
					</div>
					<p class="foot-tag">The AI Platform for Everyone.<br />Open source. Self-hostable.</p>
					<a href="https://github.com/vishnupranu/guidesoft.website" target="_blank" class="gh-link">GitHub →</a>
				</div>
				<div class="foot-col">
					<div class="foot-title">Product</div>
					<a href="#features" class="foot-link">Features</a>
					<a href="#pricing" class="foot-link">Pricing</a>
					<a href="#integrations" class="foot-link">Integrations</a>
					<a href="/auth" class="foot-link">Sign In</a>
				</div>
				<div class="foot-col">
					<div class="foot-title">Developers</div>
					<a href="/auth" class="foot-link">API Reference</a>
					<a href="#" class="foot-link">Documentation</a>
					<a href="#" class="foot-link">SDKs</a>
					<a href="#" class="foot-link">Open Source</a>
				</div>
				<div class="foot-col">
					<div class="foot-title">Company</div>
					<a href="#" class="foot-link">About</a>
					<a href="#" class="foot-link">Blog</a>
					<a href="#" class="foot-link">Privacy Policy</a>
					<a href="#" class="foot-link">Terms</a>
				</div>
			</div>
			<div class="foot-bottom">
				<span>© 2024 GUIDESOFT.WEB. All rights reserved.</span>
				<span>Made with ✦ for the AI generation</span>
			</div>
		</div>
	</footer>

</div>

<style>
:global(body){margin:0;padding:0;background:#080810;color:#e2e2ef;font-family:'Inter',system-ui,sans-serif;overflow-x:hidden;}
:global(*){box-sizing:border-box;}
:global(a){text-decoration:none;}
.landing{width:100%;}

/* ── Shared ── */
.container{max-width:1200px;margin:0 auto;padding:0 24px;}
.eyebrow{font-size:11px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#7c3aed;margin-bottom:12px;}
.center{text-align:center;}
.sec-h{font-family:'Syne',sans-serif;font-size:clamp(26px,4vw,46px);font-weight:700;line-height:1.15;color:#f0f0ff;margin:0 0 16px;}
.sec-p{font-size:16px;color:#7777aa;line-height:1.7;margin:0 0 20px;}
.gradient-text{background:linear-gradient(135deg,#a78bfa 0%,#60a5fa 50%,#34d399 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.reveal{opacity:0;transform:translateY(28px);transition:opacity 0.7s ease,transform 0.7s ease;}
:global(.revealed){opacity:1!important;transform:none!important;}
.pill{display:inline-flex;align-items:center;background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3);color:#a78bfa;padding:5px 13px;border-radius:100px;font-size:13px;font-weight:500;margin:3px;}
.pills{display:flex;flex-wrap:wrap;gap:6px;margin-top:20px;}

/* ── Buttons ── */
.btn-primary{display:inline-flex;align-items:center;background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;border:none;padding:14px 28px;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;transition:all 0.2s;box-shadow:0 0 24px rgba(124,58,237,0.35);}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 0 36px rgba(124,58,237,0.55);}
.btn-primary.large{padding:16px 36px;font-size:16px;}
.btn-primary-sm{display:inline-flex;align-items:center;background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;padding:9px 18px;border-radius:8px;font-size:14px;font-weight:600;transition:all 0.2s;}
.btn-primary-sm:hover{transform:translateY(-1px);}
.btn-outline{display:inline-flex;align-items:center;border:1px solid rgba(255,255,255,0.15);color:#c4c4d8;padding:14px 28px;border-radius:10px;font-size:15px;font-weight:500;transition:all 0.2s;}
.btn-outline:hover{border-color:rgba(167,139,250,0.5);color:#a78bfa;}
.btn-ghost{color:#9999bb;font-size:14px;font-weight:500;padding:8px 14px;border-radius:8px;transition:color 0.2s;}
.btn-ghost:hover{color:#e0e0f0;}
.btn-ghost-l{color:#c4c4d8;font-size:16px;font-weight:500;padding:14px 24px;border-radius:10px;border:1px solid rgba(255,255,255,0.12);transition:all 0.2s;}
.btn-ghost-l:hover{border-color:rgba(167,139,250,0.4);}

/* ── HERO ── */
.hero{position:relative;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;background:radial-gradient(ellipse 80% 60% at 50% -10%,rgba(124,58,237,0.25) 0%,transparent 70%),#080810;}
.hero-canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1;}
.orb{position:absolute;border-radius:50%;filter:blur(80px);pointer-events:none;z-index:0;}
.orb-1{width:600px;height:600px;background:radial-gradient(circle,rgba(124,58,237,0.18) 0%,transparent 70%);top:-200px;left:-100px;animation:f1 8s ease-in-out infinite;}
.orb-2{width:500px;height:500px;background:radial-gradient(circle,rgba(37,99,235,0.14) 0%,transparent 70%);bottom:-150px;right:-100px;animation:f2 10s ease-in-out infinite;}
.orb-3{width:300px;height:300px;background:radial-gradient(circle,rgba(52,211,153,0.1) 0%,transparent 70%);top:40%;left:60%;animation:f3 12s ease-in-out infinite;}
@keyframes f1{0%,100%{transform:translate(0,0);}50%{transform:translate(30px,20px);}}
@keyframes f2{0%,100%{transform:translate(0,0);}50%{transform:translate(-20px,-30px);}}
@keyframes f3{0%,100%{transform:translate(0,0);}50%{transform:translate(15px,-15px);}}
.hero-grid{position:absolute;inset:0;z-index:1;background-image:linear-gradient(rgba(124,58,237,0.06) 1px,transparent 1px),linear-gradient(90deg,rgba(124,58,237,0.06) 1px,transparent 1px);background-size:60px 60px;mask-image:radial-gradient(ellipse 80% 70% at 50% 50%,black 30%,transparent 80%);}

/* Nav */
.nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:20px 32px;transition:background 0.3s,backdrop-filter 0.3s;}
.nav-scrolled{background:rgba(8,8,16,0.85);backdrop-filter:blur(20px);border-bottom:1px solid rgba(124,58,237,0.12);}
.nav-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:32px;}
.nav-logo{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:700;color:#f0f0ff;}
.nav-logo-mark{width:32px;height:32px;background:linear-gradient(135deg,#7c3aed,#a78bfa);border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;color:#fff;}
.nav-logo-mark.sm{width:28px;height:28px;font-size:14px;}
.nav-logo-text{font-family:'Syne',sans-serif;}
.nav-logo-dot{color:#7c3aed;}
.nav-links{display:flex;gap:4px;flex:1;justify-content:center;}
.nav-link{padding:7px 14px;border-radius:8px;color:#9999bb;font-size:14px;font-weight:500;transition:color 0.2s,background 0.2s;}
.nav-link:hover{color:#e0e0f0;background:rgba(255,255,255,0.05);}
.nav-actions{display:flex;align-items:center;gap:8px;}

/* Hero content */
.hero-content{position:relative;z-index:10;display:flex;flex-direction:column;align-items:center;text-align:center;padding:100px 24px 60px;max-width:860px;opacity:0;transform:translateY(24px);transition:opacity 0.8s ease,transform 0.8s ease;}
.hero-content.loaded{opacity:1;transform:none;}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.35);color:#a78bfa;padding:7px 16px;border-radius:100px;font-size:13px;font-weight:500;margin-bottom:28px;}
.badge-dot{width:6px;height:6px;border-radius:50%;background:#7c3aed;box-shadow:0 0 8px #7c3aed;animation:pulse 2s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.4;}}
.hero-heading{font-family:'Syne',sans-serif;font-size:clamp(42px,7vw,80px);font-weight:800;line-height:1.1;color:#f0f0ff;margin:0 0 20px;}
.hero-sub{font-size:clamp(17px,2.5vw,21px);color:#7777aa;line-height:1.6;margin:0 0 36px;}

/* Prompt box */
.hero-prompt-wrap{display:flex;align-items:center;width:100%;max-width:680px;background:rgba(255,255,255,0.04);border:1.5px solid rgba(124,58,237,0.25);border-radius:14px;padding:10px 12px 10px 16px;gap:12px;transition:border-color 0.2s,box-shadow 0.2s;margin-bottom:12px;}
.hero-prompt-wrap.focused{border-color:rgba(124,58,237,0.7);box-shadow:0 0 0 4px rgba(124,58,237,0.1),0 0 40px rgba(124,58,237,0.15);}
.prompt-icon{color:#7c3aed;font-size:18px;flex-shrink:0;}
.hero-prompt-input{flex:1;background:none;border:none;outline:none;color:#e2e2ef;font-size:16px;font-family:'Inter',sans-serif;padding:6px 0;}
.hero-prompt-input::placeholder{color:rgba(120,120,170,0.7);}
.prompt-submit{width:42px;height:42px;border-radius:10px;background:linear-gradient(135deg,#7c3aed,#6d28d9);border:none;cursor:pointer;color:#fff;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all 0.2s;box-shadow:0 0 16px rgba(124,58,237,0.4);}
.prompt-submit:hover{transform:scale(1.08);box-shadow:0 0 24px rgba(124,58,237,0.6);}
.prompt-hint{font-size:12px;color:#555577;margin:0 0 32px;}
.hero-cta{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin-bottom:48px;}
.hero-stats{display:flex;align-items:center;gap:24px;flex-wrap:wrap;justify-content:center;}
.stat{display:flex;flex-direction:column;align-items:center;}
.stat strong{font-size:22px;font-weight:700;color:#f0f0ff;}
.stat span{font-size:12px;color:#6666aa;text-transform:uppercase;letter-spacing:1px;}
.stat-divider{width:1px;height:32px;background:rgba(255,255,255,0.1);}
.scroll-hint{position:absolute;bottom:32px;left:50%;transform:translateX(-50%);z-index:10;}
.scroll-dot{width:6px;height:30px;border:2px solid rgba(124,58,237,0.5);border-radius:10px;position:relative;overflow:hidden;}
.scroll-dot::after{content:'';position:absolute;top:4px;left:50%;transform:translateX(-50%);width:2px;height:8px;background:#7c3aed;border-radius:2px;animation:sd 2s ease-in-out infinite;}
@keyframes sd{0%,100%{transform:translateX(-50%) translateY(0);opacity:1;}80%{transform:translateX(-50%) translateY(12px);opacity:0;}}

/* ── TRUSTED ── */
.trusted{padding:40px 0;border-top:1px solid rgba(255,255,255,0.06);border-bottom:1px solid rgba(255,255,255,0.06);overflow:hidden;}
.trusted-label{text-align:center;font-size:12px;color:#5555aa;letter-spacing:2px;text-transform:uppercase;margin:0 0 20px;}
.ticker-wrap{overflow:hidden;}
.ticker-track{display:flex;width:max-content;animation:tick 25s linear infinite;}
.ticker-item{padding:8px 40px;font-size:15px;font-weight:600;color:#4444aa;border-right:1px solid rgba(124,58,237,0.12);white-space:nowrap;transition:color 0.3s;}
.ticker-item:hover{color:#a78bfa;}
@keyframes tick{from{transform:translateX(0);}to{transform:translateX(-50%);}}

/* ── WHAT IS ── */
.what-is{padding:100px 0;}
.what-grid{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center;}
.what-left .sec-p{color:#7777aa;margin-bottom:12px;}
.ui-mock{background:rgba(255,255,255,0.03);border:1px solid rgba(124,58,237,0.2);border-radius:16px;overflow:hidden;box-shadow:0 0 60px rgba(124,58,237,0.12);}
.ui-mock-header{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid rgba(124,58,237,0.1);background:rgba(124,58,237,0.05);}
.ui-dots{display:flex;gap:6px;}
.ui-dots span{width:10px;height:10px;border-radius:50%;}
.ui-dots span:nth-child(1){background:#ff5f57;}
.ui-dots span:nth-child(2){background:#febc2e;}
.ui-dots span:nth-child(3){background:#28c840;}
.ui-title-label{font-size:13px;color:#6666aa;margin:0 auto;}
.ui-mock-body{padding:20px;display:flex;flex-direction:column;gap:14px;}
.ui-msg{padding:12px 16px;border-radius:12px;font-size:14px;line-height:1.5;}
.ui-msg.user{background:rgba(124,58,237,0.2);color:#d4c4fa;border:1px solid rgba(124,58,237,0.3);align-self:flex-end;max-width:85%;}
.ui-msg.bot{background:rgba(255,255,255,0.04);color:#aaaacc;border:1px solid rgba(255,255,255,0.08);}
.model-tag{display:inline-flex;background:rgba(124,58,237,0.2);color:#a78bfa;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600;margin-bottom:8px;}
.mini-chart{display:flex;align-items:flex-end;gap:4px;height:48px;margin-top:12px;}
.mini-bar{flex:1;background:rgba(124,58,237,0.3);border-radius:3px 3px 0 0;}
.mini-bar.hi{background:#7c3aed;box-shadow:0 0 12px rgba(124,58,237,0.5);}
.ui-input{display:flex;align-items:center;justify-content:space-between;padding:8px 12px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:8px;font-size:13px;color:#4444aa;}
.send{width:24px;height:24px;background:#7c3aed;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;}

/* ── FEATURES ── */
.features{padding:100px 0;}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:48px;}
.feat-card{position:relative;overflow:hidden;padding:28px;border-radius:16px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);transition:all 0.3s;cursor:default;}
.feat-card:hover{border-color:var(--a);box-shadow:0 0 30px rgba(0,0,0,0.3),0 0 1px var(--a);transform:translateY(-4px);}
.feat-icon{font-size:28px;margin-bottom:14px;}
.feat-title{font-size:17px;font-weight:600;color:#e0e0f0;margin:0 0 8px;}
.feat-desc{font-size:14px;color:#6666aa;line-height:1.6;margin:0;}
.feat-glow{position:absolute;bottom:-30px;right:-30px;width:100px;height:100px;border-radius:50%;background:var(--a);opacity:0;filter:blur(40px);transition:opacity 0.3s;}
.feat-card:hover .feat-glow{opacity:0.18;}

/* ── HOW IT WORKS ── */
.how{padding:100px 0;}
.steps{display:flex;align-items:flex-start;justify-content:center;margin-top:60px;}
.step{flex:1;max-width:280px;display:flex;flex-direction:column;align-items:center;text-align:center;}
.step-num{font-family:'Syne',sans-serif;font-size:48px;font-weight:800;color:rgba(124,58,237,0.15);line-height:1;margin-bottom:-10px;}
.step-icon{width:64px;height:64px;border-radius:16px;background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3);display:flex;align-items:center;justify-content:center;font-size:26px;margin-bottom:20px;position:relative;z-index:1;}
.step-t{font-size:18px;font-weight:600;color:#e0e0f0;margin:0 0 10px;}
.step-d{font-size:14px;color:#6666aa;line-height:1.6;margin:0;}
.step-arr{font-size:24px;color:rgba(124,58,237,0.4);align-self:center;padding:0 20px;margin-top:-20px;}

/* ── AI CAPABILITIES ── */
.caps{padding:100px 0;background:rgba(124,58,237,0.03);}
.caps-grid{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center;}
.cap-row{display:flex;gap:16px;align-items:flex-start;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.05);}
.cap-i{font-size:22px;flex-shrink:0;}
.cap-t{font-size:15px;font-weight:600;color:#e0e0f0;margin-bottom:4px;}
.cap-d{font-size:13px;color:#5555aa;line-height:1.5;}
.models-box{background:rgba(255,255,255,0.03);border:1px solid rgba(124,58,237,0.2);border-radius:20px;padding:32px;}
.models-lbl{font-size:12px;color:#7c3aed;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px;}
.models-wrap{display:flex;flex-wrap:wrap;gap:10px;}
.model-chip{padding:8px 16px;border-radius:100px;background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.25);color:#a78bfa;font-size:13px;font-weight:500;transition:all 0.2s;}
.model-chip:hover{background:rgba(124,58,237,0.25);transform:scale(1.04);}
.models-note{font-size:12px;color:#4444aa;margin-top:16px;}

/* ── USE CASES ── */
.uc{padding:100px 0;}
.uc-tabs{display:flex;gap:8px;justify-content:center;margin:40px 0 48px;flex-wrap:wrap;}
.uc-tab{padding:10px 24px;border-radius:100px;border:1px solid rgba(255,255,255,0.1);background:transparent;color:#6666aa;font-size:14px;font-weight:500;cursor:pointer;transition:all 0.2s;font-family:'Inter',sans-serif;}
.uc-tab.active,.uc-tab:hover{background:rgba(124,58,237,0.2);border-color:rgba(124,58,237,0.5);color:#a78bfa;}
.uc-panel{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;}
.uc-h{font-family:'Syne',sans-serif;font-size:30px;font-weight:700;color:#f0f0ff;margin:0 0 16px;}
.uc-p{font-size:16px;color:#6666aa;line-height:1.7;margin:0 0 24px;}
.uc-list{list-style:none;padding:0;margin:0 0 32px;display:flex;flex-direction:column;gap:10px;}
.uc-list li{font-size:14px;color:#8888aa;}
.uc-vis{display:flex;align-items:center;justify-content:center;aspect-ratio:1;max-width:280px;margin:0 auto;background:radial-gradient(circle,rgba(124,58,237,0.15) 0%,transparent 70%);border-radius:50%;}
.uc-emoji{font-size:72px;}

/* ── INTEGRATIONS ── */
.integ{padding:100px 0;}
.integ-grid{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:40px 0;}
.integ-chip{padding:10px 20px;border-radius:10px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#8888aa;font-size:14px;font-weight:500;transition:all 0.2s;}
.integ-chip:hover{background:rgba(124,58,237,0.1);border-color:rgba(124,58,237,0.3);color:#a78bfa;transform:translateY(-2px);}
.integ-note{text-align:center;color:#5555aa;font-size:15px;}
.integ-note strong{color:#a78bfa;}

/* ── TESTIMONIALS ── */
.testi{padding:100px 0;}
.testi-carousel{position:relative;height:240px;margin:40px 0 24px;overflow:hidden;}
.testi-card{position:absolute;inset:0;max-width:700px;margin:0 auto;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:36px;opacity:0;transform:translateX(40px);transition:all 0.5s ease;pointer-events:none;}
.testi-card.active{opacity:1;transform:none;pointer-events:auto;}
.testi-card.prev{opacity:0;transform:translateX(-40px);}
.stars{color:#7c3aed;font-size:18px;margin-bottom:16px;}
.t-q{font-size:17px;color:#c4c4da;line-height:1.65;margin:0 0 24px;font-style:italic;}
.t-auth{display:flex;align-items:center;gap:14px;}
.t-av{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#7c3aed,#2563eb);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;color:#fff;flex-shrink:0;}
.t-name{font-size:14px;font-weight:600;color:#e0e0f0;}
.t-role{font-size:12px;color:#5555aa;}
.testi-dots{display:flex;gap:8px;justify-content:center;}
.tdot{width:8px;height:8px;border-radius:50%;border:none;cursor:pointer;background:rgba(124,58,237,0.25);transition:all 0.2s;}
.tdot.active{background:#7c3aed;transform:scale(1.4);}

/* ── PRICING ── */
.pricing{padding:100px 0;background:rgba(124,58,237,0.03);}
.bill-toggle{display:flex;align-items:center;gap:14px;justify-content:center;margin:32px 0 48px;font-size:14px;color:#6666aa;}
.bill-toggle span.on{color:#e0e0f0;font-weight:600;}
.toggle{width:48px;height:26px;border-radius:100px;background:rgba(255,255,255,0.1);border:none;cursor:pointer;position:relative;transition:background 0.2s;}
.toggle.annual{background:#7c3aed;}
.thumb{position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff;transition:transform 0.2s;}
.toggle.annual .thumb{transform:translateX(22px);}
.save{background:rgba(52,211,153,0.15);border:1px solid rgba(52,211,153,0.3);color:#34d399;padding:2px 8px;border-radius:100px;font-size:11px;font-weight:600;margin-left:6px;}
.plan-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;}
.plan{position:relative;padding:36px 32px;border-radius:20px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);display:flex;flex-direction:column;}
.plan.featured{border-color:rgba(124,58,237,0.5);background:rgba(124,58,237,0.08);box-shadow:0 0 40px rgba(124,58,237,0.15);}
.plan-badge{position:absolute;top:-13px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;padding:4px 16px;border-radius:100px;font-size:12px;font-weight:600;white-space:nowrap;}
.plan-name{font-family:'Syne',sans-serif;font-size:22px;font-weight:700;color:#f0f0ff;margin-bottom:6px;}
.plan-desc{font-size:13px;color:#5555aa;margin-bottom:24px;}
.plan-price{margin-bottom:28px;}
.pa{font-family:'Syne',sans-serif;font-size:42px;font-weight:800;color:#f0f0ff;}
.pp{font-size:14px;color:#5555aa;margin-left:4px;}
.plan-list{list-style:none;padding:0;margin:0 0 32px;display:flex;flex-direction:column;gap:12px;flex:1;}
.plan-list li{font-size:14px;color:#8888aa;}
.plan-btn{display:flex;align-items:center;justify-content:center;padding:13px 0;border-radius:10px;border:1px solid rgba(255,255,255,0.12);color:#8888aa;font-size:14px;font-weight:600;transition:all 0.2s;}
.plan-btn:hover{border-color:rgba(124,58,237,0.4);color:#a78bfa;}
.plan-btn.primary{background:linear-gradient(135deg,#7c3aed,#6d28d9);border-color:transparent;color:#fff;box-shadow:0 0 24px rgba(124,58,237,0.35);}
.plan-btn.primary:hover{box-shadow:0 0 40px rgba(124,58,237,0.55);transform:translateY(-2px);}

/* ── FAQ ── */
.faq{padding:100px 0;}
.faq-list{margin-top:48px;display:flex;flex-direction:column;gap:4px;}
.faq-item{border:1px solid rgba(255,255,255,0.07);border-radius:12px;overflow:hidden;transition:border-color 0.2s;}
.faq-item.open{border-color:rgba(124,58,237,0.35);}
.faq-q{width:100%;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:20px 24px;background:transparent;border:none;cursor:pointer;text-align:left;color:#c4c4da;font-size:16px;font-weight:500;transition:color 0.2s;font-family:'Inter',sans-serif;}
.faq-q:hover{color:#e0e0f0;}
.faq-item.open .faq-q{color:#e0e0f0;}
.faq-ch{font-size:20px;color:#7c3aed;flex-shrink:0;}
.faq-a{padding:0 24px 20px;color:#6666aa;font-size:15px;line-height:1.7;animation:fi 0.25s ease;}
@keyframes fi{from{opacity:0;transform:translateY(-6px);}to{opacity:1;transform:none;}}

/* ── CTA ── */
.cta-sec{padding:120px 0;}
.cta-box{position:relative;overflow:hidden;background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.25);border-radius:28px;padding:80px 40px;text-align:center;}
.cta-orb{position:absolute;top:-100px;left:50%;transform:translateX(-50%);width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,rgba(124,58,237,0.25) 0%,transparent 70%);filter:blur(60px);pointer-events:none;}
.cta-h{font-family:'Syne',sans-serif;font-size:clamp(36px,5vw,60px);font-weight:800;color:#f0f0ff;margin:16px 0 20px;}
.cta-sub{font-size:18px;color:#7777aa;margin:0 auto 40px;max-width:500px;}
.cta-btns{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;}

/* ── FOOTER ── */
.footer{padding:60px 0 40px;border-top:1px solid rgba(255,255,255,0.06);}
.foot-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:48px;margin-bottom:48px;}
.foot-logo{display:flex;align-items:center;gap:10px;font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#f0f0ff;margin-bottom:14px;}
.foot-tag{font-size:14px;color:#5555aa;line-height:1.6;margin:0 0 20px;}
.gh-link{font-size:13px;color:#5555aa;font-weight:500;padding:6px 14px;border:1px solid rgba(255,255,255,0.08);border-radius:8px;transition:all 0.2s;}
.gh-link:hover{color:#a78bfa;border-color:rgba(124,58,237,0.3);}
.foot-col{display:flex;flex-direction:column;gap:10px;}
.foot-title{font-size:13px;font-weight:600;color:#6666aa;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;}
.foot-link{font-size:14px;color:#5555aa;transition:color 0.2s;}
.foot-link:hover{color:#c4c4da;}
.foot-bottom{display:flex;justify-content:space-between;align-items:center;padding-top:24px;border-top:1px solid rgba(255,255,255,0.05);font-size:13px;color:#4444aa;flex-wrap:wrap;gap:8px;}

/* ── Responsive ── */
@media(max-width:900px){.what-grid,.caps-grid,.uc-panel{grid-template-columns:1fr;}.feat-grid,.plan-grid{grid-template-columns:1fr 1fr;}.foot-grid{grid-template-columns:1fr 1fr;}.steps{flex-direction:column;align-items:center;}.step-arr{transform:rotate(90deg);padding:8px 0;}}
@media(max-width:600px){.nav-links{display:none;}.feat-grid,.plan-grid{grid-template-columns:1fr;}.foot-grid{grid-template-columns:1fr;}.testi-carousel{height:300px;}}
</style>
