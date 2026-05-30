# 🎉 Sistema de Controle de Despesas - Executável Windows

## ✅ Autenticação Implementada!

Seu sistema agora possui **autenticação segura com criptografia de senha**.

---

## 🔐 Segurança Implementada

### ✨ Melhorias Adicionadas
- ✅ **Autenticação com Usuário e Senha** - Cada usuário tem suas credenciais
- ✅ **Criptografia de Senhas (bcrypt)** - Senhas são criptografadas com hash seguro
- ✅ **Tela de Login** - Interface moderna e intuitiva
- ✅ **Registro de Usuários** - Criação de novos usuários na primeira execução
- ✅ **Logout Seguro** - Sair do sistema mantém os dados protegidos
- ✅ **Sessão de Usuário** - Exibe usuário logado na barra lateral

---

## 📦 Detalhes do Arquivo

- **Nome:** `Controle-Despesas.exe`
- **Localização:** `dist/Controle-Despesas.exe`
- **Tamanho:** ~42 MB
- **Ícone:** Personalizado com tema de controle de despesas (símbolo R$)
- **Tipo:** Aplicação GUI sem console (windowed)

---

## 🚀 Como Usar

### Primeira Execução
1. Clique duas vezes em `Controle-Despesas.exe`
2. Na tela de login, clique em **"Registrar Novo Usuário"**
3. Digite seu nome de usuário e senha (mínimo 4 caracteres)
4. Confirme a senha
5. Após registrar, use essas credenciais para fazer login

### Execuções Posteriores
1. Clique duas vezes em `Controle-Despesas.exe`
2. Digite seu usuário e senha
3. Clique em "Login"
4. Bem-vindo! ✨

### Fazer Logout
- Clique no botão **"🔓 Logout"** na barra lateral
- Você retornará à tela de login

---

## 🎨 Recursos Inclusos

✅ **Autenticação Segura** - Login com criptografia bcrypt
✅ **Dashboard Financeiro** com cards de receitas, despesas e saldo
✅ **Gráficos** - Pizza (Receitas vs Despesas) e Barras (Histórico Mensal)
✅ **CRUD Completo** - Adicionar, Editar, Listar e Excluir receitas/despesas
✅ **Exportação Excel** - 3 abas (Resumo, Receitas, Despesas)
✅ **Exportação PDF** - Relatório profissional com tabelas
✅ **Tema Moderno** - Interface limpa e intuitiva
✅ **Banco de Dados SQLite** - Armazenamento local dos dados

---

## 📁 Estrutura de Arquivos

```
dist/
├── Controle-Despesas.exe          ← Executável principal
└── ... (dependências incluidas)

projeto/
├── main.py                         ← Principal (com login integrado)
├── auth.py                         ← Novo: Autenticação e gerenciamento de usuários
├── database.py
├── requirements.txt
├── models/
│   ├── receitas.py
│   ├── despesas.py
├── views/
│   ├── login.py                   ← Novo: Interface de login
│   ├── dashboard.py
│   ├── graficos.py
│   └── ...
└── ... (arquivos fonte)
```

---

## 🔧 Dados Persistidos

### Banco de Dados Local
- **Arquivo:** `financeiro.db` (armazenado na pasta de execução)
- **Contém:** Usuários, receitas e despesas
- **Segurança:** Senhas são criptografadas com bcrypt

### Para Manter Seus Dados
- Mantenha os arquivos `financeiro.db` junto com o `.exe`
- Se quiser compartilhar com outro computador, copie `financeiro.db` também

### Para Resetar o Sistema
1. **Resetar Senha:** Use a mesma tela de registro para registrar novo usuário
2. **Resetar Tudo:** Delete `financeiro.db` (será recriado vazio)

---

## 📋 Dependências Incluídas

O executável inclui todas as dependências necessárias:
- ✅ tkinter (GUI)
- ✅ sqlite3 (Banco de dados)
- ✅ matplotlib (Gráficos)
- ✅ openpyxl (Excel)
- ✅ reportlab (PDF)
- ✅ ttkbootstrap (Tema)
- ✅ **bcrypt (Criptografia de senhas)** ← NOVO

**Não é necessário instalar nada!** O .exe é completamente autossuficiente.

---

## 🔐 Perguntas Frequentes sobre Segurança

### Q: Minhas senhas são realmente seguras?
**A:** Sim! Utilizamos bcrypt, um algoritmo criptográfico de hash de senha de classe empresarial. Mesmo que alguém acesse o arquivo `financeiro.db`, não conseguirá descriptografar as senhas.

### Q: E se eu esqueceu minha senha?
**A:** Você pode registrar um novo usuário clicando em "Registrar Novo Usuário" na tela de login. Infelizmente, senhas antigas não podem ser recuperadas (por segurança). Você pode deletar `financeiro.db` para resetar completamente.

### Q: Posso ter múltiplos usuários?
**A:** Sim! Cada usuário pode se registrar com sua própria senha. Clique em "Registrar Novo Usuário" para criar novos usuários.

### Q: E se múltiplos usuários acessarem, seus dados são separados?
**A:** Atualmente, todos os usuários veem os mesmos dados financeiros. Se você precisar de dados separados por usuário, avise-nos para uma próxima versão.

---

## 🆘 Troubleshooting

### O aplicativo não abre
- Verifique se tem espaço em disco (o .exe tem ~42 MB)
- Tente executar como Administrador (clique direito → "Executar como administrador")
- Verifique se o antivírus não está bloqueando a execução

### Erro "Usuário não encontrado"
- Verifique se digitou o nome de usuário correto
- Lembre-se que usuário/senha diferenciam maiúsculas de minúsculas
- Se esqueceu, registre um novo usuário

### Erro "Senha incorreta"
- Verifique se tem Caps Lock ligado
- Letras e números devem corresponder exatamente
- Se esqueceu, delete `financeiro.db` para resetar

### Banco de dados não persiste
- Verifique se tem permissão de escrita na pasta `dist/`
- Se usar rede compartilhada, tente salvar em pasta local
- Verifique se o arquivo `financeiro.db` não está marcado como somente leitura

---

## 🔄 Recompilação

Se você modificar o código Python e quiser recompilá-lo em .exe, execute:

```powershell
.\compilar.bat
```

Ou use o comando manual:
```powershell
pyinstaller --onefile --windowed --icon=app_icon.ico --name="Controle-Despesas" main.py
```

**⚠️ Importante:** Após recompilar, copie o arquivo `financeiro.db` para a pasta `dist/` para manter seus dados.

---

## 📝 Mudanças Recentes

### Versão 2.0 - Autenticação Adicionada
- ✨ Sistema de login com usuário e senha
- ✨ Criptografia bcrypt para senhas
- ✨ Tela de registro de novos usuários
- ✨ Botão de logout na interface
- ✨ Exibição do usuário logado na barra lateral
- 🔄 README.md atualizado com guia de autenticação

---

## 💡 Próximas Melhorias Sugeridas

Para futuras versões, considere:
- 🔄 Backup automático para nuvem
- 👥 Dados separados por usuário
- 📱 Versão web/mobile
- 🌍 Sincronização entre dispositivos
- 📊 Relatórios mais avançados

---

**Desenvolvido com Python 3.12 + PyInstaller + bcrypt**
