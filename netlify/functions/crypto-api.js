// Netlify Function pour API Crypto
// Remplace les endpoints Flask avec API CoinGecko

const fetch = require('node-fetch');
const { neon } = require('@neondatabase/serverless');

// Charger les variables d'environnement pour le développement local
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

// Configuration de la connexion Neon avec connection pooling
// Utilise NETLIFY_DATABASE_URL (configuré par Neon) ou DATABASE_URL (développement local)
const databaseUrl = process.env.NETLIFY_DATABASE_URL || process.env.DATABASE_URL;
const sql = neon(databaseUrl, {
    connectionTimeoutMillis: 10000,
    idleTimeoutMillis: 30000,
    max: 10, // Connection pooling
});

exports.handler = async (event, context) => {
    const method = event.httpMethod;
    const path = event.path;

    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    };

    if (method === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: 'OK'
        };
    }

    try {
        // Routing des API endpoints
        if (path.includes('/crypto_price/')) {
            return await handleCryptoPrice(event, headers);
        } else if (path === '/search_crypto') {
            return await handleSearchCrypto(event, headers);
        } else if (path === '/portfolio_stats') {
            return await handlePortfolioStats(event, headers);
        } else if (path === '/market_data') {
            return await handleMarketData(event, headers);
        } else {
            return {
                statusCode: 404,
                headers,
                body: JSON.stringify({ error: 'API endpoint not found' })
            };
        }
    } catch (error) {
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

// Récupérer le prix d'une crypto
async function handleCryptoPrice(event, headers) {
    const symbol = event.path.split('/').pop();
    const coinId = getCoinId(symbol);

    try {
        const response = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${coinId}&vs_currencies=usd&include_24hr_change=true`);
        const data = await response.json();

        return {
            statusCode: 200,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                price: data[coinId]?.usd || 0,
                change_24h: data[coinId]?.usd_24h_change || 0
            })
        };
    } catch (error) {
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Failed to fetch price', message: error.message })
        };
    }
}

// Recherche de cryptomonnaies
async function handleSearchCrypto(event, headers) {
    const body = JSON.parse(event.body || '{}');
    const query = body.query || '';

    if (query.length < 2) {
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ results: [] })
        };
    }

    try {
        const response = await fetch(`https://api.coingecko.com/api/v3/search?query=${query}`);
        const data = await response.json();

        const results = data.coins?.slice(0, 10).map(coin => ({
            id: coin.id,
            name: coin.name,
            symbol: coin.symbol.toUpperCase(),
            image: coin.thumb
        })) || [];

        return {
            statusCode: 200,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ results })
        };
    } catch (error) {
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Search failed', message: error.message })
        };
    }
}

// Statistiques du portefeuille (version client-side)
async function handlePortfolioStats(event, headers) {
    // Version simplifiée - les données seront gérées côté client
    return {
        statusCode: 200,
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({
            total_value: 0,
            total_profit_loss: 0,
            total_invested: 0,
            profit_loss_percentage: 0,
            best_performer: null,
            worst_performer: null
        })
    };
}

// Données du marché
async function handleMarketData(event, headers) {
    const popularIds = ['bitcoin', 'ethereum', 'cardano', 'polkadot', 'chainlink',
        'litecoin', 'ripple', 'binancecoin', 'dogecoin', 'solana'];

    try {
        const response = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${popularIds.join(',')}&vs_currencies=usd&include_24hr_change=true`);
        const data = await response.json();

        const marketData = Object.entries(data).map(([id, info]) => ({
            name: id.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase()),
            symbol: id.toUpperCase(),
            current_price: info.usd || 0,
            price_change_24h: info.usd_24h_change || 0,
            image: `https://assets.coingecko.com/coins/images/1/large/${id}.png`
        }));

        return {
            statusCode: 200,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ market_data: marketData })
        };
    } catch (error) {
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Market data failed', message: error.message })
        };
    }
}

// Helper pour convertir symbole en ID CoinGecko
function getCoinId(symbol) {
    const mapping = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'ADA': 'cardano',
        'DOT': 'polkadot',
        'LINK': 'chainlink',
        'LTC': 'litecoin',
        'XRP': 'ripple',
        'BNB': 'binancecoin',
        'DOGE': 'dogecoin',
        'SOL': 'solana',
        'MATIC': 'matic-network',
        'AVAX': 'avalanche-2',
        'UNI': 'uniswap',
        'ATOM': 'cosmos',
        'VET': 'vechain',
        'FIL': 'filecoin',
        'TRX': 'tron',
        'ETC': 'ethereum-classic',
        'XLM': 'stellar',
        'BCH': 'bitcoin-cash'
    };

    return mapping[symbol.toUpperCase()] || symbol.toLowerCase();
}