<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	function getSentimentColor(compound: number): string {
		if (compound > 0.05) return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
		if (compound < -0.05) return 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200';
		return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200';
	}

	function getSentimentLabel(compound: number): string {
		if (compound > 0.05) return 'Positive';
		if (compound < -0.05) return 'Negative';
		return 'Neutral';
	}

	const avgSentiment = $derived(() => {
		const total = data.nameDetail.verses.reduce((acc, v) => acc + v.sentiment.compound, 0);
		return total / data.nameDetail.verses.length;
	});
</script>

<svelte:head>
	<title>{data.nameDetail.name} - Biblical Names Database</title>
</svelte:head>

<div class="min-h-screen bg-white dark:bg-gray-900 transition-colors">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<!-- Back Button -->
		<div class="mb-6">
			<a
				href="/"
				class="inline-flex items-center text-blue-600 dark:text-blue-400 hover:underline"
			>
				<svg class="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
					<path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
				</svg>
				Back to all names
			</a>
		</div>

		<!-- Header -->
		<header class="mb-8 p-6 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
			<h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
				{data.nameDetail.name}
			</h1>
			<div class="flex flex-wrap gap-4 text-sm">
				<div class="flex items-center gap-2">
					<span class="text-gray-600 dark:text-gray-400">Total mentions:</span>
					<span class="font-semibold text-gray-900 dark:text-white">
						{data.nameDetail.verses.length}
					</span>
				</div>
				<div class="flex items-center gap-2">
					<span class="text-gray-600 dark:text-gray-400">Average sentiment:</span>
					<span class="px-3 py-1 rounded font-medium {getSentimentColor(avgSentiment())}">
						{getSentimentLabel(avgSentiment())} ({avgSentiment().toFixed(2)})
					</span>
				</div>
			</div>
		</header>

		<!-- Verses List -->
		<div class="space-y-4">
			<h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
				All Verses
			</h2>
			{#each data.nameDetail.verses as verse, index}
				<article class="p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-500 transition-colors">
					<!-- Reference Header -->
					<div class="flex justify-between items-start mb-3">
						<h3 class="text-lg font-semibold text-blue-600 dark:text-blue-400">
							{verse.reference}
						</h3>
						<span class="px-2 py-1 rounded text-xs font-medium {getSentimentColor(verse.sentiment.compound)}">
							{getSentimentLabel(verse.sentiment.compound)}
						</span>
					</div>

					<!-- Verse Text -->
					<blockquote class="text-gray-700 dark:text-gray-300 mb-3 pl-4 border-l-4 border-gray-300 dark:border-gray-600">
						{verse.verse}
					</blockquote>

					<!-- Sentiment Details -->
					<div class="flex flex-wrap gap-3 text-xs text-gray-500 dark:text-gray-400">
						<div class="flex items-center gap-1">
							<span class="w-2 h-2 rounded-full bg-green-500"></span>
							<span>Positive: {(verse.sentiment.pos * 100).toFixed(0)}%</span>
						</div>
						<div class="flex items-center gap-1">
							<span class="w-2 h-2 rounded-full bg-gray-500"></span>
							<span>Neutral: {(verse.sentiment.neu * 100).toFixed(0)}%</span>
						</div>
						<div class="flex items-center gap-1">
							<span class="w-2 h-2 rounded-full bg-red-500"></span>
							<span>Negative: {(verse.sentiment.neg * 100).toFixed(0)}%</span>
						</div>
						<div class="flex items-center gap-1">
							<span>Compound: {verse.sentiment.compound.toFixed(3)}</span>
						</div>
					</div>
				</article>
			{/each}
		</div>
	</div>
</div>
