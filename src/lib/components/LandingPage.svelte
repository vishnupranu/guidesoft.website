<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	export let onSignUpClick: () => void = () => {};
	export let onLogInClick: () => void = () => {};

	// Typewriter Heading Text
	const FULL_TEXT =
		'Unlock Top AI & Data Talent You Thought Was Out of Reach -- Now Just One Click Away!';
	const BLACK_CHAR_COUNT = 67; // First part black, rest white

	let typedText = '';
	let typingFinished = false;
	let countUpValue = 0;
	let countUpFinished = false;

	let typewriterTimer: any;
	let counterTimer: any;

	// Typewriter effect logic
	function startTypewriter() {
		let index = 0;
		setTimeout(() => {
			typewriterTimer = setInterval(() => {
				if (index < FULL_TEXT.length) {
					typedText += FULL_TEXT[index];
					index++;
				} else {
					clearInterval(typewriterTimer);
					typingFinished = true;
				}
			}, 35);
		}, 400);
	}

	// CountUp hook equivalent for "20k+" Specialists
	function startCountUp() {
		setTimeout(() => {
			const duration = 2000; // 2 seconds
			const start = 0;
			const end = 20;
			const startTime = performance.now();

			function step(now: number) {
				const elapsed = now - startTime;
				const progress = Math.min(elapsed / duration, 1);
				// Ease out cubic
				const eased = 1 - Math.pow(1 - progress, 3);
				countUpValue = Math.floor(start + (end - start) * eased);

				if (progress < 1) {
					counterTimer = requestAnimationFrame(step);
				} else {
					countUpValue = end;
					countUpFinished = true;
				}
			}

			counterTimer = requestAnimationFrame(step);
		}, 1200);
	}

	onMount(() => {
		startTypewriter();
		startCountUp();
	});

	onDestroy(() => {
		if (typewriterTimer) clearInterval(typewriterTimer);
		if (counterTimer) cancelAnimationFrame(counterTimer);
	});
</script>

<style>
	/* Register CSS custom property for rotating border angle */
	@property --border-angle {
		syntax: '<angle>';
		initial-value: 0deg;
		inherits: false;
	}

	@keyframes rotateBorder {
		to {
			--border-angle: 360deg;
		}
	}

	/* Rotating Gradient Border Wrapper */
	.btn-border-wrap {
		position: relative;
		display: inline-flex;
		border-radius: 50px;
		padding: 3px;
		isolation: isolate;
		background: transparent;
	}

	.btn-border-wrap::before {
		content: '';
		position: absolute;
		inset: -3px;
		padding: 3px;
		border-radius: 50px;
		background: conic-gradient(
			from var(--border-angle),
			#a068ff,
			#070319,
			#a068ff,
			#070319,
			#a068ff
		);
		animation: rotateBorder 3s linear infinite;
		-webkit-mask:
			linear-gradient(#fff 0 0) content-box,
			linear-gradient(#fff 0 0);
		-webkit-mask-composite: xor;
		mask-composite: exclude;
		pointer-events: none;
		z-index: 1;
	}

	/* Sliding Fill Buttons */
	.btn-join {
		position: relative;
		overflow: hidden;
		border-radius: 50px;
		background-color: #000000;
		color: #ffffff;
		padding: 12px 26px;
		font-size: 15px;
		font-weight: 500;
		transition: color 0.3s ease;
		z-index: 2;
	}

	.btn-join::after {
		content: '';
		position: absolute;
		inset: 0;
		background-color: #a068ff;
		transform: translateX(-100%);
		transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1);
		z-index: -1;
		border-radius: 50px;
	}

	.btn-join:hover::after {
		transform: translateX(0);
	}

	.btn-start {
		position: relative;
		overflow: hidden;
		border-radius: 50px;
		background-color: #060218;
		color: #ffffff;
		padding: 14px 28px;
		font-size: 16px;
		font-weight: 500;
		transition: color 0.3s ease;
		z-index: 2;
	}

	.btn-start::after {
		content: '';
		position: absolute;
		inset: 0;
		background-color: #a068ff;
		transform: translateX(100%);
		transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1);
		z-index: -1;
		border-radius: 50px;
	}

	.btn-start:hover::after {
		transform: translateX(0);
	}

	/* Nav link underline scale animation */
	.nav-link {
		position: relative;
		color: #000000;
		font-size: 15px;
		font-weight: 400;
		text-decoration: none;
	}

	.nav-link::after {
		content: '';
		position: absolute;
		bottom: -2px;
		left: 0;
		width: 100%;
		height: 2px;
		background-color: #000000;
		transform: scaleX(0);
		transform-origin: left;
		transition: transform 0.3s ease;
	}

	.nav-link:hover::after {
		transform: scaleX(1);
	}

	.nav-link-white {
		position: relative;
		color: #ffffff;
		font-size: 15px;
		font-weight: 500;
		text-decoration: none;
	}

	.nav-link-white::after {
		content: '';
		position: absolute;
		bottom: -2px;
		left: 0;
		width: 100%;
		height: 2px;
		background-color: #ffffff;
		transform: scaleX(0);
		transform-origin: left;
		transition: transform 0.3s ease;
	}

	.nav-link-white:hover::after {
		transform: scaleX(1);
	}

	/* Orbit Animations */
	@keyframes spinCCW {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(-360deg);
		}
	}

	@keyframes spinCW {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}

	.orbit-1 {
		animation: spinCCW 30s linear infinite;
	}
	.orbit-2 {
		animation: spinCW 40s linear infinite;
	}
	.orbit-3 {
		animation: spinCW 50s linear infinite;
	}
	.orbit-4 {
		animation: spinCCW 60s linear infinite;
	}

	/* Counter Rotation to keep upright */
	.orbit-counter-1 {
		animation: spinCW 30s linear infinite;
	}
	.orbit-counter-2 {
		animation: spinCCW 40s linear infinite;
	}
	.orbit-counter-3 {
		animation: spinCCW 50s linear infinite;
	}
	.orbit-counter-4 {
		animation: spinCW 60s linear infinite;
	}

	/* Ticker Scroll */
	@keyframes tickerScroll {
		0% {
			transform: translateX(0);
		}
		100% {
			transform: translateX(-50%);
		}
	}

	.ticker-track {
		display: flex;
		width: max-content;
		animation: tickerScroll 20s linear infinite;
	}

	/* Blinking Cursor */
	@keyframes blink {
		0%,
		100% {
			opacity: 1;
		}
		50% {
			opacity: 0;
		}
	}

	.blinking-cursor {
		display: inline-block;
		width: 3px;
		height: 1em;
		background-color: #a068ff;
		margin-left: 2px;
		vertical-align: middle;
		animation: blink 0.8s infinite;
	}
