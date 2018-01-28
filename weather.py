import sys
import os
import requests
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

class YahooWeather: 

    def get(self, city): # get current weather through Yahoo API
        url = 'https://query.yahooapis.com/v1/public/yql?q=select%20item.condition%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22' + city + '%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
        data = requests.get(url).json()
        if data["query"]["results"]==None:
            print "There is no info for such city!"
            sys.exit()
        condition_data = data["query"]["results"]["channel"]["item"]["condition"]
        condition={}
        condition['date']=(condition_data['date'])
        condition['temp']=self.to_celsius(int(condition_data['temp']))
        condition['text']=condition_data['text']
        condition['code']=int(condition_data['code'])
        
        return condition
    
    def to_celsius(self, temp):  # go to celsius from fahrenheits
        return int((temp-32)*5./9)
    
    
class CityInfo:

    def __init__(self, city):
        self.city = city.lower()
        self.weather_provider = YahooWeather()
        
    def weather(self):
        return self.weather_provider.get(self.city)

    def pic_print(self, code): # print weather icon
        pic_filename = '%s.png' % (str(code))
        pic_path = "weather_icons\\" + pic_filename
        ''' %pylab inline
        img=mpimg.imread(pic_path)
        imgplot = plt.imshow(img)
        plt.show()'''
        os.system(pic_path)



    def fine_print(self): # final printing: weather conditions and weather icon
        weather = self.weather()
        print "\nCurrent weather in %s is as follows:\n" % (self.city)
        print "It is %s \n" % (weather['text'])
        print "The temperature is %dC degrees\n" % (weather['temp'])
        self.pic_print(weather['code'])

            
def _main():    
    if len(sys.argv)==1:
        c='moscow'
    else: c=sys.argv[1]
    city = CityInfo(c)
    city.fine_print()
    
    
if __name__ == "__main__":
    _main()