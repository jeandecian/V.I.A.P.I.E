// ------------------------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------- ARDUINO FINAL --------------------------
// ------------------------------------------------------------------------------------------------------------------------------------

/* --- SOMMAIRE ---
 *  INITIALISATION  // ligne 33
 *  COMMUNICATION   // ligne 76
   *  canal()
   *  
 *  CAPTEURS        // ligne 94
   *  DHT11()
   *  HCSR04()
   *  HCSR501()
   *  situation()
   *  servocapteurs()
   *  servoarret()
   *  capteurs()
   *  
 *  MOTEURS         // ligne 291
   *  frein()
   *  avant()
   *  arriere()
   *  rotation180()
   *  droite()
   *  gauche()
   *  
 *  AUTOMATISATION  // ligne 357
   *  start()
   *  automatic()
 */

// ------------------------------------------------------------------------------------------ INITIALISATION --------------------------
// ------------------------------------------------------------------------------------------------------------------------------------

// Bibliotheques
#include <Servo.h> // Bibliotheque Servo
#include <dht.h>   // Bibliotheque DHT11

// Initialisations variables en utilisant les bibliotheques
Servo myservo;
dht DHT;

// Initialisation des pins
int trig = A2;        // A2 - HC-SR04 - Cable orange
int echo = A3;        // A3 - HC-SR04 - Cable jaune
int pir = 2;          // 2 - HC-SR501 - Cable marron/orange
int speedLeft = 3;    // 3 - Moteur A (Left) - Integree a la carte
int dht = 4;          // 4 - DHT11 - Cable orange
int servo = 5;        // 5 - Servo - Cable orange
int brakeRight = 8;   // 8 - Moteur B (Right) - Integree a la carte
int brakeLeft = 9;    // 9 - Moteur A (Left) - Integree a la carte
int speedRight = 11;  // 11 - Moteur B (Right) - Integree a la carte
int dirLeft = 12;     // 12 - Moteur A (Left) - Integree a la carte
int dirRight = 13;    // 13 - Moteur B (Right) - Integree a la carte

// Initialisation des variables
float humidity;           // DHT11
float temperature;        // DHT11
long distance;            // HC-SR04
int calibragetime = 30;   // HC-SR501
int statut = 0;           // HC-SR501
int val = LOW;            // HC-SR501
int speedPWM = 160;       // PWM Moteurs
int speedPWMb = 170;      // PWM Moteurs B
int pos = 90;             // Servo
int somme = 0;            // Somme evenements servo
int A = 0;                // Servo 45°
int B = 0;                // Servo 90°
int C = 0;                // Servo 135°
int commandstate = 0;     // État de la commande (Automatique = 0, Manuelle = 1, Intermediaire = -1)

// ------------------------------------------------------------------
// ------------------------------------------------------------------

// -------------------------------------------------------------------------------------------- COMMUNICATION -------------------------
// ------------------------------------------------------------------------------------------------------------------------------------
// On crée ici une fonction qui va lire sur la voie serie pour une commande a distance.

void canal() {
  while (Serial.available()) {
    char inChar = Serial.read(); // On transforme ce qu'on lit sur la voie serie en charactere.
    Serial.println(inChar); // On l'affiche sur le moniteur serie.
    
    switch(inChar) {
      case '0':
        frein();
      break;
      case '1':
        avant();
      break;
      case '2':
        arriere();
      break;
      case '3':
        droite();
      break;
      case '4':
        gauche();
      break;
      case 'A':
        automatic();
      break;
      case 'M':
        commandstate = -1;
      break;
    }
  }
}

// ------------------------------------------------------------------
// ------------------------------------------------------------------

// ---------------------------------------------------------------------------------------------- CAPTEURS ----------------------------
// ------------------------------------------------------------------------------------------------------------------------------------
// DHT11()
// HCSR04()
// HCSR501()

// Fonction capteur DHT11
void DHT11() {
  int check = DHT.read11(dht);
  temperature = DHT.temperature;
  humidity = DHT.humidity;

  if (commandstate == 0) {
    if (temperature >= 45) {
      frein();
      arriere();

      for (pos = 135; pos = 45; pos -= 45) {
      myservo.write(pos);
      HCSR501();
      }
    
      rotation180();
      avant();
    }
  }

  Serial.print("T");
  Serial.println(temperature);
  Serial.print("H");
  Serial.println(humidity);

  delay(500);
  canal();
}

// Fonction capteur HC-SR04
void HCSR04() {
  digitalWrite(trig, HIGH);
  delay(10);
  digitalWrite(trig, LOW);
  /* On multiplie le temps par 0.17 car le son se propage à 340m/s = 340000mm/s = 0.34mm/us. 
  Sachant qu'il s'agit d'un aller retour on a donc 0.17mm/us */
  distance = pulseIn(echo, HIGH)*(0.17); // Résultat en millimètres

  if (distance <= 4000) {
    Serial.print("D");
    Serial.println(distance);
  }

  delay(200);
  canal();
}

