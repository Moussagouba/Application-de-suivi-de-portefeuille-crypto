// Chart.js pour l'analyse du portefeuille crypto

console.log('Chart.js chargé avec succès');

// Graphique simple pour la répartition du portefeuille (placeholder)
function createAllocationChart() {
    const ctx = document.getElementById('allocationChart');
    if (!ctx) return;

    // Données exemple pour le graphique
    const cryptoNames = document.querySelectorAll('tbody tr').length;
    if (cryptoNames === 0) return;

    // Extraire les noms et valeurs des cryptomonnaies du tableau
    const names = [];
    const values = [];
    document.querySelectorAll('tbody tr').forEach(row => {
        names.push(row.cells[0].textContent);
        values.push(parseFloat(row.cells[5].textContent.replace('$', '').replace(',', '')));
    });

    const colors = generateColors(values.length);

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: names,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Répartition du Portefeuille',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Graphique simple pour la performance (placeholder)
function createPerformanceChart() {
    const ctx = document.getElementById('performanceChart');
    if (!ctx) return;

    // Extraire les symboles et profits/pertes du tableau
    const symbols = [];
    const profits = [];
    document.querySelectorAll('tbody tr').forEach(row => {
        symbols.push(row.cells[1].textContent);
        const profitText = row.cells[7].textContent.trim();
        const profitValue = parseFloat(profitText.replace('$', '').replace(',', ''));
        profits.push(profitValue);
    });

    const colors = profits.map(profit => profit >= 0 ? '#28a745' : '#dc3545');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: symbols,
            datasets: [{
                label: 'Profit/Perte ($)',
                data: profits,
                backgroundColor: colors,
                borderColor: colors.map(color => color),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Performance par Cryptomonnaie',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

// Générer des couleurs aléatoires
function generateColors(count) {
    const colors = [];
    const hueStep = 360 / count;

    for (let i = 0; i < count; i++) {
        const hue = i * hueStep;
        colors.push(`hsl(${hue}, 70%, 60%)`);
    }

    return colors;
}

// Animation des compteurs (placeholder)
function animateCounters() {
    const totalValueElement = document.querySelector('.total-value h2');
    if (totalValueElement) {
        const originalText = totalValueElement.textContent;
        const numericValue = parseFloat(originalText.replace(/[^\d.-]/g, ''));

        // Animation simple
        let currentValue = 0;
        const increment = numericValue / 50;
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= numericValue) {
                currentValue = numericValue;
                clearInterval(timer);
            }
            totalValueElement.textContent = 'Valeur Totale: $' + currentValue.toFixed(2);
        }, 30);
    }
}

// Auto-refresh des prix (toutes les 30 secondes)
function startPriceRefresh() {
    setInterval(function () {
        fetch('/api/refresh_prices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload(); // Recharger la page pour mettre à jour les prix
                }
            })
            .catch(error => {
                console.log('Erreur lors de la mise à jour des prix:', error);
            });
    }, 30000); // 30 secondes
}

// Initialisation quand le DOM est chargé
document.addEventListener('DOMContentLoaded', function () {
    // Créer les graphiques si les canvas existent
    createAllocationChart();
    createPerformanceChart();

    // Démarrer les animations
    animateCounters();

    // Démarrer la mise à jour automatique des prix
    startPriceRefresh();
});