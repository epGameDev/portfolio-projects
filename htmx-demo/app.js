import express from "express";
import {HTMX_KNOWLEDGE} from "./data/htmx-info.js";

const PORT = 8080
const app = express()

app.use(express.static('public'));

app.get("/", (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html>
            <head>
                <title>HTMX Essentials</title>
                <link
                href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"
                rel="stylesheet"/>
                <link rel="icon" href="/icon.png" />
                <script src="/htmx.js" defer></script>
                <link rel="stylesheet" href="/main.css" />
                <script src="/htmx-2-0-8.js" defer></script>
            </head>
            <body>
                <header id="main-header">
                <img src="/htmx-logo.jpg" alt="HTMX Logo" />
                <h1>Essentials</h1>
                </header>

                <main>
                <p>HTMX is a JavaScript library that you use without writing JavaScript code.</p>
                <form>
                    <p>
                        <label for="note">Your note</label>
                        <input type="text" id="note" name="note">
                    </p>
                    <p>
                        <button hx-get="/info" hx-target="ul" hx-trigger="mouseenter[ctrlKey]" hx-swap="beforeend">Save Note</button>
                    </p>
                </form>
                <ul>
                    ${HTMX_KNOWLEDGE.map((info) => `<li>${info}</li>`).join('')}
                </ul>
                </main>
            </body>
        </html>
        `)
}) 

app.get("/info", (req, res) => {
    res.send(`<h1>Fuck You!!!</h1>`)
})

app.listen(PORT)