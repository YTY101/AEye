#include "USB.h"
#include "USBHIDMouse.h"

USBHIDMouse Mouse;

String inputString = "";
bool stringComplete = false;

void setup() {
  Serial.begin(115200);
  USB.begin();
  Mouse.begin();
}

void loop() {
  if (stringComplete) {
    inputString.trim();  // 去掉空格和换行

    // 解析格式：例如 "30,-10"
    int commaIndex = inputString.indexOf(',');
    if (commaIndex != -1) {
      String xStr = inputString.substring(0, commaIndex);
      String yStr = inputString.substring(commaIndex + 1);
      if (xStr == "x" && yStr == "x") {
        Mouse.click(MOUSE_LEFT);
        Serial.print("Mouse clicked left");
      } else {
        int dx = xStr.toInt();
        int dy = yStr.toInt();

        // 执行鼠标移动
        Mouse.move(dx, dy);

        // 打印移动的距离
        Serial.print("Mouse moved: dx = ");
        Serial.print(dx);
        Serial.print(", dy = ");
        Serial.println(dy);
      }  
        
    }

    inputString = "";
    stringComplete = false;
  }

  // 串口读取数据
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}
