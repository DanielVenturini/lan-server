# Server-HTTP-with-Socket

Projeto para a disciplina de Desenvolvimento WEB: desenvolver um servidor HTTP 1.1 usando Socket. Este, será desenvolvido utilizando a linguagem Python.

Adições dos recursos (mais antigos por ultimo):

- Começando a processar as caches de arquivos do método GET.

- Retornando requisições GET de arquivos.

- Agora está lançando uma thread para atender qualquer GET. Então quando um Socket se conectar, uma thread é lançada para atende-la e a thread principal continua a esperar outra conexão. Assim possibilitando atender mais de uma conexão ao mesmo tempo.

- Transformando o arquivo Server em uma classe.
