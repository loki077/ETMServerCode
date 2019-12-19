import socket
import time
import signal
import csv
import sys
import atexit
from datetime import date


def close_socket():
	s.close()

atexit.register(close_socket)
# b'#7,1,PowerCoreTestUnit1,5308,101903,,,,,0,0,,\r\n'


class DataPacket7:
	SendEvent = 0
	UnitID = ""
	SendDay = ""
	SendTime = ""
	Ch1 = ""
	Ch2 = ""
	Ch3 = ""
	Ch4 = ""
	Ch5 = ""
	Ch6 = ""
	Ch7 = ""

	def __init__ (self):
		self.SendEvent = 0
		self.UnitID = ""
		self.SendDay = ""
		self.SendTime = ""
		self.Ch1 = ""
		self.Ch2 = ""
		self.Ch3 = ""
		self.Ch4 = ""
		self.Ch5 = ""
		self.Ch6 = ""
		self.Ch7 = ""

	def inputData(self, tempList):
		if len(tempList) > 11:
			self.SendEvent = tempList[1]
			self.UnitID = tempList[2]
			self.SendDay = tempList[3]
			self.SendTime = tempList[4]
			self.Ch1 = tempList[5]
			self.Ch2 = tempList[6]
			self.Ch3 = tempList[7]
			self.Ch4 = tempList[8]
			self.Ch5 = tempList[9]
			self.Ch6 = tempList[10]
			self.Ch7 = tempList[11]
		# ['7', '1', 'Device9', '10', '082500', '0', '0', '0', '0', '0', '0', '0']

	def print_data(self):
		print("> Data : ", self.UnitID, self.SendDay, self.SendTime, self.Ch5, self.Ch6)
	#7,1,Device'+ str(x) +',10,082500,0,0,0,0,0,0,0'

class DataBase:
	dataPack7 = DataPacket7()
	dataBaseList = []
	UnitID = ""

	def __init__ (self, tempId):
		self.dataBaseList = []
		self.UnitID = tempId

	def add_data(self, tempData):
		self.dataBaseList.append(tempData)

	def fetch_list(self, index):
		tempList = []
		tempList.append(index)
		tempList.append(self.dataBaseList[index].SendDay)
		tempList.append(self.dataBaseList[index].SendTime)
		tempList.append(self.dataBaseList[index].UnitID)
		tempList.append(self.dataBaseList[index].Ch1)
		tempList.append(self.dataBaseList[index].Ch2)
		tempList.append(self.dataBaseList[index].Ch3)
		tempList.append(self.dataBaseList[index].Ch4)
		tempList.append(self.dataBaseList[index].Ch5)
		tempList.append(self.dataBaseList[index].Ch6)
		tempList.append(self.dataBaseList[index].Ch7)

		return tempList
		
	def print_data(self):
		# print("dataBase Len" , len(self.dataBaseList))
		for x in self.dataBaseList:
			x.print_data()

	def clear_data(self):
		self.dataBaseList = []
		del self.dataBaseList[:]

	def length(self):
		return len(self.dataBaseList)


HOST = '0.0.0.0' #Standard loopback interface address (localhost)
PORT = 2020 # Port to listen on (non-privileged port are > 1023)

counter 	 = 0
tempResponse = ""

deviceID 	 = []
dataBaseList = []

preDate 	= date.today()
namedTuple 	= time.time() # get struct_time
preTime 	= namedTuple
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(time.time())

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s.bind((HOST, PORT))
s.listen()
s.settimeout(1)

while True:
	namedTuple = time.time() # get struct_time
	currentTime = namedTuple
	currentDate = date.today()
	try:
		conn, addr = s.accept()
		print('Connected by', addr)
		data = conn.recv(1024)
		tempResponse = tempResponse + str(data)
		
	except Exception as e:
		pass
		# print(".")

	finally:
		if tempResponse:
			tempResponse = tempResponse.replace('\'b\'','')
			tempResponse = tempResponse.replace('\'','')
			tempResponse = tempResponse.replace('\\r','')
			tempResponse = tempResponse.replace('\\n','')
			dataList = []
			dataList = tempResponse.split('#')
			tempResponse = ""
			for x in dataList:
				if len(x) > 20:
					finalOut = x.split(",")
					for x in range(0, len(finalOut)):
						if finalOut[x] == "":
							finalOut[x] = "0"

					datapack = DataPacket7()
					print(finalOut)
					datapack.inputData(finalOut)
					datapack.print_data()
					if datapack.UnitID not in deviceID:
						print("**************Creating a New :", datapack.UnitID, "**************")
						deviceID.append(datapack.UnitID)
						dataBaseList.append(DataBase(datapack.UnitID))
					index = deviceID.index(datapack.UnitID)
					print("Storing in Device ", index)
					dataBaseList[index].add_data(datapack)

		if( currentTime - preTime  > 3600):
			print("**************Start Ceating File**************")
			for x in dataBaseList:
				if(x.length() > 0):
					try:						
						fileName =  str(x.UnitID)+"_"+str(preDate)+"_"+ str(currentTime) +'.csv'
						# fileName =  str(currentTime) + str(x.UnitID) +'.csv'
						print("Ceating File : ", fileName)
						with open(fileName , 'w', newline='') as file:
							writer = csv.writer(file)
							writer.writerow(["No", "Date","time", "DeviceName", "Value1", "Value2", "Value3", "Value4", "Value5", "Value6", "Value7" ])
							for z in range(0, x.length()):
								writer.writerow(x.fetch_list(z))
					except Exception as e:
						print("File creation error: " + str(msg))
				x.clear_data()
			dataBaseList = []
			deviceID = []
			del deviceID[:]
			del dataBaseList[:]
			preDate = currentDate
			preTime = currentTime
			print("*************Stop Ceating File**************")