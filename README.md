---
title: BookMatch AI
emoji: 📚
colorFrom: purple
colorTo: blue
sdk: static
app_file: app.py
pinned: true
---

# 📚 BookMatch AI

Uma aplicação web de recomendação de livros com IA, desenvolvida com Python e Flask, integrada ao modelo Gemini da Google. 

Usuários criam um perfil com seus gêneros favoritos, tiram dúvidas e se informam sobre qualquer assunto no universo literário e recebem sugestões personalizadas de leitura. Tudo isso via chat com IA.

👉 [Teste agora no Hugging Face Spaces](https://huggingface.co/spaces/vioott/BookMatchAI-Python-GeminiAPI)

## 🔧 Tecnologias utilizadas

- 🐍 Python + Flask (back-end web)
- 🌐 HTML + CSS (front-end responsivo)
- 🤖 Google Gemini 1.5 Flash (modelo de IA)
- 🧠 Sistema de logging para histórico de interações

## ✨ Funcionalidades

- Criação e edição de perfis de usuário com preferências literárias
- Interface web responsiva para chat com IA
- Respostas personalizadas com base nas preferências salvas
- Log de interações com histórico e recomendações da IA

## 🚀 Como executar localmente

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/bookmatch-ai-python-geminiAPI.git
   cd bookmatch-ai-python-geminiAPI
   python -m venv venv
   source venv/bin/activate  
   # No Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ````

2. Crie um arquivo `.env` com sua chave da API Gemini:

   ```
   GOOGLE_API_KEY=sua-chave-aqui
   ```

3. Execute o app:

   ```
   python app.py
   ```

## 🧠 Sobre o projeto

Este projeto foi criado como solução para o exercício "Implementando um 'If Mágico' em uma Aplicação de E-commerce", do curso "IA para Programação com Python", da [Trybe](https://www.betrybe.com/), para explorar aplicações de IA generativa na recomendação literária, com foco em UX, personalização e uso real de modelos LLM. 

---

Desenvolvido por Vania Ioott – Full-Stack Developer & AI Enthusiast.
