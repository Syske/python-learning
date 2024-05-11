import pyttsx3
engine = pyttsx3.init() #初始化语音引擎

engine.setProperty('rate', 100)   #设置语速
engine.setProperty('volume',0.6)  #设置音量
voices = engine.getProperty('voices') 
engine.setProperty('voice',voices[0].id)   #设置第一个语音合成器
engine.say("春光灿烂猪八戒")
engine.runAndWait()
engine.stop()