// Fonction capteur HC-SR501
void HCSR501() {
  statut = digitalRead(pir);

  if (statut == HIGH) {
    if (val == LOW) {
      Serial.println("A1");
      val = HIGH;
    }
  } else {
    if (val == HIGH) {
      Serial.println("A0");
      val = LOW;
    }
  }
  
  delay(500);
  canal();
}

// ------------------------------------------------------------------
// situation()
// servocapteurs()
// servoarret()
// capteurs

// Fonction sur les situations possibles selon la position et la distance.
void situation() {
  if (distance <= 500 && pos == 90) {
    frein();
    servoarret();
  } else {
    avant();
  }
}

// Fonction qui fait fonctionner les capteurs pendant le mouvement du vehicule.
void servocapteurs() {
  for (pos = 45; pos <= 135; pos += 45) {
    myservo.write(pos);
    Serial.print("P");
    Serial.println(pos);
    HCSR04();
    situation();
    HCSR501();
    canal();
    Serial.println("");
    delay(300);
  }
  DHT11();
}

// Fonction qui fait decider au vehicule dans quelle direction prendre.
void servoarret() {
  pos = 45;
  capteurs();

  if (distance <= 500) {
    A = 0;
  } else {
    A = 3;
  }

  pos = 90;
  capteurs();
  
  if (distance <= 500) {
    B = 0;
  } else {
    B = 5;
  }

  pos = 135;
  capteurs();

  if (distance <= 500) {
    C = 0;
  } else {
    C = 7;
  }

  somme = A+B+C;

  if (somme == 0) {
    rotation180();
  } else if ((somme == 7) || (somme == 10)) {
    droite();
  } else if (somme == 3) {
    gauche();
  } else {
    avant();
  }
}

void capteurs() {
  myservo.write(pos);
  HCSR04();
  DHT11();
  HCSR501();
  canal();
  Serial.println("");
  delay(300);
}

// ------------------------------------------------------------------
// ------------------------------------------------------------------

// ---------------------------------------------------------------------------------------------- MOTEURS -----------------------------
// ------------------------------------------------------------------------------------------------------------------------------------
// frein()
// avant()
// arriere()
// rotation180()
// droite()
// gauche()

void frein() {
  digitalWrite(brakeLeft, HIGH); // Frein gauche activee
  digitalWrite(brakeRight, HIGH); // Frein droit activee
}

void avant() {
  digitalWrite(dirLeft, LOW);
  digitalWrite(dirRight, LOW);
  digitalWrite(brakeLeft, LOW);
  digitalWrite(brakeRight, LOW);
  analogWrite(speedLeft, speedPWM);
  analogWrite(speedRight, speedPWMb);
}

void arriere() {
  digitalWrite(dirLeft, HIGH);
  digitalWrite(dirRight, HIGH);
  digitalWrite(brakeLeft, LOW);
  digitalWrite(brakeRight, LOW);
  analogWrite(speedLeft, speedPWM);
  analogWrite(speedRight, speedPWMb);
}

void rotation180() {
  digitalWrite(dirLeft, LOW);
  digitalWrite(dirRight, HIGH);
  digitalWrite(brakeLeft, LOW);
  digitalWrite(brakeRight, LOW);
  analogWrite(speedLeft, speedPWM);
  analogWrite(speedRight, speedPWM);
}

void droite() {
  arriere();
  delay(500);
  digitalWrite(brakeRight, HIGH); // Frein moteur droit enclenché
  digitalWrite(dirLeft, LOW);
  digitalWrite(brakeLeft, LOW);
  analogWrite(speedLeft, speedPWM);
  delay(1000);
  avant();
}

void gauche() {
  arriere();
  delay(500);
  digitalWrite(brakeLeft, HIGH); // Frein moteur gauche enclenché
  digitalWrite(dirRight, LOW);
  digitalWrite(brakeRight, LOW);
  analogWrite(speedRight, speedPWM);
  delay(1000);
  avant();
}

// ------------------------------------------------------------------
// ------------------------------------------------------------------

// ------------------------------------------------------------------------------------------- AUTOMATISATION -------------------------
// ------------------------------------------------------------------------------------------------------------------------------------
// start()
// automatic()

// Fonction automatique

void start() {
  myservo.write(90);
  HCSR04();

  if (distance <= 500) {
    avant();
  }
}

void automatic() {
  frein();
  servocapteurs();
}

// ------------------------------------------------------------------
// ------------------------------------------------------------------

void setup() {
  // MotorShield Setup
  pinMode(dirLeft, OUTPUT);
  pinMode(brakeLeft, OUTPUT);
  pinMode(dirRight, OUTPUT);
  pinMode(brakeRight, OUTPUT);

  // HC-SR04 Setup
  pinMode(trig, OUTPUT);
  digitalWrite(trig, LOW);
  pinMode(echo, INPUT);

  // HC-SR501 Setup
  pinMode(pir, INPUT);

  // Servo Setup
  myservo.attach(5);
  
  Serial.begin(57600); // Meme Baud rate que le module Bluetooth HC-05

  start();
}

void loop() {
  if (commandstate == 0) {
    automatic();
  } else if (commandstate == 1) {
    canal();
  } else {
    frein();
    delay(500);
    commandstate = 1;
  }
}
