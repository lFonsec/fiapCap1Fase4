#include <DHT.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 4);
int fosforoPin = 23;
int potassioPin = 4;
int ldrPin = 33;
int pinoDHT =  32;
int relePin = 2;
int releState = false;
int contador = 0;
DHT dht(pinoDHT, DHT22);

void setup() {
  Serial.begin(115200);
  // inicia o sensor dht
  dht.begin();
  //inicia o pin do rele
  pinMode(relePin, OUTPUT);
  //inicia os botoes
  pinMode(fosforoPin, INPUT_PULLUP);
  pinMode(potassioPin, INPUT_PULLUP);
  lcd.init();
  lcd.backlight();
  lcd.clear();
}

void loop() {
  lcd.setCursor(0,0);
  //pega o calor da temperatura e da umidade
  float temp = dht.readTemperature();
  float umi = dht.readHumidity();
  // pega o valor do sensor ldr
  int ldrvalue = analogRead(ldrPin);
  // seta os botoes do fosforo e do potassio
  int fosforoState = HIGH;
  fosforoState = digitalRead(fosforoPin);
  int postassioState = HIGH;
  postassioState = digitalRead(potassioPin);
  bool b = 0;
  // imprime o valor da temperatura e da umidade

  //Serial.print("Temperatura: ");
  Serial.print(temp);
  Serial.print(" ");
  //Serial.println("°C");
  //Serial.print("Umidade: ");
  Serial.println(umi);
 /* 
  Serial.println("%");
  Serial.print("Valor do PH: ");
  Serial.println(ldrvalue);

  // detecta se os botoes foram pressionados
  if(fosforoState == LOW){
    Serial.println("Fosforo apertado ");
  }
  if(postassioState == LOW){
    Serial.println("Postassio apertado");
  }
*/
  if(umi > 95){
    contador = 0;
  }
  //caso a temperatura esteja acima dos 35 graus ou a umidade esteja abaixo dos 45 
  // o rele ira ativar o led vermelho sinalizando o começo do processo de irrigação
  if(temp > 35 || umi < 45 || contador > 8){
    digitalWrite(relePin, HIGH);
   // Serial.println("Bombas de irrigação ligadas");
    b = 1;
    contador = 0;
  } else {
    digitalWrite(relePin, LOW);
   // Serial.println("Bombas de irrigação desligadas");
    b = 0;
  }
  Serial.println("-------");
  lcd.print("Tem:");
  lcd.print(temp, 1);
  lcd.print("     Fosfo:");
  lcd.print(!fosforoState);
  lcd.setCursor(0,1);
  lcd.print("Umi:");
  lcd.print(umi, 1);
  lcd.print("%    Potas:");
  lcd.print(!postassioState);
  lcd.setCursor(0,2);
  lcd.print("PH:");
  lcd.print(ldrvalue);
  lcd.print("   Contador:");
  lcd.print(contador);
  lcd.setCursor(0,3);
  lcd.print("BombasLigadas:");
  lcd.print(b);

  contador++;
  delay(800);
}
