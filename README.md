# 🏆 Projeto Bolão Copa 2026

Sistema de apostas entre amigos desenvolvido com foco em simplicidade e deploy automatizado.

## 🚀 Tecnologias Utilizadas
* **Lógica:** Python (Antigravity)
* **Interface:** HTML/CSS/JS (estático para GitHub Pages)
* **Versionamento:** GitHub Desktop
* **Hospedagem:** GitHub Pages

## 📂 Estrutura do Repositório
* `/src`: Código-fonte do motor do bolão.
* `/docs`: Arquivos de interface para o deploy no Pages.
* `data.json`: Base de dados simulada para as apostas.

## 🛠️ Como Contribuir
1. Clone o repositório via GitHub Desktop.
2. Crie uma branch para sua funcionalidade (`git checkout -b feature/nova-aposta`).
3. Commit suas alterações.
4. Faça o Push para o GitHub.

---

## 🔄 Fluxo de Trabalho: GitHub Desktop + Pages

Como você vai usar o GitHub Desktop, o processo fica muito visual. Aqui está o passo a passo:

### 1. Configuração Inicial
* Abra o GitHub Desktop e vá em **File > New Repository**.
* Nomeie como `bolao-copa-2026` e escolha o local no seu computador.
* Clique em **Publish Repository** para criar o link com o GitHub online.

### 2. O Ciclo de Desenvolvimento
* **Codifique:** Escreva suas funções no Antigravity.
* **Commit:** No GitHub Desktop, você verá os arquivos alterados na lateral esquerda. Escreva um resumo (ex: "Adicionada lógica de pontuação") e clique em **Commit to main**.
* **Push:** Clique em **Push origin** no topo para subir as alterações.

### 3. Deploy no GitHub Pages
O GitHub Pages é excelente para hospedar o front-end do seu bolão (onde os usuários marcam os palpites).
* No site do GitHub, vá em **Settings** do seu repositório.
* Clique na aba **Pages** (lateral esquerda).
* Em **Build and deployment**, selecione a branch `main` e a pasta `/root` (ou `/docs`).
* Salve. Em alguns minutos, seu bolão estará online no link `seu-usuario.github.io/bolao-copa-2026`.
