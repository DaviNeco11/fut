
# FHIRUT - Testes Automatizados para Recursos FHIR

**FHIRUT** (FHIR Unit Tester) é uma ferramenta desenvolvida para facilitar a criação, execução e verificação automatizada de testes de conformidade para recursos FHIR, utilizando o validador oficial `validator_cli.jar`.

---

## 🎯 Objetivo

Automatizar o processo de verificação de conformidade de instâncias FHIR, com geração e execução de casos de teste, validação automatizada com o validador HL7 e comparação dos resultados esperados com os obtidos.

---

## 📂 Estrutura do Projeto

```
fhirut/
├── main.py                         # Executa um teste específico
├── criar_casos_teste.py           # Gera novos casos de teste interativamente
├── validator_cli.jar              # (não incluído) precisa ser baixado manualmente
├── core/
│   ├── test_case.py               # Representa um caso de teste
│   ├── test_runner.py             # Roda o validador CLI
│   ├── result_comparator.py       # Compara resultado com o esperado
│   └── report_generator.py        # (Em desenvolvimento) Gera relatório de testes
└── tests/
    └── suite1/
        ├── test1.json             # Recurso FHIR de entrada
        └── test1_expected.json    # Resultado esperado
```

---

## ⚙️ Pré-requisitos

- Python 3.7+
- Java instalado
- [validator_cli.jar](https://github.com/hapifhir/org.hl7.fhir.core/releases) (precisa ser baixado manualmente)

---

## 🚀 Como usar

### 1. Criar um novo caso de teste

```bash
python criar_casos_teste.py
```

### 2. Executar um teste

```bash
python main.py
```

- Se o `expected.json` ainda não existir, ele será criado automaticamente com base no resultado da validação.
- Na segunda execução, o resultado será comparado com o esperado.

---

## 🧪 Resultado esperado no terminal

```bash
🚀 Executando o teste: test1
✅ Resultado salvo em: outputs/test1_result.json

📊 Resultado da comparação: ✅ TESTE APROVADO
 - Validação bem-sucedida e compatível com o esperado.
```

---

## 📥 Sobre o validator_cli.jar

Este projeto utiliza o [`validator_cli.jar`](https://github.com/hapifhir/org.hl7.fhir.core/releases) oficial da HL7 FHIR.  
Devido ao limite de tamanho do GitHub, o arquivo **não está incluso no repositório**.

Faça o download manual e coloque na raiz do projeto.

---

## 📌 Em desenvolvimento

- [ ] Execução automática de múltiplos testes
- [ ] Geração de relatórios completos
- [ ] Interface gráfica com Streamlit ou Tkinter
- [ ] Integração com CI/CD

---

## 👥 Contribuidores

- [@DaviNeco11](https://github.com/DaviNeco11)
- [@MathPaccheco](https://github.com/MathPaccheco)
- Equipe de desenvolvimento do projeto `fut`
