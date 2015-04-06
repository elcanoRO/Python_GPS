#Python Requests 2.6.0: http://docs.python-requests.org/en/latest/
#Python PyModbus 1.2.0: https://github.com/bashwork/pymodbus
#Python version  2.7.9
#Other resources:
#http://code.activestate.com/recipes/577122-transform-command-line-arguments-to-args-and-kwarg/
#http://www.scotttorborg.com/python-packaging/dependencies.html
#https://docs.python.org/2/library/struct.html

#from pymodbus.constants import Endian
#from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from struct import pack, unpack
import requests, sys, getopt, time

def takeFromModbusPutonDataDrop(dataDropID, IP_address, IP_port= 502, nr_of_conseq_floats= 4, start_reg_address= 0, delayMin= 1):
    payload = {'bin': dataDropID}
    for index_address in range(start_reg_address, (start_reg_address+ nr_of_conseq_floats)):
        with ModbusClient(host= IP_address, port= IP_port) as client:
            #take data from Modbus register
            result = client.read_holding_registers(2* index_address, 2)
            #convert the two registers to float, multiple of 2
            convertedFloat= unpack('f', pack('HH',result.registers[0], result.registers[1]))
            print result.registers, ':', convertedFloat[0]
            #push to payload variable for GET sentance
            payload.update({index_address: convertedFloat[0]})
    return payload

def Modbus2DataDrop(dataDropID, IP_address, IP_port= 502, nr_of_conseq_floats= 4, start_reg_address= 0, delayMin= 1, iterationSteps= 10):   
    for i in range(0, iterationSteps):
            payload= takeFromModbusPutonDataDrop(dataDropID, IP_address, IP_port, nr_of_conseq_floats, start_reg_address, delayMin)
            print("______")
            time.sleep(60* delayMin)
            r= requests.get("https://datadrop.wolframcloud.com/api/v1.0/Add", params= payload)
def Modbus2DataDropWhileTrue( dataDropID, IP_address, IP_port= 502, nr_of_conseq_floats= 4, start_reg_address= 0, delayMin= 1):
    payload = {'bin': dataDropID}
    #make a delay
    while True:
        for index_address in range(start_reg_address, (start_reg_address+ nr_of_conseq_floats)):
            payload= takeFromModbusPutonDataDrop(dataDropID, IP_address, IP_port, nr_of_conseq_floats, start_reg_address, delayMin)
            print("______")
            time.sleep(60* delayMin)
            r= requests.get("https://datadrop.wolframcloud.com/api/v1.0/Add", params= payload)	
            
if __name__ == "__main__":
    exec(''.join(sys.argv[1:])) 
    #C:\Users\lucian_crisan\Downloads>"c:\Python27\python.exe" Modbus2DataDrop.py Modbus2DataDrop('3YrZOnA5', '10.97.98.250', delayMin= 2)["Modbus2DataDrop('3YrZOnA5',", "'10.97.98.250',", 'delayMin=', '2)']
           
