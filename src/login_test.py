# coding: utf-8

import pywinauto
import time
import win32com.client

print(pywinauto.__version__)

# 비번
name = '아이디'
pw = '비밀번호'
cert = '공인인증서 비밀번호'

def login(name=name, pw=pw, cert=cert):

	'''
	# 파일에서 비번들 로드할경우
	with open('./ignores/pw.txt') as f:
	    itms = list(f.readlines())
	    pw = itms[0].strip()
	    cert = itms[1].strip()
	'''

	# 어플리케이션 실행
	app = pywinauto.Application()
	app.start('C:\\CREON\\STARTER\\coStarter.exe /prj:cp /id:'+name+' /pwd:'+pw+' /pwdcert:'+cert+' /autostart')
	print("Program Initiated...")

	# 업데이트 대기
	print("Waiting for program updates...")
	time.sleep(20)

	# 공지사항 창 끄기
	appp = pywinauto.Application(backend='uia')
	def connect_to_appp(appp=appp):
		appp.connect(path="C:\\Daishin\\CYBOSPLUS\\CpStart.exe")

	pywinauto.timings.wait_until_passes(60, 1, connect_to_appp)

	notice = appp.top_window()
	notice.Button3.click()
	print("Closed Notice Popup")

	print("Logged into CreonPlus Successfully")

	return appp

def logout():
	#Creon Plus 종료
	
	objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
	objCpCybos.PlusDisconnect()

	appp = pywinauto.Application(backend='uia')
	def connect_to_appp(appp=appp):
		appp.connect(path="C:\\Daishin\\CYBOSPLUS\\CpStart.exe")
	pywinauto.timings.wait_until_passes(60, 1, connect_to_appp)
	appp.kill()

	print("Exit Program")

	return

if __name__ == "__main__":
	login(name, pw, cert)
	logout()