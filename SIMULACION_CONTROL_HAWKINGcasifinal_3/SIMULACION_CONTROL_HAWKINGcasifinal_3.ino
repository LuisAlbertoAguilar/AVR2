#include <SPI.h> //Library for using SPI Communication
#include <mcp2515.h> //Library for using CAN Communication
#include <Separador.h>//separador de variables

Separador s;

//ENVÍO DE VALORES POR MEDIO DE PYTHON
//Variables de referencia
String Dirref, Velref, Frenosdelref, Frenostrasref, terminacion;

//Variables de dirección a mandar
int DirRealU, DirRealD, DirRealC;

//Variables de velocidad a mandar
int VelRealU, VelRealD, VelRealC;

//Variables de frenos delanteros a mandar
int FrenosdelRealU, FrenosdelRealD, FrenosdelRealC;

//Variables de frenos delanteros a mandar
int FrenostrasRealU, FrenostrasRealD, FrenostrasRealC;

//RECIBIMIENTO DE VALORES
int id, dato1, dato2, dato3;

//Recibimiento de velocidad
String valueString = "0 0 0 0 0 0 ";
int Dir;
int Vel;
int Frenos;
int Frenosdel;
int Frenostras;
int Btt;
int Bateria;
int DirU;
int DirD;
int DirC;//direccion
int VelU;
int VelD;
int VelCe;
int FrenosdelU;
int FrenosdelD;
int FrenosdelC;
int FrenostrasU;
int FrenostrasD;
int FrenostrasC;
int BttU;
int BttD;
int BttC;//bateria
int SSP=2;
int SIP=2;

String parsedStr[5];                         //IMPORTANTE: Este buffer debe cambiarse al tamaño deseado de acuerdo con la cantidad de datos que se vayan a estar transmitiendo. Ej.: en este demo es de [5] porque se envían %,# como verificadores de la cadena y 3 datos: posición de acelerador, freno y batería
String inputString = " ";                    // String de entrada
bool stringComplete = false;                 // booleano para detectar cuando el array este completo
String toParseString = " ";
MCP2515 mcp2515(10);

struct can_frame canMsg;
struct can_frame canMsgDir;                  //declaración de mensaje CAN 1 (Direccion)
struct can_frame canMsgVel;                  //declaración de mensaje CAN 2 (Velocidad)
struct can_frame canMsgFrenosdel;            //declaración de mensaje CAN 3 (Freno Delantero)
struct can_frame canMsgFrenostras;           //declaración de mensaje CAN 4 (Freno Trasero)

void setup() {
  while (!Serial);
  Serial.begin(115200);
  SPI.begin();                               //Begins SPI communication
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS, MCP_8MHZ); //Sets CAN at speed 500KBPS and Clock 8MHz
  mcp2515.setNormalMode();
  pinMode(4,INPUT);
  pinMode(6,INPUT);
  pinMode(7,INPUT);
  pinMode(8,INPUT);
  pinMode(9,INPUT);
  //pose superior es velocidad, pose está empatado
  //Joy izquierdo eje 2 es velocidad invertido
  //Joy derecho eje 1 dirección empatado
  
}

