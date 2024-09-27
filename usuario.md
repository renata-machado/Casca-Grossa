# Criando um Cadastro de Usuário

Este documento apresenta os passos para implementação do cadastro de usuário em um projeto de aplicação web feito com Python+FastAPI+Jinja.

## Criação do Formulário

O primeiro passo é a criação/atualização do formulário de cadastro. O formulário deve conter todos os campos necessários para o cadastro inicial do usuário. É possível deixar alguns campos para serem cadastrados em um segundo momento, depois que o usuário já tiver cadastrado os dados principais no sistema.

Lembre-se que cada campo do formulário deve ter o atributo *name* preenchido adequadamente, sendo que esse valor será usado posteriormente pela rota que irá processar o formulário. Além disso, através do atributo *action*, o formulário deve apontar para a rota que irá processar o formulário, assim como, no atributo *method*, deve-se passar o valor *post* para indicar que os dados serão **enviados** para a rota em questão através do corpo da requisição.

## Criação dos Comandos SQL

Depois de criar o formulário, você deve criar os comandos SQL compatíveis com a estrutura de cadastro de usuários da sua aplicação, de acordo com o formulário de cadastro criado no passo anterior. Se o seu cadastro passa por momentos distintos para ser completamente preenchido, os campos que serão preenchidos *a posteriori* deve estar como opcionais no SQL de criação da tabela, ou seja, **não** podem ser "NOT NULL".

Além do comando SQL para criar a tabela, você também deve incluir o comando SQL para inserir um usuário, atualizar um usuário, alterar senha e outros necessários para o projeto, conforme exemplos feitos em sala. É importante notar que, se você tem uma parte do cadastro que é feita *a posteriori*, é necessário criar um comando SQL que atualize a tabela de usuários somente com estes dados.

## Criação da Classe Modelo

Depois de criar o SQL, crie uma classe do tipo *@dataclass* chamada `UsuarioModel` que tenha exatamente a mesma estrutura da tabela de usuários, definida no comando SQL de criação da tabela.

## Criação do Repositório

Depois de criar a classe modelo, deve-se criar um repositório (*usuario_repo.py*) contendo uma função para execução de cada cada comando SQL criado no arquivo SQL.