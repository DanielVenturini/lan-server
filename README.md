# Server-HTTP-with-Socket

Projeto para a disciplina de Desenvolvimento WEB: desenvolver um servidor HTTP 1.1 usando Socket. Este, será desenvolvido utilizando a linguagem Python.

Adições dos recursos (mais antigos por ultimo):

- Obtendo e retornando o header-field Content-Length.

- Começando a processar as caches de arquivos do método GET: If-Modified-Since implementado.

- Retornando requisições GET de arquivos de 128 em 128 bytes para não "afogar" o servidor com arquivos grandes.

- Agora está lançando uma thread para atender qualquer GET. Então quando um Socket se conectar, uma thread é lançada para atende-la e a thread principal continua a esperar outra conexão.

- Transformando o arquivo Server em uma classe.
