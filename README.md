# HYDRA — Loja gamer demonstrativa (Python 3.13)

Projeto escolar com identidade gamer vermelha/preta, arte gerada por IA, catálogo ilustrativo, cadastro/login, carrinho, checkout fictício e histórico de pedidos.

## Instalar no Windows
1. Instale Python 3.13 (marque “Add Python to PATH”).
2. Extraia a pasta do projeto.
3. Execute `instalar_windows.bat`.
4. Execute `iniciar_windows.bat`.
5. Acesse http://127.0.0.1:5000.

## Publicar no Render
1. Envie a pasta para um repositório GitHub.
2. No Render, crie um Web Service e conecte o repositório.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Configure `SECRET_KEY` como variável de ambiente segura.
6. Para guardar contas e pedidos de forma persistente em produção, configure um banco PostgreSQL gerenciado. SQLite no disco efêmero do serviço pode perder dados após redeploy/restart; o disco persistente depende do plano e da configuração do Render.

## Recursos
- Registro com hash de senha (Werkzeug), login e logout.
- Carrinho em sessão e ajuste de quantidades.
- Checkout demonstrativo sem cobrança.
- Histórico de pedidos demonstrativos por conta.
- Busca de catálogo e filtros por categoria.
- Arte visual gerada por IA incluída em `static/images`.

## Limites importantes
- Os gift cards, preços e produtos são fictícios e marcados como demonstração escolar.
- Não existe pagamento real, emissão de códigos ou entrega de produtos.
- Não use dados pessoais/senhas reais para testar.
- Antes de produção, adicione proteção CSRF, limitação de tentativas de login, verificação de e-mail, política de privacidade, termos, gateway de pagamento e banco persistente.
- O suporte 24h é uma ideia do projeto, não um atendimento já ativo.
- A arte gerada por IA é ilustrativa; não representa capas oficiais nem garante direitos de revenda.
