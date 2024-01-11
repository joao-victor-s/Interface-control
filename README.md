# Main

## Ativação do Ambiente Virtual:

Antes de executar o código, ative o ambiente virtual usando o seguinte comando:

```bash
source ic-labrei/bin/activate
```

## Instalação de Requisitos:

Certifique-se de que todas as bibliotecas necessárias estão instaladas executando o seguinte comando:

```bash
pip install -r requirements.txt
```

## Execução do Código:

Para rodar o código, utilize o seguinte comando:

```bash
sudo ic-labrei/bin/python3 main.py
```

Lembre-se de ter permissões de superusuário ("sudo") para execução, caso necessário.

# Containers e MQTT

## Inicie os containers Docker

É importante iniciar os containers docker por meio do docker-compose.yml

```bash
docker-compose up
```

*Nota*: Esse comando travará o terminal com os logs dos containers, então abra outro.

## Configuração do HiveMQ (MQTT):

Para utilizar a comunicação via MQTT é necessário utilizar um Broker, como o HiveMQ, assim recomendo utilizar o MQTT Explore, um cliente MQTT que dá acesso a conectividade. 

![Alt text](image.png)

*Nota*: É possível analisar as mensagens armazenadas no banco de dados InfluxDb, por meio dos seguintes comandos:

```bash
docker exec -it influxdb sh
``````
```bash
influx
``````
```bash
use influx
``````
```bash
select * from mqtt_consumer
``````

Será aberto um conjunto de dados que estão sendo armazenados no InfluxDb. 


## Configuração do Grafana:

Acesse no navegador de sua preferência e digite a URL abaixo para acessar o container do Grafana:

```bash
http://localhost:3001/login
```

- username: admin
- Password: admin

Vá até a aba Dashboards e realize o *Import* do dashboard do LabREI e acesse.

No final será mostrado uma tela como essa, no qual é possível enviar e receber parâmetros.

![Alt text](image-2.png)



