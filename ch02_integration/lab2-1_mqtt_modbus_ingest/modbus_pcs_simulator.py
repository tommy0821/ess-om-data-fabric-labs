"""PCS 역할을 하는 Modbus TCP 시뮬레이터. 레지스터에 전압/전류/온도 값을 넣어두고 응답한다."""
from pymodbus.server import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext,
)

# 레지스터: [전압*10, 전류, 온도*10] = [3800, 0, 280] -> 380.0V, 0A, 28.0°C
store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [3800, 0, 280]))
context = ModbusServerContext(slaves=store, single=True)

if __name__ == "__main__":
    StartTcpServer(context=context, address=("localhost", 5020))
