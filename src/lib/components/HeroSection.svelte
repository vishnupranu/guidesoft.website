<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	export let onSignUpClick: () => void = () => {};
	export let onLogInClick: () => void = () => {};

	let videoElement: HTMLVideoElement;
	let opacity = 0;
	let animationFrameId: number | null = null;
	let fadingOut = false;
	let questionText = '';
	let featuresDropdownOpen = false;

	const VIDEO_URL =
		'https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260329_050842_be71947f-f16e-4a14-810c-06e83d23ddb5.mp4';

	function fadeTo(targetOpacity: number, durationMs: number, onComplete?: () => void) {
		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}

		const startOpacity = opacity;
		const startTime = performance.now();

		function step(now: number) {
			const elapsed = now - startTime;
			const progress = Math.min(elapsed / durationMs, 1);
			opacity = startOpacity + (targetOpacity - startOpacity) * progress;

			if (progress < 1) {
				animationFrameId = requestAnimationFrame(step);
			} else {
				animationFrameId = null;
				if (onComplete) onComplete();
			}
		}

		animationFrameId = requestAnimationFrame(step);
	}

	function handleTimeUpdate() {
		if (!videoElement || !videoElement.duration) return;
		const remaining = videoElement.duration - videoElement.currentTime;

		if (remaining <= 0.55 && !fadingOut && videoElement.duration > 0) {
			fadingOut = true;
			fadeTo(0, 250);
		}
	}

	function handleEnded() {
		opacity = 0;
		setTimeout(() => {
			if (!videoElement) return;
			videoElement.currentTime = 0;
			fadingOut = false;
			videoElement
				.play()
				.then(() => {
					fadeTo(1, 250);
				})
				.catch((err) => console.log('Video play error:', err));
		}, 100);
	}

	function handleLoadedData() {
		fadingOut = false;
		fadeTo(1, 250);
	}

	onMount(() => {
		if (videoElement && videoElement.readyState >= 3) {
			handleLoadedData();
		}
	});

	onDestroy(() => {
		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
		}
	});
</script>

<div
	class="relative w-full min-h-screen overflow-x-hidden flex flex-col justify-between bg-white text-black font-['Schibsted_Grotesk'] selection:bg-black selection:text-white"
