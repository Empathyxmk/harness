#include <gtest/gtest.h>
#include <memory>
#include <string>
#include <sstream>
#include <iostream>
#include <map>

// Stub implementations for translation. Replace with actual implementation as needed.
class CarModel {
  public:
    std::string model_name;
    bool air;
    bool alloy_wheels;
    bool tilt;
    bool power_locks;
    static std::map<std::string, CarModel*> models;

    CarModel(std::string model_name, bool air=false, bool alloy_wheels=false, bool tilt=false, bool power_locks=false)
      : model_name(model_name), air(air), alloy_wheels(alloy_wheels), tilt(tilt), power_locks(power_locks)
    {
      if (models.find(model_name) == models.end()) {
        models[model_name] = this;
      }
      *this = *models[model_name];
    }
    static void Clear() {
      for (auto it: models) {
        if (it.second) delete it.second;
      }
      models.clear();
    }
    void check_serial(const std::string& s) const {
      std::cout << "Checking serial " << s << " for model " << model_name << "\n";
    }
};
std::map<std::string, CarModel*> CarModel::models;

class Car {
  public:
    CarModel* model;
    std::string color;
    int serial;
    Car(CarModel* m, std::string color, int serial)
      : model(m), color(color), serial(serial) { }
    void check_serial() const {
      model->check_serial(std::to_string(serial));
    }
};

class CaptureStdout {
    std::streambuf* oldbuf;
    std::ostringstream ss;
public:
    CaptureStdout() { oldbuf = std::cout.rdbuf(ss.rdbuf()); }
    ~CaptureStdout() { std::cout.rdbuf(oldbuf); }
    std::string str() { return ss.str(); }
};

TEST(CarFlyweight, CarModelSingletonBehavior) {
    CarModel::Clear(); // Ensure test isolation
    CarModel m1("Sedan", true);
    CarModel m2("Sedan", false);
    EXPECT_EQ(&m1, &m2);
    EXPECT_EQ(m1.model_name, "Sedan");
    EXPECT_TRUE(m1.air);
    EXPECT_FALSE(m1.alloy_wheels);
    CarModel m3("Coupé", false, false, true);
    EXPECT_NE(&m3, &m1);
    EXPECT_TRUE(m3.tilt);
    EXPECT_FALSE(m3.air);
    CarModel::Clear();
}

TEST(CarFlyweight, CarModelCheckSerialOutput) {
    CarModel::Clear();
    CarModel m("X", false, false, false, true);
    CaptureStdout cap;
    m.check_serial("XYZ-123");
    std::string out = cap.str();
    EXPECT_NE(out.find("XYZ-123"), std::string::npos);
    EXPECT_NE(out.find("X"), std::string::npos);
    CarModel::Clear();
}

TEST(CarFlyweight, CarCheckSerialDelegates) {
    CarModel::Clear();
    CarModel m("TestModel");
    Car c(&m, "Red", 555);
    CaptureStdout cap;
    c.check_serial();
    std::string out = cap.str();
    EXPECT_NE(out.find("555"), std::string::npos);
    CarModel::Clear();
}

TEST(CarFlyweight, CarAttributes) {
    CarModel::Clear();
    CarModel m("Z");
    Car c(&m, "Blue", 999);
    EXPECT_EQ(c.model, &m);
    EXPECT_EQ(c.color, "Blue");
    EXPECT_EQ(c.serial, 999);
    CarModel::Clear();
}