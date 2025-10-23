💰 SISTEMA DE CONTROLE FINANCEIRO PESSOAL — DJANGO DARK MODE

Descrição Geral
Sistema financeiro completo e automatizado desenvolvido em Django 5, com interface escura em tons de preto e amarelo.
Permite gerenciar receitas, despesas, investimentos e contas a pagar, com totalizadores mensais e gerais, além de automação inteligente de contas recorrentes.
O sistema cria automaticamente novas faturas recorrentes quando faltam 10 dias ou menos para o vencimento, sem necessidade de comandos manuais ou agendadores externos.

---

FUNCIONALIDADES PRINCIPAIS

• Cadastro de receitas, despesas e investimentos com data e valor.
• Controle de contas a pagar com status de pagamento e opção de recorrência.
• Criação automática de novas contas recorrentes diretamente na home.
• Painel com totalizadores gerais e mensais: saldo líquido, patrimônio total, despesas, investimentos e contas pendentes.
• Paginação automática nas listagens (20 registros por página).
• Interface escura moderna e responsiva, baseada em preto e amarelo.

---

ESTRUTURA DO PROJETO

core/
├── settings.py  (configurações principais do Django)
economia/
├── models.py  (modelos de Receita, Despesa, Investimento e ContasPagar)
├── views.py  (lógica de dashboard e automação de recorrência)
├── urls.py
├── templates/
│    ├── base.html
│    ├── home.html
│    ├── receitas.html
│    ├── despesas.html
│    ├── investimentos.html
│    └── contas.html
├── static/css/base.css
├── management/commands/
│    ├── seed_receitas.py
│    ├── gerar_recorrentes.py
│    └── outros scripts auxiliares

---

INSTALAÇÃO E EXECUÇÃO

1. Criar ambiente virtual:
   python -m venv venv

2. Ativar ambiente virtual:
   • Linux/Mac:  source venv/bin/activate
   • Windows:  venv\Scripts\activate

3. Instalar dependências:
   pip install -r requirements.txt

4. Aplicar migrações:
   python manage.py migrate

5. Executar o servidor local:
   python manage.py runserver

6. Acessar no navegador:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

AUTOMAÇÃO DE CONTAS RECORRENTES

O sistema identifica automaticamente contas com o campo “recorrente” ativo.
Se faltar 10 dias ou menos para o vencimento atual, ele gera uma nova conta com o mesmo valor, descrição e vencimento +30 dias.
Essa lógica roda toda vez que o usuário acessa a página inicial (home), sem precisar de cron jobs ou comandos manuais.

Exemplo de log no terminal:
[AUTO] 1 conta recorrente foi gerada automaticamente em 23/10/2025.

---

PALETA DE CORES DARK

Preto: #0e0e0e
Cinza Escuro: #1c1c1c
Cinza Claro: #2a2a2a
Branco: #f5f5f5
Amarelo: #FFD700
Vermelho: #FF5555

---

ROTEIRO DE USO

1. Cadastre receitas e despesas no menu superior.
2. Cadastre contas a pagar, marcando “Recorrente” quando for uma despesa fixa.
3. Acesse a página inicial para atualizar automaticamente as recorrentes.
4. Monitore os totais no painel principal e nos módulos mensais.

---

ROADMAP FUTURO

• Adicionar botão “Gerar Próximo Mês” manual na interface.
• Exibir mensagens visuais (toast) para novas faturas criadas.
• Adicionar alertas de contas vencidas e exportação CSV/Excel.
• Implementar gráficos interativos com Chart.js.
• Sistema multiusuário com autenticação e perfis.

---

DESENVOLVIDO POR
Wesurex
Desenvolvedor Full Stack • Especialista em automações
Versão 1.0 — 2025
