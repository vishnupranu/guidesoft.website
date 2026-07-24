<script lang="ts">
	import DOMPurify from 'dompurify';
	import { marked } from 'marked';

	import { toast } from 'svelte-sonner';
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { fade, fly } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';

	import {
		WEBUI_NAME,
		config,
		user,
		socket,
		isApp,
	} from '$lib/stores';

	import { getBackendConfig } from '$lib/apis';
	import {
		getSessionUser,
		userSignIn,
		userSignUp,
	} from '$lib/apis/auths';

	// ── URL params ──────────────────────────────────────────
	let redirectTo = '/';
	let prefilledPrompt = '';
	let initialMode: 'signin' | 'signup' = 'signin';

	// ── Form state ──────────────────────────────────────────
	let mode: 'signin' | 'signup' = 'signin';
	let email = '';
	let password = '';
	let name = '';
	let loading = false;
	let showPassword = false;

	// ── Canvas particles ────────────────────────────────────
	let canvasEl: HTMLCanvasElement;
	let animId: number;
	let particles: { x: number; y: number; vx: number; vy: number; r: number; o: number }[] = [];

	// ── Typing animation ────────────────────────────────────
	const lines = [
		'Build AI pipelines in minutes',
		'Connect 12+ language models',
		'Chat with your documents',
		'Deploy agents autonomously',
		'Scale with your team'
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
				typingTimer = setTimeout(typeNext, 1600);
				return;
			}
		} else {
			charIdx--;
			typingText = line.slice(0, charIdx);
			if (charIdx <= 0) {
				typingDir = 1;
				lineIdx = (lineIdx + 1) % lines.length;
				typingTimer = setTimeout(typeNext, 300);
				return;
			}
		}
		typingTimer = setTimeout(typeNext, typingDir === 1 ? 55 : 28);
	}

	function initParticles(canvas: HTMLCanvasElement) {
		canvas.width = canvas.offsetWidth;
		canvas.height = canvas.offsetHeight;
		particles = Array.from({ length: 40 }, () => ({
			x: Math.random() * canvas.width,
			y: Math.random() * canvas.height,
			vx: (Math.random() - 0.5) * 0.25,
			vy: (Math.random() - 0.5) * 0.25,
			r: Math.random() * 1.2 + 0.4,
			o: Math.random() * 0.35 + 0.08,
		}));
	}

	function drawParticles() {
		if (!canvasEl) return;
		const ctx = canvasEl.getContext('2d')!;
		ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
		particles.forEach((p) => {
			p.x += p.vx; p.y += p.vy;
			if (p.x < 0) p.x = canvasEl.width;
			if (p.x > canvasEl.width) p.x = 0;
			if (p.y < 0) p.y = canvasEl.height;
			if (p.y > canvasEl.height) p.y = 0;
			ctx.beginPath();
			ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
			ctx.fillStyle = `rgba(167,139,250,${p.o})`;
			ctx.fill();
		});
		for (let i = 0; i < particles.length; i++) {
			for (let j = i + 1; j < particles.length; j++) {
				const dx = particles[i].x - particles[j].x;
				const dy = particles[i].y - particles[j].y;
				const d = Math.sqrt(dx * dx + dy * dy);
				if (d < 90) {
					ctx.beginPath();
					ctx.moveTo(particles[i].x, particles[i].y);
					ctx.lineTo(particles[j].x, particles[j].y);
					ctx.strokeStyle = `rgba(124,58,237,${0.1 * (1 - d / 90)})`;
					ctx.lineWidth = 0.5;
					ctx.stroke();
				}
			}
		}
		animId = requestAnimationFrame(drawParticles);
	}

	// ── Auth handlers ────────────────────────────────────────
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
		// Parse URL params
		const params = $page.url.searchParams;
		redirectTo = params.get('redirect') || '/';
		prefilledPrompt = params.get('prompt') || '';
		const modeParam = params.get('mode');
		if (modeParam === 'signup') mode = 'signup';

		// Check already signed in
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

		// Start particles
		if (canvasEl) {
			initParticles(canvasEl);
			drawParticles();
		}
		setTimeout(typeNext, 600);
	});

	onDestroy(() => {
		cancelAnimationFrame(animId);
		clearTimeout(typingTimer);
	});
