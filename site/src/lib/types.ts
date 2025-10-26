export interface Sentiment {
	neg: number;
	neu: number;
	pos: number;
	compound: number;
}

export interface NameSummary {
	name: string;
	count: number;
	sentiment: Sentiment;
}

export interface Verse {
	reference: string;
	verse: string;
	sentiment: Sentiment;
}

export interface NameDetail {
	name: string;
	verses: Verse[];
}