</style>

<div
	class="app relative w-full h-full min-h-screen flex flex-col justify-between overflow-x-hidden selection:bg-[#A068FF] selection:text-white font-['Inter']"
	style="background: url('https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260624_111401_56af5012-2263-45d3-849a-8688084d7c2a.png&w=1280&q=85') center center / cover no-repeat #0a0a0a;"
>
	<!-- HEADER -->
	<header
		class="w-full max-w-[1920px] mx-auto px-6 lg:px-16 py-6 flex items-center justify-between z-30"
	>
		<!-- Left Side: Logo + Nav Links -->
		<div class="flex items-center gap-10">
			<div class="flex items-center gap-3">
				<img src="/static/favicon.png" alt="GUIDESOFT.WEB" class="w-8 h-8 rounded-full shadow-md" />
				<span class="font-['Urbanist'] font-bold text-xl text-black tracking-tight">
					GUIDESOFT.WEB
				</span>
			</div>

			<nav class="hidden md:flex items-center gap-8">
				<a href="#team" class="nav-link">Your Team</a>
				<a href="#solutions" class="nav-link">Solutions</a>
				<a href="#blog" class="nav-link">Blog</a>
				<a href="#pricing" class="nav-link">Pricing</a>
			</nav>
		</div>

		<!-- Right Side: Log In + Join Now -->
		<div class="flex items-center gap-6">
			<button type="button" class="nav-link-white bg-transparent border-none cursor-pointer" on:click={onLogInClick}>
				Log In
			</button>

			<div class="btn-border-wrap">
				<button type="button" class="btn-join cursor-pointer" on:click={onSignUpClick}>
					Join Now
				</button>
			</div>
		</div>
	</header>

	<!-- MAIN HERO SECTION -->
	<main class="w-full max-w-[1920px] mx-auto px-6 lg:px-16 flex flex-col lg:flex-row items-center justify-between my-auto gap-12 py-8 z-20">
		<!-- HERO LEFT -->
		<div class="flex-1 max-w-[600px] pt-10 text-left">
			<!-- Heading with Typewriter Effect -->
			<h1 class="font-['Urbanist'] font-semibold text-[40px] sm:text-[52px] lg:text-[64px] leading-[1.05] tracking-[-1.5px] mb-8 min-h-[200px]">
				{#each typedText.split('') as char, i}
					<span style="color: {i < BLACK_CHAR_COUNT ? '#000000' : '#ffffff'};">
						{char}
					</span>
				{/each}
				{#if !typingFinished}
					<span class="blinking-cursor"></span>
				{/if}
			</h1>

			<!-- Start Project Button (Appears after typing) -->
			<div class="flex items-center gap-4 transition-all duration-700" class:opacity-0={!typingFinished} class:translate-y-4={!typingFinished}>
				<div class="btn-border-wrap">
					<button type="button" class="btn-start flex items-center gap-2 cursor-pointer" on:click={onSignUpClick}>
						<span>Start Project</span>
						<svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
							<path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round" />
						</svg>
					</button>
				</div>
			</div>

			<!-- Cursor Badge Element -->
			{#if typingFinished}
				<div class="mt-8 ml-[140px] sm:ml-[220px] flex items-center gap-2 animate-bounce">
					<!-- Purple Cursor Arrow SVG -->
					<svg class="w-6 h-6 text-[#A068FF] fill-current drop-shadow-md" viewBox="0 0 24 24">
						<path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z" />
					</svg>
					<!-- Label Badge -->
					<span class="bg-[#A068FF] text-white text-base font-medium px-4 py-2 rounded-[20px] shadow-lg font-['Inter']">
						David • AI Specialist
					</span>
				</div>
			{/if}
		</div>

		<!-- HERO RIGHT -- CIRCLES VISUALIZATION (720x720) -->
		<div class="relative w-[340px] sm:w-[540px] lg:w-[720px] h-[340px] sm:h-[540px] lg:h-[720px] flex items-center justify-center shrink-0">
			<!-- Concentric Circles (Orbits) -->

			<!-- Orbit 4 (Outermost: 797px / Scaled) -->
			<div class="orbit-4 absolute w-[92%] h-[92%] rounded-full border border-purple-400/30 flex items-center justify-center">
				<!-- Avatar on Orbit 4 (30deg) -->
				<div class="absolute top-[10%] left-[80%] -translate-x-1/2 -translate-y-1/2 orbit-counter-4">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/c76d8a0b99676de31c014344bfaf75bad090758d.png" alt="Avatar" class="w-12 h-12 rounded-full border-2 border-purple-500 shadow-[0_0_15px_rgba(160,104,255,0.6)] object-cover" />
				</div>
				<!-- Avatar on Orbit 4 (95deg) -->
				<div class="absolute top-[85%] left-[75%] -translate-x-1/2 -translate-y-1/2 orbit-counter-4">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/7b1b5f039de7b54cc9913e96c1923c3b15a157fa.png" alt="Avatar" class="w-16 h-16 rounded-[24px] border-2 border-orange-500 shadow-[0_0_15px_rgba(255,165,0,0.6)] object-cover" />
				</div>
				<!-- Avatar on Orbit 4 (220deg) -->
				<div class="absolute top-[70%] left-[10%] -translate-x-1/2 -translate-y-1/2 orbit-counter-4">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/9ae171d8895199349755c43fbff00e122221a027.png" alt="Avatar" class="w-16 h-16 rounded-[24px] border-2 border-pink-500 shadow-[0_0_15px_rgba(255,105,180,0.6)] object-cover" />
				</div>
				<!-- Avatar on Orbit 4 (320deg) -->
				<div class="absolute top-[15%] left-[20%] -translate-x-1/2 -translate-y-1/2 orbit-counter-4">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/926c9eb7b4bc1df846fa0e39f0b0dc3fefd80671.png" alt="Avatar" class="w-12 h-12 rounded-full border-2 border-purple-500 shadow-[0_0_15px_rgba(160,104,255,0.6)] object-cover" />
				</div>
			</div>

			<!-- Orbit 3 (649px) -->
			<div class="orbit-3 absolute w-[76%] h-[76%] rounded-full border border-purple-400/40 flex items-center justify-center">
				<!-- Avatar on Orbit 3 (130deg) -->
				<div class="absolute top-[75%] left-[20%] -translate-x-1/2 -translate-y-1/2 orbit-counter-3">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/018736aa5d0275c4ce56cfebaf2ae3007d81ca1e.png" alt="Avatar" class="w-16 h-16 rounded-full border-2 border-pink-500 shadow-[0_0_15px_rgba(255,105,180,0.6)] object-cover" />
				</div>
			</div>

			<!-- Orbit 2 (501px) -->
			<div class="orbit-2 absolute w-[58%] h-[58%] rounded-full border border-purple-400/50 flex items-center justify-center">
				<!-- Avatar on Orbit 2 (60deg) -->
				<div class="absolute top-[20%] left-[80%] -translate-x-1/2 -translate-y-1/2 orbit-counter-2">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/ca755f7f93c1126fb8bdbf99ab364a33aa9ab272.png" alt="Avatar" class="w-12 h-12 rounded-full border-2 border-yellow-400 shadow-[0_0_15px_rgba(255,215,0,0.6)] object-cover" />
				</div>
				<!-- Avatar on Orbit 2 (180deg) -->
				<div class="absolute top-[50%] left-[0%] -translate-x-1/2 -translate-y-1/2 orbit-counter-2">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/dc01064c7093dcc32674876ee3cf5e41c4a485c6.png" alt="Avatar" class="w-14 h-14 rounded-full border-2 border-pink-400 shadow-[0_0_15px_rgba(255,105,180,0.6)] object-cover" />
				</div>
				<!-- Avatar on Orbit 2 (300deg) -->
				<div class="absolute top-[10%] left-[30%] -translate-x-1/2 -translate-y-1/2 orbit-counter-2">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/d5470a58b02388336141575048720f19a50de832.png" alt="Avatar" class="w-12 h-12 rounded-[20px] border-2 border-blue-400 shadow-[0_0_15px_rgba(30,144,255,0.6)] object-cover" />
				</div>
			</div>

			<!-- Orbit 1 (Innermost: 353px) -->
			<div class="orbit-1 absolute w-[42%] h-[42%] rounded-full border border-purple-400/60 flex items-center justify-center">
				<!-- Avatar on Orbit 1 (270deg) -->
				<div class="absolute top-[0%] left-[50%] -translate-x-1/2 -translate-y-1/2 orbit-counter-1">
					<img src="https://polo-pecan-73837341.figma.site/_assets/v11/aa51718fb3af3637e6d666b6543fc27a175fada6.png" alt="Avatar" class="w-12 h-12 rounded-[20px] border-2 border-purple-500 shadow-[0_0_15px_rgba(160,104,255,0.6)] object-cover" />
				</div>
			</div>

			<!-- Center Circle Counter -->
			<div class="w-36 h-36 sm:w-44 sm:h-44 bg-white/90 backdrop-blur-md rounded-full shadow-2xl flex flex-col items-center justify-center text-center z-10 border border-purple-200">
				<span class="font-['Urbanist'] font-medium text-4xl sm:text-5xl text-black">
					{countUpValue}k+
				</span>
				<span class="font-['Urbanist'] font-semibold text-xs sm:text-sm text-neutral-600 uppercase tracking-wider">
					Specialists
				</span>
			</div>
		</div>
	</main>

	<!-- BOTTOM LOGO TICKER STRIP -->
	<footer class="w-full overflow-hidden py-6 border-t border-black/10 relative z-20">
		<div class="w-full max-w-[1920px] mx-auto px-6">
			<div class="ticker-track flex items-center gap-16">
				<!-- Logo Set 1 -->
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/1e7b0e6fcc016cd28aec5c68990118b8c54c35a5.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/3eac03c183db2ae080d910159211c14843398b61.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/17705a4c0023a0e5a99154dfb10582adbbf4260b.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/0e5f442b09dc5c248e3e60d40a65505fb1887228.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/63f99030ceb459e3c9ab9e429cfa2353491d3816.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />

				<!-- Repeated for Seamless Infinite Loop -->
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/1e7b0e6fcc016cd28aec5c68990118b8c54c35a5.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/3eac03c183db2ae080d910159211c14843398b61.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/17705a4c0023a0e5a99154dfb10582adbbf4260b.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/0e5f442b09dc5c248e3e60d40a65505fb1887228.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
				<img src="https://polo-pecan-73837341.figma.site/_assets/v11/63f99030ceb459e3c9ab9e429cfa2353491d3816.svg" alt="Partner Logo" class="w-[137px] h-[40px] object-contain opacity-80 hover:opacity-100 transition" />
			</div>
		</div>
	</footer>
</div>
