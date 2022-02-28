/********************************************************************/
// include the libraries
#include <OneWire.h>
#include <DallasTemperature.h>
#include <stdlib.h>
/********************************************************************/
// Data wires
#define ONE_WIRE_BUS 2
#define ONE_WIRE_BUS1 4
#define ONE_WIRE_BUS2 6
#define ONE_WIRE_BUS3 8


// The max number of sensors
#define MAX_SENSORS 10
/********************************************************************/
// Setup a oneWire instance to communicate with any OneWire devices
// (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);
OneWire oneWire1(ONE_WIRE_BUS1);
OneWire oneWire2(ONE_WIRE_BUS2);
OneWire oneWire3(ONE_WIRE_BUS3);
/********************************************************************/
// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);
DallasTemperature sensors1(&oneWire1);
DallasTemperature sensors2(&oneWire2);
DallasTemperature sensors3(&oneWire3);
/********************************************************************/
double strt_time;
double curr_time;
int device_count;
int device_count1;
int device_count2;
int device_count3;
int total_device_count = 0;
double ms_between_reads = 3000;

DeviceAddress addrs[MAX_SENSORS];
DeviceAddress addrs1[MAX_SENSORS];
DeviceAddress addrs2[MAX_SENSORS];
DeviceAddress addrs3[MAX_SENSORS];

void setup(void)
{
  // start serial port
  Serial.begin(9600);
  // Start up the library
  sensors.begin();
  sensors1.begin();
  sensors2.begin();
  sensors3.begin();
  // Discover the network
  device_count = discoverNetwork(sensors, addrs, device_count);
  device_count1 = discoverNetwork(sensors1, addrs1, device_count1);
  device_count2 = discoverNetwork(sensors2, addrs2, device_count2);
  device_count3 = discoverNetwork(sensors3, addrs3, device_count3);
  total_device_count += device_count + device_count1 + device_count2 + device_count3;
  Serial.print("Total number of devices on network: ");
  Serial.println(total_device_count);
  curr_time = double(millis());
}


void loop(void)
{
  getInput();
  if (double(millis()) - curr_time >= double(ms_between_reads)) {
    curr_time = double(millis());
    sensors.requestTemperatures();// Send the command to get temperature readings
    sensors.setWaitForConversion(true);
    sensors1.requestTemperatures();// Send the command to get temperature readings
    sensors1.setWaitForConversion(true);
    sensors2.requestTemperatures();// Send the command to get temperature readings
    sensors2.setWaitForConversion(true);
    sensors3.requestTemperatures();// Send the command to get temperature readings
    sensors3.setWaitForConversion(true);

    String json = "";
    json += "{";

    // Print JSON format to serial

    //Add data for first run of sensors
    for (int i = 0; i < device_count; i++) {
      json += "\"";
      for (uint8_t j = 0; j < 8; j++)
      {
        // zero pad the address if necessary
        if (addrs[i][j] < 16) json += "0" ;
        json += addrs[i][j];
      }
      json += "\"";
      /*
        Serial.print("Time");
        Serial.print(" : ");
        Serial.print(millis());
        Serial.print(", ");
      */
      //printAddress(addrs[i]);
      json += " : ";
      json += "\"";
      json += sensors.getTempF(addrs[i]);
      json += "\"";
      if ( i < device_count) {
        json += ", ";
      }
    }

    //Add data for second run of sensors
    for (int i = 0; i < device_count1; i++) {
      json += "\"";
      for (uint8_t j = 0; j < 8; j++)
      {
        // zero pad the address if necessary
        if (addrs1[i][j] < 16) json += "0" ;
        json += addrs1[i][j];
      }
      json += "\"";

      json += " : ";
      json += "\"";
      json += sensors1.getTempF(addrs1[i]);
      json += "\"";
      if ( i < device_count1 - 1) {
        json += ", ";
      }
    }
    json += ", ";


    //Add data for third run of sensors
    for (int i = 0; i < device_count2; i++) {
      json += "\"";
      for (uint8_t j = 0; j < 8; j++)
      {
        // zero pad the address if necessary
        if (addrs2[i][j] < 16) json += "0" ;
        json += addrs2[i][j];
      }
      json += "\"";

      json += " : ";
      json += "\"";
      json += sensors2.getTempF(addrs2[i]);
      json += "\"";
      if ( i < device_count2 - 1) {
        json += ", ";
      }
    }
    json += ", ";


    //Add data for forth run of sensors
    for (int i = 0; i < device_count3; i++) {
      json += "\"";
      for (uint8_t j = 0; j < 8; j++)
      {
        // zero pad the address if necessary
        if (addrs3[i][j] < 16) json += "0" ;
        json += addrs3[i][j];
      }
      json += "\"";

      json += " : ";
      json += "\"";
      json += sensors3.getTempF(addrs3[i]);
      json += "\"";
      if ( i < device_count3 - 1) {
        json += ", ";
      }
    }

    //CLOSE JSON
    json += "}";

    //Serial.print(sensors.getTempF(a));

    Serial.println(json);
  }
}

void getInput() {
  bool headFound = false;
  if (Serial.available() > 0) {
    String msg = String(Serial.readString());
    String head = msg.substring(1, 4);
    long value = msg.substring(5, 10).toInt();
    //Serial.print(head); Serial.print("   "); Serial.println(value);

    if (head == "tim") {
      ms_between_reads = value;
      //Serial.println(ms_between_reads);
    }
    if (head == "rst") {
      // Rediscover the network
      total_device_count = 0;
      device_count = discoverNetwork(sensors, addrs, device_count);
      device_count1 = discoverNetwork(sensors1, addrs1, device_count1);
      device_count2 = discoverNetwork(sensors2, addrs2, device_count2);
      device_count3 = discoverNetwork(sensors3, addrs3, device_count3);
      total_device_count += device_count + device_count1 + device_count2 + device_count3;
      Serial.print("Total number of devices on network: ");
      Serial.println(total_device_count);
    }
    //Serial.println(ms_between_reads);
  }
}


// function to print a device address
void printAddress(DeviceAddress deviceAddress)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    // zero pad the address if necessary
    if (deviceAddress[i] < 16) Serial.print("0");
    Serial.print(deviceAddress[i], HEX);
  }
}

// Function to discover network size and sensor adresses
int discoverNetwork(DallasTemperature sense, DeviceAddress address_array[], int dev_count) {

  DeviceAddress this_add;

  // Find network size
  Serial.print("Number of sensors found on lane: ");
  dev_count = sense.getDeviceCount();
  Serial.println(dev_count);
  delay(50);

  // Find adresses for all sensoprs in the network and add them to a gloabal list
  Serial.println("Getting Device Adresses...");

  for (int i = 0; i < dev_count; i++) {
    sense.getAddress(this_add, i);

    // Copy array of 8 bytes representing address to sensor address array
    memcpy(address_array[i], this_add, sizeof(address_array[i]));

    printAddress(this_add);
    Serial.println();
  }
  Serial.println("All Adresses Found");
  return dev_count;
}