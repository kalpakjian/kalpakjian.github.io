/* ==========================================================================
   reel-taste/demo-data.js — 示範資料（虛構）

   兩個用途：
   1. REEL_DEMO_RECORDS：一組「假裝是你」的觀看紀錄，按一下就能看到完整流程。
   2. REEL_DEMO_CATALOG：候選片池的離線備援（連 data/catalog.json 都讀不到時）。

   全部是虛構的觀眾資料，不對應任何真人。metadata 為 TMDB 公開欄位的手抄快照，
   類型與年份可能與實際略有出入，僅供離線示範。
   ========================================================================== */
window.REEL_DEMO_RECORDS = [
  { title: 'Shogun', type: 'tv', date: '2026-10-21', completed: 1, rating: 9, ratingSource: 'user', genres: ['劇情', '戰爭'], lang: 'en', year: 2024, platform: 'Disney+' },
  { title: 'Chernobyl', type: 'tv', date: '2026-09-12', completed: 1, rating: 10, ratingSource: 'user', genres: ['劇情', '歷史'], lang: 'en', year: 2019, platform: 'HBO' },
  { title: 'Severance', type: 'tv', date: '2026-10-08', completed: 1, rating: 9, ratingSource: 'user', genres: ['科幻', '懸疑'], lang: 'en', year: 2022, platform: 'Apple TV' },
  { title: 'Dune: Part Two', type: 'movie', date: '2026-10-02', completed: 1, rating: 9, ratingSource: 'user', genres: ['科幻', '冒險'], lang: 'en', year: 2024, platform: 'HBO' },
  { title: 'Arrival', type: 'movie', date: '2026-08-19', completed: 1, rating: 9.5, ratingSource: 'user', genres: ['科幻', '劇情'], lang: 'en', year: 2016, platform: 'Prime' },
  { title: 'The Bear', type: 'tv', date: '2026-10-15', completed: 1, rating: 8, ratingSource: 'user', genres: ['劇情', '喜劇'], lang: 'en', year: 2022, platform: 'Disney+' },
  { title: 'Past Lives', type: 'movie', date: '2026-07-30', completed: 1, rating: 9, ratingSource: 'user', genres: ['愛情', '劇情'], lang: 'en', year: 2023, platform: 'Prime' },
  { title: 'Blue Eye Samurai', type: 'tv', date: '2026-09-28', completed: 1, rating: 9, ratingSource: 'user', genres: ['動畫', '動作'], lang: 'en', year: 2023, platform: 'Netflix' },
  { title: 'Oppenheimer', type: 'movie', date: '2026-06-11', completed: 1, rating: 8.5, ratingSource: 'user', genres: ['歷史', '劇情'], lang: 'en', year: 2023, platform: 'Prime' },
  { title: 'The Last Dance', type: 'tv', date: '2026-05-20', completed: 1, rating: 7.5, ratingSource: 'user', genres: ['紀錄片'], lang: 'en', year: 2020, platform: 'Netflix' },
  { title: 'Some Reality Show', type: 'tv', date: '2026-10-25', completed: 0.04, rating: null, ratingSource: 'none', genres: ['實境'], lang: 'en', year: 2024, platform: 'Netflix' },
  { title: 'A Random Romcom', type: 'movie', date: '2026-10-27', completed: 0.15, rating: null, ratingSource: 'none', genres: ['愛情', '喜劇'], lang: 'en', year: 2025, platform: 'Netflix' },
  { title: 'Old Western Classic', type: 'movie', date: '2024-03-02', completed: 1, rating: null, ratingSource: 'none', genres: ['西部'], lang: 'en', year: 1968, platform: 'Prime' },
  { title: 'Dark', type: 'tv', date: '2026-08-05', completed: 1, rating: 9, ratingSource: 'user', genres: ['科幻', '懸疑'], lang: 'de', year: 2017, platform: 'Netflix' },
  { title: 'Money Heist', type: 'tv', date: '2026-04-14', completed: 0.85, rating: 7, ratingSource: 'user', genres: ['犯罪', '驚悚'], lang: 'es', year: 2017, platform: 'Netflix' }
];

