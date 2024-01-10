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

## Configuração do HiveMQ (MQTT):

Para utilizar a comunicação via MQTT é necessário utilizar um Broker, como o HiveMQ, assim recomendo utilziar o MQTT Explore, um cliente MQTT que dá acesso a conectividade. 

![Alt text](image.png)


## Configuração do Grafana:

Acesse no navegador de sua preferência e digite a URL abaixo para acessar o container do Grafana:

```bash
http://localhost:3001/login
```

- username: admin
- Password: admin

Vá até a aba Dashboards e realize o *Import* do dashboard do LabREI e acesse.




