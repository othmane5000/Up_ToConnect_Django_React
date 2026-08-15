const searchInput = document.getElementById('search-input');
const suggestionsBox = document.getElementById('search-suggestions');

if (searchInput) {
    let debounceTimer;

    searchInput.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const query = this.value.trim();

        if (query.length < 2) {
            suggestionsBox.innerHTML = '';
            suggestionsBox.classList.remove('active');
            return;
        }

        // Attendre 300ms après la dernière frappe avant d'interroger le serveur
        debounceTimer = setTimeout(() => {
            fetch(`/recherche-live/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = '';

                    if (data.produits.length === 0) {
                        suggestionsBox.innerHTML = '<p class="no-result">Aucun produit trouvé</p>';
                    } else {
                        data.produits.forEach(produit => {
                            const item = document.createElement('a');
                            item.href = produit.url;
                            item.className = 'suggestion-item';
                            item.innerHTML = `
                                ${produit.image ? `<img src="${produit.image}" alt="">` : ''}
                                <div>
                                    <span class="suggestion-name">${produit.name}</span>
                                    <span class="suggestion-price">${produit.price} MAD</span>
                                </div>
                            `;
                            suggestionsBox.appendChild(item);
                        });
                    }

                    suggestionsBox.classList.add('active');
                })
                .catch(() => {
                    suggestionsBox.innerHTML = '';
                });
        }, 300);
    });

    // Fermer les suggestions si on clique ailleurs sur la page
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.search-wrapper')) {
            suggestionsBox.classList.remove('active');
        }
    });
}
// ===== RECALCUL LIVE DU PANIER =====
const qtyInputs = document.querySelectorAll('.qty-input');

if (qtyInputs.length > 0) {
    qtyInputs.forEach(input => {
        input.addEventListener('input', function () {
            const unitPrice = parseFloat(this.dataset.unitPrice);
            const quantity = parseInt(this.value) || 0;
            const subtotalElement = document.getElementById(this.dataset.subtotalTarget);

            if (subtotalElement) {
                const newSubtotal = (unitPrice * quantity).toFixed(2);
                subtotalElement.textContent = `${newSubtotal} MAD`;
                subtotalElement.dataset.value = newSubtotal;
            }

            recalculateCartTotal();
        });
    });
}

function recalculateCartTotal() {
    const allSubtotals = document.querySelectorAll('.panier-subtotal');
    let total = 0;

    allSubtotals.forEach(el => {
        total += parseFloat(el.dataset.value) || 0;
    });

    const totalElement = document.getElementById('cart-total');
    if (totalElement) {
        totalElement.textContent = `${total.toFixed(2)} MAD`;
    }
}