window.REEL_DEMO_CATALOG = [
  { title: 'Blade Runner 2049', type: 'movie', year: 2017, lang: 'en', genres: ['科幻', '劇情'], vote: 8.0, votes: 13000 },
  { title: 'Annihilation', type: 'movie', year: 2018, lang: 'en', genres: ['科幻', '懸疑'], vote: 6.9, votes: 8000 },
  { title: 'Ex Machina', type: 'movie', year: 2015, lang: 'en', genres: ['科幻', '驚悚'], vote: 7.7, votes: 12000 },
  { title: 'The Leftovers', type: 'tv', year: 2014, lang: 'en', genres: ['劇情', '奇幻'], vote: 8.3, votes: 3000 },
  { title: 'Station Eleven', type: 'tv', year: 2021, lang: 'en', genres: ['劇情', '科幻'], vote: 8.0, votes: 1500 },
  { title: 'The Terror', type: 'tv', year: 2018, lang: 'en', genres: ['歷史', '恐怖'], vote: 7.8, votes: 2200 },
  { title: 'Sicario', type: 'movie', year: 2015, lang: 'en', genres: ['驚悚', '犯罪'], vote: 7.6, votes: 14000 },
  { title: 'Nightcrawler', type: 'movie', year: 2014, lang: 'en', genres: ['犯罪', '驚悚'], vote: 7.8, votes: 11000 },
  { title: 'Prisoners', type: 'movie', year: 2013, lang: 'en', genres: ['犯罪', '懸疑'], vote: 8.1, votes: 16000 },
  { title: 'Perfect Days', type: 'movie', year: 2023, lang: 'ja', genres: ['劇情'], vote: 7.9, votes: 2500 },
  { title: 'Drive My Car', type: 'movie', year: 2021, lang: 'ja', genres: ['劇情'], vote: 7.6, votes: 3000 },
  { title: 'Monster', type: 'movie', year: 2023, lang: 'ja', genres: ['劇情', '懸疑'], vote: 7.6, votes: 2200 },
  { title: 'The Wailing', type: 'movie', year: 2016, lang: 'ko', genres: ['恐怖', '懸疑'], vote: 7.4, votes: 2600 },
  { title: 'Decision to Leave', type: 'movie', year: 2022, lang: 'ko', genres: ['懸疑', '愛情'], vote: 7.3, votes: 2400 },
  { title: 'Arcane', type: 'tv', year: 2021, lang: 'en', genres: ['動畫', '動作'], vote: 8.7, votes: 5000 },
  { title: 'Cyberpunk: Edgerunners', type: 'tv', year: 2022, lang: 'ja', genres: ['動畫', '科幻'], vote: 8.3, votes: 3200 },
  { title: 'Vinland Saga', type: 'tv', year: 2019, lang: 'ja', genres: ['動畫', '歷史'], vote: 8.5, votes: 2800 },
  { title: 'The Zone of Interest', type: 'movie', year: 2023, lang: 'de', genres: ['歷史', '劇情'], vote: 7.4, votes: 2800 },
  { title: 'Anatomy of a Fall', type: 'movie', year: 2023, lang: 'fr', genres: ['劇情', '懸疑'], vote: 7.6, votes: 3400 },
  { title: 'Parasite', type: 'movie', year: 2019, lang: 'ko', genres: ['驚悚', '劇情'], vote: 8.5, votes: 19000 },
  { title: 'The Handmaiden', type: 'movie', year: 2016, lang: 'ko', genres: ['驚悚', '劇情'], vote: 8.1, votes: 5000 },
  { title: 'Free Solo', type: 'movie', year: 2018, lang: 'en', genres: ['紀錄片'], vote: 8.1, votes: 3000 },
  { title: 'Jiro Dreams of Sushi', type: 'movie', year: 2011, lang: 'ja', genres: ['紀錄片'], vote: 7.9, votes: 2100 },
  { title: 'Planet Earth II', type: 'tv', year: 2016, lang: 'en', genres: ['紀錄片'], vote: 9.2, votes: 4000 },
  { title: 'Only Murders in the Building', type: 'tv', year: 2021, lang: 'en', genres: ['喜劇', '懸疑'], vote: 8.0, votes: 4500 },
  { title: 'Slow Horses', type: 'tv', year: 2022, lang: 'en', genres: ['驚悚', '劇情'], vote: 8.2, votes: 2600 },
  { title: 'Andor', type: 'tv', year: 2022, lang: 'en', genres: ['科幻', '劇情'], vote: 8.4, votes: 6000 },
  { title: 'Fallout', type: 'tv', year: 2024, lang: 'en', genres: ['科幻', '動作'], vote: 8.0, votes: 4800 },
  { title: 'The Last of Us', type: 'tv', year: 2023, lang: 'en', genres: ['劇情', '科幻'], vote: 8.4, votes: 8200 },
  { title: 'Silo', type: 'tv', year: 2023, lang: 'en', genres: ['科幻', '懸疑'], vote: 7.7, votes: 2300 },
  { title: 'Aftersun', type: 'movie', year: 2022, lang: 'en', genres: ['劇情'], vote: 7.5, votes: 2700 },
  { title: 'The Worst Person in the World', type: 'movie', year: 2021, lang: 'no', genres: ['劇情', '愛情'], vote: 7.5, votes: 2100 },
  { title: 'Another Round', type: 'movie', year: 2020, lang: 'da', genres: ['劇情', '喜劇'], vote: 7.6, votes: 3000 },
  { title: 'Interstellar', type: 'movie', year: 2014, lang: 'en', genres: ['科幻', '劇情'], vote: 8.4, votes: 36000 },
  { title: 'Prison Playbook', type: 'tv', year: 2017, lang: 'ko', genres: ['劇情', '喜劇'], vote: 8.6, votes: 1800 },
  { title: 'A Brighter Summer Day', type: 'movie', year: 1991, lang: 'zh', genres: ['劇情'], vote: 8.2, votes: 900 },
  { title: 'Yi Yi', type: 'movie', year: 2000, lang: 'zh', genres: ['劇情'], vote: 8.1, votes: 1200 },
  { title: 'Some Cheap Horror IX', type: 'movie', year: 2024, lang: 'en', genres: ['恐怖'], vote: 3.2, votes: 90 },
  { title: 'Low Rated Drama', type: 'movie', year: 2023, lang: 'en', genres: ['劇情'], vote: 5.1, votes: 400 }
];
