<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { WEBUI_NAME, config, user } from '$lib/stores';
	import { getBackendConfig } from '$lib/apis';
	import { getSessionUser, userSignIn, userSignUp } from '$lib/apis/auths';

	// ── URL params ──────────────────────────────────────
	let redirectTo = '/';
	let prefilledPrompt = '';

	// ── Form state ──────────────────────────────────────
	let mode: 'signin' | 'signup' = 'signin';
	let email = '';
	let password = '';
	let name = '';
	let loading = false;
	let showPassword = false;

	// ── Typing animation (left panel) ───────────────────
	const lines = [
		'Build production AI agents',
		'Ship code 10x faster',
		'Research at the speed of thought',
		'Automate any workflow',
		'Deploy with confidence'
	];
	let lineIdx = 0;
	let charIdx = 0;
	let typingDir = 1;
	let typingText = '';
	let typingTimer: ReturnType<typeof setTimeout>;

	function typeNext() {
		const line = lines[lineIdx];
		if (typingDir === 1) {
			charIdx++;
			typingText = line.slice(0, charIdx);
			if (charIdx >= line.length) {
				typingDir = -1;
				typingTimer = setTimeout(typeNext, 1800);
				return;
			}
		} else {
			charIdx--;
			typingText = line.slice(0, charIdx);
			if (charIdx <= 0) {
				typingDir = 1;
				lineIdx = (lineIdx + 1) % lines.length;
				typingTimer = setTimeout(typeNext, 350);
				return;
			}
		}
		typingTimer = setTimeout(typeNext, typingDir === 1 ? 52 : 24);
	}

	// Features for left panel
	const features = [
		{ icon: '⚡', text: '12 specialized AI agents' },
		{ icon: '🔗', text: '18 model providers — OpenAI, Claude, Gemini & more' },
		{ icon: '🔥', text: '32 Firecrawl skills for autonomous web research' },
		{ icon: '🤖', text: 'Playwright browser automation built-in' },
		{ icon: '📚', text: 'RAG knowledge base with citation support' },
	];

	// ── Auth handlers ────────────────────────────────────
	async function handleSignIn() {
		if (!email.trim() || !password.trim()) {
			toast.error('Please enter your email and password.');
			return;
		}
		loading = true;
		try {
			const res = await userSignIn(email.trim(), password);
			if (res?.token) {
				localStorage.setItem('token', res.token);
				await user.set(await getSessionUser(res.token));
				const targetUrl = prefilledPrompt ? `/?prompt=${encodeURIComponent(prefilledPrompt)}` : (redirectTo || '/');
				goto(targetUrl);
			}
		} catch (err: any) {
			toast.error(err?.detail || 'Sign in failed. Please check your credentials.');
		} finally {
			loading = false;
		}
	}

	async function handleSignUp() {
		if (!name.trim() || !email.trim() || !password.trim()) {
			toast.error('Please fill in all fields.');
			return;
		}
		if (password.length < 8) {
			toast.error('Password must be at least 8 characters.');
			return;
		}
		loading = true;
		try {
			const res = await userSignUp(name.trim(), email.trim(), password, '');
			if (res?.token) {
				localStorage.setItem('token', res.token);
				await user.set(await getSessionUser(res.token));
				const targetUrl = prefilledPrompt ? `/?prompt=${encodeURIComponent(prefilledPrompt)}` : (redirectTo || '/');
				goto(targetUrl);
			}
		} catch (err: any) {
			toast.error(err?.detail || 'Sign up failed. Please try again.');
		} finally {
			loading = false;
		}
	}

	function handleKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			mode === 'signin' ? handleSignIn() : handleSignUp();
		}
	}

	onMount(async () => {
		const params = $page.url.searchParams;
		redirectTo = params.get('redirect') || '/';
		prefilledPrompt = params.get('prompt') || '';
		const modeParam = params.get('mode') || params.get('signup');
		if (modeParam === 'signup' || modeParam === 'true') mode = 'signup';

		if (localStorage.token) {
			try {
				const sessionUser = await getSessionUser(localStorage.token);
				if (sessionUser) {
					await user.set(sessionUser);
					goto(redirectTo || '/');
					return;
				}
			} catch {}
		}

		try {
			const cfg = await getBackendConfig();
			if (cfg) config.set(cfg);
		} catch {}

		typeNext();
	});

	onDestroy(() => {
		clearTimeout(typingTimer);
	});
</script>

