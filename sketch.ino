//====================================================================
// ATIVIDADE FIAP - Cap 1 - Construindo uma máquina agrícola
//====================================================================
// Autor.....: Diego Nunes Veiga
// RM........: 560658
// Turma.....: Graduação - 1TIAOR
// Data......: 11/11/2024
//====================================================================

//Bibliotecas utilizadas
#include <DHT.h>

//Botão azul (Fósforo) - Definições
#define Btfosforo 23

//Botão amarelo (Potássio) - Definições
#define Btpotassio 22

// Sensor DHT22 - Definições
#define pinDHT 21           // Pino GPIO conectado
#define modelo DHT22        // Modelo do sensor
DHT dht(pinDHT, modelo);

//Sensor LDR - Definições
#define ldrPin 34         // Pino GPIO conectado ao ADC

//Bomba de água(Relé) - Definições
#define pinbomba 19

//====================================================================
// SUBALGORITMOS
//====================================================================


// Realiza a leitura do fosforo
bool LeituraFosforo() {

  return digitalRead(Btfosforo) == HIGH;
}

// Realiza a leitura do potassio
bool LeituraPotassio() {

  return digitalRead(Btpotassio) == HIGH;
}

// Realiza a leitura da umidade do solo
float LeituraUmidade() {

  float umid = dht.readHumidity();
  return umid;
}

// Realiza a leitura do pH do solo
float LeituraLDR() {

  const float GAMMA = 0.7;
  const float RL10 = 50;

  // Realiza leitura da saída do sensor
  int ldrValue = analogRead(ldrPin);
  float voltage = ldrValue / 4096.0 * 5;
  float resistance = 2000 * voltage / (1 - voltage / 5);
  float pH = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA));

  // Limita o valor de pH até 14
  pH = min(pH,14.0f);

  return pH;
}

bool Bomba(bool fosf, bool pot, float umid, float pH){

  bool status = false;

  // Condições para ligar a bomba de água
  if (umid < 80 || ((pH >= 6.5 && pH <= 7.5) && (fosf || pot))){
    digitalWrite(pinbomba,HIGH);
    status = true;
  }else{
    digitalWrite(pinbomba, LOW);
    status = false;
  }
  return status;
}

// Apresenta as informações do fosforo no monitor
void MensagemFosforo(bool status) {

  Serial.print("Fosforo: ");

  if (status == false){
    Serial.println("normal");
  }else{
    Serial.println("baixo");
  }
}

// Apresenta as informações do potassio no monitor
void MensagemPotassio(bool status) {

  Serial.print("Potassio: ");

  if (status == false){
    Serial.println("normal");
  }else{
    Serial.println("baixo");
  }
}

// Apresenta as informações de humidade no monitor
void MensagemUmidade(float umid) {

  Serial.print("Umidade: ");

  if (isnan(umid)) {
    Serial.println("Falha ao ler do sensor DHT!");
  }else{
    Serial.print(umid);
    Serial.println(" %	");
  }
}

// Apresenta as informações de pH no monitor
void MensagemPH(float pH) {

  Serial.print("Nível de pH: ");
  Serial.println(pH);
}

void MensagemBomba(bool status){
    Serial.print("Bomba de água: ");

  if (status == true){
    Serial.println("ligada");
  }else{
    Serial.println("desligada");
  }
}

//====================================================================
// STARTUP INICIAL
//====================================================================

void setup() {

  // Configurações dos pinos
  pinMode(Btfosforo, INPUT);
  pinMode(Btpotassio, INPUT);
  pinMode(pinbomba, OUTPUT);

  // Inicia a comunicação serial
  Serial.begin(9600);

  // Inicia a comunicação do sensor DHT22
  dht.begin();

}

//====================================================================
// PROGRAMA PRINCIPAL
//====================================================================

  int imprime = 0;

void loop() {

  //Leitura dos sensores
  bool ResultF = LeituraFosforo();
  bool ResultPot = LeituraPotassio();
  float ResultUmid = LeituraUmidade();
  float ResultPH = LeituraLDR();
  bool ResultBomb = Bomba(ResultF,ResultPot,ResultUmid,ResultPH);

  if(imprime == 1000){
    //Apresentação das mensagens no terminal
    Serial.println("");
    Serial.println("LEITURA DA PLANTAÇÃO:");
    MensagemFosforo(ResultF);
    MensagemPotassio(ResultPot);
    MensagemUmidade(ResultUmid);
    MensagemPH(ResultPH);
    MensagemBomba(ResultBomb);

    // Zera a contagem para a impressão
    imprime = 0;
  }

  //Incrementa a variável para a impressão dos dados
  imprime++;
  
}