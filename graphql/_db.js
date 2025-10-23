// Dummy data for GraphQL server
// Allowed platforms: n64, ps1, ps2, xbox, snes, pc
const games = [
  { id: "g1", title: "Super Mario 64", platform: ["n64"], publisherId: "a1" },
  { id: "g2", title: "Mario Kart 64", platform: ["n64"], publisherId: "a2" },
  { id: "g3", title: "Donkey Kong Country", platform: ["snes"], publisherId: "a3" },
  { id: "g4", title: "GoldenEye 007", platform: ["n64"], publisherId: "a4" },
  { id: "g5", title: "Halo: Combat Evolved", platform: ["xbox"], publisherId: "a5" },
  { id: "g6", title: "Banjo-Kazooie", platform: ["n64"], publisherId: "a6" },
  { id: "g7", title: "Perfect Dark", platform: ["n64"], publisherId: "a7" },
  { id: "g8", title: "Halo 2", platform: ["xbox"], publisherId: "a8" },
  { id: "g9", title: "Half-Life", platform: ["pc"], publisherId: "a9" },
  { id: "g10", title: "Super Mario World", platform: ["snes"], publisherId: "a10" },
  { id: "g11", title: "Banjo-Tooie", platform: ["n64"], publisherId: "a1" },
  { id: "g12", title: "Donkey Kong Country 2", platform: ["snes"], publisherId: "a2" },
  { id: "g13", title: "Metal Gear Solid", platform: ["ps1"], publisherId: "a3" },
  { id: "g14", title: "Final Fantasy X", platform: ["ps2"], publisherId: "a4" },
  { id: "g15", title: "Halo: The Master Chief Collection", platform: ["xbox"], publisherId: "a5" },
  { id: "g16", title: "The Legend of Zelda: Ocarina of Time", platform: ["n64"], publisherId: "a6" }
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
  { id: "r1", gameId: "g1", authorId: "a2", rating: 5, content: "Groundbreaking 3D platforming — the camera and level design still hold up." },
  { id: "r2", gameId: "g1", authorId: "a3", rating: 4, content: "Great exploration and level design, some frame dips on original hardware." },
  { id: "r3", gameId: "g2", authorId: "a2", rating: 4, content: "Fast-paced and fun local multiplayer; drifting feels great." },
  { id: "r4", gameId: "g3", authorId: "a4", rating: 3, content: "Incredible SNES-era graphics and tight platforming challenges." },
  { id: "r5", gameId: "g4", authorId: "a1", rating: 5, content: "Legendary shooter with excellent single-player missions and iconic local multiplayer." },
  { id: "r6", gameId: "g4", authorId: "a5", rating: 4, content: "Multiplayer deathmatches are a blast — memorable maps and weapons." },
  { id: "r7", gameId: "g5", authorId: "a6", rating: 5, content: "Redefined console FPS; tight controls and unforgettable multiplayer." },
  { id: "r8", gameId: "g6", authorId: "a7", rating: 4, content: "Charming characters and inventive collect-a-thon gameplay." },
  { id: "r9", gameId: "g6", authorId: "a8", rating: 3, content: "Lots of collectibles; can feel grindy but very nostalgic." },
  { id: "r10", gameId: "g7", authorId: "a9", rating: 4, content: "Ambitious stealth shooter for its time with strong AI and mission variety." },
  { id: "r11", gameId: "g8", authorId: "a10", rating: 5, content: "Expanded the Halo formula with great maps and a gripping campaign." },
  { id: "r12", gameId: "g9", authorId: "a1", rating: 4, content: "A seminal PC shooter with immersive storytelling and level design." },
  { id: "r13", gameId: "g9", authorId: "a2", rating: 5, content: "Revolutionary for narrative FPS — still influential today." },
  { id: "r14", gameId: "g10", authorId: "a3", rating: 5, content: "A masterpiece of 2D platforming; tight controls and timeless levels." },
  { id: "r15", gameId: "g11", authorId: "a4", rating: 4, content: "Excellent follow-up with more worlds and polished mechanics." },
  { id: "r16", gameId: "g12", authorId: "a5", rating: 5, content: "Beautiful level design and excellent music — a strong sequel." },
  { id: "r17", gameId: "g13", authorId: "a6", rating: 5, content: "Groundbreaking stealth gameplay and cinematic storytelling." },
  { id: "r18", gameId: "g14", authorId: "a7", rating: 5, content: "Epic JRPG narrative with memorable characters and music." },
  { id: "r19", gameId: "g15", authorId: "a8", rating: 4, content: "A solid compilation — the remasters are a welcome update." },
  { id: "r20", gameId: "g16", authorId: "a9", rating: 5, content: "A landmark adventure; pioneering 3D Zelda gameplay and design." }
];

export default { games, authors, reviews };