<svelte:head>
	<title>Sign in — GUIDESOFT.WEB</title>
	<meta name="description" content="Sign in to GUIDESOFT.WEB — the enterprise AI agent operating system. Access 12 specialized AI agents, 18 model providers, and 35+ AI skills." />
</svelte:head>

<div class="auth-root" role="main">

	<!-- ── LEFT PANEL (Antigravity/Codex style: bold content + features) ── -->
	<div class="left-panel" aria-label="GUIDESOFT.WEB platform overview">

		<!-- Dot grid decoration -->
		<div class="dot-grid" aria-hidden="true"></div>

		<!-- Top logo -->
		<a href="/" class="panel-logo" aria-label="GUIDESOFT.WEB home">
			<div class="logo-triangle" aria-hidden="true">
				<svg width="24" height="24" viewBox="0 0 28 28" fill="none">
					<path d="M14 2L26 22H2L14 2Z" fill="white" />
				</svg>
			</div>
			<span class="logo-name">GUIDESOFT<span class="logo-dot">.WEB</span></span>
		</a>

		<!-- Main hero content -->
		<div class="panel-content">
			<!-- Eyebrow -->
			<div class="panel-eyebrow">
				<span class="eyebrow-pulse" aria-hidden="true"></span>
				<span>Enterprise AI Agent OS</span>
			</div>

			<!-- Massive headline — Antigravity style -->
			<h1 class="panel-headline">
				Experience<br />
				liftoff with<br />
				the next-gen<br />
				<span class="headline-gradient">agent platform</span>
			</h1>

			<!-- Typing animation subtitle -->
			<p class="panel-typing" aria-live="polite">
				{typingText}<span class="cursor" aria-hidden="true">|</span>
			</p>

			<!-- Feature list -->
			<ul class="features-list" aria-label="Platform features">
				{#each features as feat}
					<li class="feature-item">
						<span class="feat-icon" aria-hidden="true">{feat.icon}</span>
						<span>{feat.text}</span>
					</li>
				{/each}
			</ul>
		</div>

		<!-- Stats row at bottom -->
		<div class="panel-stats" aria-label="Platform statistics">
			<div class="pstat">
				<span class="pstat-num">18</span>
				<span class="pstat-label">AI Providers</span>
			</div>
			<div class="pstat-divider" aria-hidden="true"></div>
			<div class="pstat">
				<span class="pstat-num">12</span>
				<span class="pstat-label">Agents</span>
			</div>
			<div class="pstat-divider" aria-hidden="true"></div>
			<div class="pstat">
				<span class="pstat-num">35+</span>
				<span class="pstat-label">Skills</span>
			</div>
		</div>
	</div>

	<!-- ── RIGHT PANEL (Clean minimal auth form) ─────────────────────── -->
	<div class="right-panel">

		<!-- Subtle bg grid -->
		<div class="right-grid" aria-hidden="true"></div>

		<div class="form-wrapper">

			<!-- Logo (mobile only) -->
			<a href="/" class="mobile-logo" aria-label="GUIDESOFT.WEB home">
				<svg width="20" height="20" viewBox="0 0 28 28" fill="none" aria-hidden="true">
					<path d="M14 2L26 22H2L14 2Z" fill="#0a0a0a" />
				</svg>
				<span>GUIDESOFT.WEB</span>
			</a>

			<!-- Form header -->
			<div class="form-header">
				<h2 class="form-title">
					{mode === 'signin' ? 'Welcome back' : 'Create your account'}
				</h2>
				<p class="form-sub">
					{#if mode === 'signin'}
						Sign in to your GUIDESOFT.WEB workspace
					{:else}
						Start building with the enterprise AI agent platform
					{/if}
				</p>
			</div>

			<!-- Tab toggle — Codex/Antigravity style pills -->
			<div class="mode-toggle" role="tablist" aria-label="Authentication mode">
				<button
					class="mode-tab"
					class:active={mode === 'signin'}
					role="tab"
					aria-selected={mode === 'signin'}
					id="signin-tab"
					on:click={() => (mode = 'signin')}
				>
					Sign In
				</button>
				<button
					class="mode-tab"
					class:active={mode === 'signup'}
					role="tab"
					aria-selected={mode === 'signup'}
					id="signup-tab"
					on:click={() => (mode = 'signup')}
				>
					Sign Up
				</button>
			</div>

			<!-- Auth Form -->
			<form class="auth-form" on:submit|preventDefault={mode === 'signin' ? handleSignIn : handleSignUp} aria-labelledby="{mode}-tab" novalidate>

				{#if mode === 'signup'}
					<div class="field">
						<label class="field-label" for="auth-name">Full name</label>
						<input
							id="auth-name"
							class="field-input"
							type="text"
							bind:value={name}
							on:keydown={handleKeyDown}
							placeholder="Your full name"
							autocomplete="name"
							aria-required="true"
						/>
					</div>
				{/if}

				<div class="field">
					<label class="field-label" for="auth-email">Email address</label>
					<input
						id="auth-email"
						class="field-input"
						type="email"
						bind:value={email}
						on:keydown={handleKeyDown}
						placeholder="you@company.com"
						autocomplete="email"
						aria-required="true"
					/>
				</div>

				<div class="field">
					<label class="field-label" for="auth-password">
						Password
						{#if mode === 'signup'}
							<span class="field-hint">Minimum 8 characters</span>
						{/if}
					</label>
					<div class="password-wrap">
						<input
							id="auth-password"
							class="field-input"
							type={showPassword ? 'text' : 'password'}
							bind:value={password}
							on:keydown={handleKeyDown}
							placeholder={mode === 'signup' ? 'Create a strong password' : 'Enter your password'}
							autocomplete={mode === 'signin' ? 'current-password' : 'new-password'}
							aria-required="true"
						/>
						<button
							type="button"
							class="show-pw"
							on:click={() => (showPassword = !showPassword)}
							aria-label={showPassword ? 'Hide password' : 'Show password'}
						>
							{#if showPassword}
								<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
									<path d="M2 2l12 12M6.5 6.6A2 2 0 0 0 9.4 9.5M4.4 4.5A7 7 0 0 0 1.5 8s2.2 4.5 6.5 4.5a6.8 6.8 0 0 0 3.6-1M7 3.55C7.16 3.52 7.33 3.5 7.5 3.5 11.8 3.5 14.5 8 14.5 8a8.5 8.5 0 0 1-1.4 2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
								</svg>
							{:else}
								<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
									<path d="M8 3.5C3.7 3.5 1 8 1 8s2.7 4.5 7 4.5 7-4.5 7-4.5-2.7-4.5-7-4.5z" stroke="currentColor" stroke-width="1.3"/>
									<circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.3"/>
								</svg>
							{/if}
						</button>
					</div>
				</div>

				<!-- Submit button -->
				<button
					type="submit"
					class="submit-btn"
					class:loading
					disabled={loading}
					aria-busy={loading}
				>
					{#if loading}
						<span class="spinner" aria-hidden="true"></span>
						<span>{mode === 'signin' ? 'Signing in...' : 'Creating account...'}</span>
					{:else}
						<span>{mode === 'signin' ? 'Sign in' : 'Create account'}</span>
						<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
							<path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					{/if}
				</button>
			</form>

			<!-- Mode switcher -->
			<p class="switch-mode">
				{mode === 'signin' ? "Don't have an account?" : 'Already have an account?'}
				<button
					class="switch-btn"
					on:click={() => (mode = mode === 'signin' ? 'signup' : 'signin')}
				>
					{mode === 'signin' ? 'Sign up' : 'Sign in'}
				</button>
			</p>

			<!-- Terms -->
			<p class="terms">
				By continuing, you agree to GUIDESOFT.WEB's
				<a href="/terms" class="terms-link">Terms of Service</a>
				and
				<a href="/privacy" class="terms-link">Privacy Policy</a>
			</p>

			<!-- Back to home -->
			<a href="/" class="back-home">
				<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
					<path d="M9 3L5 7l4 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
				</svg>
				Back to home
			</a>
		</div>
	</div>
</div>

<style>
	/* ── ROOT ─────────────────────────────────────────────────── */
	:global(html, body) {
		margin: 0;
		padding: 0;
		height: 100%;
		overflow: hidden;
	}

	.auth-root {
		display: grid;
		grid-template-columns: 1fr 1fr;
		min-height: 100vh;
		height: 100vh;
		overflow: hidden;
		font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', system-ui, sans-serif;
		-webkit-font-smoothing: antialiased;
	}

	/* ── LEFT PANEL ───────────────────────────────────────────── */
	.left-panel {
		position: relative;
		background: #0a0a0a;
		display: flex;
		flex-direction: column;
		padding: 36px 48px;
		overflow: hidden;
	}

	.dot-grid {
		position: absolute;
		inset: 0;
		background-image: radial-gradient(circle, rgba(255,255,255,0.08) 1px, transparent 1px);
		background-size: 24px 24px;
		pointer-events: none;
	}

	/* Subtle gradient overlay */
	.left-panel::before {
		content: '';
		position: absolute;
		inset: 0;
		background: radial-gradient(ellipse 80% 60% at 20% 80%, rgba(124,58,237,0.12) 0%, transparent 60%),
					radial-gradient(ellipse 60% 40% at 80% 20%, rgba(59,130,246,0.08) 0%, transparent 60%);
		pointer-events: none;
	}

	.panel-logo {
		position: relative;
		z-index: 1;
		display: flex;
		align-items: center;
		gap: 10px;
		text-decoration: none;
		color: #fff;
		font-size: 14px;
		font-weight: 700;
		letter-spacing: -0.01em;
		flex-shrink: 0;
	}

	.logo-triangle {
		display: flex;
		align-items: center;
		opacity: 0.9;
	}

	.logo-dot {
		color: rgba(255,255,255,0.4);
	}

	.panel-content {
		position: relative;
		z-index: 1;
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: center;
		gap: 0;
		padding: 40px 0;
	}

	.panel-eyebrow {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		padding: 5px 12px;
		background: rgba(255,255,255,0.06);
		border: 1px solid rgba(255,255,255,0.1);
		border-radius: 100px;
		font-size: 12px;
		font-weight: 500;
		color: rgba(255,255,255,0.55);
		letter-spacing: 0.01em;
		margin-bottom: 28px;
		width: fit-content;
	}

	.eyebrow-pulse {
		width: 6px;
		height: 6px;
		background: #22c55e;
		border-radius: 50%;
		animation: pulse 2s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; transform: scale(1); }
		50% { opacity: 0.4; transform: scale(0.75); }
	}

	/* Massive headline — Antigravity/Codex inspired */
	.panel-headline {
		font-size: clamp(36px, 4vw, 60px);
		font-weight: 800;
		color: #ffffff;
		line-height: 1.05;
		letter-spacing: -0.04em;
		margin: 0 0 20px;
	}

	.headline-gradient {
		background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.panel-typing {
		font-size: 16px;
		color: rgba(255,255,255,0.45);
		margin: 0 0 32px;
		min-height: 24px;
		font-weight: 400;
	}

	.cursor {
		animation: blink 1s step-end infinite;
		color: #a78bfa;
	}

	@keyframes blink {
		0%, 100% { opacity: 1; }
		50% { opacity: 0; }
	}

	.features-list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 13px;
	}

	.feature-item {
		display: flex;
		align-items: center;
		gap: 12px;
		font-size: 14px;
		color: rgba(255,255,255,0.6);
		font-weight: 400;
	}

	.feat-icon {
		font-size: 16px;
		flex-shrink: 0;
		width: 24px;
	}

	.panel-stats {
		position: relative;
		z-index: 1;
		display: flex;
		align-items: center;
		gap: 24px;
		padding-top: 32px;
		border-top: 1px solid rgba(255,255,255,0.07);
	}

	.pstat {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.pstat-num {
		font-size: 22px;
		font-weight: 800;
		color: #fff;
		letter-spacing: -0.03em;
		line-height: 1;
	}

	.pstat-label {
		font-size: 11px;
		color: rgba(255,255,255,0.35);
		font-weight: 500;
	}

	.pstat-divider {
		width: 1px;
		height: 28px;
		background: rgba(255,255,255,0.1);
	}

	/* ── RIGHT PANEL ──────────────────────────────────────────── */
	.right-panel {
		position: relative;
		background: #ffffff;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 48px 40px;
		overflow-y: auto;
	}

	.right-grid {
		position: absolute;
		inset: 0;
		background-image: radial-gradient(circle, #e4e4e7 1px, transparent 1px);
		background-size: 24px 24px;
		opacity: 0.35;
		pointer-events: none;
	}

	.form-wrapper {
		position: relative;
		z-index: 1;
		width: 100%;
		max-width: 400px;
		display: flex;
		flex-direction: column;
		gap: 0;
	}

	.mobile-logo {
		display: none;
		align-items: center;
		gap: 8px;
		text-decoration: none;
		color: #0a0a0a;
		font-size: 14px;
		font-weight: 700;
		margin-bottom: 32px;
	}

	.form-header {
		margin-bottom: 28px;
	}

	.form-title {
		font-size: 28px;
		font-weight: 800;
		color: #0a0a0a;
		letter-spacing: -0.03em;
		margin: 0 0 6px;
		line-height: 1.1;
	}

	.form-sub {
		font-size: 14px;
		color: #888;
		margin: 0;
		font-weight: 400;
	}

	/* Mode toggle — pill style */
	.mode-toggle {
		display: flex;
		background: rgba(0,0,0,0.04);
		border: 1px solid rgba(0,0,0,0.08);
		border-radius: 10px;
		padding: 3px;
		gap: 3px;
		margin-bottom: 24px;
	}

	.mode-tab {
		flex: 1;
		padding: 8px 16px;
		font-size: 13.5px;
		font-weight: 600;
		color: #888;
		border: none;
		background: transparent;
		border-radius: 8px;
		cursor: pointer;
		transition: all 0.15s;
		letter-spacing: -0.01em;
	}

	.mode-tab.active {
		background: #fff;
		color: #0a0a0a;
		box-shadow: 0 1px 4px rgba(0,0,0,0.08);
	}

	/* Form */
	.auth-form {
		display: flex;
		flex-direction: column;
		gap: 16px;
		margin-bottom: 16px;
	}

	.field {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.field-label {
		font-size: 13.5px;
		font-weight: 600;
		color: #333;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.field-hint {
		font-size: 11.5px;
		color: #aaa;
		font-weight: 400;
	}

	.field-input {
		width: 100%;
		padding: 11px 14px;
		font-size: 14.5px;
		color: #0a0a0a;
		background: #fff;
		border: 1.5px solid #e4e4e7;
		border-radius: 10px;
		transition: all 0.15s;
		outline: none;
		font-family: inherit;
		box-sizing: border-box;
		-webkit-appearance: none;
	}

	.field-input::placeholder {
		color: #bbb;
	}

	.field-input:focus {
		border-color: #0a0a0a;
		box-shadow: 0 0 0 3px rgba(0,0,0,0.06);
	}

	.password-wrap {
		position: relative;
	}

	.password-wrap .field-input {
		padding-right: 44px;
	}

	.show-pw {
		position: absolute;
		right: 12px;
		top: 50%;
		transform: translateY(-50%);
		background: none;
		border: none;
		color: #aaa;
		cursor: pointer;
		padding: 4px;
		display: flex;
		align-items: center;
		transition: color 0.15s;
	}

	.show-pw:hover {
		color: #555;
	}

	/* Submit button — Codex/Antigravity dark pill */
	.submit-btn {
		width: 100%;
		padding: 12px 20px;
		background: #0a0a0a;
		color: #fff;
		border: none;
		border-radius: 10px;
		font-size: 14.5px;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		letter-spacing: -0.01em;
		margin-top: 4px;
	}

	.submit-btn:hover:not(:disabled) {
		background: #222;
		transform: translateY(-1px);
		box-shadow: 0 6px 20px rgba(0,0,0,0.15);
	}

	.submit-btn:disabled {
		opacity: 0.7;
		cursor: not-allowed;
		transform: none;
	}

	.spinner {
		width: 16px;
		height: 16px;
		border: 2px solid rgba(255,255,255,0.3);
		border-top-color: #fff;
		border-radius: 50%;
		animation: spin 0.7s linear infinite;
		flex-shrink: 0;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	.switch-mode {
		text-align: center;
		font-size: 13.5px;
		color: #888;
		margin: 0 0 12px;
	}

	.switch-btn {
		background: none;
		border: none;
		color: #0a0a0a;
		font-size: 13.5px;
		font-weight: 600;
		cursor: pointer;
		padding: 0;
		margin-left: 4px;
		text-decoration: underline;
		text-underline-offset: 2px;
	}

	.terms {
		text-align: center;
		font-size: 11.5px;
		color: #bbb;
		margin: 0 0 20px;
		line-height: 1.6;
	}

	.terms-link {
		color: #888;
		text-decoration: underline;
		text-underline-offset: 2px;
		transition: color 0.15s;
	}

	.terms-link:hover {
		color: #0a0a0a;
	}

	.back-home {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 6px;
		font-size: 13px;
		color: #aaa;
		text-decoration: none;
		transition: color 0.15s;
	}

	.back-home:hover {
		color: #555;
	}

	/* ── RESPONSIVE ───────────────────────────────────────────── */
	@media (max-width: 768px) {
		.auth-root {
			grid-template-columns: 1fr;
			height: auto;
			overflow-y: auto;
		}

		.left-panel {
			display: none;
		}

		.right-panel {
			min-height: 100vh;
			padding: 32px 24px;
		}

		.mobile-logo {
			display: flex;
		}
	}
</style>
