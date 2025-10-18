// Dummy data for GraphQL server
const games = [
  { id: "g1", title: "Starfall Odyssey", platform: ["PC", "Xbox"] },
  { id: "g2", title: "Neon Drift", platform: ["PC", "PlayStation"] },
  { id: "g3", title: "Dungeon Bloom", platform: ["Switch"] },
  { id: "g4", title: "Skyline Racers", platform: ["PC", "PS5", "Xbox"] },
  { id: "g5", title: "Echoes of Ruin", platform: ["PC"] },
  { id: "g6", title: "Pixel Frontier", platform: ["PC", "Switch"] },
  { id: "g7", title: "Quantum Chef", platform: ["Mobile", "PC"] },
  { id: "g8", title: "Midnight Harbor", platform: ["PS5"] },
  { id: "g9", title: "Orbit Authority", platform: ["PC", "Xbox"] },
  { id: "g10", title: "Verdant Tales", platform: ["Switch", "PC"] }
];

const authors = [
  { id: "a1", name: "Riley Carter", verified: true },
  { id: "a2", name: "Samira Jones", verified: false },
  { id: "a3", name: "Luca Moreno", verified: true },
  { id: "a4", name: "Avery Patel", verified: false },
  { id: "a5", name: "Noah Kim", verified: true },
  { id: "a6", name: "Maya Singh", verified: false },
  { id: "a7", name: "Ethan Brooks", verified: true },
  { id: "a8", name: "Zoe Laurent", verified: false },
  { id: "a9", name: "Hiro Tanaka", verified: true },
  { id: "a10", name: "Gabriel Rossi", verified: false }
];

const reviews = [
  { id: "r1", gameId: "g1", authorId: "a1", rating: 5, content: "An unforgettable adventure with a beautiful soundtrack." },
  { id: "r2", gameId: "g2", authorId: "a2", rating: 4, content: "Great mechanics but a few pacing issues mid-game." },
  { id: "r3", gameId: "g3", authorId: "a3", rating: 3, content: "Fun in short bursts, lacks long-term depth." },
  { id: "r4", gameId: "g4", authorId: "a4", rating: 5, content: "Polished, addictive, and full of surprises." },
  { id: "r5", gameId: "g5", authorId: "a5", rating: 2, content: "Bugs made parts of the campaign frustrating." },
  { id: "r6", gameId: "g6", authorId: "a6", rating: 4, content: "Lovely art direction; multiplayer shines." },
  { id: "r7", gameId: "g7", authorId: "a7", rating: 1, content: "Controls felt unresponsive on some platforms." },
  { id: "r8", gameId: "g8", authorId: "a8", rating: 5, content: "One of the best narrative experiences this year." },
  { id: "r9", gameId: "g9", authorId: "a9", rating: 4, content: "Strong ideas; minor balancing issues." },
  { id: "r10", gameId: "g10", authorId: "a10", rating: 3, content: "Good moments but the ending was rushed." }
];

export default { games, authors, reviews };