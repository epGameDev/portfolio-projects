export const  typeDefs = `#graphql

type Game {
    id: ID!,
    title: String!,
    platform: [String!]!,   # [String!]! Requires a string value
    reviews: [Review!]      # [Review!] optional value, but has to be of type review if any.
},

type Review {
    id: ID!,
    rating: Int!,
    content: String!,
    game: Game!,
    author: Author!,
},

type Author {
    id: ID!,
    name: String!,
    verified: Boolean!,
    reviews: [Review!]
},

# Entry point (Required)
type Query {
    reviews: [Review]     ,      # Fetches all the reviews
    review(id: ID!): Review  ,  # Fetches single review by ID, () creates a variable, '!' Means it is required
    games: [Game],
    game(id: ID!): Game,
    authors: [Author],
    author(id: ID!): Author,
},

`