import type { PageLoad } from './$types';
import type { NameDetail } from '$lib/types';
import { error } from '@sveltejs/kit';

export const load: PageLoad = async ({ params, fetch }) => {
	try {
		const response = await fetch(`/data/names/${params.slug}.json`);

		if (!response.ok) {
			throw error(404, 'Name not found');
		}

		const nameDetail: NameDetail = await response.json();

		return {
			nameDetail
		};
	} catch (err) {
		throw error(404, 'Name not found');
	}
};
