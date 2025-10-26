<script lang="ts">
	import { theme } from '$lib/stores/theme';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import type { NameSummary } from '$lib/types';

	let { data }: { data: PageData } = $props();

	let searchQuery = $state('');
	let sentimentFilter: 'all' | 'positive' | 'negative' | 'neutral' = $state('all');
	let sortBy: 'name' | 'frequency' | 'sentiment' = $state('frequency');

	onMount(() => {
		theme.init();
	});

	const filteredAndSortedNames = $derived.by(() => {
		let filtered = data.names;

		// Apply search filter
		if (searchQuery) {
			filtered = filtered.filter(name =>
				name.name.toLowerCase().includes(searchQuery.toLowerCase())
			);
		}

		// Apply sentiment filter
		if (sentimentFilter !== 'all') {
			filtered = filtered.filter(name => {
				if (sentimentFilter === 'positive') return name.sentiment.compound > 0.05;
				if (sentimentFilter === 'negative') return name.sentiment.compound < -0.05;
				if (sentimentFilter === 'neutral') return Math.abs(name.sentiment.compound) <= 0.05;
				return true;
			});
		}

		// Apply sorting
		const sorted = [...filtered];
		if (sortBy === 'name') {
			sorted.sort((a, b) => a.name.localeCompare(b.name));
		} else if (sortBy === 'frequency') {
			sorted.sort((a, b) => b.count - a.count);
		} else if (sortBy === 'sentiment') {
			sorted.sort((a, b) => b.sentiment.compound - a.sentiment.compound);
		}

		return sorted;
	});

	function getSentimentColor(compound: number): string {
		if (compound > 0.05) return 'text-green-600 dark:text-green-400';
		if (compound < -0.05) return 'text-red-600 dark:text-red-400';
		return 'text-gray-600 dark:text-gray-400';
	}

	function getSentimentLabel(compound: number): string {
		if (compound > 0.05) return 'Positive';
		if (compound < -0.05) return 'Negative';
		return 'Neutral';
	}
</script>

<div class="min-h-screen bg-white dark:bg-gray-900 transition-colors">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<!-- Header -->
		<header class="mb-8">
			<div class="flex justify-between items-center mb-4">
				<h1 class="text-4xl font-bold text-gray-900 dark:text-white">
					Biblical Names Database
				</h1>
				<button
					onclick={() => theme.toggle()}
					class="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
					aria-label="Toggle theme"
				>
					{#if $theme === 'dark'}
						<svg class="w-6 h-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
						</svg>
					{:else}
						<svg class="w-6 h-6 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
							<path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
						</svg>
					{/if}
				</button>
			</div>
			<p class="text-gray-600 dark:text-gray-400">
				Explore names from the Bible with sentiment analysis from their contextual verses
			</p>
		</header>

		<!-- Filters and Search -->
		<div class="mb-6 space-y-4">
			<!-- Search -->
			<div>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search names..."
					class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
				/>
			</div>

			<!-- Filters -->
			<div class="flex flex-wrap gap-4">
				<!-- Sentiment Filter -->
				<div class="flex-1 min-w-[200px]">
					<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
						Sentiment
					</label>
					<select
						bind:value={sentimentFilter}
						class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
					>
						<option value="all">All</option>
						<option value="positive">Positive</option>
						<option value="neutral">Neutral</option>
						<option value="negative">Negative</option>
					</select>
				</div>

				<!-- Sort By -->
				<div class="flex-1 min-w-[200px]">
					<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
						Sort By
					</label>
					<select
						bind:value={sortBy}
						class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
					>
						<option value="frequency">Frequency</option>
						<option value="name">Name (A-Z)</option>
						<option value="sentiment">Sentiment</option>
					</select>
				</div>
			</div>

			<!-- Results count -->
			<div class="text-sm text-gray-600 dark:text-gray-400">
				Showing {filteredAndSortedNames.length} of {data.names.length} names
			</div>
		</div>

		<!-- Names Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
			{#each filteredAndSortedNames as name}
				<a
					href="/name/{name.name.toLowerCase()}"
					class="block p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:shadow-lg hover:border-blue-500 dark:hover:border-blue-500 transition-all"
				>
					<div class="flex justify-between items-start mb-2">
						<h3 class="text-lg font-semibold text-gray-900 dark:text-white">
							{name.name}
						</h3>
						<span class="text-sm px-2 py-1 rounded bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
							{name.count}x
						</span>
					</div>
					<div class="flex items-center gap-2">
						<span class="text-sm font-medium {getSentimentColor(name.sentiment.compound)}">
							{getSentimentLabel(name.sentiment.compound)}
						</span>
						<span class="text-xs text-gray-500 dark:text-gray-400">
							({name.sentiment.compound.toFixed(2)})
						</span>
					</div>
					<div class="mt-2 flex gap-2 text-xs text-gray-500 dark:text-gray-400">
						<span>Pos: {(name.sentiment.pos * 100).toFixed(0)}%</span>
						<span>Neu: {(name.sentiment.neu * 100).toFixed(0)}%</span>
						<span>Neg: {(name.sentiment.neg * 100).toFixed(0)}%</span>
					</div>
				</a>
			{/each}
		</div>

		{#if filteredAndSortedNames.length === 0}
			<div class="text-center py-12 text-gray-500 dark:text-gray-400">
				No names found matching your criteria
			</div>
		{/if}
	</div>
</div>
