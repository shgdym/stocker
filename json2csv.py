import pandas as pd

def updateList():
    from SnowBallSpider import SnowBallSpider
    ObjSpider = SnowBallSpider()
    jsonData = ObjSpider.getDSZResult()
    dataframe = pd.DataFrame(jsonData)
    dataframe.to_csv("dsz.csv", index=False, sep=',', encoding="utf_8_sig")