void loop() {
  //Serial.print("JoyDerecho Eje1  ");
  //Serial.println(analogRead(A2));
  //Serial.print("JoyDerecho Eje2  ");
  //Serial.println(analogRead(A3));
  //Serial.print("JoyIzquierdo Eje1  ");
  //Serial.println(analogRead(A0));
  //Serial.print("JoyIzquierdo Eje2  ");
  //Serial.println(analogRead(A1));
  if(digitalRead(4)){
    Serial.println("emergencia");
  }
  SSP=2;
  SIP=2;
  if(digitalRead(9)){
    SSP=SSP-1;
    }
  if(digitalRead(8)){
    SSP=SSP+1;
    }
  if(digitalRead(7)){
    SIP=SIP-1;
    }
  if(digitalRead(6)){
    SIP=SIP+1;
    }
  //Serial.print("Pose superior ");
  //Serial.print(SSP);
  //Serial.print(" Pose inferior ");
  //Serial.println(SIP);
  //delay(500);
  
  if ((mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK))
  {
    id = canMsg.can_id;
    dato1 = canMsg.data[0];
    dato2 = canMsg.data[1];
    dato3 = canMsg.data[2];

    if (id == 40)
    {
      DirU = dato3;
      DirD = dato2;
      DirC = dato1;
      Dir = (DirU * 1) + (DirD * 10) + (DirC * 100);
    }

    if (id == 39)
    {
      VelU = dato3;
      VelD = dato2;
      VelCe = dato1;
      Vel = (VelU * 1) + (VelD * 10) + (VelCe * 100);
    }

    if (id == 38)
    {
      FrenosdelU = dato3;   
      FrenosdelD = dato2;
      FrenosdelC = dato1;
      Frenosdel = (FrenosdelU * 1) + (FrenosdelD * 10) + (FrenosdelC * 100);
    }

    if (id == 37)
    {
      FrenostrasU = dato3;
      FrenostrasD = dato2;
      FrenostrasC = dato1;
      Frenostras = (FrenostrasU * 1) + (FrenostrasD * 10) + (FrenostrasC * 100);
    }

    if (id == 36)
    {
      BttU = dato3;
      BttD = dato2;
      BttC = dato1;
      Btt = (BttU * 1) + (BttD * 10) + (BttC * 100);
    }

    String direccion = String(Dir);
    String velocidad = String(Vel);
    String frenosdelanteros = String(Frenosdel);
    String frenostraseros = String(Frenostras);
    String bateria = String(Btt);
    //delay(500);
    valueString = direccion + ' ' + velocidad + ' ' + frenosdelanteros + ' ' + frenostraseros + ' ' + bateria + ' ' + '%';
    Serial.println(valueString);
  }

  //SerialEvent();
  Dirref = (analogRead(A2));
  Serial.print(Dirref);
  Serial.print("   ");
  //Serial.println(A2);
  Velref = SSP*(1024-analogRead(A1))/60;
  Serial.println(Velref);
  Frenosdelref = int(0);
  Frenostrasref = int(0);
  if(Vel>Velref.toInt()){
    Frenosdelref=6*(Vel-Velref.toInt());
    Frenostrasref=6*(Vel-Velref.toInt());
    }
  stringComplete=true;
  if (true) {
    stringComplete = false;
    
    //DESMENUZADO DE VALORES DE DIRECCIÓN REAL ENVIADA POR EL MONITOR SERIAL
    int DirReal = Dirref.toInt();

    canMsgDir.can_id = 20;              // Dirección
    canMsgDir.can_dlc = 3;              // 1 byte
    //Serial.println(DirReal);
    //Fórmulas
    DirRealC = (DirReal / 100) % 10;
    DirRealD = (DirReal / 10) % 10;
    DirRealU = (DirReal % 10);
    

    //Asignación
    canMsgDir.data[0] = DirRealC;
    canMsgDir.data[1] = DirRealD;
    canMsgDir.data[2] = DirRealU;

    //Envío
    mcp2515.sendMessage(&canMsgDir);
    //Serial.println("ahivamos");
    delay(10);
    

    //DESMENUZADO DE VALORES DE VELOCIDAD REAL ENVIADA POR EL MONITOR SERIAL
    int VelReal = Velref.toInt();
    canMsgVel.can_id = 19;              // Velocidad
    canMsgVel.can_dlc = 3;              // 1 byte
    //Serial.println(VelReal);
    //Fórmulas
    VelRealC = (VelReal / 100) % 10;
    VelRealD = (VelReal / 10) % 10;
    VelRealU = VelReal % 10;
    

    //Asignación
    canMsgVel.data[0] = VelRealC;
    canMsgVel.data[1] = VelRealD;
    canMsgVel.data[2] = VelRealU;
    mcp2515.sendMessage(&canMsgVel);
    delay(10);

    //DESMENUZADO DE VALORES DE FRENOS DELANTEROS REAL ENVIADA POR EL MONITOR SERIAL
    int FrenosdelReal = Frenosdelref.toInt();
    canMsgFrenosdel.can_id = 18;              // Frenos Delanteros
    canMsgFrenosdel.can_dlc = 3;              // 1 byte
    //Serial.println(FrenosdelReal);
    //Fórmulas
    FrenosdelRealC = (FrenosdelReal / 100) % 10;
    FrenosdelRealD = (FrenosdelReal / 10) % 10;
    FrenosdelRealU = FrenosdelReal % 10;
    

    //Asignación
    canMsgFrenosdel.data[0] = FrenosdelRealC;
    canMsgFrenosdel.data[1] = FrenosdelRealD;
    canMsgFrenosdel.data[2] = FrenosdelRealU;

    //Envío
    mcp2515.sendMessage(&canMsgFrenosdel);
    delay(10);

    //DESMENUZADO DE VALORES DE FRENOS TRASEROS REAL ENVIADA POR EL MONITOR SERIAL
    int FrenostrasReal = Frenostrasref.toInt();
    canMsgFrenostras.can_id = 17;              // Frenos Traseros
    canMsgFrenostras.can_dlc = 3;              // 1 byte
    //Serial.println(FrenostrasReal);
    //Fórmulas
    FrenostrasRealC = (FrenostrasReal / 100) % 10;
    FrenostrasRealD = (FrenostrasReal / 10) % 10;
    FrenostrasRealU = FrenostrasReal % 10;
    

    //Asignación
    canMsgFrenostras.data[0] = FrenostrasRealC;
    canMsgFrenostras.data[1] = FrenostrasRealD;
    canMsgFrenostras.data[2] = FrenostrasRealU;

    //Envío
    mcp2515.sendMessage(&canMsgFrenostras);
    delay(10);
  }
}

void SerialEvent() {
  while (Serial.available()) {
    String datosrecibidos = Serial.readString();
    Dirref = s.separa(datosrecibidos, ' ', 0);
    Velref = s.separa(datosrecibidos, ' ', 1);
    Frenosdelref = s.separa(datosrecibidos, ' ', 2);
    Frenostrasref = s.separa(datosrecibidos, ' ', 3);
    terminacion = s.separa(datosrecibidos, ' ', 4);
    stringComplete = true;
    Serial.println(datosrecibidos);
    //Serial.println(Dirref);
    //Serial.println(Velref);
  }
}
