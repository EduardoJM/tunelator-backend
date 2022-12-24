<h1 align="center">
    <p align="center">Tunelator</p>
</h1>

<p align="center">
    <img src="https://raw.githubusercontent.com/EduardoJM/tunelator-backend/main/.github/images/cover.png" alt="Redirecionando e-mails para ajudar você a cuidar da sua caixa de e-mails com foco na sua privacidade" />
</p>

---

<p align="center">
    <a href="https://github.com/EduardoJM/tunelator-backend/actions/workflows/tests.yml">
        <img src="https://github.com/EduardoJM/tunelator-backend/actions/workflows/tests.yml/badge.svg" alt="GitHub Actions status">
    </a>
    <a href="https://docs.python.org/3/library/unittest.html">
        <img src="https://img.shields.io/badge/tested%20with-unittest-green" alt="Tested with unittest">
    </a>
    <a href='https://coveralls.io/github/EduardoJM/tunelator-backend?branch=main'>
        <img src='https://coveralls.io/repos/github/EduardoJM/tunelator-backend/badge.svg?branch=main' alt='Coverage Status' />
    </a>
    <a href='https://github.com/EduardoJM/tunelator-backend/issues'>
        <img src='https://img.shields.io/github/issues-raw/EduardoJM/tunelator-backend' alt='Opened Issues' />
    </a>
    <a href='https://github.com/EduardoJM/tunelator-backend/blob/main/LICENSE'>
        <img src='https://img.shields.io/github/license/EduardoJM/tunelator-backend' alt='License' />
    </a>
</p>

## 1. Sobre

O Tunelator foi um projeto desenvolvido com o intuito de prover contas de e-mail com redirecionamento automático dos e-mails da conta de redirecionamento para a conta principal do usuário, evitando assim spans e garantindo maior privacidade ao usuário.

A diferença principal entre um e-mail de redirecionamento e um e-mail temporário é que o e-mail de redirecionamento ele não tem, necessariamente, um tempo de vida definido, podendo o redirecionamento ser desativado e reativado quando necessário.

O projeto, como um "MVP", entrou em produção com poucos usuários para testes e como foi encerrado ainda nessa fase, decidi abrir o código-fonte do projeto (back-end e front-end) no GitHub como um projeto pessoal.

## 2. Arquitetura de Operação Original

Nesse repositório, existem modificações para simplificar a execução do back-end localmente, devido ao fato de que o projeto foi aberto a fins de manter uma certa "história" da aplicação. Levando isso em consideração, vale, nesse momento, mostrar um breve diagrama da arquitetura da aplicação em operação.


### 2.1 Recebimento e Reenvio de E-mails

Para o recebimento dos e-mails, configuramos um servidor (em uma VPS da Digital Ocean por ter um preço acessível para projetos pequenos como esse) de e-mails com o Postfix e um *file watcher* de modo que quando um novo e-mail caia na pasta do usuário o mesmo era salvo e processado pelo back-end da aplicação.

Aqui, enfatizando, novamente, o tamanho da aplicação, o *file watcher* era executado pelo próprio back-end django e, ainda, para evitar e-mails perdidos que o *watcher* não conseguiu capturar, a cada 10 minutos uma tarefa em segundo plano (utilizando o *celery*) é executada passando um pente fino nas pastas para encontrar arquivos não processados.

Os e-mails são processados, são adicionados banner's indicando que o e-mail foi redirecionado/reenviado e alterado o destinatário, e reenviado por meio de um serviço de SMTP contratado.

<p align="center">
    <img src="https://raw.githubusercontent.com/EduardoJM/tunelator-backend/main/.github/images/arquitetura1.png" alt="Arquitetura do app original descrita acima" />
</p>

### 2.2 Usuários de E-mails

No servidor de e-mails, configurado com o Postfix, o usuário Linux é usado como usuário de e-mail. Dessa forma, foi criada uma aplicação, com Flask, apenas para servir de interface entre a aplicação original django e o sistema operacional do servidor de e-mails (disponível em [/usersystem](https://github.com/EduardoJM/tunelator-backend/tree/main/usersystem)).

<p align="center">
    <img src="https://raw.githubusercontent.com/EduardoJM/tunelator-backend/main/.github/images/arquitetura2.png" alt="Arquitetura do app original descrita acima" />
</p>

### 2.3 Storage e Background Tasks

Para storage de arquivos, em ambiente de produção, foi configurado um ambiente com o AWS S3 (Simple Storage Service), ver [Ref 1](#ref-1). Em ambiente local, foi utilizado o sistema de storage padrão do django salvando os arquivos em disco.

Para o *celery* e a execução de tarefas em segundo plano, em ambiente local, foi utilizada um container *REDIS* como broker. Já em produção, uma configuração para o uso do AWS SQS (Simple Queue Service) foi definida para o broker.

Essas configurações podem, e devem, ser definidas dentro do arquivo `/tunelator/.env`, conforme o arquivo de exemplos `/tunelator/.env.example`.

## 3. Alterações na Arquitetura para Ambientes Locais

Para a execução em ambientes locais, principalmente após encerrar o projeto, alguns pontos do item 2 foram alterados para facilitar a execução. Não temos o servidor de e-mails e, portanto, alguns pontos não fazem tanto sentido serem mantidos, como o *file watcher*. Dessa forma, o container do *file watcher* foi removido dos arquivos do `docker-compose`. Porém, em resumo, o trecho do `docker-compose` desse container é:

```yml
# ...

  watcher:
    build:
      context: .
      dockerfile: Dockerfile.tunelator
    entrypoint: ['./entrypoints/production/entrypoint.watcher.sh']
    networks:
      - tunelator
    volumes:
      - /home:/home
    depends_on:
      - "db"
      - "api"

# ...
```

Outro ponto é que a interface de comunicação entre o sistema operacional do servidor de e-mails e do back-end django, feito em Flask, pode ser utilizado dentro de um container (aqui há um **ponto de atenção**: as informações de usuários "salvas" não são preservadas) e a aplicação foi inserida nesse repositório em [/usersystem](https://github.com/EduardoJM/tunelator-backend/tree/main/usersystem) e dockerizada.

## Referências

<a id="ref-1"></a> 1 - [django-storages + S3: lidando com arquivos de mesmo nome](https://dev.to/eduardojm/django-storages-s3-lidando-com-arquivos-de-mesmo-nome-4eo1)

<a id="ref-2"></a> 2 - [Django + Celery: testando sistemas com filas](https://dev.to/eduardojm/django-celery-testando-sistemas-com-filas-3e1n)
