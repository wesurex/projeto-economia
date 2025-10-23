# 💰 Sistema de Controle Financeiro Pessoal — Django Dark Mode

Um sistema financeiro completo e automatizado, desenvolvido em **Django 5**, com design escuro elegante e funcionalidade profissional de **recorrência automática** de contas.

---

## 🧠 Visão Geral

O projeto oferece uma solução completa para controle financeiro pessoal.
Permite o gerenciamento de **receitas**, **despesas**, **investimentos** e **contas a pagar**, com cálculos automáticos e um painel de visualização de totais gerais e mensais.

A automação inteligente gera novas faturas recorrentes quando faltam **10 dias ou menos para o vencimento atual**, diretamente ao acessar a página inicial.

---

## ⚙️ Funcionalidades

| Módulo                        | Descrição                                       | Destaques                          |
| ----------------------------- | ----------------------------------------------- | ---------------------------------- |
| 📈 **Receitas**               | Cadastra entradas financeiras                   | Exibe totais mensais e gerais      |
| 💸 **Despesas**               | Registra gastos e deduz do saldo                | Pode ser vinculada a investimentos |
| 💼 **Investimentos**          | Gerencia aplicações e rendimentos               | Calcula patrimônio acumulado       |
| 🧲 **Contas a Pagar**         | Controla vencimentos e status                   | Suporte a recorrência automática   |
| 🔁 **Recorrência Automática** | Cria novas faturas com +30 dias                 | Totalmente autônoma, sem cron      |
| 🌙 **Interface Dark Mode**    | Visual moderno, preto e amarelo                 | Responsiva e agradável             |
| 📊 **Dashboard Inteligente**  | Exibe saldo líquido, investimentos e pendências | Cálculos automáticos e precisos    |

---

## 🧹 Estrutura do Projeto

```
economia/
 ├── models.py
 ├── views.py
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
```

---

## 🖥️ Instalação

1️⃣ Clone o repositório:

```bash
git clone https://github.com/seuusuario/financeiro-django.git
cd financeiro-django
```

2️⃣ Crie o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3️⃣ Instale as dependências:

```bash
pip install -r requirements.txt
```

4️⃣ Aplique as migrações:

```bash
python manage.py migrate
```

5️⃣ Inicie o servidor:

```bash
python manage.py runserver
```

Acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔁 Automação Inteligente de Contas Recorrentes

O sistema detecta contas com o campo `recorrente=True`.
Se faltar **10 dias ou menos** para o vencimento, ele gera automaticamente uma nova conta com vencimento **+30 dias**, evitando duplicatas.

Essa lógica roda **toda vez que o usuário acessa a home**, sem precisar de cron jobs externos.

Exemplo de log:

```
[AUTO] 1 conta recorrente foi gerada automaticamente em 23/10/2025.
```

---

## 🎨 Paleta Dark Mode

| Cor          | Função             | HEX       |
| ------------ | ------------------ | --------- |
| Preto        | Fundo principal    | `#0e0e0e` |
| Cinza escuro | Blocos e cartões   | `#1c1c1c` |
| Cinza claro  | Painéis e tabelas  | `#2a2a2a` |
| Branco       | Texto e contraste  | `#f5f5f5` |
| Amarelo      | Destaques e botões | `#FFD700` |
| Vermelho     | Alertas e despesas | `#FF5555` |

---

## 🧮 Totalizadores Exibidos na Home

* 💵 Total Líquido
* 💰 Patrimônio Total
* 📈 Total de Investimentos
* 💸 Despesas Mensais
* 🧲 Contas a Pagar e Pagas
* 🗕️ Saldo do Mês Atual

---

## 🧾 Roteiro de Uso

1. Cadastre receitas, despesas e investimentos.
2. Adicione contas a pagar e marque “Recorrente” quando for uma conta fixa.
3. Ao acessar a página inicial, o sistema criará automaticamente as faturas do próximo mês quando necessário.
4. Monitore os totais no painel.

---

## 🚀 Roadmap Futuro

* [ ] Botão manual “Gerar Próximo Mês”
* [ ] Alertas visuais de novas recorrências
* [ ] Exportação CSV/Excel
* [ ] Gráficos interativos com Chart.js
* [ ] Suporte multiusuário com autenticação

---

## 👨‍💻 Desenvolvido por

**Wesurex**
Desenvolvedor Full Stack • Especialista em automações
Versão 1.0 — 2025
