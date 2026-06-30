// Inicializar AOS (si lo estás usando)
if (typeof AOS !== 'undefined') {
    AOS.init({
        duration: 1000,
        once: true,
        offset: 100
    });
}

// Carrito en localStorage
let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

// Auxiliar: obtener datos de producto desde la tarjeta
function obtenerProductoDesdeCard(card) {
    const $card = $(card);
    return {
        id: parseInt($card.data('id')),
        nombre: $card.data('nombre'),
        descripcion: $card.data('descripcion'),
        precio: parseFloat($card.data('precio')),
        imagen: $card.data('imagen')
    };
}

// Badge carrito
function actualizarContadorCarrito() {
    const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);
    const badge = document.querySelector('#cart-count');
    if (!badge) return;

    badge.textContent = totalItems;
}

// Dropdown carrito
function renderizarDropdownCarrito() {
    const container = $('#dropdown-carrito');
    if (!container.length) return;

    const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);
    const totalPrecio = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    if (totalItems === 0) {
        container.html(`
            <li>
                <div class="dropdown-item text-center py-3">
                    <h6 class="text-muted mb-1">Carrito vacío</h6>
                    <p class="mb-0 small">¡Añade productos!</p>
                </div>
            </li>
        `);
        return;
    }

    let html = `
        <li class="dropdown-header">
            <div class="d-flex justify-content-between align-items-center">
                <span>Tu carrito</span>
                <span class="badge bg-primary">${totalItems}</span>
            </div>
        </li>
    `;

    carrito.forEach(item => {
        html += `
            <li>
                <div class="dropdown-item p-2">
                    <div class="row align-items-center g-2">
                        <div class="col-3">
                            <img src="${item.imagen}" class="img-fluid rounded"
                                 style="width: 50px; height: 40px; object-fit: cover;">
                        </div>
                        <div class="col-6">
                            <h6 class="mb-0 small">${item.nombre}</h6>
                            <small class="text-success">$${item.precio.toLocaleString()}</small>
                        </div>
                        <div class="col-3 text-end">
                            <span class="badge bg-primary small">${item.cantidad}</span>
                        </div>
                    </div>
                </div>
            </li>
        `;
    });

    html += `
        <li><hr class="dropdown-divider"></li>
        <li>
            <div class="dropdown-item text-end p-2">
                <div class="d-flex justify-content-between align-items-center">
                    <span>Total:</span>
                    <strong>$${totalPrecio.toLocaleString()}</strong>
                </div>
            </div>
        </li>
        <li><hr class="dropdown-divider"></li>
        <li>
            <a class="dropdown-item text-center py-2" href="${window.CARRITO_URL}">
                <strong>Ver carrito completo →</strong>
            </a>
        </li>
    `;

    container.html(html);
}

// Carrito completo
function renderizarCarrito() {
    const container = $('#carrito-container');
    if (!container.length) return;

    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

    if (carrito.length === 0) {
        container.html(`
            <div class="text-center py-5">
                <h5 class="text-muted">Tu carrito está vacío</h5>
                <p>¡Añade productos desde la página de productos!</p>
            </div>
        `);
        const totalSpan = document.querySelector('#total-price');
        if (totalSpan) totalSpan.textContent = '0';
        return;
    }

    let html = '<div class="row g-3">';
    carrito.forEach(item => {
        html += `
            <div class="col-12">
                <article class="card bg-dark text-white">
                    <div class="card-body">
                        <div class="row align-items-center">
                            <div class="col-4 col-md-3">
                                <img src="${item.imagen}" class="img-fluid rounded" alt="${item.nombre}">
                            </div>
                            <div class="col-8 col-md-6">
                                <h6>${item.nombre}</h6>
                                <p class="mb-1">$${item.precio.toLocaleString()}</p>
                            </div>
                            <div class="col-12 col-md-3 text-end mt-2 mt-md-0">
                                <div class="input-group input-group-sm mb-1">
                                    <button class="btn btn-outline-secondary decrementar" data-id="${item.id}">-</button>
                                    <input type="number" class="form-control text-center" value="${item.cantidad}" readonly>
                                    <button class="btn btn-outline-secondary incrementar" data-id="${item.id}">+</button>
                                </div>
                                <button class="btn btn-sm btn-outline-danger eliminar-item" data-id="${item.id}">
                                    Eliminar
                                </button>
                            </div>
                        </div>
                    </div>
                </article>
            </div>
        `;
    });
    html += '</div>';

    container.html(html);
    const totalSpan = document.querySelector('#total-price');
    if (totalSpan) totalSpan.textContent = total.toLocaleString();
}

$(document).ready(function() {
    // Scroll suave en anclas
    $('a[href^="#"]').on('click', function(e) {
        const href = $(this).attr('href');
        if (href.startsWith('#') && href.length > 1) {
            e.preventDefault();
            const target = $(href);
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 80
                }, 800);
            }
        }
    });

    // Render inicial de carrito y dropdown
    renderizarCarrito();
    actualizarContadorCarrito();
    renderizarDropdownCarrito();

    // Agregar al carrito desde tarjetas de producto
    $(document).on('click', '.agregar-carrito', function() {
        const card = $(this).closest('.product-card');
        const producto = obtenerProductoDesdeCard(card);

        const itemExistente = carrito.find(item => item.id === producto.id);
        if (itemExistente) {
            itemExistente.cantidad++;
        } else {
            carrito.push({ ...producto, cantidad: 1 });
        }

        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarContadorCarrito();
        renderizarDropdownCarrito();
        renderizarCarrito();

        $(this)
            .addClass('animate__animated animate__tada')
            .delay(500)
            .queue(function() {
                $(this).removeClass('animate__tada').dequeue();
            });
    });

    // Incrementar / Decrementar / Eliminar
    $(document).on('click', '.incrementar', function() {
        const id = parseInt($(this).data('id'));
        const item = carrito.find(item => item.id === id);
        if (item) item.cantidad++;
        localStorage.setItem('carrito', JSON.stringify(carrito));
        renderizarCarrito();
        renderizarDropdownCarrito();
        actualizarContadorCarrito();
    });

    $(document).on('click', '.decrementar', function() {
        const id = parseInt($(this).data('id'));
        const item = carrito.find(item => item.id === id);
        if (item) {
            item.cantidad--;
            if (item.cantidad <= 0) carrito = carrito.filter(i => i.id !== id);
        }
        localStorage.setItem('carrito', JSON.stringify(carrito));
        renderizarCarrito();
        renderizarDropdownCarrito();
        actualizarContadorCarrito();
    });

    $(document).on('click', '.eliminar-item', function() {
        const id = parseInt($(this).data('id'));
        carrito = carrito.filter(item => item.id !== id);
        localStorage.setItem('carrito', JSON.stringify(carrito));
        renderizarCarrito();
        renderizarDropdownCarrito();
        actualizarContadorCarrito();
    });

    // Vaciar carrito
    const btnVaciar = document.querySelector('#vaciar-carrito');
    if (btnVaciar) {
        btnVaciar.addEventListener('click', () => {
            carrito = [];
            localStorage.setItem('carrito', JSON.stringify(carrito));
            renderizarCarrito();
            renderizarDropdownCarrito();
            actualizarContadorCarrito();
        });
    }
});