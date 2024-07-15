
#include <Arduino.h>
#include <WiFi.h>
#include <ModbusClientTCP.h>  // Inclui a biblioteca ModbusClient TCP


char ssid[] = "JOAO";     
char pass[] = "12345678";     

WiFiClient theClient;          // Configura/monta um Cliente
ModbusClientTCP MbTcp(theClient); // Cria uma instância ModbusTCP 

unsigned long tmrpt;  // Variavel para calculo do tempo de resposta.

/*-------------------------------------------------------------- 
     Função para manipular as respostas recebidas     
---------------------------------------------------------------*/
void handleData(ModbusMessage response, uint32_t token) 
{
   Serial.printf("Response: serverID=%d, FC=%d, Token=%08X, length=%d:\n", response.getServerID(), response.getFunctionCode(), token, response.size());
   
   for(auto& byte : response) Serial.printf("%02X ", byte); // Envia os dados recebidos pela serial

   Serial.printf("- %4d", ((uint16_t)response[3] << 8) | response[4]);  // Envia o valor do registrador, convertido para decimal (tensão aproximada da rede)
   Serial.printf("- %4dms", (uint16_t)(millis() - tmrpt));                // Calcula e envia o tempo entre requisição e resposta
   Serial.println(""); // Nova linha
}


/*-------------------------------------------------------------- 
     Função para manipular as respostas de erros      
---------------------------------------------------------------*/
void handleError(Error error, uint32_t token) 
{
   ModbusError me(error); // ModbusError retorna uma mensagem de erro, baseado no código de erro
   Serial.printf("Erro: %02X - %s\n", (int)me, (const char *)me);
}



/*-------------------------------------------------------------- 
     Setup inicial  
---------------------------------------------------------------*/
void setup(void) 
{
   Serial.begin(115200);         // Inicia a serial principal (monitor serial)
   while(!Serial) {}
   Serial.println("__ OK __");   // Aguarda serial estar OK

   WiFi.begin(ssid, pass);                // Inicia conexão a rede WiFi
   while (WiFi.status() != WL_CONNECTED)  // Aguarda conexão ser estabilicida
   {
      Serial.print(". ");
      delay(1000);
   }
  
   IPAddress wIP = WiFi.localIP();  // Adquiri IP local
   Serial.printf("WIFi IP address: %u.%u.%u.%u\n", wIP[0], wIP[1], wIP[2], wIP[3]); // Envia IP pela serial

   // Configura o ModbusTCP client.
   MbTcp.onDataHandler(&handleData);   // Configura a função de manipulação de dados (handleData) 
   MbTcp.onErrorHandler(&handleError); // Configura a função de manipulação de erros (handleError) 
   MbTcp.setTimeout(2000, 200);        // Define o tempo limite de resposta em 2000ms e o intervalo entre as solicitações para o mesmo host em 200ms
   MbTcp.begin();                      // Inicia a tarefa em segundo plano, do ModbusTCP

   MbTcp.setTarget(IPAddress(192, 168, 0, 102), 5020);   // Define o IP do servidor Modbus TCP e a porta
}


/*-------------------------------------------------------------- 
     Loop principal
---------------------------------------------------------------*/
void loop() 
{
   // A formatação para seguisição é a seguinte:    
   // - Token: para verificar se a resposta confere com a solicitação. Usamos o valor atual de millis() para isso.
   // - Server ID = 1
   // - Código de função = 0x03 (ler resgistradores do tipo Holding)
   // - Endereço inicial de leitura = 3207
   // - Numero de registradores a serem lidos = 1
   
   tmrpt = millis();
   Error err = MbTcp.addRequest((uint32_t)millis(), 1, READ_HOLD_REGISTER, 3207, 1);
   
   if (err!=SUCCESS) // Caso algo de errado na chamada da função, um código de erro será enviado pela serial e a requisição não será feita
   {
      ModbusError e(err);
      Serial.printf("Error creating request: %02X - %s\n", (int)e, (const char *)e);
   }

    delay(3000); // delay entre requisições
}
