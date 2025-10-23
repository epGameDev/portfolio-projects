import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";

import { typeDefs } from "./schema.js";
import db from "./_db.js";

const PORT = 4000;
const resolvers = {
    Query: {
        games () {
            return db.games;
        },
        game(_, args) {
            return db.games.find(game => game.id === args.id);
        },
        authors () {
            return db.authors;
        },
        author(_, args) {
            return db.authors.find(author => author.id === args.id);
        },
        reviews () {
            return db.reviews;
        },
        review(_, args) { // Three types of params, (parent, args, {context object})
            return db.reviews.find((review) => review.id === args.id);
        }
    },
    Game: {
        reviews(parent) {
            return db.reviews.filter(review => review.gameId === parent.id );
        }
    },
    Author: {
        reviews(parent) {
            return db.reviews.filter(review => review.authorId === parent.id );
        }
    },
    Review: {
        author(parent) {
            return db.authors.find(author => author.authorId === parent.authorId );
        },
        game(parent) {
            return db.games.find(game => game.authorId === parent.gameId );
        }
    }
}


// // Server Setup
// const server = new ApolloServer({
//     // Type Definitions
//     typeDefs,
//     // Resolvers
//     resolvers
// });

// const { url } = await startStandaloneServer(server, {
//     listen: { port: PORT }
// })

// console.log(`Server is running on port ${PORT}`);


// query FetchReview($id: ID!, $gamesID: ID!, $authorID: ID!) {
//   # review(id: $id) {
//   #   rating,
//   #   content
//   # },
//   # author(id: $authorID) {
//   #   name,
//   #   verified
//   # },
//   game(id: $gamesID) {
//     id,
//     title,
//     platform,
//     reviews {
//       id,
//       rating,
//       content
//     }
//   },
//   author(id: $authorID) {
//     id,
//     name,
//     verified,
//     reviews {
//       id,
//       rating,
//       content,
//     }
//   }

// }