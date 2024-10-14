from machine import I2C
import time

# MPU6050 I2C address
MPU6050_ADDR = 0x68

# MPU6050 Registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
TEMP_OUT_H = 0x41
GYRO_XOUT_H = 0x43

class MPU6050:
    def __init__(self, i2c, address=MPU6050_ADDR):
        self.i2c = i2c
        self.address = address
        # Wake up MPU6050 as it's in sleep mode initially
        self.i2c.writeto_mem(self.address, PWR_MGMT_1, b'\x00')

    def read_raw_data(self, reg):
        high = self.i2c.readfrom_mem(self.address, reg, 1)
        low = self.i2c.readfrom_mem(self.address, reg+1, 1)
        value = (high[0] << 8) | low[0]
        if value > 32768:
            value = value - 65536
        return value

    def get_accel(self):
        ax = self.read_raw_data(ACCEL_XOUT_H) / 16384.0
        ay = self.read_raw_data(ACCEL_XOUT_H + 2) / 16384.0
        az = self.read_raw_data(ACCEL_XOUT_H + 4) / 16384.0
        return ax, ay, az

    def get_gyro(self):
        gx = self.read_raw_data(GYRO_XOUT_H) / 131.0
        gy = self.read_raw_data(GYRO_XOUT_H + 2) / 131.0
        gz = self.read_raw_data(GYRO_XOUT_H + 4) / 131.0
        return gx, gy, gz

    def get_temp(self):
        temp = self.read_raw_data(TEMP_OUT_H)
        return temp / 340.0 + 36.53
