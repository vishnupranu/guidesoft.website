<script lang="ts">
	import DOMPurify from 'dompurify';
	import { marked } from 'marked';

	import { toast } from 'svelte-sonner';
	import { fade, fly, slide } from 'svelte/transition';
	import { cubicOut } from 'svelte/easing';

	import { onMount, getContext, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { getBackendConfig } from '$lib/apis';
	import {
		ldapUserSignIn,
		getSessionUser,
		userSignIn,
		userSignUp,
		updateUserTimezone
	} from '$lib/apis/auths';

	import { WEBUI_API_BASE_URL, WEBUI_BASE_URL } from '$lib/constants';
	import { WEBUI_NAME, config, user, socket } from '$lib/stores';

	import { generateInitialsImage, canvasPixelTest, getUserTimezone } from '$lib/utils';

	import Spinner from '$lib/components/common/Spinner.svelte';
	import OnBoarding from '$lib/components/OnBoarding.svelte';
	import SensitiveInput from '$lib/components/common/SensitiveInput.svelte';
	import HeroSection from '$lib/components/HeroSection.svelte';

	const i18n = getContext('i18n');

	let loaded = false;

	let mode = $config?.features.enable_ldap ? 'ldap' : 'signin';

	let form = null;

	let name = '';
	let email = '';
	let password = '';
	let confirmPassword = '';

	let ldapUsername = '';

	const setSessionUser = async (sessionUser, redirectPath: string | null = null) => {
		if (sessionUser) {
			console.log(sessionUser);
			toast.success($i18n.t(`You're now logged in.`));
			if (sessionUser.token) {
				localStorage.token = sessionUser.token;
			}
			$socket.emit('user-join', { auth: { token: sessionUser.token } });
			await user.set(sessionUser);
			await config.set(await getBackendConfig());

			// Update user timezone
			const timezone = getUserTimezone();
			if (sessionUser.token && timezone) {
				updateUserTimezone(sessionUser.token, timezone);
			}

			if (!redirectPath) {
				redirectPath = $page.url.searchParams.get('redirect') || '/';
			}

			goto(redirectPath);
			localStorage.removeItem('redirectPath');
		}
	};

	const signInHandler = async () => {
		const sessionUser = await userSignIn(email, password).catch((error) => {
			toast.error(`${error}`);
			return null;
		});

		await setSessionUser(sessionUser);
	};

	const signUpHandler = async () => {
		if ($config?.features?.enable_signup_password_confirmation) {
			if (password !== confirmPassword) {
				toast.error($i18n.t('Passwords do not match.'));
				return;
			}
		}

		const sessionUser = await userSignUp(name, email, password, generateInitialsImage(name)).catch(
			(error) => {
				toast.error(`${error}`);
				return null;
			}
		);

		await setSessionUser(sessionUser);
	};

	const ldapSignInHandler = async () => {
		const sessionUser = await ldapUserSignIn(ldapUsername, password).catch((error) => {
			toast.error(`${error}`);
			return null;
		});
		await setSessionUser(sessionUser);
	};

	const submitHandler = async () => {
		if (mode === 'ldap') {
			await ldapSignInHandler();
		} else if (mode === 'signin') {
			await signInHandler();
		} else {
			await signUpHandler();
		}
	};

	const oauthCallbackHandler = async () => {
		function getCookie(name) {
			const match = document.cookie.match(
				new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1') + '=([^;]*)')
			);
			return match ? decodeURIComponent(match[1]) : null;
		}

		const token = getCookie('token');
		if (!token) {
			return;
		}

		const sessionUser = await getSessionUser(token).catch((error) => {
			toast.error(`${error}`);
			return null;
		});

		if (!sessionUser) {
			return;
		}

		localStorage.token = token;
		await setSessionUser(sessionUser, localStorage.getItem('redirectPath') || null);
	};

	let onboarding = false;

	onMount(async () => {
		const redirectPath = $page.url.searchParams.get('redirect');
		if ($user !== undefined) {
			goto(redirectPath || '/');
		} else {
			if (redirectPath) {
				localStorage.setItem('redirectPath', redirectPath);
			}
		}

		const error = $page.url.searchParams.get('error');
		if (error) {
			toast.error(error);
		}

		await oauthCallbackHandler();
		form = $page.url.searchParams.get('form');

		if ($config?.oauth?.auto_redirect && !form && !error) {
			const providers = Object.keys($config?.oauth?.providers ?? {});
			if (
				providers.length === 1 &&
				$config?.features?.auth !== false &&
				$config?.features?.enable_login_form === false &&
				!$config?.features?.enable_ldap &&
				!$config?.features?.auth_trusted_header &&
				!$config?.onboarding &&
				!localStorage.token &&
				!document.cookie.split('; ').some((c) => c.startsWith('token='))
			) {
				window.location.href = `${WEBUI_BASE_URL}/oauth/${providers[0]}/login`;
				return;
			}
		}

		loaded = true;

		if (($config?.features?.auth_trusted_header ?? false) || $config?.features?.auth === false) {
			await signInHandler();
		} else {
			onboarding = $config?.onboarding ?? false;
		}
	});
</script>

<svelte:head>
	<title>GUIDESOFT.WEB — Transform Data Quickly</title>
</svelte:head>

<OnBoarding
	bind:show={onboarding}
	getStartedHandler={() => {
		onboarding = false;
		mode = $config?.features.enable_ldap ? 'ldap' : 'signup';
	}}
/>

<div class="w-full min-h-screen bg-white text-black font-['Schibsted_Grotesk'] overflow-x-hidden" id="auth-page">
	{#if loaded}
		<!-- Left & Right Split Layout -->
		<div class="w-full min-h-screen flex flex-col lg:flex-row">
			<!-- LEFT SIDE: Hero Section with Looping Video & Interactive Showcase -->
			<div class="w-full lg:w-[58%] min-h-screen relative border-r border-black/10">
				<HeroSection
					onSignUpClick={() => (mode = 'signup')}
					onLogInClick={() => (mode = 'signin')}
				/>
			</div>

			<!-- RIGHT SIDE: Auth Card with Framer-motion style transitions -->
			<div class="w-full lg:w-[42%] min-h-screen bg-neutral-950 text-white flex flex-col justify-between p-8 sm:p-12 lg:p-16 relative overflow-hidden">
				<!-- Background Ambient Glow -->
				<div class="absolute -top-32 -right-32 w-96 h-96 bg-emerald-500/10 blur-[120px] rounded-full pointer-events-none"></div>
				<div class="absolute -bottom-32 -left-32 w-96 h-96 bg-blue-500/10 blur-[120px] rounded-full pointer-events-none"></div>

				<!-- Right Top Header -->
				<div class="flex items-center justify-between z-10">
					<div class="flex items-center gap-2">
						<img src="/static/favicon.png" alt="GS" class="w-7 h-7 rounded-full" />
						<span class="font-bold text-lg tracking-tight text-white">GUIDESOFT.WEB</span>
					</div>

					{#if $config?.features.enable_signup && !($config?.onboarding ?? false)}
						<button
							type="button"
							class="text-sm font-medium text-white/70 hover:text-white transition flex items-center gap-1"
							on:click={() => (mode = mode === 'signin' ? 'signup' : 'signin')}
						>
							<span>{mode === 'signin' ? 'Need an account?' : 'Have an account?'}</span>
							<span class="text-white font-semibold underline underline-offset-4 ml-1">
								{mode === 'signin' ? 'Sign Up' : 'Log In'}
							</span>
						</button>
					{/if}
				</div>

				<!-- Center Auth Form -->
				<div class="w-full max-w-md mx-auto my-auto z-10 py-8">
					{#if ($config?.features.auth_trusted_header ?? false) || $config?.features.auth === false}
						<div class="flex flex-col items-center justify-center gap-4 text-center py-12">
							<Spinner className="size-8 text-white" />
							<p class="text-lg font-medium text-white/80">
								{$i18n.t('Signing in to GUIDESOFT.WEB')}
							</p>
						</div>
					{:else}
						<!-- Animated Auth Container -->
						{#key mode}
							<div
								in:fly={{ y: 20, duration: 300, easing: cubicOut }}
								out:fade={{ duration: 150 }}
								class="flex flex-col gap-6"
							>
								<!-- Heading -->
								<div class="flex flex-col gap-1.5">
									<h2 class="text-3xl sm:text-4xl font-bold font-['Fustat'] tracking-tight text-white">
										{#if $config?.onboarding ?? false}
											Get Started with GUIDESOFT.WEB
										{:else if mode === 'ldap'}
											Sign In via LDAP
										{:else if mode === 'signin'}
											Welcome Back
										{:else}
											Create Your Account
										{/if}
									</h2>

									<p class="text-sm text-neutral-400 font-['Inter']">
										{#if mode === 'signin'}
											Enter your credentials to access your data workspace
										{:else if mode === 'signup'}
											Join GUIDESOFT.WEB and start transforming data instantly
										{:else}
											Authenticate with your organization credentials
										{/if}
									</p>
								</div>

								<!-- OAuth Providers -->
								{#if Object.keys($config?.oauth?.providers ?? {}).length > 0}
									<div class="grid grid-cols-1 gap-2.5">
										{#if $config?.oauth?.providers?.google}
											<button
												class="flex justify-center items-center gap-3 bg-white/5 hover:bg-white/10 border border-white/10 transition rounded-xl font-medium text-sm py-3 text-white"
												on:click={() => (window.location.href = `${WEBUI_BASE_URL}/oauth/google/login`)}
											>
												<svg class="w-5 h-5" viewBox="0 0 48 48">
													<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
													<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
													<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
													<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
												</svg>
												<span>Continue with Google</span>
											</button>
										{/if}

										{#if $config?.oauth?.providers?.microsoft}
											<button
												class="flex justify-center items-center gap-3 bg-white/5 hover:bg-white/10 border border-white/10 transition rounded-xl font-medium text-sm py-3 text-white"
												on:click={() => (window.location.href = `${WEBUI_BASE_URL}/oauth/microsoft/login`)}
											>
												<svg class="w-5 h-5" viewBox="0 0 21 21">
													<rect x="1" y="1" width="9" height="9" fill="#f25022"/>
													<rect x="1" y="11" width="9" height="9" fill="#00a4ef"/>
													<rect x="11" y="1" width="9" height="9" fill="#7fba00"/>
													<rect x="11" y="11" width="9" height="9" fill="#ffb900"/>
												</svg>
												<span>Continue with Microsoft</span>
											</button>
										{/if}

										{#if $config?.oauth?.providers?.github}
											<button
												class="flex justify-center items-center gap-3 bg-white/5 hover:bg-white/10 border border-white/10 transition rounded-xl font-medium text-sm py-3 text-white"
												on:click={() => (window.location.href = `${WEBUI_BASE_URL}/oauth/github/login`)}
											>
												<svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
													<path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.92 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57C20.565 21.795 24 17.31 24 12c0-6.63-5.37-12-12-12z"/>
												</svg>
												<span>Continue with GitHub</span>
											</button>
										{/if}
									</div>

									<div class="relative flex items-center justify-center my-2">
										<div class="w-full border-t border-white/10"></div>
										<span class="absolute bg-neutral-950 px-3 text-xs text-neutral-500 uppercase tracking-widest font-medium">or</span>
									</div>
								{/if}

								<!-- Main Form -->
								<form
									class="flex flex-col gap-4"
									on:submit={(e) => {
										e.preventDefault();
										submitHandler();
									}}
								>
									{#if mode === 'signup'}
										<div class="flex flex-col gap-1.5">
											<label for="name" class="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
												Full Name
											</label>
											<input
												bind:value={name}
												type="text"
												id="name"
												class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder:text-neutral-500 focus:outline-none focus:border-white/30 transition font-['Inter']"
												placeholder="Jane Doe"
												required
											/>
										</div>
									{/if}

									{#if mode === 'ldap'}
										<div class="flex flex-col gap-1.5">
											<label for="username" class="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
												Username
											</label>
											<input
												bind:value={ldapUsername}
												type="text"
												id="username"
												class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder:text-neutral-500 focus:outline-none focus:border-white/30 transition font-['Inter']"
												placeholder="ldap_username"
												required
											/>
										</div>
									{:else}
										<div class="flex flex-col gap-1.5">
											<label for="email" class="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
												Email Address
											</label>
											<input
												bind:value={email}
												type="email"
												id="email"
												class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder:text-neutral-500 focus:outline-none focus:border-white/30 transition font-['Inter']"
												placeholder="name@company.com"
												required
											/>
										</div>
									{/if}

									<div class="flex flex-col gap-1.5">
										<label for="password" class="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
											Password
										</label>
										<SensitiveInput
											bind:value={password}
											type="password"
											id="password"
											class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder:text-neutral-500 focus:outline-none focus:border-white/30 transition font-['Inter']"
											placeholder="••••••••••••"
											required
										/>
									</div>

									{#if mode === 'signup' && $config?.features?.enable_signup_password_confirmation}
										<div class="flex flex-col gap-1.5">
											<label for="confirm-password" class="text-xs font-semibold text-neutral-300 uppercase tracking-wider">
												Confirm Password
											</label>
											<SensitiveInput
												bind:value={confirmPassword}
												type="password"
												id="confirm-password"
												class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder:text-neutral-500 focus:outline-none focus:border-white/30 transition font-['Inter']"
												placeholder="••••••••••••"
												required
											/>
										</div>
									{/if}

									<button
										type="submit"
										class="w-full mt-2 py-3.5 bg-white text-black font-semibold text-sm rounded-xl hover:bg-neutral-200 transition active:scale-[0.99] shadow-lg shadow-white/5"
									>
										{mode === 'signin'
											? 'Sign In'
											: mode === 'ldap'
												? 'Authenticate'
												: ($config?.onboarding ?? false)
													? 'Create Admin Account'
													: 'Create Account'}
									</button>
								</form>

								{#if $config?.features.enable_ldap && $config?.features.enable_login_form}
									<button
										type="button"
										class="text-xs text-neutral-400 hover:text-white underline text-center transition"
										on:click={() => (mode = mode === 'ldap' ? 'signin' : 'ldap')}
									>
										{mode === 'ldap' ? 'Use Email Authentication' : 'Use LDAP Authentication'}
									</button>
								{/if}
							</div>
						{/key}
					{/if}
				</div>

				<!-- Right Bottom Footer -->
				<div class="z-10 text-xs text-neutral-500 flex items-center justify-between">
					<span>Privacy Policy & Terms</span>
					<span>v1.0.0</span>
				</div>
			</div>
		</div>
	{/if}
</div>
