import type { PageLoad } from './$types';
import type { NameSummary } from '$lib/types';

export const load: PageLoad = async ({ fetch }) => {
	const response = await fetch('/data/names-summary.json');
	const names: NameSummary[] = await response.json();

	return {
		names
	};
};
