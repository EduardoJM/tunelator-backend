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
