# HYDRA — Loja gamer DEMONSTRATIVA (Python 3.13 + Flask)

Projeto escolar. **Nada é real**: não há pagamento, cobrança, entrega de jogos ou códigos.

## Rodar no Windows
1. Instale o Python 3.13 (marque "Add Python to PATH").
2. Execute `instalar_windows.bat` e depois `iniciar_windows.bat`.
3. Abra http://127.0.0.1:5000

## Publicar no Render
Build: `pip install -r requirements.txt` · Start: `gunicorn app:app` · variável `SECRET_KEY` segura.

## O que tem
- **5 categorias** (menu, página inicial e página própria): Jogos, Gift Cards, Serviços de Otimização, Mods e Upamento de Contas — 29 produtos.
- **Imagens padronizadas**: jogos em poster vertical 3:4; demais itens em banner 16:10. Artes originais geradas por `tools/gerar_imagens.py` (sem capas/logos oficiais).
- **Carrinho com soma em tempo real**: adicionar sem recarregar a página, botões + / − / remover, total, contador no topo e mini-carrinho.
- **Cupons de teste**: `HYDRA10` (10%) e `ESCOLA20` (20%).
- **Checkout fake**: dados, Pix (QR ilustrativo) ou Cartão (visual), animação de "processando", tela de confirmação com nº do pedido (`HYD-000000`).
- **Suporte**: página `/suporte` com chat demonstrativo (respostas pré-programadas, botões rápidos, "digitando…").
- Cadastro/login (senha com hash) e histórico de pedidos demo em "Minha conta" (o checkout também funciona sem login).

## Apresentação (roteiro sugerido)
Home → categoria → adicionar itens → carrinho (+/−, cupom) → pagar (Pix/Cartão) → confirmação → Suporte (chat).

## Para editar produtos
Altere a lista `PRODUCTS` em `app.py`. Para regenerar as artes: `pip install pillow` e `python tools/gerar_imagens.py`.

## Limites
- Dados de cartão digitados no checkout não são enviados nem salvos (campos sem `name`).
- Não use senhas ou dados reais. SQLite em hospedagem gratuita pode ser apagado a cada reinício.
- O suporte 24h é só uma proposta do projeto.
