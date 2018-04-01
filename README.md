# Server-HTTP-with-Socket

Projeto para a disciplina de Desenvolvimento WEB: desenvolver um servidor HTTP 1.1 usando Socket. Este, será desenvolvido utilizando a linguagem Python.

Adições dos recursos (mais antigos por ultimo):

- Interface de navegação apresenta os campos File(Name), Size - com seus respectivos tamanhos em bytes, kB, MB e GB. Quando pasta, este valor não é informado - e Last Modified.

- Interface para navegaçao pronto.

- Correçao de erros de geraçao de Mymetypes desconhecidos, da geraçao do index incorreto e caminhos no index linkavam para lugar incorreto por causa do '.'

- Interface criada para navegação entre os diretórios. Basta fazer uma requisição para 127.0.0.1:port/subpath/subsubpath ...

- Gerando o index.html para qualquer requisição de path.

- Atualizada a função de retorno do 404 Not Found.

- Quando pela primeira vez o Cliente se conecta com o Servidor, o Servidor retorna um Cookie "count=0", que é incrementado a cada conexão com o Servidor.

- Começando a processar as caches de arquivos do método GET: If-Modified-Since e If-Unmodified-Since implementado.

- Obtendo e retornando o header-field Content-Length, Content-Type e Last-Modified.

- Retornando requisições GET de arquivos de 128 em 128 bytes para não "afogar" o servidor com arquivos grandes.

- Agora está lançando uma thread para atender qualquer GET. Então quando um Socket se conectar, uma thread é lançada para atende-la e a thread principal continua a esperar outra conexão.

- Transformando o arquivo Server em uma classe.
