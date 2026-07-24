<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	let videoElement: HTMLVideoElement;
	let opacity = 0;
	let animationFrameId: number | null = null;
	let fadingOut = false;

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
	class="relative w-full h-full min-h-screen overflow-hidden flex flex-col justify-between bg-black text-white font-['Schibsted_Grotesk'] selection:bg-white selection:text-black"
>
	<!-- Cinematic Looping Video Background with custom rAF fade system -->
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
		<!-- Soft ambient dark gradient for video depth -->
		<div
			class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-black/40 pointer-events-none"
		/>
	</div>

	<!-- Clean minimal ambient branding watermark in bottom corner -->
	<div class="relative z-10 p-8 sm:p-12 mt-auto flex items-center justify-between">
		<div class="flex items-center gap-3 bg-black/40 backdrop-blur-md px-4 py-2 rounded-full border border-white/10">
			<img src="/static/favicon.png" alt="GS" class="w-6 h-6 rounded-full" />
			<span class="font-semibold text-sm tracking-tight text-white/90 font-['Schibsted_Grotesk']">
				GUIDESOFT.WEB
			</span>
		</div>
	</div>
</div>