>
	<!-- Looping Video Background -->
	<div class="absolute inset-0 overflow-hidden pointer-events-none z-0">
		<video
			bind:this={videoElement}
			src={VIDEO_URL}
			autoplay
			muted
			playsinline
			style="opacity: {opacity}; transition: none;"
			on:timeupdate={handleTimeUpdate}
			on:ended={handleEnded}
			on:loadeddata={handleLoadedData}
			class="absolute top-0 left-1/2 -translate-x-1/2 w-[115%] h-[115%] object-cover object-top"
		/>
		<!-- Soft gradient overlay for content readability -->
		<div
			class="absolute inset-0 bg-gradient-to-b from-white/40 via-white/10 to-white/80 pointer-events-none"
		/>
	</div>

	<!-- Navigation Bar -->
	<header
		class="relative z-20 w-full flex items-center justify-between px-6 md:px-16 lg:px-[120px] py-4"
	>
		<!-- Brand Logo -->
		<div class="flex items-center gap-3">
			<img src="/static/favicon.png" alt="GS" class="w-8 h-8 rounded-full shadow-xs" />
			<span
				class="font-['Schibsted_Grotesk'] font-semibold text-[24px] tracking-[-1.44px] text-black"
			>
				GUIDESOFT.WEB
			</span>
		</div>

		<!-- Menu items -->
		<nav
			class="hidden lg:flex items-center gap-8 text-[16px] font-medium tracking-[-0.2px] text-black/80"
		>
			<a href="#platform" class="hover:text-black transition-colors">Platform</a>

			<div class="relative group">
				<button
					class="flex items-center gap-1.5 hover:text-black transition-colors"
					on:click={() => (featuresDropdownOpen = !featuresDropdownOpen)}
				>
					<span>Features</span>
					<svg
						class="w-4 h-4 text-black/70 transition-transform duration-200"
						class:rotate-180={featuresDropdownOpen}
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path d="M6 9l6 6 6-6" stroke-linecap="round" stroke-linejoin="round" />
					</svg>
				</button>
				{#if featuresDropdownOpen}
					<div
						class="absolute top-full left-0 mt-2 w-48 bg-white/95 backdrop-blur-md rounded-xl shadow-xl border border-black/5 p-2 z-50 flex flex-col gap-1 text-sm"
					>
						<a href="#ai-analytics" class="px-3 py-2 rounded-lg hover:bg-black/5 transition-colors"
							>AI Data Analytics</a
						>
						<a href="#automation" class="px-3 py-2 rounded-lg hover:bg-black/5 transition-colors"
							>Automations & Workflows</a
						>
						<a href="#security" class="px-3 py-2 rounded-lg hover:bg-black/5 transition-colors"
							>Enterprise Security</a
						>
					</div>
				{/if}
			</div>

			<a href="#projects" class="hover:text-black transition-colors">Projects</a>
			<a href="#community" class="hover:text-black transition-colors">Community</a>
			<a href="#contact" class="hover:text-black transition-colors">Contact</a>
		</nav>

		<!-- Right side buttons -->
		<div class="flex items-center gap-3">
			<button
				type="button"
				class="w-[82px] h-[40px] flex items-center justify-center bg-transparent text-black text-[15px] font-medium hover:bg-black/5 rounded-lg transition"
				on:click={onSignUpClick}
			>
				Sign Up
			</button>

			<button
				type="button"
				class="w-[101px] h-[40px] flex items-center justify-center bg-black text-white text-[15px] font-medium rounded-lg shadow-xs hover:bg-black/90 transition active:scale-[0.98]"
				on:click={onLogInClick}
			>
				Log In
			</button>
		</div>
	</header>

	<!-- Hero Content (moved up with -mt-[50px]) -->
	<main
		class="relative z-10 w-full flex flex-col items-center text-center px-4 -mt-[50px] my-auto"
	>
		<div class="flex flex-col items-center max-w-[800px]">
			<!-- Badge Component -->
			<div
				class="inline-flex items-center gap-2 p-1 pr-4 bg-white/80 backdrop-blur-md rounded-full border border-black/10 shadow-2xs mb-[34px] font-['Inter'] text-[14px]"
			>
				<span
					class="inline-flex items-center gap-1.5 bg-[#0e1311] text-white px-2.5 py-1 rounded-full font-medium text-xs"
				>
					<!-- Star Icon -->
					<svg class="w-3.5 h-3.5 text-yellow-400 fill-current" viewBox="0 0 24 24">
						<path
							d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
						/>
					</svg>
					New
				</span>
				<span class="text-black/80 font-normal">Discover what's possible</span>
			</div>

			<!-- Main Headline -->
			<h1
				class="font-['Fustat'] font-bold text-[48px] sm:text-[64px] md:text-[80px] tracking-[-4.8px] leading-none text-black mb-[34px] text-center"
			>
				Transform Data Quickly
			</h1>

			<!-- Subtitle -->
			<p
				class="font-['Fustat'] font-medium text-[16px] sm:text-[20px] tracking-[-0.4px] text-[#505050] max-w-[736px] w-full md:w-[542px] mb-[44px] leading-relaxed text-center"
			>
				Upload your information and get powerful insights right away. Work smarter and achieve
				goals effortlessly.
			</p>

			<!-- Search Input Box -->
			<div
				class="w-full max-w-[728px] h-auto min-h-[200px] bg-[rgba(0,0,0,0.24)] backdrop-blur-xl rounded-[18px] p-4 flex flex-col justify-between shadow-2xl border border-white/20"
			>
				<!-- Top Row: Credit info & AI badge -->
				<div
					class="flex items-center justify-between font-['Schibsted_Grotesk'] text-[12px] font-medium text-white mb-3"
				>
					<div class="flex items-center gap-2">
						<span>60/450 credits</span>
						<button
							class="px-2.5 py-0.5 rounded-full text-black font-semibold text-[11px] bg-[rgba(90,225,76,0.89)] hover:opacity-90 transition"
						>
							Upgrade
						</button>
					</div>

					<div class="flex items-center gap-1.5 text-white/90">
						<!-- AI Sparkle Icon -->
						<svg
							class="w-4 h-4 text-emerald-300"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</svg>
						<span>Powered by GPT-4o</span>
					</div>
				</div>

				<!-- Main Input Area -->
				<div class="relative w-full bg-white rounded-[12px] shadow-lg flex items-center p-2 mb-3">
					<input
						type="text"
						bind:value={questionText}
						placeholder="Type question..."
						class="w-full bg-transparent px-3 text-[16px] text-black placeholder:text-black/60 outline-hidden border-none font-['Inter']"
					/>
					<button
						type="button"
						class="w-[36px] h-[36px] shrink-0 bg-black text-white rounded-full flex items-center justify-center hover:bg-black/80 transition active:scale-95 shadow-md"
						on:click={onSignUpClick}
					>
						<!-- Up Arrow Icon -->
						<svg
							class="w-4 h-4"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2.5"
						>
							<path d="M12 19V5M5 12l7-7 7 7" stroke-linecap="round" stroke-linejoin="round" />
						</svg>
					</button>
				</div>

				<!-- Bottom Row: Action buttons & Counter -->
				<div class="flex items-center justify-between text-[12px]">
					<div class="flex items-center gap-2">
						<button
							type="button"
							class="flex items-center gap-1.5 px-3 py-1.5 bg-[#f8f8f8] hover:bg-white text-black/80 rounded-[6px] font-medium transition shadow-2xs"
						>
							<!-- Paperclip Icon -->
							<svg
								class="w-3.5 h-3.5 text-black/70"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
							<span>Attach</span>
						</button>

						<button
							type="button"
							class="flex items-center gap-1.5 px-3 py-1.5 bg-[#f8f8f8] hover:bg-white text-black/80 rounded-[6px] font-medium transition shadow-2xs"
						>
							<!-- Microphone Icon -->
							<svg
								class="w-3.5 h-3.5 text-black/70"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
							<span>Voice</span>
						</button>

						<button
							type="button"
							class="flex items-center gap-1.5 px-3 py-1.5 bg-[#f8f8f8] hover:bg-white text-black/80 rounded-[6px] font-medium transition shadow-2xs"
						>
							<!-- Search Icon -->
							<svg
								class="w-3.5 h-3.5 text-black/70"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
							>
								<circle cx="11" cy="11" r="8" /><path
									d="M21 21l-4.35-4.35"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
							<span>Prompts</span>
						</button>
					</div>

					<span class="text-white/80 font-['Schibsted_Grotesk'] text-[12px]">
						{questionText.length}/3,000
					</span>
				</div>
			</div>
		</div>
	</main>

	<!-- Footer Spacing -->
	<footer class="relative z-20 py-4 text-center text-xs text-black/50">
		© {new Date().getFullYear()} GUIDESOFT.WEB. All rights reserved.
	</footer>
</div>
