<script lang="ts">
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { page } from '$app/stores';
	import { user } from '$lib/stores';

	import Chat from '$lib/components/chat/Chat.svelte';
	import LandingPage from '$lib/components/LandingPage.svelte';

	onMount(() => {
		if ($page.url.searchParams.get('error')) {
			toast.error($page.url.searchParams.get('error') || 'An unknown error occurred.');
		}
	});
</script>

{#if $user}
	<Chat />
{:else}
	<LandingPage />
{/if}
