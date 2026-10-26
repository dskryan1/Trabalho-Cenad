/* Checkout FAKE: troca de abas, QR ilustrativo, máscara de cartão e animação de "processando". */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const form = $('#checkout-form');
  const tabs = [...document.querySelectorAll('input[name=method]')];
  const panels = {pix: $('#pay-pix'), cartao: $('#pay-cartao')};

  function sync() {
    const m = tabs.find(t => t.checked).value;
    for (const k in panels) panels[k].hidden = k !== m;
    document.querySelectorAll('.pay-tab').forEach(l => l.classList.toggle('on', l.querySelector('input').checked));
  }
  tabs.forEach(t => t.addEventListener('change', sync)); sync();

  // QR Code ilustrativo (padrão pseudoaleatório fixo — NÃO é um QR válido)
  const cv = $('#qr'), ctx = cv.getContext('2d'), N = 25, s = cv.width / N;
  let seed = 42; const rnd = () => (seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296;
  ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, cv.width, cv.height); ctx.fillStyle = '#0b0d12';
  const finder = (x, y) => { ctx.fillRect(x*s, y*s, 7*s, 7*s); ctx.fillStyle = '#fff'; ctx.fillRect((x+1)*s, (y+1)*s, 5*s, 5*s); ctx.fillStyle = '#0b0d12'; ctx.fillRect((x+2)*s, (y+2)*s, 3*s, 3*s); };
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
    const inF = (x < 8 && y < 8) || (x > N-9 && y < 8) || (x < 8 && y > N-9);
    if (!inF && rnd() > .52) ctx.fillRect(x*s, y*s, s, s);
  }
  finder(0, 0); finder(N-7, 0); finder(0, N-7);

  $('#copy-pix').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText($('#pix-code').textContent); } catch (_) {}
    toast('Código Pix demonstrativo copiado!');
  });

  // máscaras do cartão (visual)
  $('#cc-num').addEventListener('input', e => e.target.value = e.target.value.replace(/\D/g, '').slice(0, 16).replace(/(.{4})/g, '$1 ').trim());
  $('#cc-exp').addEventListener('input', e => { let v = e.target.value.replace(/\D/g, '').slice(0, 4); if (v.length > 2) v = v.slice(0, 2) + '/' + v.slice(2); e.target.value = v; });
  $('#cc-cvv').addEventListener('input', e => e.target.value = e.target.value.replace(/\D/g, '').slice(0, 3));

  // "pagamento": valida visualmente, mostra animação e então envia o pedido fictício
  let sent = false;
  form.addEventListener('submit', e => {
    if (sent) return;
    e.preventDefault();
    const name = $('#name').value.trim(), email = $('#email').value.trim();
    if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return toast('Informe nome e e-mail válidos (fictícios).', 'err');
    const method = tabs.find(t => t.checked).value;
    if (method === 'cartao' && (!$('#cc-num').value || !$('#cc-exp').value || !$('#cc-cvv').value)) return toast('Preencha os campos do cartão (fictícios).', 'err');
    const ov = $('#processing'); ov.hidden = false; $('#pay-btn').disabled = true;
    const steps = method === 'pix'
      ? ['Aguardando confirmação do Pix…', 'Pix confirmado (simulação) ✓']
      : ['Validando cartão fictício…', 'Pagamento aprovado (simulação) ✓'];
    $('#proc-title').textContent = steps[0];
    setTimeout(() => { $('#proc-title').textContent = steps[1]; $('.spinner', ov).classList.add('ok'); }, 1500);
    setTimeout(() => { sent = true; form.submit(); }, 2500);
  });
})();
