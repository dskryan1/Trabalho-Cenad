/* Hydra — carrinho, mini-carrinho, cupom e avisos (toast) */
const brl = v => new Intl.NumberFormat('pt-BR', {style: 'currency', currency: 'BRL'}).format(v);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

function toast(msg, type = 'ok') {
  const t = $('#toast'); if (!t) return;
  t.textContent = msg; t.className = 'toast show ' + type;
  clearTimeout(toast._t); toast._t = setTimeout(() => t.className = 'toast', 2600);
}

async function api(url, body) {
  const r = await fetch(url, {
    method: body === undefined ? 'GET' : 'POST',
    headers: {'Content-Type': 'application/json', 'X-Requested-With': 'fetch'},
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const data = await r.json().catch(() => ({}));
  return {ok: r.ok, data};
}

/* ---- atualiza todos os pontos da página que mostram o carrinho ---- */
function renderCart(c) {
  $$('[data-cart-count]').forEach(e => e.textContent = c.count);
  $$('[data-cart-total]').forEach(e => e.textContent = c.total_fmt);
  $$('[data-subtotal]').forEach(e => e.textContent = c.subtotal_fmt);
  $$('[data-discount]').forEach(e => e.textContent = '− ' + c.discount_fmt);
  $$('[data-coupon-name]').forEach(e => e.textContent = c.coupon || '');
  $$('[data-discount-row]').forEach(e => e.hidden = !c.discount);

  // mini-carrinho (coluna da direita)
  const mini = $('[data-mini-items]');
  if (mini) {
    mini.innerHTML = c.items.length
      ? c.items.map(i => `<div class="cart-mini-item"><img src="${i.image_url}" alt=""><div><b>${i.name} × ${i.qty}</b><small>${i.subtotal_fmt}</small></div></div>`).join('')
      : '<p>Seu carrinho está esperando sua próxima aventura.</p>';
  }

  // página do carrinho
  const page = $('#cart-page');
  if (page) {
    const ids = new Set(c.items.map(i => String(i.id)));
    $$('.cart-row', page).forEach(row => {
      if (!ids.has(row.dataset.id)) { row.classList.add('leaving'); setTimeout(() => row.remove(), 180); return; }
      const it = c.items.find(i => String(i.id) === row.dataset.id);
      $('[data-qty]', row).textContent = it.qty;
      $('[data-line]', row).textContent = it.subtotal_fmt;
    });
    $('#cart-empty').hidden = c.items.length > 0;
    $('#cart-filled').hidden = c.items.length === 0;
  }
}

/* ---- adicionar ao carrinho sem recarregar ---- */
document.addEventListener('submit', async e => {
  const form = e.target.closest('.add-form'); if (!form) return;
  e.preventDefault();
  const btn = $('button', form), old = btn.innerHTML;
  btn.disabled = true;
  try {
    const r = await fetch(form.action, {method: 'POST', headers: {'X-Requested-With': 'fetch'}});
    const d = await r.json();
    renderCart(d.cart); toast('✓ ' + d.message);
    btn.innerHTML = '✓ Adicionado';
  } catch (_) { toast('Não foi possível adicionar.', 'err'); }
  setTimeout(() => { btn.innerHTML = old; btn.disabled = false; }, 900);
});

/* ---- página do carrinho: + / − / remover ---- */
document.addEventListener('click', async e => {
  const b = e.target.closest('.cart-row [data-act]'); if (!b) return;
  const row = b.closest('.cart-row'), id = row.dataset.id;
  const cur = parseInt($('[data-qty]', row).textContent, 10);
  const qty = b.dataset.act === 'inc' ? cur + 1 : b.dataset.act === 'dec' ? cur - 1 : 0;
  if (qty > 10) return toast('Máximo de 10 unidades por produto.', 'err');
  const {data} = await api('/api/carrinho/' + id, {qty});
  renderCart(data);
  if (qty <= 0) toast('Item removido do carrinho.');
});

/* ---- cupom ---- */
const cf = $('#coupon-form');
if (cf) cf.addEventListener('submit', async e => {
  e.preventDefault();
  const {ok, data} = await api('/api/cupom', {code: $('#coupon-input').value});
  renderCart(data.cart); toast(data.message, ok ? 'ok' : 'err');
});

/* ---- mini-carrinho: carrega estado atual ---- */
if ($('[data-mini-items]')) api('/api/carrinho').then(r => renderCart(r.data));
