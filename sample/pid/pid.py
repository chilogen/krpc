import krpc,time

class PID:
	def __init__(self):
		
		self.error1=0
		self.error2=0
		self.error3=0

		self.setValue=0
		self.oldValue=0

		self.pp=0.005
		self.ii=100000
		self.dd=0.02
		self.samplingTime=0.01

		self.kp=self.pp
		self.ki=self.samplingTime/self.ii
		self.kd=self.dd/self.samplingTime

	def set(self,value):
		self.setValue=value

	def process(self,paramer,getFun,setFun):
		while True:
			time.sleep(self.samplingTime)
			cur=getFun(paramer)
			error=self.setValue-cur
			self.error1= self.error2
			self.error2=self.error3
			self.error3=error
			delta=self.kp*(self.error3-self.error2)+self.ki*(self.error3)+self.kd*(self.error3-2*self.error2+self.error1)
			print(self.oldValue,delta,cur)
			if(self.oldValue>=0 and delta<0):
				self.oldValue=self.oldValue+delta
			if(self.oldValue<=1 and delta>0):
				self.oldValue=self.oldValue+delta
			setFun(paramer,self.oldValue)

def initkrpc():
	connection=krpc.connect()
	vessel=connection.space_center.active_vessel
	flight=vessel.flight()
	vessel.auto_pilot.target_pitch_and_heading(90, 90)
	vessel.auto_pilot.engage()
	paramer={}
	paramer['connection']=connection
	paramer['vessel']=vessel
	paramer['flight']=flight
	vessel.control.activate_next_stage()
	return paramer

def getCurrentHeight(paramer):
	return paramer['flight'].bedrock_altitude
	

def setThrustLimit(paramer,val):
	paramer['vessel'].control.throttle=val

if __name__ == '__main__':
	pidControler=PID()
	pidControler.set(float(input("Enter init height: ")))
	para=initkrpc()
	pidControler.process(para,getCurrentHeight,setThrustLimit)