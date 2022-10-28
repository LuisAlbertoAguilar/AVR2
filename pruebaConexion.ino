/*-----------Inclusión de Librerías-----------*/
#include <mcp2515.h>
//#include <BluetoothSerial.h>

 

/*----------Declaración de Variables----------*/
String commandParsed[20];
String commandBuffer;
struct can_frame msgSend;       //Estructura de mensaje para almacenar salientes
struct can_frame msgRecieve;    //Estructura de mensaje para almacenar entrantes

 

/*--------------Inicializaciones--------------*/
MCP2515 mcp2515(10);             //Inicialización del bus CAN
//BluetoothSerial SerialBT;

 

void setup()
{
  Serial.begin (115200);        //Baudrate del puerto serie
  Serial.setTimeout(200);       //Timeout de lectura
  mcp2515.reset();
  mcp2515.setBitrate(CAN_125KBPS);  //Bitrate del CAN Bus
  mcp2515.setNormalMode();          //Modo del CAN
//  SerialBT.begin("AGV_TEC_BT");     //Inicialización del Puerto Serie BT con nombre "AGV_TEC_BT"
}

 

void loop () {
  //Leer comando del puerto serie y enviarlo mediante el CAN Bus
  //Sintaxis de comando:  ID DLC Data1 Data2 Data3 Data4 ... Data8
  //Requerido que la entrada sea un numero entero separado por
  //espacios entre cada fragmento.
    
    if(Serial.available()>0){
      commandBuffer = Serial.readString();  //Leer puerto serie hasta timeout
      commandBuffer.trim();                 //Eliminación de caracteres newline (/n)
      parseCommand(commandBuffer);          //Subfunción de división del comando a enviar
      mcp2515.sendMessage(&msgSend);        //envío del comando a CAN Bus
      commandPrint(Serial, msgSend);                //Subfunción para impresión de comando con estructura CAN
      delay(100);               
    }
//    
//    if(SerialBT.available()>0){
//      commandBuffer = SerialBT.readString();  //Leer puerto Bluetooth hasta timeout
//      commandBuffer.trim();                   //Eliminación de caracteres newline (/n)
//      parseCommand(commandBuffer);            //Subfunción de división del comando a enviar
//      mcp2515.sendMessage(&msgSend);          //envío del comando a CAN Bus
//      commandPrint(SerialBT, msgSend);                //Subfunción para impresión de comando con estructura CAN al puerto Bluetooth
//      delay(100);               
//    }
//    

 

  //Recepción de comandos mediante puerto CAN Bus hacia Puerto Serie
  //Sintaxis de comando recibido: ID DLC Data1 Data2 Data3 Data4 ... Data8
  
    if (mcp2515.readMessage(&msgRecieve) == MCP2515::ERROR_OK) {
      commandPrint(Serial, msgRecieve);             //Subfunción para impresión de comando con estructura CAN
//      commandPrint(SerialBT, msgRecieve);           //Subfunción para impresión de comando con estructura CAN al puerto Bluetooth
    }
  }

 


//Función para separación del comando a enviar
void parseCommand(String CANCommand){
  int StringCount = 0;
  
  while (CANCommand.length() > 0){
      int index = CANCommand.indexOf(' '); //Indice para separación, emplea espacios entre cada dato para determinar cada fragmento
      
      if (index == -1){
        commandParsed[StringCount++] = CANCommand;
        break;
      }
      else{
        commandParsed[StringCount++] = CANCommand.substring(0, index);
        CANCommand = CANCommand.substring(index+1);
      }
    }

 

  //Guardado del comando por fragmento en struct msgSend para su envío al CAN Bus
  
  msgSend.can_id  = commandParsed[0].toInt();
  msgSend.can_dlc = commandParsed[1].toInt();
  for (int i = 0; i<msgSend.can_dlc; i++)  {  // print the data
    msgSend.data[i] = commandParsed[i+2].toInt();
  }
}

 

void commandPrint(Print &printObj, struct can_frame toPrint){
  //Impresión del header del comando con la estructura "ID DLC D0 D1 ... D7"
//  printObj.print("ID DLC"); 
//  for (int i = 0; i<toPrint.can_dlc; i++)  {  
//    printObj.print(" D");
//    printObj.print(i);
//  }
//  printObj.println();

 

  // Impresión del comando separando elementos
  printObj.print(toPrint.can_id, DEC);
  printObj.print("  ");
  printObj.print(toPrint.can_dlc, DEC);
  printObj.print("  ");
  for (int i = 0; i<toPrint.can_dlc; i++)  { 
    if(toPrint.data[i]<16){
      printObj.print(" ");
    }
    printObj.print(toPrint.data[i],DEC);
    printObj.print(" ");
  }
  printObj.println();
  printObj.println();
}
