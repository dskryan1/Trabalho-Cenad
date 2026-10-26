/* Chat de suporte DEMONSTRATIVO — respostas pré-programadas, sem servidor e sem IA. */
(() => {
  const body = document.getElementById('chat-body'), quick = document.getElementById('quick');
  const form = document.getElementById('chat-form'), input = document.getElementById('chat-text');

  const QUICK = ['Como pagar?', 'Prazo de entrega', 'Mods', 'Upamento de contas', 'Otimização de PC', 'Gift cards', 'Cupom de desconto', 'Falar com atendente'];

  // [palavras-chave], resposta
  const KB = [
    [['oi', 'ola', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'hello', 'eae'], 'Olá! 👋 Sou o Hydra Bot. Posso ajudar com pagamento, entrega, mods, otimização, gift cards e cupons. Escolha uma opção abaixo ou digite sua dúvida.'],
    [['pagar', 'pagamento', 'pix', 'cartao', 'cartão', 'boleto', 'parcel'], 'No checkout você escolhe <b>Pix</b> ou <b>Cartão</b>. Nesta versão demonstrativa os dois são <b>simulados</b>: nenhum valor é cobrado e nenhum dado de cartão é guardado.'],
    [['entrega', 'prazo', 'receber', 'chega', 'demora'], 'Na loja real a entrega seria <b>digital</b>, por e-mail, após a confirmação do pagamento. Aqui, por ser um projeto escolar, nenhum produto é entregue.'],
    [['mod', 'mods', 'textura', 'shader'], 'Na categoria <b>Mods</b> há pacotes para Minecraft e Skyrim, texturas HD, shaders e instalação assistida. Lembre-se: use mods apenas onde o jogo permitir. 🧩'],
    [['upamento', 'upar', 'nivel', 'nível', 'rank', 'conta', 'farm'], 'Em <b>Upamento de Contas</b> simulamos serviços de nível, rank, farm de recursos e missões. É apenas uma demonstração — na vida real, é importante respeitar os termos de cada jogo. 📈'],
    [['otimiz', 'fps', 'lento', 'travando', 'ping', 'formata', 'pc', 'driver'], 'Os <b>Serviços de Otimização</b> incluem limpeza, boost de FPS, ajuste de rede/ping, formatação e revisão de drivers. ⚡ Veja a categoria no menu.'],
    [['gift', 'cartao presente', 'cartão-presente', 'steam', 'xbox', 'playstation', 'google play', 'roblox', 'nintendo'], 'Os <b>Gift Cards</b> da loja são fictícios (Steam, PlayStation, Xbox, Google Play, Nintendo, Roblox) e servem só para mostrar o fluxo de compra. 🎁'],
    [['cupom', 'desconto', 'promo', 'codigo', 'código'], 'Teste os cupons <b>HYDRA10</b> (10% off) e <b>ESCOLA20</b> (20% off) na tela do carrinho. 🏷️'],
    [['reembolso', 'troca', 'devol', 'cancel'], 'Como não há cobrança real, não há reembolso. Em uma loja de verdade, a política de trocas e cancelamentos ficaria descrita nos Termos de Uso.'],
    [['senha', 'login', 'entrar', 'cadastr', 'conta hydra'], 'Você pode criar uma conta em <b>Cadastrar</b> para guardar seu histórico de pedidos. Use apenas dados fictícios e uma senha que não use em outros sites.'],
    [['atendente', 'humano', 'pessoa', 'telefone', 'email', 'e-mail'], 'Este chat é <b>demonstrativo</b> e não conecta a pessoas reais. 🙂 Na versão final do projeto, aqui entraria o atendimento humano.'],
    [['obrigad', 'valeu', 'tchau', 'ate mais', 'até mais'], 'De nada! Boas compras e bons jogos! 🎮'],
  ];
  const FALLBACK = 'Hmm, não encontrei essa resposta no meu roteiro de demonstração. 😅 Tente uma das opções rápidas abaixo ou use palavras como <i>pagamento, entrega, mods, gift card, cupom</i>.';

  const norm = s => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const time = () => new Date().toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'});
  const esc = s => s.replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));

  function add(who, html) {
    const d = document.createElement('div'); d.className = 'msg ' + who;
    d.innerHTML = `<div class="bubble">${html}<time>${time()}</time></div>`;
    body.appendChild(d); body.scrollTop = body.scrollHeight; return d;
  }
  function answer(text) {
    const n = norm(text);
    const words = n.split(/[^a-z0-9]+/);
    const hit = k => { const nk = norm(k); return nk.length <= 3 ? words.includes(nk) : n.includes(nk); };
    for (const [keys, resp] of KB) if (keys.some(hit)) return resp;
    return FALLBACK;
  }
  function botReply(text) {
    const t = document.createElement('div'); t.className = 'msg bot';
    t.innerHTML = '<div class="bubble typing"><i></i><i></i><i></i></div>'; body.appendChild(t); body.scrollTop = body.scrollHeight;
    setTimeout(() => { t.remove(); add('bot', answer(text)); }, 700 + Math.random() * 500);
  }
  function send(text) {
    text = text.trim(); if (!text) return;
    add('me', esc(text)); botReply(text);
  }

  function start() {
    body.innerHTML = '';
    add('bot', 'Olá! Eu sou o <b>Hydra Bot</b> 🐉<br>Este é um chat demonstrativo para o nosso trabalho escolar. Como posso ajudar?');
  }
  QUICK.forEach(q => { const b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.textContent = q; b.onclick = () => send(q); quick.appendChild(b); });
  form.addEventListener('submit', e => { e.preventDefault(); send(input.value); input.value = ''; input.focus(); });
  document.getElementById('chat-reset').addEventListener('click', start);
  start();
})();
