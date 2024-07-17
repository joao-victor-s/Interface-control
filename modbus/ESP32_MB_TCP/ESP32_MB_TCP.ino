#include <Arduino.h>
#include <WiFi.h>
#include <ModbusClientTCP.h>  // Inclui a biblioteca ModbusClient TCP

char ssid[] = "JOAO";     
char pass[] = "12345678";     

WiFiClient theClient;          // Configura/monta um Cliente
ModbusClientTCP MbTcp(theClient); // Cria uma instância ModbusTCP 

unsigned long tmrpt;  // Variável para cálculo do tempo de resposta
const int threshold = 20;
const int LED_BUILTIN = 2;
int touchValue; 

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

   // Configura a porta para o LED
   pinMode(LED_BUILTIN, OUTPUT);
}

/*-------------------------------------------------------------- 
     Loop principal
---------------------------------------------------------------*/
void loop() 
{
   // Leitura do valor de toque
   touchValue = touchRead(T0);
   Serial.print(touchValue);
   
   if(touchValue < threshold) {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.print(" Led ON\n");
   } else {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.print(" Led OFF\n");
   }

   // Envia o valor do touch para o servidor Modbus
   uint16_t modbusValue = (uint16_t)touchValue; // Conversão do valor lido para o tipo uint16_t
   
   tmrpt = millis();
   Error err = MbTcp.addRequest((uint32_t)millis(), 1, READ_HOLD_REGISTER, 3207, modbusValue);
   
   if (err!=SUCCESS) // Caso algo de errado na chamada da função, um código de erro será enviado pela serial e a requisição não será feita
   {
      ModbusError e(err);
      Serial.printf("Error creating request: %02X - %s\n", (int)e, (const char *)e);
   }

   delay(3000); // delay entre requisições
}
