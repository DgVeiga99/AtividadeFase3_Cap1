# AtividadeFase3_Cap1

## Sistema de Irrigação Inteligente - Fase 3 - FarmTech Solutions

Este projeto faz parte da Fase 3 do desenvolvimento do sistema de gestão agrícola para a startup FarmTech Solutions. Nesta etapa, avançamos na criação de um sistema de irrigação inteligente capaz de monitorar e ajustar a irrigação de forma automatizada. Os dados são coletados a partir de sensores simulados na plataforma Wokwi.com e enviados para um banco de dados, onde são realizadas operações CRUD.

O sistema realiza monitoramento em tempo real dos seguintes parâmetros:

- **Níveis de nutrientes:** Fósforo (P) e Potássio (K), representados por botões (entrada digital).
- **pH do solo:** Representado por um sensor LDR (Light Dependent Resistor), fornecendo dados analógicos que simulam variações do pH.
- **Umidade do solo:** Representada pelo sensor DHT22.
- **Controle de irrigação:** Ativação e desativação da bomba d'água, simulada por um relé.

## Objetivo

Criar um sistema que conecte sensores a uma plataforma digital para otimizar a irrigação agrícola, garantindo que a água seja utilizada de maneira eficiente e que a produtividade da lavoura seja maximizada.

## Estrutura do Projeto

1. **Código ESP32 (C/C++):** Coleta os dados dos sensores e controla o estado do relé ( bomba de água).
2. **Código Python (main.py):** Realiza operações CRUD (criação, leitura, atualização e exclusão) em um banco de dados SQL com dados dos sensores.

## Desenho do Circuito Completo
![image](https://github.com/user-attachments/assets/d22dd3cf-049a-410a-b018-3cf9a8de76de)

O circuito foi montado no Wokwi.com que inclui os componentes:
- **Componentes**: ESP32, DHT22, botão azul, botão amarelo, LDR e relé.

### Descrição do papel de cada sensor no sistema
- **DHT22**: Monitora a umidade do solo.
- **Botão Azul**: simula o nivel dpo nutriente fósforo no solo, podendo estar normal ou baixo.
- **Botão Amarelo**: simula o nivel dpo nutriente potássio no solo, podendo estar normal ou baixa.
- **LDR**: Simula o monitoramento do pH do solo, lendo o valor de 0 a 14.
  
  
### Como Configurar e Rodar o Projeto no Wokwi e ESP32
Para conseguir realizar a configuração do projeto, basta acessar o link abaixo:
https://wokwi.com/projects/414264106495574017

Assim será possível ter acesso ao diagrama confeccionado e configurado

### Logica de funcionamento da bomba de água
Após realizar um estudo, identificamos condições específicas para acionar a irrigação, tanto isoladamente quanto acompanhada dos nutrientes em falta. A análise resultou na tabela verdade abaixo:

![image](https://github.com/user-attachments/assets/d7c53699-a115-4acc-9414-f4ccddeeb393)

Como resultado obtivemos a seguinte equação: **bomba = (umid < 80 || ((pH >= 6.5 && pH <= 7.5) && (fosf || pot)))**

Portanto o sistema de irrigação funcionará se a umidade estiver abaixo de 80% ou se o pH estiver correto e faltando fósforo ou potássio.

A razão para não realizar a irrigação em situações onde há deficiência de nutrientes, mas o pH está fora do intervalo ideal, é que, fora da faixa de 6.5 a 7.5, a absorção desses nutrientes é significativamente prejudicada. Assim, não é conveniente irrigar para repor os nutrientes nessas condições.

## Funcionalidades do Software Python:
O software oferece uma interação completa com um banco de dados, onde os dados dos registros dos sensores são armazenados e geridos. As funcionalidades incluem:

- **Cadastro de novos registros**: Adiciona novos registros ao banco de dados.
- **Atualização de registros**: Permite modificar as informações de registros já existentes.
- **Exclusão de registros**: Remove registros do banco de dados.
- **Consulta de registros**: Exibe todos os dados no banco.
- **Limpeza do banco de dados**: Exclui todos os dados do banco.
  
O sistema armazena e processa as seguintes informações de cada registro dos sensores:

-  **Data registrada (dd/mm/aaaa)**: Utilizado para controle de momento de registro dos dados
-  **Fosforo**: Nível do insumo presente no solo, classificado como normal ou baixo
-  **Potássio**: Nível do insumo presente no solo, classificado como normal ou baixo
-  **Umidade do solo (%)**: Quantidade de água presente no solo
-  **pH do solo**: Nível de pH atual do solo da plantação
-  **Bomba de água**: Status de funcionamento da bomba de água, classificada como ligada e desligada

### Bibliotecas para instalação
* oracledb -> utilizado para realizar os comandos com o bando de dados
* pandas -> utilizado para melhorar a apresentação dos dados no terminal 
* os -> responsável por realizar as limpezas no terminal do promp de comando

### Fluxograma do funcionamento

Inicializa o processo de conexão com o banco de dados. Se a conexão for bem sucedida, procede com o fluxo do software, caso contrario informa a mensagem de erro e finaliza o programa

Início – O programa inicia com uma mensagem de saudação e introdução.

Menu Inicial – O usuário escolhe uma das seguintes opções:

- Inserir registro;
- Atualizar registro;
- Excluir registro;
- Exibir dados registrados;
- Excluir dados registrados;
- Sair do programa.


Verificar opção escolhida – O software valida a escolha. Se a entrada for inválida, solicita uma nova.

Inserir novo registro (Opção 1)
- Solicita informações do registro (data, fosforo, potássio, umidade, etc.).
- Armazena o registro no sistema.

Atualizar registro (Opção 2)
- Solicita o número do ID do banco de dados para atualizar.
- Realiza a procura do ID selecionado informando sua existencia ou não
- Permite a atualização dos dados do registro selecionado.

Excluir lote (Opção 3)
- Solicita o número do ID do banco de dados a ser excluído.
- Realiza a procura do ID selecionado informando sua existencia ou não
- Remove o registro do sistema.

Exibir lotes registrados (Opção 4)
- Exibe todos os registros no sistema.

Excluir todos os lotes (Opção 5)
- Remove todos os registros no sistema.

Sair do programa (Opção 6)
- Encerra o programa com uma mensagem de despedida.

