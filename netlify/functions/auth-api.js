// Netlify Function pour l'authentification utilisateur
const { neon } = require('@neondatabase/serverless');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

// Charger les variables d'environnement
if (process.env.NODE_ENV !== 'production') {
    const fs = require('fs');
    const path = require('path');
    const envPath = path.join(__dirname, '../../.env');
    if (fs.existsSync(envPath)) {
        const envContent = fs.readFileSync(envPath, 'utf8');
        const envVars = envContent.split('\n').filter(line => line.includes('='));
        envVars.forEach(line => {
            const [key, ...valueParts] = line.split('=');
            const value = valueParts.join('=').trim();
            if (!process.env[key.trim()]) {
                process.env[key.trim()] = value;
            }
        });
    }
}

// Configuration de la connexion Neon
const databaseUrl = process.env.NETLIFY_DATABASE_URL || process.env.DATABASE_URL;
const sql = neon(databaseUrl, {
    connectionTimeoutMillis: 10000,
    idleTimeoutMillis: 30000,
    max: 10,
});

// Clé secrète pour JWT (utilise la même que Flask)
const JWT_SECRET = process.env.JWT_SECRET || process.env.SECRET_KEY || 'crypto_portfolio_jwt_secret_2025';

exports.handler = async (event, context) => {
    const method = event.httpMethod;
    const path = event.path;

    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
    };

    if (method === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: 'OK'
        };
    }

    try {
        // Routing des endpoints d'authentification
        if (path.includes('/register') && method === 'POST') {
            return await handleRegister(event, headers);
        } else if (path.includes('/login') && method === 'POST') {
            return await handleLogin(event, headers);
        } else if (path.includes('/profile') && method === 'GET') {
            return await handleProfile(event, headers);
        } else if (path.includes('/verify') && method === 'GET') {
            return await handleVerifyToken(event, headers);
        } else {
            return {
                statusCode: 404,
                headers,
                body: JSON.stringify({ error: 'Auth endpoint not found' })
            };
        }
    } catch (error) {
        console.error('Auth API Error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                error: 'Internal server error',
                message: error.message
            })
        };
    }
};

// Inscription d'un nouvel utilisateur
async function handleRegister(event, headers) {
    const { username, email, password } = JSON.parse(event.body || '{}');

    // Validation
    if (!username || !email || !password) {
        return {
            statusCode: 400,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Tous les champs sont requis' })
        };
    }

    if (password.length < 6) {
        return {
            statusCode: 400,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Le mot de passe doit contenir au moins 6 caractères' })
        };
    }

    try {
        // Vérifier si l'utilisateur existe déjà
        const existingUser = await sql`
            SELECT id FROM "user" WHERE username = ${username} OR email = ${email}
        `;

        if (existingUser.length > 0) {
            return {
                statusCode: 409,
                headers: { ...headers, 'Content-Type': 'application/json' },
                body: JSON.stringify({ error: 'Nom d\'utilisateur ou email déjà utilisé' })
            };
        }

        // Hacher le mot de passe
        const hashedPassword = await bcrypt.hash(password, 12);

        // Créer l'utilisateur
        const result = await sql`
            INSERT INTO "user" (username, email, password_hash, created_at)
            VALUES (${username}, ${email}, ${hashedPassword}, NOW())
            RETURNING id, username, email, created_at
        `;

        const user = result[0];

        // Générer le token JWT
        const token = jwt.sign(
            {
                userId: user.id,
                username: user.username,
                email: user.email
            },
            JWT_SECRET,
            { expiresIn: '7d' }
        );

        return {
            statusCode: 201,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: 'Utilisateur créé avec succès',
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    created_at: user.created_at
                },
                token
            })
        };
    } catch (error) {
        console.error('Registration error:', error);
        return {
            statusCode: 500,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Erreur lors de l\'inscription' })
        };
    }
}

// Connexion utilisateur
async function handleLogin(event, headers) {
    const { username, password } = JSON.parse(event.body || '{}');

    if (!username || !password) {
        return {
            statusCode: 400,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Nom d\'utilisateur et mot de passe requis' })
        };
    }

    try {
        // Récupérer l'utilisateur
        const users = await sql`
            SELECT id, username, email, password_hash, created_at
            FROM "user"
            WHERE username = ${username}
        `;

        if (users.length === 0) {
            return {
                statusCode: 401,
                headers: { ...headers, 'Content-Type': 'application/json' },
                body: JSON.stringify({ error: 'Identifiants incorrects' })
            };
        }

        const user = users[0];

        // Vérifier le mot de passe
        const isValidPassword = await bcrypt.compare(password, user.password_hash);

        if (!isValidPassword) {
            return {
                statusCode: 401,
                headers: { ...headers, 'Content-Type': 'application/json' },
                body: JSON.stringify({ error: 'Identifiants incorrects' })
            };
        }

        // Générer le token JWT
        const token = jwt.sign(
            {
                userId: user.id,
                username: user.username,
                email: user.email
            },
            JWT_SECRET,
            { expiresIn: '7d' }
        );

        return {
            statusCode: 200,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: 'Connexion réussie',
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    created_at: user.created_at
                },
                token
            })
        };
    } catch (error) {
        console.error('Login error:', error);
        return {
            statusCode: 500,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Erreur lors de la connexion' })
        };
    }
}

// Récupérer le profil utilisateur
async function handleProfile(event, headers) {
    const authHeader = event.headers.authorization || event.headers.Authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return {
            statusCode: 401,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Token d\'authentification requis' })
        };
    }

    const token = authHeader.substring(7);

    try {
        // Vérifier le token
        const decoded = jwt.verify(token, JWT_SECRET);

        // Récupérer les informations complètes de l'utilisateur
        const users = await sql`
            SELECT id, username, email, created_at
            FROM "user"
            WHERE id = ${decoded.userId}
        `;

        if (users.length === 0) {
            return {
                statusCode: 404,
                headers: { ...headers, 'Content-Type': 'application/json' },
                body: JSON.stringify({ error: 'Utilisateur non trouvé' })
            };
        }

        const user = users[0];

        // Récupérer les statistiques du portefeuille
        const cryptos = await sql`
            SELECT COUNT(*) as crypto_count,
                   COALESCE(SUM(quantity * current_price), 0) as total_value,
                   COALESCE(SUM(quantity * purchase_price), 0) as total_invested
            FROM crypto
            WHERE user_id = ${user.id}
        `;

        const stats = cryptos[0];

        return {
            statusCode: 200,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    created_at: user.created_at
                },
                portfolio: {
                    crypto_count: parseInt(stats.crypto_count),
                    total_value: parseFloat(stats.total_value),
                    total_invested: parseFloat(stats.total_invested),
                    total_profit_loss: parseFloat(stats.total_value) - parseFloat(stats.total_invested)
                }
            })
        };
    } catch (error) {
        console.error('Profile error:', error);
        return {
            statusCode: 401,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Token invalide ou expiré' })
        };
    }
}

// Vérifier la validité du token
async function handleVerifyToken(event, headers) {
    const authHeader = event.headers.authorization || event.headers.Authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return {
            statusCode: 401,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Token d\'authentification requis', valid: false })
        };
    }

    const token = authHeader.substring(7);

    try {
        const decoded = jwt.verify(token, JWT_SECRET);

        return {
            statusCode: 200,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                valid: true,
                user: {
                    userId: decoded.userId,
                    username: decoded.username,
                    email: decoded.email
                }
            })
        };
    } catch (error) {
        return {
            statusCode: 401,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ error: 'Token invalide ou expiré', valid: false })
        };
    }
}