# Integração n8n com GitHub: Backup, Documentação e Evolução

Este documento detalha como integrar seus workflows do n8n com um repositório GitHub para garantir backup, versionamento, documentação e colaboração contínua.

## 1. Objetivo do Sistema

O objetivo principal é criar um repositório no GitHub (`meu-cerebro-digital`) para armazenar, versionar e proteger os workflows do n8n. Isso transforma seu sistema de automação em um ativo digital imortal, documentado e escalável.

## 2. Estrutura do Repositório

A estrutura recomendada para o repositório é a seguinte:

```
meu-cerebro-digital/
│
├── workflows/                  # Todos os workflows exportados como JSON
│   ├── venda-proposta.json
│   ├── atendimento-24h.json
│   ├── geracao-conteudo.json
│   ├── leitura-livros.json
│   └── workflow-unificado.json
│
├── prompts/                    # Prompts de IA usados nos workflows
│   ├── estilo-da-queen.txt
│   ├── educando-a-ia.txt
│   └── prompt-de-persuasao.txt
│
├── docs/                       # Documentação técnica
│   └── como-importar-no-n8n.md
│
└── README.md                   # Guia geral do sistema
```

## 3. Como Exportar um Workflow do n8n

Para exportar um workflow do n8n e salvá-lo no seu repositório GitHub, siga os passos abaixo:

1.  Abra o workflow desejado no n8n.
2.  Clique no menu de três pontos (⋯) no canto superior direito do workflow.
3.  Selecione a opção **Download as JSON**.
4.  Salve o arquivo `.json` resultante na pasta `workflows/` do seu repositório local (`meu-cerebro-digital/workflows/`).
5.  Realize um commit e push das alterações para o seu repositório GitHub.

## 4. Dica Avançada: Automatize o Backup

É altamente recomendável criar um workflow no próprio n8n para automatizar o backup dos seus workflows. Isso garante que suas automações estejam sempre seguras e versionadas.

Um exemplo de fluxo de backup automático seria:

*   **Gatilho**: Agenda (dispara diariamente, por exemplo, às 22h).
*   **Ação**: n8n exporta todos os workflows principais como JSON.
*   **Ação**: Salva os arquivos exportados em um serviço de armazenamento em nuvem (ex: Google Drive, em uma pasta "Backups Automáticos").
*   **Ação**: Executa um script (via Webhook ou GitHub Actions) que:
    *   Envia os arquivos JSON para o repositório GitHub.
    *   Realiza um commit com uma mensagem padronizada (ex: "Backup automático - {{ $now }}").

**Alternativa**: Utilize a ferramenta `n8n-workflow-exporter` para exportar todos os workflows de uma vez, simplificando o processo.

## 5. Benefícios Estratégicos

A integração do n8n com o GitHub oferece diversos benefícios estratégicos:

*   **Segurança**: Seus workflows estarão protegidos contra falhas locais, garantindo que nada se perca.
*   **Evolução**: Você poderá acompanhar a evolução dos seus workflows ao longo do tempo, visualizando as mudanças e revertendo para versões anteriores, se necessário.
*   **Colaboração**: Facilita a colaboração em equipe, permitindo que múltiplos desenvolvedores trabalhem nos mesmos workflows de forma organizada e segura.
*   **Profissionalismo**: Demonstra um alto nível de profissionalismo na gestão de seus sistemas de automação, transformando-os em ativos digitais valiosos.

## Conclusão

O n8n é o laboratório onde você cria suas automações, e o GitHub é a biblioteca onde você as preserva. Juntos, eles formam um sistema de inteligência ampliada e eterna, garantindo a longevidade e a escalabilidade do seu "Cérebro Digital da Queen".

