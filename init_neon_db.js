// Script d'initialisation de la base de données Neon PostgreSQL
const { neon } = require('@neondatabase/serverless');
const fs = require('fs');
const path = require('path');

// Charger les variables d'environnement
const envPath = path.join(__dirname, 'backend', '.env');
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

const databaseUrl = process.env.DATABASE_URL;
const sql = neon(databaseUrl);

async function createTables() {
    try {
        console.log('🔄 Initialisation de la base de données Neon PostgreSQL...');

        // Créer la table user
        await sql`
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(128) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `;
        console.log('✅ Table "user" créée');

        // Créer la table crypto
        await sql`
            CREATE TABLE IF NOT EXISTS crypto (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                symbol VARCHAR(10) NOT NULL,
                quantity DECIMAL(20,8) NOT NULL,
                purchase_price DECIMAL(20,8) NOT NULL,
                current_price DECIMAL(20,8) DEFAULT 0,
                price_change_24h DECIMAL(10,4) DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE
            )
        `;
        console.log('✅ Table "crypto" créée');

        // Créer un index pour améliorer les performances
        await sql`
            CREATE INDEX IF NOT EXISTS idx_crypto_user_id ON crypto(user_id)
        `;
        await sql`
            CREATE INDEX IF NOT EXISTS idx_crypto_symbol ON crypto(symbol)
        `;
        console.log('✅ Index créés');

        // Vérifier les tables créées
        const tables = await sql`
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('user', 'crypto')
        `;

        console.log('📊 Tables dans la base de données:');
        tables.forEach(table => {
            console.log(`   - ${table.table_name}`);
        });

        console.log('🎉 Base de données initialisée avec succès !');

    } catch (error) {
        console.error('❌ Erreur lors de l\'initialisation:', error);
        process.exit(1);
    }
}

createTables();