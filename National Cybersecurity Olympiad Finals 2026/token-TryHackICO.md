# Token - TryHackICO

## Solution TL;DR
Using the [algorithm confusion attack](https://portswigger.net/web-security/jwt/algorithm-confusion), modify a JWT token to perform privilege escalation and obtain the flag.

## Information
- **CTF:** National Cybersecurity Olympiad (Finals) 2026 - Singapore
- **Challenge name:** *Token*
- **Challenge series:** *TryHackICO*
- **Date:** *March 2026*

## Approach
The challenge endpoint brings us to a CTFd like website, where we can create/login to an account as well as view 3 challenges. Interacting with the website, we notice that we can only view the flag if our account has admin privileges. 

Through inspection of the provided `app.js` code (full code in appendix), it seems that the server checks for admin privileges using a [JWT token](https://en.wikipedia.org/wiki/JSON_Web_Token). However, the code for issuing and verifying the JWT token seems to be rather suspicious as the server only issues keys signed with the `RS256` algorithm, while it attempts to decode keys signed with the `HS256`, `RS256`, `ES256` and `PS256` algorithms.
```js
const decodeToken = (token) => {
    try {
        return jwt.verify(token, PUBLIC_KEY, { algorithms: ["HS256", "RS256", "ES256", "PS256"] });
    } catch (e) {
        return null;
    }
};

const encodeToken = (payload) => {
    return jwt.sign(payload, PRIVATE_KEY, { algorithm: 'RS256', expiresIn: '30m' });
};
```

Furthermore, the server also seems to expose the public key associated with JWT signature. This is normal as the public key can be used to verify the signatures of JWT tokens issued by this particular server.
```js
app.get("/public.pem", (req, res) => res.sendFile("public.pem", {root: __dirname}));
```

The presence of the above leaves the web app vulnerable to [algorithm confusion attacks](https://portswigger.net/web-security/jwt/algorithm-confusion), where the server signs a JWT token using an asymmetric signing algorithm (in this case `RS256`) but accepts tokens signed with symmetric signing algorithms (in this case `HS256`). For symmetric signing algorithms, since the key used to sign and verify the tokens is the same, we can simply use the obtained public key to sign and create a valid token with the `admin` field set to true, thereby elevating our privilege.

We are now able to read the flag.

## Flag
```NCO26{h0peful1y_ICO_w0nt_be_h4ck3d}```

## Tags
- NCO 2026
- Web
- JSON web token
- Algorithm confusion attack

## References
1. https://portswigger.net/web-security/jwt/algorithm-confusion
2. https://en.wikipedia.org/wiki/JSON_Web_Token

## Appendix - `app.js`
```js
const express = require('express');
const jwt = require('jsonwebtoken');
const sqlite = require('better-sqlite3');
const bcrypt = require('bcrypt');
const cookieParser = require('cookie-parser');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const FLAG = 'FAKE_FLAG';
const ADMIN_PASSWORD = 'password';

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.set('view engine', 'ejs');

const PRIVATE_KEY = fs.readFileSync('private.pem');
const PUBLIC_KEY = fs.readFileSync('public.pem');

const challenges = [
    { name: "Warmup", author: "admin", description: "Welcome to the ICO.", flag: "ICO{welcome_to_2026}" },
    { name: "Feedback", author: "admin", description: "Provide feedback.", flag: "ICO{thank_you_for_your_feedback}" },
    { name: "NCO", author: "NCO", description: "Real NCO challenge", flag: FLAG }
];

// --- Database Setup ---
const db = new sqlite('ico.db');
db.exec(`
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
`);

const adminExists = db.prepare("SELECT * FROM users WHERE username = ?").get('admin');
if (!adminExists) {
    const hashedPw = bcrypt.hashSync(ADMIN_PASSWORD, 10);
    db.prepare("INSERT INTO users (username, password) VALUES (?, ?)").run('admin', hashedPw);
}

const decodeToken = (token) => {
    try {
        return jwt.verify(token, PUBLIC_KEY, { algorithms: ["HS256", "RS256", "ES256", "PS256"] });
    } catch (e) {
        return null;
    }
};

const encodeToken = (payload) => {
    return jwt.sign(payload, PRIVATE_KEY, { algorithm: 'RS256', expiresIn: '30m' });
};

app.get('/', (req, res) => {
    res.render('front_page');
});

app.get('/challenges', (req, res) => {
    const token = req.cookies.auth;
    const auth = decodeToken(token);

    if (!auth) {
        return res.redirect('/login');
    }

    const displayed = challenges.map(c => {
        let chal = { ...c };
        if (!auth.admin) {
            chal.flag = "Only admins can see the flag!";
        }
        return chal;
    });

    res.render('CTFd', { challenges: displayed });
});

app.get('/login', (req, res) => res.render('login', { error: null }));

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const user = db.prepare("SELECT * FROM users WHERE username = ?").get(username);

    if (user && bcrypt.compareSync(password, user.password)) {
        const token = encodeToken({
            user: user.username,
            admin: user.id === 1
        });

        res.cookie('auth', token, { httpOnly: true });
        return res.redirect('/challenges');
    }
    
    res.render('login', { error: "Invalid username or password." });
});

app.get("/public.pem", (req, res) => res.sendFile("public.pem", {root: __dirname}));

app.get('/register', (req, res) => res.render('register', { error: null }));

app.post('/register', (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.render('register', { error: "Username and password are required." });
    }

    const hashedPw = bcrypt.hashSync(password, 10);

    try {
        db.prepare("INSERT INTO users (username, password) VALUES (?, ?)").run(username, hashedPw);
        res.redirect('/login'); 
    } catch (err) {
        res.render('register', { error: "Invalid username or already taken!" });
    }
});

app.listen(5000, () => {
    console.log('Server running on http://localhost:5000');
});
```
---
*Written on 28-03-2026 by gr*