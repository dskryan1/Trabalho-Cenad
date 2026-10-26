# Hydra — site gamer em Python 3.13

Site demonstrativo com visual gamer escuro, catálogo filtrável, serviços e seção de suporte. Feito com Flask e preparado para deploy no Render.

## Rodar no Windows
1. Instale Python 3.13 e marque **Add Python to PATH** durante a instalação.
2. Extraia a pasta Hydra.
3. Execute `instalar_windows.bat` uma vez.
4. Depois execute `iniciar_windows.bat`.
5. Acesse http://127.0.0.1:5000.

## Rodar no Linux/macOS
No terminal, dentro da pasta:
```bash
chmod +x instalar_linux_mac.sh iniciar_linux_mac.sh
./instalar_linux_mac.sh
./iniciar_linux_mac.sh
```

## Publicar no Render
1. Envie os arquivos desta pasta para um repositório GitHub.
2. No Render, escolha **New + → Web Service** e conecte o repositório.
3. O `render.yaml` configura build `pip install -r requirements.txt`, comando `gunicorn app:app` e health check `/health`.
4. Se criar o serviço manualmente, use:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Runtime: Python 3.13, se disponível na configuração do serviço.
5. Após o deploy, use o endereço `.onrender.com` fornecido pelo Render.

## Antes de vender de verdade
- O catálogo, nomes e preços são exemplos; confirme disponibilidade e direitos de revenda.
- O botão de contato usa um e-mail de exemplo (`suporte@hydra.example`); troque pelo canal real.
- A seção fala em suporte 24h como meta, não como serviço já operacional. Configure equipe, escala e canais antes de prometer atendimento 24h.
- Esta versão é um site institucional/vitrine, não tem cadastro, pagamentos, estoque, carrinho nem entrega automática.
- Não colete senhas ou códigos de autenticação. Venda gift cards apenas por canais autorizados e respeite os termos das plataformas.
- Não ofereça boosting, mods ou ferramentas que violem os termos de jogos/anti-cheat.

## Estrutura
- `app.py`: aplicação Flask e catálogo de exemplo.
- `templates/index.html`: página principal.
- `static/style.css`: visual responsivo.
- `static/app.js`: filtros do catálogo.
- `requirements.txt`, `Procfile`, `runtime.txt`, `render.yaml`: configuração de execução/deploy.