</script>

<svelte:head>
	<title>{mode === 'signin' ? 'Sign In' : 'Create Account'} — GUIDESOFT.WEB</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@600;700;800&display=swap" rel="stylesheet" />
</svelte:head>

<div class="auth-page">

	<!-- ═══════════════════════════
	     LEFT PANEL
	════════════════════════════════ -->
	<div class="auth-left">
		<!-- Particle canvas -->
		<canvas class="auth-canvas" bind:this={canvasEl}></canvas>

		<!-- Gradient orbs -->
		<div class="left-orb left-orb-1"></div>
		<div class="left-orb left-orb-2"></div>
		<div class="left-orb left-orb-3"></div>
		<div class="left-grid"></div>

		<!-- Content -->
		<div class="left-content">
			<!-- Logo / back link -->
			<a href="/" class="left-logo">
				<div class="logo-mark">G</div>
				<span class="logo-text">GUIDESOFT<span class="logo-dot">.WEB</span></span>
			</a>

			<div class="left-hero">
				<div class="left-badge">
					<span class="badge-dot"></span>
					AI Platform · Production Ready
				</div>

				<h1 class="left-heading">
					Your AI<br />
					<span class="gradient-text">Superpower</span><br />
					Awaits
				</h1>

				<p class="left-tagline">
					<span class="typing-text">{typingText}</span><span class="cursor">|</span>
				</p>

				<!-- Feature bullets -->
				<div class="left-bullets">
					{#each ['Multi-model AI (GPT-4, Claude, Gemini)', 'RAG with your documents', 'Autonomous AI agents', 'OpenAI-compatible API'] as b, i}
						<div class="bullet-item" style="animation-delay:{i*120}ms">
							<span class="bullet-icon">✓</span>
							{b}
						</div>
					{/each}
				</div>

				<!-- Preview card -->
				<div class="preview-card">
					<div class="preview-model-badge">GPT-4o</div>
					<div class="preview-msg">
						Summarize the Q2 report and flag any anomalies.
					</div>
					<div class="preview-response">
						<span>Analyzed 47 pages. Revenue up <strong>34%</strong> YoY. Found 2 anomalies in March expenses...</span>
						<div class="preview-bar-wrap">
							<div class="preview-bar"></div>
						</div>
					</div>
				</div>
			</div>

			<!-- Bottom stat strip -->
			<div class="left-stats">
				<div class="l-stat"><strong>50K+</strong><span>Teams</span></div>
				<div class="l-stat-divider"></div>
				<div class="l-stat"><strong>12+</strong><span>Models</span></div>
				<div class="l-stat-divider"></div>
				<div class="l-stat"><strong>99.9%</strong><span>Uptime</span></div>
			</div>
		</div>
	</div>

	<!-- ═══════════════════════════
	     RIGHT PANEL
	════════════════════════════════ -->
	<div class="auth-right">
		<div class="auth-form-wrap">

			<!-- Mode tabs -->
			<div class="auth-tabs">
				<button
					class="auth-tab"
					class:active={mode === 'signin'}
					on:click={() => (mode = 'signin')}
					id="tab-signin"
				>Sign In</button>
				<button
					class="auth-tab"
					class:active={mode === 'signup'}
					on:click={() => (mode = 'signup')}
					id="tab-signup"
				>Create Account</button>
			</div>

			{#if mode === 'signin'}
				<div in:fly={{ x: -16, duration: 300, easing: cubicOut }}>
					<h2 class="form-heading">Welcome back</h2>
					<p class="form-sub">Sign in to your GUIDESOFT account</p>

					<div class="form-fields" on:keydown={handleKeyDown} role="group">
						<div class="field">
							<label class="field-label" for="signin-email">Email</label>
							<input
								id="signin-email"
								type="email"
								bind:value={email}
								class="field-input"
								placeholder="you@company.com"
								autocomplete="email"
							/>
						</div>

						<div class="field">
							<label class="field-label" for="signin-password">
								Password
								<a href="/auth?mode=reset" class="forgot-link">Forgot?</a>
							</label>
							<div class="password-wrap">
								<input
									id="signin-password"
									type={showPassword ? 'text' : 'password'}
									bind:value={password}
									class="field-input"
									placeholder="••••••••"
									autocomplete="current-password"
								/>
								<button class="show-pw" type="button" on:click={() => (showPassword = !showPassword)} id="toggle-password">
									{showPassword ? '👁' : '👁‍🗨'}
								</button>
							</div>
						</div>

						<button class="submit-btn" on:click={handleSignIn} disabled={loading} id="btn-signin">
							{#if loading}
								<span class="spinner"></span> Signing in…
							{:else}
								Sign In →
							{/if}
						</button>
					</div>

					<div class="divider"><span>or continue with</span></div>

					<div class="oauth-btns">
						<a href="/oauth/google/login" class="oauth-btn" id="oauth-google">
							<svg viewBox="0 0 24 24" width="18" height="18"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
							Google
						</a>
						<a href="/oauth/github/login" class="oauth-btn" id="oauth-github">
							<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
							GitHub
						</a>
					</div>

					<p class="switch-mode">
						Don't have an account?
						<button class="switch-link" on:click={() => (mode = 'signup')} id="switch-to-signup">Create one free →</button>
					</p>
				</div>

			{:else}
				<div in:fly={{ x: 16, duration: 300, easing: cubicOut }}>
					<h2 class="form-heading">Create your account</h2>
					<p class="form-sub">Start building with AI — free forever</p>

					<div class="form-fields" on:keydown={handleKeyDown} role="group">
						<div class="field">
							<label class="field-label" for="signup-name">Full Name</label>
							<input
								id="signup-name"
								type="text"
								bind:value={name}
								class="field-input"
								placeholder="Alex Johnson"
								autocomplete="name"
							/>
						</div>

						<div class="field">
							<label class="field-label" for="signup-email">Email</label>
							<input
								id="signup-email"
								type="email"
								bind:value={email}
								class="field-input"
								placeholder="you@company.com"
								autocomplete="email"
							/>
						</div>

						<div class="field">
							<label class="field-label" for="signup-password">Password</label>
							<div class="password-wrap">
								<input
									id="signup-password"
									type={showPassword ? 'text' : 'password'}
									bind:value={password}
									class="field-input"
									placeholder="Min. 8 characters"
									autocomplete="new-password"
								/>
								<button class="show-pw" type="button" on:click={() => (showPassword = !showPassword)} id="toggle-password-signup">
									{showPassword ? '👁' : '👁‍🗨'}
								</button>
							</div>
							{#if password.length > 0}
								<div class="pw-strength">
									<div class="pw-bar" style="width:{Math.min(password.length/12*100, 100)}%; background:{password.length < 8 ? '#ef4444' : password.length < 12 ? '#f59e0b' : '#22c55e'}"></div>
								</div>
								<span class="pw-hint" style="color:{password.length < 8 ? '#ef4444' : password.length < 12 ? '#f59e0b' : '#22c55e'}">
									{password.length < 8 ? 'Too short' : password.length < 12 ? 'Good' : 'Strong'}
								</span>
							{/if}
						</div>

						<button class="submit-btn" on:click={handleSignUp} disabled={loading} id="btn-signup">
							{#if loading}
								<span class="spinner"></span> Creating account…
							{:else}
								Create Account →
							{/if}
						</button>
					</div>

					<div class="divider"><span>or continue with</span></div>

					<div class="oauth-btns">
						<a href="/oauth/google/login" class="oauth-btn" id="oauth-google-signup">
							<svg viewBox="0 0 24 24" width="18" height="18"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
							Google
						</a>
						<a href="/oauth/github/login" class="oauth-btn" id="oauth-github-signup">
							<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
							GitHub
						</a>
					</div>

					<p class="form-legal">
						By creating an account, you agree to our
						<a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
					</p>

					<p class="switch-mode">
						Already have an account?
						<button class="switch-link" on:click={() => (mode = 'signin')} id="switch-to-signin">Sign in →</button>
					</p>
				</div>
			{/if}

			<!-- Back to landing -->
			<div class="back-to-landing">
				<a href="/" class="back-link">← Back to GUIDESOFT.WEB</a>
			</div>
		</div>
	</div>

</div>

<style>
	:global(body) {
		margin: 0; padding: 0;
		background: #080810;
		font-family: 'Inter', system-ui, sans-serif;
		overflow: hidden;
	}
	:global(*) { box-sizing: border-box; }
	:global(a) { text-decoration: none; }

	/* ── Layout ── */
	.auth-page {
		display: flex;
		height: 100vh;
		width: 100vw;
		overflow: hidden;
	}

	/* ══════════════ LEFT ══════════════ */
	.auth-left {
		position: relative;
		flex: 1;
		background: radial-gradient(ellipse 80% 60% at 30% 40%, rgba(124,58,237,0.2) 0%, transparent 65%),
		            #08080f;
		overflow: hidden;
		display: flex;
		align-items: stretch;
		padding: 0;
	}
	.auth-canvas {
		position: absolute; inset: 0; width: 100%; height: 100%;
		pointer-events: none; z-index: 1;
	}
	.left-orb {
		position: absolute; border-radius: 50%;
		filter: blur(70px); pointer-events: none; z-index: 0;
	}
	.left-orb-1 {
		width: 500px; height: 500px;
		background: radial-gradient(circle, rgba(124,58,237,0.2) 0%, transparent 70%);
		top: -150px; left: -100px;
		animation: orb1 8s ease-in-out infinite;
	}
	.left-orb-2 {
		width: 350px; height: 350px;
		background: radial-gradient(circle, rgba(37,99,235,0.13) 0%, transparent 70%);
		bottom: -100px; right: 40px;
		animation: orb2 11s ease-in-out infinite;
	}
	.left-orb-3 {
		width: 200px; height: 200px;
		background: radial-gradient(circle, rgba(52,211,153,0.1) 0%, transparent 70%);
		top: 55%; left: 55%;
		animation: orb3 9s ease-in-out infinite;
	}
	@keyframes orb1 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(20px,15px); } }
	@keyframes orb2 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-15px,-20px); } }
	@keyframes orb3 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(10px,-10px); } }
	.left-grid {
		position: absolute; inset: 0; z-index: 1;
		background-image:
			linear-gradient(rgba(124,58,237,0.06) 1px, transparent 1px),
			linear-gradient(90deg, rgba(124,58,237,0.06) 1px, transparent 1px);
		background-size: 52px 52px;
		mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 20%, transparent 75%);
	}

	.left-content {
		position: relative; z-index: 10;
		width: 100%;
		display: flex; flex-direction: column;
		padding: 40px 52px;
		gap: 0;
	}

	.left-logo {
		display: flex; align-items: center; gap: 10px;
		margin-bottom: 48px;
	}
	.logo-mark {
		width: 36px; height: 36px; border-radius: 10px;
		background: linear-gradient(135deg, #7c3aed, #a78bfa);
		display: flex; align-items: center; justify-content: center;
		font-weight: 800; font-size: 17px; color: #fff;
	}
	.logo-text {
		font-family: 'Syne', sans-serif;
		font-size: 16px; font-weight: 700; color: #f0f0ff;
	}
	.logo-dot { color: #7c3aed; }

	.left-hero { flex: 1; display: flex; flex-direction: column; }

	.left-badge {
		display: inline-flex; align-items: center; gap: 8px;
		background: rgba(124,58,237,0.15);
		border: 1px solid rgba(124,58,237,0.3);
		color: #a78bfa; padding: 6px 14px;
		border-radius: 100px; font-size: 12px; font-weight: 500;
		margin-bottom: 24px; align-self: flex-start;
	}
	.badge-dot {
		width: 6px; height: 6px; border-radius: 50%;
		background: #7c3aed; box-shadow: 0 0 8px #7c3aed;
		animation: pulse 2s ease-in-out infinite;
	}
	@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

	.left-heading {
		font-family: 'Syne', sans-serif;
		font-size: clamp(36px, 4.5vw, 58px);
		font-weight: 800; line-height: 1.1;
		color: #f0f0ff; margin: 0 0 20px;
	}
	.gradient-text {
		background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}
	.left-tagline {
		font-size: 16px; color: #7777aa;
		min-height: 28px; margin: 0 0 32px;
	}
	.typing-text { color: #a78bfa; font-weight: 500; }
	.cursor {
		color: #7c3aed;
		animation: blink 1s step-end infinite;
	}
	@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0; } }

	.left-bullets {
		display: flex; flex-direction: column; gap: 10px;
		margin-bottom: 32px;
	}
	.bullet-item {
		display: flex; align-items: center; gap: 10px;
		font-size: 14px; color: #8888aa;
		animation: fadeUp 0.5s ease both;
	}
	@keyframes fadeUp { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:none; } }
	.bullet-icon { color: #7c3aed; font-size: 14px; }

	/* Preview card */
	.preview-card {
		background: rgba(255,255,255,0.04);
		border: 1px solid rgba(124,58,237,0.2);
		border-radius: 14px; padding: 20px;
		margin-top: auto;
	}
	.preview-model-badge {
		display: inline-flex;
		background: rgba(124,58,237,0.2); color: #a78bfa;
		padding: 3px 10px; border-radius: 4px;
		font-size: 11px; font-weight: 600; margin-bottom: 10px;
	}
	.preview-msg {
		font-size: 13px; color: #9999cc;
		background: rgba(124,58,237,0.12);
		border: 1px solid rgba(124,58,237,0.2);
		padding: 10px 14px; border-radius: 8px; margin-bottom: 12px;
	}
	.preview-response {
		font-size: 13px; color: #6666aa; line-height: 1.6;
	}
	.preview-response strong { color: #a78bfa; }
	.preview-bar-wrap {
		height: 3px; background: rgba(255,255,255,0.07);
		border-radius: 10px; margin-top: 10px; overflow: hidden;
	}
	.preview-bar {
		height: 100%; width: 70%;
		background: linear-gradient(90deg, #7c3aed, #a78bfa);
		border-radius: 10px;
		animation: progress 2s ease-in-out infinite alternate;
	}
	@keyframes progress { from { width:20%; } to { width:90%; } }

	.left-stats {
		display: flex; align-items: center; gap: 20px;
		margin-top: 28px; flex-wrap: wrap;
	}
	.l-stat { display: flex; flex-direction: column; }
	.l-stat strong { font-size: 18px; font-weight: 700; color: #f0f0ff; }
	.l-stat span { font-size: 11px; color: #5555aa; text-transform: uppercase; letter-spacing: 1px; }
	.l-stat-divider { width: 1px; height: 28px; background: rgba(255,255,255,0.08); }

	/* ══════════════ RIGHT ══════════════ */
	.auth-right {
		width: 480px; min-width: 380px;
		background: #0c0c18;
		border-left: 1px solid rgba(124,58,237,0.15);
		display: flex; align-items: center; justify-content: center;
		overflow-y: auto;
	}
	.auth-form-wrap {
		width: 100%; max-width: 380px;
		padding: 48px 40px;
	}

	/* Tabs */
	.auth-tabs {
		display: flex; gap: 4px; margin-bottom: 32px;
		background: rgba(255,255,255,0.04);
		border: 1px solid rgba(255,255,255,0.07);
		padding: 4px; border-radius: 12px;
	}
	.auth-tab {
		flex: 1; padding: 9px; border-radius: 8px;
		border: none; cursor: pointer;
		background: transparent; color: #6666aa;
		font-size: 14px; font-weight: 500;
		font-family: 'Inter', sans-serif;
		transition: all 0.2s;
	}
	.auth-tab.active {
		background: rgba(124,58,237,0.25);
		color: #c4b4fa;
		border: 1px solid rgba(124,58,237,0.3);
	}

	/* Form */
	.form-heading {
		font-family: 'Syne', sans-serif;
		font-size: 26px; font-weight: 700;
		color: #f0f0ff; margin: 0 0 6px;
	}
	.form-sub { font-size: 14px; color: #5555aa; margin: 0 0 28px; }

	.form-fields { display: flex; flex-direction: column; gap: 16px; }

	.field { display: flex; flex-direction: column; gap: 6px; }
	.field-label {
		display: flex; justify-content: space-between;
		font-size: 13px; font-weight: 500; color: #8888aa;
	}
	.forgot-link { color: #7c3aed; font-size: 12px; transition: color 0.2s; }
	.forgot-link:hover { color: #a78bfa; }

	.field-input {
		width: 100%; padding: 12px 14px;
		background: rgba(255,255,255,0.04);
		border: 1.5px solid rgba(255,255,255,0.1);
		border-radius: 10px; color: #e2e2ef;
		font-size: 15px; font-family: 'Inter', sans-serif;
		outline: none; transition: border-color 0.2s, box-shadow 0.2s;
	}
	.field-input::placeholder { color: rgba(100,100,150,0.7); }
	.field-input:focus {
		border-color: rgba(124,58,237,0.6);
		box-shadow: 0 0 0 3px rgba(124,58,237,0.1);
	}

	.password-wrap { position: relative; }
	.password-wrap .field-input { padding-right: 44px; }
	.show-pw {
		position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
		background: none; border: none; cursor: pointer;
		font-size: 16px; color: #6666aa; line-height: 1;
	}

	.pw-strength {
		height: 3px; background: rgba(255,255,255,0.07);
		border-radius: 10px; overflow: hidden; margin-top: 6px;
	}
	.pw-bar { height: 100%; border-radius: 10px; transition: all 0.3s; }
	.pw-hint { font-size: 11px; margin-top: 3px; }

	.submit-btn {
		width: 100%; padding: 14px;
		background: linear-gradient(135deg, #7c3aed, #6d28d9);
		border: none; border-radius: 10px;
		color: #fff; font-size: 15px; font-weight: 600;
		font-family: 'Inter', sans-serif;
		cursor: pointer; transition: all 0.2s;
		display: flex; align-items: center; justify-content: center; gap: 8px;
		box-shadow: 0 0 24px rgba(124,58,237,0.3);
		margin-top: 4px;
	}
	.submit-btn:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 0 36px rgba(124,58,237,0.5);
	}
	.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }

	.spinner {
		width: 16px; height: 16px; border-radius: 50%;
		border: 2px solid rgba(255,255,255,0.3);
		border-top-color: #fff;
		animation: spin 0.7s linear infinite;
	}
	@keyframes spin { to { transform: rotate(360deg); } }

	.divider {
		display: flex; align-items: center; gap: 12px;
		margin: 20px 0; color: #4444aa; font-size: 12px;
	}
	.divider::before, .divider::after {
		content: ''; flex: 1; height: 1px;
		background: rgba(255,255,255,0.07);
	}

	.oauth-btns { display: flex; gap: 10px; margin-bottom: 20px; }
	.oauth-btn {
		flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px;
		padding: 11px; border-radius: 10px;
		border: 1px solid rgba(255,255,255,0.1);
		background: rgba(255,255,255,0.04);
		color: #c4c4da; font-size: 14px; font-weight: 500;
		transition: all 0.2s;
	}
	.oauth-btn:hover {
		border-color: rgba(124,58,237,0.4);
		background: rgba(124,58,237,0.08);
		color: #e0e0f0;
	}

	.form-legal {
		font-size: 11px; color: #4444aa; text-align: center;
		margin: 8px 0 0;
	}
	.form-legal a { color: #7c3aed; }
	.form-legal a:hover { color: #a78bfa; }

	.switch-mode {
		font-size: 13px; color: #5555aa;
		text-align: center; margin: 20px 0 0;
	}
	.switch-link {
		background: none; border: none; cursor: pointer;
		color: #7c3aed; font-size: 13px;
		font-family: 'Inter', sans-serif;
		transition: color 0.2s;
	}
	.switch-link:hover { color: #a78bfa; }

	.back-to-landing {
		text-align: center; margin-top: 24px;
		padding-top: 20px;
		border-top: 1px solid rgba(255,255,255,0.05);
	}
	.back-link { font-size: 13px; color: #4444aa; transition: color 0.2s; }
	.back-link:hover { color: #7c3aed; }

	/* ── Responsive ── */
	@media (max-width: 860px) {
		.auth-left { display: none; }
		.auth-right { width: 100%; }
		:global(body) { overflow: auto; }
		.auth-page { height: auto; min-height: 100vh; }
	}
</style>
