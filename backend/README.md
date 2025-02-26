# Full Stack FastAPI & React

Este projeto é uma aplicação Full Stack utilizando **FastAPI**, **React**, **MongoDB** e **AWS LocalStack** para gerenciamento de produtos e pedidos.

## 🚀 Como Rodar o Projeto

### **1️⃣ Pré-requisitos**
- Docker e Docker Compose
- Python 3.8+
- Node.js 16+

### **2️⃣ Configuração do Banco de Dados**
```bash
docker-compose up -d
```
Isso irá iniciar o MongoDB e o backend automaticamente.

### **3️⃣ Populando o Banco de Dados**
```bash
python populate_db.py
```
Isso criará categorias, produtos e pedidos fictícios no MongoDB.

### **4️⃣ Executando o Backend**
```bash
uvicorn main:app --reload
```
A API estará disponível em `http://127.0.0.1:8000`.

### **5️⃣ Executando o Frontend**
```bash
cd frontend
npm install
npm start
```
A interface estará disponível em `http://localhost:3000`.

## 📊 Executando o Relatório de Vendas
Para gerar um relatório de vendas manualmente:
```bash
serverless invoke -f generateSalesReport
```
Isso criará um relatório no **S3 LocalStack** (`http://localhost:4566/relatorios-bucket/sales_report.json`).

## 📚 Documentação
- Acesse a **API Docs**: `http://127.0.0.1:8000/docs`
- Veja os **Componentes no Storybook**:
```bash
cd frontend
npm run storybook
